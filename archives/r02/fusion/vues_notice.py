"""Génère les vues d’atelier à partir des solides Fusion du document r02."""

from pathlib import Path
import sys

import adsk.core as core
import adsk.fusion as fusion

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from construire_montage import TAG, WorkshopForms, capture, frame, get_design, point, vector
from formes_montage import CAP_BOLTS, ROW_X, THUMB_FIX, THUMB_GUIDE
from geometrie_table import HAUTEUR_EPAULE, LONGUEURS


SERVO = {
    "J2": "MG996R · Épaule J2",
    "J3": "MG90S · Coude J3",
    "J7": "MG90S · Rotation du poignet",
    "T1": "MG90S · Fermeture des cinq doigts",
}
PAL = {
    "J2": "Palonnier J2 · enveloppe",
    "J3": "Palonnier J3 · enveloppe",
    "J7": "Palonnier de roulis · enveloppe",
    "T1": "Palonnier du tambour · enveloppe",
}
ARM = "01_Platine 02_Socle 03_Tourelle 04_Segment_1 05_Segment_2 06_Segment_3"
P = "07_Paume"
B = "12_Support_Pouce"
F = "13_Bride_Poignet"
H = "14_Moyeu"
FINGERS = "I1 I2 I3 M1 M2 M3 A1 A2 A3 U1 U2 U3"
HAND_GEOMETRY = f"{P} {B} {H} P1 P2 P3 {FINGERS}"
THUMB = "P1 P2 P3"
SIDE = (0.30, -1.0, 0.58)
PALMAR = (0.25, -0.84, -1.12)
ISO = (0.85, -1.25, 0.95)
TOP = (0.22, -0.54, 1.35)


def mm(pt):
    return tuple(x * 10 for x in pt.asArray())


def offset(a, b, r=1):
    return tuple(x + r*y for x, y in zip(a, b))


def bodies(document):
    result = {}
    for occ in get_design(document).rootComponent.occurrences:
        items = [b for b in occ.bRepBodies if b.name != "Repère de liaison"]
        result[occ.component.name] = (occ.transform2, items)
        for body in items:
            result[body.name] = (occ.transform2, [body])
            if body.name.startswith("FDM · "):
                result[body.name.split(" · ", 1)[1]] = (occ.transform2, [body])
    return result


class Studio:
    def __init__(self, app, source, scratch):
        self.app = app
        self.source = source
        self.root = get_design(scratch).rootComponent
        self.forms = WorkshopForms(get_design(scratch))
        self.objects = []
        view_dir = OUT/"Vues_Fusion"
        view_dir.mkdir(exist_ok=True)
        self.folder = view_dir
        base = self.forms.appearances["white"]
        self.native_colors = {}
        self.colors = dict(self.forms.appearances)
        for label, rgb in (("neutre", (180, 192, 203)), ("actif", (38, 157, 156)),
                           ("flèche", (232, 97, 34)), ("signal", (42, 127, 207)),
                           ("masse", (64, 72, 85)), ("puissance", (202, 55, 78))):
            color = self.forms.design.appearances.addByCopy(base, f"Notice · {label}")
            prop = next(p for p in color.appearanceProperties
                        if p.id in ("generic_diffuse", "opaque_albedo", "metal_f0")
                        and core.ColorProperty.cast(p))
            prop.value = core.Color.create(*rgb, 255)
            self.colors[label] = color

    def clear(self):
        for part in reversed(self.objects):
            part.deleteMe()
        self.objects.clear()

    def insert(self, solid, name, color):
        part = self.root.bRepBodies.add(solid)
        part.name = name
        part.appearance = color
        self.objects.append(part)
        return part

    def add(self, name, origin, shift=(0, 0, 0), color="actif", opacity=1):
        _, bodies_for_name = self.source[name]
        for orig in bodies_for_name:
            solid = self.forms.manager.copy(orig)
            self.forms.place(solid, origin)
            self.forms.place(solid, frame(shift))
            if color == "source":
                appearance = orig.appearance
                if appearance.name not in self.native_colors:
                    self.native_colors[appearance.name] = self.forms.design.appearances.addByCopy(
                        appearance, "Assemblé · "+appearance.name)
                selected = self.native_colors[appearance.name]
            else:
                selected = self.colors[color]
            created = self.insert(solid, orig.name, selected)
            if opacity < 1:
                created.opacity = opacity

    def scene(self, name):
        output = self.folder/(name+".f3d")
        export = self.forms.design.exportManager
        if not export.execute(export.createFusionArchiveExportOptions(str(output))):
            raise RuntimeError(f"Export de la vue Fusion refusé pour {name}.")

    def permanent_origin(self, name):
        m = self.source[name][0].copy() if name else frame()
        m.invert()
        return m

    def arrow(self, end, displacement, size):
        # Separate arrow solids keep the graphic in Fusion’s native image export.
        start = offset(end, displacement, .76)
        tip = offset(end, displacement, .19)
        cone = offset(tip, displacement, .17)
        self.insert(self.forms.cyl(start, cone, size*.30), "Flèche · hampe", self.colors["flèche"])
        self.insert(self.forms.cyl(cone, tip, size, .035), "Flèche · pointe", self.colors["flèche"])

    def wires(self, polylines):
        for color, radius, points in polylines:
            for start, end in zip(points, points[1:]):
                self.insert(self.forms.cyl(start, end, radius), f"Tracé indicatif · {color}", self.colors[color])

    def shot(self, name, direction, flip=False):
        boxes = [part.boundingBox for part in self.objects]
        ptr = [o for bb in boxes for o in (bb.minPoint.asArray(), bb.maxPoint.asArray())]
        center = tuple((min(v)+max(v))/2 for v in zip(*ptr))
        target = core.Point3D.create(*center)
        eye = core.Point3D.create(*(a+b*40 for a, b in zip(center, direction)))
        up = vector((0, 0, -1 if flip else 1))
        depth = target.vectorTo(eye)
        depth.normalize()
        right = up.crossProduct(depth)
        right.normalize()
        screen_up = depth.crossProduct(right)
        xy = []
        for bb in boxes:
            lo, hi = bb.minPoint, bb.maxPoint
            for x in (lo.x, hi.x):
                for y in (lo.y, hi.y):
                    for z in (lo.z, hi.z):
                        relative = target.vectorTo(core.Point3D.create(x,y,z))
                        xy.append((relative.dotProduct(right), relative.dotProduct(screen_up)))
        axes = tuple(zip(*xy))
        w, h = (max(v)-min(v) for v in axes)
        center_shift = []
        for span, axis in zip(axes, (right, screen_up)):
            axis.scaleBy((max(span)+min(span))/2)
            center_shift.append(axis)
        for shift in center_shift:
            target.translateBy(shift)
            eye.translateBy(shift)
        view = self.app.activeViewport
        camera = view.camera
        camera.cameraType = core.CameraTypes.OrthographicCameraType
        camera.isSmoothTransition = False
        camera.target, camera.eye, camera.upVector = target, eye, up
        height = max(h, w*950/1440)*1.17
        camera.setExtents(height*1440/950, height)
        view.camera = camera
        view.refresh()
        capture(view, self.folder/(name+".png"), 1440, 950, transparent=True)

    def stage(self, name, anchor, direction, fixed, movable, *, flip=False, archive=False):
        self.clear()
        origin = self.permanent_origin(anchor)
        for key in fixed.split():
            self.add(key, origin, color="neutre")
        for keys, shift, aim, size, color in movable:
            for key in keys:
                self.add(key, origin, shift, color)
            if aim is not None:
                self.arrow(aim, shift, size)
        self.shot(name, direction, flip)
        if archive:
            self.scene(name+"_éclaté")
        self.clear()
        for key in fixed.split():
            self.add(key, origin, color="neutre")
        for keys, _, _, _, color in movable:
            for key in keys:
                self.add(key, origin, color=color)
        self.shot(name+"_pose", direction, flip)


def addition(keys, shift, aim, size=1.3, color="actif"):
    return ([keys] if isinstance(keys, str) else keys, shift, aim, size, color)


def run(_context: str):
    app = core.Application.get()
    src = next(d for d in app.documents if d.isSaved and get_design(d)
               and (tag := get_design(d).rootComponent.attributes.itemByName("AURA-01","Reference"))
               and tag.value == TAG)
    source = bodies(src)
    scratch = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    get_design(scratch).designType = fusion.DesignTypes.DirectDesignType
    studio = Studio(app, source, scratch)
    part, stage = addition, studio.stage
    studio.insert(studio.forms.coupon(), "15 · Coupon Ø2", studio.colors["actif"])
    studio.shot("B01_Coupon", TOP)
    studio.clear()
    stage("C01_Platine", None, (0.95,-1.18,.70), "01_Platine", [
        part(["Bouton de lancement · encombrement"], (0,0,22), (43,-28,6)),
        part(["Corps inférieur du bouton · encombrement"], (0,0,-16), (43,-28,-7)),
        *(part(f"Entretoise M4 · {x} / {y}",(0,0,-17),(x,y,-12),1.4,"metal")
          for x in (-54,51) for y in (-40,40))])
    stage("C02_Socle", None, ISO, "01_Platine", [
        part("02_Socle",(0,0,14),(18,-10,27),2.2),
        part("03_Tourelle",(0,0,31),(0,-5,43),2.2),
        part("M4 · Axe de socle orientable",(0,0,74),(0,0,42),1.7,"metal")])
    for n, parent, child, center, size in ((2,"03_Tourelle","04_Segment_1",0,2), (3,"04_Segment_1","05_Segment_2",LONGUEURS[0],1.5)):
        z = HAUTEUR_EPAULE if n == 2 else 0
        stage(f"D0{n-1}_Servo", parent, (-.40,-1,.72), parent, [
            part(SERVO[f"J{n}"], (0,-37,0), (center,-26,z),size)])
        stage(f"D0{n+1}_Pivot", parent, (0.58,1,.74), parent, [
            part(SERVO[f"J{n}"], (0,0,0), None, color="neutre"),
            part([child,PAL[f"J{n}"]], (0,0,24), (center,0,z+4),size),
            part(f"Écrou M3 captif · J{n}",(0,0,20),(center,4,z),1.3,"metal"),
            part(f"Axe passif M3 · J{n}",(0,31,0),(center,13,z),1.4,"metal")])
    stage("D05_Segment", "06_Segment_3", TOP, "05_Segment_2",
          [part("06_Segment_3",(28,0,0),(0,0,0),1.55)])
    stage("E01_Bride", P, (.70,-1,.44), "06_Segment_3", [
        part([F,SERVO["J7"]], (23,0,0),(-5,1,0),1.6),
        *(part(f"M2×12 · Bride de poignet {i}", (41,0,0), tuple(v for v in (-2,y,z)),1.15,"metal")
          for i,(y,z) in enumerate(CAP_BOLTS,1))],archive=True)
    studio.clear()
    prism=studio.permanent_origin(P)
    studio.add("06_Segment_3",prism,color="neutre",opacity=.27)
    studio.add(F,prism,color="neutre",opacity=.45)
    studio.add(SERVO["J7"],prism,color="actif")
    studio.shot("E01_Bride_Interieur",(.65,-1,.65))
    stage("E02_Moyeu", P, TOP, f"06_Segment_3 {F}", [
        part(PAL["J7"],(0,0,0),None,color="neutre"),
        part(H,(14,0,0),(6,0,0)),
        part(P,(33,0,0),(23,0,1),1.6),
        *(part(f"M2×6 · Moyeu {i}", (33,0,20), None,color="metal") for i in (1,2))])
    stage("E03_Transmission", P, PALMAR, f"{P} {H}", [
        part(SERVO["T1"], (0,22,0),(17,14,-10)),
        part(PAL["T1"],(0,29,0),None,color="metal"),
        part("10_Tambour",(0,39,0),(17,21,-10),1.15),
        part("11_Palonnier",(19,0,0),(48,2,-9)),
        *(part(f"M2×6 · Butée du répartiteur {i}",(0,0,-20),(50.76,y,-11.80),.95,"metal")
          for i,y in ((1,-19.8),(2,19.8)))], flip=True)
    stage("E04_Phalanges", "I1", TOP, "I1", [
        part("I2", (8,0,0),(17,0,0),.60),
        part("I3",(16,0,0),(30,0,0),.60),
        part("Axe vissé · I2",(8,-13,0),None,color="metal"),
        part("Axe vissé · I3",(16,-13,0),None,color="metal"),
        part("Écrou · I2",(8,13,0),None,color="metal"),
        part("Écrou · I3",(16,13,0),None,color="metal")])
    stage("E04_Phalanges_Pouce", "P1", TOP, "", [
        part(B,(-9,0,0),(-5,0,0),.65),
        part("P1",(0,0,0),None), part("P2",(7,0,0),(14,0,0),.64),
        part("P3",(14,0,0),(26.5,0,0),.64),
        *(part(f"Axe vissé · P{i}",((i-1)*7,-13,0),None,color="metal") for i in (1,2,3)),
        *(part(f"Écrou · P{i}",((i-1)*7,13,0),None,color="metal") for i in (1,2,3))])
    stage("E05_Axe", P, TOP, f"{P} {FINGERS}", [
        part("Axe acier commun aux quatre doigts",(0,-57,0),(ROW_X,-24,0),1.6,"metal"),
        part("Retenue d’axe · côté -1",(0,-20,0),(ROW_X-3.15,-24,0),.95,"metal"),
        part("Retenue d’axe · côté +1",(0,18,0),(ROW_X-3.15,24,0),.95,"metal")],archive=True)
    x,y=THUMB_GUIDE
    stage("E06_Pouce", P, PALMAR, f"{P} {FINGERS}", [
        part([B,*THUMB.split()],(0,-22,0),(21,-23,-1),1.4),
        *(part(f"Vis support {i}",(0,0,-14-4*i),(sx,sy,-4.7),.75,"metal")
          for i,(sx,sy) in enumerate(THUMB_FIX,1)),
        *(part(f"Écrou support {i}",(0,0,13),None,color="metal") for i in (1,2)),
        part("Rondelle · renvoi -6.92",(0,0,-7),None,color="metal"),
        part("Entretoise lisse · renvoi du pouce",(0,0,-14),(x,y,-9),.85,"metal"),
        part("Rondelle · renvoi -10.72",(0,0,-21),None,color="metal"),
        part("M3×8 · Renvoi de tendon du pouce",(0,0,-30),(x,y,-10.7),.85,"metal")],flip=True,archive=True)
    studio.clear()
    palm_origin = studio.permanent_origin(P)
    for key in (*HAND_GEOMETRY.split(), "10_Tambour", "11_Palonnier"):
        studio.add(key,palm_origin,color="neutre" if key not in ("10_Tambour","11_Palonnier") else "actif")
    studio.add("Entretoise lisse · renvoi du pouce",palm_origin,color="metal")
    thumb_tip = studio.source["P3"][0].translation
    tip = core.Point3D.create(*thumb_tip.asArray())
    tip.transformBy(palm_origin)
    thumb_tip_mm = mm(tip)
    tendon_lines = [("puissance", .34, ((48,-17,-9.15),(55.75,-25,-9.15),(53.75,-29.75,-9.15),
                                       (40,-32,-7),(25,-26,-5),offset(thumb_tip_mm,(2,0,-2)))),
                    ("signal",.36,((18,19.1,-15.8),(28,16.0,-11),(44,0,-9.8),(48.1,0,-9.6)))]
    tendon_lines.extend(("actif",.25,((48,py,-8.8),(46,py,-7),(46,py,-3.9),
                                    (52,py,-3.5),(66.0,py,-2.9),(78,py,-2.9),(91,py,-3.0)))
                         for py in (-18.6,-6.2,6.2,18.6))
    studio.wires(tendon_lines)
    studio.shot("E07_Tendons",PALMAR, True)
    stage("F01_Electronique", None, (-.58,-1.1,1.1), "01_Platine 02_Socle", [
        part("Nano ATmega328P · encombrement",(0,0,23),(-46,0,10),1.6),
        part("Bouton de lancement · encombrement",(0,0,16),(43,-28,6),1.1)])
    studio.clear()
    world = studio.permanent_origin(None)
    for key in (*ARM.split(),*HAND_GEOMETRY.split(),SERVO["J2"],SERVO["J3"],SERVO["J7"],SERVO["T1"],
                "Nano ATmega328P · encombrement"):
        studio.add(key,world,color="neutre" if key not in SERVO.values() else "actif")
    # Parcours de pose indicatif, à vérifier avec les cordons du kit.
    joints = [mm(studio.source[key][0].translation) for key in
              ("04_Segment_1","05_Segment_2","06_Segment_3",P,"P1")]

    def local(key, xyz):
        q=point(xyz)
        q.transformBy(source[key][0])
        return mm(q)

    lo = [(-53,-10,11),(-38,-14,10),(-25,-18,11),(-35,-30,19),(-41,-35,36)]
    j2 = lo+[local(SERVO["J2"],(22,0,-40))]
    arm = lo+[local("04_Segment_1",xyz) for xyz in ((1,-22,-5),(8,-11,2),(13,0,4.5),(32,0,4.5))]
    j3 = arm+[local("04_Segment_1",(39,-9,7)),local(SERVO["J3"],(12,0,-26))]
    wrist = arm+[local("04_Segment_1",(44,0,7)),
                 local("05_Segment_2",(0,-7,12)),local("05_Segment_2",(10,0,5.1)),
                 local("05_Segment_2",(26,0,5.1)),local("05_Segment_2",(38,0,9))]
    j7 = wrist+[local(P,(-31,-3,9)),local(P,(-24,-1.5,5))]
    t1 = wrist+[local(P,(-26,-14,13)),local(P,(-11,-19,10)),
                local(P,(-1,-21,-8)),local(P,(9,-15,-18)),local(P,(18,-6,-16))]
    wires=[]
    for path_index, points in enumerate((j2,j3,j7,t1)):
        for color,k in (("signal",0),("puissance",-1.2),("masse",1.2)):
            shift=k+(path_index-1.5)*2.8
            wires.append((color,.36,tuple(offset(p,(0,shift,0)) for p in points)))
    studio.wires(wires)
    studio.shot("G01_Parcours", (0.95,-1.4,.84))
    stage("H01_Capots", None, (0.52,-1.2,1.12), ARM, [
        part("08_Capot",(0,0,28),offset(joints[0],(20,0,8)),2),
        part("09_Capot",(0,0,28),offset(joints[1],(18,0,8)),2)])
    studio.clear()
    for occ in get_design(src).rootComponent.occurrences:
        if occ.component.name == "Rondelle de renvoi du pouce":
            studio.add(occ.bRepBodies.item(0).name,world,color="source")
        else:
            studio.add(occ.component.name,world,color="source")
    studio.shot("H02_Ensemble", ISO)
    studio.shot("H03_Ensemble_Arriere",(-.62,1.28,.81))
    scratch.close(False)
    src.activate()
    print(f"{len(list(studio.folder.glob('*.png')))} vues Fusion dans {studio.folder.name}")
