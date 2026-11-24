"""Vérifications du document natif AURA-009 table r03."""

import json
from itertools import product
import math
from pathlib import Path

import adsk.core as core
import adsk.fusion as fusion

from construire_montage import Workshop, get_design
from faisceau_table_r03 import OLD, transform
from formes_table_r03 import (
    ANCHOR_X, ANCHOR_Y, Geometry, J2_LIMITS, J3_LIMITS, J7_LIMITS,
    J2_STOPS, J3_STOPS,
)
from geometrie import point, vector

OUT=Path(__file__).resolve().parent
HOME=(0,0,0,0,0)
MAIN_JOINTS={"J1":"03_Tourelle","J2":"04_Segment_1","J3":"05_Segment_2",
             "J7":"07_Paume","T1":"10_Tambour"}


class ExistingTable(Workshop):
    def __init__(self, doc):
        self.doc=doc
        self.design=get_design(doc)
        self.root=self.design.rootComponent
        attrs=self.root.attributes
        assert attrs.itemByName("AURA-01","Reference").value.endswith("r03")
        self.calibration=json.loads(attrs.itemByName("AURA-01","Calibration").value)
        self.flexion=json.loads(attrs.itemByName("AURA-01","Flexions").value)
        self.slider_zero=json.loads(attrs.itemByName("AURA-01","Traverse").value)
        self.occ,self.prints,self.print_groups,self.stage,self.joints={},{},{},{},{}
        self.native_links=self.root.motionLinks.count==16
        self.forms=object.__new__(Geometry)
        self.forms.design=self.design
        self.forms.manager=fusion.TemporaryBRepManager.get()
        for occ in self.root.occurrences:
            comp=occ.component
            code=comp.attributes.itemByName("AURA-01","Repere").value
            self.occ[code]=occ
            group=comp.attributes.itemByName("AURA-01","Impression")
            if group:
                self.prints[code]=(occ,"FDM · "+code,0)
                self.print_groups[code]=group.value
            parent=comp.attributes.itemByName("AURA-01","Parent")
            if parent:
                self.stage[code]=parent.value
        self.stage["11_Palonnier"]="07_Paume"
        for joint in self.root.asBuiltJoints:
            short=joint.name.split(" · ")[0]
            if short=="T2":
                self.slider=joint
                continue
            if short in MAIN_JOINTS or short in self.flexion:
                code=MAIN_JOINTS.get(short,short)
                axis="z" if short=="J1" else "x" if short=="J7" else "y"
                self.joints[code]=(joint.jointMotion,axis,None)
        assert len(self.joints)==20
        assert self.slider


def active():
    return ExistingTable(core.Application.get().activeDocument)


def body_key(body):
    occ=body.assemblyContext
    comp=occ.component if occ else body.parentComponent
    tag=comp.attributes.itemByName("AURA-01","Repere") if comp else None
    if tag:
        return tag.value
    if body.name.startswith("["):
        return body.name[1:].split("]",1)[0]
    return body.name.removeprefix("FDM · ")


def interference(design,root,omit_cables=False):
    bins=core.ObjectCollection.create()
    for occ in root.occurrences:
        for body in occ.bRepBodies:
            if not body.name.startswith("Repère de liaison") and not (omit_cables and body.name.startswith("[CAB_")):
                bins.add(body)
    query=design.createInterferenceInput(bins)
    query.areCoincidentFacesIncluded=False
    report=design.analyzeInterference(query)
    if report is None:
        raise RuntimeError("Calcul d'interférences indisponible.")
    raw=[]
    for hit in report:
        a,b=hit.entityOne,hit.entityTwo
        key_a,key_b=body_key(a),body_key(b)
        volume=hit.interferenceBody.volume*1000
        if volume>.006 and key_a!=key_b:
            c=hit.interferenceBody.physicalProperties.centerOfMass
            raw.append({"a":key_a,"b":key_b,"corps":[a.name,b.name],"mm3":round(volume,4),
                        "centre_mm":[round(t*10,3) for t in c.asArray()]})
    return raw


def inspect_in_draft(rig):
    records=interference(rig.design,rig.root)
    print(json.dumps({"repos":len(records),"contacts":records},ensure_ascii=False))


def samples():
    poses=[HOME]
    for axis,(lo,hi) in enumerate(((-18,18),J2_LIMITS,J3_LIMITS,J7_LIMITS)):
        for target in (lo,lo/2,hi/2,hi):
            q=list(HOME)
            q[axis]=target
            poses.append(tuple(q))
    poses.extend((0,0,0,0,f) for f in (.25,.5,.75,1))
    poses.extend(product((-18,18),J2_LIMITS,J3_LIMITS,J7_LIMITS,(0,1)))
    poses.extend(((0,-7,10,20,.4),(0,7,-5,-20,.6),(0,5,5,-24,.25),
                  (0,-5,6,24,.75),(-10,5,7,14,.75),(10,-5,-5,-14,.5)))
    return list(dict.fromkeys(poses))


def shifted(shape, delta, manager):
    moving=manager.copy(shape)
    tx=core.Matrix3D.create()
    tx.translation=vector(tuple(x/10 for x in delta))
    assert manager.transform(moving,tx)
    return moving


def volume_overlap(manager,a,b):
    aa,bb=a.boundingBox,b.boundingBox
    for amin,amax,bmin,bmax in zip(aa.minPoint.asArray(),aa.maxPoint.asArray(),
                                  bb.minPoint.asArray(),bb.maxPoint.asArray()):
        if amin>=bmax or bmin>=amax:
            return 0.
    result=manager.copy(a)
    ok=manager.booleanOperation(result,manager.copy(b),fusion.BooleanTypes.IntersectionBooleanType)
    if not ok:
        # Les boîtes peuvent se recouper sans intersection de solides.
        if result.isValid and not result.faces.count:
            return 0.
        raise RuntimeError("Intersection Fusion refusée sur des boîtes recouvrantes.")
    return result.volume*1000 if result.isSolid else 0.


def cable_manifest(rig):
    attr=rig.root.attributes.itemByName("AURA-01","Faisceau")
    assert attr and not any(code in rig.occ for code in OLD)
    return json.loads(attr.value)


def data_cables(rig,manifest,pivots):
    offsets={}
    for item in manifest["interfaces"]:
        a=transform(item["point_a"],rig.occ[item["a"]].transform2)
        b=transform(item["point_b"],rig.occ[item["b"]].transform2)
        offsets[item["nom"]]=round(math.dist(a,b),8)
    angles={name:round(math.degrees(math.remainder(pivots[name].rotationValue-value,2*math.pi)),5)
            for name,value in manifest["pivots_neutre_rad"].items()}
    return {"ecart_max_mm":max(offsets.values()),"raccords_mm":offsets,"rotation_guides_deg":angles}


def check_mounts_at_home(rig,manifest):
    refs=("01_Platine","03_Tourelle","P11_Garde_J2","ROT_J2",
          "P12_Garde_J3","ROT_J3","13_Bride_Poignet","07_Paume")
    measure=core.Application.get().measureManager
    pairs=[(row["repere"],host) for row,host in zip(manifest["attaches"],refs)]
    pairs.extend((row["collier"],row["host"]) for row in manifest["colliers"])
    records=[]
    for code,host in pairs:
        b=rig.occ[code].bRepBodies.itemByName("FDM · "+code)
        assert b,code
        faces=[x for x in rig.occ[host].bRepBodies if not x.name.startswith("Repère de liaison")]
        gap=round(min(measure.measureMinimumDistance(b,x).value*10 for x in faces),4)
        records.append({"repere":code,"appui":host,"jeu_mm":gap})
    return records


def moments_model(rig):
    bodies=[]
    override={"SERVO_J2":55.0,"SERVO_J3":23.0,"SERVO_T1":13.4,"SERVO_J7":13.4,
              "CTRL":7.0,"TTL":4.0,"BTN":6.0,"CTRL_VISION":3.0,"CORNE_J3":1.6}
    for code,occ in rig.occ.items():
        if code.startswith(("CAB_","PLUG_")):
            continue
        native=[b for b in occ.component.bRepBodies if not b.name.startswith("Repère de liaison")]
        volumes=sum(b.volume for b in native)
        lineage=[code]
        while lineage[-1] in rig.stage:
            lineage.append(rig.stage[lineage[-1]])
        for body in native:
            printed=code in rig.prints and body.name.startswith("FDM · ")
            if code in override:
                mass=override[code]*body.volume/volumes
            else:
                density=(1.27 if printed else
                         1.45 if code.startswith(("PALIER","FIL_")) or "conducteur guidé" in body.name else
                         2.7 if code.startswith("DOG_") or "Entretoise M5" in body.name else 7.85)
                mass=body.volume*density
            pos=body.physicalProperties.centerOfMass.copy()
            bodies.append((code,occ,tuple(lineage),mass,pos,printed))
    return bodies


def pose_loads(rig,parts):
    world=[]
    for code,occ,lineage,mass,pos,printed in parts:
        p=pos.copy()
        p.transformBy(occ.transform2)
        world.append((code,lineage,mass,p,printed))
    tip=point((12.5,0,-1.2))
    tip.transformBy(rig.occ["M3"].transform2)
    # Provision mesurable pour fils, petits écrous et nœuds mobiles.
    reserve=point((25,0,-5))
    reserve.transformBy(rig.occ["07_Paume"].transform2)
    tail=("07_Paume","06_Segment_3","05_Segment_2","04_Segment_1")
    world.append(("QUINCAILLERIE",tail,10.0,reserve,False))
    cases={}
    for label,payload,ballast,fdm in (("vide_sans_lest",0,False,1),("20g_sans_lest",20,False,1),
                                     ("20g_avec_lest",20,True,1),("20g_80pct",20,False,.8)):
        loads=[(stage,mass*(fdm if printed else 1),p) for code,stage,mass,p,printed in world
               if code!="LEST" or ballast]
        if payload:
            loads.append((tail,payload,tip))
        total=sum(mass for _,mass,_ in loads)
        center=[sum(m*p.asArray()[i] for _,m,p in loads)*10/total for i in range(3)]
        dist=min(center[0]-ANCHOR_X[0],ANCHOR_X[1]-center[0],
                 center[1]-ANCHOR_Y[0],ANCHOR_Y[1]-center[1])
        torques={}
        for joint,key in (("J2","04_Segment_1"),("J3","05_Segment_2"),("J7","07_Paume")):
            tx=rig.occ[key].transform2
            pivot=point((0,0,0))
            pivot.transformBy(tx)
            axs=vector((1,0,0) if joint=="J7" else (0,1,0))
            axs.transformBy(tx)
            torque=0.
            inertia=0.
            for stage,mass,p in loads:
                if key not in stage:
                    continue
                arm=pivot.vectorTo(p)
                torque+=arm.crossProduct(vector((0,0,-9.81*mass/1000))).dotProduct(axs)/100
                inertia+=(mass/1000)*(arm.dotProduct(arm)-arm.dotProduct(axs)**2)/10000
            torques[joint]={"gravite_Nm":round(abs(torque),6),
                           "inertie_points_kgm2":round(inertia,8)}
        cases[label]={"masse_g":round(total,3),"centre_mm":[round(x,3) for x in center],
                      "rappel_min_Nm":round(total*9.81*dist/1e6,6),
                      "marge_appui_mm":round(dist,3),"axes":torques}
    return cases


def motion_batch(start,count):
    rig=active()
    out=OUT/"Verification_Mouvements_r03.json"
    states=samples()
    manifest=cable_manifest(rig)
    pivots={j.name:j.jointMotion for j in rig.root.asBuiltJoints if j.name in manifest["pivots_neutre_rad"]}
    if start==0:
        rig.position(HOME)
        value={"fusion":core.Application.get().version,"seuil_mm3":.006,"poses_cible":len(states),
               "cables_volumiques":True,"faisceau":manifest,"appuis_faisceau":check_mounts_at_home(rig,manifest),"poses":[]}
    else:
        value=json.loads(out.read_text(encoding="utf8"))
        if len(value["poses"])!=start or value["faisceau"]!=manifest:
            raise RuntimeError("Lot de contrôle incohérent.")
    parts=moments_model(rig)
    try:
        for pose in states[start:start+count]:
            rig.position(pose)
            hit=interference(rig.design,rig.root)
            value["poses"].append({"pose":pose,"interferences":hit,
                "cables":data_cables(rig,manifest,pivots),"statique":pose_loads(rig,parts)})
    finally:
        rig.position(HOME)
    out.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    last=value["poses"][start:]
    print(json.dumps({"nombre":len(value["poses"]),"cible":len(states),
                      "poses_avec_interference":[[p["pose"],p["interferences"]] for p in last if p["interferences"]],
                      "ecart_faisceau_max_mm":max(p["cables"]["ecart_max_mm"] for p in last)},
                     ensure_ascii=False))


def operations_at_home():
    rig=active()
    rig.position(HOME)
    man=rig.forms.manager
    directions=(("Moteur J2 extrait côté gauche","SERVO_J2",("P07_Porte_J2","03_Tourelle"),
                 (0,-1,0),range(0,43,2)),
                ("Moteur J3 extrait côté gauche","SERVO_J3",("P08_Porte_J3","04_Segment_1"),
                 (0,-1,0),range(0,43,2)),
                ("Arbre J2 hors goupille et rotor","AXE_J2",("PALIER_J2_G","PALIER_J2_D","04_Segment_1"),
                 (0,1,0),range(0,63,2)),
                ("Arbre J3 hors goupille et rotor","AXE_J3",("PALIER_J3_G","PALIER_J3_D","05_Segment_2"),
                 (0,1,0),range(0,63,2)),
                ("Support du pouce sortant, axe commun en place","12_Support_Pouce",
                 ("07_Paume","SERVO_T1","14_Moyeu","11_Palonnier"),(0,-1,0),range(0,20,1)),
                ("Cassette J7 extraite, paume et arbre déposés","13_Bride_Poignet",
                 ("06_Segment_3",),(1,0,0),range(0,42,2)))
    results=[]
    for name,key,others,axis,ranges in directions:
        direction=vector(axis)
        if key in ("12_Support_Pouce","13_Bride_Poignet"):
            direction.transformBy(rig.occ["07_Paume"].transform2)
        xyz=direction.asArray()
        shapes=list(rig.occ[key].bRepBodies)
        if key=="13_Bride_Poignet":
            shapes.extend(rig.occ["SERVO_J7"].bRepBodies)
        fixed=[(c,b) for c in others for b in rig.occ[c].bRepBodies if not b.name.startswith("Repère de liaison")]
        hits=[]
        for n in ranges:
            for moving in shapes:
                tool=shifted(moving,tuple(n*a for a in xyz),man)
                for other,body in fixed:
                    v=volume_overlap(man,tool,body)
                    if v>.006:
                        hits.append([n,other,round(v,4)])
        results.append({"description":name,"positions":len(ranges),"contacts":hits})
    stops=[]
    for axis,name,limits in ((2,"04_Segment_1",J2_STOPS),(3,"05_Segment_2",J3_STOPS)):
        joint=rig.joints[name][0]
        ends=joint.rotationLimits
        desired=ends.isMinimumValueEnabled,ends.isMaximumValueEnabled
        try:
            ends.isMinimumValueEnabled=ends.isMaximumValueEnabled=False
            rotor=next(b for b in rig.occ[f"ROT_J{axis}"].bRepBodies if "Doigt de butée" in b.name)
            pins=[b for b in rig.occ[f"STAT_J{axis}"].bRepBodies if "Butée acier" in b.name]
            for endpoint in limits:
                side=math.copysign(1,endpoint)
                for angle in (endpoint-side,endpoint,endpoint+side,endpoint+2*side):
                    rig.set_rotation(name,angle)
                    stops.append({"axe":f"J{axis}","angle_deg":angle,
                                  "contact_butee_mm3":round(sum(volume_overlap(man,rotor,b) for b in pins),5)})
        finally:
            rig.position(HOME)
            ends.isMinimumValueEnabled,ends.isMaximumValueEnabled=desired
    data={"corridors":results,"butees":stops}
    (OUT/"Verification_Assemblage_r03.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(data,ensure_ascii=False))



def tool_access_at_home():
    """Sonder l’entrée axiale d’embouts cylindriques sur les fixations modélisées."""
    rig=active()
    assert all(abs(rig.angle(code))<.001 for code in MAIN_JOINTS.values())
    man=rig.forms.manager
    solids=[(code,body) for code,occ in rig.occ.items() for body in occ.bRepBodies
            if not body.name.startswith("Repère de liaison")]
    cases=[]

    def select(prefix, marker, axis, sign, diameter, length, removed=()):
        for code,body in solids:
            if code.startswith(prefix) and marker in body.name:
                cases.append((code,body,axis,sign,diameter,length,removed))


    select("ANC_","Tête M5",2,1,5,60)
    select("STAT_J2","Vis traversante M2,5",1,-1,3.6,42)
    for axis in (2,3):
        select(f"STAT_J{axis}","Tirant M3 support",1,-1,4,45,((f"SERVO_J{axis}",""),))
        removed=((f"P{axis+9:02}_Garde_J{axis}",""),
                 (f"STAT_J{axis}","Butée acier"),(f"CAB_J{axis}",""))
        select(f"STAT_J{axis}","Tirant M3 carter",1,1,4,45,removed)
    select("Vis_Bride_","",0,1,3,32,
           tuple((key,"") for key in ("07_Paume","14_Moyeu","DOG_J7","SERVO_T1")))
    select("Vis_Support_","Vis support",2,-1,3,32)
    select("Vis_Moyeu_","",2,1,3,32)
    select("Vis_Traverse_","",2,-1,3,32)

    def contacts(a,b,diameter,transform):
        start,end=core.Point3D.create(*a),core.Point3D.create(*b)
        start.transformBy(transform)
        end.transformBy(transform)
        probe=man.createCylinderOrCone(start,diameter/20,end,diameter/20)
        touches=[]
        for key,body in solids:
            volume=volume_overlap(man,probe,body)
            if volume>.006:
                touches.append({"repere":key,"corps":body.name,"mm3":round(volume,4)})
        return touches

    def after(touches,removals):
        return [t for t in touches if not any(t["repere"]==key and name in t["corps"]
                                             for key,name in removals)]

    rows=[]
    for code,fastener,axis,sign,diameter,length,removed in cases:
        bbox=fastener.nativeObject.boundingBox
        lo,hi=bbox.minPoint.asArray(),bbox.maxPoint.asArray()
        a=[(v+w)/2 for v,w in zip(lo,hi)]
        a[axis]=(hi if sign==1 else lo)[axis]+sign*.004
        b=a.copy()
        b[axis]+=sign*length/10
        transform=rig.occ[code].transform2
        start=core.Point3D.create(*a)
        start.transformBy(transform)
        touches=contacts(a,b,diameter,transform)
        row={"repere":code,"fixation":fastener.name,
             "diametre_embout_mm":diameter,"longueur_mm":length,
             "entree_mm":[round(v*10,3) for v in start.asArray()],
             "contacts_montage_complet":touches,"deposes_prevues":removed,
             "contacts_apres_depose":after(touches,removed)}
        if "Tirant M3 support" in fastener.name:
            bend=(a[0],a[1]-.28,a[2])
            tip=(bend[0],bend[1],bend[2]-3.)
            elbow_hits=contacts(a,bend,2.9,transform)+contacts(bend,tip,1.8,transform)
            row["embout_coude_indicatif"]={"course_axiale_mm":2.8,"diametre_pointe_mm":2.9,
                 "diametre_manche_mm":1.8,"longueur_manche_mm":30.,
                 "contacts_apres_depose":after(elbow_hits,removed)}
        rows.append(row)

    out=OUT/"Verification_Assemblage_r03.json"
    report=json.loads(out.read_text(encoding="utf8"))
    report["acces_embouts_HOME"]=rows
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"nombre":len(rows),
                      "sans_contact":sum(not r["contacts_montage_complet"] for r in rows),
                      "conditionnels":sum(bool(r["contacts_montage_complet"]) and not r["contacts_apres_depose"] for r in rows),
                      "obstacles":[[r["repere"],r["fixation"],r["contacts_apres_depose"]] for r in rows
                                   if r["contacts_apres_depose"]]},ensure_ascii=False))


def opposing_thumb():
    from construire_montage import measure_thumb
    rig=active()
    data=measure_thumb(core.Application.get(),rig)
    result={"poses":len(data),"jeu_min_paume_mm":min(p["jeu_paume_mm"] for p in data),
            "jeu_min_chape_mm":min(p["jeu_chape_mm"] for p in data),
            "interferences":[p for p in data if p["interferences"]],"mesures":data}
    (OUT/"Verification_Pouce_r03.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in result.items() if k!="mesures"},ensure_ascii=False))
