from campagne_fusion import *

def run(_context):
    assembly = Assembly()
    results = []
    cases = list(unique_samples())
    for i in range(130, 146):
        title, target = cases[i]
        # Le changement de côté sur une butée est rejoué par pas depuis le neutre.
        initial = {k: assembly.angle(k) for k in COMMANDS}
        for f in (0.8, 0.6, 0.4, 0.2, 0):
            assembly.position({k: initial[k] * f for k in COMMANDS})
        for f in (0.12, 0.25, 0.4, 0.55, 0.7, 0.85, 0.94, 0.98, 0.997, 1):
            assembly.position({k: target[k] * f for k in COMMANDS})
        result = assembly.pose_results(title, target, i in (130, 135, 143, 145))
        results.append(dict(index=i, **result))
    assembly.position({})
    with gzip.open(OUTPUT / "preuves" / "fusion_reprises_130_145.json.gz", "wt", encoding="utf-8") as fp:
        json.dump(results, fp, ensure_ascii=False, separators=(",", ":"))
    print(json.dumps([[r["index"],r["max_error_deg"],r.get("min_hand_z_mm"),len(r.get("intersections_over_0_03_mm3",[]))] for r in results]))
