"""Réduit les lumières de butée et recale la hauteur du support ancré."""
import json
import math
from pathlib import Path

from interfaces import collision
from stabiliser import Model, boolean, cut, cylinder, put_attr

TABLE_Z = -90.0
ANCHORS = ((-61,-47),(-61,47),(68,-47),(68,47))
STOPS = {"J2":(22.0,17.7), "J3":(33.0,10.9)}


def stop_slot(model, axis, nominal, radius):
    key = axis+"_Roue"
    target=model.copy(key)
    stop_radius=2.25
    for sense in (-1,1):
        offset=2*math.asin((1.45+stop_radius)/(2*radius))
        angle=math.pi/2+sense*(math.radians(nominal)+offset)
        x,y=radius*math.cos(angle),radius*math.sin(angle)
        plug=cylinder((x,y,0),(x,y,5.15),stop_radius)
        boolean(target,plug)
    model.replace(key,target)


def new_feet(model):
    floor=TABLE_Z
    # Les origines natives des rehausses conservent leur repère de la copie initiale.
    x = -.5
    core=cylinder((x,0,floor),(x,0,floor+4),15)
    for lo,hi,r0,r1 in ((floor+3.8,floor+11,15,9),(floor+10.8,-8,9,9),
                        (-8.2,-2,9,9.8),(-2.2,0,9.8,9.8)):
        boolean(core,cylinder((x,0,lo),(x,0,hi),r0,r1))
    cut(core,cylinder((x,0,floor-1),(x,0,1),2.8))
    for i in range(1,5):
        key=f"Pied_Rehausse_{i}"
        model.replace(key,model.tmp.copy(core))
        comp=model.occ[key].component
        comp.name="Entretoise d’ancrage 90 mm"
        comp.partNumber="AURA-V5-Rehausse_90_M5"
        put_attr(comp,"Impression","Rehausse_90_M5")
    put_attr(model.root,"PlanDeTravail",{"plan_table_mm":floor,"ancrage_xy_mm":ANCHORS})


def observe_stop(m, axis, angle, pairs):
    actual=m.pose({axis:angle})[axis]
    contacts=[collision(m,m.solids(a)[0],m.solids(b)[0]) for a,b in pairs]
    if abs(actual-angle)>.065:
        raise RuntimeError(f"Pose de butée refusée {axis} {angle}°")
    return max(contacts)


def nudge_stops(m):
    pairs={"J1":[("05_Tourelle","Butee_J1_"+str(i)) for i in (1,2)],
           "J2":[("J2_Roue","But_J2")],"J3":[("J3_Roue","But_J3")]}
    angle_brackets={"J1":(88,95),"J2":(21,25),"J3":(32,36)}
    measured={}
    for axis in pairs:
        motor=f"P{axis[-1]}M"
        limits=[m.joints[v].jointMotion.rotationLimits for v in (axis,motor)]
        m.pose({})
        for lim in limits:
            lim.isMinimumValueEnabled=lim.isMaximumValueEnabled=False
        rows=[]
        try:
            for sense in (-1,1):
                lo,hi=angle_brackets[axis]
                assert observe_stop(m,axis,sense*lo,pairs[axis])<.015, (axis,lo)
                assert observe_stop(m,axis,sense*hi,pairs[axis])>.015, (axis,hi)
                for i in range(6):
                    mid=(lo+hi)/2
                    if observe_stop(m,axis,sense*mid,pairs[axis])<=.015:
                        lo=mid
                    else:
                        hi=mid
                rows.append(dict(direction=sense,last_clear_deg=lo,first_contact_deg=hi))
        finally:
            m.pose({})
            for lim in limits:
                lim.isMinimumValueEnabled=lim.isMaximumValueEnabled=True
        measured[axis]=rows
    return measured


def run(_context,output):
    m=Model()
    m.require_copy()
    m.pose({})
    for axis,params in STOPS.items():
        stop_slot(m,axis,*params)
    new_feet(m)
    measured=nudge_stops(m)
    put_attr(m.root,"Butees",measured)
    Path(output).write_text(json.dumps(measured,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(measured))
