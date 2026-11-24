from campagne_fusion import *

PITCH_REMOVED = {
    "Moteur_J1": ("06_Garde_J1", "Coque_Socle", "J1_Pignon"),
    "Moteur_J2": ("Coque_Epaule", "Garde_J2", "J2_Pignon"),
    "Moteur_J3": ("Coque_Bras", "Garde_J3", "J3_Pignon", "Embout_Coude"),
    "Moteur_J7": ("Coque_Avant", "Capot_Cassette", "Capot_Paume", "J7_Palonnier", "J7_Support"),
    "Moteur_J2R": ("Coque_Socle", "Tambour_J2R", "Support_J2R"),
    "Moteur_J3R": ("Coque_Socle", "Tambour_J3R", "Support_J3R"),
}
FLEX = ("Gaine", "Tendon", "Brin", "Fil_", "Faisceau", "Alimentation", "Enroulement", "Traction")


def move(manager, body, direction, travel):
    moved = manager.copy(body)
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(*(d * travel / 10 for d in direction))
    if not manager.transform(moved, transform):
        raise RuntimeError("Translation temporaire refusée.")
    return moved


def overlap(manager, a, b, bounds_a, bounds_b):
    la, ha = bounds_a
    lb, hb = bounds_b
    if any(min(ha[i], hb[i]) - max(la[i], lb[i]) <= 1e-5 for i in range(3)):
        return 0.0
    target = manager.copy(a)
    status = manager.booleanOperation(target, b, fusion.BooleanTypes.IntersectionBooleanType)
    if status and target.isSolid:
        return target.volume * 1000
    if target.isValid and target.faces.count == 0:
        return 0.0
    # Un test booléen indéterminé reste distinct d’une voie dégagée.
    return None if not status else 0.0


def paths(assembly, selected=None):
    manager = fusion.TemporaryBRepManager.get()
    model = [(k, manager.copy(b), bb(b)) for k, bodies in assembly.body.items() if not k.startswith(FLEX) for b in bodies]
    for k, b, box in model:
        if any(abs(x - y) > .05 for u, v in zip(bb(b), box) for x, y in zip(u, v)):
            raise RuntimeError(f"Le noyau a copié {k} hors repère d’assemblage.")
    available = {
        **PITCH_REMOVED,
        **{f"Moteur_F{code}": ("Coque_Avant", "Capot_Cassette", "Embout_Coude",
                              "Capot_Paume", f"Bobine_{code}", f"Palonnier_F{code}") for code in "PIMAU"},
        "09_Cassette_SG90": ("Coque_Avant", "Capot_Cassette", "Embout_Coude", "Capot_Paume"),
    }
    if selected is not None:
        available = selected
    for key, removed in available.items():
        if key not in assembly.occ:
            continue
        if key == "09_Cassette_SG90":
            moving_keys = {key, *(k for k, parent in assembly.parents.items() if parent == key and not k.startswith(FLEX))}
            # Les bobines solidaires des axes moteur suivent aussi le sous-ensemble.
            moving_keys |= {k for k, parent in assembly.parents.items() if parent in moving_keys and not k.startswith(FLEX)}
        else:
            moving_keys = {key}
        motions = [(k, b) for k, b, _ in model if k in moving_keys]
        fixed = [(k, b, box) for k, b, box in model if k not in moving_keys and k not in removed]
        directions = []
        for axis in range(3):
            for sign in (-1, 1):
                direction = [0, 0, 0]
                direction[axis] = sign
                failure = None
                unknown = 0
                for travel in (1, 3, 6, 12, 22, 38, 62):
                    for mk, part in motions:
                        moved = move(manager, part, direction, travel)
                        box = bb(moved)
                        for fk, fb, fixed_box in fixed:
                            volume = overlap(manager, moved, fb, box, fixed_box)
                            if volume is None:
                                unknown += 1
                            elif volume > 0.03:
                                failure = [travel, mk, fk, round(volume, 6)]
                                break
                        if failure:
                            break
                    if failure:
                        break
                directions.append({"dir": direction, "first_overlap": failure, "indeterminate": unknown})
        yield {"moving": key, "moving_keys": sorted(moving_keys),
               "removed": [k for k in removed if k in assembly.occ],
               "listed_not_found": [k for k in removed if k not in assembly.occ], "directions": directions}


def pinch_grid(assembly):
    values = (0, 23, 46, 69, 83, 92)
    rows = []
    for p in values:
        for i in values:
            q = {"Servo_P": p, "Servo_I": i}
            actual = assembly.position(q)
            if any(abs(actual[k]-v) > .02 for k,v in q.items()):
                rows.append({"p": p, "i": i, "refused": True})
                continue
            distances = {}
            for a, b in (("P3","I3"), ("P2","I3"), ("P3","I2")):
                record = assembly.app.measureManager.measureMinimumDistance(assembly.body[a][0], assembly.body[b][0])
                distances[a + "/" + b] = [round(record.value * 10, 6), xyz(record.positionOne), xyz(record.positionTwo)]
            rows.append({"p": p, "i": i, "distances": distances})
    return rows


def run(_context):
    assembly = Assembly()
    folder = OUTPUT / "preuves"
    try:
        assembly.position({})
        grasp = pinch_grid(assembly)
        (folder / "pince_grille_fusion.json").write_text(json.dumps(grasp, indent=2), encoding="utf-8")
        assembly.position({})
        access = list(paths(assembly))
        (folder / "couloirs_montage_fusion.json").write_text(json.dumps(access, ensure_ascii=False, indent=2), encoding="utf-8")
    finally:
        assembly.position({})
    print(json.dumps({"grasp": len(grasp), "grasp_min": min((r["distances"]["P3/I3"][0],r["p"],r["i"]) for r in grasp if "distances" in r),
        "test_access": [[r["moving"], [d["dir"] for d in r["directions"] if not d["first_overlap"] and not d["indeterminate"]],
                         r["listed_not_found"]] for r in access]}, ensure_ascii=False))
