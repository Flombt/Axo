"""Graphiques de contre-audit à partir des résultats datés et du registre."""
from collections import Counter
import json
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

P=Path("docs/diagnostic/corrections")
O=P/"graphiques"
COLORS=["#126e69","#65a887","#ebae62","#a85656","#798598","#5c547c"]
OLD="#8093a6"
NEW="#116f69"
ORDER=("Résolu et vérifié numériquement","Corrigé, qualification physique nécessaire",
       "Partiellement corrigé","Non résolu","Non applicable après reconception",
       "Bloqué par une limitation extérieure")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(fig,name):
    fig.savefig(O/name,dpi=185,facecolor=fig.get_facecolor(),bbox_inches="tight",pad_inches=.19)
    plt.close(fig)


def maturity(data):
    domains=list(data["domaines"])
    labels=[label.replace("Intelligence artificielle","IA") for label in domains]
    old=[sum(x["v5_audit"]) for x in data["domaines"].values()]
    new=[sum(x["stabilisation"]) for x in data["domaines"].values()]
    pos=np.arange(len(domains))
    fig,ax=plt.subplots(figsize=(9.1,6.1),layout="constrained")
    ax.barh(pos+.17,old,.31,color=OLD,label="V5 roulis · audit")
    ax.barh(pos-.17,new,.31,color=NEW,label="V5 stabilisation")
    for y,num in zip(pos,new):
        ax.text(num+1,y-.17,f"{num}",va="center",size=9,color="#153c3c")
    ax.set(yticks=pos,yticklabels=labels,xlim=(0,100),xlabel="Note sur 100")
    ax.invert_yaxis()
    ax.grid(axis="x",alpha=.18)
    ax.legend(frameon=False,loc="lower right")
    ax.set_title("Maturité technique par domaine",loc="left",weight="bold",size=15)
    save(fig,"01_maturite_par_domaine.png")


def statuses():
    lines=Path("RAPPORT_CORRECTIONS.md").read_text(encoding="utf-8").splitlines()
    records=[]
    for line in lines:
        match=re.match(r"\| (A01-P[0-4]-\d+) \| (P[0-4]) \| ([^|]+) \|",line)
        if match:
            records.append((match[1],match[2],match[3].strip()))
    if len(records)!=35 or any(s not in ORDER for _,_,s in records):
        raise ValueError("Les 35 statuts du registre doivent être renseignés.")
    fig,axes=plt.subplots(1,2,figsize=(11,5.3),layout="constrained",gridspec_kw={"width_ratios":[1.0,1.5]})
    levels=["P"+str(i) for i in range(5)]
    totals=Counter(p for _,p,_ in records)
    unique_status=Counter(s for _,_,s in records)
    for i,l in enumerate(levels):
        parts = Counter(s for _,lvl,s in records if lvl==l)
        lower=0
        for s,color in zip(ORDER,COLORS):
            v=parts[s]
            if v:
                axes[0].bar(i,v,bottom=lower,color=color,width=.64)
                axes[0].text(i,lower+v/2,str(v),ha="center",va="center",color="white",weight="bold",size=9)
            lower+=v
        axes[0].text(i,lower+.3,str(totals[l]),ha="center",size=9)
    axes[0].set(xticks=range(5),xticklabels=levels,ylim=(0,19),ylabel="Identifiants")
    axes[0].set_title("Criticités d’origine",loc="left",weight="bold")
    short=["Résolu numériquement","Qualification physique","Partiel","Non résolu",
           "Non applicable","Limitation extérieure"]
    for i,(s,color) in enumerate(zip(ORDER,COLORS)):
        v=unique_status[s]
        axes[1].barh(i,v,color=color)
        axes[1].text(v+.24,i,str(v),va="center")
    axes[1].set(yticks=range(6),yticklabels=short,xlim=(0,max(unique_status.values())+3))
    axes[1].invert_yaxis()
    axes[1].set_title("Statuts après correction",loc="left",weight="bold")
    save(fig,"02_criticites_et_statuts.png")


def resources(d):
    calc=load(P/"calculs.json")
    slices=load("manufacturing/Anycubic/verification.json")
    per_machine={}
    for row in slices["profiles"]:
        machine=row["machine"]
        r=per_machine.setdefault(machine,{"grammes":0,"heures":0,"planches":0})
        if row["group"] != "Coupons":
            r["grammes"]+=sum(p["grams"] for p in row["plates"])
            r["heures"]+=sum(p["seconds"] for p in row["plates"])/3600
            r["planches"]+=len(row["plates"])
    fig,axes=plt.subplots(2,2,figsize=(10.5,7.6),layout="constrained")
    ax=axes[0,0]
    v=[149.48,88.74,188.74]
    ax.barh([2,1,0],v,color=[OLD,NEW,"#bb6860"])
    ax.axvline(150,color="#502c30",ls="--",lw=1.1,label="Plafond")
    ax.set(yticks=[2,1,0],yticklabels=["V5 roulis · cible","Éléments chiffrés",
                                     "Correction · avec provisions"],xlim=(0,225),xlabel="€ TTC")
    for i,x in enumerate(v):
        ax.text(x+2,2-i,f"{x:.2f}".replace(".",","),va="center",size=8)
    ax.set_title("Budget d’achat · filament en stock",loc="left",weight="bold")
    ax.legend(frameon=False,loc="lower right")
    ax=axes[0,1]
    new=calc["loads"][0]["total_mass_g"]
    ax.barh([1,0],[774.86,new],color=[OLD,NEW])
    ax.set(yticks=[1,0],yticklabels=["V5 roulis","V5 stabilisation"],xlim=(0,max(new,775)*1.17),
           xlabel="g calculés, assemblage à vide")
    ax.text(774.86+17,1,"775",va="center")
    ax.text(new+17,0,str(round(new)),va="center")
    ax.set_title("Masse calculée, PETG plein",loc="left",weight="bold")
    ax=axes[1,0]
    covers={k:v for k,v in per_machine.items() if v["planches"]>0}
    names=[k.replace("_"," ") for k in covers]
    values=[v["heures"] for v in covers.values()]
    if values:
        ax.barh(list(range(len(names))),values,color=NEW)
        for i,(time,rec) in enumerate(zip(values,covers.values())):
            label = f"{time:.1f} h · {rec['grammes']:.0f} g".replace(".", ",")
            ax.text(time+.4,i,label,va="center",size=8)
        ax.set(xlim=(0,max(values)*1.42),yticks=range(len(names)),yticklabels=names,xlabel="h, hors coupons")
    ax.set_title("Temps et matière tranchés",loc="left",weight="bold")
    ax.text(.0,-.28,"V5 roulis · aucun plateau de la révision à comparer",transform=ax.transAxes,size=8)
    ax=axes[1,1]
    notes=list(d["fabrication"].values())
    old=sum(q["audit"] for q in notes)
    new=sum(q["stabilisation"] for q in notes)
    ax.barh([1,0],[old,new],color=[OLD,NEW])
    ax.set(yticks=[1,0],yticklabels=["V5 roulis","V5 stabilisation"],xlim=(0,100),xlabel="Points sur 100")
    ax.text(old+2,1,str(old),va="center")
    ax.text(new+2,0,str(new),va="center")
    ax.set_title("Préparation à la fabrication",loc="left",weight="bold")
    save(fig,"03_budget_masse_tranchage_preparation.png")


def guards():
    calc=load(P/"calculs.json")["table"]
    fig,ax=plt.subplots(figsize=(8.5,4.2),layout="constrained")
    axes=["Anciennes butées\navec rehausse","Butées physiques\nJ7 sur 360°","Commande couplée"]
    values=[r["clearance_lower_bound_mm"] for r in calc]
    bars=ax.barh(axes,values,color=[COLORS[3],COLORS[1],COLORS[0]],height=.52)
    ax.axvline(0,color="#28283a",lw=1.0)
    ax.set(xlim=(-11,max(values)+9),xlabel="Distance minimale garantie par le calcul géométrique [mm]")
    for bar,val in zip(bars,values):
        ax.text(val+(1.0 if val>0 else -1.0),bar.get_y()+bar.get_height()/2,
                f"{val:+.1f}".replace(".",","),ha="left" if val>0 else "right",va="center",weight="bold")
    ax.set_title("Garde au plan de pose · rehausse 90 mm",loc="left",weight="bold")
    ax.grid(axis="x",alpha=.20)
    save(fig,"04_garde_table.png")

def label_part(ax, label, target, position, color="#116f69"):
    ax.annotate(label, xy=target, xytext=position, color=color, fontsize=10,
                fontweight="bold", arrowprops={"arrowstyle":"->","color":color,"lw":1.6},
                bbox={"fc":"white","ec":"none","pad":3})


def pinch_compare():
    folder=P/"visuels"
    before=Path("docs/diagnostic/latest/wireframes/09_pince_annotee.png")
    after=folder/"04_fusion_pince.png"
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout="constrained",
                          gridspec_kw={"width_ratios":[1.52,1]})
    a,b=axes
    a.imshow(plt.imread(before))
    a.set(xlim=(125,2125),ylim=(1003,242))
    b.imshow(plt.imread(after))
    a.set_title("V5 roulis · 17,68 mm",loc="left",weight="bold",size=14)
    b.set_title("V5 stabilisation · 3,70 mm",loc="left",weight="bold",size=14)
    b.set(xlim=(701,1265),ylim=(853,402))
    label_part(b,"Sabot de P3",(930,739),(716,808))
    label_part(b,"Phalange I3",(1003,753),(1074,808),"#344c5e")
    for ax in axes:
        ax.axis("off")
    fig.suptitle("Pince pouce-index · deux tambours à 92°",size=16,weight="bold")
    fig.savefig(folder/"10_pince_comparee.png",dpi=155,facecolor=fig.get_facecolor(),bbox_inches="tight")
    plt.close(fig)


def wireframe_details():
    folder = P / "visuels"
    views = (
        ("03_fusion_axe_creux.png", "J1 · passage axial et ancrage", (340,1130,925,135), (
            ("Faisceau axial", (744,265), (805,183)),
            ("Tube Ø10/8", (739,398), (410,360)),
            ("Quatre rehausses de 90 mm", (814,773), (840,835)),
        )),
        ("05_fusion_compensation.png", "J2 et J3 · compensation et boucles", (30,1460,855,78), (
            ("Ressort J2", (451,584), (185,715)),
            ("Ressort J3", (794,436), (806,580)),
            ("Boucle au poignet", (1281,428), (1150,542)),
        )),
    )
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), layout="constrained",
                             gridspec_kw={"width_ratios":[1,1.85]})
    for ax, (filename, title, bounds, labels) in zip(axes, views):
        ax.imshow(plt.imread(folder / filename))
        ax.set(xlim=bounds[:2], ylim=bounds[2:])
        for label, target, position in labels:
            label_part(ax, label, target, position)
        ax.set_title(title, loc="left", weight="bold", size=13)
        ax.axis("off")
    fig.savefig(folder / "11_passages_et_compensation.png", dpi=155, bbox_inches="tight")
    plt.close(fig)


def main():
    O.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.right":False,"axes.spines.top":False,
                         "axes.labelcolor":"#283a4d","xtick.color":"#283a4d","ytick.color":"#283a4d",
                         "axes.titlecolor":"#202d37","figure.facecolor":"#f9fbfb",
                         "axes.facecolor":"#f9fbfb"})
    d=load(P/"maturite.json")
    maturity(d)
    statuses()
    resources(d)
    guards()
    pinch_compare()
    wireframe_details()


if __name__=="__main__":
    main()
