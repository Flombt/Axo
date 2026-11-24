"""Audit d'interférences et génération de la version FDM dans Autodesk Fusion."""

from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import traceback

import adsk
import adsk.core as core
import adsk.fusion as fusion


SOURCE = Path(__file__).resolve().parent
OUT = SOURCE.parent
BASELINE = OUT.parent / "AURA-01_V3_Main-articulee_r02.f3d"
REPORT = OUT / "Verification_FDM_r03.json"
TITLE = "AURA-01 V3 FDM r03"


def write_report(report):
    pending = REPORT.with_suffix(".tmp")
    pending.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pending.replace(REPORT)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def open_f3d(app, file):
    importer = app.importManager
    document = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(file)))
    if document is None:
        raise RuntimeError(f"Ouverture Fusion refusée pour {file.name}")
    return document


def get_design(document):
    result = fusion.Design.cast(document.products.itemByProductType("DesignProductType"))
    if result is None:
        raise RuntimeError("Le document ne contient pas de conception Fusion.")
    return result


def overlap_results(design, bodies):
    inputs = core.ObjectCollection.create()
    for body in bodies:
        inputs.add(body)
    options = design.createInterferenceInput(inputs)
    options.areCoincidentFacesIncluded = False
    results = design.analyzeInterference(options)
    if results is None:
        raise RuntimeError("Fusion n'a renvoyé aucun résultat d'interférence.")
    collisions = []
    for i in range(results.count):
        r = results.item(i)
        volume = r.interferenceBody.volume * 1000
        if volume > 0.001:
            collisions.append((r.entityOne, r.entityTwo, volume))
    return collisions


def identify(entity):
    context = entity.assemblyContext
    owner = entity.parentComponent
    if not context and not owner:
        raise RuntimeError(f"Le propriétaire du corps {entity.name} est inconnu.")
    return (context.name if context else owner.name, entity.name)


def structural_at(design):
    return [
        b for occ in design.rootComponent.occurrences for b in occ.bRepBodies
        if not any(k in b.name.casefold() for k in (
            "axe", "pivot", "enveloppe moteur", "kst x06", "bague du pivot"))
    ]


def pair(first, other, volume):
    return {"a": identify(first), "b": identify(other), "volume_mm3": round(volume, 3)}


def audit_baseline(app, digest):
    document = open_f3d(app, BASELINE)
    try:
        design = get_design(document)
        root = design.rootComponent
        occurrences = list(root.occurrences)
        bodies = [b for o in occurrences for b in o.bRepBodies]
        structural = structural_at(design)
        collisions, internal = [], []
        for first, other, volume in overlap_results(design, structural):
            entry = pair(first, other, volume)
            (collisions if entry["a"][0] != entry["b"][0] else internal).append(entry)
        collisions.sort(key=lambda v: v["volume_mm3"], reverse=True)
        internal.sort(key=lambda v: v["volume_mm3"], reverse=True)
        return {"source": BASELINE.name, "sha256": digest, "reimport_fusion": True,
                "attribution": "occurrence ou composant propriétaire natif",
                "pivots": root.asBuiltJoints.count, "occurrences": len(occurrences),
                "corps_total": len(bodies), "corps_controles": len(structural),
                "interferences_entre_occurrences_a_HOME": len(collisions),
                "recouvrements_dans_les_occurrences_a_HOME": len(internal),
                "exemples_recouvrements_internes": internal[:12], "interferences": collisions}
    finally:
        document.close(False)


def compare_baseline(app, report):
    saved = json.loads((OUT.parent/"Verification_CAO.json").read_text(encoding="utf-8"))
    original = saved["pivots"]
    document = open_f3d(app, BASELINE)
    try:
        design = get_design(document)
        joints = {j.name.split(" · ", 1)[0]:fusion.RevoluteJointMotion.cast(j.jointMotion)
                  for j in design.rootComponent.asBuiltJoints}
        if set(joints) != set(original):
            raise RuntimeError("Noms des 22 pivots d'origine introuvables.")
        zeros = {k:m.rotationValue for k,m in joints.items()}
        metrics = {"poses_communes": 0, "poses_en_interference_r02": 0,
                   "poses_d_origine_refusees": [], "interferences": []}
        chosen = ("100 %", "/8", " 5/11", " 11/11")
        for sample in report["analyse_r03"]["poses_sans_interference"]:
            name, pose = sample["nom"], sample["angles_deg"]
            if name != "HOME" and not any(name.endswith(x) for x in chosen):
                continue
            if any(not original[k]["bornes_mecaniques_deg"][0] - .01 <= v <= original[k]["bornes_mecaniques_deg"][1] + .01
                   for k,v in pose.items()):
                continue
            expected = {k:zeros[k] + math.radians(original[k]["signe_natif"]*pose.get(k,0))
                        for k in joints}
            try:
                for k,motion in joints.items():
                    if abs(motion.rotationValue-expected[k]) > .00001:
                        motion.rotationValue = expected[k]
                if any(abs(joints[k].rotationValue-val)>math.radians(.13) for k,val in expected.items()):
                    raise RuntimeError("Angles d'origine non atteints.")
            except RuntimeError:
                metrics["poses_d_origine_refusees"].append(name)
                continue
            hits=[]
            for first, other, volume in overlap_results(design, structural_at(design)):
                entry=pair(first, other, volume)
                if entry["a"][0]!=entry["b"][0]:
                    hits.append(entry)
            metrics["poses_communes"] += 1
            if hits:
                metrics["poses_en_interference_r02"] += 1
                metrics["interferences"].append({"pose":name,"contacts":hits})
            adsk.doEvents()
        return metrics
    finally:
        document.close(False)


def run(_context):
    app = core.Application.get()
    report = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.is_file() else {}
    report.pop("erreur", None)
    analyse = report.get("analyse_r03")
    if analyse and "colis" in analyse:
        analyse["poses_sans_interference"] = analyse.pop("colis")
    report["application"] = app.version
    try:
        digest = sha256(BASELINE.read_bytes()).hexdigest()
        audit = report.get("audit_r02", {})
        verified = (report.get("etape") == "CAO et exports FDM contrôlés" and
                    report.get("archive") and (OUT/report["archive"]).is_file() and
                    sha256((OUT/report["archive"]).read_bytes()).hexdigest() == report.get("archive_sha256"))
        audit_stale = audit.get("sha256") != digest or "attribution" not in audit
        if audit_stale:
            report["etape"] = "Audit de la V3 r02"
            write_report(report)
            report["audit_r02"] = audit_baseline(app, digest)
        if verified:
            if audit_stale or "comparaison_r02" not in report:
                report["comparaison_r02"] = compare_baseline(app, report)
            report["etape"] = "CAO et exports FDM contrôlés"
            write_report(report)
            return
        report["etape"] = "Audit r02 terminé"
        write_report(report)
        builder = SOURCE / "construction.py"
        if not builder.is_file():
            return
        base = load_module(OUT.parent / "Generateur_AURA_V3/geometrie.py", "aura_base")
        geometry = load_module(SOURCE / "geometrie_fdm.py", "aura_fdm_geom")
        build = load_module(builder, "aura_fdm_builder")
        build.make(app, base, geometry, report, write_report, get_design, open_f3d, overlap_results, identify)
        if report["etape"] == "CAO et exports FDM contrôlés":
            report["comparaison_r02"] = compare_baseline(app, report)
            write_report(report)
    except Exception:
        report["erreur"] = traceback.format_exc()
        write_report(report)
        adsk.log(report["erreur"])
