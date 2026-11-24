"""Implantation de la main à tendons et de son poignet dans le bras V3 de table."""

import adsk.core as core

from geometrie import frame, point, vector
from geometrie_table import AXE_SERVO, FIXATIONS_SOCLE, Formes, HAUTEUR_EPAULE, LONGUEURS


DIGITS = (
    ("P", "Pouce", (25, -21.1, 0), -51, 29, (14, 12, 11), (31, 38, 35)),
    ("I", "Index", (51, -16.5, 0), -4, 0, (16, 14, 12.5), (38, 48, 40)),
    ("M", "Majeur", (52.5, -5.55, 0), 0, 0, (16, 14, 12.5), (38, 48, 40)),
    ("A", "Annulaire", (50.4, 5.55, 0), 3, 0, (16, 14, 12.5), (38, 48, 40)),
    ("U", "Auriculaire", (46.4, 16.5, 0), 7, 0, (16, 14, 12.5), (36, 45, 38)),
)
WIND = 72
COURSE = 7.5
CURSOR = (48.4, 0, -8.8)
DRUM = (17, 16.23, -10.65)
MOTOR_H = (17, 14.5, -10.65)
FLEX_RADIUS = 3.05
MOUNT_LARGE = (-13.2, 35.5)


class ArticulatedForms(Formes):
    def axial(self, lo, hi, radius, y=0, z=0):
        return self.cyl((lo, y, z), (hi, y, z), radius)

    def oriented(self, at, x, y, z):
        transform = core.Matrix3D.create()
        transform.setWithCoordinateSystem(point(at), vector(x), vector(y), vector(z))
        return transform

    def manual_pod(self):
        height = 32.25
        body = self.cyl((0, 0, 0), (0, 0, height), 29, 23.8)
        self.cut(body, self.cyl((0, 0, -0.3), (0, 0, 25.2), 25.6, 20.8),
                 self.hole_z(0, 0, 28.25, 32.5, 12.35),
                 self.hole_z(0, 0, 24.9, 32.45, 2.2))
        for x in FIXATIONS_SOCLE:
            self.union(body, self.hole_z(x, 0, 0, 5, 4))
            self.cut(body, self.hole_z(x, 0, -0.2, 4.75, 1.35))
        return self.cut(body, self.box(-31, -21, -12.8, -5, -1, 7))

    def large_servo(self):
        body = self.rounded(-9.5, 31.2, -9.85, 9.85, -45.1, -5.4, 1.45)
        self.union(body, self.rounded(-15.4, 39.4, -9.85, 9.85, -17, -14.5, 1.2),
                   self.hole_z(0, 0, -6, -1.4, 6.1),
                   self.hole_z(0, 0, -1.65, -0.08, 2.95))
        for x in MOUNT_LARGE:
            for y in (-5.1, 5.1):
                self.cut(body, self.hole_z(x, y, -17.2, -14.25, 1.4))
        return body

    def turret_large(self):
        shoulder = HAUTEUR_EPAULE
        body = self.cyl((0, 0, 0), (0, 0, 3.6), 22.7, 21.4)
        self.union(body, self.hole_z(0, 0, -4, 0.35, 12),
                   self.side(-10.5, 10.5, 2, shoulder+8.6, 11.55, 15.6, 4.5),
                   self.side(-37, -12, 1.7, 9.4, -26.2, -10, 3.0),
                   self.side(-38, -33, 5.1, shoulder-1.7, -26.25, -21.1, 2.0))
        mount = self.rounded(-17.2, 41.2, -13, 13, -14.5, -11, 3.0)
        servo = self.servo_lat(0, shoulder)
        self.union(body, self.place(mount, servo))
        for tool in [
            self.box(-9.9, 31.6, -10.25, 10.25, -18.1, 0.1),
            self.box(-15.75, 39.75, -10.25, 10.25, -46, -14.5),
            *(self.hole_z(x, y, -17.2, -10.7, 1.32)
              for x in MOUNT_LARGE for y in (-5.1, 5.1)),
        ]:
            self.cut(body, self.place(tool, servo))
        return self.cut(body, self.hole_z(0, 0, -4.3, 4.25, 2.18),
                        self.hole_z(0, 13.5, -0.1, 4, 1.7),
                        self.hole_y(0, shoulder, 11.3, 15.8, 1.68))

    def wrist_servo_frame(self):
        return self.oriented((0, 0, 0), (0, 0, -1), (0, 1, 0), (1, 0, 0))

    def inside_wrist(self):
        length = LONGUEURS[2]
        wrist = self.wrist_frame()
        body = self.side(0.32, length-9.2, -6.4, 6.4, -7.7, 7.7, 3.9)
        self.union(body, self.insert(), self.side(1.4, 12, -9.3, 8.9, -8.2, 8.2, 3.6))
        self.cut(body, self.hole_z(-4.7, 0, -3.6, 3.6, 1.65))
        module = self.axial(-8.3, -0.28, 12.4)
        self.union(module,
                   self.side(-32.1, -3.8, -8.2, 6.45, -10.45, -6.55, 3.5),
                   self.side(-32.1, -3.8, -8.2, 6.45, 6.55, 10.45, 3.5),
                   self.place(self.servo_mount(), self.wrist_servo_frame()))
        self.cut(module, self.axial(-3.6, 0.2, 10.05),
                 self.box(-32.4, -12.7, -3.7, 3.7, -10.2, -4.4))
        for tool in self.servo_holes():
            self.cut(module, self.place(tool, self.wrist_servo_frame()))
        self.union(body, self.place(module, wrist))
        # The housing installs from below between these two rails.
        for tool in (self.box(-34, -10, -6.45, 6.45, -20, 6.15),
                     self.box(-34, -8.2, -6.45, 6.45, -20, -1.1)):
            self.cut(body, self.place(tool, wrist))
        for tool in self.servo_holes():
            self.cut(body, self.place(self.place(tool, self.wrist_servo_frame()), wrist))
        return body

    def hand_servo_frame(self):
        return self.oriented(MOTOR_H, (1, 0, 0), (0, 0, -1), (0, 1, 0))

    def fork(self, length, wide):
        pieces = []
        for sign in (-1, 1):
            y0, y1 = sorted((sign*2.3, sign*wide))
            pieces.extend((
                self.hole_y(length, 0, y0, y1, 3.45),
                self.side(length-6.15, length+0.1, -3.1, 3.1, y0, y1, 1.3),
            ))
        return pieces

    def phalanx(self, length, tip):
        half = 4.2
        back = self.side(4.3, length if tip else length-4.8, -4.05, 3.45, -half, half, 1.22)
        tongue = self.hole_y(0, 0, -2.03, 2.03, 3.34)
        self.union(back, tongue, self.side(2.1, 5.65, -3.2, 3.2, -2.03, 2.03, 0.95))
        self.cut(back, self.hole_y(0, 0, -2.39, 2.39, 1.09))
        if not tip:
            self.union(back, *self.fork(length, half))
            self.cut(back, self.hole_y(length, 0, -4.45, 4.45, 1.09))
        self.cut(back, self.axial(2.6, length-0.2 if tip else length-4, 0.72, z=-2.66))
        if tip:
            self.cut(back, self.hole_y(length-2.15, -2.6, -4.4, 4.4, 0.88),
                     self.hole_y(length-2.2, 1.6, -4.4, 4.4, 0.86))
        else:
            self.cut(back, self.axial(3.0, length-4.1, 0.72, z=2.0))
        return back

    def palm(self):
        body = self.rounded(6, 51, -22.35, 22.35, -4.55, 4.5, 7.7)
        # Axial collar with radial support, plus the seat of the original horn.
        sleeve = self.cut(self.axial(-3.25, 0.95, 9.68),
                          self.axial(-3.5, 0.45, 7.45))
        driver = self.axial(1.7, 5.4, 9.7)
        self.union(body, driver, sleeve, self.axial(0.69, 2.14, 9.68),
                   self.side(4, 13.4, -6.8, 6.6, -10, 10, 3.1))
        # The driver reaches the central screw from the distal end of the palm.
        self.cut(body, self.axial(-0.15, 1.7, 9.25), self.axial(1.65, 54.5, 2.05))
        for z in (-5.8, 5.8):
            self.cut(body, self.axial(1.65, 5.5, 0.83, z=z))
        self.cut(body, self.rounded(19, 42, -16.6, 3.3, -4.68, 1.35, 3),
                 self.rounded(27.5, 44, 8.3, 16.7, -4.68, 1.35, 2.6))

        # Servo saddle, held at the underside of the white palm.
        mounting = self.hand_servo_frame()
        self.union(body, self.place(self.servo_mount(), mounting))
        for tool in self.servo_holes():
            self.cut(body, self.place(tool, mounting))
        self.cut(body, self.box(10.85, 34.5, -17.2, 9.5, -5.0, -3.95))

        # A printed rail pair guides the equaliser, which stays accessible from the palm.
        for sign in (-1, 1):
            ya, yb = sorted((sign*17.65, sign*21.5))
            rail = self.side(37.1, 51.9, -11.72, -3.9, ya, yb, 1.3)
            self.union(body, rail)
            self.cut(body, self.hole_z(50.76, sign*19.8, -12.05, -4.1, 0.86))
        self.cut(body, self.box(37.45, 52.15, -20.65, 20.65, -10.28, -7.32))

        for _, _, start, yaw, roll, _, _ in DIGITS:
            relief = self.box(-3.65, 12.4, -4.85, 4.85, -9.55, 9.3)
            self.cut(body, self.place(relief, frame(start, yaw=yaw, roll=roll)))

        for _, _, start, yaw, roll, _, _ in DIGITS:
            transform = frame(start, yaw=yaw, roll=roll)
            y = 4.3
            # Forkes are built on protruding palm lobes with stress-distributing roots.
            root = self.side(-13, -4.75, -4.25, 4.35, -y, y, 1.7)
            self.union(root, *self.fork(0, y))
            guide = self.cut(self.axial(-9.2, -4.1, 1.65, z=-3.55),
                             self.axial(-9.4, -3.9, 0.83, z=-3.55))
            self.union(root, guide)
            self.union(body, self.place(root, transform))
            self.cut(body, self.place(self.hole_y(0, 0, -4.6, 4.6, 1.09), transform),
                     self.place(self.box(-4.12, 1, -2.28, 2.28, -4.15, 4.15), transform),
                     self.place(self.axial(-10.2, -3.85, 0.82, z=-3.55), transform),
                     self.place(self.hole_y(-10.7, 3.15, -4.3, 4.3, 0.76), transform))
            for y in (-1.85, 1.85):
                self.cut(body, self.place(self.hole_z(-10.7, y, -7.5, 7.7, 0.79), transform))
        return self.cut(body,
                        self.box(10.72, 34.52, -17.2, 10, -17.2, -4.21),
                        self.hole_y(DRUM[0], DRUM[2], 16.21, 22.77, 7.95),
                        self.hole_y(MOTOR_H[0], MOTOR_H[2], 14.38, 16.22, 9.31))

    def drum(self):
        end = self.hole_y(0, 0, 0, 6.05, 6.0)
        self.union(end, self.hole_y(0, 0, 0, 1.25, 7.55),
                   self.hole_y(0, 0, 4.68, 6.05, 7.55))
        self.cut(end, self.hole_y(0, 0, -0.16, 6.25, 1.29))
        for x in (-5.8, 5.8):
            self.cut(end, self.hole_y(x, 0, -0.14, 6.2, 1.05))
        return self.cut(end, self.axial(1.6, 8, 0.86, y=3.1, z=1.7))

    def cursor(self):
        slider = self.rounded(-1.25, 1.25, -20.23, 20.23, -1.13, 1.13, 0.69)
        for y in (-16.8, -11.0, -4.2, 4.2, 12, 17.9):
            self.cut(slider, self.axial(-1.45, 1.45, 0.67, y=y))
        return slider
