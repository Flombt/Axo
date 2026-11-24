from campagne_fusion import *

def write_geometry(assembly):
    records = []
    for info, occ in assembly.occ.items():
        for body in occ.component.bRepBodies:
            if not body.isSolid or body.name == "Repère de liaison":
                continue
            calculator = body.meshManager.createMeshCalculator()
            calculator.surfaceTolerance = .016
            mesh = calculator.calculate()
            nodes = [xyz(p) for p in mesh.nodeCoordinates]
            records.append({"part": info, "vertices_local_mm": nodes, "triangles": list(mesh.nodeIndices)})
    with gzip.open(OUTPUT / "preuves" / "maillages_visuels_fusion.json.gz", "wt", encoding="utf-8") as stream:
        json.dump(records, stream, separators=(",", ":"))
    return len(records)


def measure(assembly):
    jobs = [
        ("doigts ouverts", {}, [("P3", "I3"), ("I3", "M3"), ("M3", "A3"), ("A3", "U3")]),
        ("pince 46", {"Servo_P": 46, "Servo_I": 46}, [("P3", "I3"), ("P2", "I3")]),
        ("pince 75", {"Servo_P": 75, "Servo_I": 75}, [("P3", "I3"), ("P2", "I3")]),
        ("pince 92", {"Servo_P": 92, "Servo_I": 92}, [("P3", "I3"), ("P2", "I3")]),
        ("poing 92", dict.fromkeys(FINGERS, 92), [("P3", "I3"), ("I3", "M3"), ("M3", "A3"), ("A3", "U3"),
                                                  ("P3", "11_Paume"), ("I3", "11_Paume")]),
        ("J1 -88", {"J1": -88}, [("Butee_J1_1", "05_Tourelle"), ("Butee_J1_2", "05_Tourelle")]),
        ("J1 88", {"J1": 88}, [("Butee_J1_1", "05_Tourelle"), ("Butee_J1_2", "05_Tourelle")]),
        ("J2R -20", {"J2R": -20}, [("But_J2R", "07_Bras")]),
        ("J2R +20", {"J2R": 20}, [("But_J2R", "07_Bras")]),
        ("J3R -24", {"J3R": -24}, [("But_J3R", "08_Avant_bras")]),
        ("J3R +24", {"J3R": 24}, [("But_J3R", "08_Avant_bras")]),
    ]
    rows = []
    for label, target, pairs in jobs:
        actual = assembly.position(target)
        for a, b in pairs:
            try:
                measure_result = assembly.app.measureManager.measureMinimumDistance(assembly.body[a][0], assembly.body[b][0])
                rows.append({"pose": label, "pair": [a, b], "distance_mm": round(measure_result.value * 10, 6),
                             "points_mm": [xyz(measure_result.positionOne), xyz(measure_result.positionTwo)]})
            except (AttributeError, RuntimeError, KeyError, IndexError) as exc:
                rows.append({"pose": label, "pair": [a,b], "error": str(exc)})
    return rows


def snapshot(assembly, file, pose, selection, view, wire=False):
    assembly.position(pose)
    for key, occurrence in assembly.occ.items():
        occurrence.isLightBulbOn = key in selection
    viewport = assembly.app.activeViewport
    camera = viewport.camera
    camera.isSmoothTransition = False
    camera.viewOrientation = view
    camera.isFitView = True
    viewport.camera = camera
    if wire:
        style = next((getattr(core.VisualStyles, name) for name in
                      ("WireframeVisibleEdgesOnlyVisualStyle", "WireframeVisualStyle") if hasattr(core.VisualStyles, name)), None)
        if style is not None:
            viewport.visualStyle = style
    elif hasattr(core.VisualStyles, "ShadedWithVisibleEdgesVisualStyle"):
        viewport.visualStyle = core.VisualStyles.ShadedWithVisibleEdgesVisualStyle
    viewport.refresh()
    return viewport.saveAsImageFile(str(OUTPUT / "wireframes" / file), 1500, 900)


def run(_context):
    assembly = Assembly()
    old = {k: o.isLightBulbOn for k, o in assembly.occ.items()}
    home = {k for k, v in old.items() if v}
    try:
        assembly.position({})
        meshes = write_geometry(assembly)
        distances = measure(assembly)
        (OUTPUT / "preuves" / "distances_fusion.json").write_text(
            json.dumps(distances, ensure_ascii=False, indent=2), encoding="utf-8")
        o = core.ViewOrientations
        shots = {}
        for file, pose, keep, view, wire in [
            ("02_fusion_butees_basses.png", {"J2": -21, "J3": -32}, home, o.FrontViewOrientation, True),
            ("03_fusion_socle_j1.png", {"J1": 88}, {k for k in assembly.occ if k.startswith(("01_", "02_", "03_", "R608", "Gaine_Socle", "Gaine_Colonne", "J1", "Pied_But", "Butee_J1", "Moteur_J", "Tambour_J", "Support_J", "Pico", "Faisceau_Colonne"))}, o.TopViewOrientation, True),
            ("04_fusion_paliers_j2r_j3r.png", {"J2R": 20, "J3R": 24}, {k for k in assembly.occ if k.startswith(("J2_Chape", "J3_Chape", "07_Bras", "08_Avant", "Palier_J2R", "Palier_J3R", "But_J2R", "But_J3R", "Raccord", "Gaine_Bras"))}, o.IsoTopRightViewOrientation, False),
            ("05_fusion_flexion_independante.png", {"Servo_P": 75, "Servo_I": 75}, {k for k in assembly.occ if k.startswith(("09_", "11_", "12_", "13_", "Bob", "Moteur_F", "Palonnier_F", "Tendon", "Traction", "Moteur_J7")) or k in DRIVEN}, o.IsoTopRightViewOrientation, False),
        ]:
            shots[file] = snapshot(assembly, file, pose, keep, view, wire)
        print(json.dumps({"mesh_bodies": meshes, "distances": distances, "shots": shots}, ensure_ascii=False))
    finally:
        assembly.position({})
        for k, occurrence in assembly.occ.items():
            occurrence.isLightBulbOn = old[k]
