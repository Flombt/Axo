"""Exploiter les mesures Fusion sans ouverture ni modification des modèles."""
from collections import Counter, defaultdict
import csv
import gzip
import json
from pathlib import Path
import math
import sys

try:
    import numpy as np
except ModuleNotFoundError:
    sys.path.insert(0, str(Path.home() / "AppData/Local/Temp/aura-audit-deps"))
    import numpy as np

ROOT = Path.cwd()
OUT = ROOT / "docs/diagnostic/latest/preuves"
G = 9.80665
VARIABLE = ("Gaine", "Tendon", "Brin", "Fil_", "Faisceau", "Alimentation", "Enroulement", "Traction")
PORTS = {"J2R_1": (23.1, -12.10, 4.83), "J2R_2": (23.1, -16.51, 4.83),
         "J3R_1": (23.1, 6.43, 4.83), "J3R_2": (23.1, 10.86, 4.83)}
PITCH = ("J1", "J2", "J2R", "J3", "J3R", "J7")
ACCEL = {"J1": 50, "J2": 35, "J2R": 35, "J3": 50, "J3R": 50, "J7": 50}
TO_REWORK = {
    "01_Platine": "Revoir le volume de service pour le faisceau et les deux motorisations de roulis.",
    "05_Tourelle": "Reprendre les quatre traversées excentrées et le passage électrique.",
    "Coque_Socle": "Plusieurs recouvrements CAO avec les enveloppes des gaines.",
    "Coque_Bras": "Recouvre les enveloppes des deux gaines J3R.",
    "Capot_Cassette": "Recouvre le faisceau de cassette dans la pose neutre.",
    "09_Cassette_SG90": "Reprendre la sortie du faisceau et contrôler les accès aux palonniers.",
    "J2_Chape_Tangage": "Revoir l’interface de passage des gaines et la retenue à la coupure.",
    "J3_Chape_Tangage": "Revoir l’interface de passage des gaines et la retenue à la coupure.",
    "07_Bras": "Revoir le passage des deux gaines J3R et les attaches de son capot.",
    "08_Avant_bras": "Gaines et cassette occupent des volumes communs sur certaines poses.",
}


def matrix(value):
    transform = np.array(value).reshape(4, 4).copy()
    transform[:3, 3] *= 10
    return transform


def point(transform, xyz):
    return transform[:3, :3] @ xyz + transform[:3, 3]


def ancestors(parts, key):
    while key is not None:
        yield key
        key = parts[key]["parent"]


def weight(key, part, fill):
    volume = part["volume_mm3"]
    if part["print_ref"]:
        return 0.00127 * fill * volume
    if key in ("Moteur_J2", "Moteur_J3"):
        return 55.0
    if key in ("Moteur_J2R", "Moteur_J3R"):
        return 13.4
    if key.startswith("Moteur_"):
        return 9.0
    if key.startswith("R608_"):
        return 12.0
    if "Pico" in part["name"]:
        return 3.5
    if key.startswith("Gaine"):
        # Enveloppe extérieure Ø4 modélisée pleine, évidement du tube Ø2.
        return 0.00215 * .75 * volume
    if key.startswith(VARIABLE):
        return 0.00135 * volume
    if "Palonnier" in key or "palonnier fourni" in part["name"].lower():
        return 0.0013 * volume
    return 0.00785 * volume


def pose_mechanics(parts, joints, pose, fill, load_g, deck_rect, bolt_rect):
    keys = list(parts)
    masses = np.array([weight(k, parts[k], fill) for k in keys]) / 1000
    neutral = {k: matrix(row["transform"]) for k, row in parts.items()}
    current = {k: matrix(m) for k, m in pose["transforms"].items()}
    rel = {k: current[k] @ np.linalg.inv(neutral[k]) for k in keys}
    com = np.array([point(rel[k], parts[k]["com_mm"]) for k in keys]) / 1000
    tip_box = np.array(parts["M3"]["local_bounds_mm"][0])
    tip_local = tip_box.mean(axis=0)
    tip_local[0] = tip_box[1, 0]
    load = point(current["M3"], tip_local) / 1000
    centre = ((masses[:, None] * com).sum(axis=0) + load_g / 1000 * load) / (masses.sum() + load_g / 1000)
    req = {}
    for k in PITCH:
        joint = joints[k]
        child, parent = joint["child"], joint["parent"]
        axis = rel[parent][:3, :3] @ np.array(joint["axis"])
        axis /= np.linalg.norm(axis)
        origin = point(rel[parent], joint["pivot_mm"]) / 1000
        mask = np.array([child in ancestors(parts, name) for name in keys])
        arms = np.vstack([com[mask] - origin, load - origin])
        chosen = np.r_[masses[mask], load_g / 1000]
        lever = np.dot(np.cross(arms, (0, 0, -1)), axis)
        gravity = abs(float(chosen @ lever) * G)
        radius2 = np.sum(arms * arms, axis=1) - np.square(arms @ axis)
        inertia = float(chosen @ radius2)
        req[k] = {"gravity_nm": gravity,
                  "point_mass_inertia_kg_m2": inertia,
                  "accel_nm": inertia * math.radians(ACCEL[k])}
    x, y = centre[:2] * 1000

    def margin(rect):
        return min(x - rect[0], rect[1] - x, y - rect[2], rect[3] - y)

    return {"centre_mm": (centre * 1000).tolist(), "mass_g": float(masses.sum() * 1000 + load_g),
            "reach_m": float(np.linalg.norm(load[:2])), "above_deck_free_margin_mm": margin(deck_rect),
            "anchor_projection_margin_mm": margin(bolt_rect),
            "free_restoring_moment_nm": float((masses.sum() + load_g / 1000) * G * margin(deck_rect) / 1000),
            "axis": req}


def classify(parts, poses):
    home = poses[0].get("intersections_over_0_03_mm3", [])
    baseline = {tuple(sorted(hit[:2])) for hit in home}
    pairs = {}
    counts = Counter()
    for pose in poses:
        entries = pose.get("intersections_over_0_03_mm3")
        if entries is None:
            continue
        this_pose = defaultdict(list)
        for a, b, v in entries:
            this_pose[tuple(sorted((a, b)))].append(v)
        for key, volumes in this_pose.items():
            flex = any(k.startswith(VARIABLE) for k in key)
            label = "enveloppe souple" if flex else "solides rigides"
            aggregate = pairs.setdefault(key, {"parts": list(key), "class": label, "present_neutral": key in baseline,
                                              "pose_count": 0, "peak_sum_mm3": 0, "peak_lump_mm3": 0,
                                              "strongest_pose": None})
            aggregate["pose_count"] += 1
            aggregate["peak_lump_mm3"] = max(aggregate["peak_lump_mm3"], max(volumes))
            if sum(volumes) > aggregate["peak_sum_mm3"]:
                aggregate["peak_sum_mm3"] = round(sum(volumes), 5)
                aggregate["strongest_pose"] = pose["index"]
            counts[label] += len(volumes)
    return {"pose_count": sum("intersections_over_0_03_mm3" in p for p in poses),
            "neutral_records": len(home), "lump_count": dict(counts),
            "pairs": sorted(pairs.values(), key=lambda row: -row["peak_sum_mm3"])}


def export_parts(parts):
    counts = Counter(p["print_ref"] for p in parts.values() if p["print_ref"])
    with (OUT / "pieces_v5_roulis.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        fields = ("repere", "designation", "parent", "reference_impression", "quantite_reference", "encombrement_local_mm",
                  "volume_mm3", "diametres_CA0_mm", "statut", "preuve_ou_action")
        writer = csv.DictWriter(stream, fields, delimiter=";")
        writer.writeheader()
        for k, p in parts.items():
            box = np.array(p["local_bounds_mm"])
            size = box[:, 1, :].max(axis=0) - box[:, 0, :].min(axis=0) if len(box) else [0, 0, 0]
            reference = p["print_ref"]
            if reference and k in TO_REWORK:
                status, note = "Modification nécessaire", TO_REWORK[k] + " Export V5 absent."
            elif reference:
                status, note = "Impression bloquée", "Géométrie native mesurée. STL/3MF et tranchage de cette révision absents."
            elif k.startswith(VARIABLE):
                status, note = "Achetable à spécifier", "Représentation souple au neutre. Reprendre longueur, rayon, sorties et références."
            else:
                status, note = "Montage à blanc requis", "Gabarit CAO ou métal. Vérifier référence, appuis, visserie et accès avec le lot."
            writer.writerow(dict(zip(fields, (k, p["name"], p["parent"], reference, counts[reference],
                                              " × ".join(f"{v:.3f}" for v in size), p["volume_mm3"],
                                              ", ".join(str(x) for x in sorted({x[0] for x in p["cylinders"]})),
                                              status, note))))


def pose_routing(parts, poses):
    rest = matrix(parts["05_Tourelle"]["transform"])
    report = []
    for pose in poses:
        if "transforms" not in pose:
            continue
        mt = matrix(pose["transforms"]["05_Tourelle"])
        separation = {k: float(np.linalg.norm(point(mt, xyz) - point(rest, xyz))) for k, xyz in PORTS.items()}
        report.append({"index": pose["index"], "yaw": pose["target"]["J1"], "end_mismatch_mm": separation})
    return report


def main():
    geometry = json.loads((OUT / "fusion_geometrie_neutre.json").read_text(encoding="utf-8"))
    parts, joints = geometry["parts"], geometry["joints"]
    poses = sorted([r for path in OUT.glob("fusion_poses_*.json.gz") for r in
                    json.load(gzip.open(path, "rt", encoding="utf-8"))], key=lambda r: r["index"])
    if len({p["index"] for p in poses}) != len(poses):
        raise ValueError("Une pose a été enregistrée deux fois.")
    attempted = {p["index"]: p for p in poses}
    for path in OUT.glob("fusion_reprises_*.json.gz"):
        for retry in json.load(gzip.open(path, "rt", encoding="utf-8")):
            if "transforms" in retry and "transforms" not in attempted[retry["index"]]:
                attempted[retry["index"]] = retry
    poses = sorted(attempted.values(), key=lambda r: r["index"])
    export_parts(parts)
    deck = parts["01_Platine"]
    low, high = deck["world_bounds_mm"][0]
    deck_rect = [low[0], high[0], low[1], high[1]]
    anchors = sorted({(round(c[1][0], 3), round(c[1][1], 3)) for c in deck["cylinders"]
                     if 4.95 <= c[0] <= 6.25 and abs(c[2][2]) > .99
                     and abs(c[1][0]) >= 48 and abs(c[1][1]) >= 36})
    if len(anchors) != 4:
        raise ValueError(f"Quatre perçages d’ancrage attendus, obtenus {anchors}")
    xs, ys = zip(*anchors)
    bolt_rect = [min(xs), max(xs), min(ys), max(ys)]
    valid = [p for p in poses if "transforms" in p]
    scenarios = {}
    for fill, load_g in [(1.0, 0), (1.0, 10), (1.0, 20), (.6, 0), (.6, 20)]:
        rows = [(p["index"], pose_mechanics(parts, joints, p, fill, load_g, deck_rect, bolt_rect)) for p in valid]
        scores = {k: {metric: max((r["axis"][k][metric], i) for i, r in rows)
                      for metric in next(iter(rows))[1]["axis"][k]} for k in PITCH}
        scenarios[f"petg_{fill:g}_charge_{load_g}g"] = {
            "home": rows[0][1], "max_axis": scores,
            "min_bolt_margin_mm": min((r["anchor_projection_margin_mm"], i) for i, r in rows),
            "min_free_margin_mm": min((r["above_deck_free_margin_mm"], i) for i, r in rows),
            "min_restoring_nm": min((r["free_restoring_moment_nm"], i) for i, r in rows),
            "max_reach_m": max((r["reach_m"], i) for i, r in rows),
        }
    routing = pose_routing(parts, valid)
    issues = classify(parts, poses)
    results = {"parts": len(parts), "print_parts": sum(bool(p["print_ref"]) for p in parts.values()),
               "print_references": len({p["print_ref"] for p in parts.values() if p["print_ref"]}),
               "printed_solid_g": sum(weight(k, p, 1) for k, p in parts.items() if p["print_ref"]),
               "printed_max_local_mm": max(float((np.array(p["local_bounds_mm"])[0, 1] - np.array(p["local_bounds_mm"])[0, 0]).max())
                                           for p in parts.values() if p["print_ref"]),
               "anchors_xy_mm": anchors, "deck_rect_mm": deck_rect, "bolt_rect_mm": bolt_rect,
               "native_pose_count": len(valid), "refused_indices": [p["index"] for p in poses if "transforms" not in p],
               "worst_table_mm": min((r["min_hand_z_mm"], r["index"]) for r in valid),
               "below_table_indices": [r["index"] for r in valid if r["min_hand_z_mm"] < 0],
               "scenarios": scenarios, "routing": routing, "interference": issues}
    (OUT / "analyse_mecanique.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in results.items() if k not in ("scenarios", "routing", "interference")}, ensure_ascii=False))
    print(json.dumps({s: {"mass_g": r["home"]["mass_g"], "centre_mm": r["home"]["centre_mm"],
                         "stability": [r["min_bolt_margin_mm"], r["min_free_margin_mm"], r["min_restoring_nm"]],
                         "gravity": {k:v["gravity_nm"] for k,v in r["max_axis"].items()},
                         "accel": {k:v["accel_nm"] for k,v in r["max_axis"].items()}} for s,r in scenarios.items()}))
    print(json.dumps({"neutral_records": issues["neutral_records"], "pose_count": issues["pose_count"],
                      "rigid": [r for r in issues["pairs"] if r["class"]=="solides rigides"][:20],
                      "at_88": [r for r in routing if r["index"]==4]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
