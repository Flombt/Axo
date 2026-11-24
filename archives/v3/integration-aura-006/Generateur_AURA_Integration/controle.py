"""Réouverture des bancs exportés et contrôle d'accès par déplacement d'un solide."""

from pathlib import Path

import adsk.fusion as fusion


ROOT = Path(__file__).resolve().parents[1]
REVISION = 1


def objects(component):
    roster = {}
    for occ in component.allOccurrences:
        for body in occ.bRepBodies:
            if body.isSolid and body.name != "Repère local":
                roster[body.name] = (body.nativeObject or body, occ.transform2)
    return roster


def world(manager, item):
    copy = manager.copy(item[0])
    if not manager.transform(copy, item[1]):
        raise RuntimeError("Transformation du solide d’archive impossible.")
    return copy


def intersect_boxes(a, b):
    return all(ma <= ni and mi <= na for ma, mi, na, ni in
               zip(a.minPoint.asArray(), b.minPoint.asArray(), a.maxPoint.asArray(), b.maxPoint.asArray()))


def travel(base, manager, roster, part, keys, direction, offsets):
    envelope = world(manager, roster[part])
    comparison = {name: world(manager, roster[name]) for name in keys}
    rows = []
    for offset in offsets:
        candidate = manager.copy(envelope)
        manager.transform(candidate, base.frame(tuple(offset * x for x in direction)))
        box = candidate.boundingBox
        hits = []
        for name, fixed in comparison.items():
            if not intersect_boxes(box, fixed.boundingBox):
                continue
            temp = manager.copy(candidate)
            if manager.booleanOperation(temp, fixed, fusion.BooleanTypes.IntersectionBooleanType) and temp.volume * 1000 > .002:
                hits.append({"piece": name, "mm3": round(temp.volume * 1000, 3)})
        rows.append({"translation_mm": offset, "interferences": hits})
    return rows


def native_joins(root):
    return {j.name: j for j in root.asBuiltJoints
            if fusion.RevoluteJointMotion.cast(j.jointMotion)}


def build(app, base, util, report, write, export_archive, open_f3d, get_design):
    manager = fusion.TemporaryBRepManager.get()
    current = app.activeDocument
    results = {}
    for module, path in (("doigt", ROOT / "01_Doigt/AURA-01_Doigt_Pilote.f3d"),
                          ("epaule", ROOT / "02_Epaule/AURA-01_J2_Epaule_Pilote.f3d")):
        doc = open_f3d(app, path)
        try:
            design = get_design(doc)
            root = design.rootComponent
            roster = objects(root)
            pivots = native_joins(root)
            tests = {}
            info = {"archive": path.name, "sha256": util.digest(path), "pivots": sorted(pivots),
                    "composants": root.occurrences.count,
                    "historique_parametrique": design.designType == fusion.DesignTypes.ParametricDesignType}
            if module == "doigt":
                for i in (1, 2, 3):
                    part, shell = f"KST_{i}", f"D0{i}_Phalange"
                    tests[f"sortie_moteur_{i}_vers_le_bas"] = travel(base, manager, roster, part,
                                                                     [shell], (0, 0, -1), range(0, 17, 1))
            else:
                keys = ["J20_Socle", "J21_Levier", "J22_Cartouche", "Poulie_16", "Poulie_64",
                        "Arbre_entree", "Arbre_J2", "Courroie", "ROBOTIS_XM540", "Frein_stator"]
                tests["carter_sans_vis_vers_exterieur"] = travel(base, manager, roster, "J23_Carter",
                                                                  keys, (0, 1, 0), range(0, 66, 3))
                tests["moteur_sans_palonnier_vers_arriere"] = travel(base, manager, roster, "ROBOTIS_XM540",
                                                                     ["J20_Socle", "J22_Cartouche", "Support_XM540",
                                                                      "J21_Levier", "Frein_stator"],
                                                                     (0, -1, 0), range(0, 55, 2))
            info["chemins"] = tests
            results[module] = info
        finally:
            doc.close(False)
    report["controle"] = {"bancs": results, "termine": True}
    write(report)
    if current:
        current.activate()
