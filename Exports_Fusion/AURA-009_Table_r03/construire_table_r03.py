"""Construction native du bras AURA-009 de table r03 dans Autodesk Fusion."""

from pathlib import Path
import importlib
import json
import math
import sys

import adsk.core as core
import adsk.fusion as fusion


HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
for name in ("AURA-009_Montage", "AURA-008_Main_Poignet", "AURA-007_Bras_Table",
             "AURA_V3/Generateur_AURA_V3"):
    folder = HERE.parent / name
    if not folder.is_dir():
        folder = HERE / "sources_heritage" / name
    sys.path.insert(0, str(folder))

from construire_montage import Workshop, get_design
from formes_articulees import CURSOR, MOUNT_LARGE
from geometrie import compose, frame, point, vector
from geometrie_table import ANGLES_REPOS, LONGUEURS
import formes_table_r03 as shapes

importlib.reload(shapes)

TITLE = "AURA-01 — V3 de table — AURA-009 r03"
DRAFT = TITLE + " (mise au point)"
TAG = "AURA-009 · V3 de table · r03"
SOURCE = "AURA-009 / V3 de table r02 / Fusion v1"
VENDOR = HERE.parent / "AURA_01_Integration_mecatronique/Plans_constructeurs/XC330_ROBOTIS.step"
if not VENDOR.is_file():
    VENDOR = HERE / "sources_heritage" / "XC330_ROBOTIS.step"

ORIENTATIONS = {
    "02_Socle": {"roll": 180}, "03_Tourelle": {"roll": 90},
    "04_Segment_1": {"roll": 90}, "05_Segment_2": {"roll": 90},
    "06_Segment_3": {"roll": 180}, "07_Paume": {"roll": 180},
    "10_Tambour": {"roll": -90}, "11_Palonnier": {"pitch": 90},
    "13_Bride_Poignet": {"pitch": -90}, "14_Moyeu": {"pitch": 90},
    "P07_Porte_J2": {"roll": 90}, "P08_Porte_J3": {"roll": 90},
    "P09_Frein_J2": {"roll": -90}, "P10_Frein_J3": {"roll": -90},
    "P11_Garde_J2": {"roll": 90}, "P12_Garde_J3": {"roll": 90},
}


class Table(Workshop):
    def __init__(self, document, motor_bodies):
        self.doc = document
        self.design = get_design(document)
        self.design.designType = fusion.DesignTypes.ParametricDesignType
        self.root = self.design.rootComponent
        self.forms = shapes.Geometry(self.design)
        self.occ, self.prints, self.markers, self.joints = {}, {}, {}, {}
        self.flexion, self.print_groups, self.lengths = {}, {}, {}
        self.native_links = False
        self.motor_bodies = motor_bodies
        self.stage = {}

    def fixed(self, parent, child):
        super().fixed(parent, child)
        self.stage[child] = parent
        self.occ[child].component.attributes.add("AURA-01", "Parent", parent)

    def hinge(self, parent, child, label, axis, bounds):
        super().hinge(parent, child, label, axis, bounds)
        self.stage[child] = parent
        comp = self.occ[child].component
        comp.attributes.add("AURA-01", "Parent", parent)
        comp.attributes.add("AURA-01", "Joint", label.split(" · ")[0])

    def parameters(self):
        params = self.design.userParameters
        for name, expression, units, description in (
            ("LongueurPlatine", "180 mm", "mm", "Taille pilotant l'esquisse native du plateau"),
            ("LargeurPlatine", "144 mm", "mm", "Taille pilotant l'esquisse native du plateau"),
            ("EpaisseurPlatine", "6 mm", "mm", "Extrusion native du plateau"),
            ("DiametreAncrage", "5.5 mm", "mm", "Diamètre pilotant les quatre passages"),
            ("AxePorteur", "5 mm", "mm", "Cote de définition du tendeur de pivot"),
            ("AlesageBague", "7.10 mm", "mm", "Diamètre nominal FDM à ajuster sur coupon"),
            ("HauteurJ2", "82 mm", "mm", "Cote de définition du centre d'épaule"),
            ("EntraxeJ2J3", f"{LONGUEURS[0]} mm", "mm", "Cote de définition du bras"),
            ("EntraxeJ3Raccord", f"{LONGUEURS[1]} mm", "mm", "Cote de définition de l'avant-bras"),
            ("CourseTraverse", "7.5 mm", "mm", "Course CAO nominale à qualifier"),
        ):
            params.add(name,core.ValueInput.createByString(expression),units,description)

    def remember_code(self):
        for code, occ in self.occ.items():
            occ.component.partNumber = "AURA009-R03-" + code
            occ.component.attributes.add("AURA-01", "Repere", code)
            if code in self.prints:
                occ.component.attributes.add("AURA-01", "Impression", self.print_groups.get(code,code))
            for body in occ.component.bRepBodies:
                if not body.name.startswith(("Repère de liaison","FDM · ")):
                    body.name=f"[{code}] {body.name}"

    def deck(self):
        code = "01_Platine"
        occ = self.root.occurrences.addNewComponent(frame())
        comp = occ.component
        comp.name = "01 · Platine PETG ancrée M5"
        sketch = comp.sketches.add(comp.xYConstructionPlane)
        sketch.name = "Platine · encombrement et perçages M5"
        lines = sketch.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(point((shapes.BASE_X[0],-72,0)),
                                          point((shapes.BASE_X[1],72,0)))
        for horizontal, name, offset in (
            (True,"LongueurPlatine",(26,-82,0)),
            (False,"LargeurPlatine",(-77,0,0)),
        ):
            edge = next(e for e in rect if (abs(e.startSketchPoint.geometry.y -
                                              e.endSketchPoint.geometry.y)<.001)==horizontal)
            label = (fusion.DimensionOrientations.HorizontalDimensionOrientation if horizontal
                     else fusion.DimensionOrientations.VerticalDimensionOrientation)
            dim = sketch.sketchDimensions.addDistanceDimension(edge.startSketchPoint,
                         edge.endSketchPoint,label,point(offset))
            dim.parameter.expression = name
        circles = sketch.sketchCurves.sketchCircles
        drills = [circles.addByCenterRadius(point((x,y,0)),.275)
                  for x in shapes.ANCHOR_X for y in shapes.ANCHOR_Y]
        for other in drills[1:]:
            sketch.geometricConstraints.addEqual(drills[0],other)
        sketch.sketchDimensions.addDiameterDimension(drills[0],point((-45,-51,0))).parameter.expression="DiametreAncrage"
        for x,y,r in ((32,0,2.25),(-32,0,2.25),(0,-32,2.25),(0,32,2.25),
                      (-26,-60,6.15),(-42,45,1.75),(-42,65,1.75),(20,45,1.75),(20,65,1.75)):
            circles.addByCenterRadius(point((x,y,0)),r/10)
        profile = max(sketch.profiles,key=lambda p:p.areaProperties().area)
        feature = comp.features.extrudeFeatures.addSimple(profile,
                   core.ValueInput.createByString("EpaisseurPlatine"),
                   fusion.FeatureOperations.NewBodyFeatureOperation)
        feature.name="Extrusion pilotée · platine"
        body = feature.bodies.item(0)
        body.name="FDM · "+code
        body.appearance=self.forms.appearances["dark"]
        sketch.isLightBulbOn=False
        self.prints[code]=(occ,body.name,0)
        self.occ[code]=occ
        occ.isGrounded=True

    def place_hardware(self, code, label, parent, at, parts):
        self.add(code,label,at,parts)
        self.fixed(parent,code)

    def hardware(self,code,label,parent,at,shape,appearance="metal"):
        if code.startswith("Vis_Bride_"):
            self.forms.place(shape,frame((2.85,0,0)))
        super().hardware(code,label,parent,at,shape,appearance)

    def printed_fixed(self, code, label, parent, at, shape, finish="ice"):
        self.printed(code,label,at,shape,finish)
        self.fixed(parent,code)

    def bolt_y(self,x,z,y0,y1,r=1.36,head=2.5,side=-1):
        f=self.forms
        a,b=(y0-1.6,y0+.12) if side<0 else (y1-.12,y1+1.6)
        return f.union(f.hole_y(x,z,y0,y1,r),f.hole_y(x,z,a,b,head))

    def base_hardware(self, base, turret):
        f=self.forms
        self.hardware("AXE_J1","J1 · axe fixe Ø8", "02_Socle", base,
                      f.hole_z(0,0,29.5,44.9,4))
        self.hardware("RON_J1","J1 · rondelle d’appui Ø32", "02_Socle", base,
                      f.ring_z(36.02,36.96,16,4.25), "metal")
        self.hardware("COL_J1","J1 · bague de retenue supérieure", "02_Socle", base,
                      f.ring_z(43.08,45.5,7.0,4.01), "metal")
        ballast = f.rounded(-48,98,-46,46,-3.1,-.3,4)
        for x in (-32,32):
            f.cut(ballast,f.hole_z(x,0,-3.3,.1,2.35))
        self.hardware("LEST","Lest amovible acier · scénario +0,30 kg",
                      "01_Platine",base,ballast)
        for i,(x,y) in enumerate(((x,y) for x in shapes.ANCHOR_X for y in shapes.ANCHOR_Y),1):
            parts=[
                (f.ring_z(-10,0,6.0,2.75,x,y),"metal","Entretoise M5"),
                (f.hole_z(x,y,-11,6.98,2.48),"metal","Tige M5 (support hors modèle)"),
                (f.ring_z(6.02,6.92,5.5,2.55,x,y),"metal","Rondelle M5"),
                (f.hole_z(x,y,6.97,8.85,4.1),"metal","Tête M5")
            ]
            self.place_hardware(f"ANC_{i}",f"Fixations établies · M5 {i}","01_Platine",base,parts)
        # Le doigt d'index est garé pour les vérifications avec J1 libre.
        self.hardware("PION_J1","J1 · pion Ø3 à garer avant rotation","01_Platine",
                      frame((-49,17,0)),f.hole_z(0,0,6.05,23,1.50),"accent")

    def axes(self,n,parent,child,parent_pose,child_pose,pitch,stops):
        f=self.forms
        for side,letter in ((-1,"G"),(1,"D")):
            self.hardware(f"PALIER_J{n}_{letter}",f"J{n} · bague PFM-0507-05 {letter}",
                          parent,parent_pose,f.bush(side),"accent")
        self.hardware(f"AXE_J{n}",f"J{n} · arbre porteur Ø5 et méplat",
                      child,child_pose,f.shaft())
        self.hardware(f"PION_J{n}",f"J{n} · goupille transversale Ø2",
                      child,child_pose,f.hole_z(0,0,-8.3,8.3,.975))
        self.hardware(f"DOG_J{n}",f"J{n} · accouplement d’arbre à méplat",
                      child,child_pose,f.drive_collar(n,pitch),"accent")
        at=compose(parent_pose,f.motor_frame(n))
        if n==2:
            self.hardware("SERVO_J2","MG996R · actionneur J2",parent,at,f.large_servo(),"rubber")
            horn=f.ring_y(-29.91,-28.27,6.30,2.99)
            for x in (-4.7,4.7):
                f.cut(horn,f.hole_y(x,0,-30,-28.15,1.05))
            self.hardware("CORNE_J2","J2 · interface cannelée et entraxe d’adaptation",
                          child,child_pose,horn,"metal")
            pins=[(f.hole_y(x,0,-29.87,-25.3,.98),"metal","Goupille d’entraînement Ø2")
                  for x in (-4.7,4.7)]
        else:
            horn=[part for part in self.motor_bodies if part[2].endswith("04")]
            body=[part for part in self.motor_bodies if part not in horn]
            self.place_hardware("SERVO_J3","ROBOTIS XC330-M288-T · STEP constructeur",parent,at,body)
            horn_pose=compose(compose(child_pose,frame(pitch=-pitch)),f.motor_frame(n))
            self.place_hardware("CORNE_J3","J3 · palonnier constructeur percé Ø12",
                                child,horn_pose,horn)
            pins=[(f.hole_y(x,z,-31.1,-26.30,.78),"metal","Axe de vis M2 sur cercle Ø12")
                  for x,z in f.xc_pitch_circle(pitch)]
        self.place_hardware(f"COUPLE_J{n}",f"J{n} · liaison palonnier–arbre",
                            child,child_pose,pins)
        self.printed_fixed(f"P0{n+5}_Porte_J{n}",f"J{n} · support moteur démontable",
                           parent,parent_pose,f.motor_mount(n))
        self.printed_fixed(f"P{n+7:02}_Frein_J{n}",f"J{n} · carter friction et ancrage de ressort",
                           parent,parent_pose,f.brake_carrier(),"dark")
        self.printed_fixed(f"P{n+9:02}_Garde_J{n}", f"J{n} · garde et porte-butées",
                           parent,parent_pose,f.stop_plate(pitch,stops),"ice")
        static = [(f.brake_pad(14.58,15.10),"rubber","Garniture face intérieure"),
                  (f.brake_pad(16.90,17.42),"rubber","Garniture face extérieure"),
                  (f.ring_y(17.42,18.48,10.2,5.75),"metal","Ressort de précharge"),
                  (f.ring_y(18.50,19.16,11.7,5.75),"metal","Plaque acier de précharge"),
                  (f.ring_y(24.82,30.24,8.45,6.15),"accent","Enveloppe ressort de compensation")]
        for degrees in stops:
            angle=f.stop_angle(pitch,degrees)
            x,z=shapes.STOP_R*math.cos(angle),shapes.STOP_R*math.sin(angle)
            static.append((f.hole_y(x,z,29.25,34.7,1.5),"metal",f"Butée acier {degrees:+d}°"))
        for x in (-8,7.5):
            static.extend((
                (self.bolt_y(x,-13.4,-22.3,-12.35),"metal","Tirant M3 support moteur"),
                (self.bolt_y(x,-13.4,12.42,23.52,side=1),"metal","Tirant M3 carter"),
            ))
        if n==2:
            for u in MOUNT_LARGE:
                for z in (-5.1,5.1):
                    static.append((self.bolt_y(-u,z,-45.71,-38.79,1.19,2.3),"metal","Vis traversante M2,5"))
                    static.append((f.ring_y(-40.8,-39.12,2.43,1.27,-u,z),"metal","Écrou M2,5"))
        self.place_hardware(f"STAT_J{n}",f"J{n} · garnitures, ressort et quincaillerie",parent,parent_pose,static)
        moving=[
            (f.brake_disc(),"metal","Disque lié à l’arbre"),
            (f.rotor_stop(),"accent","Doigt de butée et attache du ressort"),
            (f.ring_y(36.76,37.98,5.4,2.52),"metal","Collier de retenue d’arbre"),
        ]
        self.place_hardware(f"ROT_J{n}",f"J{n} · rotor de retenue passive",child,child_pose,moving)

    def electronics(self, base):
        f=self.forms
        tray = f.rounded(-46,24,42,69,6.04,8.6,3)
        for x,y in ((-42,45),(-42,65),(20,45),(20,65)):
            f.cut(tray,f.hole_z(x,y,5.9,9,1.7))
        self.printed_fixed("P15_Platine_cartes","Platine démontable Nano et interface TTL",
                           "01_Platine",base,tray,"ice")
        nano,usb,chip=f.nano()
        self.place_hardware("CTRL","Nano 45 × 18 · réserve volumique",
                           "P15_Platine_cartes",frame((-22.5,54.5,8.65),yaw=90),
                           [(nano,"accent","Carte Nano"),(usb,"metal","Mini USB"),(chip,"dark","Composants")])
        self.add("TTL","Interface TTL 5 V · volume réservé 18 × 26",
                 frame((12,54.5,8.70)),[(f.box(-7.5,7.5,-12,12,0,1.5),"accent","Circuit"),
                                      (f.box(-6.9,6.9,5.0,12,1.5,6.2),"rubber","Embase TTL")])
        self.fixed("P15_Platine_cartes","TTL")
        self.hardware("BTN","Commande de cycle NO · Ø12","01_Platine",frame((-26,-60,0)),
                      f.union(f.hole_z(0,0,-6.45,6.09,5.8),f.hole_z(0,0,6.02,9.55,7.6)),"accent")
        self.hardware("CTRL_VISION","Interface caméra et capteur hors bras",
                      "01_Platine",frame((78,54,0)),
                      f.cut(f.rounded(-12,12,-8,8,6.02,8.15,2),
                            *(f.hole_z(x,0,6,8.4,1.65) for x in (-8,8))),"ice")

    def hand_hardware(self,palm):
        f=self.forms
        cursor=compose(palm,frame(CURSOR))
        parts=[]
        for i,y in enumerate(shapes.BRANCH_Y,1):
            parts.extend((
                (f.axial(-2.47,4.25,.99,y),"metal",f"Réglage de tendon M2 · {i}"),
                (f.ring_x(-2.43,-.94,1.51,1.02,y),"accent",f"Enveloppe de compression · {i}"),
                (f.ring_x(2.73,3.85,1.6,1.01,y),"metal",f"Écrou/accroche · {i}"),
                (f.ring_x(-3.03,-2.49,1.57,1.02,y),"metal",f"Collerette · {i}"),
            ))
        self.place_hardware("T2_COMP","Cinq tiges M2 et ressorts · réglage individuel",
                            "11_Palonnier",cursor,parts)

    def wiring(self, poses):
        from faisceau_table_r03 import Harness
        Harness(self).install(poses)

    def build(self):
        f=self.forms
        base=frame()
        yaw=frame((0,0,shapes.J1_Z))
        shoulder=compose(yaw,frame((0,0,shapes.J2_Z)))
        arm=compose(shoulder,frame(pitch=ANGLES_REPOS[0]))
        elbow=compose(arm,frame((shapes.J3_X,0,0)))
        fore=compose(elbow,frame(pitch=ANGLES_REPOS[1]))
        end=compose(fore,frame((LONGUEURS[1],0,0),pitch=ANGLES_REPOS[2]))
        palm=compose(end,f.wrist_frame())
        self.parameters()
        self.deck()
        self.printed_fixed("02_Socle","02 · Socle et interface J1 préparée","01_Platine",base,f.pedestal(),"dark")
        self.printed("03_Tourelle","03 · Tourelle et chape porteuse J2",yaw,f.turret_link(),"ice",axis="z")
        self.hinge("02_Socle","03_Tourelle","J1 · Azimut indexable manuel","z",(-18,18))
        self.printed("04_Segment_1","04 · Bras supérieur à deux appuis J3",arm,f.segment_one(),"dark",axis="y")
        self.hinge("03_Tourelle","04_Segment_1","J2 · Épaule sur arbre porté","y",shapes.J2_LIMITS)
        self.printed("05_Segment_2","05 · Avant-bras et moyeu J3",fore,f.segment_two(),"dark",axis="y")
        self.hinge("04_Segment_1","05_Segment_2","J3 · Coude XC330 sur arbre porté","y",shapes.J3_LIMITS)
        self.printed_fixed("06_Segment_3","06 · Logement du poignet et tenon","05_Segment_2",end,f.wrist_link())
        self.hardware("VIS_SEG3","Raccord segment 3 · vis M3 et rondelle",
                      "05_Segment_2",end,
                      f.union(f.hole_z(-4.7,0,-9.6,9.5,1.47),f.hole_z(-4.7,0,9.42,11.3,2.6)))
        self.printed("07_Paume","07 · Paume anthropomorphe",palm,f.palm(),"white",axis="x")
        self.hinge("06_Segment_3","07_Paume","J7 · Roulis sur deux roulements","x",shapes.J7_LIMITS)
        for i,(parent,pose) in enumerate((("04_Segment_1",arm),("05_Segment_2",fore))):
            self.printed_fixed(f"0{8+i}_Capot",f"0{8+i} · Capot démontable",parent,pose,
                               f.lid(LONGUEURS[i]),"accent")
        self.axes(2,"03_Tourelle","04_Segment_1",shoulder,arm,ANGLES_REPOS[0],shapes.J2_STOPS)
        self.axes(3,"04_Segment_1","05_Segment_2",elbow,fore,ANGLES_REPOS[1],shapes.J3_STOPS)
        self.base_hardware(base,yaw)
        self.electronics(base)
        self.moveable_hand(palm)
        self.hand_hardware(palm)
        self.wiring({"base":base,"yaw":yaw,"arm":arm,"fore":fore,"end":end,"palm":palm})
        self.root.attributes.add("AURA-01","Reference",TAG)
        self.root.attributes.add("AURA-01","Source",SOURCE)
        self.remember_code()

    def moveable_hand(self,palm):
        f=self.forms
        old_flange,old_hub = f.wrist_flange, f.wrist_hub
        f.wrist_flange,f.wrist_hub = f.wrist_bearing_carrier, f.wrist_shaft
        try:
            super().moveable_hand(palm)
        finally:
            f.wrist_flange,f.wrist_hub = old_flange,old_hub
        stator=compose(compose(palm,frame((shapes.WRIST_SHIFT,0,0))),f.wrist_servo_frame())
        self.hardware("SERVO_J7","MG90S · J7 déporté dans la cassette","06_Segment_3",stator,f.servo(),"rubber")
        for i,x in enumerate((-7.48,-2.14),1):
            self.hardware(f"RLT_J7_{i}",f"J7 · roulement 61800-2RS1 {i}","13_Bride_Poignet",
                          palm,f.wrist_bushing(x),"metal")
        self.hardware("ENT_J7","J7 · entretoise des bagues intérieures","14_Moyeu",palm,
                      f.ring_x(-2.45,-2.17,6.05,5.0),"metal")
        self.hardware("DOG_J7","J7 · entraîneur court et retenue arrière","14_Moyeu",palm,
                      f.ring_x(-8.38,-7.48,5.38,2.39),"accent")
        self.hardware("SERVO_T1","MG90S · T1 tirage des doigts","07_Paume",
                      compose(palm,f.hand_servo_frame()),f.servo(),"rubber")
        self.occ["13_Bride_Poignet"].component.name="13 · Cassette J7 à deux roulements"
        self.occ["14_Moyeu"].component.name="14 · Arbre J7 Ø10 et clé de paume"


def read_vendor(app):
    doc = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    try:
        design = get_design(doc)
        design.designType = fusion.DesignTypes.DirectDesignType
        im = app.importManager
        assert im.importToTarget(im.createSTEPImportOptions(str(VENDOR)),design.rootComponent)
        bodies = list(design.rootComponent.bRepBodies)
        for occ in design.rootComponent.allOccurrences:
            bodies.extend(occ.bRepBodies)
        manager=fusion.TemporaryBRepManager.get()
        return [(manager.copy(b),"rubber" if i<3 else "metal",f"XC330 · solide {i+1:02}")
                for i,b in enumerate(bodies) if b.isSolid]
    finally:
        doc.close(False)


def run(_context: str):
    app=core.Application.get()
    for doc in list(app.documents):
        if not doc.isSaved and doc.name==DRAFT:
            doc.close(False)
    vendors=read_vendor(app)
    doc=app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    doc.name=DRAFT
    rig=Table(doc,vendors)
    rig.build()
    rig.calibrate_axes()
    rig.root.attributes.add("AURA-01","Calibration",json.dumps(rig.calibration))
    rig.root.attributes.add("AURA-01","Traverse",json.dumps(rig.slider_zero))
    rig.root.attributes.add("AURA-01","Flexions",json.dumps(rig.flexion))
    print("r03",app.version,"occurrences",len(rig.occ),"impressions",len(rig.prints),
          "pivots",len(rig.joints),"paramètres",rig.design.userParameters.count)
    from verification_table_r03 import inspect_in_draft
    inspect_in_draft(rig)
