"""Copie de travail pleine grandeur: main motorisée et implantation embarquée."""

import importlib.util
import math
from pathlib import Path

import adsk
import adsk.core as core
import adsk.fusion as fusion


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "03_Integration"
ARCHIVE = ROOT / "AURA-01 — V3 — Intégration mécatronique.f3d"
REVISION = 3
LIMITS = {"J1": (-70, 70), "J2": (-31, 14), "J3": (-22, 25), "J4": (-32, 31),
          "J5": (-36, 36), "J6": (-29, 29), "Paume": (-55, 55)}
FINGERS = (
    ("P", "Pouce", (44, -78.7, 0), -51),
    ("I", "Index", (112, -54, 0), -1),
    ("M", "Majeur", (117, -18, 0), 0),
    ("A", "Annulaire", (113, 18, 0), 0),
    ("O", "Auriculaire", (107, 54, 0), 2),
)


def load(name):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"aura_integration_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Finger:
    def __init__(self, bench, code, label, frame):
        self.bench = bench
        self.g = bench.g
        self.base = bench.base
        self.frame = frame
        self.label = label
        self.code = code

    def key(self, local):
        return local if local == "Paume" else self.code + "_" + local

    def part(self, key, title, body, finish, origin, axis=None, typed=None):
        frame = self.base.compose(self.frame, self.base.frame(origin))
        return self.bench.part(self.key(key), self.label + " · " + title, body, finish, axis=axis,
                               typed=typed, placement=frame)

    def rigid(self, child, parent):
        return self.bench.rigid(self.key(child), self.key(parent))

    def pivot(self, key, rotor, stator, point):
        return self.bench.pivot(self.key(key), self.key(rotor), self.key(stator), self.key(point))

    def ring(self, *args):
        return self.bench.ring(*args)


def palm(bench, forms, finger_script):
    g = bench.g
    body = g.rounded(8, 97, -65, 66, -11.3, 8.9, 20)
    g.union(body, g.rounded(.85, 32, -19.5, 19.5, -13.2, 8.9, 5.8))
    g.cut(body, forms.bore((0, 0, 0), 0, 28.5, 5.20, "x", -1),
          g.rounded(11, 83, -55, 55, -13.4, 4.7, 9))
    for x in (20, 77):
        for y in (-16, 15):
            g.union(body, g.cyl((x, y, -11.60), (x, y, 5.04), 2.25))
            g.cut(body, g.cyl((x, y, -12.1), (x, y, -1), 1.22))
    corner = g.rounded(12, 52, -65, -45, -4, 8.9, 6)
    g.union(body, corner)
    for _, _, origin, yaw in FINGERS:
        anchors = g.rounded(-38, -17.5, -14.9, 14.9, 1.8, 8.9, 3)
        for lug in forms.finger_fork(0, -30):
            g.union(anchors, lug)
        finger_script.coupler_pocket(bench, anchors, 0)
        finger_script.passive_stop(bench, anchors, 0)
        g.union(body, forms.move(anchors, origin, yaw))
        sweep = g.cyl((0,-11.72,0),(0,11.72,0),16.2)
        g.cut(body, forms.move(sweep, origin, yaw))
    return body


def link(bench, key, parent, motion_limits):
    joint = bench.pivot(key, key, parent)
    m = joint.jointMotion
    at = m.rotationValue
    low, high = (at + math.radians(x) for x in motion_limits)
    m.rotationLimits.minimumValue = low
    m.rotationLimits.maximumValue = high
    m.rotationLimits.isMinimumValueEnabled = True
    m.rotationLimits.isMaximumValueEnabled = True
    return joint


def structural_chain(bench, shape_source, forms, finger_script):
    b = bench.base
    frames = {"Socle": b.frame(), "J1": b.frame((0, 0, 27.2))}
    joints = {}
    bench.part("Socle", "Socle ancré · repris de la V3 r03", forms.fixed()[0],
               "dark", placement=frames["Socle"]).isGrounded = True
    bench.part("J1", "J1 · tourelle de départ r03", forms.turret()[0], "ice", axis="z", placement=frames["J1"])
    joints["J1"] = link(bench, "J1", "Socle", LIMITS["J1"])
    parent, offset = "J1", (0, 0, 69)
    for n, (length, _, _, pitch) in enumerate(shape_source.ARM, 2):
        key = f"J{n}"
        frames[key] = b.compose(frames[parent], b.frame(offset, pitch=pitch))
        bench.part(key, f"{key} · segment r03", forms.arm(n - 1)[0], "dark", axis="y", placement=frames[key])
        joints[key] = link(bench, key, parent, LIMITS[key])
        parent, offset = key, (length, 0, 0)
    for key, label, offset, angle, orient, body in (
        ("J5", "J5 · déviation du poignet r03", offset, 0, "z", forms.yaw()[0]),
        ("J6", "J6 · flexion du poignet r03", (45, 0, 8.5), 12, "y", forms.pitch()[0]),
        ("Paume", "J7 · paume blanche, interfaces des cinq doigts", (40.3, 0, 0), 0, "x",
         palm(bench, forms, finger_script)),
    ):
        frames[key] = b.compose(frames[parent], b.frame(offset, pitch=angle))
        bench.part(key, label, body, "white" if key == "Paume" else "ice", axis=orient,
                   placement=frames[key], print_face=180 if key == "Paume" else None)
        joints[key] = link(bench, key, parent, LIMITS[key])
        parent = key
    return frames, joints


def hand(bench, forms, fingers, palm_frame, util):
    report = []
    for code, label, origin, yaw in FINGERS:
        frame = bench.base.compose(palm_frame, bench.base.frame(origin, yaw=yaw))
        fk = Finger(bench, code, label, frame)
        parent = "Paume"
        for i, x in enumerate(fingers.ORIGINS, 1):
            name = f"Phalange_{i}"
            shell, motor = fingers.phalanx(fk, forms, i)
            fk.part(name, f"phalange {i}", shell, "white", (x, 0, 0))
            fingers.put_rings(fk, i, x, parent, name)
            joint = fingers.actuate(fk, i, x, parent, name, motor)
            fk.part(f"Cable_{i}", f"sortie gaine P{i}", fingers.cable_exit(fk.g), "accent", (x, 0, 0))
            fk.rigid(f"Cable_{i}", name)
            parent = name

            motion = joint.jointMotion
            zero = motion.rotationValue
            marker = bench.base.point((19, 0, 0))
            normal = bench.base.vector((0, 0, 1))
            normal.transformBy(frame)
            occ = bench.parts[fk.key(name)]
            opened = marker.copy()
            opened.transformBy(occ.transform2)
            util.apply_pose(motion, 7, zero)
            moved = marker.copy()
            moved.transformBy(occ.transform2)
            direct = 1 if opened.vectorTo(moved).dotProduct(normal) < 0 else -1
            stroke = 10 * opened.distanceTo(moved)
            util.apply_pose(motion, 0, zero)
            limits = motion.rotationLimits
            limits.minimumValue, limits.maximumValue = sorted((zero, zero + direct * math.radians(fingers.RANGE)))
            limits.isMinimumValueEnabled = True
            limits.isMaximumValueEnabled = True
            report.append((code, i, joint, zero, direct, round(stroke, 3)))
    return report


def vendor_shapes(bench, file):
    app = bench.app
    document = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    try:
        design = bench.get_design(document)
        design.designType = fusion.DesignTypes.DirectDesignType
        reader = app.importManager
        opt = reader.createSTEPImportOptions(str(file))
        if not reader.importToTarget(opt, design.rootComponent):
            raise RuntimeError(f"Lecture impossible {file.name}.")
        bodies = list(design.rootComponent.bRepBodies)
        for occurrence in design.rootComponent.allOccurrences:
            bodies.extend(occurrence.bRepBodies)
        result = [bench.g.manager.copy(b) for b in bodies if b.isSolid]
        if not result:
            raise RuntimeError(f"Aucun solide reconnu dans {file.name}.")
        return result
    finally:
        document.close(False)
        bench.doc.activate()


def place_vendors(bench, frames):
    vendors = {m: vendor_shapes(bench, ROOT / "Plans_constructeurs" / f"{m}_ROBOTIS.step")
               for m in ("XM540", "XM430", "XC330")}
    b = bench.base
    out = {}
    lateral = [(0, 0, -1), (-1, 0, 0), (0, 1, 0)]
    upright = [(0, 1, 0), (-1, 0, 0), (0, 0, 1)]
    forward = [(0, 0, 1), (0, -1, 0), (1, 0, 0)]
    for key, code, rel, basis in (
        ("J1", "XM430", (0, 0, -22), upright),
        ("J3", "XM540", (0, 0, 0), lateral),
        ("J4", "XM430", (0, 0, 0), lateral),
        ("J5", "XC330", (0, 0, -10), upright),
        ("J6", "XM430", (0, 0, 0), lateral),
        ("Paume", "XC330", (-5, 0, 0), forward),
    ):
        a = core.Matrix3D.create()
        a.setWithCoordinateSystem(b.point(rel), *(b.vector(v) for v in basis))
        position = b.compose(frames[key], a)
        bodies = vendors[code]
        motor = []
        for i, form in enumerate(bodies, 1):
            part = f"OEM_{key}_{i}"
            bench.part(part, f"{key} · {code} STEP ({i}) · implantation à vérifier",
                       bench.g.manager.copy(form), "metal", placement=position, typed=f"ROBOTIS {code}")
            bench.rigid(part, "Socle" if key == "J1" else key)
            motor.append(part)
        out[key] = {"famille": code, "solides": motor}
    return out


def isolated_pose_check(joints, zeros, pose, util):
    for key, joint in joints.items():
        util.apply_pose(joint.jointMotion, pose.get(key, 0), zeros[key])


def build(app, base, util, report, write, export_archive, open_f3d, get_design):
    OUT.mkdir(exist_ok=True)
    finger_script, energy, cabling = load("doigt"), load("energie"), load("faisceau")
    form_source = finger_script.source_geometry()
    bench = util.Bench(app, base, get_design, "AURA-01 — V3 — Intégration mécatronique")
    forms = form_source.Printable(base, bench.g)
    frames, joints = structural_chain(bench, form_source, forms, finger_script)
    fingers = hand(bench, forms, finger_script, frames["Paume"], util)
    hand_keys = {"Paume"} | {k for k in bench.parts if k[0:2] in {"P_", "I_", "M_", "A_", "O_"}}
    base_keys = set(bench.parts) - hand_keys
    energy.module_layout(bench)
    energy.hand_modules(bench, frames["Paume"])
    brace = energy.loom(bench, frames)
    sources = place_vendors(bench, frames)
    zeros = {key: j.jointMotion.rotationValue for key, j in joints.items()}
    oem = {k for k in bench.parts if k.startswith("OEM_")}
    module_keys = {k for k in bench.parts if k.startswith(("E_", "E0", "Connecteur_", "Faisceau_"))}
    poses = []
    for flexion in (0, 12, 24, 36, 45):
        for _, _, j, zero, sign, _ in fingers:
            util.apply_pose(j.jointMotion, flexion, zero, sign)
        poses.append({"flexion_simultanee": flexion, "interferences": bench.measure(keys=hand_keys)})
        adsk.doEvents()
    for pose in ({"P": (27, 45, 27), "I": (45, 28, 34), "M": (38, 41, 39)},
                 {"P": (0, 30, 18), "I": (45, 14, 2), "A": (40, 45, 44), "O": (45, 25, 19)},
                 {"M": (45, 45, 45), "O": (45, 45, 45)}):
        for code, i, j, zero, sign, _ in fingers:
            util.apply_pose(j.jointMotion, pose.get(code, (0, 0, 0))[i - 1], zero, sign)
        poses.append({"flexions_individuelles": pose, "interferences": bench.measure(keys=hand_keys)})
        adsk.doEvents()
    for _, _, j, zero, sign, _ in fingers:
        util.apply_pose(j.jointMotion, 0, zero, sign)
    original_vendor_assembly = {part: axis for axis, model in sources.items() for part in model["solides"]}
    oem_collisions = [hit for hit in bench.measure(keys=base_keys | {"Paume"} | oem)
                      if original_vendor_assembly.get(hit["a"],"structure") != original_vendor_assembly.get(hit["b"],"structure")]
    for key in oem:
        bench.parts[key].isLightBulbOn = False
    arms = []
    states = ({}, {"J1": -52}, {"J1": 52}, {"J2": -25, "J3": 17, "J4": 18},
              {"J5": 27, "J6": -20, "Paume": 35}, {"J5": -27, "J6": 20, "Paume": -35})
    for i, state in enumerate(states, 1):
        isolated_pose_check(joints, zeros, state, util)
        hits = bench.measure(keys=base_keys | {"Paume"} | module_keys)
        flexibles, snapshot = cabling.study(bench, energy, base_keys | {"Paume", "E_Batterie",
                                                                       "E_Pi5", "E_Coupure"})
        if not state:
            home = snapshot
        arms.append({"angles": state, "interferences": [hit for hit in hits
                     if hit["a"] in module_keys or hit["b"] in module_keys],
                     "boucles_de_service": flexibles})
        report["progression_boucles"] = {"poses": i, "cible": len(states)}
        write(report)
        adsk.doEvents()
    isolated_pose_check(joints, zeros, {}, util)
    for name, vertices, radius in home:
        key = "Boucle_HOME_" + name
        bench.part(key, name + " · enveloppe flexible à HOME", energy.tube(bench, vertices, radius), "accent")
        bench.rigid(key, "Socle")
        bench.parts[key].isLightBulbOn = False
    report["integration"] = {
        "pivots_r03_repris": len(joints),
        "pivots_doigts_motorises": len(fingers),
        "avance_temoin_7deg_mm": {code + str(i): v for code, i, _, _, _, v in fingers},
        "modeles_moteurs_constructeurs": sources,
        "interferences_implantations_OEM": oem_collisions,
        "positions_doigts_mm": FINGERS,
        "poses_main": poses,
        "encombrements_electriques": arms,
        "longueurs_troncons_droits_mm": brace,
        "batterie_dimensions_mm": energy.BAT_DIMS,
        "batterie": energy.BATTERY,
        "solides_mecaniques_repris": sorted(base_keys),
        "statut_J2": "Banc J2 indépendant. J2 de l'assemblage r03 représente une articulation virtuelle.",
    }
    report.pop("progression_boucles",None)
    write(report)
    bench.camera((120, 0, 85), (340, -615, 415), 920, OUT / "Integration_HOME.png")
    export_archive(bench.design, ARCHIVE)
    data = report["integration"]
    data["archive"] = ARCHIVE.name
    data["sha256"] = util.digest(ARCHIVE)
    output = bench.parts["Paume"].transform2
    b = bench.base
    base_xyz = b.point((65, 0, 0))
    base_xyz.transformBy(output)
    t = tuple(x * 10 for x in base_xyz.asArray())
    for _, _, joint, zero, sign, _ in fingers:
        util.apply_pose(joint.jointMotion, 36, zero, sign)
    bench.camera(t, (t[0] + 117, t[1] - 184, t[2] + 115), 318, OUT / "Main_fermee.png")
    for _, _, joint, zero, sign, _ in fingers:
        util.apply_pose(joint.jointMotion, 0, zero, sign)
    # The calibration geometry is exported beside the trial parts, outside the assembly archive.
    counts = bench.root.occurrences.count, bench.root.asBuiltJoints.count
    bench.part("E04_Coupon_ajustements", "Coupon perçages, roulements et bagues", energy.coupon(bench.g),
               "white", (-85, 230, 0), print_face=0)
    data["fabrication"] = bench.export_prints(OUT)
    bench.parts["E04_Coupon_ajustements"].deleteMe()
    document = open_f3d(app, ARCHIVE)
    reopened = get_design(document)
    data["rouvert_dans_fusion"] = counts == (reopened.rootComponent.occurrences.count,
                                            reopened.rootComponent.asBuiltJoints.count)
    data["liaisons_archive_rouverte"] = reopened.rootComponent.asBuiltJoints.count
    data["termine"] = True
    write(report)
    document.activate()
