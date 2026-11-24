"""Banc autonome de l'épaule: courroie, cartouche double appui et frein passif."""

import math
from pathlib import Path

import adsk
import adsk.core as core
import adsk.fusion as fusion


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "02_Epaule"
REVISION = 4
PITCH = 5.0
R_SMALL, R_BIG = (n * PITCH / math.tau for n in (16, 64))
RATIO = 4
Z = 146.0
X_MOTOR = -58.0
ELBOW_LIMIT = 60
CART_FOOT = ((-81, 59), (-81, 95), (-35, 59), (-35, 95))
GUARD_FOOT = ((-85.25, 105.5), (53, 103.5))
SERVO_FOOT_Y = (37.5, 44.9)


def belt_geometry():
    d = R_BIG - R_SMALL
    a, b = 90.0, 150.0
    for _ in range(55):
        c = (a + b) / 2
        t = math.asin(d / c)
        length = 2 * math.sqrt(c * c - d * d) + math.pi * (R_BIG + R_SMALL) + 2 * t * d
        if length < 425:
            a = c
        else:
            b = c
    return c, t


CENTER, TANGENT_ANGLE = belt_geometry()
MOTOR_Z = Z - math.sqrt(CENTER**2 - X_MOTOR**2)
DRIVE = X_MOTOR, 0, MOTOR_Z
LOAD = 0, 0, Z


def clip(g, body, cutter):
    if not g.manager.booleanOperation(body, cutter, fusion.BooleanTypes.IntersectionBooleanType):
        raise RuntimeError("Intersection d'usinage du banc J2 impossible.")
    return body


def oriented(bench, pos, direction, length, width, height):
    u = bench.base.vector((direction[0], 0, direction[1]))
    bounds = core.OrientedBoundingBox3D.create(bench.base.point(pos), u, bench.base.vector((0, 1, 0)),
                                               length / 10, width / 10, height / 10)
    return bench.g.manager.createBox(bounds)


def belt(bench):
    u = (-X_MOTOR / CENTER, (Z - MOTOR_Z) / CENTER)
    v = (-u[1], u[0])
    shift = -math.sin(TANGENT_ANGLE)
    rings = []
    for x, z, rad, side in ((X_MOTOR, MOTOR_Z, R_SMALL, -1), (0, Z, R_BIG, 1)):
        body = bench.ring(x, z, 64, 79, rad + 2.85, rad - .65)
        lateral = shift * (rad + 1.1) + side * 54.75
        box = oriented(bench, (x + lateral * u[0], 71.5, z + lateral * u[1]), u, 111, 18, 140)
        rings.append(clip(bench.g, body, box))
    bands = []
    for side in (-1, 1):
        n = tuple(shift * q + side * math.cos(TANGENT_ANGLE) * r for q, r in zip(u, v))
        s = X_MOTOR + n[0] * (R_SMALL + 1.10), MOTOR_Z + n[1] * (R_SMALL + 1.10)
        l = n[0] * (R_BIG + 1.10), Z + n[1] * (R_BIG + 1.10)
        length = math.dist(s, l)
        direction = tuple((b - a) / length for a, b in zip(s, l))
        bands.append(oriented(bench, ((s[0] + l[0]) / 2, 71.5, (s[1] + l[1]) / 2),
                              direction, length + 1.5, 15, 3.48))
    return bench.g.union(rings[0], rings[1], *bands)


def shaft(g, low, high, key_ranges):
    s = g.cyl((0, low, 0), (0, high, 0), 6)
    for a, b in key_ranges:
        g.cut(s, g.box(-2.03, 2.03, a, b, 4.17, 7))
    return s


def keyway(g, body, low, high):
    return g.cut(body, g.box(-2.10, 2.10, low - .1, high + .1, 4.12, 8.27))


def pulley(bench, r):
    g = bench.g
    p = g.cyl((0, 63.7, 0), (0, 79.3, 0), r - .79)
    g.union(p, g.cyl((0, 61.5, 0), (0, 63.86, 0), r + 2.2),
            g.cyl((0, 79.14, 0), (0, 81.5, 0), r + 2.2))
    g.cut(p, g.cyl((0, 61, 0), (0, 82, 0), 6.04))
    return keyway(g, p, 61.5, 81.5)


def bearing(bench, index, x, z, y0, which):
    inner = bench.ring(0, 0, y0, y0 + 8, 8.2, 6.0)
    outer = bench.ring(0, 0, y0, y0 + 8, 14, 8.25)
    for tag, label, body, neighbor in (("int", "bague intérieure", inner, which),
                                      ("ext", "bague extérieure", outer,
                                       "J20_Socle" if x == 0 else "J22_Cartouche")):
        name = f"6001_{index}_{tag}"
        bench.part(name, f"SKF 6001-2RSH · {label} {index}", body, "metal", (x, 0, z), typed="SKF 6001-2RSH")
        bench.rigid(name, neighbor)


def fastener(bench, key, where, span, rad, head, parent, face="y"):
    g = bench.g
    vector = [(0, v, 0) if face == "y" else (0, 0, v) for v in span]
    body = g.cyl(vector[0], vector[1], rad)
    start = span[1] - .006
    end = span[1] + head * .68
    points = [(0, v, 0) if face == "y" else (0, 0, v) for v in (start, end)]
    g.union(body, g.cyl(points[0], points[1], head))
    bench.part(key, key.replace("_", " "), body, "metal", where)
    bench.rigid(key, parent)


def commercial_step(bench, filename, source_frame):
    app, g = bench.app, bench.g
    document = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    try:
        design = bench.get_design(document)
        design.designType = fusion.DesignTypes.DirectDesignType
        reader = app.importManager
        opt = reader.createSTEPImportOptions(str(ROOT / "Plans_constructeurs" / filename))
        if not reader.importToTarget(opt, design.rootComponent):
            raise RuntimeError(f"Import STEP constructeur impossible {filename}.")
        bodies = list(design.rootComponent.bRepBodies)
        for occurrence in design.rootComponent.allOccurrences:
            bodies.extend(occurrence.bRepBodies)
        shapes = [g.manager.copy(b) for b in bodies if b.isSolid]
        if len(shapes) != 1:
            raise RuntimeError(f"{len(shapes)} solides renvoyés dans {filename}.")
        solid = shapes[0]
        if not g.manager.transform(solid, source_frame):
            raise RuntimeError("Alignement du STEP constructeur impossible.")
        return solid
    finally:
        document.close(False)
        bench.doc.activate()


def support(bench):
    g = bench.g
    foot = g.rounded(-109, 76, -73, 119, 0, 12, 8)
    for y0, y1 in ((-45, -30), (29, 44)):
        tower = g.box(-27, 26, y0, y1, 9, Z)
        g.union(tower, g.cyl((0, y0, Z), (0, y1, Z), 26))
        g.union(foot, tower)
        g.cut(foot, g.cyl((0, y0 - .1, Z), (0, y1 + .1, Z), 10.72))
        a, b = (-45.15, -34.0) if y0 < 0 else (32.0, 44.15)
        g.cut(foot, g.cyl((0, a, Z), (0, b, Z), 14.04))
        for x in (-20, 20):
            g.cut(foot, g.cyl((x, y0 - .1, Z), (x, y1 + .1, Z), 3.51 if y0 < 0 else 2.68))
    rail = g.rounded(-86, -30, 20, 101, 10, 27, 4)
    g.union(foot, rail)
    for x in (-92, 60):
        for y in (-58, 106):
            g.cut(foot, g.cyl((x, y, -1), (x, y, 13), 3.35))
    for x, y in CART_FOOT:
        g.cut(foot, g.cyl((x, y, 12), (x, y, 27.25), 2.58))
    for y in SERVO_FOOT_Y:
        g.cut(foot, g.cyl((-70.5, y, 19), (-70.5, y, 27.3), 1.98))
    for x, y in GUARD_FOOT:
        g.cut(foot, g.cyl((x, y, 4), (x, y, 13), 2.22))
    return foot


def cartridge(bench):
    g = bench.g
    # A removable bearing bridge routes belt tension to the bed, away from the motor horn.
    foot = g.rounded(-88, -28, 48.7, 101, 27.03, 38, 4)
    for y0, y1, start in ((51, 61.2, 52), (86, 98.2, 89)):
        a = g.box(X_MOTOR - 19, X_MOTOR + 19, y0, y1, 36, MOTOR_Z)
        g.union(a, g.cyl((X_MOTOR, y0, MOTOR_Z), (X_MOTOR, y1, MOTOR_Z), 19))
        g.union(foot, a)
        g.cut(foot, g.cyl((X_MOTOR, y0 - .2, MOTOR_Z), (X_MOTOR, y1 + .2, MOTOR_Z), 10.72),
              g.cyl((X_MOTOR, start, MOTOR_Z), (X_MOTOR, y1 + .2, MOTOR_Z), 14.04))
    for x, y in CART_FOOT:
        for dx in (-2, -1, 0, 1, 2):
            g.cut(foot, g.cyl((x + dx, y, 26.5), (x + dx, y, 38.5), 2.65))
    for y in (60.13, 97.15):
        g.cut(foot, g.cyl((X_MOTOR, y, MOTOR_Z), (X_MOTOR, y + .93, MOTOR_Z), 14.47))
    return foot


def load_arm(bench):
    g = bench.g
    hub = g.cyl((0, -12.9, 0), (0, 12.9, 0), 21.25)
    g.union(hub, g.box(14, 62.5, -12.9, 12.9, -7.8, 7.8))
    g.cut(hub, g.cyl((0, -14, 0), (0, 14, 0), 6.04))
    keyway(g, hub, -12.9, 12.9)
    arm = g.rounded(13, 177, -19, 19, -11, 13, 6)
    g.cut(arm, g.box(11, 62.65, -13.05, 13.05, -13, 13.4))
    for x in (42, 55):
        for body in (arm, hub):
            g.cut(body, g.cyl((x, -20, 0), (x, 20, 0), 3.18))
    for x in (124, 148, 169):
        g.cut(arm, g.cyl((x, 0, -12), (x, 0, 14), 3.25))
    # The stop pin attaches to the metal hub on a welded lug, outside the load beam.
    g.union(hub, g.box(13, 38, -21.6, -12.72, -7.7, 7.7))
    g.cut(hub, g.cyl((34, -22, 0), (34, -16, 0), 4.08))
    g.cut(arm, g.box(12, 38.25, -20, -12.98, -7.95, 7.95))
    return arm, hub


def limit_plate(bench):
    g = bench.g
    stop = bench.ring(0, 0, -28.3, -22.2, 43, 10.9)
    for degree in range(-2, 63, 2):
        a = math.radians(degree)
        x, z = 34 * math.cos(a), 34 * math.sin(a)
        g.cut(stop, g.cyl((x, -29, z), (x, -21, z), 4.34))
    for x in (-20, 20):
        stub = bench.ring(x, 0, -30.0, -28.15, 4.6, 2.74)
        g.cut(stop, g.cyl((x, -29, 0), (x, -21, 0), 2.74))
        g.union(stop, stub)
        g.cut(stop, g.cyl((x, -25.23, 0), (x, -21, 0), 4.14))
    return stop


def guard(bench):
    g = bench.g
    base = g.rounded(-97, 73, 86, 119, 12.04, 18, 4)
    g.union(base, g.box(-96, 72, 111, 116, 16, 206),
            g.box(-96, -91, 85, 115, 16, 206), g.box(64, 72, 85, 115, 16, 206))
    g.union(base, g.box(-96, 72, 86, 116, 202, 208))
    g.cut(base, g.box(-87, -29, 85, 101.3, 11.95, 27.3))
    for x, y in GUARD_FOOT:
        g.cut(base, g.cyl((x, y, 11), (x, y, 19), 2.25))
    return base


def report_load():
    masses = (
        ("segment_1", .14272, .075), ("motor_J3", .165, .130), ("hardware_J3", .080, .140),
        ("segment_2", .11904, .200), ("motor_J4", .082, .253), ("hardware_J4", .060, .263),
        ("segment_3", .08771, .319), ("motor_J5", .023, .375), ("hardware_J5", .040, .375),
        ("wrist_1", .02737, .395), ("wrist_2", .02580, .443), ("motor_J6", .082, .414),
        ("motor_J7", .023, .455), ("hardware_J6_J7", .045, .440),
        ("hand_and_15_KST", .40746, .580), ("cables", .060, .380), ("payload", .100, .700),
        ("J2_mobile_moyeu_estimation", .220, .036),
    )
    static = 9.81 * sum(m * x for _, m, x in masses)
    inertia = sum(m * x * x for _, m, x in masses)
    design = (static + .6 * inertia + .25) * 1.35
    return {"masse_distale_kg": round(sum(m for _, m, _ in masses), 4),
            "hypotheses_kg_m": masses, "couple_statique_Nm": round(static, 3),
            "inertie_kgm2": round(inertia, 4), "acceleration_rad_s2": .6,
            "frottement_Nm_hyp": .25, "coefficient": 1.35, "couple_dimensionnement_Nm": round(design, 3),
            "rendement_hyp": .85, "couple_moteur_Nm": round(design / (4 * .85), 3),
            "vitesse_sortie_a_vide_tr_min": 7, "surcouple_maintien_frein_Nm": round(16 / design, 2)}


def build(app, base, util, report, write, export_archive, open_f3d, get_design):
    OUT.mkdir(exist_ok=True)
    bench = util.Bench(app, base, get_design, "J2 épaule avec frein à manque de courant")
    g = bench.g
    bench.part("J20_Socle", "J2 · platine ancrée et deux montants", support(bench), "dark",
               print_face=0).isGrounded = True
    bench.part("J22_Cartouche", "J2 · cartouche amovible, deux roulements d'entrée", cartridge(bench),
               "ice", print_face=0)
    bench.rigid("J22_Cartouche", "J20_Socle")
    for x, y in CART_FOOT:
        fastener(bench, f"Vis_cartouche_{x}_{y}", (x, y, 0), (19, 38.12), 2.46, 4,
                 "J20_Socle", "z")

    frame = base.frame((0, 16.2, 0), roll=-90)
    model = commercial_step(bench, "XM540_ROBOTIS.step", frame)
    stator = clip(g, g.manager.copy(model), g.box(-40, 40, -22, 39.3, -20, 55))
    horn = clip(g, model, g.box(-20, 20, 39.3, 48, -20, 20))
    for x in (-13.5, 13.5):
        g.cut(stator, g.cyl((x, 34.36, 10.5), (x, 38.44, 10.5), 1.29))
    for a in range(0, 360, 45):
        x, z = 11 * math.cos(math.radians(a)), 11 * math.sin(math.radians(a))
        g.cut(horn, g.cyl((x, 40.6, z), (x, 45.0, z), 1.26))
    bench.part("ROBOTIS_XM540", "XM540-W270-T · solide officiel rogné au plan de sortie",
               stator, "metal", DRIVE, typed="ROBOTIS XM540-W270-T")
    bench.part("HN13_N101", "HN13-N101 · face active et vis M3 du modèle officiel", horn, "metal", DRIVE, "y")
    bench.rigid("ROBOTIS_XM540", "J20_Socle")
    # The bracket uses the two auxiliary tapped mounting holes, not the four case screws.
    bracket = g.box(-20, 20, 38.28, 41.22, 4.0, 24.0)
    g.cut(bracket, g.cyl((0, 38, 0), (0, 42, 0), 14.6))
    for x in (-13.5, 13.5):
        g.cut(bracket, g.cyl((x, 38, 10.5), (x, 42, 10.5), 1.40))
    g.union(bracket, g.box(-21, -17, 42, 48, 27.05 - MOTOR_Z, 23.8),
            g.box(-20.7, -17, 40.9, 42.3, 7, 23.8))
    g.union(bracket, g.box(-22, -7, 33.8, 48.4, 27.05 - MOTOR_Z, 32 - MOTOR_Z))
    for y in SERVO_FOOT_Y:
        for dx in (-1.4, 0, 1.4):
            g.cut(bracket, g.cyl((-12.5 + dx, y, 26.9 - MOTOR_Z), (-12.5 + dx, y, 32.5 - MOTOR_Z), 2.3))
    bench.part("Support_XM540", "Équerre métallique démontable XM540", bracket, "metal", DRIVE)
    bench.rigid("Support_XM540", "J20_Socle")
    for y in SERVO_FOOT_Y:
        fastener(bench, f"Vis_socle_XM540_{y}", (-70.5, y, 0), (23.2, 32.05), 1.93, 3.45,
                 "J20_Socle", "z")
    for x in (-13.5, 13.5):
        fastener(bench, f"Vis_XM540_{x}", (X_MOTOR + x, 0, MOTOR_Z + 10.5),
                 (35.90, 41.26), 1.20, 2.13, "Support_XM540")

    link = g.cyl((0, 43.52, 0), (0, 49, 0), 13.6)
    g.cut(link, g.cyl((0, 43.2, 0), (0, 47, 0), 5.17))
    for a in range(0, 360, 45):
        x, z = 11 * math.cos(math.radians(a)), 11 * math.sin(math.radians(a))
        g.cut(link, g.cyl((x, 43.25, z), (x, 49.2, z), 1.34))
        if a % 90 == 0:
            fastener(bench, f"Vis_horn_{a}", (X_MOTOR + x, 0, MOTOR_Z + z),
                     (41.5, 49.04), 1.18, 2.10, "HN13_N101")
    s = shaft(g, 47.5, 102, ((62, 81.2),))
    g.union(s, link)
    bench.part("Arbre_entree", "Arbre d’entrée Ø12 avec bride usinée", s, "metal", DRIVE)
    bench.rigid("Arbre_entree", "HN13_N101")

    output_ranges = ((-106, -58), (-13.1, 12.9), (61.8, 81.25))
    bench.part("Arbre_J2", "Arbre traversant Ø12 × 200, acier à clavettes", shaft(g, -109, 91, output_ranges),
               "metal", LOAD, "y")
    for side, center, ranges in (("input", DRIVE, ((62, 81.2),)), ("J2", LOAD, output_ranges)):
        for i, (a, b) in enumerate(ranges):
            name = f"Clavette_{side}_{i}"
            bench.part(name, "Clavette parallèle acier 4 × 4", g.box(-2, 2, a + .15, b - .15, 4.18, 8.18),
                       "metal", center)
            bench.rigid(name, "Arbre_entree" if side == "input" else "Arbre_J2")
    for xy, ys, rotor in ((DRIVE, (52, 89), "Arbre_entree"), (LOAD, (-42, 32), "Arbre_J2")):
        for y in ys:
            bearing(bench, str(y).replace("-", "m"), xy[0], xy[2], y, rotor)
    for y in (60.1, 97.12):
        n = f"Circlip_palier_{y}"
        shape = bench.ring(0, 0, y, y + .9, 14.03, 12.98)
        bench.part(n, "Arrêt de bague extérieure · anneau DIN472 à qualifier", shape, "metal", DRIVE)
        bench.rigid(n, "J22_Cartouche")
    for side, collar, lip in (("g", (-47.25, -45.03), (-45.18, -42.04)),
                               ("d", (44.05, 46.22), (40.04, 44.16))):
        keep = bench.ring(0, 0, *collar, 25.3, 10.17)
        g.union(keep, bench.ring(0, 0, *lip, 13.94, 10.17))
        for x in (-20, 20):
            g.cut(keep, g.cyl((x, collar[0] - 1, 0), (x, collar[1] + 1, 0), 2.68))
        n = f"Couvercle_palier_{side}"
        bench.part(n, "Couvercle métallique de retenue extérieure Ø28", keep, "metal", LOAD)
        bench.rigid(n, "J20_Socle")
    for rotor, center, positions in (("Arbre_entree", DRIVE, (60.1, 81.7, 97.41)),
                                     ("Arbre_J2", LOAD, (-46.64, -33.96, 27.36, 40.04, 82.0))):
        for i, y in enumerate(positions):
            tag = f"Bague_{rotor}_{i}"
            width = 1.13 if y == 60.1 else 4.6
            bench.part(tag, "Retenue axiale Ø12 avec vis de serrage",
                       bench.ring(0, 0, y, y + width, 9.9, 6.02),
                       "metal", center)
            bench.rigid(tag, rotor)

    for size, name, center, r, drive in ((16, "Poulie_16", DRIVE, R_SMALL, "Arbre_entree"),
                                         (64, "Poulie_64", LOAD, R_BIG, "Arbre_J2")):
        bench.part(name, f"Poulie crantée métallique {size}T · volume d'interface", pulley(bench, r), "metal", center)
        bench.rigid(name, drive)
    bench.part("Courroie", "Courroie Gates 425‑5M‑15 · enveloppe de pas", belt(bench), "rubber")
    bench.rigid("Courroie", "J20_Socle")

    arm, hub = load_arm(bench)
    bench.part("Moyeu_J2", "Moyeu acier claveté et patte de butée", hub, "metal", LOAD)
    bench.rigid("Moyeu_J2", "Arbre_J2")
    bench.part("J21_Levier", "Levier structurel d’essai, fixation des masses", arm, "ice", LOAD, print_face=180)
    bench.rigid("J21_Levier", "Moyeu_J2")
    for x in (42, 55):
        fastener(bench, f"Vis_hub_M6_{x}", (x, 0, Z), (-19.0, 19.03), 2.98, 5, "Moyeu_J2")
    bench.part("Platine_butee", "Butée J2 · secteur acier rainuré", limit_plate(bench), "metal", LOAD)
    bench.rigid("Platine_butee", "J20_Socle")
    for x in (-20, 20):
        for side, low, high in (("ex", -44.96, -40.22), ("int", -39.74, -30.03)):
            tag = f"Douille_M5_{side}_{x}"
            bench.part(tag, "Douille taraudée M5 Ø7, retenue sur montant", bench.ring(x, 0, low, high, 3.48, 2.50),
                       "metal", LOAD)
            bench.rigid(tag, "J20_Socle")
        fastener(bench, f"Vis_butee_M5_{x}", (x, 0, Z), (-39.8, -25.17), 2.46, 4.05, "Platine_butee")
    bench.part("Pion_butee", "Pion de butée acier Ø8", g.cyl((34, -29, 0), (34, -16, 0), 4),
               "accent", LOAD)
    bench.rigid("Pion_butee", "Moyeu_J2")

    mount = bench.ring(0, 0, -62.05, -53.1, 50.7, 13.66)
    for x in (-20, 20):
        tab = bench.ring(x, 0, -53.20, -47.29, 7.1, 2.72)
        g.union(mount, tab)
        g.cut(mount, g.cyl((x, -62.5, 0), (x, -52.7, 0), 2.72))
        g.cut(mount, g.cyl((x, -62.5, 0), (x, -59.3, 0), 4.35))
    brake = bench.ring(0, 0, -105.2, -62.14, 51, 13.5)
    for a in range(0, 360, 90):
        x, z = 46.5 * math.cos(math.radians(a)), 46.5 * math.sin(math.radians(a))
        for o in (mount, brake):
            g.cut(o, g.cyl((x, -106, z), (x, -52, z), 2.76))
    bench.part("Fixe_frein", "Bride d’adaptation du frein en acier", mount, "metal", LOAD)
    bench.rigid("Fixe_frein", "J20_Socle")
    for x in (-20, 20):
        local = g.cyl((x, -59.42, 0), (x, -41.17, 0), 2.46)
        g.union(local, g.cyl((x, -61.96, 0), (x, -59.35, 0), 4.2))
        name = f"Vis_bride_frein_{x}"
        bench.part(name, "Vis noyée et bride de réaction M5", local, "metal", LOAD)
        bench.rigid(name, "Fixe_frein")
    bench.part("Frein_stator", "Frein à ressort Kendrion KS 10110A00-0001 · enveloppe",
               brake, "dark", LOAD, typed="Kendrion KS 10110A00-0001")
    bench.rigid("Frein_stator", "Fixe_frein")
    for a in range(0, 360, 90):
        x, z = 46.5 * math.cos(math.radians(a)), 46.5 * math.sin(math.radians(a))
        fastener(bench, f"Vis_frein_M5_{a}", (x, 0, Z + z), (-76, -53.07), 2.46, 4.0, "Fixe_frein")
    slider = bench.ring(0, 0, -103, -64, 13.35, 6.05)
    keyway(g, slider, -103, -64)
    bench.part("Frein_moyeu", "Moyeu du frein sur arbre J2 · portée Ø12 et clavette", slider,
               "metal", LOAD)
    bench.rigid("Frein_moyeu", "Arbre_J2")

    bench.part("J23_Carter", "Carter d’essai démontable", guard(bench), "dark", print_face=0).isLightBulbOn=False
    bench.rigid("J23_Carter", "J20_Socle")
    for x, y in GUARD_FOOT:
        fastener(bench, f"Vis_carter_M4_{x}", (x, y, 0), (5.0, 18.03), 1.95, 3.4, "J20_Socle", "z")
    connector = g.rounded(-104, -87, -14, 1, 17, 28, 2)
    g.union(connector, g.cyl((-99, -1, 22), (-99, 21, 22), 2.4))
    bench.part("Reserve_J2", "Réserve de connecteur et sortie gaine fixe", connector, "accent")
    bench.rigid("Reserve_J2", "J20_Socle")

    driver = bench.pivot("Moteur_J2", "HN13_N101", "ROBOTIS_XM540")
    driven = bench.pivot("Sortie_J2", "Arbre_J2", "J20_Socle")
    d_motion, l_motion = driver.jointMotion, driven.jointMotion
    d_zero, l_zero = d_motion.rotationValue, l_motion.rotationValue
    witness_local = base.point((155, 0, 0))
    sig = 1
    util.apply_pose(l_motion, 4, l_zero)
    trial = witness_local.copy()
    trial.transformBy(bench.parts["J21_Levier"].transform2)
    if trial.z * 10 < Z:
        sig = -1
    util.apply_pose(l_motion, 0, l_zero)
    link_input = bench.root.motionLinks.createInput(driver, driven)
    link_input.motionOne = fusion.JointMotionTypes.RevoluteJointRotateMotionType
    link_input.motionTwo = fusion.JointMotionTypes.RevoluteJointRotateMotionType
    link_input.valueOne = core.ValueInput.createByString("360 deg")
    link_input.valueTwo = core.ValueInput.createByString("90 deg")
    motion_link = bench.root.motionLinks.add(link_input)
    motion_link.name = "Synchronisme 16:64 (4:1)"
    util.apply_pose(d_motion, 16, d_zero, sig)
    first = math.degrees(l_motion.rotationValue - l_zero)
    used_driver = abs(first - sig * 4) <= .13
    states = []
    for angle in (*range(0, 61, 5), 69, 60, 40, 0, -7):
        if used_driver:
            util.apply_pose(d_motion, angle * RATIO, d_zero, sig)
        else:
            util.apply_pose(l_motion, angle, l_zero, sig)
        actual = math.degrees(math.remainder(l_motion.rotationValue - l_zero, math.tau)) * sig
        motor_angle = math.degrees(d_motion.rotationValue - d_zero) * sig
        motor_angle += 360 * round((angle * RATIO - motor_angle) / 360)
        witness = witness_local.copy()
        witness.transformBy(bench.parts["J21_Levier"].transform2)
        states.append({"commande_sortie_deg": angle,
                       "course_moteur_deg": round(motor_angle, 3),
                       "course_sortie_deg": round(actual, 3),
                       "temoin_xyz_mm": [round(x * 10, 3) for x in witness.asArray()],
                       "interferences": bench.measure()})
        adsk.doEvents()
    util.apply_pose(l_motion, 0, l_zero)
    limits = l_motion.rotationLimits
    limits.minimumValue, limits.maximumValue = sorted((l_zero, l_zero + sig * math.radians(ELBOW_LIMIT)))
    limits.isMinimumValueEnabled = limits.isMaximumValueEnabled = True
    data = {"rapport": RATIO, "entraxe_mm": round(CENTER, 3),
            "enroulement_petite_poulie_deg": round(180 - 2 * math.degrees(TANGENT_ANGLE), 2),
            "positions_mm": {"moteur": DRIVE, "arbre": LOAD}, "entraine_par_le_moteur": used_driver,
            "controle_entree_16deg_sortie": round(first, 3), "liaisons": bench.root.asBuiltJoints.count,
            "poses": states, "dimensionnement": report_load()}
    report["epaule"] = data
    write(report)
    bench.camera((5, 8, 98), (250, 360, 280), 365, OUT / "Epaule_transmission.png")
    bench.parts["J23_Carter"].isLightBulbOn=True
    bench.camera((5, 8, 98), (260, 300, 320), 365, OUT / "Epaule_carter.png")
    archive = OUT / "AURA-01_J2_Epaule_Pilote.f3d"
    export_archive(bench.design, archive)
    data["archive"], data["sha256"] = archive.name, util.digest(archive)
    data["fabrication"] = bench.export_prints(OUT)
    data["termine"] = True
    write(report)
    bench.doc.activate()
