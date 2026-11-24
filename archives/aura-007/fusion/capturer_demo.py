"""Capture le geste sur les liaisons natives de l'archive Fusion."""

import json
from pathlib import Path
import sys

import adsk.core as core
import adsk.fusion as fusion

sys.path.insert(0, str(Path(__file__).resolve().parent))

from construire_table import (
    ARCHIVE, CHECKS, LIMITES, OUT, POSES, Assembly, capture, get_design, set_camera, write,
)
from geometrie import point


def run(_context: str):
    app = core.Application.get()
    opened = app.activeDocument
    report = json.loads(CHECKS.read_text(encoding="utf-8"))
    info = opened.dataFile
    if not opened.isSaved or info is None:
        raise RuntimeError("Ouvrir le bras enregistré avant la capture.")
    report["cloud"] = {
        "nom": opened.name, "projet": info.parentProject.name, "version": info.versionNumber,
        "fusion_id": info.id, "url": info.fusionWebURL, "traitement_termine": info.isComplete,
    }
    write(report)
    importer = app.importManager
    scratch = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(ARCHIVE)))
    design = get_design(scratch)
    root = design.rootComponent

    # Reattach the motion driver to the occurrences in the imported document.
    rig = Assembly.__new__(Assembly)
    rig.occ = {}
    rig.joints = {}
    revolute = [j for j in root.asBuiltJoints
                if j.jointMotion.jointType == fusion.JointTypes.RevoluteJointType]
    revolute.sort(key=lambda j: j.name)
    for joint, code, axis, limits in zip(revolute, ("03_Tourelle", "04_Segment_1", "05_Segment_2"),
                                          ("z", "y", "y"), LIMITES):
        rig.occ[code] = next(o for o in root.occurrences if o.component.name.startswith(code[:2] + " ·"))
        rig.joints[code] = (joint.jointMotion, axis, limits)
    rig.calibrate()
    view = set_camera(app)
    # Leave headroom for the gesture while keeping the entire base in shot.
    camera = view.camera
    camera.target, camera.eye = point((53, -1, 75)), point((141, -390, 240))
    camera.setExtents(350 / 10, 216 / 10)
    view.camera = camera
    view.refresh()

    directory = OUT / "_images_demo"
    directory.mkdir(exist_ok=True)
    index = 0
    for (start, finish, count, pause) in (
        (POSES[0][1], POSES[1][1], 39, 9),
        (POSES[1][1], POSES[2][1], 40, 9),
        (POSES[2][1], POSES[3][1], 37, 10),
    ):
        for step in range(count + 1):
            t = step / count
            t = t * t * (3 - 2 * t)
            rig.move([a + (b - a) * t for a, b in zip(start, finish)])
            view.refresh()
            capture(view, directory / f"{index:04}.png", 1200, 720, transparent=True)
            index += 1
        for _ in range(pause):
            capture(view, directory / f"{index:04}.png", 1200, 720, transparent=True)
            index += 1
    rig.move((0, 0, 0))
    cover = next(o for o in root.occurrences if o.component.name.startswith("02 ·"))
    cover.isLightBulbOn = False
    for occ in root.occurrences:
        if occ.component.name.startswith(("08 ·", "09 ·")):
            occ.isLightBulbOn = False
    closeup = set_camera(app, detail=True)
    capture(closeup, OUT / "AURA-01_Implantation_moteurs.png", 1550, 1070, transparent=True)
    scratch.close(False)
    opened.activate()
    set_camera(app)
    report["demonstration"] = {"source": "Liaisons natives Fusion", "images": index, "cadence_images_s": 24}
    write(report)
    print(json.dumps({"cloud": report["cloud"], "images_capturées": index}, ensure_ascii=False))
