"""Formes de la révision AURA-009 de table r03, cotes en millimètres."""

import math

from formes_montage import WorkshopForms
from formes_articulees import CURSOR, MOUNT_LARGE
from geometrie import frame
from geometrie_table import ANGLES_REPOS, LONGUEURS


BASE_X = (-64, 116)
ANCHOR_X = (-52, 104)
ANCHOR_Y = (-60, 60)
J1_Z = 37
J2_Z = 45
J3_X = LONGUEURS[0]
BRANCH_Y = (-15.0, -7.5, 0.0, 7.5, 15.0)
J2_LIMITS = (-10, 10)
J3_LIMITS = (-10, 14)
J7_LIMITS = (-28, 28)
J2_STOPS = (-14, 14)
J3_STOPS = (-14, 18)
PIVOT_BORE = 3.55
STOP_R = 17.5
WRIST_SHIFT = -8.4
WRIST_BOLTS = tuple((y, z) for y in (-10.35, 10.35) for z in (-7.6, 7.6))


class Geometry(WorkshopForms):
    def ring_y(self, y0, y1, outer, inner, x=0, z=0):
        return self.cut(self.hole_y(x, z, y0, y1, outer),
                        self.hole_y(x, z, y0-.1, y1+.1, inner))

    def ring_x(self, x0, x1, outer, inner, y=0, z=0):
        return self.cut(self.axial(x0, x1, outer, y, z),
                        self.axial(x0-.1, x1+.1, inner, y, z))

    def ring_z(self, z0, z1, outer, inner, x=0, y=0):
        return self.cut(self.hole_z(x, y, z0, z1, outer),
                        self.hole_z(x, y, z0-.1, z1+.1, inner))

    def pedestal(self):
        base = self.hole_z(0, 0, 6, 11.2, 39)
        wall = self.cut(self.cyl((0, 0, 11), (0, 0, 32.4), 34, 28),
                        self.cyl((0, 0, 10.8), (0, 0, 32.6), 28, 23))
        cap = self.hole_z(0, 0, 31.9, 36, 28)
        body = self.union(base, wall, cap)
        for x, y in ((32, 0), (-32, 0), (0, -32), (0, 32)):
            self.cut(body, self.hole_z(x, y, 5.9, 11.4, 2.25))
        for x in (-20, 20):
            for y in (-13, 13):
                self.cut(body, self.hole_z(x, y, 31.8, 36.2, 1.65))
        self.cut(body, self.hole_z(0, 0, 5.9, 36.2, 4.15),self.hole_z(-22,0,31.8,36.2,1.62),
                 self.hole_z(0,0,5.9,11.4,24),
                 self.box(-37, -24, 2, 13, 10, 19))
        return body

    def turret_link(self):
        base = self.hole_z(0, 0, 0, 6, 25.5)
        for side in (-1, 1):
            lo, hi = sorted((side*9.35, side*14.35))
            self.union(base, self.side(-13.4, 12.8, 4, J2_Z+3.2, lo, hi, 3.1),
                       self.hole_y(0, J2_Z, lo, hi, 9.3))
            self.cut(base, self.hole_y(0, J2_Z, lo-.15, hi+.15, PIVOT_BORE))
        self.union(base, self.side(-15, 14, 4, 12.5, -13.9, 13.9, 2.3))
        self.cut(base, self.hole_z(0, 0, -.1, 8.2, 4.25),
                 self.hole_z(0,0,6.03,9.1,7.14))
        for a in (-18, 0, 18):
            r = math.radians(a)
            self.cut(base, self.hole_z(-22*math.cos(r), 22*math.sin(r), -.1, 6.2, 1.62))
        self.axis_shelves(base, 0, J2_Z)
        return base

    def axis_shelves(self, body, x, z):
        for a, b in ((-18.7, -12.7), (12.7, 18.7)):
            shelf = self.side(x-13.5, x+11.7, z-17, z-7.6, a, b, 2.8)
            self.union(body, shelf)
            for dx in (-8, 7.5):
                low, high = (a-.1,-11.9) if a<0 else (11.9,b+.1)
                self.cut(body,self.hole_y(x+dx,z-13.4,low,high,1.65))
        self.cut(body,self.hole_y(x,z,14.36,19,13.13))

    def shaft_hub(self, outer):
        body = self.hole_y(0, 0, -7.9, 7.9, outer)
        self.cut(body, self.hole_y(0, 0, -8.1, 8.1, 2.6),
                 self.hole_z(0, 0, -outer-.1, outer+.1, 1.10))
        return body

    def segment_one(self):
        x = J3_X
        body = self.shaft_hub(9.1)
        self.union(body, self.side(1.5, x-13.0, -6.35, 6.2, -7.9, 7.9, 3.1))
        for side in (-1, 1):
            lo, hi = sorted((side*9.35, side*14.35))
            self.union(body, self.side(x-20.7, x+4, -7.15, 7.15, lo, hi, 3.1),
                       self.hole_y(x, 0, lo, hi, 8.9),
                       self.side(x-22, x-13.5, -6.15, 6.15, min(lo,-1), max(hi,1), 2.2))
            self.cut(body, self.hole_y(x, 0, lo-.1, hi+.1, PIVOT_BORE))
        self.cut(body, self.rounded(8, x-22.5, -4, 4, -2.75, 6.4, 2.2))
        self.cut(body,self.hole_y(0,0,-8.1,8.1,2.6),self.hole_z(0,0,-9.2,9.2,1.1))
        self.axis_shelves(body, x, 0)
        return self.lid_holes(body, x)

    def segment_two(self):
        x = LONGUEURS[1]
        body = self.shaft_hub(8.55)
        self.union(body, self.side(2, x-3, -6.3, 6.2, -7.9, 7.9, 3.1),
                   self.side(x-13.3, x+5.6, -8.6, 8.7, -8.3, 8.3, 4.2))
        end = frame((x, 0, 0), pitch=ANGLES_REPOS[2])
        for tool in [self.box(0, 40, -40, 40, -30, 30), *self.socket_tools()]:
            self.cut(body, self.place(tool, end))
        self.cut(body, self.rounded(8, x-13.5, -4.4, 4.4, -2.65, 6.4, 2.0))
        self.cut(body,self.hole_y(0,0,-8.1,8.1,2.6),self.hole_z(0,0,-8.7,8.7,1.1))
        return self.lid_holes(body, x)

    def bush(self, side):
        barrel = sorted((side*9.34, side*14.35))
        flange = sorted((side*8.35, side*9.35))
        body = self.union(self.hole_y(0, 0, *barrel, 3.50),
                          self.hole_y(0, 0, *flange, 5.5))
        return self.cut(body, self.hole_y(0, 0, -14.5, 14.5, 2.50))

    def shaft(self):
        return self.cut(self.hole_y(0, 0, -25.8, 38.0, 2.5),
                        self.hole_z(0, 0, -2.65, 2.65, 1.0),
                        self.box(-2.6, 2.6, -25.9, -14.92, 1.9, 2.6))

    def drive_collar(self,n,pitch):
        body = self.hole_y(0, 0, -28.25, -15.0, 6.35)
        bore = self.cut(self.hole_y(0, 0, -26.0, -14.9, 2.57),
                        self.box(-3, 3, -26.1, -14.8, 1.95, 3))
        self.cut(body, bore)
        if n == 2:
            for x in (-4.7, 4.7):
                self.cut(body,self.hole_y(x,0,-28.4,-24.6,1.10))
        else:
            self.union(body,self.hole_y(0,0,-28.51,-26.25,8.35))
            for x,z in self.xc_pitch_circle(pitch):
                self.cut(body,self.hole_y(x,z,-28.60,-26.13,1.10))
        self.cut(body,self.hole_y(0,0,-28.6,-26.06,2.01))
        return body

    def xc_pitch_circle(self,pitch):
        angles=[math.radians(a-pitch) for a in (0,90,180,270)]
        return [(6*math.cos(a),6*math.sin(a)) for a in angles]

    def motor_frame(self, n):
        if n == 2:
            return self.oriented((0,-28.55,0), (-1,0,0), (0,0,1), (0,1,0))
        return self.oriented((0,-35.05,0), (0,0,1), (1,0,0), (0,1,0))

    def motor_mount(self, n):
        if n == 2:
            y0 = -43.0
            plate = self.side(-42.0, 19, -15.8, 13.6, y0, y0+4, 2.1)
            self.cut(plate, self.box(-31.65, 9.95, y0-.2, y0+4.2, -10.3, 10.3))
            for x in MOUNT_LARGE:
                for z in (-5.1,5.1):
                    self.cut(plate, self.hole_y(-x, z, y0-.2, y0+4.2, 1.39),
                             self.hole_y(-x, z, y0+2.2, y0+4.2, 2.68))
        else:
            y0 = -52.4
            plate = self.side(-28.6, 13.4, -15.8, 13.6, y0, y0+8, 2.3)
            self.cut(plate, self.box(-24.9, 9.9, y0-.2, y0+8.2, -10.35, 10.35))
            for x in (-26.5,11.6):
                self.cut(plate, self.hole_z(x, y0+4, 8.5, 13.8, 1.12))
        for x in (-8,7.5):
            self.union(plate, self.rounded(x-3.15, x+3.15, y0+.4, -18.75, -15.8, -11.3, 2.25))
            self.cut(plate, self.hole_y(x, -13.4, -28.0, -18.65, 1.66),
                     self.hole_y(x,-13.4,-28.0,-22.17,2.58))
        self.union(plate,self.ring_y(-29.0,-18.87,11.35,8.78))
        for x in (-8,7.5):
            self.union(plate,self.box(x-2.8,x+2.8,-22.08,-19.24,-15.8,-7.12))
            self.cut(plate,self.hole_y(x,-13.4,-22.12,-18.65,1.66))
        if n==2:
            self.cut(plate,self.box(14.95,19.2,y0-.1,y0+4.1,-15.9,-9.6))
        else:
            self.cut(plate,self.box(-28.7,-25.8,y0-.1,y0+8.1,-15.9,-10.65))
        return plate

    def brake_carrier(self):
        # Chape ouverte vers +Y pour introduire la pile de friction et l'axe.
        body = self.ring_y(18.8, 24.7, 15.55, 13.3)
        pad = self.side(-13.05, 11.3, -16.6, -10.4, 18.75, 23.7, 2.1)
        self.union(body, pad)
        for x in (-8,7.5):
            self.cut(body, self.hole_y(x,-13.4,18.6,24.9,1.68),
                     self.hole_y(x,-13.4,23.37,25.5,2.58))
        for lo,hi in ((-16.1,-14.0),(14.0,16.1)):
            self.union(body,self.box(lo,hi,14.45,19.45,-2.65,2.65))
            self.cut(body,self.box(lo+.16,hi-.16,14.38,19.05,-1.92,1.92))
        self.cut(body,self.box(11.85,14.95,14.35,19.02,-1.84,1.84),
                 self.box(-14.95,-11.85,14.35,19.02,-1.84,1.84))
        self.cut(body,self.hole_y(0,0,14.4,19.25,13.15))
        for x in (-13.7,13.7):
            self.union(body, self.side(x-2.4,x+2.4,-5.6,5.6,23.9,29.0,1.15))
            self.cut(body, self.hole_y(x, 0, 24.8, 29.2, 1.3))
        return body

    def stop_angle(self, degrees, target):
        delta = math.degrees(2*math.asin((1.85+1.50)/(2*STOP_R)))
        return math.radians(degrees + target + math.copysign(delta,target))

    def stop_plate(self, pitch, limits):
        plate = self.ring_y(29.0, 36.2, 23, 21.65)
        for x in (-13.7,13.7):
            a,b = sorted((x,math.copysign(22.2,x)))
            self.union(plate,self.box(a,b,29.0,30.5,-3.4,3.4),
                       self.hole_y(x,0,29.0,30.5,3.25))
            self.cut(plate,self.hole_y(x,0,28.9,30.6,1.30))
        for degrees in limits:
            angle = self.stop_angle(pitch,degrees)
            x,z = STOP_R*math.cos(angle), STOP_R*math.sin(angle)
            spoke = self.side(16.8,22.55,-2.25,2.25,29.0,30.5,.6)
            self.union(plate,self.place(spoke,frame(pitch=math.degrees(angle))),
                       self.hole_y(x,z,29.0,30.5,2.25))
            self.cut(plate,self.hole_y(x,z,28.9,30.6,1.58))
        return plate

    def rotor_stop(self):
        body = self.ring_y(34.55, 36.7, 7.5, 2.57)
        self.union(body, self.side(5.4, 19.45, -1.75, 1.75, 34.55, 36.7, 1.2),
                   self.hole_y(STOP_R, 0, 30.75, 36.6, 1.85))
        for z in (-4.45,4.45):
            self.cut(body,self.hole_y(0,z,34.45,36.8,1.05))
        return body

    def brake_disc(self):
        return self.ring_y(15.12,16.88,12.95,2.56)

    def brake_pad(self,y0,y1):
        body = self.ring_y(y0,y1,12.90,5.7)
        return self.union(body,self.box(11.9,14.7,y0,y1,-1.7,1.7),
                          self.box(-14.7,-11.9,y0,y1,-1.7,1.7))

    def wrist_link(self):
        body = self.inside_wrist()
        wrist = self.wrist_frame()
        for tool in (
            self.box(-39.6,-8.48,-7.0,7.0,-18,6.7),
            self.box(-35.5,-8.48,-7.0,7.0,-22.7,11.0),
            self.box(-40.0,-23,-14,-6.75,-11,2),
            self.box(-21.35,-8.43,-9.25,9.25,-23.9,12.2),
        ):
            self.cut(body,self.place(tool,wrist))
        return body

    def wrist_bearing_carrier(self):
        body = self.ring_x(-8.32,3.2,16.48,9.59)
        self.union(body,self.ring_x(-8.3,-7.5,9.76,5.49))
        mount = self.place(self.servo_mount(),self.wrist_servo_frame())
        self.place(mount,frame((WRIST_SHIFT,0,0)))
        # Deux traverses contournent le palonnier, une équerre reprend le moteur.
        for lo,hi in ((-8.35,-6.48),(6.48,8.35)):
            self.union(body,self.box(-21.2,-7.85,lo,hi,-8.4,-5.55))
        self.union(body,mount)
        motor = self.wrist_servo_frame()
        for cutter in self.servo_holes():
            self.place(cutter,motor)
            self.cut(body,self.place(cutter,frame((WRIST_SHIFT,0,0))))
        for y,z in WRIST_BOLTS:
            self.cut(body,self.axial(-21.35,3.35,1.22,y,z),
                     self.axial(.8,3.3,2.18,y,z))
        return body

    def wrist_shaft(self):
        body = self.ring_x(-7.42,4.75,4.99,2.05)
        self.union(body,self.ring_x(2.96,4.75,6.2,2.05))
        tongue = self.rounded(4.6,13.45,-4.18,4.18,-2.05,2.05,1.09)
        self.union(body,tongue)
        for x,y in ((10.25,-3.1),(10.25,3.1)):
            self.cut(body,self.hole_z(x,y,-2.2,2.16,.87))
        return body

    def wrist_bushing(self,start):
        return self.ring_x(start,start+5,9.5,5.0)

    def palm(self):
        body = super().palm()
        # Ouverture locale au-dessus de la traverse. Les rails latéraux restent intacts.
        self.cut(body,self.box(37.9,53.2,-17.5,17.5,-10.7,-6.1))
        # Jeu de l'index fermé devant le bord du support de guide du pouce.
        self.cut(body,self.box(53.32,54.4,-23.05,-21.9,-6.66,-5.00))
        return body

    def cursor(self):
        carrier = self.rounded(-1.22,1.04,-20.23,20.23,-1.10,1.10,.60)
        self.union(carrier,self.rounded(-2.45,2.65,-17.25,17.25,-1.53,1.53,1.05))
        for y in BRANCH_Y:
            self.cut(carrier,self.axial(-2.6,2.8,1.18,y),self.axial(-2.6,-.90,1.62,y))
        self.cut(carrier,self.axial(-2.58,2.8,.67,-18.1))
        self.cut(carrier,self.box(-2.57,-1.71,2.10,4.85,-1.66,1.66))
        return carrier

    def phalanx(self,length,tip):
        last = length if tip else length-4.72
        body = self.side(5.2,last,-4.03,3.45,-4.20,4.20,1.05)
        self.union(body,self.hole_y(0,0,-2.02,2.02,3.37),
                   self.side(2.04,6.30,-3.91,3.12,-2.02,2.02,1.06))
        self.cut(body,self.tear_y(0,0,-2.25,2.25,1.2))
        if not tip:
            self.union(body,*self.fork_blocks(length))
            self.cut(body,self.tear_y(length,0,-5,5,1.2),self.captive_y(length))
        self.cut(body,self.axial(1.7,length+.25,.72,z=-1.93),
                 self.rounded(1.53,4.52,-.97,.97,-4.35,-1.56,.69))
        if tip:
            self.cut(body,self.hole_y(length-2.2,-1.75,-4.65,4.65,.92),
                     self.hole_y(length-2.2,1.75,-4.65,4.65,.93))
        else:
            self.cut(body,self.axial(2.56,length+.2,.76,z=1.9),
                     self.rounded(2.39,4.66,-.99,.99,1.51,4.39,.62))
        return self.cut(body,self.box(-8,length+6,-6,6,-6,-3.97))

    def horizontal_coupon(self):
        body = self.rounded(-19,19,-6.0,6.0,0,8,1.8)
        for x,r in zip((-13,-6.5,0,6.5,13),(1.05,1.125,1.20,1.275,1.35)):
            self.cut(body,self.tear_y(x,3.5,-6.1,6.1,r))
        return body

    def fixing_coupon(self):
        bare = self.rounded(-25,25,-9,9,0,7,2)
        for x,r in ((-18,1.25),(-12,1.39),(-6,1.62),(1,2.15),(9,3.55),(18,3.65)):
            self.cut(bare,self.hole_z(x,2,-.1,7.1,r))
        for x,(b,l) in ((-14,(2.24,2.55)),(-4,(3.02,3.34))):
            self.cut(bare,self.box(x-l,x+l,-5-b,-5+b,3.5,7.1))
        return bare

    def motor_coupon(self):
        plate = self.rounded(-29,29,-13.4,13.4,0,4.4,2)
        self.cut(plate,self.rounded(-20.75,20.75,-10.25,10.25,-.1,4.6,1.6))
        for x in (-24.35,24.35):
            for y in (-5.1,5.1):
                self.cut(plate,self.hole_z(x,y,-.1,4.6,1.39))
        return plate
