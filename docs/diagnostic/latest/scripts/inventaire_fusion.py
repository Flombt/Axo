"""Inventaire descriptif du document Fusion actif, exécutable sans modifier la CAO."""
import json
import math
import os
from pathlib import Path

import adsk.core as core
import adsk.fusion as fusion

PROJECT_ROOT = (Path(os.environ["AURA_PROJECT_ROOT"]) if "AURA_PROJECT_ROOT" in os.environ
                else Path(__file__).resolve().parents[4])
OUTPUT = PROJECT_ROOT / "docs/diagnostic/latest/preuves"


def xyz(value, factor=10):
    return [round(value.x * factor, 6), round(value.y * factor, 6), round(value.z * factor, 6)]


def bounds(box):
    return [xyz(box.minPoint), xyz(box.maxPoint)]


def record_body(body):
    mass = body.physicalProperties
    diameters = {}
    for face in body.faces:
        cylinder = core.Cylinder.cast(face.geometry)
        if cylinder:
            diameter = round(cylinder.radius * 20, 4)
            diameters[diameter] = diameters.get(diameter, 0) + 1
    return {
        "name": body.name, "solid": body.isSolid, "faces": body.faces.count,
        "bounds_mm": bounds(body.preciseBoundingBox),
        "volume_mm3": round(body.volume * 1000, 5),
        "centroid_mm": xyz(mass.centerOfMass), "material_fusion": body.material.name,
        "cylinders_diameter_mm": sorted(diameters.items()),
    }


def joint_record(joint):
    motion = fusion.RevoluteJointMotion.cast(joint.jointMotion)
    item = {"name": joint.name, "type": str(joint.jointMotion.jointType),
            "one": joint.occurrenceOne.name if joint.occurrenceOne else None,
            "two": joint.occurrenceTwo.name if joint.occurrenceTwo else None}
    if motion:
        limits = motion.rotationLimits
        item["angle_deg"] = round(math.degrees(motion.rotationValue), 6)
        item["limits_deg"] = [round(math.degrees(limits.minimumValue), 6) if limits.isMinimumValueEnabled else None,
                              round(math.degrees(limits.maximumValue), 6) if limits.isMaximumValueEnabled else None]
        item["axis"] = xyz(motion.rotationAxisVector, 1)
        item["pivot_mm"] = xyz(joint.geometry.origin) if joint.geometry else None
    return item


def run(_context):
    app = core.Application.get()
    doc = app.activeDocument
    datafile = doc.dataFile
    design = fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    if datafile.id != "urn:adsk.wipprod:dm.lineage:S7DLYnxoTsq4-clhF52BRA":
        raise RuntimeError("Le document Fusion actif n’est pas la V5 roulis auditée.")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    occurrences = [
        {"name": occ.name, "component": occ.component.name, "visible": occ.isLightBulbOn,
         "origin_mm": xyz(occ.transform2.translation), "bodies": [record_body(b) for b in occ.bRepBodies]}
        for occ in root.allOccurrences
    ]
    data = {
        "document": doc.name, "id": datafile.id, "version": datafile.versionNumber,
        "latest": datafile.latestVersionNumber, "fusion": app.version, "modified": doc.isModified,
        "units": design.unitsManager.defaultLengthUnits, "root_bbox_mm": bounds(root.preciseBoundingBox),
        "occurrences": occurrences, "joints": [joint_record(j) for j in root.asBuiltJoints],
        "links": [link.name for link in root.motionLinks],
    }
    (OUTPUT / "fusion_actif.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"version": data["version"], "occurrences": len(occurrences),
                      "revolute": [j for j in data["joints"] if "angle_deg" in j]}, ensure_ascii=False))
