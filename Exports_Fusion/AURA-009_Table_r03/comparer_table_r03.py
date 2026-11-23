"""Images de comparaison et graphiques statiques à partir des résultats r03."""

from collections import Counter
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


PAPER="#f3f7f8"
INK="#13252e"
SMALL="#48616c"
RULE="#d6e0e4"
BEFORE="#8e9ea6"
AFTER="#087789"
STATUS={
    "corrigé numériquement":"#087789",
    "partiellement corrigé":"#58a5aa",
    "en attente de qualification physique":"#c87c18",
    "non corrigé":"#586974",
}


def font(size,bold=False):
    f=Path("C:/Windows/Fonts")/("segoeuib.ttf" if bold else "segoeui.ttf")
    return ImageFont.truetype(str(f),size) if f.is_file() else ImageFont.load_default(size)


def page(height,title,detail):
    im=Image.new("RGB",(1600,height),PAPER)
    d=ImageDraw.Draw(im)
    d.text((67,43),title,font=font(52,True),fill=INK)
    d.text((69,111),detail,font=font(25),fill=SMALL)
    d.line((70,162,1530,162),fill=RULE,width=2)
    return im,d


def box(d,x,y,w,h,color):
    if w>0:
        d.rounded_rectangle((x,y,x+w,y+h),radius=min(5,w/2),fill=color)


def scores(folder,series):
    im,d=page(1140,"Maturité technique du bras","Même barème sur 100 · r02 de table et AURA-009 r03")
    x,width=445,980
    for value in range(0,101,20):
        px=x+width*value/100
        d.line((px,204,px,1010),fill=RULE,width=2)
        d.text((px,180),str(value),font=font(24),fill=SMALL,anchor="mm")
    for i,row in enumerate(series):
        y=227+69*i
        d.text((70,y+18),row["nom"],font=font(25,True),fill=INK)
        for j,key,col in ((0,"avant",BEFORE),(1,"apres",AFTER)):
            w=width*row[key]/100
            box(d,x,y+26*j,w,17,col)
            d.text((x+w+10,y-7+26*j),str(row[key]),font=font(22,True),fill=INK)
    box(d,79,1055,24,21,BEFORE)
    d.text((114,1050),"r02",font=font(23),fill=SMALL)
    box(d,190,1055,24,21,AFTER)
    d.text((225,1050),"r03",font=font(23),fill=SMALL)
    d.text((350,1050),"La validation physique reste à faire et la commande r03 est à adapter.",font=font(23),fill=SMALL)
    im.save(folder/"maturite_r02_r03.png")


def issues(folder,items):
    im,d=page(801,"Évolution des problèmes P0 à P4","Priorités d’origine conservées · les statuts r03 décrivent la preuve disponible")
    x,width=250,1130
    totals=Counter(p["p"] for p in items)
    unit=width/max(totals.values())
    for i,key in enumerate(("P0","P1","P2","P3","P4")):
        y=202+i*96
        d.text((68,y+9),key,font=font(35,True),fill=INK)
        d.text((162,y-4),"r02",font=font(22),fill=SMALL)
        d.text((162,y+34),"r03",font=font(22),fill=SMALL)
        box(d,x,y,totals[key]*unit,24,BEFORE)
        d.text((x+totals[key]*unit+12,y-4),str(totals[key]),font=font(23,True),fill=INK)
        row=Counter(p["statut"] for p in items if p["p"]==key)
        px=x
        for name,color in STATUS.items():
            n=row[name]
            if n:
                box(d,px,y+37,n*unit-2,27,color)
                d.text((px+n*unit/2,y+50),str(n),font=font(19,True),fill="white",anchor="mm")
                px+=n*unit
    for i,(title,col) in enumerate(STATUS.items()):
        px=73+(i%2)*725
        y=707+(i//2)*33
        box(d,px,y,20,20,col)
        d.text((px+30,y-4),title,font=font(23),fill=SMALL)
    im.save(folder/"problemes_r02_r03.png")


def picture(atelier,file,size):
    src=Image.open(atelier/file).convert("RGBA")
    if src.getextrema()[3][0]==0:
        src=src.crop(src.getbbox())
    src.thumbnail(size,Image.Resampling.LANCZOS)
    tile=Image.new("RGB",size,"#e8eff1")
    tile.paste(src,((size[0]-src.width)//2,(size[1]-src.height)//2),src)
    return tile


def comparison(root,folder):
    origin=root/"AURA-01_Notice_Montage"
    if not origin.is_dir():
        origin=root/"Rendus"
    pairs=(
        ("Ensemble", "Apercu_Bras_Montage_r02.png", "renders/r03/01_trois_quarts.png",
         "Platine étroite et actionnement direct", "Platine 180 × 144 mm et gardes latérales"),
        ("Épaule", "Vues_Fusion/D03_Pivot_pose.png", "wireframes/r03/04_coupe_epaule.png",
         "Montage de l’axe côté servo", "Arbre Ø5 à deux bagues et support M2,5 traversant"),
        ("Coude", "Vues_Fusion/D04_Pivot_pose.png", "wireframes/r03/05_coupe_coude.png",
         "Pivot avec MG90S", "XC330, arbre porté et retenue passive"),
        ("Poignet", "Vues_Fusion/E01_Bride_Interieur.png", "wireframes/r03/06_coupe_poignet.png",
         "Cassette moteur de roulis", "Cassette et arbre Ø10 sur deux roulements"),
        ("Main", "Apercu_Pouce_r02.png", "renders/r03/09_main.png",
         "Chape démontable du pouce", "Ligaments renforcés et cinq réglages de tendon"),
    )
    row_height=425
    im,d=page(246+len(pairs)*row_height,"AURA-009 · r02 et r03",
              "Comparaison des assemblages et des articulations · vues CAO à échelles différentes")
    for x,title in ((65,"r02 · Référence"),(820,"r03 · Articulations portées")):
        d.text((x,184),title,font=font(32,True),fill=INK)
    for i,(label,before,after,before_caption,after_caption) in enumerate(pairs):
        y=241+i*row_height
        d.text((65,y),label,font=font(24,True),fill=INK)
        for x,path,name,caption in ((65,origin,before,before_caption),(820,root/"docs",after,after_caption)):
            im.paste(picture(path,name,(730,332)),(x,y+36))
            d.text((x+2,y+374),caption,font=font(23),fill=SMALL)
        d.line((65,y+414,1550,y+414),fill=RULE,width=2)
    im.save(folder/"comparaison_mecanique_r02_r03.png")


def main(root):
    folder=root/"docs/diagnostic"
    data=json.loads((folder/"donnees_r02_r03.json").read_text(encoding="utf8"))
    scores(folder,data["scores"])
    issues(folder,data["problemes"])
    comparison(root,folder)


if __name__=="__main__":
    main(Path(sys.argv[1]))
