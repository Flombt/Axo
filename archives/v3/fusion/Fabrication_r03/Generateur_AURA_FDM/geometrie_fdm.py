"""Formes FDM en mm et positions des pivots, sans dépendance à une imprimante."""

import math
import adsk.core as core


ARM = (
    (140, 55.0, 46, 52),
    (123, 55.0, 44, -34),
    (112, 46.0, 38, -37),
)
FINGER_LENGTHS = (46, 42, 37)
FINGERS = (
    ("P", "Pouce", (33, -68.5, 0), -49),
    ("I", "Index", (111, -48.5, 0), -1),
    ("M", "Majeur", (116, -16.2, 0), 0),
    ("A", "Annulaire", (111, 16.2, 0), 1),
    ("O", "Auriculaire", (105, 48.5, 0), 3),
)
PARTS = {
    "BASE": ("01_Socle", "Socle ancré", 1, "dark", "base"),
    "J1": ("02_Tourelle", "Tourelle et chape d’épaule", 1, "ice", "base"),
    "J2": ("03_Segment_proximal", "Segment proximal", 1, "dark", "dos"),
    "J3": ("04_Segment_intermediaire", "Segment intermédiaire", 1, "dark", "dos"),
    "J4": ("05_Segment_distal", "Segment distal", 1, "dark", "flanc"),
    "J5": ("06_Poignet_deviation", "Poignet · déviation", 1, "ice", "dos"),
    "J6": ("07_Poignet_flexion", "Poignet · flexion et palier de roulis", 1, "ice", "dos"),
    "J7": ("08_Paume", "Paume blanche", 1, "white", "dos"),
    "F1": ("09_Phalange_proximale", "Phalange proximale", 5, "white", "dos"),
    "F2": ("10_Phalange_moyenne", "Phalange moyenne", 5, "white", "dos"),
    "F3": ("11_Phalange_distale", "Phalange distale", 5, "white", "dos"),
}


class Printable:
    def __init__(self, base, solids):
        self.base = base
        self.g = solids

    def move(self, body, xyz, yaw=0):
        if not self.g.manager.transform(body, self.base.frame(xyz, yaw=yaw)):
            raise RuntimeError("Transformation d’une forme impossible.")
        return body

    def bore(self, xyz, low, high, radius, axis, roof=None):
        """A horizontal bore has a 45 degree roof on its upward side as printed."""
        g = self.g
        x, y, z = xyz
        if axis == "z":
            round_part = g.cyl((x, y, low), (x, y, high), radius)
            boss = g.box(-radius / 2, radius / 2, -radius / 2, radius / 2, low, high)
            vector = (0, 0, 1)
            offset = (x, y + roof * radius / math.sqrt(2), 0) if roof is not None else None
        elif axis == "y":
            round_part = g.cyl((x, low, z), (x, high, z), radius)
            boss = g.box(-radius / 2, radius / 2, low, high, -radius / 2, radius / 2)
            vector = (0, 1, 0)
            offset = (x, 0, z + roof * radius / math.sqrt(2)) if roof is not None else None
        else:
            round_part = g.cyl((low, y, z), (high, y, z), radius)
            boss = g.box(low, high, -radius / 2, radius / 2, -radius / 2, radius / 2)
            vector = (1, 0, 0)
            offset = (0, y, z + roof * radius / math.sqrt(2)) if roof is not None else None
        if offset is not None:
            spin = core.Matrix3D.create()
            spin.setToRotation(math.pi / 4, self.base.vector(vector), self.base.point((0, 0, 0)))
            if not g.manager.transform(boss, spin):
                raise RuntimeError("Construction du toit de perçage impossible.")
            g.union(round_part, self.move(boss, offset))
        return round_part

    def cheeks(self, x, z, start, inner, outer, z_low, z_high, radius, roof=-1):
        """Parallel raised sides leave the center free for rotation of the next link."""
        g = self.g
        result = []
        for low, high in ((-outer, -inner), (inner, outer)):
            lug = g.rounded(start, x + min(9, z_high - z), low, high,
                            z_low, z_high, min(2.6, (outer - inner) / 2 - 0.04))
            g.cut(lug, self.bore((x, 0, z), low - 1, high + 1, radius, "y", roof))
            result.append(lug)
        return result

    def fixed(self):
        g = self.g
        body = g.rounded(-93, 93, -88, 88, 0, 10, 14)
        g.union(body, g.cyl((0, 0, 9.6), (0, 0, 26), 57, 49))
        g.cut(body, self.bore((0, 0, 0), -1, 27, 11.6, "z"))
        for x in (-74, 74):
            for y in (-70, 70):
                g.cut(body, self.bore((x, y, 0), -1, 11, 3.45, "z"))
        for x in (-17, 17):
            for y in (-19, 19):
                g.cut(body, self.bore((x, y, 0), 18, 27, 1.65, "z"))
        return body, None

    def turret(self):
        g = self.g
        body = g.cyl((0, 0, 0), (0, 0, 13), 47.5, 42.5)
        for side in (-1, 1):
            low, high = sorted((side * 28.15, side * 34.3))
            g.union(body, g.rounded(-20, 22, low, high, 8.2, 85, 2.8))
        g.cut(body, self.bore((0, 0, 0), -1, 14, 5.15, "z"))
        g.cut(body, self.bore((0, 0, 69), -35.5, 35.5, 4.35, "y", 1))
        for y in (-31.1, 31.1):
            g.cut(body, self.bore((-12, y, 0), -1, 10, 1.7, "z"))
        return body, None

    def arm(self, i):
        g = self.g
        length, width, height, _ = ARM[i - 1]
        half = width / 2
        top = height / 2
        lead = -19 if i < 3 else -16.8
        # Underneath, the servo and harness can be reached from one opening.
        body = g.rounded(lead, length - 34, -half, half, -top, top, 7.5)
        motor_l, motor_w, motor_h = (58.5, 44, 33.5) if i < 3 else (46.5, 34, 28.5)
        motor_start = -13.1 if i < 3 else -10.8
        motor = g.box(motor_start, motor_start + motor_l, -motor_w / 2, motor_w / 2, -motor_h / 2, motor_h / 2)
        motor_pocket = g.rounded(motor_start - 1.5, motor_start + motor_l + 3,
                                 -motor_w / 2 - 1.1, motor_w / 2 + 1.1, -top - 1,
                                 motor_h / 2 + 1.05, 2)
        g.cut(body, motor_pocket)
        cable_x0 = motor_start + motor_l + 1
        g.cut(body, g.rounded(cable_x0, length - 39.0, -12.5, 12.5, -top - 1, top - 4.1, 2.4))
        g.cut(body, self.bore((0, 0, 0), -half - 1, half + 1, 4.25, "y", -1 if i < 3 else None))
        if i < 3:
            inner = ARM[i][1] / 2 + 0.70
            outer = inner + 6.45
            bridge = g.rounded(length - 49, length - 31.3, -outer, outer, top - 10.8, top, 4.3)
            g.union(body, bridge)
            for lug in self.cheeks(length, 0, length - 44, inner, outer, -12, top, 4.35):
                g.union(body, lug)
        else:
            # The terminal ring is entirely below the yaw stage's seating plane.
            nose = g.rounded(length - 51, length + 14.8, -half, half, -14.0, -1.15, 8)
            g.union(body, nose)
            g.cut(body, self.bore((length, 0, 0), -15, 0, 4.35, "z", -1))
        return body, motor

    def yaw(self):
        g = self.g
        body = g.rounded(-14, 24, -24.3, 24.3, 0.8, 19, 10.5)
        g.cut(body, self.bore((0, 0, 0), -1, 20, 4.2, "z"))
        for lug in self.cheeks(45, 8.5, 16, 18.75, 24.3, -0.2, 19, 3.3):
            g.union(body, lug)
        return body, None

    def pitch(self):
        g = self.g
        body = g.rounded(-10.8, 39, -18, 18, -12.7, 10.5, 7.0)
        g.cut(body, self.bore((0, 0, 0), -19, 19, 3.2, "y", -1))
        g.cut(body, self.bore((0, 0, 0), 23, 40, 5.25, "x", -1))
        g.cut(body, g.rounded(5.5, 23.8, -12.3, 12.3, -13, 5.9, 3.2))
        return body, None

    def finger_fork(self, x, start, top=8.9):
        return self.cheeks(x, 0, start, 11.85, 15.0, -6.2, top, 1.7)

    def palm(self):
        g = self.g
        body = g.rounded(8, 87, -61, 61, -12.1, 8.9, 21.4)
        hub = g.rounded(0.85, 33, -19.5, 19.5, -13.2, 8.9, 5.9)
        g.union(body, hub)
        g.cut(body, self.bore((0, 0, 0), 0, 28.5, 5.2, "x", -1))
        g.cut(body, g.rounded(28, 82, -54, 54, -14, 5.2, 12))
        distal_bridge = g.rounded(70, 89.0, -63, 63, 0.5, 8.9, 5.6)
        g.union(body, distal_bridge)
        for code, _, position, yaw in FINGERS:
            if code == "P":
                shoulder = g.rounded(-29, -13.9, -17, 17, 1.2, 8.9, 4)
                g.union(body, self.move(shoulder, position, yaw))
            start = -42 if code != "P" else -25.2
            for lug in self.finger_fork(0, start):
                g.union(body, self.move(lug, position, yaw))
            if code == "P":
                space = g.box(-14, 22, -11.55, 11.55, -16, 16)
                g.cut(body, self.move(space, position, yaw))
        return body, None

    def finger(self, stage):
        g = self.g
        length = FINGER_LENGTHS[stage - 1]
        tip = stage == 3
        end = length - (1.4 if tip else 15.1)
        top, bottom = 8.9, -7.5
        shell = g.rounded(-10.3, end, -11.05, 11.05, bottom, top, 3.4)
        opening = g.rounded(-9.63, 21.4, -8.92, 8.92, bottom - 1, 5.95, 1.35)
        g.cut(shell, opening)
        # The output shaft can slide into the housing while the motor is inserted.
        g.cut(shell, g.box(-2.45, 2.45, 8.0, 11.8, bottom - 1.0, 0.4))
        g.cut(shell, self.bore((0, 0, 0), 8.7, 12, 2.53, "y", -1))
        g.cut(shell, self.bore((0, 0, 0), -12, -8.65, 1.7, "y", -1))
        g.cut(shell, g.box(4.1, 20.8, -10.5, -8.0, bottom - 1, -0.8))
        for x in (-7, 17):
            mount = g.box(x - 1.69, x + 1.69, -10.45, 3.40, -1.6, 7.9)
            g.union(shell, mount)
            g.cut(shell, self.bore((x, 0, 0), -0.5, 3.58, 0.81, "y", -1))
            g.cut(shell, self.bore((x, 0, 0), 8.45, 11.6, 1.51, "y", -1))
        g.cut(shell, g.box(19.7, 22.7, -3.1, 3.1, bottom - 1, 3.5))
        if tip:
            g.cut(shell, g.rounded(23.1, end - 3.3, -7.9, 7.9, bottom - 1, 5.95, 1.6))
        else:
            back = g.rounded(end - 6.4, end, -15.0, 15.0, 1.1, top, 2.5)
            g.union(shell, back)
            for lug in self.finger_fork(length, end - 4.9, top):
                g.union(shell, lug)
        motor = g.box(-5, 15, -8.3, 8.3, -3.5, 3.5)
        g.union(motor, g.box(-9, 19, 3.6, 4.6, -3.5, 3.5), g.cyl((0, 8.25, 0), (0, 11, 0), 1.95))
        for x in (-7, 17):
            g.cut(motor, g.cyl((x, 3.45, 0), (x, 4.75, 0), 1.1))
        return shell, motor
