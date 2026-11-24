"""Construit un nouveau bras dans Fusion et contrôle ses liaisons natives."""

from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path
import sys
import tempfile

import adsk
import adsk.core as core
import adsk.fusion as fusion

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "AURA_V3" / "Generateur_AURA_V3"))
sys.path.insert(0, str(OUT))

from geometrie import compose, frame, point, vector
from geometrie_table import (
    ANGLES_REPOS, AXE_SERVO, Formes, HAUTEUR_EPAULE, HAUTEUR_TOURELLE,
    LIMITES, LONGUEURS, POSES,
)

TITLE = "AURA-01 — V3 de table — 3 axes"
ARCHIVE = OUT / "AURA-01_V3_de_table_r01.f3d"
CHECKS = OUT / "Verification_Fusion.json"
DESCRIPTION = "AURA-007 — Prototype de table pour présentation — r01"


def write(data):
    CHECKS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_design(document):
    return fusion.Design.cast(document.products.itemByProductType("DesignProductType"))


class Assembly:
    def __init__(self, doc):
        self.design = get_design(doc)
        self.design.designType = fusion.DesignTypes.ParametricDesignType
        self.root = self.design.rootComponent
        self.forms = Formes(self.design)
        self.occ = {}
        self.prints = {}
        self.markers = {}
        self.joints = {}

    def add(self, code, label, at, parts, *, print_orientation=None, axis=None):
        occ = self.root.occurrences.addNewComponent(at)
        component = occ.component
        component.name = label
        feature = component.features.baseFeatures.add()
        feature.name = "Géométrie de " + label.split(" · ")[-1]
        feature.startEdit()
        for i, (shape, appearance, name) in enumerate(parts):
            if not shape.isSolid or shape.lumps.count != 1:
                raise RuntimeError(f"{label} / {name} comporte {shape.lumps.count} volumes.")
            b = component.bRepBodies.add(shape, feature)
            b.name = name
            b.appearance = self.forms.appearances[appearance]
            if i == 0 and print_orientation is not None:
                self.prints[code] = (occ, name, print_orientation)
        if axis:
            marker = component.bRepBodies.add(self.forms.pivot(axis, 0.24, 1.18), feature)
            marker.name = "Repère de liaison"
        feature.finishEdit()
        if axis:
            self.markers[code] = next(b for b in occ.bRepBodies if b.name == "Repère de liaison")
        self.occ[code] = occ
        return occ

    def printed(self, code, label, at, shape, appearance, face=0, axis=None):
        return self.add(code, label, at, [(shape, appearance, "FDM · " + code)],
                        print_orientation=face, axis=axis)

    def hardware(self, code, label, parent, at, shape, appearance="metal"):
        self.add(code, label, at, [(shape, appearance, label)])
        self.fixed(parent, code)

    def fixed(self, parent, child):
        col = self.root.asBuiltJoints
        spec = col.createInput(self.occ[child], self.occ[parent], None)
        if not spec.setAsRigidJointMotion():
            raise RuntimeError(f"Blocage de {child} refusé.")
        j = col.add(spec)
        j.name = "Fixation · " + child
        j.isLightBulbOn = False

    def hinge(self, parent, child, label, axis, bounds):
        body = self.markers[child]
        edge = next(e for e in body.edges if core.Circle3D.cast(e.geometry))
        geometry = fusion.JointGeometry.createByCurve(edge, fusion.JointKeyPointTypes.CenterKeyPoint)
        col = self.root.asBuiltJoints
        spec = col.createInput(self.occ[child], self.occ[parent], geometry)
        if not spec.setAsRevoluteJointMotion(fusion.JointDirections.ZAxisJointDirection):
            raise RuntimeError(f"Pivot de {child} refusé.")
        joint = col.add(spec)
        joint.name = label
        joint.isLightBulbOn = False
        body.isLightBulbOn = False
        self.joints[child] = (joint.jointMotion, axis, bounds)

    def build(self):
        f = self.forms
        base, pod, turret = frame(), frame((0, 0, 4.25)), frame((0, 0, HAUTEUR_TOURELLE))
        arm = compose(turret, frame((0, 0, HAUTEUR_EPAULE), pitch=ANGLES_REPOS[0]))
        forearm = compose(arm, frame((LONGUEURS[0], 0, 0), pitch=ANGLES_REPOS[1]))
        end = compose(forearm, frame((LONGUEURS[1], 0, 0), pitch=ANGLES_REPOS[2]))
        hand = compose(end, f.wrist_frame())
        self.printed("01_Platine", "01 · Platine et commande", base, f.base(), "dark").isGrounded = True
        self.printed("02_Socle", "02 · Socle évasé, logement J1", pod, f.pod(), "dark", 180)
        self.fixed("01_Platine", "02_Socle")
        self.printed("03_Tourelle", "03 · Tourelle et chape d’épaule", turret, f.turret(), "ice", 180, "z")
        self.hinge("02_Socle", "03_Tourelle", "J1 · Rotation du socle", "z", LIMITES[0])
        self.printed("04_Segment_1", "04 · Segment 1, bras supérieur", arm, f.arm(), "dark", 90, "y")
        self.hinge("03_Tourelle", "04_Segment_1", "J2 · Élévation de l’épaule", "y", LIMITES[1])
        self.printed("05_Segment_2", "05 · Segment 2, avant-bras", forearm, f.forearm(), "dark", 0, "y")
        self.hinge("04_Segment_1", "05_Segment_2", "J3 · Flexion du coude", "y", LIMITES[2])
        self.printed("06_Segment_3", "06 · Segment 3 et poignet fixe", end, f.terminal(), "ice")
        self.fixed("05_Segment_2", "06_Segment_3")
        self.printed("07_Main", "07 · Main blanche monobloc", hand, f.hand(), "white")
        self.fixed("06_Segment_3", "07_Main")
        for i, (parent, placement) in enumerate((("04_Segment_1", arm), ("05_Segment_2", forearm))):
            key = f"0{8+i}_Capot"
            self.printed(key, f"0{8+i} · Capot démontable du segment {i+1}",
                         placement, f.lid(LONGUEURS[i]), "accent")
            self.fixed(parent, key)

        placement = compose(pod, frame((0, 0, 30.9)))
        self.hardware("M1", "MG90S · Moteur J1", "02_Socle", placement, f.servo(), "rubber")
        self.hardware("P1", "Palonnier d’origine · J1", "03_Tourelle", placement, f.horn(), "metal")
        for n, parent, parent_frame, child, child_frame, x, z in (
            (2, "03_Tourelle", turret, "04_Segment_1", arm, 0, HAUTEUR_EPAULE),
            (3, "04_Segment_1", arm, "05_Segment_2", forearm, LONGUEURS[0], 0),
        ):
            self.hardware(f"M{n}", f"MG90S · Moteur J{n}", parent,
                          compose(parent_frame, f.servo_lat(x, z)), f.servo(), "rubber")
            self.hardware(f"P{n}", f"Palonnier d’origine · J{n}", child,
                          compose(child_frame, f.servo_lat(0)), f.horn(), "metal")
            self.hardware(f"A{n}", f"Axe passif M3 · J{n}", parent,
                          compose(parent_frame, frame((x, 0, z))), f.pin(), "metal")

        nano, usb, chip = f.nano()
        self.add("CTRL", "Arduino Nano Every · encombrement", frame((-46, 0, 8.7)),
                 [(nano, "accent", "Carte 45 × 18 mm"), (usb, "metal", "Prise USB"),
                  (chip, "dark", "Microcontrôleur")])
        self.fixed("01_Platine", "CTRL")
        bouton = f.union(f.hole_z(0, 0, 0.25, 4.25, 5.9),
                         f.hole_z(0, 0, 4, 6, 7.6), f.hole_z(0, 0, 5.8, 7.8, 4.3))
        self.hardware("BTN", "Bouton de lancement · encombrement", "01_Platine",
                      frame((43, -28, 0)), bouton, "accent")
        self.root.attributes.add("AURA-01", "Reference", "AURA-007 · V3 de table · r01")

    def calibrate(self):
        self.calibration = {}
        for key, (motion, axis, bounds) in self.joints.items():
            origin = motion.rotationValue
            before = self.occ[key].transform2
            others = {k: m.rotationValue for k, (m, _, _) in self.joints.items() if k != key}
            motion.rotationValue = origin + math.radians(5)
            after = self.occ[key].transform2
            witness = point((22, 0, 0))
            original, displaced = witness.copy(), witness.copy()
            original.transformBy(before)
            displaced.transformBy(after)
            pivot = point((0, 0, 0))
            pivot.transformBy(before)
            direction = vector((0, 0, 1) if axis == "z" else (0, -1, 0))
            direction.transformBy(before)
            reference = direction.crossProduct(pivot.vectorTo(original))
            sign = 1 if reference.dotProduct(original.vectorTo(displaced)) > 0 else -1
            distance = original.distanceTo(displaced) * 10
            drift = max(abs(math.degrees(self.joints[k][0].rotationValue - value))
                        for k, value in others.items())
            if not 1.87 < distance < 1.97 or drift > 0.1:
                raise RuntimeError(f"Mouvement {key} incohérent : {distance:.3f} mm, {drift:.3f}° induits.")
            motion.rotationValue = origin
            limits = motion.rotationLimits
            lo, hi = sorted(origin + sign * math.radians(angle) for angle in bounds)
            limits.minimumValue = lo
            limits.maximumValue = hi
            limits.isMinimumValueEnabled = limits.isMaximumValueEnabled = True
            self.calibration[key] = (origin, sign, round(distance, 4), round(drift, 6))

    def move(self, pose):
        for (key, (motion, _, _)), value in zip(self.joints.items(), pose):
            origin, sign, _, _ = self.calibration[key]
            target = origin + sign * math.radians(value)
            motion.rotationValue = target
            if abs(target - motion.rotationValue) > math.radians(0.08):
                raise RuntimeError(f"Pose refusée sur {key} : {pose}.")

    def weights(self, pivot):
        codes = ["05_Segment_2", "06_Segment_3", "07_Main", "09_Capot", "P3"]
        if pivot == "04_Segment_1":
            codes += ["04_Segment_1", "08_Capot", "M3", "P2", "A3"]
        output = []
        for code in codes:
            occ = self.occ[code]
            native = next(b for b in occ.component.bRepBodies if b.name != "Repère de liaison")
            if code.startswith("M"):
                mass = 13.4
            elif code.startswith("P"):
                mass = 0.75
            elif code.startswith("A"):
                mass = 2
            else:
                mass = native.volume * 1.27
            output.append((occ, mass, native.physicalProperties.centerOfMass))
        # Allow 6 g of wires, washers and screws at the wrist.
        output.append((self.occ["06_Segment_3"], 6, point((LONGUEURS[2], 0, 0))))
        return output

    def gravity(self, key, weights):
        pivot_pose = self.occ[key].transform2
        joint_axis = vector((0, 1, 0))
        joint_axis.transformBy(pivot_pose)
        origin = point((0, 0, 0))
        origin.transformBy(pivot_pose)
        moment = 0
        for occ, mass, center in weights:
            center = center.copy()
            center.transformBy(occ.transform2)
            arm = origin.vectorTo(center)
            force = vector((0, 0, -9.81 * mass / 1000))
            moment += arm.crossProduct(force).dotProduct(joint_axis) / 100
        return abs(moment)

    def interference(self):
        bodies = core.ObjectCollection.create()
        for occ in self.occ.values():
            for b in occ.bRepBodies:
                if b.name != "Repère de liaison":
                    bodies.add(b)
        query = self.design.createInterferenceInput(bodies)
        query.areCoincidentFacesIncluded = False
        results = self.design.analyzeInterference(query)
        if results is None:
            raise RuntimeError("Analyse d’interférences indisponible.")
        return [
            {"a": r.entityOne.name, "b": r.entityTwo.name,
             "volume_mm3": round(r.interferenceBody.volume * 1000, 5)}
            for r in results if r.interferenceBody.volume * 1000 > 0.006
        ]


def describe_movement(rig, full=False):
    rig.calibrate()
    vertices = list(product(*((lo, 0, hi) for lo, hi in LIMITES))) if full else [
        (0, 0, 0), (30, 12, 18), (30, -12, -13), (-30, -12, 18), (-30, 12, -13),
    ]
    motion_poses = []
    for (_, start), (_, end) in zip(POSES, POSES[1:]):
        for i in range(13 if full else 3):
            t = i / (12 if full else 2)
            motion_poses.append(tuple(round(a + (b - a) * t, 3) for a, b in zip(start, end)))
    samples = list(dict.fromkeys([*vertices, *motion_poses]))
    collisions = []
    points = {"J2": "04_Segment_1", "J3": "05_Segment_2"}
    weights = {j: rig.weights(key) for j, key in points.items()}
    peak = {j: (0, (0, 0, 0)) for j in points}
    for pose in samples:
        rig.move(pose)
        issues = rig.interference()
        if issues:
            collisions.append({"pose_deg": pose, "paires": issues})
        for joint, key in points.items():
            peak[joint] = max(peak[joint], (rig.gravity(key, weights[joint]), pose))
    rig.move((0, 0, 0))
    return {
        "pivots": [
            {"joint": label, "axe_local": axis.upper(),
             "limites_deg": bounds, "angle_test_deg": 5,
             "deplacement_temoin_mm": rig.calibration[key][2],
             "derive_autres_axes_deg": rig.calibration[key][3]}
            for label, (key, (_, axis, bounds)) in zip(("J1", "J2", "J3"), rig.joints.items())
        ],
        "poses_analysees": len(samples),
        "seuil_interference_mm3": 0.006,
        "interferences": collisions,
        "couple_statique": {
            "hypothese": "PETG plein 1,27 g/cm³, 13,4 g par servo, à vide, 6 g de câbles et de vis au poignet",
            "axes": {j: {"max_Nm": round(t, 4), "pose_deg": pose,
                         "masse_mobile_g": round(sum(mass for _, mass, _ in weights[j]), 1)}
                     for j, (t, pose) in peak.items()},
        },
    }


def set_camera(app, detail=False, alternate=False):
    view = app.activeViewport
    cam = view.camera
    cam.cameraType = core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.upVector = vector((0, 0, 1))
    if detail:
        cam.target, cam.eye = point((12, -12, 45)), point((115, -230, 158))
        cam.setExtents(186 / 10, 133 / 10)
    elif alternate:
        cam.target, cam.eye = point((44, -3, 61)), point((143, 385, 220))
        cam.setExtents(290 / 10, 171 / 10)
    else:
        cam.target, cam.eye = point((53, -1, 60)), point((141, -390, 225))
        cam.setExtents(290 / 10, 175 / 10)
    view.camera = cam
    view.refresh()
    return view


def capture(view, path, width, height, transparent=False):
    options = core.SaveImageFileOptions.create(str(path))
    options.width = width
    options.height = height
    options.isBackgroundTransparent = transparent
    if not view.saveAsImageFileWithOptions(options):
        raise RuntimeError(f"Capture refusée : {path.name}.")


def meshes(app, rig):
    output = OUT / "STL"
    output.mkdir(exist_ok=True)
    temp_doc = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    design = get_design(temp_doc)
    design.designType = fusion.DesignTypes.DirectDesignType
    root = design.rootComponent
    results = []
    for code, (occ, name, roll) in rig.prints.items():
        native = next(b for b in occ.component.bRepBodies if b.name == name)
        body = rig.forms.manager.copy(native)
        rig.forms.place(body, frame(roll=roll))
        bbox = body.boundingBox
        lo, hi = bbox.minPoint, bbox.maxPoint
        rig.forms.place(body, frame((-(lo.x+hi.x)*5, -(lo.y+hi.y)*5, -10*lo.z)))
        output_body = root.bRepBodies.add(body)
        filename = output / (code + ".stl")
        options = design.exportManager.createSTLExportOptions(output_body, str(filename))
        options.isBinaryFormat = True
        options.meshRefinement = fusion.MeshRefinementSettings.MeshRefinementHigh
        if not design.exportManager.execute(options) or filename.stat().st_size <= 84:
            raise RuntimeError(f"Export STL refusé : {code}.")
        results.append({"reference": code, "nom": occ.component.name, "quantite": 1,
                        "stl": filename.name, "orientation_roulis_deg": roll,
                        "dimensions_mm": [round(10 * d, 4) for d in
                                          (hi.x-lo.x, hi.y-lo.y, hi.z-lo.z)],
                        "volume_cm3": round(native.volume, 4),
                        "sha256": sha256(filename.read_bytes()).hexdigest()})
    temp_doc.close(False)
    return results


def archive(appl, doc, rig):
    with tempfile.TemporaryDirectory(prefix="Aura007_") as path:
        local = Path(path) / ARCHIVE.name
        manager = rig.design.exportManager
        if not manager.execute(manager.createFusionArchiveExportOptions(str(local))):
            raise RuntimeError("Export F3D refusé.")
        importer = appl.importManager
        imported = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(local)))
        root = get_design(imported).rootComponent
        count = root.allOccurrences.count
        revolute = sum(j.jointMotion.jointType == fusion.JointTypes.RevoluteJointType
                       for j in root.asBuiltJoints)
        if count != rig.root.allOccurrences.count or revolute != 3:
            raise RuntimeError(f"F3D réouvert incomplet : {count} composants et {revolute} pivots.")
        imported.close(False)
        ARCHIVE.write_bytes(local.read_bytes())
    doc.activate()
    return {"nom": ARCHIVE.name, "occurrences_reouvertes": count, "pivots_reouverts": revolute,
            "sha256": sha256(ARCHIVE.read_bytes()).hexdigest()}


def run(_context: str):
    app = core.Application.get()
    source = next((d for d in app.documents if d.isSaved and "Intégration mécatronique" in d.name),
                  app.activeDocument)
    previous = [d for d in app.documents if not d.isSaved and d.name.startswith(TITLE + " (travail)")]
    design_doc = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    design_doc.name = TITLE + " (travail)"
    rig = Assembly(design_doc)
    rig.build()
    report = describe_movement(rig, full=True)
    report["reference"] = source.name
    report["version_fusion"] = app.version
    report["occurrences"] = rig.root.allOccurrences.count
    report["pieces"] = len(rig.prints)
    write(report)
    view = set_camera(app)
    view.saveAsImageFile(str(OUT / "Controle_vue_Fusion.png"), 1320, 800)
    if not report["interferences"]:
        report["archive"] = archive(app, design_doc, rig)
        write(report)
        report["nomenclature"] = meshes(app, rig)
        design_doc.activate()
        view = set_camera(app)
        capture(view, OUT / "AURA-01_V3_de_table.png", 1720, 1040, transparent=True)
        alt = set_camera(app, alternate=True)
        capture(alt, OUT / "AURA-01_V3_de_table_cote_pivots.png", 1720, 1040, transparent=True)
        set_camera(app)
        for draft in previous:
            draft.close(False)
        write(report)
    print(json.dumps({**report, "interferences": report["interferences"][:3]}, ensure_ascii=False))
