"""Doigt autonome équipé de trois servos et d'un montage de mesure."""

import importlib.util
import math
from pathlib import Path

import adsk


HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT/"01_Doigt"
LENGTHS=(46.0,42.0,37.0)
ORIGINS=(0.0,46.0,88.0)
RANGE=45


def source_geometry():
    path=ROOT.parent/"AURA_V3/Fabrication_r03/Generateur_AURA_FDM/geometrie_fdm.py"
    spec=importlib.util.spec_from_file_location("aura_fdm_r03",path)
    value=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def coupler_pocket(bench,body,x):
    g=bench.g
    g.union(body,g.rounded(x+5.75,x+11.4,11.65,15.8,-3.4,4.5,1.3))
    g.cut(body,g.box(x-4.25,x+10.5,8.35,13.30,-4.4,4.4))
    g.cut(body,g.cyl((x+8,12.5,0),(x+8,16.1,0),.94),
          g.cyl((x,12.65,0),(x,15.9,0),2.45))


def passive_stop(bench,body,x):
    g=bench.g
    g.union(body,g.rounded(x+2.8,x+12.15,-15.0,-11.85,-9.4,4.1,1.4))
    holes=[]
    for a in range(-1,RANGE+3,2):
        z=-9*math.sin(math.radians(a))
        cx=x+9*math.cos(math.radians(a))
        holes.append(g.cyl((cx,-15.5,z),(cx,-11.35,z),1.23))
    g.cut(body,g.union(holes[0],*holes[1:]))


def fork(bench,form):
    g=bench.g
    base=g.rounded(-55,-11,-28,28,-19.0,-9.0,4.6)
    frame=g.rounded(-50,-12.0,-16,16,-9.8,8.9,4)
    g.union(base,frame)
    for lug in form.finger_fork(0,-28):
        g.union(base,lug)
    coupler_pocket(bench,base,0)
    passive_stop(bench,base,0)
    g.cut(base,g.cyl((0,-11.7,0),(0,11.7,0),15.6))
    for y in (-21,21):
        g.cut(base,g.cyl((-40,y,-20),(-40,y,-8.4),2.3))
    return base


def put_rings(bench,i,x,parent,link):
    g=bench.g
    where=(x,0,0)
    bushing=bench.ring(0,0,-11.50,-8.50,2.25,1.525)
    bench.part(f"Palier_{i}",f"Bague igus GSM-0304-03 · P{i}",bushing,"ice",where,typed="igus GSM-0304-03")
    bench.rigid(f"Palier_{i}",link)
    pin=g.cyl((0,-15.9,0),(0,-8.48,0),1.50)
    bench.part(f"Axe_{i}",f"Axe passif acier Ø3, L7,4 · P{i}",pin,"metal",where)
    bench.rigid(f"Axe_{i}",parent)
    washer=bench.ring(0,0,-16.55,-15.02,3.5,1.51)
    bench.part(f"Bague_arret_{i}",f"Bague de retenue Ø3 · P{i}",washer,"metal",where)
    bench.rigid(f"Bague_arret_{i}",parent)
    stop=g.cyl((9,-14.85,0),(9,-8.9,0),.98)
    bench.part(f"Doigt_arret_{i}",f"Goupille de butée Ø2 · P{i}",stop,"accent",where)
    bench.rigid(f"Doigt_arret_{i}",link)


def actuate(bench,i,x,parent,link,motor):
    g=bench.g
    where=(x,0,0)
    g.cut(motor,g.cyl((0,9.15,0),(0,11.5,0),.74))
    bench.part(f"KST_{i}",f"KST X06 V6.0 · corps P{i}",motor,"dark",where,
               typed="KST X06 V6.0 · corps établi à partir du plan coté")
    bench.rigid(f"KST_{i}",link)
    for p in (-7,17):
        screw=g.cyl((p,.64,0),(p,4.65,0),.80)
        g.union(screw,g.cyl((p,4.61,0),(p,6.08,0),1.59))
        tag=f"Vis_KST_{i}_{p}"
        bench.part(tag,"Vis de patte M2 × 4 et tête de référence",screw,"metal",where)
        bench.rigid(tag,link)
    # The horn and shaft face are aligned in the XZ plane.
    arm=g.rounded(-2.6,10,-2.05,2.05,-.84,.84,1.68)
    transform=bench.base.frame((0,12.28,0),roll=90)
    if not g.manager.transform(arm,transform):
        raise RuntimeError("Orientation du palonnier impossible.")
    top=g.cyl((0,11.50,0),(0,13.12,0),3.58)
    g.union(top,g.cyl((0,8.53,0),(0,11.57,0),3.63),arm)
    g.cut(top,g.cyl((0,8.30,0),(0,11.05,0),1.97),g.cyl((0,10.9,0),(0,13.4,0),.87))
    for p in (4.1,6.05,8.0):
        g.cut(top,g.cyl((p,11.3,0),(p,13.4,0),.845))
    tag=f"Palonnier_{i}"
    bench.part(tag,f"Palonnier 15T 7075 TLS0082 · P{i}",top,"metal",where,"y",
               typed="Tomas Liu Studio TLS0082 · épaisseurs et perçages à mesurer")
    bench.rigid(tag,parent)
    fast=g.cyl((8,11.48,0),(8,16.24,0),.80)
    g.union(fast,g.cyl((8,15.83,0),(8,17.18,0),1.45))
    bench.part(f"Liaison_horn_{i}","Vis liaison palonnier à R8 · M1,6 candidat",fast,"metal",where)
    bench.rigid(f"Liaison_horn_{i}",parent)
    hub_screw=g.cyl((0,9.2,0),(0,13.20,0),.70)
    g.union(hub_screw,g.cyl((0,13.13,0),(0,14.11,0),1.45))
    bench.part(f"Vis_spline_{i}","Vis centrale du palonnier · confirmer la vis fournie",hub_screw,"metal",where)
    bench.rigid(f"Vis_spline_{i}",tag)
    return bench.pivot(f"Moteur_P{i}",f"KST_{i}",tag,tag)


def phalanx(bench,forms,i):
    g=bench.g
    shell,motor=forms.finger(i)
    g.cut(shell,g.box(-6.4,12,8.45,11.65,-7.8,8.1),
          g.cyl((0,-11.75,0),(0,-8.46,0),2.26),
          g.cyl((9,-11.75,0),(9,-8.8,0),1.03),
          g.cyl((0,-11.72,0),(0,-8.43,0),1.55),
          g.cyl((13.1,-7.25,-3.0),(13.1,-7.25,-16),1.42))
    if i<3:
        coupler_pocket(bench,shell,LENGTHS[i-1])
        passive_stop(bench,shell,LENGTHS[i-1])
    return shell,motor


def cable_exit(g):
    return g.cyl((13.1,-7.25,-3.6),(13.1,-7.25,-12.4),1.15)


def build(app,base,util,report,write,export_archive,open_f3d,get_design):
    OUT.mkdir(exist_ok=True)
    bench=util.Bench(app,base,get_design,"Doigt motorisé et plaque d’essai")
    g=bench.g
    forms=source_geometry().Printable(base,g)
    bench.part("D00_Banc","Plaque ancrée et chape de départ",fork(bench,forms),"dark",print_face=0).isGrounded=True
    axes=[]
    previous="D00_Banc"
    for i,x in enumerate(ORIGINS,1):
        shell,motor=phalanx(bench,forms,i)
        name=f"D0{i}_Phalange"
        bench.part(name,f"Phalange motorisée {i}",shell,"white",(x,0,0),print_face=180)
        put_rings(bench,i,x,previous,name)
        axes.append(actuate(bench,i,x,previous,name,motor))
        cable=cable_exit(g)
        bench.part(f"Sortie_fil_{i}",f"Réserve câble PWM · P{i}",cable,"accent",(x,0,0))
        bench.rigid(f"Sortie_fil_{i}",name)
        previous=name
    document=bench.doc
    zero=[]
    sign=[]
    advances=[]
    for i,joint in enumerate(axes,1):
        motion=joint.jointMotion
        at=motion.rotationValue
        zero.append(at)
        local=base.point((17,0,0))
        before=local.copy()
        before.transformBy(bench.parts[f"D0{i}_Phalange"].transform2)
        util.apply_pose(motion,8,at)
        after=local.copy()
        after.transformBy(bench.parts[f"D0{i}_Phalange"].transform2)
        direction=1 if after.z<before.z else -1
        sign.append(direction)
        advances.append(round(10*before.distanceTo(after),3))
        util.apply_pose(motion,0,at)
    test=[(0,0,0)]
    for i in range(3):
        for value in (10,25,35,45,47,53):
            test.append(tuple(value if j==i else 0 for j in range(3)))
    test.extend((x,x,x) for x in (9,18,27,36,45))
    samples=[]
    for angles in test:
        for joint,angle,origin,direction in zip(axes,angles,zero,sign):
            util.apply_pose(joint.jointMotion,angle,origin,direction)
        overlap=bench.measure()
        samples.append({"commandes":angles,"interferences":overlap})
        adsk.doEvents()
    for joint,origin,direction in zip(axes,zero,sign):
        util.apply_pose(joint.jointMotion,0,origin,direction)
        limits=joint.jointMotion.rotationLimits
        lo,hi=sorted((origin,origin+direction*math.radians(RANGE)))
        limits.minimumValue=lo
        limits.maximumValue=hi
        limits.isMinimumValueEnabled=True
        limits.isMaximumValueEnabled=True
    data={"pivots_moteurs":len(axes),"liaisons":bench.root.asBuiltJoints.count,
          "deplacement_temoins_mm_pour_8deg":advances,"poses":samples}
    report["doigt"]=data
    write(report)
    out_file=OUT/"AURA-01_Doigt_Pilote.f3d"
    bench.camera((42,0,-5),(100,-165,116),214,OUT/"Doigt_ouvert.png")
    export_archive(bench.design,out_file)
    data["archive"]=out_file.name
    data["sha256"]=util.digest(out_file)
    data["fabrication"]=bench.export_prints(OUT)
    data["termine"]=True
    write(report)
    document.activate()
