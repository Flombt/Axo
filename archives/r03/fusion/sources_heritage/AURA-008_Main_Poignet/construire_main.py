"""Modèle V3 séparé, cinématique à tendons et contrôle volumique dans Fusion."""

import json
import math
from hashlib import sha256
from pathlib import Path
import sys
import tempfile

import adsk.core as core
import adsk.fusion as fusion


OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "AURA-007_Bras_Table"))
sys.path.insert(0, str(OUT))

from construire_table import Assembly, capture, get_design
from formes_articulees import (
    ArticulatedForms, COURSE, CURSOR, DIGITS, DRUM, MOTOR_H, WIND,
)
from geometrie import compose, frame, point, vector
from geometrie_table import ANGLES_REPOS, HAUTEUR_EPAULE, HAUTEUR_TOURELLE, LONGUEURS


TITLE = "AURA-01 — V3 de table — Main et poignet articulés"
TAG = "AURA-008 · V3 de table · r01"
ARCHIVE = OUT / "AURA-01_V3_Main_Poignet_r01.f3d"
REPORT = OUT / "Verification_Fusion.json"
BASE_RANGES = ((-30, 30), (-12, 12), (-13, 18), (-36, 36))
FIXED_AXES = ("03_Tourelle", "04_Segment_1", "05_Segment_2", "07_Paume")
DEMO = (
    (0, 0, 0, 0, 0),
    (0, 8, 10, -30, 0),
    (0, 8, 10, 34, 0),
    (0, 8, 10, 34, 1),
    (0, 8, 10, -27, 1),
    (0, 8, 10, -27, 0),
    (0, 0, 0, 0, 0),
)


def write_report(data):
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Brazo(Assembly):
    def __init__(self, document):
        self.design = get_design(document)
        self.design.designType = fusion.DesignTypes.ParametricDesignType
        self.root = self.design.rootComponent
        self.forms = ArticulatedForms(self.design)
        self.occ, self.prints, self.markers, self.joints = {}, {}, {}, {}
        self.flexion = {}
        self.print_groups = {}
        self.hand_axes = {}
        self.native_links = False

    def build(self):
        f = self.forms
        base, pod, turret = frame(), frame((0, 0, 4.25)), frame((0, 0, HAUTEUR_TOURELLE))
        arm = compose(turret, frame((0, 0, HAUTEUR_EPAULE), pitch=ANGLES_REPOS[0]))
        fore = compose(arm, frame((LONGUEURS[0], 0, 0), pitch=ANGLES_REPOS[1]))
        end = compose(fore, frame((LONGUEURS[1], 0, 0), pitch=ANGLES_REPOS[2]))
        palm = compose(end, f.wrist_frame())
        self.printed("01_Platine", "01 · Platine et commande", base, f.base(), "dark").isGrounded = True
        self.printed("02_Socle", "02 · Socle évasé, pivot manuel", pod, f.manual_pod(), "dark", 180)
        self.fixed("01_Platine", "02_Socle")
        self.printed("03_Tourelle", "03 · Tourelle et chape MG996R", turret, f.turret_large(), "ice", 180, "z")
        self.hinge("02_Socle", "03_Tourelle", "J1 · Orientation manuelle du socle", "z", BASE_RANGES[0])
        self.printed("04_Segment_1", "04 · Segment 1, bras supérieur", arm, f.arm(), "dark", 90, "y")
        self.hinge("03_Tourelle", "04_Segment_1", "J2 · Élévation de l’épaule", "y", BASE_RANGES[1])
        self.printed("05_Segment_2", "05 · Segment 2, avant-bras", fore, f.forearm(), "dark", 0, "y")
        self.hinge("04_Segment_1", "05_Segment_2", "J3 · Flexion du coude", "y", BASE_RANGES[2])
        self.printed("06_Segment_3", "06 · Segment 3, logement du poignet", end, f.inside_wrist(), "ice")
        self.fixed("05_Segment_2", "06_Segment_3")
        self.printed("07_Paume", "07 · Paume blanche et selle MG90S", palm, f.palm(), "white", 180, "x")
        self.hinge("06_Segment_3", "07_Paume", "J7 · Roulis du poignet", "x", BASE_RANGES[3])
        for i, (parent, placement) in enumerate((("04_Segment_1", arm), ("05_Segment_2", fore))):
            key = f"0{8+i}_Capot"
            self.printed(key, f"0{8+i} · Capot démontable du segment {i+1}",
                         placement, f.lid(LONGUEURS[i]), "accent")
            self.fixed(parent, key)

        for n, parent, parent_frame, child, child_frame, x, z in (
            (2, "03_Tourelle", turret, "04_Segment_1", arm, 0, HAUTEUR_EPAULE),
            (3, "04_Segment_1", arm, "05_Segment_2", fore, LONGUEURS[0], 0),
        ):
            name, body = ("MG996R", f.large_servo()) if n == 2 else ("MG90S", f.servo())
            self.hardware(f"SERVO_J{n}", f"{name} · Épaule J2" if n == 2 else "MG90S · Coude J3",
                          parent, compose(parent_frame, f.servo_lat(x, z)), body, "rubber")
            self.hardware(f"PAL_J{n}", f"Palonnier J{n} · enveloppe", child,
                          compose(child_frame, f.servo_lat(0)), f.horn())
            self.hardware(f"AXE_J{n}", f"Axe passif M3 · J{n}", parent,
                          compose(parent_frame, frame((x, 0, z))), f.pin())
        stator = compose(palm, f.wrist_servo_frame())
        self.hardware("SERVO_J7", "MG90S · Rotation du poignet", "06_Segment_3", stator, f.servo(), "rubber")
        self.hardware("PAL_J7", "Palonnier de roulis · enveloppe", "07_Paume", stator, f.horn())
        servo_h = compose(palm, f.hand_servo_frame())
        self.hardware("SERVO_T1", "MG90S · Fermeture des cinq doigts", "07_Paume", servo_h, f.servo(), "rubber")
        bolt = f.union(f.hole_z(0, 0, -10.3, 3.7, 2), f.hole_z(0, 0, 3.6, 5.9, 4.0))
        self.hardware("AXE_J1", "M4 · Axe de socle orientable", "02_Socle", turret, bolt)

        nano, usb, chip = f.nano()
        self.add("CTRL", "Nano ATmega328P · encombrement", frame((-46, 0, 8.7)),
                 [(nano, "accent", "Carte Nano"), (usb, "metal", "Prise USB"),
                  (chip, "dark", "Microcontrôleur")])
        self.fixed("01_Platine", "CTRL")
        bouton = f.union(f.hole_z(0, 0, 0.25, 4.25, 5.9),
                         f.hole_z(0, 0, 4, 6, 7.6), f.hole_z(0, 0, 5.8, 7.8, 4.3))
        self.hardware("BTN", "Bouton de lancement · encombrement", "01_Platine",
                      frame((43, -28, 0)), bouton, "accent")

        self.moveable_hand(palm)
        if len(self.occ) != self.root.occurrences.count:
            raise RuntimeError("Chaque occurrence doit être vérifiée sous un identifiant distinct.")
        self.root.attributes.add("AURA-01", "Reference", TAG)

    def moveable_hand(self, palm):
        f = self.forms
        self.printed("10_Tambour", "10 · Tambour de traction", compose(palm, frame(DRUM)),
                     f.drum(), "accent", -90, "y")
        self.hinge("07_Paume", "10_Tambour", "T1 · Fermeture groupée des doigts", "y", (-2, WIND+2))
        self.hardware("PAL_T1", "Palonnier du tambour · enveloppe", "10_Tambour",
                      compose(palm, f.hand_servo_frame()), f.horn())

        cursor = self.printed("11_Palonnier", "11 · Traverse des cinq tendons", compose(palm, frame(CURSOR)),
                              f.cursor(), "accent", 0, "x")
        edge = next(e for e in self.markers["11_Palonnier"].edges if core.Circle3D.cast(e.geometry))
        geo = fusion.JointGeometry.createByCurve(edge, fusion.JointKeyPointTypes.CenterKeyPoint)
        collection = self.root.asBuiltJoints
        input_ = collection.createInput(cursor, self.occ["07_Paume"], geo)
        if not input_.setAsSliderJointMotion(fusion.JointDirections.ZAxisJointDirection):
            raise RuntimeError("Course du répartiteur refusée.")
        self.slider = collection.add(input_)
        self.slider.name = "T2 · Course du répartiteur"
        self.slider.isLightBulbOn = self.markers["11_Palonnier"].isLightBulbOn = False

        for letter, name, pos, yaw, roll, lengths, angles in DIGITS:
            at = compose(palm, frame(pos, yaw=yaw, roll=roll))
            parent = "07_Paume"
            for i, (length, angle) in enumerate(zip(lengths, angles), 1):
                code = f"{letter}{i}"
                label = f"{name} · Phalange {i}"
                pin = f.hole_y(0, 0, -4.33, 4.33, 0.99)
                group = f"Phalange_{'pouce' if letter=='P' else 'doigt'}_{i}"
                self.add(code, label, at,
                         [(f.phalanx(length, i == 3), "white", f"FDM · {code}"),
                          (pin, "metal", f"Axe Ø2 · {code}")], print_orientation=0, axis="y")
                self.hinge(parent, code, f"{code} · {label}", "y", (-1.5, angle+2))
                self.flexion[code] = angle
                self.print_groups[code] = group
                at = compose(at, frame((length, 0, 0)))
                parent = code

    def calibrate_axes(self):
        self.calibration = {}
        directions = {"x": (1, 0, 0), "y": (0, -1, 0), "z": (0, 0, 1)}
        for key, (motion, axis, bounds) in self.joints.items():
            origin = motion.rotationValue
            before = self.occ[key].transform2
            handed = directions[axis] if key not in self.flexion else (0, 1, 0)
            n = vector(handed)
            n.transformBy(before)
            test = math.radians(4)
            motion.rotationValue = origin + test
            witness = (0, 18, 0) if axis == "x" else (18, 0, 0)
            p, moved, center = point(witness), point(witness), point((0, 0, 0))
            p.transformBy(before)
            moved.transformBy(self.occ[key].transform2)
            center.transformBy(before)
            travel = p.distanceTo(moved)*10
            if not 1.21 < travel < 1.31:
                raise RuntimeError(f"Course angulaire incorrecte {key} : {travel:.3f} mm.")
            sign = 1 if n.crossProduct(center.vectorTo(p)).dotProduct(p.vectorTo(moved)) > 0 else -1
            motion.rotationValue = origin
            limits = motion.rotationLimits
            limits.minimumValue, limits.maximumValue = sorted(origin+sign*math.radians(a) for a in bounds)
            limits.isMinimumValueEnabled = limits.isMaximumValueEnabled = True
            self.calibration[key] = origin, sign, round(travel, 4)
        motion = self.slider.jointMotion
        zero = motion.slideValue
        old = self.occ["11_Palonnier"].transform2
        motion.slideValue = zero+0.1
        delta = self.occ["11_Palonnier"].transform2.translation
        delta.subtract(old.translation)
        x = vector((-1, 0, 0))
        x.transformBy(old)
        value = x.dotProduct(delta)
        if not 0.09 < abs(value) < 0.11:
            raise RuntimeError(f"Course de la traverse incorrecte : {value} cm.")
        sign = 1 if value > 0 else -1
        motion.slideValue = zero
        lim = motion.slideLimits
        lim.minimumValue, lim.maximumValue = sorted((zero-sign*0.025, zero+sign*(COURSE+0.25)/10))
        lim.isMinimumValueEnabled = lim.isMaximumValueEnabled = True
        self.slider_zero = (zero, sign)

    def set_rotation(self, code, angle):
        motion = self.joints[code][0]
        origin, sign, _ = self.calibration[code]
        goal = origin+sign*math.radians(angle)
        if abs(motion.rotationValue-goal) > 1e-7:
            motion.rotationValue = goal
        if abs(motion.rotationValue-goal) > math.radians(0.09):
            actual = self.angle(code)
            raise RuntimeError(f"Pose refusée sur {code} : {angle:.3f}°, obtenue {actual:.3f}°.")

    def angle(self, code):
        origin, sign, _ = self.calibration[code]
        return math.degrees(self.joints[code][0].rotationValue-origin)*sign

    def position(self, pose):
        if self.native_links:
            axis_changed = any(abs(self.angle(code)-angle) > 0.0001
                               for code, angle in zip(FIXED_AXES, pose[:4]))
            if axis_changed:
                # Fusion sometimes locks a parent pivot while the shared rotation
                # constraints are displaced. Set the arm first, then the grip.
                self.set_rotation("10_Tambour", 0)
        for code, angle in zip(FIXED_AXES, pose[:4]):
            self.set_rotation(code, angle)
        grip = pose[4]
        self.set_rotation("10_Tambour", grip*WIND)
        zero, sign = self.slider_zero
        if not self.native_links:
            for code, angle in self.flexion.items():
                self.set_rotation(code, grip*angle)
            self.slider.jointMotion.slideValue = zero+sign*grip*COURSE/10
        else:
            for code, angle in self.flexion.items():
                if abs(self.angle(code)-grip*angle) > 0.3:
                    raise RuntimeError(f"Suivi du doigt incorrect : {code}.")
            if abs(self.slider.jointMotion.slideValue-zero-sign*grip*COURSE/10)>0.025:
                raise RuntimeError("Course du répartiteur incohérente.")

    def link_fingers(self):
        self.position((0, 0, 0, 0, 0))
        joints = {j.name.split(" · ")[0]:j for j in self.root.asBuiltJoints}
        collection = self.root.motionLinks
        master = joints["T1"]
        unit = core.ValueInput.createByString
        rot = fusion.JointMotionTypes.RevoluteJointRotateMotionType
        slide = fusion.JointMotionTypes.SliderJointSlideMotionType
        for code, angle in self.flexion.items():
            spec = collection.createInput(master, joints[code])
            spec.motionOne, spec.valueOne = rot, unit(f"{WIND} deg")
            spec.motionTwo, spec.valueTwo = rot, unit(f"{angle} deg")
            spec.isReversed = self.calibration["10_Tambour"][1] != self.calibration[code][1]
            link = collection.add(spec)
            if not link:
                raise RuntimeError(f"Couplage Fusion refusé : {code}.")
            link.name = "Tendon · " + code
        spec = collection.createInput(master, self.slider)
        spec.motionOne, spec.valueOne = rot, unit(f"{WIND} deg")
        spec.motionTwo, spec.valueTwo = slide, unit(f"{COURSE} mm")
        spec.isReversed = self.calibration["10_Tambour"][1] != self.slider_zero[1]
        link = collection.add(spec)
        if not link:
            raise RuntimeError("Raccord tambour-traverse refusé.")
        link.name = "Enroulement · Traverse"
        self.native_links = True
        for grip in (0.25, 0.5, 0.75, 1, 0):
            self.position((0, 0, 0, 0, grip))

    def weights_after(self, joint):
        printed = ["05_Segment_2", "06_Segment_3", "07_Paume", "09_Capot", "10_Tambour", "11_Palonnier",
                   *self.flexion.keys()]
        hardware = {"SERVO_J7": 13.4, "SERVO_T1": 13.4, "PAL_J7": 0.75,
                    "PAL_T1": 0.75, "PAL_J3": 0.75}
        if joint == "04_Segment_1":
            printed += ["04_Segment_1", "08_Capot"]
            hardware.update({"SERVO_J3": 13.4, "PAL_J2": 0.9, "AXE_J3": 2})
        weights = []
        for key in printed+list(hardware):
            occ = self.occ[key]
            for body in occ.component.bRepBodies:
                if body.name == "Repère de liaison":
                    continue
                density = 7.85 if body.name.startswith("Axe Ø2") else 1.27
                weights.append((occ, hardware.get(key, body.volume*density),
                                body.physicalProperties.centerOfMass))
        weights.append((self.occ["07_Paume"], 10, point((20, 0, -5))))
        return weights

    def check(self):
        tests = list(DEMO)
        for twist in (-36, 0, 36):
            for fraction in (0, 0.25, 0.5, 0.75, 1):
                tests.append((0, 0, 0, twist, fraction))
        for start, finish in zip(DEMO, DEMO[1:]):
            for n in range(1, 7):
                tests.append(tuple(round(a+(b-a)*n/7, 4) for a, b in zip(start, finish)))
        for j1 in (-30, 30):
            for j2 in (-12, 12):
                for j3 in (-13, 18):
                    for j7 in (-36, 36):
                        tests.append((j1, j2, j3, j7, 1))
        errors = []
        poses = list(dict.fromkeys(tests))
        axes = dict(zip(("J2", "J3"), FIXED_AXES[1:3]))
        hardware = {name: self.weights_after(axis) for name, axis in axes.items()}
        maximum = {name: (0, (0, 0, 0, 0, 0)) for name in axes}
        for pose in poses:
            self.position(pose)
            hits = self.interference()
            if hits:
                errors.append({"pose": pose, "interferences": hits})
            for name, axis in axes.items():
                maximum[name] = max(maximum[name], (self.gravity(axis, hardware[name]), pose))
        self.position((0, 0, 0, 0, 0))
        moments = {name: {"Nm": round(value, 4), "pose": pose,
                          "masse_mobile_g": round(sum(w[1] for w in hardware[name]), 1)}
                   for name, (value, pose) in maximum.items()}
        return poses, errors, moments


def camera(app, detail=False, movie=False):
    view = app.activeViewport
    cam = view.camera
    cam.cameraType = core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.upVector = vector((0, 0, 1))
    if detail:
        cam.target, cam.eye = point((151, -3, 100)), point((268, -130, 217))
        cam.setExtents(170/10, 124/10)
    elif movie:
        cam.target, cam.eye = point((60, 0, 83)), point((163, -432, 255))
        cam.setExtents(351/10, 223/10)
    else:
        cam.target, cam.eye = point((59, -1, 63)), point((173, -427, 249))
        cam.setExtents(321/10, 194/10)
    view.camera = cam
    view.refresh()
    return view


def export_archive(app, doc, rig):
    with tempfile.TemporaryDirectory(prefix="AURA008_Fusion_") as folder:
        local = Path(folder)/ARCHIVE.name
        export = rig.design.exportManager
        if not export.execute(export.createFusionArchiveExportOptions(str(local))):
            raise RuntimeError("Archive de la main non exportée.")
        importer = app.importManager
        opened = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(local)))
        root = get_design(opened).rootComponent
        counts = (root.allOccurrences.count, root.asBuiltJoints.count, root.motionLinks.count)
        expected = (rig.root.allOccurrences.count, rig.root.asBuiltJoints.count, rig.root.motionLinks.count)
        if counts != expected:
            raise RuntimeError(f"Relu {counts}, attendu {expected}.")
        opened.close(False)
        ARCHIVE.write_bytes(local.read_bytes())
    doc.activate()
    return {"fichier": ARCHIVE.name, "sha256": sha256(ARCHIVE.read_bytes()).hexdigest(),
            "occurrences": counts[0], "liaisons": counts[1], "couplages": counts[2]}


def export_prints(app, rig):
    groups = {}
    for key in rig.prints:
        code = rig.print_groups.get(key, key)
        groups.setdefault(code, []).append(key)
    outside = OUT/"STL"
    outside.mkdir(exist_ok=True)
    scratch = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    design = get_design(scratch)
    design.designType = fusion.DesignTypes.DirectDesignType
    geometry = rig.forms
    results = []
    for group, keys in groups.items():
        occurrence, name, roll = rig.prints[keys[0]]
        native = next(b for b in occurrence.component.bRepBodies if b.name == name)
        temporary = geometry.manager.copy(native)
        geometry.place(temporary, frame(roll=roll))
        lo, hi = temporary.boundingBox.minPoint, temporary.boundingBox.maxPoint
        geometry.place(temporary, frame((-(lo.x+hi.x)*5, -(lo.y+hi.y)*5, -10*lo.z)))
        current = design.rootComponent.bRepBodies.add(temporary)
        file = outside/(group+".stl")
        opts = design.exportManager.createSTLExportOptions(current, str(file))
        opts.isBinaryFormat = True
        opts.meshRefinement = fusion.MeshRefinementSettings.MeshRefinementHigh
        if not design.exportManager.execute(opts) or file.stat().st_size <= 84:
            raise RuntimeError(f"Export de {group} refusé.")
        results.append({"reference": group, "quantite": len(keys), "instances": keys, "stl": file.name,
                        "dimensions_mm": [round(10*(a-b), 4) for a,b in zip(hi.asArray(), lo.asArray())],
                        "volume_cm3": round(native.volume, 4),
                        "sha256": sha256(file.read_bytes()).hexdigest()})
    scratch.close(False)
    return results


def run(_context: str):
    app = core.Application.get()
    drafts = [d for d in app.documents if not d.isSaved and d.name == TITLE+" (travail)"]
    document = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    document.name = TITLE + " (travail)"
    rig = Brazo(document)
    rig.build()
    rig.calibrate_axes()
    rig.link_fingers()
    poses, errors, moments = rig.check()
    view = camera(app)
    capture(view, OUT/"Controle_Bras.png", 1400, 900, transparent=True)
    view = camera(app, detail=True)
    capture(view, OUT/"Controle_Main.png", 1400, 950, transparent=True)
    camera(app)
    report = {"fusion": app.version, "poses": len(poses), "erreurs": errors,
              "occurrences": rig.root.allOccurrences.count, "pivots": len(rig.joints),
              "couplages": rig.root.motionLinks.count,
              "pieces_fdm": len(rig.prints), "course_traverse_mm": COURSE,
              "angles_flexion_nominale_deg": rig.flexion, "couple_statique": moments,
              "calibration": rig.calibration, "calibration_traverse": rig.slider_zero}
    write_report(report)
    if not errors:
        report["archive"] = export_archive(app, document, rig)
        write_report(report)
        report["nomenclature"] = export_prints(app, rig)
        document.activate()
        view = camera(app)
        capture(view, OUT/"AURA-01_Bras_Main_Poignet.png", 1740, 1030, transparent=True)
        view = camera(app, detail=True)
        capture(view, OUT/"AURA-01_Main_ouverte.png", 1520, 985, transparent=True)
        rig.position((0, 0, 0, 0, 1))
        view.refresh()
        capture(view, OUT/"AURA-01_Main_fermee.png", 1520, 985, transparent=True)
        rig.position((0, 0, 0, 0, 0))
        camera(app)
        for draft in drafts:
            draft.close(False)
        write_report(report)
    print(json.dumps({k: v for k,v in report.items()
                      if k not in ("calibration", "nomenclature", "erreurs")}, ensure_ascii=False))
    if errors:
        print(json.dumps(errors[:3], ensure_ascii=False))
