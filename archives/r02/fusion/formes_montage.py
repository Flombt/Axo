"""Géométrie r02. Les cotes et les jeux sont en millimètres."""

from math import sqrt

import adsk.fusion as fusion

from formes_articulees import ArticulatedForms, DRUM, MOTOR_H
from geometrie import frame
from geometrie_table import LONGUEURS, VIS_SERVO


ROW_X = 51.5
ROW_Y = (-18.6, -6.2, 6.2, 18.6)
AXLE_HALF = 23.78
JOINT_HALF = 4.65
TONGUE_HALF = 2.02
FORK_INSIDE = 2.56
AXIS_R = 1.20
THUMB = (25.7, -32.35, -0.48)
THUMB_YAW, THUMB_ROLL = -51, 18
THUMB_FIX = ((19.7, -19.55), (32.2, -19.55))
THUMB_GUIDE = (53.12, -27.04)
CAP_BOLTS = tuple((y, z) for y in (-10.35, 10.35) for z in (-7.60, 7.60))
HUB_BOLTS = ((10.25, -3.1), (10.25, 3.1))
FINGERS = (
    ("P", "Pouce", THUMB, THUMB_YAW, THUMB_ROLL, (14, 12.5, 11), (31, 37, 34)),
    ("I", "Index", (ROW_X, ROW_Y[0], 0), 0, 0, (16, 14, 12.5), (37, 45, 39)),
    ("M", "Majeur", (ROW_X, ROW_Y[1], 0), 0, 0, (16, 14, 12.5), (38, 46, 40)),
    ("A", "Annulaire", (ROW_X, ROW_Y[2], 0), 0, 0, (16, 14, 12.5), (37, 45, 39)),
    ("U", "Auriculaire", (ROW_X, ROW_Y[3], 0), 0, 0, (14, 12.5, 11), (34, 42, 37)),
)


class WorkshopForms(ArticulatedForms):
    def tear_y(self, x, z, low, high, radius):
        # A pointed roof above the working circle keeps supports out of the hole.
        half = radius * 1.46 / sqrt(2)
        diamond = self.place(self.box(-half, half, low, high, -half, half),
                             frame((x, 0, z), pitch=45))
        roof = self.box(x-3*radius, x+3*radius, low-0.1, high+0.1,
                        z+0.76*radius, z+2*radius)
        self.op(diamond, roof, fusion.BooleanTypes.IntersectionBooleanType)
        return self.union(self.hole_y(x, z, low, high, radius), diamond)

    def fork_blocks(self, x):
        result = []
        for k in (-1, 1):
            y0, y1 = sorted((k*FORK_INSIDE, k*JOINT_HALF))
            result.extend((self.hole_y(x, 0, y0, y1, 4.05),
                           self.side(x-6.65, x-0.05, -3.5, 3.5, y0, y1, 1.3)))
        return result

    def captive_y(self, x, z=0):
        # M2 nut inserted from the outside, with two flats preventing rotation.
        return self.box(x-2.53, x+2.53, 2.82, JOINT_HALF+0.25, z-2.24, z+2.24)

    def phalanx(self, length, tip):
        last = length if tip else length-4.72
        body = self.side(5.2, last, -3.54, 3.45, -4.20, 4.20, 1.05)
        self.union(body, self.hole_y(0, 0, -TONGUE_HALF, TONGUE_HALF, 3.37),
                   self.side(2.04, 6.27, -3.31, 3.12, -TONGUE_HALF, TONGUE_HALF, 1.06))
        self.cut(body, self.tear_y(0, 0, -2.25, 2.25, AXIS_R))
        if not tip:
            self.union(body, *self.fork_blocks(length))
            self.cut(body, self.tear_y(length, 0, -5.0, 5.0, AXIS_R),
                     self.captive_y(length))
        # A straight, short eye to thread the cord before routing the next link.
        self.cut(body, self.axial(1.7, length+0.25, 0.72, z=-1.93))
        self.cut(body, self.rounded(1.53, 4.52, -0.97, 0.97, -4.35, -1.56, 0.69))
        if tip:
            self.cut(body, self.hole_y(length-2.2, -1.9, -4.65, 4.65, 0.95),
                     self.hole_y(length-2.2, 1.75, -4.65, 4.65, 0.93))
        else:
            self.cut(body, self.axial(2.56, length+0.2, 0.76, z=1.9),
                     self.rounded(2.39, 4.66, -0.99, 0.99, 1.51, 4.39, 0.62))
        # One datum on both the fork and the eye, in the palmar print orientation.
        return self.cut(body, self.box(-8, length+6, -6, 6, -6, -3.23))

    def thumb_frame(self):
        return frame(THUMB, yaw=THUMB_YAW, roll=THUMB_ROLL)

    def thumb_bracket(self):
        flange = self.rounded(14.55, 36.25, -27.25, -17.58, -4.70, -1.45, 2.15)
        neck = self.side(-13.6, -4.78, -3.9, 3.65, -JOINT_HALF, JOINT_HALF, 1.56)
        self.union(neck, *self.fork_blocks(0))
        self.cut(neck, self.tear_y(0, 0, -5.0, 5.0, AXIS_R), self.captive_y(0),
                 self.axial(-13.8, -4.52, 0.85, z=-1.98))
        self.union(flange, self.place(neck, self.thumb_frame()))
        # Leave an unmistakable seam around the removable bracket.
        self.cut(flange, self.box(11, 42, -25.73, -13, -1.45, 9.5))
        for tool in (
            self.box(-4.4, 12.3, -2.54, 2.54, -9.7, 8.7),
            self.box(4.11, 14, -5.1, 5.1, -9.8, 8),
            self.box(-0.8, 4.27, -4.4, 4.4, -10, -3.91),
            self.tear_y(0, 0, -5.5, 5.5, AXIS_R),
            self.hole_y(0, 0, -11, -4.66, 2.12),
            self.captive_y(0),
            self.axial(-14.0, -4.21, 0.85, z=-1.98),
            self.box(-14.4, -10.9, -1.14, 1.14, -8.6, -1.67),
        ):
            self.cut(flange, self.place(tool, self.thumb_frame()))
        for x, y in THUMB_FIX:
            self.cut(flange, self.hole_z(x, y, -5.1, -1.15, 1.18))
        return self.cut(flange, self.box(0, 42, -43, -14, -10, -4.70))

    def palm(self):
        body = self.rounded(6, 51.15, -25.20, 25.20, -4.62, 4.68, 7.2)
        self.union(body, self.rounded(5.86, 17.3, -10.5, 10.5, -4.62, 4.68, 2.45))
        # A keyed socket clears the bearing body. The whole dorsal face lies flat.
        self.cut(body, self.box(5.72, 13.95, -4.55, 4.55, -2.4, 2.4),
                 self.axial(5.7, 55.2, 2.15),
                 self.rounded(19, 43.3, -16.1, 3.15, -4.78, 1.25, 3),
                 self.rounded(27.5, 45, 8.3, 16.7, -4.78, 1.25, 2.6))
        for x, y in HUB_BOLTS:
            self.cut(body, self.hole_z(x, y, 2.25, 5.05, 1.18))

        motor = self.hand_servo_frame()
        self.union(body, self.place(self.servo_mount(), motor))
        for tool in self.servo_holes():
            self.cut(body, self.place(tool, motor))
        self.cut(body, self.box(10.68, 34.6, -18.1, 10.1, -17.3, -4.14))

        for k in (-1, 1):
            y0, y1 = sorted((k*17.65, k*21.5))
            self.union(body, self.side(37.1, 51.9, -11.74, -3.92, y0, y1, 1.3))
            self.cut(body, self.hole_z(50.76, k*19.8, -12.05, -4.1, 0.86))
        self.cut(body, self.box(37.4, 52.07, -20.73, 20.73, -10.38, -7.29))

        # Four coaxial fingers share an actual shaft, inserted from the thumb side.
        for y in ROW_Y:
            self.cut(body, self.box(ROW_X-4.11, ROW_X+10.0, y-4.84, y+4.84, -11.3, 9.1))
        for y in ROW_Y:
            rt = frame((ROW_X, y, 0))
            neck = self.side(-12.65, -4.82, -4.13, 4.1, -JOINT_HALF, JOINT_HALF, 1.38)
            self.union(neck, *self.fork_blocks(0))
            guide = self.axial(-9.65, -5.5, 1.49, z=-3.36)
            self.union(neck, guide)
            self.union(body, self.place(neck, rt))
            self.cut(body, self.place(self.axial(-11.55, -3.69, 0.85, z=-3.36), rt),
                     self.place(self.box(-11.89, -9.36, -0.99, 0.99, -13.2, -2.97), rt))
            for delta in (-1.85, 1.85):
                self.cut(body, self.hole_z(ROW_X-10.6, y+delta, -5.6, 5.05, 0.91))
        self.cut(body, self.tear_y(ROW_X, 0, -28, 28, AXIS_R),
                 self.box(45.25, 64.0, -29, -23.62, -6.9, 7.1),
                 self.box(45.25, 64.0, 23.62, 29, -6.9, 7.1))
        for y0, y1 in ((-24.5, -17.25), (17.25, 24.5)):
            self.cut(body, self.hole_y(ROW_X-3.15, 0, y0, y1, 0.90))

        # The thumb slides under the edge of the palm and is screwed on last.
        self.cut(body, self.box(13.18, 36.72, -26.45, -17.26, -5.10, -1.05))
        for x, y in THUMB_FIX:
            self.cut(body, self.hole_z(x, y, -5.1, 4.92, 1.18),
                     self.box(x-2.53, x+2.53, y-2.24, y+2.24, 2.72, 4.95))
        # Lacing openings lead to free air on both sides.
        for x in (14.9, 18.0):
            self.cut(body, self.hole_z(x, -22.10, -5.5, 5.2, 0.96))
        # A forward fixed guide reverses the thumb cord before it runs to the bracket.
        x, y = THUMB_GUIDE
        self.union(body, self.rounded(45.85, 54.2, -28.7, -22.08, -6.47, -3.31, 1.4),
                   self.hole_z(x, y, -6.47, -3.34, 3.23))
        self.cut(body, self.hole_z(x, y, -6.67, -3.26, 1.27))
        return self.cut(body, self.hole_y(DRUM[0], DRUM[2], 16.20, 22.85, 8.03),
                        self.hole_y(MOTOR_H[0], MOTOR_H[2], 14.35, 16.23, 9.42),
                        self.box(6.04, 39.54, -30.4, 4.46, -17.46, -4.00),
                        self.box(3.8, 5.83, -11.0, 11.0, -30, 20),
                        self.box(5.66, 14.05, -4.65, 4.65, -2.51, 2.51))

    def wrist_hub(self):
        sleeve = self.cut(self.axial(-3.25, 0.95, 9.67),
                          self.axial(-3.51, 0.44, 7.49))
        self.union(sleeve, self.axial(0.69, 5.51, 9.68),
                   self.rounded(5.27, 13.45, -4.18, 4.18, -2.05, 2.05, 1.09))
        self.cut(sleeve, self.axial(-0.16, 1.86, 9.25), self.axial(1.52, 14, 2.18))
        for z in (-5.8, 5.8):
            self.cut(sleeve, self.axial(1.60, 5.23, 0.86, z=z))
        for x, y in HUB_BOLTS:
            self.cut(sleeve, self.hole_z(x, y, -2.2, 2.16, 0.87))
        return sleeve

    def wrist_flange(self):
        body = self.axial(-8.32, -0.36, 15.48)
        servo = self.wrist_servo_frame()
        self.union(body, self.place(self.servo_mount(), servo))
        for tool in self.servo_holes():
            self.cut(body, self.place(tool, servo))
        self.cut(body, self.axial(-3.67, 0.2, 10.15))
        for y, z in CAP_BOLTS:
            self.cut(body, self.axial(-9, 0.12, 1.18, y, z),
                     self.axial(-2.04, 0.1, 2.12, y, z))
        return body

    def inside_wrist(self):
        length = LONGUEURS[2]
        wrist = self.wrist_frame()
        body = self.side(0.32, length-14, -6.55, 6.42, -7.68, 7.68, 3.72)
        self.union(body, self.insert(), self.side(1.4, 11.8, -9.2, 8.5, -8.25, 8.25, 3.5))
        self.cut(body, self.hole_z(-4.7, 0, -3.7, 3.7, 1.65))
        rails = self.side(-34.3, -8.53, -9.4, 8.42, -12.42, -6.94, 2.1)
        self.union(rails, self.side(-34.3, -8.53, -9.4, 8.42, 6.94, 12.42, 2.1),
                   self.rounded(-34.3, -15, -10.6, 10.6, 6.9, 8.42, 2.4))
        for y, z in CAP_BOLTS:
            self.union(rails, self.axial(-16, -8.53, 2.67, y, z))
            self.cut(rails, self.axial(-16.28, -8.36, 0.92, y, z))
        self.union(body, self.place(rails, wrist))
        # The servo and its removable face enter along X from the front.
        self.cut(body, self.place(self.box(-31.7, 0.15, -6.48, 6.48, -18.2, 6.23), wrist),
                 self.place(self.box(-12.6, 0.15, -6.48, 6.48, -22.5, 11.08), wrist),
                 self.place(self.box(-10.25, -8.30, -9.34, 9.34, -24.25, 12.05), wrist))
        return body

    def proximal(self, length):
        body = super().proximal(length)
        return self.cut(body, self.box(-3.47, 3.47, 3.05, 6.02, -3.06, 7.12),
                        self.tear_y(0, 0, 2.58, 11.38, 1.76))

    def servo_holes(self):
        passages = super().servo_holes()[:2]
        return passages+[self.hole_z(x, 0, -13, -6.3, 0.92) for x in VIS_SERVO]

    def drum(self):
        spool = self.hole_y(0, 0, 0, 6.05, 6)
        self.union(spool,
                   self.hole_y(0, 0, 0, 0.62, 7.24),
                   self.cyl((0,0.58,0), (0,1.95,0), 7.24, 6),
                   self.cyl((0,4.09,0), (0,5.52,0), 6, 7.24),
                   self.hole_y(0,0,5.47,6.05,7.24))
        for x,r in ((-5.8,1.05),(0,1.29),(5.8,1.05)):
            self.cut(spool, self.hole_y(x,0,-0.16,6.25,r))
        return self.cut(spool,self.axial(1.6,8,0.86,y=3.1,z=1.7))

    def pin(self):
        return self.union(super().pin(), self.hole_y(0, 0, 2.34, 6.85, 1.47))

    def turret_large(self):
        return self.cut(super().turret_large(),
                        self.tear_y(0, 27, 11.25, 15.9, 1.75))

    def arm(self):
        return self.cut(super().arm(),
                        self.tear_y(LONGUEURS[0], 0, 11.25, 15.9, 1.75))

    def coupon(self):
        strip = self.rounded(0, 38, -5.6, 5.6, 0, 2.9, 1.8)
        for x, r in zip((6,12.5,19,25.5,32), (1.05,1.125,1.20,1.275,1.35)):
            self.cut(strip, self.hole_z(x, 0, -0.2, 3.1, r))
        return strip
