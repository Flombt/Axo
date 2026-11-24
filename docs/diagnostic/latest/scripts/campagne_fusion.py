START = 0
STOP = 20
INTERFERENCE = True

"""Campagne Fusion sur une réimportation F3D temporaire de la V5 roulis."""
import gzip
import json
import math
import os
from itertools import product
from pathlib import Path

import adsk.core as core
import adsk.fusion as fusion

PROJECT_ROOT = (Path(os.environ["AURA_PROJECT_ROOT"]) if "AURA_PROJECT_ROOT" in os.environ
                else Path(__file__).resolve().parents[4])
OUTPUT = PROJECT_ROOT / "docs/diagnostic/latest"
AXES = {"J1": 88, "J2": 21, "J2R": 20, "J3": 32, "J3R": 24, "J7": 32}
FINGERS = ["Servo_" + code for code in "PIMAU"]
COMMANDS = [*AXES, *FINGERS]
DRIVEN = ["P1M", "P2M", "P2RM", "P3M", "P3RM"] + [f"{code}{i}" for code in "PIMAU" for i in (1, 2, 3)]


def attr(entity, name):
    value = entity.attributes.itemByName("AURA-01", name)
    return value.value if value else None


def xyz(p, scale=10):
    return [round(x * scale, 6) for x in p.asArray()]


def bb(body):
    box = getattr(body, "preciseBoundingBox", None) or body.boundingBox
    return [xyz(box.minPoint), xyz(box.maxPoint)]


def samples():
    yield "neutre", {}
    yield "butées basses", {"J2": -21, "J3": -32}
    yield "poing", dict.fromkeys(FINGERS, 92)
    yield "pince 75", {"Servo_P": 75, "Servo_I": 75}
    yield "lacets positifs", {"J1": 88}
    for axis, peak in AXES.items():
        for value in (-peak, -peak / 2, peak / 2, peak):
            yield f"{axis} {value:g}", {axis: value}
    for axis in FINGERS:
        for value in (25, 75, 92):
            yield f"{axis} {value}", {axis: value}
    for j2, j3 in product((-21, -14, -7, 0, 7, 14, 21), (-32, -24, -16, -8, 0, 8, 16, 24, 32)):
        yield f"grille {j2}/{j3}", {"J2": j2, "J3": j3}
    for j2, j3, j2r, j3r, j7 in product((-21, 12), (1, -18), (-20, 20), (-24, 24), (-32, 32)):
        yield "roulis et tangages", {"J2": j2, "J3": j3, "J2R": j2r, "J3R": j3r, "J7": j7}
    for j1, j2r, j3r, j7 in product((-88, 88), (-20, 20), (-24, 24), (-32, 32)):
        yield "lacet, roulis et prise", {"J1": j1, "J2R": j2r, "J3R": j3r, "J7": j7,
                                        "J2": -7, "J3": -7, "Servo_P": 92, "Servo_I": 92, "Servo_M": 65}
    for f in (25, 46, 75, 92):
        yield f"pince {f}", {"Servo_P": f, "Servo_I": f}
        yield f"poing {f}", dict.fromkeys(FINGERS, f)
    yield "prise dépareillée", dict(zip(FINGERS, (12, 92, 56, 0, 71)))


def unique_samples():
    seen = set()
    for label, target in samples():
        vector = tuple(target.get(axis, 0) for axis in COMMANDS)
        if vector not in seen:
            seen.add(vector)
            yield label, dict(zip(COMMANDS, vector))


class Assembly:
    def __init__(self):
        self.app = core.Application.get()
        self.doc = self.app.activeDocument
        self.design = fusion.Design.cast(self.app.activeProduct)
        self.root = self.design.rootComponent
        if self.doc.isSaved or self.root.allOccurrences.count != 154 or not attr(self.root, "Source"):
            raise RuntimeError("Sélectionner l’archive V5 roulis importée dans un document sans enregistrement.")
        self.occ = {attr(o.component, "Repere"): o for o in self.root.occurrences}
        self.by_name = {o.name: k for k, o in self.occ.items()}
        self.joints = {j.name.split(" · ")[0]: j for j in self.root.asBuiltJoints
                       if fusion.RevoluteJointMotion.cast(j.jointMotion)}
        self.cal = json.loads(attr(self.root, "Calibration"))
        self.groups = {k: attr(o.component, "Impression") for k, o in self.occ.items()}
        self.parents = {k: attr(o.component, "Parent") for k, o in self.occ.items()}
        self.body = {k: [b for b in o.bRepBodies if b.isSolid and b.name != "Repère de liaison"]
                     for k, o in self.occ.items()}
        if len(self.occ) != 154 or any(not k for k in self.occ):
            raise RuntimeError("Repères manquants ou en double.")

    def angle(self, key):
        zero, sign, _ = self.cal[key]
        return math.degrees(math.remainder(self.joints[key].jointMotion.rotationValue - zero, math.tau)) * sign

    def position(self, target):
        for key in COMMANDS:
            value = target.get(key, 0)
            zero, sign, _ = self.cal[key]
            motion = self.joints[key].jointMotion
            angle = zero + sign * math.radians(value)
            if abs(motion.rotationValue - angle) > 1e-8:
                motion.rotationValue = angle
        return {key: round(self.angle(key), 5) for key in [*COMMANDS, *DRIVEN]}

    def inventory(self):
        records = {}
        for key, occurrence in self.occ.items():
            bodies = self.body[key]
            native = [b for b in occurrence.component.bRepBodies if b.isSolid and b.name != "Repère de liaison"]
            cylinders = []
            for b in bodies:
                for face in b.faces:
                    cyl = core.Cylinder.cast(face.geometry)
                    if cyl:
                        cylinders.append([round(cyl.radius * 20, 5), xyz(cyl.origin),
                                          xyz(cyl.axis, 1), bb(face)])
            weighted = [(b.volume, b.physicalProperties.centerOfMass) for b in bodies]
            volume = sum(v for v, _ in weighted)
            com = [round(sum(v * xyz(p)[i] for v, p in weighted) / volume, 6) for i in range(3)] if volume else None
            records[key] = {"name": occurrence.component.name, "parent": self.parents[key],
                            "print_ref": self.groups[key], "volume_mm3": round(volume * 1000, 6),
                            "com_mm": com, "world_bounds_mm": [bb(b) for b in bodies],
                            "local_bounds_mm": [bb(b) for b in native], "cylinders": cylinders,
                            "transform": occurrence.transform2.asArray()}
        joints = {key: {"pivot_mm": xyz(j.geometry.origin),
                        "axis": xyz(j.jointMotion.rotationAxisVector, 1),
                        "child": self.by_name[j.occurrenceOne.name],
                        "parent": self.by_name[j.occurrenceTwo.name]} for key, j in self.joints.items()}
        return {"parts": records, "joints": joints,
                "calibration": self.cal, "attributes": {v.name: v.value for v in self.root.attributes}}

    def interference(self):
        collection = core.ObjectCollection.create()
        for bodies in self.body.values():
            for body in bodies:
                collection.add(body)
        query = self.design.createInterferenceInput(collection)
        query.areCoincidentFacesIncluded = False
        results = self.design.analyzeInterference(query)
        if results is None:
            raise RuntimeError("Analyse d’interférence Fusion sans résultat.")
        hits = []
        for hit in results:
            a, b = hit.entityOne, hit.entityTwo
            part_a, part_b = [self.by_name[b.assemblyContext.name] if b.assemblyContext else
                              attr(b.parentComponent, "Repere") or b.name for b in (a, b)]
            volume = hit.interferenceBody.volume * 1000
            if volume > 0.03 and part_a != part_b:
                hits.append([part_a, part_b, round(volume, 6)])
        return {"bodies": collection.count, "intersections_over_0_03_mm3": hits}

    def pose_results(self, title, target, interference):
        actual = self.position(target)
        error = max(abs(actual[key] - value) for key, value in target.items())
        result = {"label": title, "target": target, "actual": actual, "max_error_deg": error}
        if error > 0.02:
            return result
        hand_keys = [self.joints["J7"].occurrenceOne.name]
        hand_keys += [j.occurrenceOne.name for k, j in self.joints.items() if len(k) == 2 and k[0] in "PIMAU" and k[1].isdigit()]
        result["min_hand_z_mm"] = min(bb(b)[0][2] for o in hand_keys for b in self.body[self.by_name[o]])
        result["transforms"] = {k: o.transform2.asArray() for k, o in self.occ.items()}
        if interference:
            result.update(self.interference())
        return result


def run(_context):
    assembly = Assembly()
    assembly.position({})
    directory = OUTPUT / "preuves"
    directory.mkdir(parents=True, exist_ok=True)
    if START == 0:
        (directory / "fusion_geometrie_neutre.json").write_text(
            json.dumps(assembly.inventory(), ensure_ascii=False, indent=2), encoding="utf-8")
    cases = list(unique_samples())
    results = []
    try:
        for index in range(START, min(STOP, len(cases))):
            title, target = cases[index]
            result = assembly.pose_results(title, target, INTERFERENCE is True or index in INTERFERENCE)
            results.append(dict(index=index, **result))
    finally:
        with gzip.open(directory / f"fusion_poses_{START:03d}.json.gz", "wt", encoding="utf-8") as fp:
            json.dump(results, fp, ensure_ascii=False, separators=(",", ":"))
        assembly.position({})
    print(json.dumps({"planned": len(cases), "completed": len(results),
                      "checks": [[r["index"], r["label"], r["max_error_deg"], r.get("min_hand_z_mm"),
                                  len(r.get("intersections_over_0_03_mm3", []))] for r in results]},
                     ensure_ascii=False))
