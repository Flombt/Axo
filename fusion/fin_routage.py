"""Dégagement des gaines et ressorts à partir de leurs positions aux articulations."""
import json
import math
from pathlib import Path

from controle_cao import bend_report, relative, write
from interfaces import collision
from routage import J1_HIGH, LOOPS, length, loop_curve, polyline_solid
from stabiliser import Model, add, cut, cylinder, get_attr, put_attr, scale, sub


def shape_loop(m, neutral, name, allowance=0.0, trim=0.0):
    conf=LOOPS[name]
    a,b=(relative(m,neutral,owner,pos) for owner,pos in ((conf["parent"],conf["a"]),
                                                        (conf["child"],conf["b"])))
    out0=relative(m,neutral,conf["parent"],(0,0,0))
    out1=relative(m,neutral,conf["parent"],conf["out"])
    pts, radius, _=loop_curve(a,b,sub(out1,out0),conf["length"])
    if trim:
        pts=trim_ends(pts,trim)
    return polyline_solid(m,pts,conf["radius"]+allowance)


def trim_ends(points,lost):
    values=list(points)
    for reverse in (False,True):
        need=lost
        for i in range(len(values)-1):
            path=sub(values[i+1],values[i])
            span=length(path)
            if span>need:
                first=add(values[i],scale(need/span,path))
                values=[first,*values[i+1:]]
                break
            need-=span
        values.reverse()
    return values


def largest(m,shape):
    if shape.lumps.count>1:
        solid=max(shape.lumps,key=lambda lump:sum(face.area for face in lump.faces))
        assert m.tmp.deleteFaces(list(solid.faces),False)
    return shape


def sweep_remove(m, neutral, target, cases, factory):
    body=m.copy(target)
    initial=body.volume
    for q in cases:
        m.pose(q)
        tool=factory()
        t=m.occ[target].transform2.copy()
        assert t.invert() and m.tmp.transform(tool,t)
        if collision(m,body,tool)>1e-4:
            cut(body,tool)
    m.pose({})
    m.replace(target,largest(m,body))
    return round((initial-body.volume)*1000,4)


def offset_springs(m):
    springs=json.loads(get_attr(m.root,"Compensation"))
    for k,cfg in springs.items():
        a,b=cfg["fixed"],cfg["moving"]
        pa,pb=(add(p,(0,10.0,0)) for p in (a,b))
        wire="Ressort_"+k
        native=cylinder(pa,pb,cfg["diam_mm"]/2)
        t=m.occ[wire].transform2.copy()
        assert t.invert() and m.tmp.transform(native,t)
        m.replace(wire,native)
        upper=m.place("Axe_Haut_Ressort_"+k,"Axe lisse M3 retenu du ressort supérieur "+k,cfg["parent"],
                      cylinder(add(a,(0,-3.4,0)),add(pa,(0,2.5,0)),1.5))
        put_attr(upper.component,"Montage","Rondelles et retenue axiale de l’œil")
        lower="Axe_Ressort_"+k
        revised=cylinder(add(b,(0,-4,0)),add(pb,(0,2.5,0)),1.5)
        t=m.occ[lower].transform2.copy()
        assert t.invert() and m.tmp.transform(revised,t)
        m.replace(lower,revised)
        cfg["fixed"],cfg["moving"]=pa,pb
    put_attr(m.root,"Compensation",springs)


def cable_fixed(m, neutral):
    # Le même passage est calculé dans le repère mobile du longeron pour toute
    # la course et dans le repère fixe du capot. L’ouverture inclut un jeu de pose.
    return polyline_solid(m,[relative(m,neutral,"05_Tourelle",p) for p in J1_HIGH],4.35)


def run(ctx,folder):
    m=Model()
    m.require_copy()
    m.pose({})
    path=Path(folder)
    base=json.loads((path/"geometrie_neutre.json").read_text(encoding="utf-8"))
    adjust={}
    for target,cases in (("Coque_Epaule",[{}]),
                         ("J2_Chape_Tangage",[{"J2":v} for v in (-21,-15,-9,-3,3,9,15,21)])):
        adjust[f"fixe/{target}"]=sweep_remove(m,base,target,cases,lambda:cable_fixed(m,base))
    for name,target,axis in (("Boucle_J2","J2_Chape_Tangage","J2"),
                             ("Boucle_J3","J3_Chape_Tangage","J3")):
        values=(21 if axis=="J2" else 32)
        cases=[{axis:j*values/6} for j in range(-6,7)]
        adjust[f"{name}/{target}"]=sweep_remove(m,base,target,cases,lambda:shape_loop(m,base,name,.7))
    offset_springs(m)
    put_attr(m.root,"FinitionsFaisceau",adjust)
    write(path/"reprises_faisceau.json",adjust)
    print(json.dumps(adjust))


def verify(m,neutral,folder):
    cfg=json.loads(get_attr(m.root,"Compensation"))
    tracked=[{}, {"J1":88}, {"J1":-88}, {"J2":-21,"J3":-32,"J7":32},
             {"J2":21,"J3":32,"J7":-32}, {"J2":-21,"J3":32,"J7":-32},
             {"J2":15,"J3":-19,"J7":-20}, {"J2":-15,"J3":-20,"J7":20}]
    results=[]
    try:
        for q in tracked:
            m.pose(q)
            shapes={name:shape_loop(m,neutral,name,trim=8.5 if name=="Boucle_J7" else 0)
                    for name in LOOPS}
            for ax,spring in cfg.items():
                a=relative(m,neutral,spring["parent"],spring["fixed"])
                b=relative(m,neutral,spring["child"],spring["moving"])
                ab=sub(b,a)
                u=scale(1/length(ab),ab)
                shapes["Ressort_"+ax]=cylinder(add(a,scale(4,u)),add(b,scale(-4,u)),spring["diam_mm"]/2)
            for k in ("Faisceau_Socle_Axe","Faisceau_Tourelle"):
                shapes[k]=m.tmp.copy(m.solids(k)[0])
            overlaps=[]
            for k,tool in shapes.items():
                for v in m.occ:
                    if get_attr(m.occ[v].component,"Souple") or v.startswith("Tendon_"):
                        continue
                    for b in m.solids(v):
                        vmm=collision(m,tool,b)
                        if vmm>.03:
                            overlaps.append([k,v,round(vmm,4)])
            results.append({"q":q,"overlaps":sorted(overlaps),"bend":bend_report(m,neutral)})
    finally:
        m.pose({})
    write(Path(folder)/"passages_brep_final.json",results)
    print(json.dumps([[row["q"],row["overlaps"]] for row in results]))


def wrist_ends(m,folder):
    # La gaine tressée s'arrête avant les deux peignes. Les cinq liners
    # terminent séparément dans des ports de Ø2,24 mm.
    path=Path(folder)
    neutral=json.loads((path/"geometrie_neutre.json").read_text(encoding="utf-8"))
    u=LOOPS["Boucle_J7"]
    adjust={}
    q=[{"J7":v} for v in (-32,-24,-16,-8,0,8,16,24,32)]
    for cap in ("Capot_Cassette","Capot_Paume"):
        adjust[cap]=sweep_remove(m,neutral,cap,q,
                                 lambda:shape_loop(m,neutral,"Boucle_J7",.42,8.5))
    solid=shape_loop(m,neutral,"Boucle_J7",trim=8.5)
    inv=m.occ["Boucle_J7"].transform2.copy()
    assert inv.invert() and m.tmp.transform(solid,inv)
    m.replace("Boucle_J7",solid)
    for suffix,p,owner in (("Amont",u["a"],u["parent"]),("Aval",u["b"],u["child"])):
        for j in range(5):
            theta=j*2*math.pi/5
            cx,cy,cz=add(p,(2.45*math.cos(theta),0,2.45*math.sin(theta)))
            sheath=cylinder((cx,cy-8.5,cz),(cx,cy+1.7,cz),1.0)
            cut(sheath,cylinder((cx,cy-9.0,cz),(cx,cy+2.0,cz),.50))
            key=f"Liner_{suffix}_{j+1}"
            occ=m.place(key,f"Liner PTFE Ø2/1 {suffix} {j+1}",owner,sheath)
            put_attr(occ.component,"Souple","Extrémité individuelle, ajustement à éprouver")
    put_attr(m.root,"SortiesJ7",dict(sleeve_ends_mm=8.5,trims=adjust))
    write(path/"sorties_j7.json",adjust)
