"""Montage natif r02 et vérification des enveloppes d’assemblage."""

from hashlib import sha256
import json
import math
from pathlib import Path
import sys
import tempfile

import adsk.core as core
import adsk.fusion as fusion

OUT = Path(__file__).resolve().parent
for folder in ("AURA-008_Main_Poignet", "AURA-007_Bras_Table",
               "AURA_V3/Generateur_AURA_V3", "AURA-009_Montage"):
    sys.path.insert(0, str(OUT.parent/folder))

from construire_main import Brazo, camera, capture, get_design
from formes_articulees import CURSOR, DRUM, WIND
from formes_montage import (
    AXLE_HALF, CAP_BOLTS, FINGERS, HUB_BOLTS, JOINT_HALF, ROW_X, THUMB_FIX, THUMB_GUIDE, WorkshopForms,
)
from geometrie import compose, frame, point, vector
from geometrie_table import HAUTEUR_EPAULE, LONGUEURS, VIS_SERVO


TITLE = "AURA-01 — V3 articulée — Montage r02"
TAG = "AURA-009 · V3 articulée · Montage r02"
REPORT = OUT/"Verification_Montage.json"
ARCHIVE = OUT/"AURA-01_V3_Articulee_Montage_r02.f3d"
HOME = (0, 0, 0, 0, 0)
PRINT_FRAMES = {
    "02_Socle": {"roll": 180}, "03_Tourelle": {"roll": 180}, "04_Segment_1": {"roll": 90},
    "05_Segment_2": {"roll": 90}, "06_Segment_3": {"roll": 180},
    "07_Paume": {"roll": 180}, "10_Tambour": {"roll": -90},
    "11_Palonnier": {"pitch": 90}, "13_Bride_Poignet": {"pitch": -90}, "14_Moyeu": {"pitch": 90},
}


def write(data):
    REPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


class Workshop(Brazo):
    def __init__(self, document):
        self.design = get_design(document)
        self.design.designType = fusion.DesignTypes.ParametricDesignType
        self.root = self.design.rootComponent
        self.forms = WorkshopForms(self.design)
        self.occ, self.prints, self.markers, self.joints = {}, {}, {}, {}
        self.flexion, self.print_groups = {}, {}
        self.native_links = False
        self.lengths = {}

    def build(self):
        super().build()
        f = self.forms
        self.root.attributes.itemByName("AURA-01", "Reference").value = TAG
        for joint, key in ((2,"04_Segment_1"), (3,"05_Segment_2")):
            self.hardware(f"CAPTIF_J{joint}", f"Écrou M3 captif · J{joint}", key,
                          self.occ[key].transform2, self.hex_nut(3.32, 5.72, 2.75, 1.52))
        for x in (-54, 51):
            for y in (-40, 40):
                b = f.cut(f.hole_z(0, 0, -20, 0, 4.75),
                          f.hole_z(0, 0, -20.1, 0.1, 2.05))
                name = f"Entretoise M4 · {x} / {y}"
                self.hardware(name, name, "01_Platine", frame((x, y, 0)), b, "metal")
        b = f.hole_z(0, 0, -14.7, 0.25, 5.55)
        self.hardware("BTN_BAS", "Corps inférieur du bouton · encombrement",
                      "01_Platine", frame((43, -28, 0)), b, "rubber")

    def hex_nut(self, low, high, flat_half=2, hole=1.025):
        f = self.forms
        extent = flat_half*1.5
        nut = f.box(-extent, extent, low, high, -flat_half, flat_half)
        for angle in (60, 120):
            other = f.place(f.box(-extent-0.1, extent+0.1, low-0.05, high+0.05,
                                  -flat_half, flat_half), frame(pitch=angle))
            f.op(nut, other, fusion.BooleanTypes.IntersectionBooleanType)
        return f.cut(nut, f.hole_y(0, 0, low-0.1, high+0.1, hole))

    def fasten_digit(self, code, parent, at):
        f = self.forms
        shaft = f.union(f.hole_y(0, 0, -JOINT_HALF-0.06, 10-JOINT_HALF, 0.994),
                        f.hole_y(0, 0, -JOINT_HALF-1.58, -JOINT_HALF-0.025, 1.98))
        key = "Vis_" + code
        self.add(key, f"{code} · Vis M2×10 et écrou captif", at,
                 [(shaft, "metal", f"Axe vissé · {code}"),
                  (self.hex_nut(3.01, 4.61), "metal", f"Écrou · {code}")])
        self.fixed(parent, key)

    def moveable_hand(self, palm):
        f = self.forms
        identity = palm
        for code, label, parent, shape, appearance in (
            ("12_Support_Pouce", "12 · Support démontable du pouce", "07_Paume", f.thumb_bracket(), "white"),
            ("13_Bride_Poignet", "13 · Bride et support du servo J7", "06_Segment_3", f.wrist_flange(), "ice"),
            ("14_Moyeu", "14 · Moyeu tournant démontable", "07_Paume", f.wrist_hub(), "white"),
        ):
            self.printed(code, label, identity, shape, appearance)
            self.fixed(parent, code)
        self.hand_fastenings(palm)

        self.printed("10_Tambour", "10 · Tambour de traction", compose(palm, frame(DRUM)),
                     f.drum(), "accent", -90, "y")
        self.hinge("07_Paume", "10_Tambour", "T1 · Fermeture groupée des doigts", "y", (-2, WIND+2))
        self.hardware("PAL_T1", "Palonnier du tambour · enveloppe", "10_Tambour",
                      compose(palm, f.hand_servo_frame()), f.horn())
        cursor = self.printed("11_Palonnier", "11 · Traverse des cinq tendons", compose(palm, frame(CURSOR)),
                              f.cursor(), "accent", 0, "x")
        edge = next(e for e in self.markers["11_Palonnier"].edges if core.Circle3D.cast(e.geometry))
        geo = fusion.JointGeometry.createByCurve(edge, fusion.JointKeyPointTypes.CenterKeyPoint)
        collection = self.root.asBuiltJoints
        spec = collection.createInput(cursor, self.occ["07_Paume"], geo)
        if not spec.setAsSliderJointMotion(fusion.JointDirections.ZAxisJointDirection):
            raise RuntimeError("Course du répartiteur refusée.")
        self.slider = collection.add(spec)
        self.slider.name = "T2 · Course du répartiteur"
        self.slider.isLightBulbOn = self.markers["11_Palonnier"].isLightBulbOn = False

        rod = f.hole_y(ROW_X, 0, -AXLE_HALF, AXLE_HALF, 0.993)
        self.hardware("ROD", "Axe acier commun aux quatre doigts", "07_Paume", palm, rod)
        for side in (-1, 1):
            x = ROW_X-3.15
            lo, hi = sorted((side*23.89, side*24.34))
            washer = f.cut(f.hole_y(x, 0, lo, hi, 2.52), f.hole_y(x, 0, lo-0.1, hi+0.1, 1.09))
            start, end = sorted((side*21.30, side*24.41))
            head0, head1 = sorted((side*24.34, side*25.88))
            screw = f.union(f.hole_y(x, 0, start, end, 0.84), f.hole_y(x, 0, head0, head1, 1.95))
            self.add(f"Retenue_{side}", f"Retenue d’axe · côté {side:+}", palm,
                     [(washer, "metal", f"Rondelle d’arrêt {side:+}"),
                      (screw, "metal", f"Vis d’arrêt {side:+}")])
            self.fixed("07_Paume", f"Retenue_{side}")

        for code, label, start, yaw, roll, lengths, angles in FINGERS:
            at = compose(palm, frame(start, yaw=yaw, roll=roll))
            previous = "12_Support_Pouce" if code == "P" else "07_Paume"
            for i, (length, angle) in enumerate(zip(lengths, angles), 1):
                key = f"{code}{i}"
                title = f"{label} · Phalange {i}"
                self.printed(key, title, at, f.phalanx(length, i==3), "white", axis="y")
                self.hinge(previous, key, f"{key} · {title}", "y", (-1.5, angle+2))
                self.flexion[key] = angle
                self.lengths[key] = length
                self.print_groups[key] = f"{'Bout' if i==3 else 'Phalange'}_{str(length).replace('.','p')}"
                if i>1 or code=="P":
                    self.fasten_digit(key, previous, at)
                at = compose(at, frame((length, 0, 0)))
                previous = key

    def hand_fastenings(self, palm):
        f = self.forms
        for i, (x,y) in enumerate(THUMB_FIX, 1):
            stem = f.union(f.hole_z(x, y, -4.76, 5.31, 0.985),
                           f.hole_z(x, y, -6.28, -4.72, 1.98))
            nut = f.place(self.hex_nut(2.84, 4.44), frame((x,y,0), roll=90))
            key = f"Vis_Support_{i}"
            self.add(key, f"M2×10 · Support du pouce {i}", palm,
                     [(stem,"metal",f"Vis support {i}"), (nut,"metal",f"Écrou support {i}")])
            self.fixed("07_Paume",key)
        for i, (y,z) in enumerate(CAP_BOLTS, 1):
            bolt = f.union(f.axial(-14.01, -1.95, 0.84, y,z),
                           f.axial(-2.02, -0.48, 1.98, y,z))
            self.hardware(f"Vis_Bride_{i}", f"M2×12 · Bride de poignet {i}",
                          "06_Segment_3", palm, bolt)
        for i, (x,y) in enumerate(HUB_BOLTS, 1):
            bolt = f.union(f.hole_z(x,y,-1.32,4.72,0.83),
                           f.hole_z(x,y,4.70,6.25,1.98))
            self.hardware(f"Vis_Moyeu_{i}", f"M2×6 · Moyeu {i}", "07_Paume",palm,bolt)
        for i,y in enumerate((-19.8,19.8),1):
            bolt = f.union(f.hole_z(50.76,y,-11.80,-5.79,0.81),
                           f.hole_z(50.76,y,-13.35,-11.76,1.98))
            self.hardware(f"Vis_Traverse_{i}", f"M2×6 · Butée du répartiteur {i}", "07_Paume",palm,bolt)
        x, y = THUMB_GUIDE
        sleeve = f.cut(f.hole_z(x,y,-10.22,-6.92,2.42),
                       f.hole_z(x,y,-10.28,-6.88,1.55))
        for lo,hi in ((-10.72,-10.22),(-6.92,-6.47)):
            flange = f.cut(f.hole_z(x,y,lo,hi,3.15),f.hole_z(x,y,lo-0.1,hi+0.1,1.56))
            self.add(f"Guide_{lo}", "Rondelle de renvoi du pouce", palm,
                     [(flange,"metal",f"Rondelle · renvoi {lo}")])
            self.fixed("07_Paume",f"Guide_{lo}")
        self.hardware("Guide_lisse", "Entretoise lisse · renvoi du pouce", "07_Paume",palm,sleeve)
        bolt = f.union(f.hole_z(x,y,-10.76,-2.71,1.17),
                       f.hole_z(x,y,-12.83,-10.74,2.78))
        self.hardware("Vis_Guide","M3×8 · Renvoi de tendon du pouce","07_Paume",palm,bolt)

    def weights_after(self, joint):
        weights = super().weights_after(joint)
        extra_prints = ("12_Support_Pouce","13_Bride_Poignet","14_Moyeu")
        fasteners = ("Vis_","Retenue_")
        for key, occ in self.occ.items():
            if key not in extra_prints and key != "ROD" and not key.startswith((*fasteners,"Guide_")):
                continue
            density = 1.27 if key in extra_prints else 7.85
            for body in occ.component.bRepBodies:
                weights.append((occ, body.volume*density, body.physicalProperties.centerOfMass))
        for key in (("CAPTIF_J2","CAPTIF_J3") if joint=="04_Segment_1" else ("CAPTIF_J3",)):
            occ = self.occ[key]
            body = occ.component.bRepBodies.item(0)
            weights.append((occ, body.volume*7.85, body.physicalProperties.centerOfMass))
        return weights

    def assembly_checks(self):
        """Run tool and assembly sweeps in the neutral pose, excluding removed parts."""
        f = self.forms
        self.position(HOME)
        used = {}
        for key, occ in self.occ.items():
            if key in self.prints:
                name = self.prints[key][1]
                # Assembly scenarios need just the component's own printed geometry.
                used[key] = f.manager.copy(occ.bRepBodies.itemByName(name))
        results = []

        def sweep(label, moving, direction, samples, context, obstacles):
            poses, contacts, maximum = [], [], 0.0
            fixed = {key: used[key] if key in used else once(key) for key in obstacles}
            for distance in samples:
                form = f.manager.copy(moving)
                f.place(form, frame(tuple(distance*p for p in direction)))
                at = f.place(form, context)
                for key, obstacle in fixed.items():
                    overlap = vol(at, obstacle)
                    if overlap > 0.006:
                        contacts.append((distance, key, round(overlap, 4)))
                        maximum = max(maximum, overlap)
                poses.append(distance)
            results.append({"operation": label, "positions_mm": poses, "obstacles": list(obstacles),
                            "interferences": contacts, "maximum_mm3": round(maximum, 4)})

        def once(key):
            body = next(b for b in self.occ[key].bRepBodies if b.name != "Repère de liaison")
            return f.manager.copy(body)

        def vol(a, b):
            bounds_a, bounds_b = a.boundingBox, b.boundingBox
            for axis in "xyz":
                if (getattr(bounds_a.minPoint,axis) >= getattr(bounds_b.maxPoint,axis) or
                    getattr(bounds_b.minPoint,axis) >= getattr(bounds_a.maxPoint,axis)):
                    return 0
            aux = f.manager.copy(a)
            if not f.manager.booleanOperation(aux, b, fusion.BooleanTypes.IntersectionBooleanType):
                raise RuntimeError("Échec du calcul du corridor d’assemblage.")
            return aux.volume*1000 if aux.isSolid else 0

        # A whole common shaft enters from the left with the thumb and stops removed.
        palm = self.occ["07_Paume"].transform2
        sweep("Axe commun des quatre doigts depuis le côté du pouce",
              f.hole_y(ROW_X, 0, -AXLE_HALF, AXLE_HALF, 1.0), (0,-1,0), range(53,-1,-1),
              palm, ("07_Paume","I1","M1","A1","U1","SERVO_T1","11_Palonnier"))
        sweep("Dépose du support du pouce vers le côté",
              f.thumb_bracket(), (0,-1,0), range(0,19), palm,
              ("07_Paume","SERVO_T1","11_Palonnier","14_Moyeu"))
        sweep("Insertion de la traverse par le bout des rails, doigts démontés",
              f.cursor(), (1,0,0), range(12,-1,-1),
              compose(palm, frame(CURSOR)), ("07_Paume","SERVO_T1","14_Moyeu"))
        sweep("MG90S de main dans la selle, support du pouce retiré",
              f.servo(), (0,0,-1), range(34,-1,-1), compose(palm,f.hand_servo_frame()),
              ("07_Paume","14_Moyeu","11_Palonnier","10_Tambour"))
        sweep("MG996R dans la chape, bras non monté",
              f.large_servo(), (0,0,-1), range(47,-1,-1),
              compose(self.occ["03_Tourelle"].transform2, f.servo_lat(0, HAUTEUR_EPAULE)),
              ("03_Tourelle",))
        sweep("MG90S de coude depuis l’extérieur, avant-bras non monté", f.servo(), (0,0,-1),
              range(35,-1,-1), compose(self.occ["04_Segment_1"].transform2,f.servo_lat(LONGUEURS[0])),
              ("04_Segment_1",))
        module = f.union(f.wrist_flange(), f.place(f.servo(), f.wrist_servo_frame()))
        sweep("Servo de roulis déjà vissé sur sa bride, insertion par l’avant",
              module, (1,0,0), range(36,-1,-1), palm, ("06_Segment_3",))
        sweep("Moyeu enfilé dans la bride de roulis, paume déposée",
              f.wrist_hub(),(1,0,0),range(10,-1,-1),palm, ("13_Bride_Poignet","SERVO_J7"))
        sweep("Paume déposée dans l’axe à partir du moyeu tournant",
              f.palm(), (1,0,0), range(13,-1,-1), palm, ("14_Moyeu","13_Bride_Poignet"))
        for n, parent, child in ((2,"03_Tourelle","04_Segment_1"),(3,"04_Segment_1","05_Segment_2")):
            sweep(f"Axe passif M3 J{n}, accès par la joue extérieure",
                  f.pin(), (0,1,0), range(23,-1,-1), self.occ[f"AXE_J{n}"].transform2,
                  (parent,child,f"CAPTIF_J{n}"))
        sweep("Tenon du troisième segment dans l’avant-bras",
              f.inside_wrist(), (1,0,0), range(12,-1,-1), self.occ["06_Segment_3"].transform2,
              ("05_Segment_2",))
        sweep("Axe M4 du socle avant montage du bras",
              f.hole_z(0,0,-10.3,3.64,2), (0,0,1), range(18,-1,-1),
              self.occ["03_Tourelle"].transform2, ("02_Socle","03_Tourelle"))
        for i,(x,y) in enumerate(THUMB_FIX,1):
            sweep(f"Tournevis du support de pouce, vis {i}, par-dessous",
                  f.hole_z(x,y,-25,-6.32,2.30), (0,0,0), (0,), palm,
                  ("07_Paume","12_Support_Pouce","SERVO_T1"))
        for i,(y,z) in enumerate(CAP_BOLTS,1):
            sweep(f"Tournevis de bride Ø3,6, vis {i}, paume déposée",
                  f.axial(-0.43,17.5,1.80,y,z), (0,0,0), (0,), palm,
                  ("13_Bride_Poignet","06_Segment_3"))
        for letter in ("P","I","M","A","U"):
            for n in ((1,2,3) if letter=="P" else (2,3)):
                child = f"{letter}{n}"
                parent = f"{letter}{n-1}" if n>1 else "12_Support_Pouce"
                bit = f.union(f.hole_y(0,0,-6.15,5.34,1.0),
                              f.hole_y(0,0,-17.8,-5.02,1.94))
                sweep(f"Vis latérale M2 {child}, doigt seul sur l’établi",
                      bit, (0,-1,0), range(13,-1,-1), self.occ[child].transform2, (parent,child))
        visited = set()
        for code,length in self.lengths.items():
            group = self.print_groups[code]
            if group in visited:
                continue
            visited.add(group)
            sweep(f"Aiguille Ø0,9 dans le guide du {group}",
                  f.axial(1.94,length+0.8,0.45,z=-1.93), (1,0,0), range(9,-1,-1),
                  self.occ[code].transform2, (code,))
            sweep(f"Ouverture du guide du {group} côté paume",
                  f.hole_z(3.25,0,-7,-1.94,0.43), (0,0,0), (0,),
                  self.occ[code].transform2, (code,))
        for n,y in enumerate((-18.6,-6.2,6.2,18.6),1):
            sweep(f"Entrée accessible du tendon dans la paume, doigt {n}",
                  f.hole_z(ROW_X-10.57,y,-9.8,-3.37,0.45), (0,0,0), (0,),
                  palm, ("07_Paume",))
            sweep(f"Sortie du guide débouchant, doigt {n}",
                  f.axial(ROW_X-10.75,ROW_X-3.52,0.45,y=y,z=-3.36), (1,0,0), range(7,-1,-1),
                  palm, ("07_Paume",))
        return results


def export_prints(app, rig):
    groups = {}
    for key in rig.prints:
        groups.setdefault(rig.print_groups.get(key, key), []).append(key)
    out = OUT/"STL"
    out.mkdir(exist_ok=True)
    scratch = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    design = get_design(scratch)
    design.designType = fusion.DesignTypes.DirectDesignType
    g = rig.forms
    items = []
    sources = []
    for group, keys in groups.items():
        occ, name, _ = rig.prints[keys[0]]
        b = occ.component.bRepBodies.itemByName(name)
        sources.append((group, keys, g.manager.copy(b), PRINT_FRAMES.get(group, {})))
    sources.append(("15_Coupon_Jeux", [], g.coupon(), {}))
    for group, keys, shape, orientation in sources:
        g.place(shape, frame(**orientation))
        lo, hi = shape.boundingBox.minPoint, shape.boundingBox.maxPoint
        g.place(shape, frame((-(lo.x+hi.x)*5, -(lo.y+hi.y)*5, -lo.z*10)))
        b = design.rootComponent.bRepBodies.add(shape)
        path = out/(group+".stl")
        ex = design.exportManager
        options = ex.createSTLExportOptions(b, str(path))
        options.isBinaryFormat = True
        options.meshRefinement = fusion.MeshRefinementSettings.MeshRefinementHigh
        if not ex.execute(options) or path.stat().st_size<=84:
            raise RuntimeError(f"STL refusé : {group}.")
        items.append({"reference":group, "instances":keys, "quantite_robot":len(keys),
                      "stl":path.name, "dimensions_mm":[round((a-b)*10,4) for a,b in
                                                     zip(hi.asArray(),lo.asArray())],
                      "orientations_deg":orientation, "volume_cm3":round(shape.volume,4),
                      "sha256":sha256(path.read_bytes()).hexdigest()})
    scratch.close(False)
    return items


def export_archive(app, doc, rig):
    with tempfile.TemporaryDirectory(prefix="Aura009_") as area:
        file = Path(area)/ARCHIVE.name
        e = rig.design.exportManager
        if not e.execute(e.createFusionArchiveExportOptions(str(file))):
            raise RuntimeError("Échec de l’archive r02.")
        importer = app.importManager
        reopened = importer.importToNewDocument(importer.createFusionArchiveImportOptions(str(file)))
        root = get_design(reopened).rootComponent
        counts = root.occurrences.count, root.asBuiltJoints.count, root.motionLinks.count
        assert counts == (rig.root.occurrences.count, rig.root.asBuiltJoints.count, 16)
        reopened.close(False)
        ARCHIVE.write_bytes(file.read_bytes())
    doc.activate()
    return {"fichier":ARCHIVE.name,"sha256":sha256(ARCHIVE.read_bytes()).hexdigest(),
            "occurrences":counts[0],"liaisons":counts[1],"couplages":counts[2]}


def measure_thumb(app, rig):
    keys = ("P1","P2","P3")
    rig.position(HOME)
    links = list(rig.root.motionLinks)
    was_linked = rig.native_links
    for link in links:
        link.isSuppressed = True
    rig.native_links = False
    first = rig.occ["P1"].bRepBodies.itemByName("FDM · P1")
    palm = rig.occ["07_Paume"].bRepBodies.itemByName("FDM · 07_Paume")
    support = rig.occ["12_Support_Pouce"].bRepBodies.itemByName("FDM · 12_Support_Pouce")
    results = []
    p1 = (0, 8, 16, 24, 31, 33)
    neighbors = ("07_Paume","12_Support_Pouce","Retenue_-1","ROD","SERVO_T1",
                 "P1","P2","P3","Vis_P1","Vis_P2","Vis_P3","I1","I2","I3","Vis_I2","Vis_I3")
    objects = core.ObjectCollection.create()
    for key in neighbors:
        for b in rig.occ[key].bRepBodies:
            if b.name != "Repère de liaison":
                objects.add(b)
    for frac in (0,1):
        for index in ("I1","I2","I3"):
            rig.set_rotation(index, frac*rig.flexion[index])
        for theta in p1:
            for angle2 in (0, 19, 39):
                for angle3 in (0, 36):
                    states = (theta,angle2,angle3)
                    for key,angle in zip(keys,states):
                        rig.set_rotation(key,angle)
                    query = rig.design.createInterferenceInput(objects)
                    query.areCoincidentFacesIncluded = False
                    overlaps = rig.design.analyzeInterference(query)
                    found = [(r.entityOne.name,r.entityTwo.name,round(r.interferenceBody.volume*1000,5))
                             for r in overlaps if r.interferenceBody.volume*1000 > 0.006
                             and any(r.entityOne.name.endswith(k) or r.entityTwo.name.endswith(k) for k in keys)]
                    results.append({"angles_deg":states,"index_fraction":frac,
                                    "jeu_paume_mm":round(app.measureManager.measureMinimumDistance(first,palm).value*10,4),
                                    "jeu_chape_mm":round(app.measureManager.measureMinimumDistance(first,support).value*10,4),
                                    "interferences":found})
    for key in (*keys,"I1","I2","I3"):
        rig.set_rotation(key,0)
    for link in links:
        link.isSuppressed = False
    rig.native_links=was_linked
    rig.position(HOME)
    return results


def thumb_view(app, rig):
    view = app.activeViewport
    body = rig.occ["12_Support_Pouce"].bRepBodies.itemByName("FDM · 12_Support_Pouce")
    center = body.boundingBox
    at = tuple((a+b)*5 for a,b in zip(center.minPoint.asArray(),center.maxPoint.asArray()))
    c = view.camera
    c.cameraType = core.CameraTypes.OrthographicCameraType
    c.isSmoothTransition = False
    c.target = point(at)
    c.eye = point(tuple(a+b for a,b in zip(at, (60,-87,122))))
    c.upVector = vector((0,0,1))
    c.setExtents(114/10, 100/10)
    view.camera = c
    view.refresh()
    return view


def run(_context: str):
    app = core.Application.get()
    old_drafts = [d for d in app.documents if not d.isSaved and d.name==TITLE+" (contrôle)"]
    draft = app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    draft.name = TITLE+" (contrôle)"
    rig = Workshop(draft)
    rig.build()
    rig.calibrate_axes()
    static_hits = rig.interference()
    test_thumb = measure_thumb(app, rig)
    paths = rig.assembly_checks()
    view = thumb_view(app, rig)
    capture(view, OUT/"Apercu_Pouce_r02.png", 1400, 1100, transparent=True)
    camera(app)
    data = {"fusion":app.version,"tag":TAG,"pieces":len(rig.prints),"occurrences":len(rig.occ),
            "interferences_repos":static_hits,
            "pouce":{"poses":test_thumb,
                     "jeu_min_paume_mm":min(x["jeu_paume_mm"] for x in test_thumb),
                     "jeu_min_chape_mm":min(x["jeu_chape_mm"] for x in test_thumb)},
            "montage":paths,
            "renvoi_pouce":{"point_xy_mm":THUMB_GUIDE,"retrait_traverse_mm":7.5,
                "course_geometrique_approchee_mm":round(math.hypot(THUMB_GUIDE[0]-CURSOR[0]+7.5,
                                                                  THUMB_GUIDE[1]+16.8)
                                                        -math.hypot(THUMB_GUIDE[0]-CURSOR[0],
                                                                    THUMB_GUIDE[1]+16.8),3)}}
    write(data)
    if not (static_hits or any(x["interferences"] for x in test_thumb)
            or any(p["interferences"] for p in paths)):
        poses, intersections, estimated = rig.check()
        data["global"] = {"poses":len(poses),"interferences":intersections,"couples_Nm":estimated}
        data["pivots"] = len(rig.joints)
        data["calibration"] = rig.calibration
        data["calibration_traverse"] = rig.slider_zero
        data["angles_flexion_nominale_deg"] = rig.flexion
        write(data)
        if not intersections:
            rig.link_fingers()
            data["couplages"] = rig.root.motionLinks.count
            data["archive"] = export_archive(app,draft,rig)
            write(data)
            data["nomenclature"] = export_prints(app,rig)
            draft.activate()
            capture(camera(app), OUT/"Apercu_Bras_Montage_r02.png", 1680, 1040, transparent=True)
            thumb = thumb_view(app,rig)
            rig.position((0,0,0,0,1))
            thumb.refresh()
            capture(thumb, OUT/"Apercu_Pouce_Flechi_r02.png", 1400, 1100, transparent=True)
            rig.position(HOME)
            camera(app)
            for other in old_drafts:
                other.close(False)
            write(data)
    print(json.dumps({"repos":static_hits,"pouce_collisions":[x for x in test_thumb if x["interferences"]][:4],
                      "jeu_paume":data["pouce"]["jeu_min_paume_mm"],"jeu_chape":data["pouce"]["jeu_min_chape_mm"],
                      "montage":[(p["operation"],p["maximum_mm3"],p["interferences"][:3]) for p in paths if p["interferences"]],
                      "global":data.get("global"),"exports":len(data.get("nomenclature",[]))},
                     ensure_ascii=False))
