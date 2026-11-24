"""Géométrie native AURA-01 V3. Les cotes de cette source sont en millimètres."""

import math

import adsk.core as core
import adsk.fusion as fusion


DIGITS = (
    ("P", "Pouce",   (31, -70, -4), -59, 48, (48, 44, 39)),
    ("I", "Index",  (108, -48, 0),  -1,  0, (52, 46, 39)),
    ("M", "Majeur", (111, -16, 1),   0,  0, (55, 49, 41)),
    ("A", "Annulaire", (109, 16, 0), 1,  0, (51, 46, 39)),
    ("O", "Auriculaire", (103, 48, -1), 3, 0, (45, 42, 37)),
)
SEGMENTS = ((140, 54, 46, 52), (123, 54, 44, -34), (112, 46, 38, -37))
M1, M2, M3 = "XM540-W270-T", "XM540-W270-T", "XM430-W350-T"
WHITE = (255, 255, 255)


def point(pos):
    return core.Point3D.create(*(value / 10 for value in pos))


def vector(values):
    return core.Vector3D.create(*values)


def frame(offset=(0, 0, 0), yaw=0, pitch=0, roll=0):
    tx = core.Matrix3D.create()
    tx.setToRotation(math.radians(yaw), vector((0, 0, 1)), point((0, 0, 0)))
    for angle, axis in ((-pitch, (0, 1, 0)), (roll, (1, 0, 0))):
        turn = core.Matrix3D.create()
        turn.setToRotation(math.radians(angle), vector(axis), point((0, 0, 0)))
        turn.transformBy(tx)
        tx = turn
    tx.translation = vector(tuple(v / 10 for v in offset))
    return tx


def compose(parent, child):
    result = child.copy()
    result.transformBy(parent)
    return result


class Solids:
    def __init__(self, design):
        self.design = design
        self.manager = fusion.TemporaryBRepManager.get()
        self.appearances = self.make_appearances()

    def make_appearances(self):
        import adsk.core

        libraries = adsk.core.Application.get().materialLibraries
        known = ("generic_diffuse", "opaque_albedo", "metal_f0")
        source, fallback, property_id = None, None, None
        for library in libraries:
            for appearance in library.appearances:
                name = appearance.name.casefold()
                if not any(term in name for term in ("plastic", "plastique", "enamel", "émail")):
                    continue
                p = next((p.id for p in appearance.appearanceProperties
                          if p.id in known and core.ColorProperty.cast(p)), None)
                if p is None:
                    continue
                fallback = fallback or (appearance, p)
                if any(term in name for term in ("white", "blanc")):
                    source, property_id = appearance, p
                    break
            if source:
                break
        if not source:
            if fallback is None:
                raise RuntimeError("Bibliothèque d’apparences Fusion introuvable")
            source, property_id = fallback
        result = {}
        for key, label, rgb in (
            ("white", "AURA - Blanc céramique", WHITE),
            ("ice", "AURA - Gris perle", (172, 187, 196)),
            ("dark", "AURA - Graphite profond", (37, 49, 58)),
            ("rubber", "AURA - Anthracite", (57, 67, 74)),
            ("metal", "AURA - Métal satiné", (116, 143, 155)),
            ("accent", "AURA - Bleu pétrole", (19, 106, 122)),
        ):
            appearance = self.design.appearances.addByCopy(source, label)
            prop = core.ColorProperty.cast(appearance.appearanceProperties.itemById(property_id))
            if not prop:
                raise RuntimeError(f"Propriété de couleur introuvable : {source.name}")
            prop.value = core.Color.create(*rgb, 255)
            result[key] = appearance
        return result

    def box(self, x0, x1, y0, y1, z0, z1):
        mid = point(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        bounds = core.OrientedBoundingBox3D.create(
            mid, vector((1, 0, 0)), vector((0, 1, 0)), (x1 - x0) / 10,
            (y1 - y0) / 10, (z1 - z0) / 10,
        )
        return self.manager.createBox(bounds)

    def cyl(self, start, end, radius, end_radius=None):
        return self.manager.createCylinderOrCone(
            point(start), radius / 10, point(end),
            (radius if end_radius is None else end_radius) / 10,
        )

    def op(self, target, tool, operation):
        if not self.manager.booleanOperation(target, tool, operation):
            raise RuntimeError(f"Fusion a refusé une opération booléenne {operation}")
        return target

    def union(self, target, *tools):
        for tool in tools:
            self.op(target, tool, fusion.BooleanTypes.UnionBooleanType)
        return target

    def cut(self, target, *tools):
        for tool in tools:
            self.op(target, tool, fusion.BooleanTypes.DifferenceBooleanType)
        return target

    def rounded(self, x0, x1, y0, y1, z0, z1, radius):
        body = self.box(x0, x1, y0 + radius, y1 - radius, z0, z1)
        self.union(body, self.box(x0 + radius, x1 - radius, y0, y1, z0, z1))
        for x in (x0 + radius, x1 - radius):
            for y in (y0 + radius, y1 - radius):
                self.union(body, self.cyl((x, y, z0), (x, y, z1), radius))
        return body

    def lugs(self, pivot, inner, outer, radius, bore, axis="y", reach=None):
        x, y, z = pivot
        reach = radius + 5 if reach is None else reach
        shapes = []
        for low, high in ((-outer, -inner), (inner, outer)):
            if axis == "y":
                a, b = (x, y + low, z), (x, y + high, z)
                tail = self.box(x - reach, x + radius * 0.4, y + low, y + high,
                                z - radius * 0.63, z + radius * 0.63)
            else:
                a, b = (x, y, z + low), (x, y, z + high)
                tail = self.box(x - reach, x + radius * 0.4, y - radius * 0.63,
                                y + radius * 0.63, z + low, z + high)
            shapes.append(self.cut(self.union(self.cyl(a, b, radius), tail),
                                   self.cyl(a, b, bore)))
        return shapes

    def finger_fork(self, x, reach):
        passive, active = self.lugs((x, 0, 0), 11.8, 14.95, 8.1, 1.65, reach=reach)
        # The active cheek receives the servo horn; the opposite cheek carries the pin.
        seat = self.cyl((x, 10.82, 0), (x, 13, 0), 3.9)
        self.cut(seat, self.cyl((x, 10.7, 0), (x, 13.1, 0), 2.12))
        return passive, self.union(active, seat)

    def fixed(self, table):
        plate = self.rounded(-137, 137, -108, 108, 0, 9, 18)
        for x in (-110, 110):
            for y in (-84, 84):
                self.cut(plate, self.cyl((x, y, -1), (x, y, 11), 3.35))
        table += [
            ("Platine ancrée, 4 passages Ø6,7", "dark", plate),
            ("Socle évasé", "ice", self.cyl((0, 0, 9), (0, 0, 25), 64, 57)),
            ("Couronne fixe", "dark", self.cyl((0, 0, 25), (0, 0, 31), 56)),
        ]

    def turret(self, table):
        table += [
            ("Pivot J1", "metal", self.cyl((0, 0, 0), (0, 0, 4), 31)),
            ("Bande de lacet", "accent", self.cyl((0, 0, 4), (0, 0, 8), 55)),
            ("Tourelle", "dark", self.cyl((0, 0, 8), (0, 0, 19), 54, 49)),
            ("Montant d’épaule", "ice", self.rounded(-33, 28, -35, 35, 19, 57, 13)),
        ]
        for side in (-1, 1):
            low, high = sorted((side * 28.2, side * 34.2))
            rib = self.box(-19, 18, low, high, 47, 72)
            cheek = self.cyl((0, low, 72), (0, high, 72), 23)
            bore = self.cyl((0, low - 1, 72), (0, high + 1, 72), 4.2)
            table.append(("Chape épaule", "dark", self.cut(self.union(cheek, rib), bore)))

    def pivot(self, axis, radius, half_span):
        ends = {"x": ((-half_span, 0, 0), (half_span, 0, 0)),
                "y": ((0, -half_span, 0), (0, half_span, 0)),
                "z": ((0, 0, -half_span), (0, 0, half_span))}
        a, b = ends[axis]
        return self.cyl(a, b, radius)

    def arm(self, table, index, length, width, height):
        thick = height / 2
        wide = width / 2
        case_len, case_w, case_h = (58.5, 44, 33.5) if index < 3 else (46.5, 34, 28.5)
        shell = self.rounded(-19, length - 26, -wide, wide, -thick, thick - 3, 8)
        core = self.rounded(-15, length - 29, -wide + 3.7, wide - 3.7, -thick + 4, thick + 2, 5)
        # Four continuous rails around the motor pocket and routing space.
        self.cut(shell, core)
        top = self.rounded(-16, length - 28, -wide + 0.7, wide - 0.7, thick - 2.7, thick + 1.3, 8)
        stripe = self.rounded(36, length - 30, -4.1, 4.1, thick + 1.3, thick + 2.1, 3)
        table += [
            ("Axe acier coaxial", "metal", self.pivot("y", 4, wide + 7)),
            ("Longeron évidé", "dark", shell),
            ("Coque longitudinale", "ice", top),
            ("Repère longitudinal", "accent", stripe),
            ("Enveloppe moteur " + (M1, M2, M3)[index - 1], "dark",
             self.box(-12, case_len - 12, -case_w / 2, case_w / 2, -case_h / 2, case_h / 2)),
        ]
        if index < 3:
            child_width = SEGMENTS[index][1]
            axis, inner, outer = "y", child_width / 2 + 0.7, child_width / 2 + 6.2
        else:
            axis, inner, outer = "z", 12.5, 18.5
        for cheek in self.lugs((length, 0, 0), inner, outer, 16, 4.2, axis, 42):
            table.append(("Chape de sortie", "dark", cheek))
        # A transverse bridge joins the two cheeks to the end of the structural spine.
        join = (self.box(length - 34, length - 28, -outer, outer, -10, 10)
                if axis == "y" else self.box(length - 34, length - 28, -16, 16, -outer, outer))
        table.append(("Pont de chape", "dark", join))

    def yaw_wrist(self, table):
        table += [
            ("Axe de déviation du poignet", "metal", self.pivot("z", 4, 19)),
            ("Corps de déviation", "dark", self.rounded(-12, 31, -19, 19, -11.7, 11.7, 5)),
            ("Cape du poignet", "ice", self.rounded(4, 24, -17, 17, 11.7, 15.2, 5)),
        ]
        # The second yoke sits outside the body of the pitch stage.
        for cheek in self.lugs((43, 0, 0), 18.8, 24.1, 13, 3.2, reach=21):
            table.append(("Chape de flexion", "metal", cheek))

    def pitch_wrist(self, table):
        table += [
            ("Axe de flexion du poignet", "metal", self.pivot("y", 3, 24.5)),
            ("Corps de flexion", "dark", self.rounded(-10, 29, -17.7, 17.7, -11, 11, 6)),
            ("Palier de roulis", "ice", self.cyl((21, 0, 0), (36.5, 0, 0), 19)),
            ("Bague repère", "accent", self.cyl((36.5, 0, 0), (39, 0, 0), 17)),
        ]

    def palm(self, table):
        shell = self.rounded(3, 93, -61, 61, -12.7, 10.3, 24)
        niche = self.rounded(17, 87, -54, 54, -9.8, 11.5, 14)
        self.cut(shell, niche)
        lid = self.rounded(4, 92, -60.5, 60.5, 10.6, 14, 24)
        inset = self.rounded(22, 71, -15, 15, 14, 15, 12)
        table += [
            ("Axe de roulis", "metal", self.pivot("x", 7.5, 7)),
            ("Moyeu de main", "white", self.cyl((0.65, 0, 0), (16, 0, 0), 17)),
            ("Coque blanche de paume", "white", shell),
            ("Capot blanc démontable", "white", lid),
            ("Médaillon", "ice", inset),
            ("Renfort traversant des doigts", "white", self.rounded(79, 94, -56, 56, -8, 5, 5)),
            ("Support de pouce", "white", self.rounded(20, 53, -73, -38, -11, 1, 8)),
        ]
        for _, label, xyz, yaw, roll, _ in DIGITS:
            tx = frame(xyz, yaw=yaw, roll=roll)
            for cheek in self.finger_fork(0, 25):
                if not self.manager.transform(cheek, tx):
                    raise RuntimeError(label)
                table.append(("Fourche paume - " + label, "white", cheek))

    def phalanx(self, table, length, tip):
        limit = length - (0.9 if tip else 13)
        # 20 x 7 x 16.6 mm body, nominal 28 mm across the mounting ears.
        # At the joint, X follows the phalanx, Y is the output shaft, Z the 7 mm thickness.
        body = self.rounded(-10.4, limit, -11.45, 11.45, -7.8, 7.1, 3.5)
        pocket = self.rounded(-9.55, 21.2, -8.87, 8.87, -4.35, 9.0, 1.15)
        journal = self.cyl((0, -12, 0), (0, 12, 0), 2.75)
        horn_clearance = self.cyl((0, 10.63, 0), (0, 12, 0), 4.12)
        wire_relief = self.box(5, 21.8, -10.6, -7.7, -5.5, -1.6)
        wire_entry = self.box(-11.1, -7.1, -6.3, -2.3, -5.6, -1.8)
        self.cut(body, pocket, journal, horn_clearance, wire_relief, wire_entry)
        if tip:
            self.cut(body, self.rounded(25.5, limit - 3.5, -8.1, 8.1, -5.4, 8, 1.9))
        else:
            self.cut(body, self.box(19.9, limit + 0.4, -3.2, 3.2, -4.9, -1.0))
        lid = self.rounded(-10.15, limit - 0.3, -11.2, 11.2, 7.1, 9.25, 3.4)
        for y in (-6.2, 6.2):
            self.cut(lid, self.cyl((23, y, 6.9), (23, y, 9.6), 1.13))
            self.cut(body, self.cyl((23, y, 3.5), (23, y, 7.3), 0.82))
        motor = self.box(-5, 15, -8.3, 8.3, -3.5, 3.5)
        self.union(motor, self.box(-9, 19, 3.6, 4.6, -3.5, 3.5),
                   self.cyl((0, 8.27, 0), (0, 11, 0), 1.95))
        for x in (-7, 17):
            self.cut(motor, self.cyl((x, 3.5, 0), (x, 4.7, 0), 1.1))
        pin = self.cyl((0, -15.25, 0), (0, -8.65, 0), 1.52)
        bushing = self.cut(self.cyl((0, -11.65, 0), (0, -8.6, 0), 2.64),
                           self.cyl((0, -11.8, 0), (0, -8.5, 0), 1.53))
        table += [
            ("Pivot passif acier coaxial, côté opposé au servo", "metal", pin),
            ("Bague du pivot passif", "metal", bushing),
            ("Châssis blanc à logement moteur", "white", body),
            ("Capot blanc démontable", "white", lid),
            ("KST X06 V6.0 - corps et pattes", "dark", motor),
        ]
        # Positive registration for the case and an open route toward the next hinge.
        for side in (-1, 1):
            low, high = sorted((side * 8.1, side * 10.1))
            table.append(("Rail d’appui du servo", "ice",
                          self.box(-5.7, 17.1, low, high, -4.35, -3.58)))
        if tip:
            table.append(("Pulpe souple du doigt", "ice",
                          self.rounded(length - 15, length - 1.7, -8.5, 8.5, -10, -7.8, 3.9)))
        else:
            for cheek in self.finger_fork(length, 24):
                table.append(("Fourche distale blanche", "white", cheek))
            for side in (-1, 1):
                low, high = sorted((side * 10.1, side * 14.95))
                table.append(("Pont latéral", "white",
                              self.box(length - 23, length - 17, low, high, -4.5, 4.5)))
