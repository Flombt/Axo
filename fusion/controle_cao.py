"""Campagne Fusion native et extraction des solides pour la V5 stabilisée."""
import gzip
import json
import math
from pathlib import Path

import adsk.core as core
import adsk.fusion as fusion

from stabiliser import Model, get_attr, mm, point, sub
from interfaces import bounding
from routage import LOOPS, loop_curve

COMMANDS = ("J1", "J2", "J3", "J7", *("Servo_" + k for k in "PIMAU"))
DRIVEN = ("P1M", "P2M", "P3M", *(k + str(i) for k in "PIMAU" for i in (1, 2, 3)))
TOL_MM = .08


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def neutral_data(m, folder):
    m.pose({})
    records, meshes = {}, []
    names = {o.name: k for k,o in m.occ.items()}
    for key,o in m.occ.items():
        native = m.solids(key,True)
        assembly = m.solids(key)
        volumes = [b.volume * 1000 for b in assembly]
        solid_volume = sum(volumes)
        com = [sum(v * mm(b.physicalProperties.centerOfMass)[i] for v,b in zip(volumes,assembly))/solid_volume
               for i in range(3)] if solid_volume else None
        records[key] = dict(name=o.component.name, parent=get_attr(o.component,"Parent"),
                            part_number=o.component.partNumber, transform=o.transform2.asArray(),
                            volume_mm3=solid_volume, com_mm=com,
                            print_ref=get_attr(o.component,"Impression"),
                            flexible=get_attr(o.component,"Souple"),
                            world_bounds_mm=[bounding(b) for b in assembly])
        for b in native:
            calculator=b.meshManager.createMeshCalculator()
            calculator.surfaceTolerance = TOL_MM / 10
            mesh=calculator.calculate()
            if not mesh or not mesh.triangleCount:
                raise RuntimeError("Maillage Fusion absent pour " + key)
            meshes.append({"part":key, "v":[[round(x,5) for x in mm(p)] for p in mesh.nodeCoordinates],
                           "f":list(mesh.nodeIndices)})
    joints = {key: {"pivot_mm":mm(j.geometry.origin),
                    "axis":j.jointMotion.rotationAxisVector.asArray(),
                    "child":names[j.occurrenceOne.name],"parent":names[j.occurrenceTwo.name]}
              for key,j in m.joints.items() if key in m.cal}
    attrs = {v.name:v.value for v in m.root.attributes}
    data = {"parts":records, "joints":joints, "attributes":attrs,
            "mesh_tolerance_mm":TOL_MM, "fusion_version":m.app.version}
    write(folder/"geometrie_neutre.json",data)
    with gzip.open(folder/"maillages_natifs.json.gz","wt",encoding="utf-8") as stream:
        json.dump(meshes,stream,ensure_ascii=False,separators=(",",":"))
    return data


def relative(m, neutral, owner, xyz):
    p = point(xyz)
    t = core.Matrix3D.create()
    assert t.setWithArray(neutral["parts"][owner]["transform"]) and t.invert()
    assert p.transformBy(t) and p.transformBy(m.occ[owner].transform2)
    return mm(p)


def bend_report(m, neutral):
    rows = {}
    for name, cfg in LOOPS.items():
        parent, child = cfg["parent"], cfg["child"]
        a,b = [relative(m,neutral,k,xyz) for k,xyz in ((parent,cfg["a"]),(child,cfg["b"]))]
        t = core.Matrix3D.create()
        assert t.setWithArray(neutral["parts"][parent]["transform"]) and t.invert()
        out = core.Vector3D.create(*cfg["out"])
        assert out.transformBy(t) and out.transformBy(m.occ[parent].transform2)
        try:
            pts, radius, straight = loop_curve(a,b,out.asArray(),cfg["length"])
            rows[name] = {"bend_mm": radius,"straight_mm":straight,
                          "min_z_mm":min(p[2] for p in pts)-cfg["radius"]}
        except ValueError as error:
            rows[name] = {"error":str(error)}
    for axis,cfg in json.loads(get_attr(m.root,"Compensation") or "{}").items():
        a = relative(m,neutral,cfg["parent"],cfg["fixed"])
        b = relative(m,neutral,cfg["child"],cfg["moving"])
        piv = relative(m,neutral,neutral["joints"][axis]["parent"],neutral["joints"][axis]["pivot_mm"])
        lever = sub(b,piv)
        direction = sub(a,b)
        d = math.sqrt(sum(u*u for u in direction))
        cross = core.Vector3D.create(*lever).crossProduct(core.Vector3D.create(*direction))
        frame = core.Matrix3D.create()
        k=neutral["joints"][axis]["parent"]
        assert frame.setWithArray(neutral["parts"][k]["transform"]) and frame.invert()
        unit_axis = core.Vector3D.create(*neutral["joints"][axis]["axis"])
        assert unit_axis.transformBy(frame) and unit_axis.transformBy(m.occ[k].transform2)
        force = cfg["preload_n"] + cfg["rate_n_mm"]*(d-cfg["free_mm"]) if d>=cfg["free_mm"] else 0
        rows["Ressort_"+axis] = {"length_mm":d,"newton":force,
                                 "torque_nm":cross.dotProduct(unit_axis)/d*force/1000}
    return rows


def overlaps(m):
    collection = core.ObjectCollection.create()
    key_by_name = {o.name:k for k,o in m.occ.items()}
    for key,occ in m.occ.items():
        if get_attr(occ.component,"Souple") or key.startswith("Tendon_"):
            continue
        for b in m.solids(key):
            collection.add(b)
    inputs = m.design.createInterferenceInput(collection)
    inputs.areCoincidentFacesIncluded = False
    result = m.design.analyzeInterference(inputs)
    if result is None:
        raise RuntimeError("Résultat d’interférences absent")
    rows = []
    for hit in result:
        a,b = [key_by_name.get(o.assemblyContext.name,o.name) if o.assemblyContext else get_attr(o.parentComponent, "Repere") or o.name
               for o in (hit.entityOne,hit.entityTwo)]
        v=hit.interferenceBody.volume*1000
        if a != b and v > .03:
            rows.append([a,b,round(v,5)])
    return sorted(rows)


def solve(m, target):
    m.pose({})
    actual=m.pose(target)
    def error():
        return max(abs(actual[k]-target.get(k,0)) for k in COMMANDS)
    if error()>.02:
        m.pose({})
        for step in range(1,25):
            actual=m.pose({key:value*step/24 for key,value in target.items()})
    return actual,error()


def case(m, neutral, label, target, scan, keep_transform=False):
    actual,err=solve(m,target)
    row = dict(label=label,target=target,actual={k:round(actual[k],5) for k in (*COMMANDS,*DRIVEN)},
               error_deg=round(err,6))
    if err>.02:
        return row
    hand = ["11_Paume",*(f"{k}{j}" for k in "PIMAU" for j in range(1,4))]
    row["hand_z_mm"]=min(bounding(b)[0][2] for k in hand for b in m.solids(k))
    mpos = m.app.measureManager.measureMinimumDistance(m.solids("P3")[0],m.solids("I3")[0])
    row["pince_mm"]=mpos.value*10
    row["passages"]=bend_report(m,neutral)
    if scan:
        row["rigid_overlaps"]=overlaps(m)
    if keep_transform:
        row["transform"]={k:o.transform2.asArray() for k,o in m.occ.items()}
    return row


def campaign(folder, base_cases):
    m=Model()
    folder.mkdir(parents=True,exist_ok=True)
    neutral=neutral_data(m,folder)
    guarded={"J2":-21,"J3":-32}
    important=[("Neutre",{},True),("Tangages bas J7 -32",dict(guarded,J7=-32),True),
               ("Tangages bas J7 +32",dict(guarded,J7=32),True),
               ("Tangages bas poing",dict(guarded,**dict.fromkeys(COMMANDS[4:],92)),True),
               ("Pince à 92",{"Servo_P":92,"Servo_I":92},True),
               ("J1 gauche",{"J1":-88},True),("J1 droite",{"J1":88},True),
               ("Main poing",dict.fromkeys(COMMANDS[4:],92),True),
               ("Prise cylindrique commandée",{"Servo_P":75,"Servo_I":56,"Servo_M":68,"Servo_A":68,"Servo_U":59},True)]
    results = []
    try:
        for name,q,scan in important:
            results.append(case(m,neutral,name,q,scan,True))
        write(folder/"poses_reperes.json",results)
        cases = []
        for i,(title,source) in enumerate(base_cases):
            mapped = {k:source.get(k,0) for k in COMMANDS}
            row = case(m,neutral,title,mapped,i in range(0,153,12))
            row.update(source_case=i,roulis_retires_deg={k:source[k] for k in ("J2R","J3R") if source[k]})
            cases.append(row)
        write(folder/"campagne_fusion.json",cases)
    finally:
        m.pose({})
    print(json.dumps({"native":len(cases),"confirmed":sum(p["error_deg"]<=.02 for p in cases),
                      "min_hand_z":min(p["hand_z_mm"] for p in (*results,*cases) if "hand_z_mm" in p),
                      "overlaps":[[p["label"],p.get("rigid_overlaps",[])] for p in results]},
                     ensure_ascii=False))


def candidates(folder):
    m=Model()
    neutral=neutral_data(m,folder)
    samples=[]
    for q in ({"J2":j2,"J3":j3,"J7":j7} for j2,j3 in ((0,0),(-21,-32),(21,32),(-21,32),(21,-32))
              for j7 in (-32,0,32)):
        samples.append(case(m,neutral,str(q),q,True))
    write(folder/"precontrole.json",samples)
    m.pose({})
    print(json.dumps([[r["target"],round(r.get("hand_z_mm",0),3),r.get("rigid_overlaps",[])]
                      for r in samples],ensure_ascii=False))
