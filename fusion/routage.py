"""Enveloppes des faisceaux et guides de service de la V5 stabilisée."""
import math

import adsk.core as core

from stabiliser import (Model, add, boolean, box, cut, cylinder, get_attr,
                        mm, point, put_attr, retire, scale, sub, unit)
from compensation import add_world, segment


# Les points neutres sont exprimés en mm dans Fusion, les longueurs sont libres entre brides.
LOOPS = {
    "Boucle_J2": {"a":(-12,37,73), "b":(37,37,88), "parent":"05_Tourelle", "child":"J2_Chape_Tangage",
                 "out":(0,1,0), "length":92.0, "radius":3.4, "minimum":15.0},
    "Boucle_J3": {"a":(53,37,109), "b":(100,37,112), "parent":"J2_Chape_Tangage", "child":"J3_Chape_Tangage",
                 "out":(0,1,0), "length":90.0, "radius":3.0, "minimum":15.0},
    "Boucle_J7": {"a":(151,-33,110), "b":(192,-33,113), "parent":"J3_Chape_Tangage", "child":"11_Paume",
                 "out":(0,-1,0), "length":84.0, "radius":3.8, "minimum":15.0},
}
J1_RADIUS = 3.4
J1_FREE_MM = 124.0
def upper_route():
    side = math.sqrt(.5)
    arc = [math.pi*i/16 for i in range(1,9)]
    points = [(0,0,56),(0,0,61)]
    for t in arc:
        horizontal = 12*(1-math.cos(t))*side
        points.append((-horizontal, horizontal, 61+12*math.sin(t)))
    for i in range(1,6):
        angle = math.pi*(5-i)/20
        points.append((-12*math.cos(angle),12*(2*side-math.sin(angle)),73))
    return points + [(-12,37,73)]


J1_HIGH = upper_route()


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def length(a):
    return math.sqrt(dot(a,a))


def loop_curve(a, b, outward, requested):
    # Deux brins droits tangents et un arc de 180° de rayon D/2.
    span = sub(b,a)
    radius = length(span)/2
    chord = unit(span)
    outward = unit(sub(outward, scale(dot(outward,chord),chord)))
    straight = (requested - math.pi*radius)/2
    if straight < -1e-7:
        raise ValueError(f"Boucle trop courte de {-2*straight:.2f} mm")
    middle = add(scale(.5,add(a,b)),scale(straight,outward))
    points = [a]
    for i in range(25):
        t = math.pi*i/24
        offset = add(scale(-radius*math.cos(t),chord),scale(radius*math.sin(t),outward))
        p = add(middle,offset)
        if length(sub(p,points[-1])) > 1e-6:
            points.append(p)
    if length(sub(b,points[-1])) > 1e-6:
        points.append(b)
    return points, radius, straight


def polyline_solid(model, points, radius, rounded=True):
    if rounded:
        result = segment(model,points[0],points[1],radius)
    else:
        result = cylinder(points[0],points[1],radius)
    for a,b in zip(points[1:],points[2:]):
        if length(sub(b,a)) < 1e-5:
            continue
        boolean(result, segment(model,a,b,radius) if rounded else cylinder(a,b,radius))
    return result


def wire(model,key,parent,points,radius):
    shape=polyline_solid(model,points,radius)
    occ=model.place(key,key.replace("_"," "),parent,shape)
    put_attr(occ.component,"Souple","Enveloppe souple au neutre")


def fairlead(model,key,parent,root,center,axis,diam,ten_mm=8):
    d = scale(1,unit(axis))
    lo,hi = add(center,scale(-ten_mm/2,d)),add(center,scale(ten_mm/2,d))
    shape = segment(model,root,center,4.3,4.6)
    boolean(shape,cylinder(lo,hi,diam/2+2.6))
    hole = cylinder(add(lo,scale(-2,d)),add(hi,scale(2,d)),diam/2)
    # La seconde découpe autorise l’introduction du faisceau et la fermeture par collier.
    gap = box(add(center,(0,0,diam/2+2)),(diam-1,ten_mm+5,6)) if axis[1] else None
    cut(shape,hole,*([gap] if gap else []))
    t=model.occ[parent].transform2.copy()
    assert t.invert()
    owner = model.copy(parent)
    seed = model.tmp.copy(owner)
    assert model.tmp.transform(shape,t)
    boolean(seed,shape)
    if seed.lumps.count != 1:
        raise RuntimeError("Reprise du guide non solidaire "+key)
    model.replace(parent,seed)


def native_routing(model):
    model.require_copy()
    if not get_attr(model.root,"Compensation"):
        raise RuntimeError("Ajouter d’abord les appuis de compensation.")
    model.pose({})
    old = [key for key in model.occ if key.startswith("Traction_")]
    retire(model,old)
    # Le volume de traversée est dégagé dans la tourelle. Le dernier changement de
    # direction est abordé par une réserve de fil côté extérieur du guide.
    upper = J1_HIGH
    passage = polyline_solid(model,upper,4.5)
    add_world(model,"05_Tourelle",[],[passage])
    lower=[(16,0,-53),(12,0,-53)]
    lower += [(12-12*math.sin(t),0,-41-12*math.cos(t))
              for t in (math.pi*i/16 for i in range(1,9))]
    lower += [(0,0,57.2)]
    wire(model,"Faisceau_Socle_Axe","01_Platine",lower,J1_RADIUS)
    wire(model,"Faisceau_Tourelle","05_Tourelle",upper,J1_RADIUS)

    add_world(model,"05_Tourelle",[box((-12,32.0,73),(10,12,9)),
                                    segment(model,(-14,38,89),(-12,32,72),4.8,4.4)],
              [cylinder((-12,24,73),(-12,39,73),4.10)])
    fairlead(model,"Bras_J2","J2_Chape_Tangage",(40,44,86),LOOPS["Boucle_J2"]["b"],(0,1,0),7.8)
    fairlead(model,"Départ_J3","J2_Chape_Tangage",(70.903524,44,129),LOOPS["Boucle_J3"]["a"],(0,1,0),7.0)
    fairlead(model,"Avant_bras_J3","J3_Chape_Tangage",(98.903524,44,121),LOOPS["Boucle_J3"]["b"],(0,1,0),7.0)

    for name,cfg in LOOPS.items():
        points,radius,tail = loop_curve(cfg["a"],cfg["b"],cfg["out"],cfg["length"])
        assert radius>=cfg["minimum"], name
        wire(model,name,cfg["parent"],points,cfg["radius"])

    # Gabarits de la distribution 5 V. Le bloc secteur reste externe à la platine.
    panel = box((40,20,-39),(64,36,17))
    model.place("Distribution_5V","Gabarit basse tension, relais et dérivations",
                "01_Platine",panel)
    put_attr(model.root,"Boucles",LOOPS)
    put_attr(model.root,"Torsion_J1",{"du_tube":[-12,63],"r_faisceau_mm":J1_RADIUS,"longueur_libre_mm":J1_FREE_MM})
    print("Axe traversant, volumes de service et guides ajoutés.")


def run(ctx):
    native_routing(Model())
