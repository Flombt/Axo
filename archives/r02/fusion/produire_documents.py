"""Met en page la notice et exporte les documents du kit AURA-009 r02."""

import csv
from pathlib import Path
import re
from xml.sax.saxutils import escape

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from etapes_notice import CHAPTER, DIGITS, STAGES
from nomenclature_kit import INDEX, ITEMS, ROOT, SLICER


W, H = landscape(A4)
LEFT, RIGHT = 35, W-35
TEAL = colors.HexColor("#106A70")
DARK = colors.HexColor("#172936")
MID = colors.HexColor("#4E616B")
EDGE = colors.HexColor("#D3DEE1")
PAPER = colors.HexColor("#F0F5F5")
ORANGE = colors.HexColor("#A7471E")
LIGHT_ORANGE = colors.HexColor("#FBEEE5")
BLUE = colors.HexColor("#23659B")
RED = colors.HexColor("#A52D45")
WHITE = colors.white
FONT_PATH = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("UI", str(FONT_PATH/"segoeui.ttf")))
pdfmetrics.registerFont(TTFont("UI-Bold", str(FONT_PATH/"segoeuib.ttf")))
pdfmetrics.registerFont(TTFont("Mono", str(FONT_PATH/"consola.ttf")))
pdfmetrics.registerFontFamily("UI", normal="UI", bold="UI-Bold")

VIEW = ROOT/"Vues_Fusion"
SECTION_SEQUENCE = (["B01","C01","C02","D01","D02","D03","D04","D05",
                     "E01","E02","E03","E04","E05","E06","E07","F01","G01","G02",
                     "H01","I01","I02","J01"])
PAGES = {stage:i for i,stage in enumerate(SECTION_SEQUENCE,5)}
SOURCES = (
    ("TowerPro · MG996R", "https://towerpro.com.tw/product/mg996r/"),
    ("TowerPro · MG90S", "https://towerpro.com.tw/product/mg90s-3/"),
    ("Joy-IT · fiche et brochage du Nano", "https://www.joy-it.net/files/files/Produkte/ARD_NanoV3P/ARD_NANOV3P_Datasheet-EN.pdf"),
    ("Mean Well · fiche du GST25A", "https://www.meanwell.com/Upload/PDF/GST25A/GST25A-SPEC.PDF"),
    ("Arduino · bibliothèque Servo", "https://docs.arduino.cc/libraries/servo/"),
    ("Arduino · choisir le processeur du Nano", "https://support.arduino.cc/hc/en-us/articles/4401874331410-Select-the-right-processor-for-Arduino-Nano"),
)


def write(c,x,y,words,size=11,font="UI",ink=DARK,align="left"):
    c.setFillColor(ink)
    c.setFont(font,size)
    {"left":c.drawString,"right":c.drawRightString,"center":c.drawCentredString}[align](x,y,words)


def para(c,x,y,w,words,size=10,leading=None,ink=DARK,strong=False):
    s = ParagraphStyle("aura", fontName="UI-Bold" if strong else "UI", fontSize=size,
                       leading=leading or size*1.27, textColor=ink)
    p = Paragraph(escape(words),s)
    _, height = p.wrap(w,400)
    p.drawOn(c,x,y-height)
    return y-height


def rect(c,x,y,w,h,fill=PAPER,border=None,r=8):
    c.setFillColor(fill)
    c.setStrokeColor(border or fill)
    c.roundRect(x,y,w,h,r,fill=1,stroke=bool(border))


def line(c,coords,ink=EDGE,width=1):
    c.setStrokeColor(ink)
    c.setLineWidth(width)
    p=c.beginPath()
    p.moveTo(*coords[0])
    for point in coords[1:]:
        p.lineTo(*point)
    c.drawPath(p)


def paragraph_block(c,x,y,w,title,text,kind=None):
    ink, fill = (ORANGE,LIGHT_ORANGE) if kind=="attention" else (TEAL,PAPER)
    s=ParagraphStyle("box",fontName="UI",fontSize=10,leading=12.4,textColor=DARK)
    p=Paragraph(escape(text),s)
    _, n=p.wrap(w-22,300)
    h=25+n+10
    rect(c,x,y-h,w,h,fill=fill)
    write(c,x+11,y-15,title,9,"UI-Bold",ink)
    p.drawOn(c,x+11,y-24-n)
    return y-h


def native_png(c,asset,x,y,w,h):
    source = VIEW/(asset+".png")
    if not source.is_file():
        source = ROOT/(asset+".png")
    with Image.open(source) as raw:
        rgba=raw.convert("RGBA")
        image=rgba.crop(rgba.getbbox())
        factor=min(w/image.width,h/image.height)
        sw,sh=image.width*factor,image.height*factor
        c.drawImage(ImageReader(image),x+(w-sw)/2,y+(h-sh)/2,sw,sh,mask="auto")


def page(c,series,title,sub,chapter=None):
    n=c.getPageNumber()
    c.setFillColor(TEAL)
    c.rect(0,H-7,W,7,fill=1,stroke=0)
    label = f"{series.upper()}    /    {chapter.upper()}" if chapter else series.upper()
    write(c,LEFT,554,label,9.5,"UI-Bold",TEAL)
    write(c,RIGHT,554,"AURA-01   /   KIT R02",9.5,"UI-Bold",TEAL,"right")
    size=29
    while pdfmetrics.stringWidth(title,"UI-Bold",size)>RIGHT-LEFT:
        size-=1
    write(c,LEFT,514,title,size,"UI-Bold")
    end=para(c,LEFT,498,RIGHT-LEFT,sub,11,ink=MID)
    assert end>462
    line(c,[(LEFT,42),(RIGHT,42)])
    write(c,LEFT,25,"AURA-009    •    Révision mécanique r02    •    23 NOV 2026",8.5,ink=MID)
    write(c,RIGHT,25,f"{n:02}",10,"UI-Bold",TEAL,"right")


def table(c,x,y,widths,headers,rows,fs=9.2,padding=4,minimum=22):
    w=sum(widths)
    rect(c,x,y-24,w,24,fill=TEAL,r=4)
    px=x
    for head,width in zip(headers,widths):
        write(c,px+7,y-15.5,head,8.5,"UI-Bold",WHITE)
        px+=width
    cursor=y-24
    for n,row in enumerate(rows):
        cells=[]
        for val,width in zip(row,widths):
            s=ParagraphStyle("cell",fontName="UI",fontSize=fs,leading=fs*1.23,textColor=DARK)
            p=Paragraph(escape(str(val)),s)
            _, h=p.wrap(width-14,160)
            cells.append((p,h))
        height=max(minimum,max(h for _,h in cells)+2*padding)
        if n%2==0:
            c.setFillColor(PAPER)
            c.rect(x,cursor-height,w,height,fill=1,stroke=0)
        px=x
        for (p,h),width in zip(cells,widths):
            p.drawOn(c,px+7,cursor-(height+h)/2)
            px+=width
        line(c,[(x,cursor-height),(x+w,cursor-height)],EDGE,.35)
        cursor-=height
    assert cursor>=48,(c.getPageNumber(),"table trop haute",cursor)
    return cursor


def inventory(c):
    rows=sorted((item for item in ITEMS if item.code.startswith("IMP")),key=lambda k:k.code)
    page(c,"Notice de montage","A · Pièces imprimées","29 pièces pour le robot, plus le coupon d’atelier. Les cotes sont les encombrements des STL orientés.",
         "Inventaire / 1")
    table(c,LEFT,471,[56,188,34,130,76,287],["Réf.","Pièce","Qté","Dimensions","Tranchage","Identification / orientation"],
          [(i.code,i.nom,i.qt,i.specification,i.etat.replace("Tranché ",""),i.note) for i in rows],
          fs=8.6,padding=2.6,minimum=19.4)
    c.showPage()
    page(c,"Notice de montage","A · Moteurs et fixations","Compter les pièces avant montage. Les longueurs candidates se vérifient à blanc avec la visserie du lot.",
         "Inventaire / 2")
    hardware=[i for i in ITEMS if i.code.startswith(("MTR","FIX"))]
    header=["Réf.","Pièce","Qté","Caractéristiques"]
    cols=[47,130,26,177]
    for x,subset in ((LEFT,hardware[:13]),(W/2+6,hardware[13:])):
        table(c,x,471,cols,header,[(i.code,i.nom,i.qt,i.specification) for i in subset],fs=8.7,padding=4,minimum=22)
    c.showPage()
    page(c,"Notice de montage","A · Électronique, câbles et consommables","Chaque code renvoie à sa position, ses étapes et sa référence d’achat quand elle a été identifiée.",
         "Inventaire / 3")
    e=[i for i in ITEMS if i.code.startswith("ELEC")]
    cables=[i for i in ITEMS if i.code.startswith(("CAB","TRN"))]
    header=["Réf.","Pièce","Qté","Caractéristiques"]
    cols=[48,118,25,187]
    for x,subset in ((LEFT,e),(W/2+6,cables)):
        table(c,x,471,cols,header,[(i.code,i.nom,i.qt,i.specification) for i in subset],fs=9,padding=4,minimum=23)
    paragraph_block(c,LEFT,224,378,"OUTILS",
                    "Pied à coulisse, petite lime, tournevis adaptés à M2/M3/M4 et aux moteurs, clés M3/M4, aiguille Ø0,9, pince coupante pour acier, multimètre et alimentation à courant surveillé.")
    paragraph_block(c,LEFT,136,378,"ÉTAT DES RÉFÉRENCES",
                    "Les STL et données d’atelier se trouvent à côté de la notice. Vérifier les pièces candidates et les raccordements sur l’exemplaire imprimé.")
    c.showPage()


def stage_inventory(c,x,y,w,listing):
    write(c,x,y,"PIÈCES À PRÉPARER",8.3,"UI-Bold",TEAL)
    # Each quantity is tied to a unique product code from the full inventory.
    content=[]
    for token in listing.split():
        num,_,ref = token.rpartition("*")
        item=INDEX[ref]
        qt=int(num) if num else item.qt
        content.append(f"{qt}× {ref}")
    col=x
    baseline=y-17
    for entry in content:
        tw=pdfmetrics.stringWidth(entry,"UI-Bold",8.8)+16
        if col+tw>x+w:
            col=x
            baseline-=21
        rect(c,col,baseline-4,tw,16,fill=PAPER,r=4)
        write(c,col+8,baseline,entry,8.8,"UI-Bold")
        col+=tw+4
    return baseline-17


def list_steps(c,x,y,w,lines,size=10.4):
    for n,description in enumerate(lines,1):
        rect(c,x,y-15,16,16,fill=TEAL,r=4)
        write(c,x+8,y-10,str(n),8,"UI-Bold",WHITE,"center")
        y=para(c,x+25,y,w-25,description,size,leading=size*1.29)-9
    return y


def stage(c,step):
    assert c.getPageNumber()==PAGES[step.code]
    page(c,"Notice de montage",step.code+" · "+step.title,step.subtitle,
         CHAPTER[step.code[0]])
    x1, x2, view_w, notes_w = LEFT, 523, 467, RIGHT-523
    write(c,x1,459,"VUE FUSION",9,"UI-Bold",TEAL)
    if step.code=="E04":
        native_png(c,step.asset,x1,241,view_w,204)
        native_png(c,step.detail,x1,71,200,156)
        digit_rows=[(label,p1,p2,p3) for _,label,p1,p2,p3 in DIGITS]
        table(c,x1+209,211,[75,58,58,59],["Doigt","Racine","Milieu","Bout"],digit_rows,fs=8.6,minimum=19)
        write(c,x1,229,"POUCE · 3 AXES VISSÉS",8.2,"UI-Bold",TEAL)
    elif step.code=="E07":
        native_png(c,step.asset,x1+9,159,view_w-18,287)
        write(c,x1+14,148,"BLEU   Tambour → traverse",9,"UI-Bold",BLUE)
        write(c,x1+14,129,"VERT   Traverse → quatre doigts droits",9,"UI-Bold",TEAL)
        write(c,x1+14,110,"ROSE   Traverse → renvoi → pouce",9,"UI-Bold",RED)
        write(c,x1+14,87,"Tracé sous la paume. Les élastiques se montent sur le dos.",9,ink=MID)
    elif step.code=="B01":
        native_png(c,step.asset,x1+12,236,view_w-24,180)
        table(c,x1+15,219,[117,64,64,64,64,64],["Ø du coupon","2,10","2,25","2,40","2,55","2,70"],
              [("Tige acier Ø2","Essai","Essai","Cible CAO","Essai","Essai")],fs=9)
        paragraph_block(c,x1+15,151,436,"IMPRIMER D’ABORD",
                        "PETG · buse 0,4 mm · couche 0,20 mm · cinq périmètres. Comparer le coupon à un vrai œillet horizontal.")
    elif step.code=="G01":
        native_png(c,step.asset,x1+10,120,view_w-20,324)
        write(c,x1+16,95,"Signal S",9,"UI-Bold",BLUE)
        write(c,x1+118,95,"+5 V servos",9,"UI-Bold",RED)
        write(c,x1+249,95,"Masse commune GND",9,"UI-Bold",MID)
    else:
        hero_h = 273
        native_png(c,step.asset,x1+9,177,view_w-18,hero_h)
        write(c,x1+5,154,"POSITION APRÈS EMBOÎTEMENT",8.6,"UI-Bold",TEAL)
        native_png(c,step.asset+"_pose",x1+8,58,211,91)
        if step.code=="E01":
            native_png(c,"E01_Bride_Interieur",x1+218,55,234,100)
            write(c,x1+225,154,"SERVO DANS LA CASSETTE",8.6,"UI-Bold",TEAL)
        elif step.code=="H01":
            native_png(c,"H03_Ensemble_Arriere",x1+222,55,231,100)
            write(c,x1+224,154,"ROBOT TERMINÉ · VUE ARRIÈRE",8.6,"UI-Bold",TEAL)
        else:
            rect(c,x1+234,83,219,45,fill=PAPER)
            write(c,x1+245,110,"VERT    Pièce ajoutée",9,"UI-Bold",TEAL)
            write(c,x1+245,94,"ORANGE    Sens d’insertion",9,"UI-Bold",ORANGE)
    y=stage_inventory(c,x2,459,notes_w,step.parts)
    y=list_steps(c,x2,y,notes_w,step.directions)
    y=paragraph_block(c,x2,y-4,notes_w,"RÉSULTAT ATTENDU",step.result)-8
    y=paragraph_block(c,x2,y,notes_w,"POINT DE VIGILANCE",step.warning,"attention")
    assert y>=51,(step.code,y)
    c.showPage()


def path_line(c,segments,ink,width=1.7):
    line(c,segments,WHITE,width+3.5)
    line(c,segments,ink,width)


def dot(c,x,y,ink):
    c.setFillColor(ink)
    c.circle(x,y,2.5,fill=1,stroke=0)


def electric(c,manual=False):
    if not manual:
        assert c.getPageNumber()==PAGES["G02"]
    page(c,"Manuel technique" if manual else "Notice de montage","G02 · Câbler la puissance et les signaux",
         "Câbler hors tension. Les numéros D correspondent à la sérigraphie du Nano. Vérifier les trois positions du connecteur de chaque servo.",
         "Schéma de raccordement")
    xplus,xgnd=412,485
    rect(c,LEFT,226,194,234,fill=PAPER,border=EDGE)
    write(c,LEFT+13,440,"ELEC-01  /  Nano ARD_NANOV3P",11,"UI-Bold")
    write(c,LEFT+13,421,"CAB-07  ·  mini-USB ↔ source USB 5 V",8.8,ink=MID)
    write(c,LEFT+13,407,"PC ou chargeur USB 5 V (ELEC-07)",8.6,ink=MID)
    rect(c,LEFT,173,194,43,fill=PAPER,border=EDGE)
    write(c,LEFT+13,196,"ELEC-03   ·   Poussoir NO",9.9,"UI-Bold")
    write(c,LEFT+13,181,"CAB-05  ·  D2 ↔ bouton ↔ GND",8.8,ink=MID)
    line(c,[(115,216),(115,226)],BLUE,1.6)
    line(c,[(138,216),(138,226)],MID,1.6)
    line(c,[(xplus,140),(xplus,407)],RED,2.4)
    line(c,[(xgnd,106),(xgnd,407)],MID,2.4)
    write(c,xplus,428,"+5 V",9,"UI-Bold",RED,"center")
    write(c,xgnd,428,"GND",9,"UI-Bold",MID,"center")
    for idx,(axis,pin,cable,servo) in enumerate((("J2","D3","CAB-01","MTR-01 · MG996R"),
                                                  ("J3","D5","CAB-02","MTR-02 · MG90S"),
                                                  ("J7","D6","CAB-03","MTR-03 · MG90S"),
                                                  ("T1","D9","CAB-04","MTR-04 · MG90S"))):
        y=376-idx*41
        write(c,LEFT+13,y+2,axis+"   ·   "+pin,9.1,"UI-Bold",BLUE)
        write(c,256,y+17,cable+"  •  S",8.5,"UI-Bold",BLUE)
        # Gaps at unconnected crossings keep the four signals distinct from both buses.
        path_line(c,[(229,y+3),(585,y+3)],BLUE)
        path_line(c,[(xplus,y-6),(585,y-6)],RED)
        line(c,[(xgnd,y-15),(585,y-15)],MID,1.7)
        dot(c,xplus,y-6,RED)
        dot(c,xgnd,y-15,MID)
        rect(c,585,y-20,222,37,fill=PAPER,border=EDGE,r=5)
        for d,txt,ink in ((3,"S",BLUE),(-6,"+",RED),(-15,"–",MID)):
            write(c,593,y+d-2.6,txt,7,"UI-Bold",ink)
        write(c,619,y,servo,10,"UI-Bold")
        write(c,619,y-13,{"J2":"Épaule","J3":"Coude","J7":"Poignet","T1":"Fermeture des cinq doigts"}[axis],8.6,ink=MID)
    write(c,240,199,"CAB-06   GND Nano → GND commun",8.5,ink=MID)
    path_line(c,[(229,236),(247,236),(247,185),(xgnd,185)],MID)
    dot(c,xgnd,185,MID)
    rect(c,LEFT,98,170,61,fill=PAPER,border=EDGE)
    write(c,LEFT+12,141,"ELEC-02   ·   5 V / 4 A",9.4,"UI-Bold")
    write(c,LEFT+12,127,"GST25A05-P1J · centre +",8.9,ink=MID)
    write(c,LEFT+12,113,"CAB-09 · cordon pour IEC C14",8.3,ink=MID)
    line(c,[(205,140),(xplus,140)],RED,2)
    line(c,[(205,106),(xgnd,106)],MID,2)
    for x,w,label,word in ((220,79,"ELEC-06","Fusible"),(310,86,"ELEC-05","Coupure +5 V")):
        rect(c,x,129,w,33,fill=WHITE,border=EDGE,r=4)
        write(c,x+w/2,148,label,7.2,"UI-Bold",RED,"center")
        write(c,x+w/2,135,word,8.2,"UI",DARK,"center")
    write(c,219,113,"CAB-08   ·   fiche CC 5,5 × 2,1 mm",8.1,ink=MID)
    rect(c,515,103,292,69,fill=PAPER)
    write(c,526,152,"ELEC-04   ·   BORNES DU RAIL SERVOS",8.8,"UI-Bold",TEAL)
    para(c,526,142,272,"Distribuer +5 V et GND en étoile. Le fil CAB-06 joint seulement les masses. Contrôler la polarité du P1J et le sens S/+ /– de chaque servo avant raccordement.",9.1,ink=MID)
    para(c,LEFT,86,772,"Résultat attendu • coupure servos ouverte, le Nano reste lisible par USB et aucune branche servo ne mesure +5 V. Le bouton D2 reste un signal de commande.",9.3,ink=DARK)
    c.showPage()


def cover(c):
    c.bookmarkPage("couverture")
    page(c,"Notice de montage","AURA-01 · Bras robotique","Kit V3 articulé · révision mécanique r02", "Notice d’atelier")
    rect(c,LEFT,65,288,400,fill=PAPER)
    write(c,LEFT+18,432,"ASSEMBLAGE DU KIT",10,"UI-Bold",TEAL)
    para(c,LEFT+18,406,247,"Trois segments, un poignet motorisé et une main blanche de cinq doigts à trois phalanges.",14,leading=18)
    toc=[("A","Inventaire",2),("B","Préparation",5),("C","Base",6),("D","Bras",8),
         ("E","Poignet et main",13),("F","Électronique",20),("G","Câblage",21),
         ("H","Fermeture",23),("I","Mise en service",24),("J","Logiciel",26)]
    for n,(key,name,p) in enumerate(toc):
        y=326-22*n
        write(c,LEFT+18,y,key,9.4,"UI-Bold",TEAL)
        write(c,LEFT+42,y,name,10.1)
        write(c,LEFT+263,y,f"{p:02}",9.7,"UI-Bold",TEAL,"right")
    native_png(c,"H02_Ensemble",335,109,RIGHT-338,350)
    write(c,353,111,"4 servos   /   29 pièces imprimées   /   A4 paysage",10,"UI-Bold",TEAL)
    para(c,353,95,448,"Révision vérifiée en CAO et au tranchage. Monter d’abord un doigt à blanc. Le câblage, les couples en fonctionnement et la prise d’objet restent à essayer sur le robot.",9.4,ink=MID)
    c.showPage()


def first_power(c):
    page(c,"Notice de montage","I01 · Vérifier hors charge",
         "Un support fixe doit tenir le bras pendant les essais. Garder la coupure physique du +5 V à portée.", "Mise en service")
    native_png(c,"H03_Ensemble_Arriere",40,167,333,272)
    paragraph_block(c,LEFT,149,330,"ARRÊT MATÉRIEL",
                    "Couper ELEC-05 et garder le bras soutenu. Couper le bloc secteur. Avant de remettre le rail sous tension, désarmer par STOP ou redémarrer le Nano.","attention")
    y=list_steps(c,394,463,410,(
        "Débrancher les quatre servos et retirer toute charge. Contrôler l’ancrage, les axes, la chape, les fils, les capots ouverts si besoin et la liberté des tendons à la main.",
        "Vérifier au multimètre l’absence de court-circuit, la continuité des masses et les polarités. Mettre sous tension le +5 V servos seul, sans moteurs. Mesurer de P1J à chaque prise.",
        "Actionner ELEC-05. Confirmer que le +5 V disparaît à chaque prise. Vérifier ensuite que le Nano s’allume seul sur USB et que le rail moteur reste coupé.",
        "Installer le programme selon J01, rail servos coupé. Lire INFO. Le firmware annonce PWM inactif à la mise sous tension. Tester D2 par un lancement après calibration complète.",
        "Mettre sous tension un seul servo par essai en I02. Mesurer la tension sur son connecteur en mouvement et le courant d’alimentation. Contrôler d’abord sans tringlerie."),
        11)
    paragraph_block(c,394,y-5,410,"VALIDATION",
                    "Polarités vérifiées, coupure matérielle fonctionnelle et contrôleur accessible. Le poussoir D2 est la seule entrée de cette version. Aucun capteur de position externe ni mesure de courant intégrée.")
    c.showPage()
    page(c,"Notice de montage","I02 · Calibrer un axe à la fois",
         "Ouvrir le moniteur série à 115 200 bit/s. Commencer avec palonnier désengagé et bras soutenu.", "Mise en service")
    y=list_steps(c,LEFT,462,438,(
        "Ne connecter au rail que le servo essayé. Envoyer TEST J2 1500 pour commencer sur l’épaule. C’est une impulsion de référence sur servo désengagé. Relever le sens du mouvement par petits pas.",
        "Couper le rail et engager le palonnier à la référence. Soutenir le bras. Reprendre depuis la référence, par incréments de 10 à 20 µs. Marquer les limites avant point dur, pincement, traction excessive ou baisse de tension.",
        "Envoyer STOP, puis CAL J2 min home max signe avec les mesures. Répéter pour J3, J7, puis T1. Le signe indique vers quel côté se fait le geste. Réduire les limites pour garder une marge.",
        "Lorsque les quatre plages sont mesurées, envoyer SAVE puis INFO. Couper l’énergie moteur, remettre le bras soutenu à HOME et raccorder les quatre axes. Utiliser J01 pour lancer un cycle court.",
        "Valider à vide, d’abord un mouvement puis la séquence. Noter les mesures de tension, courant au déplacement, échauffement, garde des fils et retour complet des doigts."),
        10.5)
    paragraph_block(c,LEFT,y-4,438,"RÉSULTAT ATTENDU",
                    "Les quatre plages viennent du robot monté. La prise d’objet et les mouvements simultanés demandent une campagne distincte.")
    native_png(c,"Apercu_Pouce_Flechi_r02",493,204,310,243)
    paragraph_block(c,493,187,312,"ORDRE DE CALIBRATION",
                    "J2 épaule → J3 coude → J7 roulis → T1 doigts. Vérifier les tendons sans moteur avant de calibrer T1.",
                    "attention")
    c.showPage()


def software(c,technical=False):
    page(c,"Manuel technique" if technical else "Notice de montage","J01 · Installer et lancer le cycle",
         "Le programme d’atelier tourne sur le Nano. Après calibration et armement, le bouton lance le cycle sans PC.", "Logiciel embarqué")
    x1, x2 = LEFT, 472
    write(c,x1,456,"INSTALLER",9.5,"UI-Bold",TEAL)
    y=list_steps(c,x1,438,407,(
        "Ouvrir Firmware/AURA009_Atelier/AURA009_Atelier.ino dans Arduino IDE. Installer Arduino AVR Boards et la bibliothèque Servo. EEPROM fait partie du cœur AVR.",
        "Brancher le mini-USB CAB-07, sélectionner Arduino Nano, le port détecté et le processeur ATmega328P. Si la connexion échoue, utiliser la variante Old Bootloader selon la carte reçue.",
        "Téléverser avec le +5 V servos coupé. Démarrer le moniteur série à 115 200 bit/s. Lire INFO et suivre I02 pour remplir les quatre plages avant SAVE.",
        "Soutenir le bras et le remettre à ses quatre positions de référence avant de rétablir le rail. Maintenir D2 environ deux secondes pour tenir HOME. Relâcher, puis faire un appui bref pour le cycle.",
        "Un appui en mouvement ou STOP au port série coupe le PWM. À l’arrêt, maintenir le bouton deux secondes pour désarmer. En cas de blocage, utiliser la coupure matérielle ELEC-05."
    ),10.5)
    paragraph_block(c,x1,y-2,410,"RÉSULTAT ATTENDU",
                    "J2, J3, J7 puis T1 se déplacent l’un après l’autre et reviennent à HOME. Le cycle utilise un quart de la plage calibrée dans le sens choisi.")
    rect(c,x2,228,326,235,fill=PAPER,border=EDGE)
    write(c,x2+14,443,"COMMANDES DU MONITEUR SÉRIE",9.5,"UI-Bold",TEAL)
    commands=[("INFO","Voir les broches et les plages."),
              ("TEST <axe> <µs>","Servo unique. Premier ordre à 1500, sortie libre."),
              ("CAL <axe> <min> <home> <max> <+|->","Enregistrer en RAM les mesures pour un axe."),
              ("SAVE","Écrire les quatre plages valides en EEPROM."),
              ("STOP","Couper les impulsions. Le rail reste alimenté.")]
    for n,(title,sub) in enumerate(commands):
        y=417-41*n
        write(c,x2+14,y,title,8.65,"Mono")
        write(c,x2+14,y-15,sub,8.5,ink=MID)
    paragraph_block(c,x2,201,326,"ÉTAT DU LOGICIEL",
                    "Compilation pour les deux variantes Nano ATmega328P. Téléversement et fonctionnement sur le robot à valider. Commande locale programmée, sans IA ni retour externe.")
    c.showPage()


def notice():
    c=Canvas(str(ROOT/"Notice_Montage_AURA-01_r02.pdf"),pagesize=(W,H),pageCompression=1)
    c.setTitle("AURA-01 r02 — Notice de montage")
    c.setAuthor("Projet AURA-01")
    cover(c)
    inventory(c)
    for step in STAGES:
        if step.code=="H01":
            electric(c)
        stage(c,step)
    first_power(c)
    software(c)
    assert c.getPageNumber()==27,c.getPageNumber()
    c.save()


def inventory_csv():
    target=ROOT/"Inventaire_Kit_AURA-01_r02.csv"
    with target.open("w",encoding="utf-8-sig",newline="") as stream:
        writer=csv.writer(stream)
        writer.writerow(("Réf.","Catégorie","Composant","Quantité","Cotes et caractéristiques",
                         "Étapes","Pages notice","Statut","Occurrences Fusion","Fichier STL",
                         "STEP assemblage","Lien achat vérifié","Notes"))
        for i in ITEMS:
            writer.writerow((i.code,i.famille,i.nom,i.qt,i.specification,i.etapes,
                             " / ".join(str(PAGES[p]) for p in i.etapes.split()),i.etat,i.fusion,
                             i.stl,i.step,i.url,i.note))


def pdf_file(filename,title):
    c=Canvas(str(ROOT/filename),pagesize=(W,H),pageCompression=1)
    c.setTitle(title)
    c.setAuthor("Projet AURA-01")
    return c


def technical():
    c=pdf_file("Manuel_Technique_AURA-01_r02.pdf","AURA-01 r02 — Manuel technique")
    page(c,"Manuel technique","AURA-01 · Configuration et limites",
         "Révision V3 articulée r02 · robot de table alimenté par le secteur et commandé localement par un Nano.")
    width=370
    native_png(c,"H02_Ensemble",430,173,363,282)
    specs = [
        ("Platine","126 × 100 mm · 4 entretoises de 20 mm"),
        ("Segments","47 / 44 / 40 mm entre repères de construction"),
        ("J1","Pivot vertical manuel · ±30° sondés"),
        ("J2 / Épaule","MG996R · −12° à +12° sondés"),
        ("J3 / Coude","MG90S · −13° à +18° sondés"),
        ("Segment 3","Raccord fixe par tenon et M3 traversante"),
        ("J7 / Roulis","MG90S · ±36° sondés"),
        ("T1 / T2","MG90S · tambour 72° / traverse 7,5 mm"),
        ("Doigts","5 × 3 pivots · fermeture à commande commune"),
    ]
    table(c,LEFT,470,[119,251],["Sous-ensemble","Caractéristique CAO"],specs,fs=10.1,minimum=28)
    paragraph_block(c,LEFT,179,width,"COUPLES GRAVITAIRES ESTIMÉS",
                    "À vide, J2 0,143 N·m et J3 0,100 N·m sur les poses calculées, modèle PETG plein avec masses de quincaillerie estimées. Les valeurs constructeur au blocage à 4,8 V sont ≈0,92 et ≈0,18 N·m. Mesurer le courant et l’échauffement, surtout au coude.",
                    "attention")
    paragraph_block(c,436,169,width,"ACTIONNEURS ET FONCTIONS",
                    "Le poignet roule autour de l’axe de l’avant-bras. Les tendons ferment la main et les rappels élastiques la rouvrent. Le montage de table possède un bouton de commande. La batterie, les capteurs externes et l’IA appartiennent aux autres pistes du projet.")
    c.showPage()

    page(c,"Manuel technique","Fabrication et jeux",
         "Les STL r02 sont orientés en millimètres. Importer les plateaux 3MF dans PrusaSlicer et adapter le profil à l’imprimante réelle.")
    sched=[]
    for plate in SLICER["plateaux"]:
        sched.append((plate["fichier"].split(".")[0],plate["instances"],
                      f"{plate['filament_g']:.2f}".replace(".",",")+" g",
                      plate["duree"].replace("h"," h").replace("m"," min").replace("s"," s"),
                      "Oui" if plate["supports"] else "Non"))
    table(c,LEFT,469,[181,44,72,102,63],["Plateau","Qté","Masse","Temps estimé","Supports"],sched,fs=9.8,minimum=28)
    plate_durations = (plate["duree"] for plate in SLICER["plateaux"] if not plate["fichier"].startswith("00_"))
    total = sum(int(n)*{"h":3600,"m":60,"s":1}[unit] for duration in plate_durations
                for n,unit in re.findall(r"(\d+)([hms])",duration))
    h,m = divmod(round(total/60),60)
    mass = round(SLICER["filament_robot_g"])
    paragraph_block(c,LEFT,286,462,"RÉGLAGES DE DÉPART",
                    f"PETG · buse 0,4 mm · couche 0,20 mm. Les quatre plateaux robot totalisent environ {mass} g et {h} h {m:02d} min, supports compris. Orientations des segments 2 et 3 reprises pour améliorer l’appui. Dégager les poches à écrou et les chenaux.")
    paragraph_block(c,LEFT,186,462,"ORDRE DE VALIDATION",
                    "Coupon Ø2 + index → chape de pouce avec renvoi → joint d’épaule et joint de coude → poignet avec cordon → robot à vide. Commander un exemplaire des pièces candidates avant un lot.")
    native_png(c,"E06_Pouce_pose",522,258,279,206)
    table(c,522,249,[153,132],["Contrôle CAO","Cote / état"],[
        ("Alésage des doigts","Ø2,40 avec toit pointu"),
        ("Jeu latéral chape / œillet","0,54 mm par côté"),
        ("P1 contre la paume","3,24 mm mini mesuré"),
        ("Axe acier commun","Ø2 × 47,5–47,6 mm"),
        ("Commande du pouce","≈4,67 mm de traction"),
        ("Jeu imprimé minimum","À mesurer sur l’index"),
    ],fs=9,minimum=23)
    c.showPage()
    electric(c,True)

    page(c,"Manuel technique","Implanter et entretenir le faisceau",
         "Les pièces de carte et de poussoir dans Fusion représentent leur encombrement. Le rail 5 V puissance est externe à la platine.")
    native_png(c,"G01_Parcours",LEFT,130,429,324)
    write(c,LEFT,111,"Parcours de pose sur la géométrie r02",10,"UI-Bold",TEAL)
    para(c,LEFT,96,426,"Les brins représentent le chemin de montage à repérer. Les boucles restent à mesurer avec les connecteurs, le fil et leur raideur réels.",9.5,ink=MID)
    y=paragraph_block(c,486,472,318,"DÉPART DE PLATINE",
        "Distribuer le rail sur un bornier isolé à quatre départs. Prévoir un boîtier externe fixé, avec coupure accessible et fusible dimensionné. Réunir les masses au bornier et conserver deux alimentations séparées.")
    y=paragraph_block(c,486,y-9,318,"PIVOTS ET RÉSERVES",
        "Faire une marque à la référence du socle. Former une boucle aux articulations et une boucle extérieure au roulis pour T1. Poser les colliers de sorte qu’ils retiennent la gaine sans étrangler les fils.")
    y=paragraph_block(c,486,y-9,318,"IMPULSIONS ET CONNECTEURS",
        "Les signaux S viennent du Nano. Repérer S, + et – sur la fiche du servo et dans sa documentation, contrôler la continuité puis étiqueter les deux extrémités. Vérifier P1J centre positif.")
    y=paragraph_block(c,486,y-9,318,"RISQUE DE COUPLE AU DÉMARRAGE",
        "La coupure du rail libère les servos. Soutenir le bras. Si le 5 V chute ou le Nano redémarre, traiter les masses et les branches avant tout essai.", "attention")
    assert y>=49,y
    c.showPage()
    software(c,True)

    page(c,"Manuel technique","Contrôles effectués et à consigner",
         "La fabrication et la mise en service s’acceptent par essais successifs sur l’exemplaire monté.")
    table(c,LEFT,473,[154,306,310],["Examen","Résultat numérique","Relevé atelier à faire"],[
        ("Interférences du robot","72 poses globales échantillonnées. Aucun volume détecté au seuil 0,006 mm³.",
         "Observer les mouvements lents avec les câbles et le bras soutenu, puis à vide."),
        ("Pouce et index","72 positions ciblées. Aucun chevauchement échantillonné. Jeu mini 0,54 mm à la chape.",
         "Passage à la main de l’ouvert au fermé. Vérifier rappel et sens du renvoi."),
        ("Ordre de montage","48 chemins, 598 positions. Deux insertions en chape rééchantillonnées tous les 0,5 mm.",
         "Passage réel des outils et profondeur des vis. Faire un blanc avant tout serrage."),
        ("Impression","19 références de robot et un coupon tranchés individuellement. Cinq 3MF vérifiés.",
         "Mesurer les trous et l’accroche. Rejeter une fissure d’oreille ou une fourche voilée."),
        ("Alimentation et logiciel","Schéma r02. Compilation Nano ATmega328P / Old Bootloader. Aucun montage alimenté.",
         "Mesurer polarités, chute de tension, action de la coupure, calibration et cinq cycles."),
        ("Couple / résistance","Gravité calculée à vide. Tenue des couches et endurance à qualifier.",
         "Mesurer courant et température. Essais de charge par incréments sur bâti avec arrêt accessible."),
    ],fs=9.5,minimum=45)
    write(c,LEFT,154,"RÉFÉRENCES CONSTRUCTEURS ET OUTILS",9,"UI-Bold",TEAL)
    for n,(title,url) in enumerate(SOURCES):
        x,y=LEFT+(n%2)*386,133-(n//2)*22
        write(c,x,y,title,9.2,ink=BLUE)
        c.linkURL(url,(x,y-2,x+pdfmetrics.stringWidth(title,"UI",9.2),y+11),relative=0)
    c.showPage()
    c.save()


def troubleshooting():
    c=pdf_file("Depannage_AURA-01_r02.pdf","AURA-01 r02 — Guide de dépannage")
    page(c,"Guide de dépannage","Un joint coince ou prend du jeu",
         "Couper le 5 V des servos, soutenir le bras et prendre une photo des repères avant intervention.")
    native_png(c,"E06_Pouce",515,241,284,219)
    native_png(c,"E05_Axe",515,67,284,158)
    table(c,LEFT,466,[115,352],["Symptôme","Contrôle et intervention"],[
        ("Tige impossible à enfiler","Déposer le pouce, retirer les deux retenues et désaligner volontairement un doigt à la fois pour isoler le point dur. Refaire le coupon et contrôler Ø2 sur la tige. E05."),
        ("Doigt lâche ou dur","Ouvrir la chape sur l’établi, retirer la M2×10 et vérifier la poche d’écrou, la bavure du trou ou une vis trop serrée. Remplacer la phalange du même code. E04."),
        ("Pouce contre la paume","Vérifier r02, la position de la chape, la tête des deux M2×10 et la liberté de l’index. Une fourche voilée ou un reste de support suffit à bloquer. E06."),
        ("Le pouce s’ouvre en tirant","Vérifier le demi-tour autour du manchon avant puis le passage dans la chape. Ne pas croiser avec le fil de l’index. Détendre, refaire l’essai à la main. E07."),
        ("Les doigts restent fermés","Contrôler les rappels dorsaux et l’absence de pincement sur la traverse. Libérer l’écrou trop serré, passer une aiguille dans le guide puis régler la tension. E03–E07."),
    ],fs=10.1,minimum=58)
    c.showPage()
    page(c,"Guide de dépannage","Un servo chauffe, broute ou reste immobile",
         "Essayer chaque moteur hors charge avec les autres prises déconnectées du rail. La coupure matérielle doit rester à portée.")
    table(c,LEFT,470,[185,585],["Symptôme","Contrôle et intervention"],[
        ("Aucun servo ne bouge","Lire INFO. Vérifier les quatre calibrations, l’appui long puis bref, et 5 V au bornier. Distinguer la coupure du rail servos et le bouton D2."),
        ("Un servo seul ne bouge","Vérifier l’étiquette côté carte et moteur, le signal S et la polarité de la fiche. Mesurer le rail à sa prise. Retirer le palonnier et répéter TEST sur son axe uniquement."),
        ("Le Nano redémarre","Contrôler chargeur, continuité de la masse commune, serrage du bornier et chute du +5 V servo au connecteur. Retirer toute charge. Examiner les pics de courant sur un seul axe à la fois."),
        ("Le coude tremble ou chauffe","Soutenir le bras, vérifier pivot M3, liberté du faisceau, calibration et alignement du palonnier. Réduire l’amplitude. Si la tenue à vide reste instable, traiter J3 avant tout nouvel essai."),
        ("Débattement dans le mauvais sens","Sur le servo désengagé, relever ce qu’une impulsion plus haute produit. Corriger le signe dans CAL, contrôler HOME et sauvegarder."),
        ("Le motoréducteur tourne sans fin","Vérifier que le modèle reçu est bien un servo de position. Stopper et remplacer la variante 360°. Recalibrer avec le servo de remplacement."),
        ("J7 tire sur le fil T1","Ouvrir le montage avant une nouvelle rotation. Refaire la boucle extérieure à J7 et raccourcir le débattement si la réserve est insuffisante."),
    ],fs=10,minimum=46)
    c.showPage()
    page(c,"Guide de dépannage","Accéder aux composants internes",
         "Les références renvoient à la notice de montage et au CSV. Remettre l’axe réparé en position de référence avant le nouvel essai.")
    native_png(c,"E01_Bride",512,244,285,222)
    native_png(c,"E03_Transmission",525,63,266,174)
    table(c,LEFT,474,[115,348],["À remplacer","Chemin de démontage"],[
        ("J7 · MTR-03","Débrancher T1, détacher la boucle extérieure, retirer la paume (2 M2×6), puis la vis centrale et le moyeu. Retirer les 4 M2×12 et sortir la cassette par l’avant. E01–E02."),
        ("T1 · MTR-04","Libérer la traction, déposer le tambour et les deux vis de pattes, sortir le MG90S selon l’ouverture de la selle. Retirer la chape de pouce si elle masque l’accès. E03."),
        ("J2 / J3","Enlever le capot adjacent et soutenir les deux tronçons. Retirer vis centrale et axe passif, sortir le segment vers le haut, puis déposer le corps du moteur. D01–D04."),
        ("Phalange droite","Retirer les deux retenues de l’axe et la chape du pouce avec ses deux M2×10. Rentrer ou sortir la tige côté pouce. Remplacer le code IMP de la phalange cassée. E04–E06."),
        ("Nano ou poussoir","Débrancher USB et rail, détacher les étiquettes en gardant l’ordre, couper le collier du Nano ou enlever l’écrou du bouton dessous. Reprendre le contrôle G02."),
    ],fs=10.1,minimum=58)
    c.showPage()
    c.save()


if __name__=="__main__":
    inventory_csv()
    notice()
    technical()
    troubleshooting()
