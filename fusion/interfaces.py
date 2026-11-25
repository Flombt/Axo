"""Reprise des interfaces natives de la V5 stabilisée."""
import json
import math

import adsk.core as core
import adsk.fusion as fusion

from stabiliser import (ANCHORS, Model, add, boolean, cut, cylinder, get_attr,
                        mm, point, put_attr, scale, sub, unit)


def axial(z0, z1, outer, inner=0):
    body = cylinder((0, 0, z0), (0, 0, z1), outer)
    if inner:
        cut(body, cylinder((0, 0, z0 - .5), (0, 0, z1 + .5), inner))
    return body


def identify(model, key, name, part):
    old = model.occ[key].component
    old.name = name
    old.partNumber = part


def hollow_base(model):
    model.pose({})
    # Deux logements d'appui opposés. Introduction du roulement haut par le dessus.
    housing = model.copy("02_Palier_J1")
    for lo, hi in ((6.03, 15.85), (23.6, 34.35)):
        boolean(housing, axial(lo, hi, 15.7, 11.2))
    cut(housing, axial(5.5, 14.04, 13.12),
        axial(25.65, 41.5, 13.12), axial(10, 32, 7.65))
    model.replace("02_Palier_J1", housing)

    plate = model.copy("01_Platine")
    cut(plate, axial(-1, 7, 10.35))
    model.replace("01_Platine", plate)
    # Recentrer les corps des quatre rehausses sur les perçages natifs.
    for i, (x, _) in enumerate(ANCHORS, 1):
        key = f"Pied_Rehausse_{i}"
        shape = model.copy(key)
        t = core.Matrix3D.create()
        t.translation = core.Vector3D.create(-0.05, 0, 0)
        assert model.tmp.transform(shape, t)
        model.replace(key, shape)

    for key, z0 in (("R608_1", 6.0), ("R608_2", 25.65)):
        model.replace(key, axial(z0, z0 + 8, 13, 5))
        identify(model, key, "Roulement 6000-ZZ · 10 × 26 × 8", "6000-ZZ")
        put_attr(model.occ[key].component, "Repere", key.replace("608", "6000"))
    model.replace("Entretoise_J1", axial(14.02, 25.63, 7.0, 5.12))
    model.replace("Appui_J1", axial(33.66, 34.43, 7.0, 5.08))
    model.replace("Axe_J1", axial(-12, 63, 5, 4))
    identify(model, "Axe_J1", "Tube de précision J1 Ø10/8 × 75 mm", "Tube-10-8-L75")
    model.replace("Nut_J1", axial(52.2, 60.2, 10, 5))
    identify(model, "Nut_J1", "Bague de serrage J1 haute Ø10/20 × 8", "Collier-10-20-8")
    model.place("Collier_J1_Bas", "Bague de serrage J1 basse Ø10/20 × 8",
                "05_Tourelle", axial(-3, 5, 10, 5))
    model.place("Rondelle_Basse_J1", "Rondelle de bague intérieure Ø10/14 × 1",
                "05_Tourelle", axial(5, 6, 7.0, 5.08))

    wheel = model.copy("J1_Roue")
    cut(wheel, axial(-1, 6.2, 5.17))
    model.replace("J1_Roue", wheel)
    turret = model.copy("05_Tourelle")
    cut(turret, axial(-8, 25.2, 5.25), axial(7.7, 18.8, 10.65))
    model.replace("05_Tourelle", turret)

    for i, y in ((1, -28.467188), (2, 28.467188)):
        key = f"Butee_J1_{i}"
        model.replace(key, cylinder((-5.533461, y, 36), (-5.533461, y, 43.5), 1.95))
        identify(model, key, "Vis d’arrêt J1 M4, hauteur de pointe 43,5 mm", "ISO-M4")
    model.refresh()
    put_attr(model.root, "PlanDeTravail", {"plan_table_mm": -72, "ancrage_xy_mm": ANCHORS})
    put_attr(model.root, "AxeCreuxJ1", {"tube":[10,8,75], "roulements":"6000-ZZ",
                                      "faisceau_max_diametre_mm":6.8, "axe_mm":[0,0]})
    print("Axe creux Ø10/8, deux 6000 et quatre rehausses recentrées.")


def bounding(body):
    bounds = body.preciseBoundingBox
    return mm(bounds.minPoint), mm(bounds.maxPoint)


def collision(model, a, b, eps=0.03):
    lo_a, hi_a = bounding(a)
    lo_b, hi_b = bounding(b)
    if any(min(ub, ua) - max(lb, la) <= 1e-5 for la, ua, lb, ub in zip(lo_a, hi_a, lo_b, hi_b)):
        return 0.0
    candidate = model.tmp.copy(a)
    ok = model.tmp.booleanOperation(candidate, b, fusion.BooleanTypes.IntersectionBooleanType)
    if candidate.isSolid and ok:
        return candidate.volume * 1000
    if candidate.isValid and candidate.faces.count == 0:
        return 0.0
    if ok:
        return 0.0
    raise RuntimeError(f"Volume d'interférence indéterminé au-dessus du seuil {eps} mm³")


def to_world(model, body, key):
    candidate = model.tmp.copy(body)
    assert model.tmp.transform(candidate, model.occ[key].transform2)
    return candidate


def thumb_shape(model):
    shape = model.copy("P3")
    actual = model.pose({"Servo_P": 92, "Servo_I": 92})
    if min(actual["Servo_P"], actual["Servo_I"]) < 91.98:
        raise RuntimeError("Pose de construction de la pince non atteinte.")
    body_p, body_i = (model.solids(key)[0] for key in ("P3", "I3"))
    closest = model.app.measureManager.measureMinimumDistance(body_p, body_i)
    p, i = mm(closest.positionOne), mm(closest.positionTwo)
    com = mm(body_p.physicalProperties.centerOfMass)
    aim = unit(sub(i, p))
    root = add(p, scale(4.2, unit(sub(com, p))))
    tip = add(p, scale(closest.value * 10 - 6.8, aim))
    pad = cylinder(root, tip, 3.8, 3.1)
    head = model.tmp.createSphere(point(tip), .31)
    boolean(pad, head)
    transform = model.occ["P3"].transform2.copy()
    assert transform.invert() and model.tmp.transform(pad, transform)
    boolean(shape, pad)
    if shape.lumps.count != 1:
        raise RuntimeError("Sabot dissocié de la phalange.")
    return shape


def thumb(model):
    shape = thumb_shape(model)
    distances = []
    for p in (0, 23, 46, 69, 83, 92):
        for i in (0, 23, 46, 69, 83, 92):
            target = {"Servo_P": p, "Servo_I": i, "Servo_M": i, "Servo_A": i, "Servo_U": i}
            actual = model.pose(target)
            if any(abs(target[k] - actual[k]) > .02 for k in target):
                raise RuntimeError(f"Pince, position non atteinte à {p}/{i}.")
            test = to_world(model, shape, "P3")
            for key in ("P1","11_Paume","12_Chape_Pouce","I1","I2","I3","M1","M2","M3","A1","A2","A3","U1","U2","U3"):
                for other in model.solids(key):
                    volume = collision(model, test, other)
                    if volume > .03:
                        raise RuntimeError(f"Pince {p}/{i}, interférence P3/{key}: {volume:.3f} mm³")
            d = model.app.measureManager.measureMinimumDistance(test, model.solids("I3")[0])
            distances.append([p, i, round(d.value * 10, 5)])
    model.pose({})
    model.replace("P3", shape)
    print(json.dumps({"pince_avant_mm":17.680769,"pince_min_mm":min(d[2] for d in distances),
                      "pince":distances,"sabot_volume_mm3": round(shape.volume*1000, 4)}))


def move(model, body, direction, travel):
    transformed = model.tmp.copy(body)
    t = core.Matrix3D.create()
    t.translation = core.Vector3D.create(*(x * travel / 10 for x in direction))
    assert model.tmp.transform(transformed, t)
    return transformed


ACCESS = {
    "Moteur_J2": ("05_Tourelle", (0, 1, 0), {"Coque_Epaule","Garde_J2","J2_Pignon"}),
    "Moteur_J3": ("J2_Chape_Tangage", (0, 1, 0), {"Coque_Bras","Garde_J3","J3_Pignon","Embout_Coude"}),
    "Moteur_J7": ("J3_Chape_Tangage", (0, 0, -1), {"Coque_Avant","Capot_Cassette","Capot_Paume","Palonnier_J7","Support_J7"}),
}
FLEX = ("Tendon_", "Traction_", "Faisceau_")


def motor_access(model, key):
    support, direction, removed = ACCESS[key]
    source = model.tmp.copy(model.solids(key)[0])
    blocks = [(k, model.tmp.copy(b)) for k in model.occ if k not in {key, *removed}
              and not k.startswith(FLEX) for b in model.solids(k)]
    bad = {}
    for distance in range(0, 61):
        motor = move(model, source, direction, distance)
        for k, b in blocks:
            volume = collision(model, motor, b)
            if volume > .03:
                bad.setdefault(k, []).append([distance, round(volume, 4)])
    return {"motor":key, "support":support, "direction":direction, "removed":sorted(removed), "blocks":bad}


def access_report(model):
    model.pose({})
    results = [motor_access(model, key) for key in ACCESS]
    print(json.dumps(results))


def run(_context):
    model = Model()
    model.require_copy()
    if not get_attr(model.root, "Revision"):
        raise RuntimeError("Appliquer le noyau de stabilisation avant les interfaces.")
    hollow_base(model)
    thumb(model)
    access_report(model)
