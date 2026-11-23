"""Solides du bras de table. Dimensions de construction en millimètres."""

import adsk.core as core

from geometrie import Solids, frame, point, vector


LONGUEURS = (47, 44, 40)
ANGLES_REPOS = (56, -38, -38)
HAUTEUR_TOURELLE = 36.9
HAUTEUR_EPAULE = 27
AXE_SERVO = -10.8
VIS_SERVO = (-8.2, 19.7)
FIXATIONS_SOCLE = (-29, 29)
POSES = (
    ("Repos", (0, 0, 0)),
    ("Salut à droite", (21, 9, 13)),
    ("Salut à gauche", (-21, 9, 13)),
    ("Retour", (0, 0, 0)),
)
LIMITES = ((-30, 30), (-12, 12), (-13, 18))
ANGLE_POIGNET = 12


class Formes(Solids):
    def place(self, body, transform):
        if not self.manager.transform(body, transform):
            raise RuntimeError("Transformation de solide refusée.")
        return body

    def side(self, x0, x1, z0, z1, y0, y1, radius):
        return self.place(
            self.rounded(x0, x1, z0, z1, -y1, -y0, radius), frame(roll=90)
        )

    def hole_y(self, x, z, low, high, radius):
        return self.cyl((x, low, z), (x, high, z), radius)

    def hole_z(self, x, y, low, high, radius):
        return self.cyl((x, y, low), (x, y, high), radius)

    def servo_lat(self, x, z=0):
        transform = core.Matrix3D.create()
        transform.setWithCoordinateSystem(
            point((x, AXE_SERVO, z)), vector((-1, 0, 0)),
            vector((0, 0, 1)), vector((0, 1, 0)),
        )
        return transform

    def servo_holes(self):
        # Passage du boîtier et perçages indicatifs pour les deux pattes.
        return [
            self.box(-6.05, 17.45, -6.45, 6.45, -12, 0.1),
            self.box(-11, 22.4, -6.45, 6.45, -32, -10),
            *(self.hole_z(x, 0, -13, -6.3, 1.05) for x in VIS_SERVO),
        ]

    def servo_mount(self):
        return self.rounded(-11.7, 23.6, -9, 9, -10, -7.2, 2.5)

    def servo(self):
        case = self.rounded(-5.7, 17.1, -6.1, 6.1, -30.8, -5.4, 0.9)
        self.union(case,
                   self.rounded(-10.6, 22, -6.1, 6.1, -12.1, -10, 0.8),
                   self.hole_z(0, 0, -5.7, -1.5, 5.2),
                   self.hole_z(0, 0, -1.7, -0.08, 2.35))
        for x in VIS_SERVO:
            self.cut(case, self.hole_z(x, 0, -13, -9.8, 1.1))
        return case

    def horn(self):
        body = self.rounded(-8.8, 8.8, -2.7, 2.7, 0, 1.7, 1.6)
        self.union(body, self.hole_z(0, 0, 0, 1.7, 3.6))
        for x in (-5.8, 5.8):
            self.cut(body, self.hole_z(x, 0, -0.1, 1.8, 0.85))
        return self.cut(body, self.hole_z(0, 0, -0.1, 1.8, 1.05))

    def base(self):
        body = self.rounded(-65, 61, -50, 50, 0, 4, 8)
        for x in (-54, 51):
            for y in (-40, 40):
                self.cut(body, self.hole_z(x, y, -1, 5, 2.2))
        for x in FIXATIONS_SOCLE:
            self.cut(body, self.hole_z(x, 0, -1, 5, 1.7),
                     self.cyl((x, 0, -0.1), (x, 0, 2.65), 3.25, 1.7))
        # Saddle points hold the Nano with a light cable tie across its short side.
        for y in (-18, 18):
            for x in (-53, -39):
                self.union(body, self.hole_z(x, y, 3.7, 8.7, 1.8))
        for x in (-57.8, -34.2):
            self.cut(body, self.rounded(x-1.05, x+1.05, -3.6, 3.6, -1, 5, 0.7))
        self.cut(body, self.hole_z(43, -28, -1, 5, 6.15))
        # A passage toward the central servo remains open at the underside.
        return self.cut(body, self.rounded(-33, -24, -13, -5, 2, 5, 1.8))

    def pod(self):
        height = 32.25
        body = self.cyl((0, 0, 0), (0, 0, height), 29, 23.8)
        self.cut(body, self.cyl((0, 0, -0.2), (0, 0, 24.3), 25.6, 20.6),
                 self.hole_z(0, 0, 25.7, height + 0.2, 12.35))
        pose = frame((0, 0, 30.9))
        # The removable pod carries the motor. Its annular top supports yaw.
        self.union(body, self.place(self.servo_mount(), pose))
        for x in FIXATIONS_SOCLE:
            self.union(body, self.hole_z(x, 0, 0, 5, 4))
            self.cut(body, self.hole_z(x, 0, -0.2, 4.5, 1.35))
        self.cut(body,
                 self.box(-31, -21.7, -12.8, -5.1, -1, 7),
                 self.box(-28, -16, 8.5, 15, 24.7, 30.4))
        for cutter in self.servo_holes():
            self.cut(body, self.place(cutter, pose))
        return body

    def turret(self):
        shoulder = HAUTEUR_EPAULE
        dish = self.cyl((0, 0, 0), (0, 0, 3.5), 22.7, 21.4)
        sleeve = self.cut(self.hole_z(0, 0, -4, 0.4, 12),
                          self.hole_z(0, 0, -4.2, 0.15, 9.35))
        self.union(dish, sleeve)
        # Shoulder bracket with one mounting plate and the passive cheek opposite.
        pose = self.servo_lat(0, shoulder)
        self.union(
            dish, self.side(-25, -19, 1.8, shoulder, -21, -17.2, 1.8),
            self.side(-10.5, 10.5, 2, shoulder + 8.6, 11.55, 15.6, 4.5),
            self.side(-19.5, -9, 2.3, 13, -20, -10.4, 2.2),
            self.place(self.servo_mount(), pose),
        )
        self.cut(dish, self.hole_y(0, shoulder, 11.35, 15.8, 1.68),
                 self.hole_z(0, 0, -0.2, 4, 2.3),
                 self.hole_z(0, 13.4, -0.15, 3.7, 1.7))
        for x in (-5.8, 5.8):
            self.cut(dish, self.hole_z(x, 0, -0.2, 4, 1.22))
        for cutter in self.servo_holes():
            self.cut(dish, self.place(cutter, pose))
        return dish

    def proximal(self, length):
        body = self.side(-6.8, length - 11, -6.7, 6.7, -7.8, 7.8, 4.4)
        self.union(body,
                   self.hole_y(0, 0, -9.1, -5.6, 9.1),
                   self.hole_y(0, 0, 5.6, 11.1, 8.5))
        self.cut(body,
                 self.rounded(9.5, length-13, -5, 5, -4.25, 7.1, 2.2),
                 self.hole_y(0, 0, -9.2, 11.25, 1.68))
        # Two clearance slots accept the original horn arms after bench fitting.
        for x in (-5.8, 5.8):
            self.cut(body, self.side(x-1.75, x+1.75, -1.15, 1.15, -9.3, -4.35, 0.85))
        self.cut(body, self.side(-8, 8, -4.1, 4.1, -5.2, -2.95, 1.4))
        return body

    def arm(self):
        length = LONGUEURS[0]
        body = self.proximal(length)
        pose = self.servo_lat(length)
        self.union(body, self.place(self.servo_mount(), pose),
                   self.side(length-27.2, length-20.6, -8, 5.7, -20.7, -7.1, 2.2),
                   self.side(length-25, length-18, -6, 5.7, 7, 13.2, 2.1),
                   self.side(length-24, length+8.8, -8.2, 8.2, 11.55, 15.6, 4.6))
        self.cut(body, self.hole_y(length, 0, 11.3, 15.8, 1.68),
                 self.rounded(29, 36, -2.5, 2.5, -6.9, -3.9, 1.2))
        for cutter in self.servo_holes():
            self.cut(body, self.place(cutter, pose))
        return self.lid_holes(body, length)

    def lid_holes(self, body, length):
        for x, y in ((11.4, 5.8), (length-18.2, -5.8)):
            self.cut(body, self.hole_z(x, y, 3.6, 7, 0.85))
        return body

    def lid(self, length):
        body = self.rounded(8.6, length-14.5, -7.65, 7.65, 6.7, 8.35, 2.5)
        for x, y in ((11.4, 5.8), (length-18.2, -5.8)):
            self.cut(body, self.hole_z(x, y, 6.6, 8.5, 1.1))
        return body

    def socket_tools(self):
        return [
            self.box(-8.45, 0.2, -4.28, 4.28, -3.0, 3.0),
            self.hole_z(-4.7, 0, -25, 25, 1.65),
        ]

    def insert(self):
        return self.rounded(-8.05, 2.9, -3.95, 3.95, -2.72, 2.72, 1)

    def forearm(self):
        length = LONGUEURS[1]
        body = self.proximal(length)
        end = frame((length, 0, 0), pitch=ANGLES_REPOS[2])
        self.union(body, self.side(length-13.9, length+5.6, -8.7, 8.8, -8.3, 8.3, 4.8))
        for tool in [self.box(0, 50, -40, 40, -30, 30), *self.socket_tools()]:
            self.cut(body, self.place(tool, end))
        return self.lid_holes(body, length)

    def wrist_frame(self):
        return frame((LONGUEURS[2], 0, 0), pitch=ANGLE_POIGNET)

    def terminal(self):
        length = LONGUEURS[2]
        body = self.side(0.32, length-0.5, -7.2, 7, -7.3, 7.3, 3.6)
        self.union(body, self.insert(),
                   self.side(1.2, 12, -9.4, 9, -8.25, 8.25, 3.6),
                   self.side(length-13, length+3.6, -7.9, 7.9, -9.4, 9.4, 4.2))
        self.cut(body, self.hole_z(-4.7, 0, -4, 4, 1.65),
                 self.rounded(11, length-11, -4.9, 4.9, -4.2, 7.3, 1.8))
        for tool in [self.box(0, 50, -40, 40, -30, 30), *self.socket_tools()]:
            self.cut(body, self.place(tool, self.wrist_frame()))
        return body

    def hand(self):
        palm = self.rounded(1.1, 33.8, -19, 19, -3.5, 3.5, 5.6)
        self.union(palm, self.insert(),
                   self.rounded(0.34, 12, -6.4, 6.4, -3.5, 3.5, 2.5))
        self.cut(palm, self.hole_z(-4.7, 0, -4, 4, 1.65))
        for start, yaw, width, lengths in (
            ((10.8, -14, 0), -51, 8.5, (10, 8, 8)),
            ((31, -13.7, 0), -3, 8, (13.5, 9.4, 8.4)),
            ((32, -4.7, 0), 0, 8.3, (15.1, 10.3, 8.6)),
            ((32, 4.8, 0), 2, 7.6, (13.5, 9.3, 8.1)),
            ((29.2, 13.5, 0), 6, 7.1, (11.2, 8, 7.9)),
        ):
            pose = frame(start, yaw=yaw)
            run = 0
            for i, length in enumerate(lengths):
                half = width/2 - i*0.35
                segment = self.rounded(run-1.1, run+length-0.35, -half, half,
                                       -3.5, 3.5 - i*0.25, 2)
                if i < 2:
                    neck = self.rounded(run+length-2.5, run+length+1.3, -half+0.95,
                                        half-0.95, -3.5, 0.9, 1.05)
                    self.union(segment, neck)
                self.union(palm, self.place(segment, pose))
                run += length
        return palm

    def pin(self):
        return self.union(self.hole_y(0, 0, 6.6, 16.2, 1.48),
                          self.hole_y(0, 0, 15.6, 16.5, 3.15),
                          self.hole_y(0, 0, 16.35, 18.25, 2.7))

    def nano(self):
        board = self.rounded(-9, 9, -22.5, 22.5, 0, 1.6, 1.15)
        usb = self.box(-3.8, 3.8, 17.8, 23.2, 1.6, 4.55)
        chip = self.box(-3, 3, -4.8, 1.2, 1.6, 2.9)
        return board, usb, chip
