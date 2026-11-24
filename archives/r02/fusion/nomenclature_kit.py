"""Références communes à la notice et à l’inventaire du kit r02."""

from dataclasses import dataclass
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
NODE = "AURA-01_V3_Articulee_Montage_r02"
CAD = json.loads((ROOT/"Verification_Montage.json").read_text(encoding="utf-8"))
SLICER = json.loads((ROOT/"Verification_Tranchage.json").read_text(encoding="utf-8"))

VENDOR = {
    "J2": "https://www.intermodel.fr/servos/6705-mg-996r-rotation-a-180-55gr11kg-tower-pro-servo-tower-pro-mg996-995.html",
    "MG90S": "https://www.flashrc.com/fr/servos-rc-precision-fiabilite-pour-modelisme/3661-servo-micro-mg90s-metal-towerpro-8800223313015.html",
    "Nano": "https://www.reichelt.com/fr/fr/shop/produit/carte_nano_compatible_arduino_atmega328p_mini-usb-395379",
    "bloc": "https://www.tme.eu/fr/details/gst25a05-p1j/alimentations-de-bureau/mean-well/",
    "acier": "https://www.flashrc.com/fr/corde-a-piano-acier/3149-corde-a-piano-cap-20mm.html",
    "nylon": "https://www.decathlon.fr/p/fil-de-peche-line-4x4-250m/_/R-p-194133",
}

@dataclass(frozen=True)
class Item:
    code: str
    famille: str
    nom: str
    qt: int
    specification: str
    etapes: str
    etat: str
    fusion: str = ""
    stl: str = ""
    step: str = ""
    url: str = ""
    note: str = ""


PRINTS = {
    "01_Platine": ("IMP-01", "Platine", "C01", "Face plane sur le plateau"),
    "02_Socle": ("IMP-02", "Socle évasé", "C02", "Face supérieure sur le plateau"),
    "03_Tourelle": ("IMP-03", "Tourelle et chape d’épaule", "C02", "Face supérieure en bas selon 3MF"),
    "04_Segment_1": ("IMP-04", "Segment 1 · bras supérieur", "D02", "Sur la joue selon 3MF"),
    "05_Segment_2": ("IMP-05", "Segment 2 · avant-bras", "D04", "Joue plane au sol. Supports selon 3MF"),
    "06_Segment_3": ("IMP-06", "Segment 3 · logement du poignet", "D05", "Face haute au sol. Supports selon 3MF"),
    "07_Paume": ("IMP-07", "Paume blanche", "E02", "Face dorsale horizontale en bas"),
    "08_Capot": ("IMP-08", "Capot long du segment 1", "H01", "Face plane en bas. 23,9 mm de long"),
    "09_Capot": ("IMP-09", "Capot court du segment 2", "H01", "Face plane en bas. 20,9 mm de long"),
    "10_Tambour": ("IMP-10", "Tambour de traction T1", "E03", "Sur la joue du tambour. Gorge Ø12"),
    "11_Palonnier": ("IMP-11", "Traverse des cinq tendons T2", "E03", "Traverse au sol selon 3MF"),
    "12_Support_Pouce": ("IMP-12", "Chape amovible du pouce", "E04 E06", "Retirer les supports du dessous"),
    "13_Bride_Poignet": ("IMP-13", "Bride et cassette J7", "E01", "Face selon 3MF. Dégager les quatre vis"),
    "14_Moyeu": ("IMP-14", "Moyeu de roulis à clé", "E02", "Face selon 3MF. Dégager l’accès à la vis centrale"),
    "Phalange_14": ("IMP-15", "Phalange de pas 14", "E04", "P1 / I2 / M2 / A2 / U1"),
    "Phalange_12p5": ("IMP-16", "Phalange de pas 12,5", "E04", "P2 / U2"),
    "Bout_11": ("IMP-17", "Bout de doigt de pas 11", "E04", "P3 / U3. Deux œillets transversaux"),
    "Phalange_16": ("IMP-18", "Phalange de pas 16", "E04", "I1 / M1 / A1"),
    "Bout_12p5": ("IMP-19", "Bout de doigt de pas 12,5", "E04", "I3 / M3 / A3. Deux œillets transversaux"),
    "15_Coupon_Jeux": ("IMP-20", "Coupon d’atelier Ø2", "B01", "Ø2,10 / 2,25 / 2,40 / 2,55 / 2,70"),
}


def printed_items():
    support = {x["reference"]: x["supports_generes"] for x in SLICER["preuves_individuelles"]}
    for shape in CAD["nomenclature"]:
        name = shape["reference"]
        code, title, step, note = PRINTS[name]
        dims = " × ".join(f"{x:.2f}".rstrip("0").rstrip(".").replace(".",",") for x in shape["dimensions_mm"])
        state = "Tranché avec supports" if support[name] else "Tranché sans supports"
        yield Item(code,"Impression" if shape["instances"] else "Préparation",title,
                   shape["quantite_robot"] or 1, f"{dims} mm",step,state,
                   ", ".join(shape["instances"]),f"STL/{shape['stl']}",
                   NODE+".step" if shape["instances"] else "",note=note)


def bought(code, family, name, qty, spec, stage, cad="", vendor="", note="",
           state="Réalisation à valider sur établi"):
    return Item(code,family,name,qty,spec,stage,state,cad,
                step=NODE+".step" if cad else "",url=VENDOR.get(vendor,""),note=note)


MOTORS = [
    bought("MTR-01","Moteur","TowerPro MG996R · épaule J2",1,"Servo de position 180° · 4,8–6,6 V constructeur","D01 G01 G02","MG996R · Épaule J2","J2"),
    bought("MTR-02","Moteur","TowerPro MG90S · coude J3",1,"Servo de position · MG90S","D03 G01 G02","MG90S · Coude J3","MG90S"),
    bought("MTR-03","Moteur","TowerPro MG90S · roulis J7",1,"Servo de position · MG90S","E01 G01 G02","MG90S · Rotation du poignet","MG90S"),
    bought("MTR-04","Moteur","TowerPro MG90S · doigts T1",1,"Servo de position · MG90S","E03 G01 G02","MG90S · Fermeture des cinq doigts","MG90S"),
]

FIXINGS = [
    ("FIX-01","Entretoise de platine M4",4,"Longueur 20 mm. Corps ≤ Ø9,5","C01","Entretoise M4","", "Traversante. Dégage le bouton"),
    ("FIX-02","Fixation de platine M4",4,"M4 × (24 mm + épaisseur support + prise écrou)","C01","","", "4 vis + 4 rondelles + 4 écrous. M4×40 pour un support traversant de 8–9 mm. Adapter à l’établi"),
    ("FIX-03","Vis fraisée du socle",2,"M3×8 · fraisée 90° · tête ≤ Ø6,5","C02","","","Fût dans les deux bossages du socle"),
    ("FIX-04","Pivot manuel et retenue",1,"Vis M4×18, 1 rondelle M4 fine, 1 écrou frein M4","C02","M4 · Axe de socle orientable","","Contrôler la pile, la saillie et la tête en atelier"),
    ("FIX-05","Fixation des pattes du MG996R",4,"M2,5×8 vis pour plastique · candidate","D01","","","Pattes / bagues du lot à mesurer. Trous pilotes CAO Ø2,64. Short-list à vérifier avec le servo"),
    ("FIX-06","Vis des pattes MG90S",6,"2 par moteur · vis fournies compatibles avec pilote Ø1,84","D03 E01 E03","","","Longueur utile selon le kit moteur. Ne pas percer la coque"),
    ("FIX-07","Palonnier du servo avec vis centrale",4,"1 palonnier court 2 bras + 1 vis du lot par moteur","D02 D04 E02 E03","Palonniers J2/J3/J7/T1 · enveloppes","","Cannelures et vis propres à chaque lot. Entraxe latéral CAO 11,6"),
    ("FIX-08","Vis latérales du palonnier",8,"2 par palonnier · diamètre/longueur sur échantillon","D02 D04 E02 E03","","","Utiliser la vis du lot adaptée. Rondelle fine si portée trop petite"),
    ("FIX-09","Axe passif et écrou captif",2,"M3×14 tête basse + écrou M3 standard · 1 set par pivot","D02 D04","Axe passif M3 · J2/J3 et Écrou M3 captif","","Tête côté joue extérieure. Vérifier saillie et libre rotation"),
    ("FIX-10","Fixation du tenon du segment 3",1,"Vis M3×25 + 1 rondelle + 1 écrou frein M3","D05","","","Cote candidate. Assembler à blanc et mesurer l’empilement"),
    ("FIX-11","Vis de bride J7",4,"M2×12 · tête bombée Ø≤4,1 · DIN 7985","E01","M2×12 · Bride de poignet","","Tournevis de tige Ø≤3,6"),
    ("FIX-12","Vis du moyeu et de la traverse",4,"M2×6 · DIN 7985 · 2 + 2","E02 E03","M2×6 · Moyeu / Butée du répartiteur","","Les deux vis de butée ne traversent pas le rail"),
    ("FIX-13","Axes des doigts et fixations du pouce",13,"M2×10 tête bombée DIN 7985 · 11 + 2","E04 E06","Axes P1–P3, I2–U3 et vis du support du pouce","","Chape et phalanges, montage à blanc"),
    ("FIX-14","Écrou captif M2",13,"Écrou M2 standard · sur plats 4 mm","E04 E06","Écrous P1–P3, I2–U3 et support du pouce","","Écrous minces uniquement après vérification de la prise"),
    ("FIX-15","Axe commun des quatre doigts",1,"Tige Ø2 acier · couper à 47,5–47,6 mm","E05","Axe acier commun aux quatre doigts","acier","Arêtes cassées. La tige est vendue en longueur 1 m"),
    ("FIX-16","Vis de retenue de l’axe commun",2,"M2×3 tête bombée · 1 par côté","E05","Vis d’arrêt","","Ne bloque pas la rotation de la tige"),
    ("FIX-17","Rondelle de retenue de l’axe",2,"Øint ≈2,2 · Øext 5,0 · ép. ≈0,45 mm","E05","Rondelle d’arrêt","","Recouvre le bout de la tige sans le serrer"),
    ("FIX-18","Vis de renvoi du pouce",1,"M3×8 · tête bombée","E06","M3×8 · Renvoi de tendon du pouce","","Sous la paume"),
    ("FIX-19","Rondelle de renvoi du pouce",2,"Øint ≈3,1 · Øext ≈6,3 · ép. 0,45–0,50 mm","E06","Rondelles de renvoi","","Tenir le fil dans la gorge lisse"),
    ("FIX-20","Manchon lisse de renvoi du pouce",1,"Øint 3,1 × Øext 4,8 × L 3,3 mm","E06","Entretoise lisse · renvoi du pouce","","Prélever dans un tube lisse et ébavurer les deux faces"),
    ("FIX-21","Vis des capots",4,"M2×4 · tête bombée · 2 par capot","H01","","","Les vis plus longues peuvent bloquer dans le fond du pilote"),
    ("FIX-22","Attache du Nano et points de retenue",6,"6 colliers souples ≤2,5 mm de large · 1 Nano + 5 faisceau","F01 G01","","","Glisser un isolant entre PCB et collier si besoin"),
]

ELECTRIC = [
    ("ELEC-01","Carte Joy-IT Nano",1,"ARD_NANOV3P · ATmega328P 16 MHz · 5 V · mini-USB","F01 G02 J01","Nano ATmega328P · encombrement","Nano","Comparer l’orientation de la prise à la platine"),
    ("ELEC-02","Alimentation secteur des servos",1,"Mean Well GST25A05-P1J · 5 V / 4 A nominal","G02 I01","","bloc","Externe à la platine. Ne pas ouvrir le boîtier secteur"),
    ("ELEC-03","Bouton de lancement",1,"Poussoir NO à deux bornes · montage nominal Ø12","C01 F01 G02","Bouton et corps inférieur · encombrements","","Mesurer profondeur et orientation des cosses. Contrôler à l’ohmmètre"),
    ("ELEC-04","Répartiteur puissance 5 V / GND",1,"Bornier isolé ≥5 A, 4 branches + arrivée et GND logique","F01 G02","","","Monter à l’extérieur du volume balayé, dans un boîtier fixé"),
    ("ELEC-05","Coupure du rail servos",1,"Interrupteur indépendant accessible · ≥5 A CC à 5 V","F01 G02 I01","","","Coupure matérielle du +5 V en amont du bornier. Bouton de lancement distinct"),
    ("ELEC-06","Fusible et porte-fusible",1,"Protection du rail 5 V · cible ≤4 A à valider","F01 G02 I01","","","Dimensionner selon courant mesuré et ampacité du câblage"),
    ("ELEC-07","Source USB pour le Nano",1,"USB 5 V régulé · PC atelier ou chargeur USB 5 V","G02 J01","","","Pour le cycle sans PC, utiliser un chargeur USB compatible"),
]

CABLES = [
    ("CAB-01","J2 · prolongateur servo",1,"3 voies S / + / – · réserve de départ 150 mm","G01 G02","","","D3 / rail +5 V / GND → MG996R"),
    ("CAB-02","J3 · prolongateur servo",1,"3 voies S / + / – · réserve de départ 200 mm","G01 G02","","","D5 / rail +5 V / GND → MG90S coude"),
    ("CAB-03","J7 · prolongateur servo",1,"3 voies S / + / – · réserve de départ 250 mm","G01 G02","","","D6 / rail +5 V / GND → MG90S poignet"),
    ("CAB-04","T1 · prolongateur servo",1,"3 voies S / + / – · réserve de départ 300 mm","G01 G02","","","D9 / rail +5 V / GND → MG90S main"),
    ("CAB-05","Liaison du poussoir",1,"2 conducteurs souples · départ 150 mm","F01 G02","","","D2 / GND Nano → bouton NO"),
    ("CAB-06","Masse logique commune",1,"1 fil · départ 150 mm","G02","","","GND Nano → GND du bornier. Mesurer la continuité"),
    ("CAB-07","Câble mini-USB de données",1,"USB A vers mini-B · longueur selon source","G02 J01","","","ELEC-01 → PC ou chargeur USB 5 V"),
    ("CAB-08","Entrée CC, coupure et fusible",1,"Fiche 5,5 × 2,1 mm femelle + fil souple ≥0,75 mm²","G02","","","ELEC-02 → ELEC-06 → ELEC-05 → ELEC-04 sur +. P1J centre positif. Vérifier au multimètre"),
    ("CAB-09","Cordon secteur du bloc Mean Well",1,"Cordon local adapté à l’entrée IEC C14 du bloc","G02","","","Bloc ELEC-02 → prise secteur. Cordon du fournisseur ou CE adapté"),
    ("CAB-10","Gaine, isolation et étiquettes",1,"1 lot de gaine souple fendue + thermorétractable + étiquettes","F01 G01 G02","","","Dimensionner à sec. Aucun raccord secteur monté dans le robot"),
    ("TRN-01","Tendons de doigts",5,"Nylon Ø0,40 mm · 5 brins de départ 150 mm","E07","","nylon","Un par doigt. Identifier P/I/M/A/U"),
    ("TRN-02","Cordage tambour–traverse",1,"Nylon Ø0,40 mm · brin de départ 140 mm","E07","","nylon","Dimension de coupe avec marge de réglage, à essayer"),
    ("TRN-03","Retours des doigts",5,"Élastique fin ≈Ø0,8–1 mm · un par doigt","E07","","","Longueur à régler. Retour dorsal avec faible prétension"),
]

ITEMS = list(printed_items()) + MOTORS
for family, rows in (("Visserie", FIXINGS),("Électronique", ELECTRIC),("Faisceau / transmission", CABLES)):
    ITEMS.extend(bought(code,family,name,qty,spec,stage,cad,vendor,note)
                 for code,name,qty,spec,stage,cad,vendor,note in rows)

INDEX = {item.code: item for item in ITEMS}
assert len(INDEX) == len(ITEMS)
assert sum(x.qt for x in ITEMS if x.famille == "Impression") == 29
