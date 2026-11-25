"""Crée et vérifie une variante locale d'Axo_bras_final v1 dans Autodesk Fusion."""

import hashlib
import json
import math
import sys
from itertools import product
from pathlib import Path

import adsk.core as core
import adsk.fusion as fusion

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Axo bras final" / "Modèle 3D" / "Axo_bras_final.f3d"
FOLDER = ROOT / "Axo bras final - Capteurs"
NAME = "Axo bras final - Capteurs"
SHA_SOURCE = "b4e6b6ea1f3961df31049d50c2b16ee7164a069bb5c45df64d8f8aba220407a1"

sys.path.insert(0, str(ROOT / "fusion"))
sys.path.insert(0, str(ROOT / "docs" / "diagnostic" / "latest" / "scripts"))
previous_bytecode_setting = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    from stabiliser import boolean, box, cut, cylinder, get_attr, mm, point, put_attr
    from campagne_fusion import Assembly, AXES, unique_samples
finally:
    sys.dont_write_bytecode = previous_bytecode_setting

M5_ANCHORS = [(-61, -47), (-61, 47)]
PI_HOLES = list(product((-132.5, -83.5), (-39, 19)))
LID_HOLES = [(-140, -50), (-140, 50), (-79.5, -50), (-79.5, 50)]
CAM_MOUNT = [(-132, -12.9), (-132, 12.9)]
CAM_PCB = list(product((-10.5, 10.5), (36.8, 49.3)))


def cuboid(x, y, z):
    spans = (x, y, z)
    return box(tuple((lo + hi) / 2 for lo, hi in spans), tuple(hi - lo for lo, hi in spans))


def z_hole(x, y, z0, z1, radius, end_radius=None):
    return cylinder((x, y, z0), (x, y, z1), radius, end_radius)


def x_hole(y, z, x0, x1, radius, end_radius=None):
    return cylinder((x0, y, z), (x1, y, z), radius, end_radius)


def rounded_xy(x, y, z, r):
    x0, x1 = x
    y0, y1 = y
    body = cuboid((x0 + r, x1 - r), y, z)
    boolean(body, cuboid(x, (y0 + r, y1 - r), z))
    for cx, cy in product((x0 + r, x1 - r), (y0 + r, y1 - r)):
        boolean(body, z_hole(cx, cy, *z, r))
    return body


def rounded_yz(x, y, z, r):
    y0, y1 = y
    z0, z1 = z
    body = cuboid(x, (y0 + r, y1 - r), z)
    boolean(body, cuboid(x, y, (z0 + r, z1 - r)))
    for cy, cz in product((y0 + r, y1 - r), (z0 + r, z1 - r)):
        boolean(body, x_hole(cy, cz, *x, r))
    return body


def tray():
    body = rounded_xy((-147, -73), (-54, 54), (0, 28), 5)
    cut(body, rounded_xy((-144.2, -75.8), (-51.2, 51.2), (3.4, 29), 3))
    for x, y in M5_ANCHORS:
        boolean(body, rounded_xy((-80, -54), (y - 7, y + 7), (6.05, 12.05), 3))
        cut(body, z_hole(x, y, 5, 13, 2.8))

    # Fenêtres débouchantes USB/Ethernet, alimentation/HDMI et accès microSD.
    cut(body, cuboid((-135.5, -82), (39, 55), (6.5, 29)),
        cuboid((-148, -133), (-41, 6.5), (5.5, 29)),
        cuboid((-121, -90), (-55, -40), (3.1, 29)))

    for x, y in PI_HOLES:
        boolean(body, z_hole(x, y, 3.2, 8.3, 3.1))
        # Vis M2,5 par le dessous, tête entièrement au-dessus du plan de pose.
        cut(body, z_hole(x, y, -1, 9, 1.4),
            z_hole(x, y, -1, 2.4, 2.65))
    for x, y in LID_HOLES:
        boolean(body, z_hole(x, y, 3.2, 28, 3.9))
        cut(body, z_hole(x, y, 21.5, 28.5, 2.10))
    # Ouvertures d'entrée d'air sur la face latérale, en dehors de la microSD.
    for x in (-140, -135, -130, -125):
        cut(body, cuboid((x - 0.9, x + 0.9), (-55, -50), (6, 15)))
    return body


def lid():
    body = rounded_xy((-147, -73), (-54, 54), (28, 31), 5)
    for x, y in LID_HOLES:
        cut(body, z_hole(x, y, 27.5, 31.5, 1.65),
            z_hole(x, y, 29.5, 31.2, 1.65, 3.15))
    # Sortie du flux du refroidisseur, avec des ponts de 2,8 mm.
    for x in (-121, -115.4, -109.8, -104.2, -98.6, -93, -87.4):
        cut(body, rounded_xy((x - 1.4, x + 1.4), (-29, 29), (27, 32), 1.35))
    cut(body, rounded_xy((-139.2, -128.5), (-9.1, 9.1), (27, 32), 1.5))
    for x, y in CAM_MOUNT:
        cut(body, z_hole(x, y, 27, 32, 1.65),
            z_hole(x, y, 27.8, 29.5, 3.15, 1.65))
    return body


def camera_shell():
    body = rounded_yz((-147, -127), (-16.7, 16.7), (31, 60), 3.2)
    cut(body, rounded_yz((-144.4, -126.5), (-13.9, 13.9), (32.6, 58.1), 2))
    # La platine optique est plus haute que le rebord inférieur. La nappe descend dans le capot.
    cut(body, cuboid((-139.2, -126), (-9.1, 9.1), (30.8, 33.3)))
    for y, z in CAM_PCB:
        boolean(body, x_hole(y, z + 6, -144.8, -138, 2.35))
        cut(body, x_hole(y, z + 6, -142.3, -137.8, 1.48))
    for x, y in CAM_MOUNT:
        boolean(body, z_hole(x, y, 31, 36.2, 3.5))
        cut(body, z_hole(x, y, 30.5, 35.6, 2.1))
    # Ouverture optique conique, dégagement du bloc optique sur la face interne.
    cut(body, x_hole(0, 50, -147.3, -144.35, 8.0, 6.4),
        x_hole(0, 50, -144.6, -141.8, 6.4))
    for y in (-13.6, 13.6):
        boolean(body, x_hole(y, 46, -133, -127, 2.55))
        cut(body, x_hole(y, 46, -131.0, -126.8, 1.55))
    return body


def camera_back():
    body = rounded_yz((-127, -124.7), (-16.7, 16.7), (31, 60), 3.2)
    for y in (-13.6, 13.6):
        cut(body, x_hole(y, 46, -127.3, -124.4, 1.15),
            x_hole(y, 46, -126.0, -124.5, 1.15, 2.05))
    return body


def component(design, parent, key, label, shape, appearance, printable=True):
    assert shape.isSolid and shape.lumps.count == 1, key
    occurrence = parent.occurrences.addNewComponent(core.Matrix3D.create())
    comp = occurrence.component
    comp.name = label
    comp.partNumber = "AXO-CAP-" + key
    put_attr(comp, "Repere", key)
    put_attr(comp, "Impression", key if printable else "")
    feature = comp.features.baseFeatures.add()
    feature.name = label
    assert feature.startEdit()
    try:
        body = comp.bRepBodies.add(shape, feature)
        assert body, key
        body.name = key
    finally:
        assert feature.finishEdit()
    body = comp.bRepBodies.item(0)
    if appearance:
        body.appearance = appearance
    return body


def extents(body):
    bb = body.preciseBoundingBox
    return [list(mm(bb.minPoint)), list(mm(bb.maxPoint))]


def native(occurrence):
    return [[b.name, b.faces.count, round(b.volume * 1000, 5), extents(b)]
            for b in occurrence.component.bRepBodies if b.isSolid]


def signature(assembly):
    return {
        "occurrences": {k: [o.component.name, o.transform2.asArray(), native(o)]
                        for k, o in assembly.occ.items()},
        "joints": sorted((j.name, j.jointMotion.jointType)
                         for j in assembly.root.asBuiltJoints),
        "liens": sorted(link.name for link in assembly.root.motionLinks)
    }


def snapshot(viewport, img, eye, target, up, extent):
    camera = viewport.camera
    camera.cameraType = core.CameraTypes.OrthographicCameraType
    camera.eye = point(eye)
    camera.target = point(target)
    camera.upVector = core.Vector3D.create(*up)
    camera.viewExtents = extent / 10
    camera.isSmoothTransition = False
    viewport.camera = camera
    viewport.visualStyle = core.VisualStyles.ShadedVisualStyle
    viewport.refresh()
    if img is not None:
        assert viewport.saveAsImageFile(str(img), 1700, 1050)


def checks(assembly, new_world, electronic):
    """N'évalue que les interférences ajoutées par la variante."""
    tmp = fusion.TemporaryBRepManager.get()
    closest_box = (float("inf"), "", "", "")
    hits = []
    candidates = 0
    cases = list(unique_samples())
    for ends in product((-1, 1), repeat=len(AXES)):
        cases.append(("butées combinées", dict(zip(
            AXES, (sign * limit for sign, limit in zip(ends, AXES.values()))))))
    limits = [(key, body, extents(body)) for key, body in new_world.items()]
    pairs = [(a, b) for i, a in enumerate(limits) for b in limits[i + 1:]]

    def interference(a, b, pose):
        nonlocal candidates
        key1, body1, a_box = a
        key2, body2, b_box = b
        if any(a_box[1][i] <= b_box[0][i] + 0.0001
               or b_box[1][i] <= a_box[0][i] + 0.0001 for i in range(3)):
            return
        candidates += 1
        probe = tmp.copy(body1)
        op = fusion.BooleanTypes.IntersectionBooleanType
        if tmp.booleanOperation(probe, tmp.copy(body2), op):
            volume = probe.volume * 1000 if probe.lumps.count else 0
            if volume > 0.03:
                hits.append([pose, key1, key2, round(volume, 4)])

    for a, b in pairs:
        interference(a, b, "sous-assemblage fixe")
    for key, body in electronic.items():
        for limit in limits:
            interference((key, body, extents(body)), limit, "gabarit électronique")

    report = []
    for index, (label, wanted) in enumerate(cases):
        actual = assembly.position(wanted)
        error = max(abs(actual[k] - value) for k, value in wanted.items()) if wanted else 0
        if error > 0.04:
            assembly.position({})
            for step in range(1, 5):
                actual = assembly.position({key: value * step / 4 for key, value in wanted.items()})
            error = max(abs(actual[k] - value) for k, value in wanted.items())
        report.append({"pose": label, "angles_deg": wanted, "erreur_deg": round(error, 6),
                       "atteinte": error <= .04})
        if error > .04:
            continue
        for key, bodies in assembly.body.items():
            for body in bodies:
                bounds = extents(body)
                for limit in limits:
                    separation = math.sqrt(sum(max(0, bounds[0][i] - limit[2][1][i],
                                                   limit[2][0][i] - bounds[1][i]) ** 2
                                               for i in range(3)))
                    if key != "01_Platine" and separation > 0 and separation < closest_box[0]:
                        closest_box = (separation, label, key, limit[0])
                    interference((key, body, bounds), limit, index)
    assembly.position({})
    return {"poses": report, "boites_candidates": candidates,
            "approche_boites_hors_platine": closest_box, "interferences_mm3": hits}


def run(_context):
    app = core.Application.get()
    work = FOLDER / "Contrôles"
    work.mkdir(parents=True, exist_ok=True)
    status = work / "fusion.log"
    archive = FOLDER / (NAME + ".f3d")
    doc = None
    try:
        status.write_text("Import local\n", encoding="utf-8")
        assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SHA_SOURCE
        importer = app.importManager
        doc = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(SOURCE)))
        assert doc and not doc.isSaved
        source = Assembly()
        source.position({})
        initial = signature(source)
        design, root = source.design, source.root
        appearance = lambda key: source.occ[key].component.bRepBodies.item(0).appearance
        parent_occ = root.occurrences.addNewComponent(core.Matrix3D.create())
        parent_occ.component.name = "Module fixe · Vision et audio"
        parent_occ.isGrounded = True
        parent = parent_occ.component
        bodies = {}
        print_root = FOLDER / "Impression 3D" / "STL"
        print_root.mkdir(parents=True, exist_ok=True)
        export = design.exportManager
        stl_native = {}

        status.write_text("Création des solides\n", encoding="utf-8")
        for key, label, shape, color in [
            ("01_Bac_Pi5", "Bac Raspberry Pi 5 · deux ancrages M5", tray(), "01_Platine"),
            ("02_Couvercle", "Couvercle ventilé · démontable", lid(), "Coque_Socle"),
            ("03_Coque_Camera", "Coque optique · Camera Module 3 Wide", camera_shell(), "Coque_Socle"),
            ("04_Dos_Camera", "Dos démontable du module optique", camera_back(), "01_Platine"),
        ]:
            body = component(design, parent, key, label, shape, appearance(color))
            bodies[key] = body
            options = export.createSTLExportOptions(body, str(print_root / (key + ".stl")))
            options.meshRefinement = fusion.MeshRefinementSettings.MeshRefinementHigh
            assert export.execute(options), key
            stl_native[key] = {"volume_mm3": body.volume * 1000, "boite_mm": extents(body)}

        # Gabarits visuels séparés des solides imprimables.
        mock = parent.occurrences.addNewComponent(core.Matrix3D.create())
        mock.component.name = "Gabarits électroniques"
        mock.isLightBulbOn = False
        board = rounded_xy((-136, -80), (-42.5, 42.5), (8.3, 9.9), 3)
        for x, y in PI_HOLES:
            cut(board, z_hole(x, y, 7, 11, 1.35))
        pc_camera = rounded_yz((-138, -136.9), (-12.5, 12.5), (33.45, 57.31), 1.8)
        for y, z in CAM_PCB:
            cut(pc_camera, x_hole(y, z + 6, -139, -136, 1.1))
        mock_parts = [
            ("Pi_5", "Encombrement carte Raspberry Pi 5", board, "Pico"),
            ("USB_1", "Empilage USB-A 1", cuboid((-96.4, -82.1), (25, 45.5), (9.9, 25.6)), "R608_1"),
            ("USB_2", "Empilage USB-A 2", cuboid((-114.2, -99.6), (25, 45.5), (9.9, 25.6)), "R608_1"),
            ("Ethernet", "Encombrement Ethernet", cuboid((-134, -117.4), (22, 45.5), (9.9, 25.7)), "R608_1"),
            ("Refroidisseur", "Encombrement du refroidisseur actif",
             rounded_xy((-128.5, -86), (-39, 24.5), (9.9, 23.6), 3.5), "R608_1"),
            ("PCB_Camera", "Encombrement Camera Module 3 Wide", pc_camera, "Pico"),
            ("Objectif", "Gabarit optique Wide",
             x_hole(0, 50, -146.3, -138, 3.5, 4.7), "01_Platine"),
            ("Micro_USB", "Micro USB-A · enveloppe de référence",
             rounded_xy((-116.05, -97.75), (45.5, 58), (18, 25), 2.2), "01_Platine"),
        ]
        for key, label, shape, color in mock_parts:
            bodies[key] = component(design, mock.component, key, label, shape, appearance(color), False)
        mock.isLightBulbOn = True
        for o in mock.component.occurrences:
            o.isLightBulbOn = get_attr(o.component, "Repere") in {"Objectif", "Micro_USB"}
        put_attr(root, "Axo_Capteurs_Source_SHA256", SHA_SOURCE)
        put_attr(root, "Axo_Capteurs", "Module stationnaire autonome, révision 01")

        new_world, electronic = {}, {}
        print_keys = set(stl_native)
        for o in root.allOccurrences:
            key = get_attr(o.component, "Repere")
            if key in print_keys:
                new_world[key] = o.bRepBodies.item(0)
            elif key in bodies:
                electronic[key] = o.bRepBodies.item(0)
        status.write_text("Vérification des poses Fusion\n", encoding="utf-8")
        report = checks(source, new_world, electronic)
        if report["interferences_mm3"]:
            (work / "validation_provisoire.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            raise RuntimeError(report["interferences_mm3"][:10])
        assert len(source.occ) == 154

        mesh_data = {}
        for key, body in bodies.items():
            calc = body.meshManager.createMeshCalculator()
            calc.surfaceTolerance = .004
            data = calc.calculate()
            mesh_data[key] = {"sommets_mm": [mm(p) for p in data.nodeCoordinates],
                              "triangles": list(data.nodeIndices)}
        (work / "maillages_capteurs.json").write_text(json.dumps(mesh_data, separators=(",", ":")), encoding="utf-8")

        viewport = app.activeViewport
        snapshot(viewport, None, (-410, -570, 360), (45, 0, 60), (0, 0, 1), 520)
        assert export.execute(export.createFusionArchiveExportOptions(str(archive))), archive
        status.write_text("Réimportation et comparaison de la copie\n", encoding="utf-8")
        reopened = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(archive)))
        assert reopened and not reopened.isSaved
        check_design = fusion.Design.cast(app.activeProduct)
        rroot = check_design.rootComponent
        original_reopened = {
            get_attr(o.component, "Repere"): o for o in rroot.occurrences
            if get_attr(o.component, "Repere") in initial["occurrences"]
        }
        assert len(original_reopened) == len(initial["occurrences"])
        for key, occurrence in original_reopened.items():
            expected = initial["occurrences"][key]
            coordinates = occurrence.transform2.asArray()
            assert max(abs(a - b) for a, b in zip(coordinates, expected[1])) < 1e-6, key
            parts = native(occurrence)
            assert len(parts) == len(expected[2]), key
            for after, before in zip(parts, expected[2]):
                assert after[:2] == before[:2] and abs(after[2] - before[2]) < 0.001, key
                assert all(abs(a - b) < .0001 for ap, bp in zip(after[3], before[3])
                           for a, b in zip(ap, bp)), key
        assert sorted((j.name, j.jointMotion.jointType) for j in rroot.asBuiltJoints) == initial["joints"]
        assert sorted(link.name for link in rroot.motionLinks) == initial["liens"]
        reopened_adds = {get_attr(o.component, "Repere") for o in rroot.allOccurrences}
        assert set(bodies).issubset(reopened_adds)

        snapshot(app.activeViewport, None, (-410, -570, 360), (45, 0, 60), (0, 0, 1), 520)
        report.update({"source_sha256": SHA_SOURCE, "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                       "occurrences_origine": len(source.occ), "liaisons_origine": len(initial["joints"]),
                       "liens_de_mouvement_origine": len(initial["liens"]), "reimportation_verifiee": True,
                       "pieces_imprimables": stl_native})
        (work / "validation_fusion.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        doc.close(False)
        reopened.activate()
        status.unlink()
        (work / "validation_provisoire.json").unlink(missing_ok=True)
    except Exception:
        import traceback
        status.write_text(traceback.format_exc(), encoding="utf-8")
        if doc and doc.isValid:
            doc.close(False)
