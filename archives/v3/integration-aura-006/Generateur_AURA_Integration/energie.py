"""Implantation du compartiment batterie, commande et capteurs de la V3."""

import math


BATTERY = "RELiON RB24V20"
BAT_X = -207
BAT_DIMS = (195, 131, 171)
TRAY = (-2, 137, 0)


def fixed(bench, key, label, body, finish, parent, origin=(0, 0, 0), print_face=None, reference=None):
    bench.part(key, label, body, finish, origin, print_face=print_face, typed=reference)
    bench.rigid(key, parent)


def module_layout(bench):
    g = bench.g
    dock = g.rounded(-107, 107, -75, 75, 0, 21.4, 8)
    g.cut(dock, g.box(-98.6, 98.6, -67.1, 67.1, 8, 22.0))
    for x in (-101.5, 101.5):
        for y in (-70.5, 70.5):
            g.cut(dock, g.cyl((x, y, -1), (x, y, 23), 2.78))
    for x in (-39, 39):
        for y in (-70, 70):
            g.cut(dock, g.box(x - 11, x + 11, y - 6, y + 6, 8, 22.0))
    fixed(bench, "E01_Berceau_batterie", "Berceau batterie · deux sangles et quatre boulons au bâti",
          dock, "dark", "Socle", (BAT_X, 0, 0), 0)
    h = 8.12 + BAT_DIMS[2]
    pack = g.box(-97.5, 97.5, -65.5, 65.5, 8.12, h)
    fixed(bench, "E_Batterie", "Batterie externe LiFePO₄ 25,6 V · réserve d'encombrement",
          pack, "ice", "E01_Berceau_batterie", (BAT_X, 0, 0), reference=BATTERY)
    for x in (-66, 66):
        fixed(bench, "E_Borne_reserve_" + str(x), "Dégagement cosse isolée et câble batterie",
              g.cyl((x, 0, h + .06), (x, 0, h + 42), 12.4), "accent", "E_Batterie", (BAT_X, 0, 0))
    for x in (-39, 39):
        u = g.box(x - 10, x + 10, -68, 68, h + .12, h + 1.37)
        g.union(u, g.box(x - 10, x + 10, -68, -66.15, 12, h + .8),
                g.box(x - 10, x + 10, 66.15, 68, 12, h + .8))
        fixed(bench, "E_Sangle_" + str(x), "Sangle dédiée 20 mm avec garde sur les bornes",
              u, "rubber", "E01_Berceau_batterie", (BAT_X, 0, 0))

    tray = g.rounded(-90, 90, -47, 47, 0, 8, 6)
    g.union(tray, g.box(-88, -84, -42, 42, 6, 31), g.box(84, 88, -42, 42, 6, 31))
    for x in (-73, 73):
        for y in (-40, 37):
            g.cut(tray, g.cyl((x, y, -1), (x, y, 9), 2.75))
    for x in (-76.5, -18.5):
        for y in (-24.5, 24.5):
            g.union(tray, g.cyl((x, y, 7.6), (x, y, 13.9), 3.5))
            g.cut(tray, g.cyl((x, y, 7.4), (x, y, 14.2), 1.31))
    fixed(bench, "E02_Platine", "Platine électronique amovible et entretoises Raspberry Pi",
          tray, "dark", "Socle", TRAY, 0)
    pi = g.box(-80, 5, -28, 28, 14.02, 36.1)
    for x in (-76.5, -18.5):
        for y in (-24.5, 24.5):
            g.cut(pi, g.cyl((x, y, 13), (x, y, 37), 1.55))
    fixed(bench, "E_Pi5", "Raspberry Pi 5 et dégagement refroidisseur",
          pi, "ice", "E02_Platine", TRAY, reference="Raspberry Pi 5 85 × 56 mm")
    fixed(bench, "E_OpenRB", "OpenRB‑150 · logique et signal TTL",
          g.box(11, 77, -29, -4, 14.1, 29.5), "accent", "E02_Platine", TRAY, reference="ROBOTIS OpenRB-150 66 × 25 mm")
    fixed(bench, "E_Coupure", "Réserve de relais, contacteurs et fusibles",
          g.box(11, 82, 6, 39, 14.1, 69.0), "metal", "E02_Platine", TRAY)
    fixed(bench, "E_Plaque_DC", "Réserve convertisseurs et dissipateur · plateau métallique distinct",
          g.box(99, 245, -42, 41, 2, 51), "metal", "Socle", TRAY)
    fixed(bench, "E_Prise_charge", "Connecteur de recharge avec verrou matériel marche",
          g.box(-58, -35, 30, 44, 25, 46), "rubber", "E02_Platine", TRAY)
    fixed(bench, "E_Support_camera", "Support fixe caméra 25 × 24, marge d’objectif",
          g.rounded(28, 60, -82, -52.5, 10.04, 27.4, 3), "dark", "Socle", print_face=0)
    fixed(bench, "E_Camera", "Raspberry Pi Camera Module 3, emplacement fixe",
          g.box(31.5, 56.5, -79, -55, 27.47, 38.97), "accent", "E_Support_camera",
          reference="Raspberry Pi Camera Module 3")
    fixed(bench, "E_Micro", "Zone microphone I²S et mousse, séparée des engrenages",
          g.box(62.2, 81.2, -84, -69.1, 11.2, 20), "ice", "Socle")
    fixed(bench, "E_Estop", "Zone arrêt d’urgence accessible, sur socle fixe",
          g.cyl((63, 43, 11), (63, 43, 36), 17.3), "accent", "Socle")


def tray_for_hand(bench):
    g = bench.g
    tray = g.rounded(13, 84, -19, 18, -18, -11.70, 3.2)
    g.cut(tray, g.box(16.5, 81.5, -15.1, 14, -15.7, -11.6))
    for x in (20, 77):
        for y in (-16, 15):
            g.cut(tray, g.cyl((x, y, -18.3), (x, y, -11.2), 1.18))
    return tray


def hand_modules(bench, palm_frame):
    g = bench.g
    for key, name, volume, finish, orientation, reference in (
        ("E03_Platine_PWM", "Berceau déporté logique main, accès par dessous", tray_for_hand(bench), "white", 180, None),
        ("E_PWM", "PCA9685 carte 815 · signaux PWM seuls", g.box(18, 80.5, -13.9, 11.5, -15.65, -11.78),
         "accent", None, "Adafruit 815 – carte 62,5 × 25,4 mm"),
        ("E_MCU_main", "Réserve carte MCU main / RS‑485", g.box(13, 67, 22, 45, -10.5, -.6), "accent", None, None),
        ("E_Power_main", "Réserve répartition 6 V et connecteurs par doigt",
         g.box(29, 71, -45, -21, -13.2, -3.0), "metal", None, None),
        ("E_ToF", "Réserve module proximité sur dos de la main", g.box(70, 90, -8, 8, 9.08, 16.4), "accent", None, None),
    ):
        bench.part(key, name, volume, finish, print_face=orientation, typed=reference, placement=palm_frame)
        bench.rigid(key, "Paume")


def tube(bench, vertices, radius):
    g = bench.g
    sections = []
    for a, b in zip(vertices, vertices[1:]):
        unit = tuple((v - u) / math.dist(a, b) for u, v in zip(a, b))
        aa = tuple(v - .4 * u for v, u in zip(a, unit))
        bb = tuple(v + .4 * u for v, u in zip(b, unit))
        sections.append(g.cyl(aa, bb, radius))
    return g.union(sections[0], *sections[1:])


ROUTES = (
        ("Socle", "Socle → J1", ((-14, 101, 25), (-55, 101, 25), (-63, 42, 27)), 4.5),
        ("J1", "J1 → J2", ((-39, -19, 19), (-42, -27, 48), (-33, -45, 67)), 4.3),
        ("J2", "J2 → J3", ((5, -44, -15), (40, -43.5, -16), (113, -42.5, -16), (128, -44, -14)), 4.2),
        ("J3", "J3 → J4", ((18, -48, -15), (44, -48, -16), (94, -48, -13), (105, -48, -11)), 4.0),
        ("J4", "J4 → J5", ((25, -41, -14), (79, -38, -14), (105, -35, -10)), 3.9),
        ("J5", "J5 → J6", ((0, -31, 16), (21, -31, 16), (41, -31, 17)), 3.5),
        ("J6", "J6 → J7", ((5, -39, -9), (19, -39, -13), (34, -36, -15)), 3.3),
)


def loom(bench, frames):
    g = bench.g
    # The moving joints need independent service loops. These solids reserve the straight runs.
    lengths = {}
    for parent, label, points, radius in ROUTES:
        name = "Faisceau_" + parent
        bench.part(name, label + " · tronçon rigide d’encombrement", tube(bench, points, radius),
                   "accent", placement=frames[parent])
        bench.rigid(name, parent)
        lengths[parent] = round(sum(math.dist(a, b) for a, b in zip(points, points[1:])), 1)
        for index, point in enumerate((points[0], points[-1])):
            x, y, z = point
            n = f"Connecteur_{parent}_{index}"
            volume = g.rounded(x - 6.3, x + 6.3, y - 6.6, y + 6.6, z - 5, z + 5, 2.0)
            neighbor = points[1] if index == 0 else points[-2]
            unit = tuple((p - q) / math.dist(point, neighbor) for p, q in zip(point, neighbor))
            a = tuple(p - 12 * u for p, u in zip(point, unit))
            b = tuple(p + 12 * u for p, u in zip(point, unit))
            g.cut(volume, g.cyl(a, b, radius + .45))
            bench.part(n, "Dégagement connecteur et extraction " + label, volume, "metal", placement=frames[parent])
            bench.rigid(n, parent)
    return lengths


def coupon(g):
    block = g.rounded(-65, 65, -23, 23, 0, 9, 3)
    for x, r in ((-52, 2.20), (-37, 2.25), (-22, 2.27), (-7, 2.30), (8, 2.34), (23, 1.54)):
        g.cut(block, g.cyl((x, -11, -1), (x, -11, 10), r))
    for x, r in ((-47, 13.98), (-13, 14.04), (22, 14.13)):
        g.cut(block, g.cyl((x, 6, -1), (x, 6, 10), r))
    for y, r in ((-8, 1.37), (0, 1.50), (8, 1.57), (16, 1.68)):
        g.cut(block, g.cyl((50, y, -1), (50, y, 10), r))
    return block
