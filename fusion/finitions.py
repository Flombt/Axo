"""Dégagement des capots et interfaces démontables V5 stabilisation."""
import json
import math
from pathlib import Path

import adsk.fusion as fusion

from compensation import SPRINGS, add_world, segment
from interfaces import ACCESS, collision, motor_access, move
from stabiliser import Model, add, boolean, box, cut, cylinder, get_attr, point, put_attr, sub


COVERS = {"Coque_Epaule":"05_Tourelle","Coque_Bras":"J2_Chape_Tangage",
          "Coque_Avant":"J3_Chape_Tangage","Embout_Coude":"J3_Chape_Tangage"}


def relief(model, target, tool):
    shield = model.copy(target)
    insert = model.copy(tool,target)
    original=shield.volume
    for axis in ((1,0,0),(0,1,0),(0,0,1)):
        for travel in (-.30,.30):
            cut(shield,move(model,insert,axis,travel))
    cut(shield,insert)
    if shield.lumps.count > 1:
        shell=max(shield.lumps,key=lambda lump:sum(face.area for face in lump.faces))
        assert model.tmp.deleteFaces(list(shell.faces),False),target
    model.replace(target,shield)
    return round((original-shield.volume)*1000,4)


def adjust_fittings(m):
    values={}
    for cap,carrier in COVERS.items():
        values[cap]=relief(m,cap,carrier)
    # Les gabarits métalliques restent en place pendant le perçage de leur
    # diamètre et pendant le contrôle de montage.
    for axis, cfg in SPRINGS.items():
        x,y,z=cfg["fixed"]
        cutout=cylinder((x,y,cfg["seat_z"]-10),(x,y,z+2.0),2.80)
        add_world(m,cfg["parent"],[],[cutout])
        p=cfg["moving"]
        shaft=cylinder(add(p,(0,-7.0,0)),add(p,(0,8.0,0)),1.72)
        add_world(m,cfg["child"],[],[shaft])
    values["Relief_contact_MG996_J3"]=relief(m,"J2_Chape_Tangage","Moteur_J3")
    return values


def material_point(m, key, center):
    body=m.solids(key)[0]
    offsets=[(a,b,c) for a in range(-5,6) for b in range(-5,6) for c in range(-5,6)]
    offsets.sort(key=lambda xyz:sum(t*t for t in xyz))
    for v in offsets:
        p=add(center,v)
        if body.pointContainment(point(p))==fusion.PointContainment.PointInsidePointContainment:
            return p
    raise RuntimeError("Appui introuvable sur "+key)


def comb(m,key, owner, center, root, sign):
    a=add(center,(0,-3.5,0))
    b=add(center,(0,3.5,0))
    shape=cylinder(a,b,5.8)
    attach=segment(m,root,add(center,(0,0,2.7)),3.4,3.5)
    boolean(shape,attach)
    for index in range(5):
        angle=index*2*math.pi/5
        dx,dz=2.45*math.cos(angle),2.45*math.sin(angle)
        offset=(dx,0,dz)
        through=cylinder(add(a,add(offset,(0,-.4,0))),add(b,add(offset,(0,.4,0))),.68)
        cavity=cylinder(add(center,add(offset,(0,-sign*1.8,0))),
                         add(center,add(offset,(0,sign*4.0,0))),1.12)
        cut(shape,through,cavity)
    add_world(m,owner,[shape],[])
    put_attr(m.occ[owner].component,"ArretPTFE","Cinq conduits Ø2 mm, marches Ø1,36 mm")


def run(_context, out):
    m=Model()
    m.require_copy()
    m.pose({})
    if get_attr(m.root,"Degagements"):
        raise RuntimeError("Dégagements déjà repris")
    removed=adjust_fittings(m)
    conf=json.loads(get_attr(m.root,"Boucles"))["Boucle_J7"]
    comb(m,"Arret_J7_Amont","Capot_Cassette",conf["a"],
         material_point(m,"Capot_Cassette",(150,-24,107)),-1)
    comb(m,"Arret_J7_Aval","Capot_Paume",conf["b"],
         material_point(m,"Capot_Paume",(192,-22,115)),-1)
    put_attr(m.root,"Degagements",removed)
    out=Path(out)
    out.write_text(json.dumps(removed,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(removed))
