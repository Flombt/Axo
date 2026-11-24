"""Reprend la paume enregistrée, vérifie les liaisons et actualise les exports."""

import json
from pathlib import Path
import sys

import adsk.core as core
import adsk.fusion as fusion

sys.path.insert(0, str(Path(__file__).resolve().parent))

from construire_main import (
    BASE_RANGES, FIXED_AXES, OUT, REPORT, TAG, TITLE, Brazo, camera, capture,
    export_archive, export_prints, get_design, write_report,
)
from formes_articulees import ArticulatedForms, WIND


def connect(doc, data):
    rig = Brazo.__new__(Brazo)
    rig.design = get_design(doc)
    rig.root = rig.design.rootComponent
    forms = ArticulatedForms.__new__(ArticulatedForms)
    forms.design = rig.design
    forms.manager = fusion.TemporaryBRepManager.get()
    rig.forms = forms
    rig.occ, rig.prints = {}, {}
    rig.print_groups = {key: entry["reference"] for entry in data["nomenclature"]
                        for key in entry["instances"]}
    orientations = {"02_Socle": 180, "03_Tourelle": 180, "04_Segment_1": 90,
                    "07_Paume": 180, "10_Tambour": -90}
    hardware_labels = {
        "MG996R · Épaule J2": "SERVO_J2", "MG90S · Coude J3": "SERVO_J3",
        "MG90S · Rotation du poignet": "SERVO_J7",
        "MG90S · Fermeture des cinq doigts": "SERVO_T1",
        "Palonnier J2 · enveloppe": "PAL_J2", "Palonnier J3 · enveloppe": "PAL_J3",
        "Axe passif M3 · J3": "AXE_J3", "Palonnier de roulis · enveloppe": "PAL_J7",
        "Palonnier du tambour · enveloppe": "PAL_T1",
    }
    for occ in rig.root.occurrences:
        part = next((b for b in occ.bRepBodies if b.name.startswith("FDM · ")), None)
        if part:
            key = part.name.split(" · ")[1]
            rig.prints[key] = occ, part.name, orientations.get(key, 0)
        else:
            label = occ.component.name
            key = hardware_labels.get(label, label)
        rig.occ[key] = occ
    assert len(rig.occ) == rig.root.occurrences.count
    joints = {j.name.split(" · ")[0]:j for j in rig.root.asBuiltJoints}
    rig.joints = {code: (joints[name].jointMotion, axis, limits)
                  for code,name,axis,limits in zip(FIXED_AXES, ("J1","J2","J3","J7"),
                                                   ("z","y","y","x"), BASE_RANGES)}
    rig.joints["10_Tambour"] = joints["T1"].jointMotion, "y", (-2, WIND+2)
    rig.flexion = data["angles_flexion_nominale_deg"]
    for key, limit in rig.flexion.items():
        rig.joints[key] = joints[key].jointMotion, "y", (-1.5, limit+2)
    rig.slider = joints["T2"]
    rig.native_links = True
    rig.calibration = data["calibration"]
    rig.slider_zero = data["calibration_traverse"]
    return rig


def run(_context: str):
    app = core.Application.get()
    doc = app.activeDocument
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    rig = connect(doc, report)
    tag = rig.root.attributes.itemByName("AURA-01", "Reference")
    if not (doc.name == TITLE and doc.isSaved and tag and tag.value == TAG):
        raise RuntimeError("Ouvrir la copie AURA-008 enregistrée.")

    occ = rig.occ["07_Paume"]
    comp = occ.component
    build = comp.features.baseFeatures.item(0)
    palm = rig.forms.palm()
    if palm.lumps.count != 1 or not palm.isSolid:
        raise RuntimeError("La paume doit rester un solide.")
    if not build.startEdit():
        raise RuntimeError("Impossible d’ouvrir la paume pour percer les passages.")
    source = next(b for b in build.sourceBodies if b.name == "FDM · 07_Paume")
    if not build.updateBody(source, palm):
        raise RuntimeError("Fusion a refusé les nouveaux perçages.")
    if not build.finishEdit():
        raise RuntimeError("Impossible de terminer la reprise de la paume.")

    poses, errors, moments = rig.check()
    report.update({"poses": len(poses), "erreurs": errors, "couple_statique": moments})
    write_report(report)
    if errors:
        raise RuntimeError(f"Contacts à vérifier : {errors[:2]}")
    camera(app)
    report["archive"] = export_archive(app, doc, rig)
    report["nomenclature"] = export_prints(app, rig)
    doc.activate()
    hero = camera(app)
    capture(hero, OUT/"AURA-01_Bras_Main_Poignet.png", 1740, 1030, transparent=True)
    view = camera(app, detail=True)
    capture(view, OUT/"AURA-01_Main_ouverte.png", 1520, 985, transparent=True)
    rig.position((0, 0, 0, 0, 1))
    view.refresh()
    capture(view, OUT/"AURA-01_Main_fermee.png", 1520, 985, transparent=True)
    rig.position((0, 0, 0, 0, 0))
    camera(app)
    if not doc.save("Passages accessibles pour les cinq élastiques de rappel, contrôlés dans Fusion"):
        raise RuntimeError("Enregistrement des passages débouchants refusé.")
    write_report(report)
    print(json.dumps({"document": doc.name, "pose": len(poses),
                      "collisions": len(errors), "couples": moments}, ensure_ascii=False))
