"""Corrections de l'assemblage natif V5 roulis depuis une copie réimportée."""
import json
import math

import adsk.core as core
import adsk.fusion as fusion

ATTR = "AURA-01"
BASELINE_SHA = "55d3f7964cd04625a4f9062db03c406900fc6acf57cedec86a5bfd5b46495361"
REVISION = "V5-stabilisation"
TABLE_Z = -72.0
PRINT_FOOT = "Rehausse_72_M5"
ANCHORS = ((-60.5, -47), (-60.5, 47), (68.5, -47), (68.5, 47))
RETIRED = ("Moteur_J2R", "Moteur_J3R", "Support_J2R", "Support_J3R", "Tambour_J2R",
           "Tambour_J3R", "Palier_J2R", "Palier_J3R", "But_J2R", "But_J3R")
RETIRED_PREFIX = ("Gaine_", "BrinTambour_", "BrinCollier_", "Enroulement_", "Raccord_J")
HISTORICAL_CABLES = ("Alimentation_Fixe", "Faisceau_Colonne", "Faisceau_Bras",
                     "Faisceau_Cassette", "Fil_M1")


def get_attr(entity, key):
    attr = entity.attributes.itemByName(ATTR, key)
    return attr.value if attr else None


def put_attr(entity, key, value):
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    entity.attributes.add(ATTR, key, value)


def point(xyz):
    return core.Point3D.create(*(x / 10 for x in xyz))


def vector(xyz):
    return core.Vector3D.create(*xyz)


def mm(p):
    return tuple(x * 10 for x in p.asArray())


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(s, a):
    return tuple(s * x for x in a)


def unit(a):
    return scale(1 / math.sqrt(sum(x*x for x in a)), a)


def cylinder(a, b, r1, r2=None):
    return fusion.TemporaryBRepManager.get().createCylinderOrCone(
        point(a), r1 / 10, point(b), (r1 if r2 is None else r2) / 10)


def box(center, size, u=(1, 0, 0), v=(0, 1, 0)):
    obb = core.OrientedBoundingBox3D.create(point(center), vector(u), vector(v),
                                         *(x / 10 for x in size))
    return fusion.TemporaryBRepManager.get().createBox(obb)


def boolean(target, tool, op=fusion.BooleanTypes.UnionBooleanType):
    if not fusion.TemporaryBRepManager.get().booleanOperation(target, tool, op):
        raise RuntimeError(f"Booléen Fusion refusé ({op}).")
    return target


def cut(target, *tools):
    for tool in tools:
        boolean(target, tool, fusion.BooleanTypes.DifferenceBooleanType)
    return target


class Model:
    def __init__(self):
        self.app = core.Application.get()
        self.doc = self.app.activeDocument
        self.design = fusion.Design.cast(self.app.activeProduct)
        self.root = self.design.rootComponent
        self.tmp = fusion.TemporaryBRepManager.get()
        if not self.doc.name.startswith("AURA-01 V5") or not get_attr(self.root, "Calibration"):
            raise RuntimeError("Sélectionner la copie AURA-01 V5 attendue.")
        self.refresh()

    def refresh(self):
        self.occ = {get_attr(o.component, "Repere"): o for o in self.root.occurrences}
        self.joints = {j.name.split(" · ")[0]: j for j in self.root.asBuiltJoints}
        self.cal = json.loads(get_attr(self.root, "Calibration"))
        if len(self.occ) != self.root.occurrences.count or None in self.occ:
            raise RuntimeError("Les repères d’assemblage doivent être uniques.")

    def require_copy(self):
        if self.doc.isSaved:
            raise RuntimeError("Appliquer les corrections sur la copie locale importée.")

    def solids(self, key, native=False):
        occurrence = self.occ[key]
        bodies = occurrence.component.bRepBodies if native else occurrence.bRepBodies
        return [b for b in bodies if b.isSolid and b.name != "Repère de liaison"]

    def copy(self, key, dest=None):
        body = self.tmp.copy(self.solids(key, True)[0])
        if dest is not None:
            transform = self.occ[dest].transform2.copy()
            assert transform.invert()
            # transformBy prémultiplie la matrice déjà portée par le corps.
            assert self.tmp.transform(body, self.occ[key].transform2)
            assert self.tmp.transform(body, transform)
        return body

    def replace(self, key, shape):
        if not shape.isSolid or shape.lumps.count != 1:
            raise RuntimeError(f"{key} doit rester un solide monobloc.")
        feature = self.occ[key].component.features.baseFeatures.item(0)
        assert feature.startEdit(), key
        try:
            target = next(b for b in feature.bodies if b.isSolid and b.name != "Repère de liaison")
            assert feature.updateBody(target, shape), key
        finally:
            assert feature.finishEdit(), key
        assert len(self.solids(key, True)) == 1

    def place(self, key, label, parent, shape, ref="", world_origin=(0, 0, 0)):
        transform = core.Matrix3D.create()
        transform.translation = vector(scale(.1, world_origin))
        occurrence = self.root.occurrences.addNewComponent(transform)
        comp = occurrence.component
        comp.name = label
        comp.partNumber = "AURA-V5-" + (ref or key)
        for name, value in (("Repere", key), ("Impression", ref), ("Parent", parent)):
            put_attr(comp, name, value)
        base = comp.features.baseFeatures.add()
        base.name = label
        assert base.startEdit()
        try:
            body = comp.bRepBodies.add(shape, base)
            assert body
            body.name = ("FDM · " if ref else "") + key
        finally:
            assert base.finishEdit()
        joint_input = self.root.asBuiltJoints.createInput(occurrence, self.occ[parent], None)
        assert joint_input.setAsRigidJointMotion()
        joint = self.root.asBuiltJoints.add(joint_input)
        assert joint
        joint.name = key + " · " + label
        self.occ[key] = occurrence
        return occurrence

    def pose(self, target):
        for key in ("J1", "J2", "J3", "J7", *("Servo_" + k for k in "PIMAU")):
            zero, sign, _ = self.cal[key]
            value = zero + sign * math.radians(target.get(key, 0))
            motion = self.joints[key].jointMotion
            if abs(motion.rotationValue - value) > 1e-8:
                motion.rotationValue = value
        return {key: self.angle(key) for key in self.cal}

    def angle(self, key):
        zero, sign, _ = self.cal[key]
        native = self.joints[key].jointMotion.rotationValue - zero
        return math.degrees(math.remainder(native, math.tau)) * sign


def convert_to_rigid(model, axis):
    joint = model.joints[axis]
    assert joint.timelineObject.rollTo(True)
    try:
        assert joint.setAsRigidJointMotion(), axis
    finally:
        assert model.design.timeline.moveToEnd()
    assert fusion.RigidJointMotion.cast(joint.jointMotion), axis


def fuse_shaft(model, pitch, link, station):
    shoulder = model.copy(pitch)
    # La nervure annulaire s’appuie sur le tourillon et la première joue pleine de l’arbre.
    sleeve = cylinder((station - 1.4, 0, 0), (station + 7.0, 0, 0), 11.0)
    cut(sleeve, cylinder((station - 2, 0, 0), (station + 7.5, 0, 0), 4.35))
    boolean(shoulder, sleeve)
    boolean(shoulder, model.copy(link, pitch))
    model.replace(pitch, shoulder)
    comp = model.occ[link].component
    assert comp.features.removeFeatures.add(model.solids(link, True)[0])
    put_attr(comp, "Impression", "")
    comp.name = "Repère cinématique · " + link
    model.occ[pitch].component.name += " et longeron d’une pièce"
    print(pitch, "volume fusionné mm³", round(shoulder.volume * 1000, 3))


def retire(model, keys):
    # En fin de chronologie, les liaisons des pièces retirées restent récupérables dans le parent.
    for key in keys:
        occurrence = model.occ[key]
        assert model.root.features.removeFeatures.add(occurrence), key
    model.refresh()


def feet(model):
    base = cylinder((0, 0, TABLE_Z), (0, 0, TABLE_Z + 4), 15.0)
    for from_z, to_z, r1, r2 in ((-68.2, -61, 15, 9), (-61.2, -8, 9, 9),
                                 (-8.2, -2, 9, 9.8), (-2.2, 0, 9.8, 9.8)):
        boolean(base, cylinder((0, 0, from_z), (0, 0, to_z), r1, r2))
    cut(base, cylinder((0, 0, TABLE_Z - 1), (0, 0, 1), 2.8))
    for i, (x, y) in enumerate(ANCHORS, 1):
        occurrence = model.place(f"Pied_Rehausse_{i}", "Entretoise d’ancrage 72 mm",
                                 "01_Platine", model.tmp.copy(base), PRINT_FOOT, (x, y, 0))
        put_attr(occurrence.component, "Impression_AxeZ", "+Z")


def core_changes(model):
    model.require_copy()
    if get_attr(model.root, "Revision") or len(model.occ) != 154:
        raise RuntimeError("Repartir d’une archive V5 roulis v1 intacte.")
    model.pose({})
    for motion in list(model.root.motionLinks):
        if motion.name in ("Tambours de J2R", "Tambours de J3R"):
            assert motion.deleteMe()
    for axis in ("J2R", "J3R"):
        convert_to_rigid(model, axis)
    fuse_shaft(model, "J2_Chape_Tangage", "07_Bras", 10.2)
    fuse_shaft(model, "J3_Chape_Tangage", "08_Avant_bras", 7.8)
    # Déposer d’abord les tambours qui dépendent directement des moteurs.
    keys = sorted((k for k in model.occ if k in (*RETIRED, *HISTORICAL_CABLES)
                   or k.startswith(RETIRED_PREFIX)), key=lambda k: not k.startswith("Tambour_"))
    retire(model, keys)
    for name in ("Calibration", "Courses_deg", "Moteurs"):
        attr = json.loads(get_attr(model.root, name))
        for key in ("J2R", "J3R", "P2RM", "P3RM"):
            attr.pop(key, None)
        put_attr(model.root, name, attr)
    put_attr(model.root, "Source", dict(document="AURA-01 V5 — Revue design · Roulis épaule et coude",
                                       version=1, sha256=BASELINE_SHA))
    put_attr(model.root, "PlanDeTravail", {"plan_table_mm":TABLE_Z, "ancrage_xy_mm": ANCHORS})
    put_attr(model.root, "Revision", REVISION)
    feet(model)
    model.refresh()
    print(json.dumps({"occurrences": len(model.occ), "links": model.root.motionLinks.count,
                      "table_z_mm": TABLE_Z, "retired": keys, "calibration": list(model.cal)}))


def run(_context):
    core_changes(Model())
