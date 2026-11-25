"""Rejouer les cibles refusées dans l’espace des commandes et des pignons."""
import json
import math
from pathlib import Path

from controle_cao import COMMANDS, write
from stabiliser import Model

GEARS={"J1":("P1M",-22/38),"J2":("P2M",-3),"J3":("P3M",-2)}


def set_angle(model,axis,q):
    initial,sign,_=model.cal[axis]
    motion=model.joints[axis].jointMotion
    prior=motion.rotationValue
    goal=initial+sign*math.radians(q)
    if abs(prior-goal)>1e-7:
        motion.rotationValue=goal


def test(model,target,reverse,use_motor,only_azimuth,pieces):
    sequence=list(COMMANDS)
    if reverse:
        sequence.reverse()
    model.pose({})
    for step in range(1,pieces+1):
        for k in sequence:
            cmd,value=(k,target[k])
            if use_motor and k in GEARS and (not only_azimuth or k=="J1"):
                cmd,ratio=GEARS[k]
                value*=ratio
            q=value*step/pieces
            set_angle(model,cmd,q)
    # Réinsister seulement sur les axes qui s'écartent de leur cible.
    for _ in range(2):
        for k in sequence:
            if abs(model.angle(k)-target[k])>.02:
                set_angle(model,k,target[k])
    actual={k:round(model.angle(k),6) for k in COMMANDS}
    return actual,max(abs(actual[k]-target[k]) for k in COMMANDS)


def run(_context,folder):
    path=Path(folder)
    original=json.loads((path/"campagne_fusion.json").read_text(encoding="utf-8"))
    broken={}
    for r in original:
        if r["error_deg"]>.02:
            key=tuple(r["target"][k] for k in COMMANDS)
            broken.setdefault(key,[]).append(r["source_case"])
    model=Model()
    output=[]
    try:
        for values,groups in broken.items():
            q=dict(zip(COMMANDS,values))
            tried=[]
            for reverse,motor,just_yaw,steps in (
                (True,False,False,1),(False,True,True,1),(True,True,True,1),
                (False,True,False,1),(True,True,False,1),(True,False,False,5),
                (False,True,True,5),(True,True,True,5)):
                actual,e=test(model,q,reverse,motor,just_yaw,steps)
                tried.append(dict(reverse=reverse,use_motor=motor,only_j1_motor=just_yaw,steps=steps,
                                  error_deg=e,actual=actual))
                if e<=.02:
                    break
            row={"cases":groups,"target":q,"tried":tried,
                 "confirmed":any(r["error_deg"]<=.02 for r in tried)}
            output.append(row)
            write(path/"reprises_poses.json",output)
    finally:
        model.pose({})
    print(json.dumps([[o["cases"],o["confirmed"],min(k["error_deg"] for k in o["tried"])] for o in output]))


def verifier_geometrie(_context,folder):
    """Vérifie les corps natifs positionnés par la FK, en mémoire et hors solveur."""
    import adsk.core as core
    from interfaces import bounding, collision
    from stabiliser import get_attr

    p=Path(folder)
    requests=json.loads((p/"poses_calcul_independant.json").read_text(encoding="utf-8"))
    parts0=json.loads((p/"geometrie_neutre.json").read_text(encoding="utf-8"))["parts"]
    m=Model()
    results=[]
    for entry in requests:
        on_pose={}
        for k,o in m.occ.items():
            if get_attr(o.component,"Souple") or k.startswith("Tendon_"):
                continue
            tr=core.Matrix3D.create()
            assert tr.setWithArray(entry["relative"][k])
            origin=core.Matrix3D.create()
            assert origin.setWithArray(parts0[k]["transform"])
            parts=[]
            for b in m.solids(k,True):
                temp=m.tmp.copy(b)
                assert m.tmp.transform(temp,origin) and m.tmp.transform(temp,tr)
                parts.append((temp,bounding(temp)))
            on_pose[k]=parts
        flat=[(k,b,lo,hi) for k,bodies in on_pose.items() for b,(lo,hi) in bodies]
        hits=[]
        for index,(a,body,lo,hi) in enumerate(flat):
            for key,shape,lb,hb in flat[index+1:]:
                if a==key or any(min(hi[j],hb[j])-max(lo[j],lb[j])<=1e-5 for j in range(3)):
                    continue
                volume=collision(m,body,shape)
                if volume>.03:
                    hits.append([a,key,round(volume,5)])
        hand = ("11_Paume", *(k+str(i) for k in "PIMAU" for i in (1,2,3)))
        gap=m.app.measureManager.measureMinimumDistance(on_pose["P3"][0][0],on_pose["I3"][0][0]).value*10
        results.append({"label":entry["label"],"cases":entry["cases"],"target":entry["target"],
                        "minimum_z_hand_mm":min(lo[2] for k in hand for _,(lo,hi) in on_pose[k]),
                        "pince_mm":gap,"intersections":hits,"native_solver_confirmed":False})
    write(p/"contreposes_brep.json",results)
    print(json.dumps([[r["cases"],r["label"],r["intersections"]] for r in results]))
