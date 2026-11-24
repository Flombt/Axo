"""Monte les pièces FDM, mesure les collisions et exporte les solides imprimables."""

from hashlib import sha256
import math
from pathlib import Path
import tempfile

import adsk
import adsk.core as core
import adsk.fusion as fusion


OUT = Path(__file__).resolve().parents[1]
ARCHIVE = OUT / "AURA-01_V3_FDM_r03.f3d"
SHAFTS = tuple(core.Vector3D.create(*t) for t in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
LIMITS = {
    "J1": (-70, 70), "J2": (-31, 14), "J3": (-22, 25), "J4": (-32, 31),
    "J5": (-36, 36), "J6": (-29, 29), "J7": (-55, 55),
}
FLEX = (56, 63, 55)


class Rig:
    def __init__(self, design, base, geometry):
        self.design, self.base, self.geometry = design, base, geometry
        self.root = design.rootComponent
        self.solids = base.Solids(design)
        self.forms = geometry.Printable(base, self.solids)
        self.parts = {}
        self.occurrences = {}
        self.joints = {}
        self.zeros = {}
        self.signs = {}
        self.bounds = {}
        self.axis = {}
        self.inspections = []

    def part(self, key, ref, placement, builder, axis=None, *args):
        if ref in self.parts:
            existing, _, _, _ = self.parts[ref]
            occ = self.root.occurrences.addExistingComponent(existing, placement)
        else:
            occ = self.root.occurrences.addNewComponent(placement)
            comp = occ.component
            comp.name = self.geometry.PARTS[ref][1]
            shape, motor = builder(*args)
            if not shape.isSolid or shape.lumps.count != 1:
                raise RuntimeError(f"La pièce {ref} doit être un seul solide connecté ({shape.lumps.count}).")
            g = self.solids
            feature = comp.features.baseFeatures.add()
            feature.name = "Solide FDM et références"
            feature.startEdit()
            native = comp.bRepBodies.add(shape, feature)
            native.name = "FDM · " + self.geometry.PARTS[ref][0]
            native.appearance = g.appearances[self.geometry.PARTS[ref][3]]
            if motor:
                body = comp.bRepBodies.add(motor, feature)
                body.name = "Enveloppe servo · référence"
                body.appearance = g.appearances["metal"]
            if axis:
                marker = comp.bRepBodies.add(g.pivot(axis, 0.33, 1.2), feature)
                marker.name = "Repère cinématique · hors impression"
            feature.finishEdit()
            printed = next(b for b in comp.bRepBodies if b.name.startswith("FDM"))
            self.parts[ref] = (comp, printed, shape.volume, placement.copy())
        self.occurrences[key] = occ
        self.inspections.extend(
            body for body in occ.bRepBodies if body.name.startswith(("FDM", "Enveloppe servo"))
        )
        return occ

    def hinge(self, parent, key, axis, bounds):
        occ = self.occurrences[key]
        body = next(b for b in occ.bRepBodies if b.name.startswith("Repère cinématique"))
        edge = next(e for e in body.edges if core.Circle3D.cast(e.geometry))
        point = fusion.JointGeometry.createByCurve(edge, fusion.JointKeyPointTypes.CenterKeyPoint)
        collection = self.root.asBuiltJoints
        input = collection.createInput(occ, self.occurrences[parent], point)
        if not input.setAsRevoluteJointMotion(fusion.JointDirections.ZAxisJointDirection):
            raise RuntimeError(f"Création de pivot refusée {key}.")
        joint = collection.add(input)
        joint.name = key
        joint.isLightBulbOn = False
        body.isLightBulbOn = False
        self.joints[key] = fusion.RevoluteJointMotion.cast(joint.jointMotion)
        self.bounds[key] = bounds
        self.axis[key] = axis

    def build(self):
        frame, compose = self.base.frame, self.base.compose
        self.part("BASE", "BASE", frame(), self.forms.fixed).isGrounded = True
        turret = frame((0, 0, 27.2))
        self.part("J1", "J1", turret, self.forms.turret, "z")
        self.hinge("BASE", "J1", "z", LIMITS["J1"])
        parent, parent_frame, offset = "J1", turret, (0, 0, 69)
        for i, (length, _, _, pitch) in enumerate(self.geometry.ARM, 1):
            key = f"J{i + 1}"
            placement = compose(parent_frame, frame(offset, pitch=pitch))
            self.part(key, key, placement, self.forms.arm, "y", i)
            self.hinge(parent, key, "y", LIMITS[key])
            parent, parent_frame, offset = key, placement, (length, 0, 0)
        yaw = compose(parent_frame, frame(offset))
        self.part("J5", "J5", yaw, self.forms.yaw, "z")
        self.hinge("J4", "J5", "z", LIMITS["J5"])
        pitch = compose(yaw, frame((45, 0, 8.5), pitch=12))
        self.part("J6", "J6", pitch, self.forms.pitch, "y")
        self.hinge("J5", "J6", "y", LIMITS["J6"])
        palm = compose(pitch, frame((40.3, 0, 0)))
        self.part("J7", "J7", palm, self.forms.palm, "x")
        self.hinge("J6", "J7", "x", LIMITS["J7"])
        for short, label, position, yaw in self.geometry.FINGERS:
            placement = compose(palm, frame(position, yaw=yaw))
            previous = "J7"
            for n, length in enumerate(self.geometry.FINGER_LENGTHS, 1):
                key = f"{short}{n}"
                self.part(key, f"F{n}", placement, self.forms.finger, "y", n)
                self.hinge(previous, key, "y", (0, FLEX[n - 1]))
                placement = compose(placement, frame((length, 0, 0)))
                previous = key
        self.root.attributes.add("AURA-01", "Modele", "V3 FDM r03")
        if (len(self.parts), len(self.occurrences), len(self.joints)) != (11, 23, 22):
            raise RuntimeError("La nomenclature cinématique n'est pas complète.")

    def calibrate(self):
        results = {}
        for key, motion in self.joints.items():
            origin = motion.rotationValue
            self.zeros[key] = origin
            other = {k:m.rotationValue for k,m in self.joints.items() if k != key}
            before = self.occurrences[key].transform2
            angle = math.radians(8)
            motion.rotationValue = origin + angle
            if abs(origin + angle - motion.rotationValue) > math.radians(.04):
                raise RuntimeError(f"Impossible d'entraîner {key} de 8°.")
            after = self.occurrences[key].transform2
            axis = self.axis[key]
            v = SHAFTS["xyz".index(axis)].copy()
            v.transformBy(before)
            reference = (0, 18, 0) if axis == "x" else (18, 0, 0)
            witness = self.base.point(reference)
            moved = witness.copy()
            pivot = self.base.point((0, 0, 0))
            witness.transformBy(before)
            moved.transformBy(after)
            pivot.transformBy(before)
            handed = v.crossProduct(pivot.vectorTo(witness)).dotProduct(witness.vectorTo(moved))
            travel = witness.distanceTo(moved) * 10
            if not 2.3 < travel < 2.8:
                raise RuntimeError(f"Repère de mouvement incorrect sur {key} ({travel} mm).")
            sign = 1 if handed > 0 else -1
            self.signs[key] = sign
            drift = max(abs(math.degrees(self.joints[k].rotationValue - at)) for k,at in other.items())
            if drift > .12:
                raise RuntimeError(f"{key} entraîne une autre articulation de {drift}°.")
            motion.rotationValue = origin
            bounds = self.bounds[key]
            lo, hi = sorted(origin + math.radians(sign * v) for v in bounds)
            lim = motion.rotationLimits
            lim.minimumValue, lim.maximumValue = lo, hi
            lim.isMinimumValueEnabled = lim.isMaximumValueEnabled = True
            results[key] = {"axe": axis.upper(), "bornes_deg": bounds, "temoin_8deg_mm": round(travel, 4),
                            "variation_max_autre_axe_deg": round(drift, 6)}
        return results

    def drive(self, pose):
        expectations = {}
        for key, motion in self.joints.items():
            angle = pose.get(key, 0)
            lo, hi = self.bounds[key]
            if not lo - .0001 <= angle <= hi + .0001:
                raise ValueError(f"Pose hors limites {key}: {angle}.")
            target = self.zeros[key] + math.radians(angle * self.signs[key])
            expectations[key] = target
            if abs(target - motion.rotationValue) > 1e-6:
                motion.rotationValue = target
        if any(abs(expectations[k] - m.rotationValue) > math.radians(.13) for k,m in self.joints.items()):
            raise RuntimeError(f"Le solveur Fusion a refusé la pose {pose}.")


def candidate_poses(rig):
    yield "HOME", {}
    for key, (lo, hi) in rig.bounds.items():
        for edge in (lo, hi):
            if edge:
                for fraction in (.35, .68, 1):
                    yield f"{key} seul {fraction:.0%} de {edge}°", {key: fraction * edge}
    for short, label, _, _ in rig.geometry.FINGERS:
        for step in range(1, 6):
            yield f"Fermeture {label} {20 * step} %", {
                f"{short}{i}": angle * step / 5 for i,angle in enumerate(FLEX, 1)
            }
    for step in range(1, 9):
        yield f"Flexion synchronisée {step}/8", {
            f"{short}{i}": deg * step / 8 for short, *_ in rig.geometry.FINGERS
            for i, deg in enumerate(FLEX, 1)
        }
    keyframes = (
        ("Salut", {"J1": 45, "J2": -19, "J3": 22, "J4": -14, "J5": -22, "J6": 16, "J7": 48}),
        ("Retour à gauche", {"J1": -55, "J2": -11, "J3": 14, "J4": -11, "J5": 28, "J6": -12, "J7": -55}),
        ("Bras tendu", {"J1": 10, "J2": 7, "J3": -7, "J4": -19, "J5": -19, "J6": 3, "J7": 8}),
        ("Main retournée", {"J1": 13, "J2": -5, "J3": 8, "J4": 2, "J5": -22, "J6": -17, "J7": 55}),
    )
    for label, pose in keyframes:
        for step in range(1,12):
            t = step / 11
            instance = {k: v*t for k,v in pose.items()}
            if label in ("Salut", "Main retournée"):
                instance.update({f"{short}{i}": 0.72 * t * amount for short,*_ in rig.geometry.FINGERS
                                 for i,amount in enumerate(FLEX,1)})
            yield f"{label} {step}/11", instance


def sample_interferences(rig, measure, name_body, report, write):
    report["analyse_r03"] = {
        "corps_controles": len(rig.inspections), "poses": 0, "poses_en_interference": 0,
        "interferences": [], "poses_sans_interference": [],
    }
    summary = report["analyse_r03"]
    for label, pose in candidate_poses(rig):
        rig.drive(pose)
        overlaps = measure(rig.design, rig.inspections)
        summary["poses"] += 1
        if overlaps:
            summary["poses_en_interference"] += 1
            if len(summary["interferences"]) < 32:
                summary["interferences"].append({
                    "pose": label, "angles_deg": pose,
                    "contacts": [{"a": name_body(a), "b": name_body(b), "volume_mm3": round(v, 4)}
                                 for a,b,v in overlaps],
                })
        else:
            summary["poses_sans_interference"].append({"nom": label, "angles_deg": pose})
        if summary["poses"] % 16 == 1:
            write(report)
            adsk.doEvents()
    rig.drive({})
    write(report)


def write_print_meshes(app, rig, get_design):
    path = OUT / "STL_orientes"
    path.mkdir(exist_ok=True)
    context = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    try:
        design = get_design(context)
        design.designType = fusion.DesignTypes.DirectDesignType
        root = design.rootComponent
        g = rig.solids
        result = []
        for key, (_, native, volume, _) in rig.parts.items():
            name, label, quantity, _, face = rig.geometry.PARTS[key]
            temporary = g.manager.copy(native)
            if face in ("dos", "flanc"):
                transform = rig.base.frame(roll=180 if face == "dos" else -90)
                if not g.manager.transform(temporary, transform):
                    raise RuntimeError(f"Orientation refusée {name}.")
            box = temporary.boundingBox
            center = box.minPoint
            top = box.maxPoint
            offset = tuple(-factor for factor in ((center.x+top.x)*5, (center.y+top.y)*5, center.z*10))
            if not g.manager.transform(temporary, rig.base.frame(offset)):
                raise RuntimeError(f"Placement refusé {name}.")
            printed = root.bRepBodies.add(temporary)
            printed.name = name
            dest = path / (name + ".stl")
            export = design.exportManager
            opts = export.createSTLExportOptions(printed, str(dest))
            opts.isBinaryFormat = True
            opts.meshRefinement = fusion.MeshRefinementSettings.MeshRefinementHigh
            if not export.execute(opts) or dest.stat().st_size < 100:
                raise RuntimeError(f"Export STL refusé {name}.")
            result.append({"reference": name, "nom": label, "quantite": quantity, "face": face,
                           "volume_cm3": round(volume, 3),
                           "dimensions_mm": [round((top.x-center.x)*10, 3), round((top.y-center.y)*10, 3),
                                             round((top.z-center.z)*10, 3)],
                           "stl": dest.name, "sha256": sha256(dest.read_bytes()).hexdigest()})
        return result
    finally:
        context.close(False)


def make(app, base, geometry, report, write, get_design, open_f3d, measure, name_body):
    document = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    design = get_design(document)
    design.designType = fusion.DesignTypes.ParametricDesignType
    report["etape"] = "Construction r03"
    write(report)
    rig = Rig(design, base, geometry)
    rig.build()
    report["pivots"] = rig.calibrate()
    report["etape"] = "Contrôle des interférences r03"
    write(report)
    sample_interferences(rig, measure, name_body, report, write)
    if report["analyse_r03"]["poses_en_interference"]:
        report["etape"] = "Interférences r03 à corriger"
        write(report)
        return
    document.activate()
    viewport = app.activeViewport
    cam = viewport.camera
    cam.cameraType = core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.target = base.point((215, -8, 141))
    cam.eye = base.point((445, -715, 464))
    cam.upVector = base.vector((0, 0, 1))
    cam.viewExtents = 694 / 10
    viewport.camera = cam
    viewport.refresh()
    preview = OUT / "AURA_V3_FDM_Apercu.png"
    viewport.saveAsImageFile(str(preview), 1600, 1010)
    report["etape"] = "Export et réouverture de la r03"
    write(report)
    with tempfile.TemporaryDirectory(prefix="AURA_FDM_Fusion_") as area:
        local = Path(area) / ARCHIVE.name
        export = design.exportManager
        if not export.execute(export.createFusionArchiveExportOptions(str(local))):
            raise RuntimeError("Fusion a refusé l'export F3D.")
        reloaded = open_f3d(app, local)
        try:
            root = get_design(reloaded).rootComponent
            if root.occurrences.count != 23 or root.asBuiltJoints.count != 22:
                raise RuntimeError("L'archive rouverte est incomplète.")
            roundtrip = {"occurrences": 23, "pivots": 22}
        finally:
            reloaded.close(False)
        scratch = ARCHIVE.with_suffix(".tmp")
        scratch.write_bytes(local.read_bytes())
        scratch.replace(ARCHIVE)
    report["reouverture_fusion_r03"] = roundtrip
    report["archive"] = ARCHIVE.name
    report["archive_sha256"] = sha256(ARCHIVE.read_bytes()).hexdigest()
    report["apercu"] = preview.name
    report["etape"] = "Export de onze solides imprimables"
    write(report)
    report["nomenclature"] = write_print_meshes(app, rig, get_design)
    report["nombre_pieces_imprimees"] = sum(row["quantite"] for row in report["nomenclature"])
    report["etape"] = "CAO et exports FDM contrôlés"
    write(report)
    document.activate()
