"""Cherche une dépose par translations successives sur les solides Fusion."""
import heapq
import json
from pathlib import Path

from controle_cao import write
from interfaces import ACCESS, bounding, collision
from stabiliser import Model, get_attr

STEPS=((0,1,0),(0,-1,0),(-1,0,0),(1,0,0),(0,0,-1),(0,0,1))
S = 2.0


def translate(m, body, offset):
    import adsk.core as core
    shift=core.Matrix3D.create()
    shift.translation=core.Vector3D.create(*(a/10 for a in offset))
    b=m.tmp.copy(body)
    assert m.tmp.transform(b,shift)
    return b


def find(m, key):
    required={*ACCESS[key][2],"Friction_J3_2","Ressort_J2","Ressort_J3","Tige_Ressort_J2","Tige_Ressort_J3",
              "Axe_Haut_Ressort_J2","Axe_Haut_Ressort_J3"}
    source=m.tmp.copy(m.solids(key)[0])
    vectors=[(k,b,bounding(b)) for k in m.occ if k not in {key,*required}
             and not get_attr(m.occ[k].component,"Souple") and not k.startswith("Tendon_")
             for live in m.solids(k) for b in (m.tmp.copy(live),)]
    low,high=bounding(source)
    vectors=[(k,b,lo,hi) for k,b,(lo,hi) in vectors if all(
             min(hi[i],high[i]+v[1])>=max(lo[i],low[i]+v[0]) for i,v in enumerate(((-32,32),(-55,64),(-34,38))))]
    hit_cache={}
    def blocked(shift):
        if shift not in hit_cache:
            a,b=([v[i]+shift[i] for i in range(3)] for v in (low,high))
            body=None
            for name,k,lo,hi in vectors:
                if any(min(hi[i],b[i])-max(lo[i],a[i])<=1e-4 for i in range(3)):
                    continue
                if body is None:
                    body=translate(m,source,shift)
                if collision(m,body,k)>.03:
                    hit_cache[shift]=True
                    return True
            hit_cache[shift]=False
        return hit_cache[shift]

    origin=(0,0,0)
    start=[(0,0,origin)]
    prior={origin:None}
    walked=0
    while start and walked<1350:
        _,depth,current=heapq.heappop(start)
        walked+=1
        if abs(current[1])>=58 or abs(current[0])>=32 or abs(current[2])>=36:
            order=[current]
            while prior[order[-1]] is not None:
                order.append(prior[order[-1]])
            full=list(reversed(order))
            for a,b in zip(full,full[1:]):
                if any(blocked(tuple(round(a[i]+(b[i]-a[i])*t/8,4) for i in range(3))) for t in range(1,8)):
                    return dict(motor=key,path_mm=None,reason="collision de transition",
                                steps_tested=len(hit_cache))
            return dict(motor=key,path_mm=full,steps_tested=len(hit_cache),removed=sorted(required))
        for direction in STEPS:
            next_q=tuple(x+S*d for x,d in zip(current,direction))
            if next_q in prior or abs(next_q[0])>32 or abs(next_q[2])>36 or not -58<=next_q[1]<=58:
                continue
            if blocked(next_q):
                continue
            midway=tuple((a+b)/2 for a,b in zip(current,next_q))
            if blocked(midway):
                continue
            prior[next_q]=current
            goal_dist=min(58-abs(next_q[1]),32-abs(next_q[0]),36-abs(next_q[2]))
            heapq.heappush(start,(depth+1+goal_dist/S,depth+1,next_q))
    return dict(motor=key,path_mm=None,reason="aucune sortie dans le réseau éprouvé",
                visited=walked,steps_tested=len(hit_cache),removed=sorted(required))


def run(_context,out):
    m=Model()
    assert max(abs(m.angle(k)) for k in ("J1","J2","J3","J7"))<.02
    proof=Path(out)
    results=[]
    for k in ("Moteur_J2","Moteur_J3"):
        results.append(find(m,k))
        write(proof,results)
    print(json.dumps(results))
