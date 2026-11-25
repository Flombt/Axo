"""Compensation réglable des tangages, géométrie Fusion et paramètres de calcul."""
import json

import adsk.core as core

from stabiliser import Model, add, boolean, box, cut, cylinder, get_attr, put_attr

# Point fixe et point mobile au neutre, en mm dans l’assemblage. Cotés à l’axe
# des deux accrochages, pour calculer la longueur utile et le bras de levier.
SPRINGS = {
    "J2": {"parent":"05_Tourelle", "child":"J2_Chape_Tangage", "root_fixed":(-8,21,87),
           "root_mobile":(37,7,114), "seat_z":91, "fixed":(-16,44,163), "moving":(40,44,83),
           "ref":"TA0500-063-0600", "free_mm":60.0, "long_mm":124.72,
           "preload_n":2.37, "rate_n_mm":.22, "diam_mm":5.0, "tige_mm":88},
    "J3": {"parent":"J2_Chape_Tangage", "child":"J3_Chape_Tangage", "root_fixed":(59,10,125),
           "root_mobile":(96,7,125), "seat_z":128, "fixed":(70.903524,44,161.569692),
           "moving":(98.903524,44,119.069692), "ref":"TA0400-050-0320", "free_mm":32.0,
           "long_mm":65.60, "preload_n":1.49, "rate_n_mm":.27, "diam_mm":4.0, "tige_mm":48},
}


def segment(model, a, b, r0, r1=None):
    r1 = r0 if r1 is None else r1
    shaft = cylinder(a,b,r0,r1)
    boolean(shaft,model.tmp.createSphere(core.Point3D.create(*(x/10 for x in a)),r0/10))
    boolean(shaft,model.tmp.createSphere(core.Point3D.create(*(x/10 for x in b)),r1/10))
    return shaft


def add_world(model, key, features, cutters):
    neutral = model.copy(key)
    transform = model.occ[key].transform2.copy()
    assert transform.invert()
    for tool in features:
        assert model.tmp.transform(tool, transform)
        boolean(neutral, tool)
    for tool in cutters:
        assert model.tmp.transform(tool, transform)
        cut(neutral,tool)
    model.replace(key,neutral)


def column(model, axis, cfg):
    root = cfg["root_fixed"]
    x, y, z = cfg["fixed"]
    seat = cfg["seat_z"]
    end = (x, y, seat)
    if axis == "J3":
        offset=(root[0],root[1],135)
        out=(root[0],y-2,135)
        braces=[segment(model,root,offset,2.8,4.8),segment(model,offset,out,4.8),
                segment(model,out,end,4.8,5.2)]
    else:
        braces=[segment(model,root,end,2.8,5.2),
                segment(model,(-8,21,77),end,2.8,4.7)]
    boss = cylinder((x,y,seat-5),(x,y,seat+5),6.0)
    hole = cylinder((x,y,seat-10),(x,y,seat+9),2.72)
    add_world(model,cfg["parent"],[*braces,boss],[hole])

    stem = cylinder((x,y,seat-8),(x,y,z-1),2.5)
    eye = cylinder((x,y-2.5,z),(x,y+2.5,z),4.0)
    boolean(stem,eye)
    cut(stem,cylinder((x,y-4.5,z),(x,y+4.5,z),1.65))
    model.place("Tige_Ressort_"+axis, "Tige M5 et œillet fermé "+axis, cfg["parent"],stem)

    root = cfg["root_mobile"]
    p = cfg["moving"]
    high=(root[0],root[1],131 if axis=="J2" else 129)
    corner=(root[0],p[1],high[2])
    lift=segment(model,root,high,2.8,4.4)
    outer=segment(model,high,corner,4.4)
    union=segment(model,corner,p,4.4,5.6)
    lug = cylinder(add(p,(0,-4,0)),add(p,(0,4,0)),5.4)
    hole = cylinder(add(p,(0,-8,0)),add(p,(0,8,0)),1.64)
    add_world(model,cfg["child"],[lift,outer,union,lug],[hole])
    pin = cylinder(add(p,(0,-4,0)),add(p,(0,6.5,0)),1.52)
    model.place("Axe_Ressort_"+axis,"Axe M3 retenu "+axis,cfg["child"],pin)
    # Le gabarit de diamètre est testé aux positions calculées, selon les deux ancrages.
    shape = cylinder(cfg["fixed"], cfg["moving"], cfg["diam_mm"]/2)
    occ = model.place("Ressort_"+axis,"Enveloppe du ressort "+cfg["ref"]+" au neutre",cfg["parent"],shape)
    put_attr(occ.component,"Souple","Enveloppe ressort au neutre")


def run(ctx):
    model=Model()
    model.require_copy()
    if get_attr(model.root,"Compensation"):
        raise RuntimeError("Supports de compensation déjà créés.")
    model.pose({})
    for axis,cfg in SPRINGS.items():
        column(model,axis,cfg)
    put_attr(model.root,"Compensation",SPRINGS)
    print(json.dumps(SPRINGS))
