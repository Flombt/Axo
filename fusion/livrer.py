"""Vues natives, éprouvettes et exports d’une copie Fusion de la V5 stabilisée."""
import json
import math
from pathlib import Path

import adsk.core as core
import adsk.fusion as fusion

from stabiliser import Model, box, cut, cylinder, get_attr, mm
from controle_cao import TOL_MM, solve, write


def bearing_coupon():
    block=box((0,0,4.5),(96,32,9))
    for x, radius in ((-31,13.0),(0,13.12),(31,13.24)):
        cut(block,cylinder((x,0,-1),(x,0,10),11),
            cylinder((x,0,.95),(x,0,10),radius))
    return block


def fastener_coupon():
    block=box((0,0,4),(84,25,8))
    for x,d in ((-35,2.05),(-25,2.25),(-15,3.18),(-5,3.38),(5,5.25),(15,5.50),(25,5.70),(35,10.2)):
        cut(block,cylinder((x,5,-1),(x,5,9),d/2),
            cylinder((x,-13,4),(x,0,4),d/2))
    return block


def servo_coupon(micro):
    if micro:
        body=box((0,0,2.7),(43,22,5.4))
        empty=box((0,0,2.7),(23.4,12.7,8.0))
        hole_x,hole_y,r=14,0,1.1
    else:
        body=box((0,0,2.7),(58,29,5.4))
        empty=box((0,0,2.7),(41.0,20.15,8.0))
        hole_x,hole_y,r=24.6,5.1,1.45
    cut(body,empty)
    for x in (-hole_x,hole_x):
        for y in set((-hole_y,hole_y)):
            cut(body,cylinder((x,y,-.2),(x,y,5.6),r))
    return body


def inserts_coupon():
    block = box((0,0,4),(46,18,8))
    for x,d in ((-14,4.0),(0,4.25),(14,4.50)):
        cut(block,cylinder((x,0,-1),(x,0,9),1.4),cylinder((x,0,2),(x,0,9),d/2))
    return block


def coupons(m, folder):
    doc=m.app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    try:
        d=fusion.Design.cast(m.app.activeProduct)
        d.designType=fusion.DesignTypes.DirectDesignType
        solids=(
            ("Coupon_6000",bearing_coupon()),
            ("Coupon_Axes",fastener_coupon()),
            ("Coupon_SG90",servo_coupon(True)),
            ("Coupon_MG996R",servo_coupon(False)),
            ("Coupon_Inserts",inserts_coupon())
        )
        rows=[]
        for name, b in solids:
            body=d.rootComponent.bRepBodies.add(b)
            assert body and body.isSolid and body.lumps.count==1,name
            mesh_calc=body.meshManager.createMeshCalculator()
            mesh_calc.surfaceTolerance=.033/10
            mesh=mesh_calc.calculate()
            rows.append({"part":name,"v":[[round(x,6) for x in mm(p)] for p in mesh.nodeCoordinates],
                         "f":list(mesh.nodeIndices),"volume_mm3":body.volume*1000})
        write(folder/"coupons_natifs.json",rows)
    finally:
        doc.close(False)
        m.doc.activate()


def shot(m, folder, name, keep, orientation, pose, wire=False):
    actual,err=solve(m,pose)
    assert err<=.02, (name,err)
    for key,occ in m.occ.items():
        occ.isLightBulbOn=key in keep
    viewport=m.app.activeViewport
    camera=viewport.camera
    camera.viewOrientation=orientation
    camera.isSmoothTransition=False
    camera.isFitView=True
    viewport.camera=camera
    style = "WireframeVisibleEdgesOnlyVisualStyle" if wire else "ShadedWithVisibleEdgesVisualStyle"
    if hasattr(core.VisualStyles,style):
        viewport.visualStyle=getattr(core.VisualStyles,style)
    viewport.refresh()
    assert viewport.saveAsImageFile(str(folder/name),1500,950),name


def visuals(m, folder):
    folder.mkdir(parents=True,exist_ok=True)
    display={k:o.isLightBulbOn for k,o in m.occ.items()}
    style=m.app.activeViewport.visualStyle
    camera=m.app.activeViewport.camera
    vis={k for k in m.occ if m.solids(k,True) and not k.startswith("Tendon_")}
    o=core.ViewOrientations
    try:
        shot(m,folder,"01_fusion_ensemble.png",vis,o.IsoTopRightViewOrientation,{})
        shot(m,folder,"02_fusion_plan_table.png",vis,o.FrontViewOrientation,{"J2":-21,"J3":-32,"J7":32},True)
        shot(m,folder,"03_fusion_axe_creux.png",{k for k in vis if k.startswith(
            ("Axe_J1","01_","02_","R6000","Faisceau_Socle","Faisceau_Tourelle","J1","Entretoise","Collier","Pied_Rehausse"))},
             o.IsoTopRightViewOrientation,{},True)
        shot(m,folder,"04_fusion_pince.png",{k for k in vis if len(k)==2 or k.startswith(
            ("11_","12_","Vis_","Peigne_","Capot_Paume"))},o.IsoTopRightViewOrientation,
             {"Servo_P":92,"Servo_I":92})
        shot(m,folder,"05_fusion_compensation.png",{k for k in vis if k.startswith(
            ("J2_Chape","J3_Chape","Ressort_","Axe_Ressort","Tige_Ressort","05_","Boucle_"))},
             o.FrontViewOrientation,{},True)
    finally:
        m.pose({})
        for key,occ in m.occ.items():
            occ.isLightBulbOn=display[key]
        m.app.activeViewport.visualStyle=style
        m.app.activeViewport.camera=camera


def samples_animation(m,folder):
    states=[]
    for i in range(37):
        t = i/36
        q = {"J1":30*math.sin(2*math.pi*t),"J2":8*math.sin(2*math.pi*t),
             "J3":14*math.sin(2*math.pi*t),"J7":18*math.sin(2*math.pi*t)}
        if t>=1/3:
            f=math.sin(math.pi*(t-1/3)/(2/3))**2
            q.update(Servo_P=92*f, Servo_I=92*f, Servo_M=24*f)
        q={k:round(v,1) for k,v in q.items()}
        actual,err=solve(m,q)
        if err>.02:
            raise RuntimeError("Animation refusée à l'image "+str(i))
        states.append({"frame":i,"angle":q,"transform":{k:o.transform2.asArray() for k,o in m.occ.items()}})
    m.pose({})
    write(folder/"animation_native.json",states)


def step_and_f3d(m, root):
    m.pose({})
    ex=m.design.exportManager
    step=root/"manufacturing/AURA-01.step"
    cad=root/"fusion/AURA-01.f3d"
    stage=cad.with_name("AURA-01.stabilisation.f3d")
    assert ex.execute(ex.createSTEPExportOptions(str(step))),str(step)
    assert ex.execute(ex.createFusionArchiveExportOptions(str(stage))),str(stage)
    stage.replace(cad)
