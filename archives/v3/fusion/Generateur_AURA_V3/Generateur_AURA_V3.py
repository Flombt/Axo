"""Génère, vérifie et filme dans Fusion la maquette locale AURA-01 V3."""

import importlib.util
import json
import math
from pathlib import Path
import tempfile
import traceback

import adsk
import adsk.core as core
import adsk.fusion as fusion


SOURCE = Path(__file__).resolve().parent
OUTPUT = SOURCE.parent
STATUS = OUTPUT / "Verification_CAO.json"
TITLE = "AURA-01 V3 — Main articulée"
ARCHIVE = OUTPUT / "AURA-01_V3_Main-articulee.f3d"


def load_geometry():
    spec = importlib.util.spec_from_file_location("aura_v3_geometrie", SOURCE / "geometrie.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_status(data):
    scratch = STATUS.with_suffix(".tmp")
    scratch.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    scratch.replace(STATUS)


def assemble(design, geom, status):
    root = design.rootComponent
    g = geom.Solids(design)
    components = {}
    joints = {}
    checks = {}
    home = {}

    def add(key, label, placement, builder, *args):
        occ = root.occurrences.addNewComponent(placement)
        if not occ:
            raise RuntimeError(f"Occurrence refusée : {key}")
        comp = occ.component
        comp.name = label
        source_bodies = []
        builder(source_bodies, *args)
        feature = comp.features.baseFeatures.add()
        feature.name = "Volumes cotés — " + key
        feature.startEdit()
        names = []
        for i, (name, finish, temporary) in enumerate(source_bodies, 1):
            n = f"{i:02d} {name}"
            body = comp.bRepBodies.add(temporary, feature)
            if not body or not body.isSolid:
                raise RuntimeError(f"Corps non fermé : {key} / {name}")
            body.appearance = g.appearances[finish]
            body.name = n
            names.append(n)
        feature.finishEdit()
        bodies = {b.name:b for b in comp.bRepBodies}
        if any(n not in bodies for n in names):
            raise RuntimeError(f"Corps de résultat indisponible : {key}")
        components[key] = occ
        home[key] = placement.copy()
        return bodies[names[0]]

    def connect(parent, child, pivot_body, label, bounds, axis):
        occ = components[child]
        pivot = pivot_body.createForAssemblyContext(occ)
        curve = next((edge for edge in pivot.edges if core.Circle3D.cast(edge.geometry)), None)
        if not curve:
            raise RuntimeError(f"Cercle de pivot introuvable : {child}")
        geometry = fusion.JointGeometry.createByCurve(curve, fusion.JointKeyPointTypes.CenterKeyPoint)
        if not geometry:
            raise RuntimeError(f"Origine de pivot introuvable : {child}")
        native = root.asBuiltJoints
        inp = native.createInput(occ, components[parent], geometry)
        if not inp or not inp.setAsRevoluteJointMotion(fusion.JointDirections.ZAxisJointDirection):
            raise RuntimeError(f"Définition du pivot refusée : {child}")
        joint = native.add(inp)
        if not joint:
            raise RuntimeError(f"Pivot refusé : {child}")
        joint.name = f"{child} · {label}"
        motion = fusion.RevoluteJointMotion.cast(joint.jointMotion)
        if not motion:
            raise RuntimeError(f"Liaison non rotative : {child}")
        joints[child] = (motion, joint, bounds, axis)

    add("BASE", "00 · Platine et socle fixe", geom.frame(), g.fixed)
    base = components["BASE"]
    base.isGrounded = True
    yaw = geom.frame((0, 0, 31))
    p = add("J1", "01 · Tourelle de lacet", yaw, g.turret)
    connect("BASE", "J1", p, "lacet du socle", (-100, 100), "z")
    parent = "J1"
    parent_frame = yaw
    origin = (0, 0, 72)
    labels = ("Segment proximal", "Segment intermédiaire", "Segment distal")
    for index, ((length, width, height, pitch), label) in enumerate(zip(geom.SEGMENTS, labels), 2):
        stage_frame = geom.compose(parent_frame, geom.frame(origin, pitch=pitch))
        key = f"J{index}"
        p = add(key, f"{index:02d} · {label}", stage_frame, g.arm, index - 1, length, width, height)
        connect(parent, key, p, label.lower(), (-30, 33), "y")
        origin = (length, 0, 0)
        parent, parent_frame = key, stage_frame

    yaw_frame = geom.compose(parent_frame, geom.frame(origin, pitch=9))
    p = add("J5", "05 · Poignet, déviation", yaw_frame, g.yaw_wrist)
    connect("J4", "J5", p, "déviation du poignet", (-32, 32), "z")
    pitch_frame = geom.compose(yaw_frame, geom.frame((43, 0, 0), pitch=5))
    p = add("J6", "06 · Poignet, flexion", pitch_frame, g.pitch_wrist)
    connect("J5", "J6", p, "flexion du poignet", (-32, 34), "y")
    palm_frame = geom.compose(pitch_frame, geom.frame((40, 0, 0)))
    p = add("J7", "07 · Poignet, roulis et paume blanche", palm_frame, g.palm)
    connect("J6", "J7", p, "roulis de la main", (-72, 72), "x")
    status.update(etape="Construction des quinze phalanges", liaisons=len(joints))
    save_status(status)

    flex_maxima = (62, 72, 66)
    for short, digit, offset, yaw_deg, roll_deg, sizes in geom.DIGITS:
        placement = geom.compose(palm_frame, geom.frame(offset, yaw=yaw_deg, roll=roll_deg))
        parent = "J7"
        for n, length in enumerate(sizes, 1):
            if n > 1:
                placement = geom.compose(placement, geom.frame((sizes[n - 2], 0, 0)))
            key = f"{short}{n}"
            p = add(key, f"{digit} · Phalange {n} · KST X06", placement, g.phalanx, length, n == 3)
            connect(parent, key, p, f"{digit.lower()}, phalange {n}", (0, flex_maxima[n - 1]), "y")
            parent = key

    root.attributes.add("AURA-01", "Modele", TITLE)
    if len(joints) != 22 or sum(o.component.bRepBodies.count == 0 for o in components.values()):
        raise RuntimeError("Assemblage incomplet")
    expected_axes = {"x":core.Vector3D.create(1,0,0), "y":core.Vector3D.create(0,1,0),
                     "z":core.Vector3D.create(0,0,1)}
    direction = {}
    home_values = {}
    status.update(etape="Contrôle des pivots natifs dans Fusion", liaisons=len(joints))
    save_status(status)

    for key, (motion, joint, bounds, axis) in joints.items():
        initial = motion.rotationValue
        home_values[key] = initial
        before = components[key].transform2
        other_before = {k:j[0].rotationValue for k,j in joints.items() if k != key}
        motion.rotationValue = initial + math.radians(8)
        if not math.isclose(motion.rotationValue - initial, math.radians(8), abs_tol=0.001):
            raise RuntimeError(f"Lecture angulaire à 8° refusée : {key}")
        after = components[key].transform2
        axis_vector = expected_axes[axis].copy()
        axis_vector.transformBy(before)
        probe = geom.point((0, 15, 0) if axis == "x" else (20, 0, 0))
        start = probe.copy()
        end = probe.copy()
        start.transformBy(before)
        end.transformBy(after)
        fixed = geom.point((0, 0, 0))
        fixed_before = fixed.copy()
        fixed.transformBy(after)
        fixed_before.transformBy(before)
        if fixed.distanceTo(fixed_before) > 0.015:
            raise RuntimeError(f"Le centre du pivot s’est déplacé : {key}")
        tangential = axis_vector.crossProduct(fixed_before.vectorTo(start))
        sign = 1 if tangential.dotProduct(start.vectorTo(end)) >= 0 else -1
        delta = start.distanceTo(end) * 10
        if delta < 1.6 or delta > 3.2:
            raise RuntimeError(f"Déplacement du point témoin incohérent : {key}, {delta} mm")
        drift = max(abs(joints[k][0].rotationValue - value) for k,value in other_before.items())
        if drift > math.radians(0.15):
            raise RuntimeError(f"Entraînement d’une autre articulation : {key}, {math.degrees(drift):.3f}°")
        motion.rotationValue = initial
        direction[key] = sign
        limits = motion.rotationLimits
        lo, hi = sorted((initial + math.radians(sign * bounds[0]), initial + math.radians(sign * bounds[1])))
        limits.minimumValue = lo
        limits.maximumValue = hi
        limits.isMinimumValueEnabled = True
        limits.isMaximumValueEnabled = True
        joint.isLightBulbOn = False
        checks[key] = {"axe_local": axis.upper(), "commande_deg": 8.0,
                       "deplacement_temoin_mm": round(delta, 3),
                       "derive_max_autre_joint_deg": round(math.degrees(drift), 5),
                       "bornes_mecaniques_deg": list(bounds),
                       "signe_natif": sign}

    def drive(values):
        for key, (motion, joint, _, _) in joints.items():
            val = home_values[key] + math.radians(direction[key] * values.get(key, 0))
            if abs(motion.rotationValue - val) > 1e-5:
                motion.rotationValue = val

    drive({})
    status["pivots"] = checks
    status["composants"] = len(components)
    status["corps"] = sum(o.component.bRepBodies.count for o in components.values())
    status["moteurs_main_visibles"] = 15
    status["apercu_motion"] = "Chaque pivot natif testé séparément à 8°. Mesure au point témoin."
    ids_des_doigts = [f"{prefix}{n}" for prefix, *_ in geom.DIGITS for n in (1, 2, 3)]
    volumes = {}
    for key in ids_des_doigts:
        elements = list(components[key].bRepBodies)
        housing = next(b for b in elements if "Châssis blanc" in b.name)
        motor = next(b for b in elements if "corps et pattes" in b.name)
        targets = core.ObjectCollection.create()
        targets.add(housing)
        targets.add(motor)
        options = design.createInterferenceInput(targets)
        intersections = design.analyzeInterference(options)
        if intersections is None or intersections.count != 0:
            raise RuntimeError(f"Interférence boîtier/logement : {key}")
        volumes[key] = round(sum(body.volume for body in elements
                                 if "Pivot passif" not in body.name and body != motor), 3)
    status["logements_testes_sans_interference"] = len(volumes)
    status["volumes_phalanges_hors_servo_et_axe_cm3"] = volumes
    return drive, components, home


def camera(viewport, geom, target, eye, size):
    cam = viewport.camera
    cam.cameraType = core.CameraTypes.OrthographicCameraType
    cam.isSmoothTransition = False
    cam.target = geom.point(target)
    cam.eye = geom.point(eye)
    cam.upVector = geom.vector((0, 0, 1))
    cam.viewExtents = size / 10
    viewport.camera = cam
    viewport.refresh()


def capture(viewport, file, width=1000, height=650):
    viewport.refresh()
    if not viewport.saveAsImageFile(str(file), width, height) or file.stat().st_size < 2000:
        raise RuntimeError(f"Fusion n’a pas exporté le rendu : {file.name}")


def animate(viewport, geom, drive, palm, status):
    frames = Path(tempfile.mkdtemp(prefix="AURA_V3_Fusion_"))
    status.update(etape="Capture de la vidéo dans Fusion", dossier_images=str(frames),
                  frequence_images=16, images_produites=0)
    save_status(status)
    target = geom.point((105, -4, 0))
    target.transformBy(palm)
    focus = (target.x * 10, target.y * 10, target.z * 10)

    def near(delta, extent):
        eye = tuple(value + offset for value,offset in zip(focus, delta))
        camera(viewport, geom, focus, eye, extent)

    def s_curve(t):
        return (1 - math.cos(math.tau * t)) / 2

    def shot(count, poses):
        for i in range(count):
            drive(poses(i / (count - 1)))
            k = status["images_produites"]
            capture(viewport, frames / f"image_{k:04d}.png")
            status["images_produites"] += 1
            if i % 12 == 0:
                save_status(status)
                adsk.doEvents()

    near((215, -405, 300), 350)
    shot(48, lambda t:{
        "J5": 10 * s_curve(t),
        "J6": -11 * s_curve(t),
        "J7": 55 * math.sin(math.tau * t),
    })
    near((174, -265, 295), 290)

    def fingers(t):
        values = {}
        for digit_index, (key, *_) in enumerate(geom.DIGITS):
            start = digit_index * 0.055
            a = max(0.0, min(1.0, (t - start) / 0.78))
            degrees = (23, 32, 29) if key == "P" else (28, 42, 35)
            for n, flex in enumerate(degrees, 1):
                values[f"{key}{n}"] = flex * s_curve(a)
        return values

    shot(64, fingers)
    camera(viewport, geom, (216, 0, 137), (470, -795, 482), 716)

    def arm_pose(t):
        w = math.sin(math.tau*t)
        a = s_curve(t)
        return {"J1": 20 * w, "J2": -13 * a, "J3": 21 * a, "J4": -22 * a,
                "J5": -15 * w, "J6": 10 * w, "J7": -16 * a}

    shot(56, arm_pose)
    drive({})
    camera(viewport, geom, (216, 0, 137), (470, -795, 482), 716)
    status.update(etape="Capture terminée", animation="Rendu du viewport natif d’Autodesk Fusion")
    save_status(status)


def run(_context):
    app = core.Application.get()
    status = {"etape": "Initialisation", "application": app.version}
    save_status(status)
    doc = None
    try:
        geom = load_geometry()
        doc = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
        design = fusion.Design.cast(doc.products.itemByProductType("DesignProductType"))
        if not design:
            raise RuntimeError("Nouveau document Fusion absent")
        design.designType = fusion.DesignTypes.ParametricDesignType
        drive, components, home = assemble(design, geom, status)
        viewport = app.activeViewport
        camera(viewport, geom, (216, 0, 137), (470, -795, 482), 716)
        adsk.doEvents()
        status.update(etape="Export de l’assemblage Fusion")
        save_status(status)
        export = design.exportManager
        archive = ARCHIVE
        revision = 1
        while archive.exists():
            revision += 1
            archive = ARCHIVE.with_stem(f"{ARCHIVE.stem}_r{revision:02d}")
        archive_opts = export.createFusionArchiveExportOptions(str(archive))
        if not export.execute(archive_opts) or archive.stat().st_size < 10000:
            raise RuntimeError("Export F3D incomplet")
        status["archive"] = str(archive)
        preview = OUTPUT / "AURA_V3_Apercu.png"
        capture(viewport, preview, 1600, 1050)
        status["apercu"] = str(preview)
        animate(viewport, geom, drive, home["J7"], status)
    except Exception:
        status["erreur"] = traceback.format_exc()
        save_status(status)
        adsk.log(status["erreur"])
        if doc and "archive" not in status:
            doc.close(False)
