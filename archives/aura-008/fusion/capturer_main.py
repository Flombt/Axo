"""Captures Fusion de la rotation du poignet et de la fermeture des cinq doigts."""

import json
from pathlib import Path
import sys

import adsk.core as core

sys.path.insert(0, str(Path(__file__).resolve().parent))

from construire_main import ARCHIVE, OUT, REPORT, TITLE, camera, capture, write_report
from finaliser_main import connect
from geometrie import point, vector


def view_hand(app, rig):
    occurrences = [rig.occ[key] for key in rig.flexion] + [rig.occ["07_Paume"]]
    bounds = [occ.boundingBox for occ in occurrences]
    minimum = [min(getattr(b.minPoint, axis) for b in bounds)*10 for axis in "xyz"]
    maximum = [max(getattr(b.maxPoint, axis) for b in bounds)*10 for axis in "xyz"]
    target = tuple((a+b)/2 for a,b in zip(minimum, maximum))
    viewport = app.activeViewport
    cam = viewport.camera
    cam.target = point(target)
    cam.eye = point(tuple(a+b for a,b in zip(target, (99, -169, 107))))
    cam.upVector = vector((0, 0, 1))
    cam.cameraType = core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.setExtents(173/10, 109/10)
    viewport.camera = cam
    viewport.refresh()
    return viewport


def run(_context: str):
    app = core.Application.get()
    doc = app.activeDocument
    if doc.name != TITLE or not doc.isSaved:
        raise RuntimeError("Ouvrir la version enregistrée de la main.")
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    cloud = doc.dataFile
    data["cloud"] = {"nom": doc.name, "projet": cloud.parentProject.name, "version":cloud.versionNumber,
                     "id": cloud.id, "url":cloud.fusionWebURL, "synchronise":cloud.isComplete}
    write_report(data)
    importer = app.importManager
    scratch = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(ARCHIVE)))
    rig = connect(scratch, data)
    home = (0, 0, 0, 0, 0)
    up = (0, 8, 10, -30, 0)
    rolled = (0, 8, 10, 34, 0)
    closed = (0, 8, 10, 34, 1)
    phases = (
        (home, up, 26, 5, "bras"),
        (up, rolled, 26, 7, "main"),
        (rolled, closed, 26, 9, "main"),
        (closed, rolled, 23, 4, "main"),
        (rolled, home, 26, 8, "bras"),
    )
    output = OUT/"_images_demo"
    output.mkdir(exist_ok=True)
    index = 0
    for start, finish, frames, pause, plan in phases:
        rig.position(start)
        if plan == "bras":
            viewport = camera(app, movie=True)
        elif start == up:
            viewport = view_hand(app, rig)
        for n in range(frames+pause):
            t = min(1, n/(frames-1))
            t = t*t*(3-2*t)
            rig.position(tuple(a+(b-a)*t for a,b in zip(start, finish)))
            viewport.refresh()
            capture(viewport, output/f"{index:04d}.png", 1200, 750, transparent=True)
            index += 1
    rig.position(home)
    viewport = camera(app, detail=True)
    cam = viewport.camera
    cam.target, cam.eye = point((150, -2, 96)), point((223, -162, 19))
    cam.setExtents(166/10, 121/10)
    viewport.camera = cam
    viewport.refresh()
    capture(viewport, OUT/"AURA-01_Paume_transmission.png", 1400, 1000, transparent=True)
    scratch.close(False)
    doc.activate()
    camera(app)
    data["video"] = {"images_fusion":index, "cadence":24, "nom":"AURA-01_Poignet_Phalanges.mp4"}
    write_report(data)
    print(json.dumps({"cloud":data["cloud"],"images":index},ensure_ascii=False))
