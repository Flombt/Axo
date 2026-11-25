"""Ajuste les couloirs de dépose et vérifie les dégagements BRep."""
import json
from pathlib import Path

from stabiliser import Model, box, cut, get_attr, sub
from interfaces import ACCESS, bounding, collision, motor_access, move
import adsk.fusion as fusion

CASSETTE = {"09_Cassette_SG90", *("Moteur_F" + k for k in "PIMAU"),
            *("Bobine_" + k for k in "PIMAU"), *("Palonnier_F" + k for k in "PIMAU"),
            "Embout_Coude"}


def groups(samples):
    clusters = []
    for step, bounds in samples:
        if not clusters or step - clusters[-1][-1][0] > .5:
            clusters.append([])
        clusters[-1].append((step,bounds))
    return clusters


def fixture_clearance(model, motor):
    support, direction, removed = ACCESS[motor]
    support_world = model.tmp.copy(model.solids(support)[0])
    source = model.tmp.copy(model.solids(motor)[0])
    hits = []
    for index in range(101):
        distance = index * .5
        path = move(model, source, direction, distance)
        if collision(model, support_world, path) <= .002:
            continue
        intersection = model.tmp.copy(path)
        assert model.tmp.booleanOperation(intersection, support_world, fusion.BooleanTypes.IntersectionBooleanType)
        hits.append((distance, bounding(intersection)))
    if not hits:
        return {"motor": motor, "cut_mm3": 0, "boxes_mm": []}
    old_shape = model.copy(support)
    original_volume = old_shape.volume
    t = model.occ[support].transform2.copy()
    assert t.invert()
    evidence = []
    for series in groups(hits):
        # L’enveloppe de chaque zone touchée supprime localement le crochet qui bloque.
        low = [min(b[0][i] for _, b in series)-.40 for i in range(3)]
        high = [max(b[1][i] for _, b in series)+.40 for i in range(3)]
        solid = box([(a+b)/2 for a,b in zip(low,high)], sub(high,low))
        assert model.tmp.transform(solid,t)
        cut(old_shape,solid)
        evidence.append([low, high, series[0][0], series[-1][0]])
    model.replace(support,old_shape)
    return {"motor":motor, "support":support, "cut_mm3":round((original_volume-old_shape.volume)*1000,4),
            "initial_volume_mm3":round(original_volume*1000,4),"boxes_mm":evidence}


def run(_context, output):
    m=Model()
    m.require_copy()
    if not get_attr(m.root, "AxeCreuxJ1"):
        raise RuntimeError("Appliquer les reprises du socle.")
    m.pose({})
    ACCESS["Moteur_J3"][2].add("Friction_J3_2")
    ACCESS["Moteur_J7"][2].update(CASSETTE)
    report = {"reprise":[fixture_clearance(m,k) for k in ACCESS],
              "apres":[motor_access(m,k) for k in ACCESS]}
    Path(output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"retraits":report["reprise"],"blocages":[(q["motor"],q["blocks"]) for q in report["apres"]]}))
