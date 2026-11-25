"""Bornes de hauteur et efforts sur les maillages du modèle Fusion.
Exécution requise depuis la racine du projet avec NumPy et SciPy.
"""
import gzip
import json
import math
from pathlib import Path

import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation

PROOF = Path("docs/diagnostic/corrections")
G = 9.80665
DIGITS = "PIMAU"
AUX = {"P1M": ("J1", -22/38), "P2M":("J2",-3), "P3M":("J3",-2)}


def load(name):
    return json.loads((PROOF/name).read_text(encoding="utf-8"))


def transforms(raw):
    transform = np.array(raw).reshape(4,4).copy()
    transform[:3,3] *= 10.0
    return transform


def hull(data):
    if len(data) <= 4:
        return data
    points = np.unique(np.round(data, 6),axis=0)
    index = ConvexHull(points, qhull_options="QJ").vertices
    return points[index]


class Model:
    def __init__(self):
        data = load("geometrie_neutre.json")
        self.parts,self.joints = data["parts"],data["joints"]
        self.cal=json.loads(data["attributes"]["Calibration"])
        self.flex=json.loads(data["attributes"]["Flexions"])
        self.plan=json.loads(data["attributes"]["PlanDeTravail"])
        self.spring=json.loads(data["attributes"].get("Compensation","{}"))
        self.tol=data["mesh_tolerance_mm"]
        self.poses={k:transforms(p["transform"]) for k,p in self.parts.items()}
        self.child = {v["child"]:k for k,v in self.joints.items()}
        self.chain = {}
        for key in self.parts:
            path=[]
            parent=key
            while parent:
                if parent in self.child:
                    path.append(self.child[parent])
                parent=self.parts[parent]["parent"]
            self.chain[key]=path[::-1]
        with gzip.open(PROOF/"maillages_natifs.json.gz","rt",encoding="utf-8") as f:
            entries=json.load(f)
        self.vertices={}
        for part in entries:
            k=part["part"]
            raw=np.asarray(part["v"])
            world=raw @ self.poses[k][:3,:3].T + self.poses[k][:3,3]
            self.vertices.setdefault(k,[]).append(world)
        self.vertices={k:hull(np.concatenate(v)) for k,v in self.vertices.items()}

    def angle(self, key, q):
        if key in AUX:
            a,r=AUX[key]
            return q.get(a,0.0)*r
        if key in self.flex:
            return q.get("Servo_"+key[0],0.0)*self.flex[key]/92
        return q.get(key,0.0)

    def transform_joint(self,key,q):
        joint=self.joints[key]
        origin=np.array(joint["pivot_mm"])
        rotation=Rotation.from_rotvec(np.asarray(joint["axis"])*math.radians(q*self.cal[key][1])).as_matrix()
        m=np.eye(4)
        m[:3,:3]=rotation
        m[:3,3]=origin-rotation@origin
        return m

    def matrices(self,q):
        angles={k:self.transform_joint(k,self.angle(k,q)) for k in self.joints}
        cache={():np.eye(4)}
        def for_chain(path):
            if path not in cache:
                cache[path]=for_chain(path[:-1])@angles[path[-1]]
            return cache[path]
        return {k:for_chain(tuple(chain)) for k,chain in self.chain.items()}


def apply(t, points):
    return np.asarray(points) @ t[:3,:3].T + t[:3,3]


def crosscheck(m, cases):
    result=[]
    for c in cases:
        if not c.get("transform"):
            continue
        angles=c["target"]
        current=m.matrices(angles)
        errors={}
        for k,native in c["transform"].items():
            a=current[k]@m.poses[k]
            b=transforms(native)
            mount=np.linalg.norm(a[:3,3]-b[:3,3])
            direction=np.linalg.norm(a[:3,:3]-b[:3,:3])
            errors[k]=max(mount, direction*50)
        worst=max(errors,key=errors.get)
        result.append({"pose":c["label"],"part":worst,"error_mm":errors[worst]})
    return result


def grid(low,hi,dx):
    return np.linspace(low,hi,math.ceil((hi-low)/dx)+1)


def swept(m,cloud,axis,values):
    return hull(np.concatenate([apply(m.transform_joint(axis,v),cloud) for v in values]))


def rigid_groups(m,pitch_limits):
    groups={k:[] for k in ["fixed","J2","J3","J7"]}
    servo_clouds={k:[] for k in DIGITS}
    servo_radii={k:0.0 for k in DIGITS}
    for k,cloud in m.vertices.items():
        body=m.parts[k]
        if body["flexible"] or k.startswith("Tendon_"):
            continue
        chain=m.chain[k]
        group=next((j for j in ("J7","J3","J2") if j in chain),"fixed")
        finger=[j for j in chain if j in m.flex]
        if finger:
            digit=finger[0][0]
            for q in grid(0,92,1.0):
                current=np.eye(4)
                for j in finger:
                    current=current@m.transform_joint(j,q*m.flex[j]/92)
                servo_clouds[digit].append(apply(current,cloud))
            # Chaque rayon est borné par les distances entre pivots et la longueur
            # maximale entre le dernier pivot et un sommet, quelle que soit la flexion.
            pivots=np.array([m.joints[j]["pivot_mm"] for j in finger])
            lengths=np.linalg.norm(np.diff(pivots,axis=0),axis=1)
            radius=max(np.linalg.norm(cloud-pivots[-1],axis=1))
            derivative=sum((sum(lengths[i:])+radius)*m.flex[j]/92 for i,j in enumerate(finger))
            servo_radii[digit]=max(servo_radii[digit],derivative)
            continue
        active=next((j for j in chain if j in AUX or j.startswith("Servo_")),None)
        if active:
            bound = 92 if active.startswith("Servo_") else pitch_limits[AUX[active][0]]*abs(AUX[active][1])
            if active in AUX:
                values=grid(-bound,bound,1.0)
            else:
                values=grid(0,bound,1.0)
            cloud=swept(m,cloud,active,values)
            # Enveloppe de rotation conservatrice de tout sommet entre deux stations.
            centre=np.array(m.joints[active]["pivot_mm"])
            radial=max(np.linalg.norm(cloud-centre,axis=1))
            cloud=np.concatenate([cloud+[0,0,delta] for delta in (-math.radians(.5)*radial,math.radians(.5)*radial)])
        groups[group].append(cloud)
    for digit,arrays in servo_clouds.items():
        groups["J7"].append(hull(np.concatenate(arrays)))
    return {k:hull(np.concatenate(v)) for k,v in groups.items()},max(servo_radii.values())


def table(m,q2,q3,coupled=False,q7=32):
    clouds, finger_r=rigid_groups(m,{"J1":94,"J2":q2,"J3":q3})
    wrist=swept(m,clouds["J7"],"J7",grid(-q7,q7,1.0))
    fore=hull(np.concatenate([wrist,clouds["J3"]]))
    poses=[apply(m.transform_joint("J3",b),fore) for b in grid(-q3,q3,.5)]
    arm=clouds["J2"]
    arms=[hull(np.concatenate([a,arm])) for a in poses]
    z_min=math.inf
    worst=None
    for a in grid(-q2,q2,.5):
        t=m.transform_joint("J2",a)
        for v,b in zip(arms,grid(-q3,q3,.5)):
            if coupled and a + .6*b < -36.4:
                continue
            z=float((v@t[2,:3]+t[2,3]).min())
            if z<z_min:
                z_min,worst=z,(float(a),float(b))
    origin={k:np.array(m.joints[k]["pivot_mm"]) for k in ("J2","J3","J7")}
    wrist_r=max(np.linalg.norm(clouds["J7"]-origin["J7"],axis=1))
    j3_r=max(max(np.linalg.norm(clouds["J3"]-origin["J3"],axis=1)),
             np.linalg.norm(origin["J7"]-origin["J3"])+wrist_r)
    j2_r=max(max(np.linalg.norm(arm-origin["J2"],axis=1)),
             np.linalg.norm(origin["J3"]-origin["J2"])+j3_r)
    error=m.tol+.15+math.radians(.5)*(finger_r+wrist_r)+math.radians(.25)*(j3_r+j2_r)
    return {"limits_deg":[q2,q3,q7],"coupled":coupled,"min_sample_mm":z_min,"worst":worst,
            "tolerance_and_lipschitz_mm":error,"conservative_min_z_mm":z_min-error,
            "table_z_mm":m.plan["plan_table_mm"],"clearance_lower_bound_mm":z_min-error-m.plan["plan_table_mm"]}


def mass(p,k,fill):
    if p["print_ref"]:
        return .00127*fill*p["volume_mm3"]
    if not p["com_mm"]:
        return 0.0
    if k in ("Moteur_J2","Moteur_J3"):
        return 55.0
    if k.startswith("Moteur_"):
        return 9.0
    if k.startswith("R6000_"):
        return 19.4
    if k=="Pico":
        return 3.5
    if k=="Distribution_5V":
        return 55.0
    if k.startswith("Ressort_"):
        return 4 if k.endswith("J2") else 3
    if p["flexible"] or k.startswith("Tendon_"):
        return .00058*p["volume_mm3"]
    if "Palonnier" in k:
        return .0013*p["volume_mm3"]
    return .00785*p["volume_mm3"]


def dynamics(m,cases):
    keys=[k for k in m.parts if m.parts[k]["com_mm"]]
    load_tip=m.vertices["M3"][np.argmax(m.vertices["M3"][:,0])]
    solutions=[]
    for fill,load_g in ((1.0,0),(1.0,10),(1.0,20),(.6,0),(.6,20)):
        weights=np.array([mass(m.parts[k],k,fill) for k in keys])/1000
        out={"fill_mass_fraction":fill,"payload_g":load_g,"total_mass_g":float(weights.sum()*1000)}
        parameters={k:[] for k in ("J2","J3")}
        stability=[]
        for case in cases:
            if case["error_deg"]>.02:
                continue
            q=case["target"]
            by_part=m.matrices(q)
            com=np.array([apply(by_part[k],m.parts[k]["com_mm"]) for k in keys])/1000
            payload=apply(by_part["M3"],load_tip)/1000
            support=(weights@com + load_g / 1000 * payload)/(weights.sum()+load_g/1000)
            moment_arm=min(support[0]+.061,.068-support[0],support[1]+.047,.047-support[1])
            stability.append((float(moment_arm*1000),float(support[2]*1000)))
            for axis in ("J2","J3"):
                joint=m.joints[axis]
                base=by_part[joint["parent"]]
                anchor=apply(base,joint["pivot_mm"])/1000
                line=base[:3,:3]@np.asarray(joint["axis"])
                mask=np.array([axis in m.chain[k] for k in keys])
                rw=np.r_[weights[mask],load_g/1000]
                positions=np.vstack([com[mask],payload])-anchor
                gravity=-float(rw@np.dot(np.cross(positions,[0,0,-G]),line))
                spring=case.get("passages",{}).get("Ressort_"+axis,{}).get("torque_nm",0)
                static=abs(gravity-spring)+.12*abs(spring)
                inertia=float(rw @ np.sum(np.cross(positions,line)**2,axis=1))
                alpha=math.radians(35 if axis=="J2" else 50)
                friction=.10 if axis=="J2" else .07
                parameters[axis].append([gravity,spring,static,static+inertia*alpha+friction+.01])
        out["axes"]={k:{name:float(np.max(np.array(v)[:,i])) for i,name in
                        enumerate(("gravity_nm","spring_nm","residual_static_with_tolerance_nm","dynamic_nm"))}
                     for k,v in parameters.items()}
        out["anchor_margin_mm"]=min(stability)[0]
        out["com_max_z_from_table_mm"]=max(x[1] for x in stability)-m.plan["plan_table_mm"]
        solutions.append(out)
    return solutions


def main():
    model=Model()
    p=PROOF/"poses_reperes.json"
    cases=load(p.name) if p.exists() else load("precontrole.json")
    cross=crosscheck(model,cases)
    if cross and max(r["error_mm"] for r in cross)>.2:
        raise SystemExit("La FK analytique diverge des repères Fusion.")
    data={"fk_crosscheck":cross,
          "table":[table(model,26,36),table(model,22.2,33.3,q7=180),table(model,21,32,True,q7=30)],
          "mass_print_petg_solid_g":sum(mass(p,k,1.0) for k,p in model.parts.items() if p["print_ref"]),
          "loads":dynamics(model,cases+(load("campagne_fusion.json") if (PROOF/"campagne_fusion.json").exists() else []))}
    (PROOF/"calculs.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(data,ensure_ascii=False))



def fallback_poses():
    model=Model()
    failed = {}
    for record in load("campagne_fusion.json"):
        if record["error_deg"]>.02:
            key=tuple(record["target"].items())
            failed.setdefault(key,[]).append(record["source_case"])
    rows=[]
    for target, source in failed.items():
        q=dict(target)
        for tag,case in (("historique",q),("enveloppe_commande",q|{"J7":math.copysign(30,q["J7"])})):
            relative={}
            for key,t in model.matrices(case).items():
                native=t.copy()
                native[:3,3]/=10
                relative[key]=native.ravel().tolist()
            rows.append({"cases":source,"label":tag,"target":case,"relative":relative})
    p=PROOF/"poses_calcul_independant.json"
    p.write_text(json.dumps(rows,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")


if __name__=="__main__":
    main()
    fallback_poses()
