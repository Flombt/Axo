"""Capture une démonstration cinématique à partir de l’archive r02."""

import json
from pathlib import Path
import sys
import tempfile

import adsk.core as core

OUT = Path(__file__).resolve().parent
sys.path.insert(0,str(OUT))
from construire_montage import ARCHIVE, REPORT, Workshop, camera, capture, get_design
from construire_main import BASE_RANGES, FIXED_AXES
from formes_articulees import WIND
from capturer_main import view_hand


def connect(document, data):
    rig = Workshop.__new__(Workshop)
    rig.design = get_design(document)
    rig.root = rig.design.rootComponent
    rig.occ = {}
    for occ in rig.root.occurrences:
        for body in occ.bRepBodies:
            if body.name.startswith("FDM · "):
                rig.occ[body.name.split(" · ",1)[1]] = occ
    joints = {j.name.split(" · ",1)[0]:j for j in rig.root.asBuiltJoints}
    rig.joints = {code:(joints[name].jointMotion, axis, limits)
                  for code,name,axis,limits in zip(FIXED_AXES,("J1","J2","J3","J7"),
                                                   ("z","y","y","x"),BASE_RANGES)}
    rig.joints["10_Tambour"] = joints["T1"].jointMotion,"y",(-2,WIND+2)
    rig.flexion = data["angles_flexion_nominale_deg"]
    for code, limit in rig.flexion.items():
        rig.joints[code] = joints[code].jointMotion,"y",(-1.5,limit+2)
    rig.slider = joints["T2"]
    rig.calibration = data["calibration"]
    rig.slider_zero = data["calibration_traverse"]
    rig.native_links = False
    for link in rig.root.motionLinks:
        link.isSuppressed = True
    return rig


def run(_context: str):
    app=core.Application.get()
    src=app.activeDocument
    importer=app.importManager
    document=importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(ARCHIVE)))
    document.name="AURA-009 essai vidéo"
    rig=connect(document,json.loads(REPORT.read_text(encoding="utf-8")))
    home=(0,0,0,0,0)
    raised=(0,10,14,0,0)
    wrist_left=(0,10,14,-32,0)
    wrist_right=(0,10,14,28,0)
    grip=(0,10,14,28,1)
    shots=[
        (home,raised,27,8,"bras"),
        (raised,wrist_left,24,5,"main"),
        (wrist_left,wrist_right,28,6,"main"),
        (wrist_right,grip,25,10,"main"),
        (grip,wrist_right,22,6,"main"),
        (wrist_right,home,26,10,"bras"),
    ]
    target=Path(tempfile.mkdtemp(prefix="Aura009_R02_Fusion_"))
    index=0
    for start,finish,samples,pause,view in shots:
        rig.position(start)
        viewport=camera(app,movie=True) if view=="bras" else view_hand(app,rig)
        for n in range(samples+pause):
            t=min(1,n/(samples-1))
            u=t*t*(3-2*t)
            rig.position(tuple(a+(b-a)*u for a,b in zip(start,finish)))
            viewport.refresh()
            capture(viewport,target/f"{index:04d}.png",1200,750,transparent=True)
            index+=1
    document.close(False)
    src.activate()
    print(json.dumps({"dossier":str(target),"images":index,"cadence":20},ensure_ascii=False))
