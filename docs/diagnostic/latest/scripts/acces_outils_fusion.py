"""Essais ciblés de démontage et d’accès d’outils sur la copie d’audit Fusion."""
import json
from campagne_fusion import Assembly, OUTPUT, bb, core, fusion
from couloirs_et_pince_fusion import overlap, paths

SELECTION = {
    "Moteur_J7": ("Coque_Avant", "Capot_Cassette", "Capot_Paume", "Palonnier_J7", "Support_J7"),
    "Moteur_J1": ("06_Garde_J1", "Coque_Socle", "J1_Pignon", "03_Porte_J1"),
}

def tooling(assembly):
    manager = fusion.TemporaryBRepManager.get()
    fixed = [(k, manager.copy(b), bb(b)) for k,bodies in assembly.body.items() for b in bodies]
    combinations = [
        ("J2 tête M5 + douille", [0, -32.32, 82], [0, -67.32, 82], 6, "Axe_J2", ["Coque_Epaule", "Garde_J2"]),
        ("J2 écrou M5 + douille", [0, 24.82, 82], [0, 59.82, 82], 6, "Ecrou_J2", ["Coque_Epaule", "Garde_J2"]),
        ("J3 tête M5 + douille", [71.903524, -32.32, 117.069692], [71.903524, -67.32, 117.069692], 6,
         "Axe_J3", ["Coque_Bras", "Garde_J3"]),
        ("J3 écrou M5 + douille", [71.903524, 24.82, 117.069692], [71.903524, 59.82, 117.069692], 6,
         "Ecrou_J3", ["Coque_Bras", "Garde_J3"]),
        ("J1 tête M8 depuis le dessous", [0, .0, 0], [0, .0, -40], 10, "Axe_J1", []),
    ]
    rows = []
    for label, start, end, radius, hardware, removed in combinations:
        p, q = [core.Point3D.create(*(x / 10 for x in v)) for v in (start,end)]
        tube = manager.createCylinderOrCone(p, radius / 10, q, radius / 10)
        box = bb(tube)
        collisions, unknown = [], []
        for key, body, bounds in fixed:
            if key in removed or key == hardware:
                continue
            v = overlap(manager, tube, body, box, bounds)
            if v is None:
                unknown.append(key)
            elif v > .03:
                collisions.append([key, round(v,6)])
        rows.append({"test":label,"start_mm":start,"end_mm":end,"radius_mm":radius,"removed":removed,
                     "collisions":collisions,"indeterminate":unknown,
                     "support_plane_conflict":label.startswith("J1")})
    return rows


def run(_context):
    assembly = Assembly()
    assembly.position({})
    result = {"alternate_paths":list(paths(assembly, SELECTION)), "tooling":tooling(assembly)}
    target = OUTPUT / "preuves" / "acces_outils_fusion.json"
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
