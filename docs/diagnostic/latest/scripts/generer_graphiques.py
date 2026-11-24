"""Graphiques du rapport. Exécuter depuis la racine Aura."""
from collections import Counter
import json
from pathlib import Path
import sys

try:
    import matplotlib
    import numpy as np
except ModuleNotFoundError:
    sys.path.insert(0, str(Path.home() / "AppData/Local/Temp/aura-audit-deps"))
    import matplotlib
    import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

AUDIT = Path("docs/diagnostic/latest")
OUT = AUDIT / "graphs"
DATA = json.loads((AUDIT / "donnees_graphiques.json").read_text(encoding="utf-8"))
OLD = json.loads(Path("archives/r03/diagnostic/donnees_r02_r03.json").read_text(encoding="utf-8"))
NAVY, BLUE, TEAL, ORANGE, RED, GRAY, LIGHT = "#18354a", "#456cb1", "#13796d", "#c55a29", "#a62e43", "#6b7580", "#e7edf1"
FRENCH = {"axes.edgecolor": LIGHT, "axes.labelcolor": NAVY, "axes.titlecolor": NAVY,
          "text.color": NAVY, "xtick.color": NAVY, "ytick.color": NAVY, "font.size": 11, "axes.titleweight":"bold"}
plt.rcParams.update(FRENCH)
OUT.mkdir(parents=True, exist_ok=True)


def save(figure, filename, header, foot=None):
    figure.suptitle(header, x=.065, y=.97, ha="left", fontsize=21, fontweight="bold")
    if foot:
        figure.text(.065, .028, foot, color=GRAY, fontsize=9, va="bottom")
    figure.tight_layout(rect=(.045, .07, .985, .92))
    figure.savefig(OUT / filename, dpi=160, facecolor="white")
    plt.close(figure)


def barvalues(ax, values, labels, color, fmt=None):
    bars = ax.bar(labels, values, color=color, width=.59)
    ax.bar_label(bars, labels=[fmt(x) if fmt else str(x) for x in values], padding=5, color=NAVY)
    ax.grid(axis="y", color=LIGHT, linewidth=.8)
    ax.set_axisbelow(True)
    return bars


def dec(x, digits=2):
    return f"{x:.{digits}f}".replace(".", ",")


def radar():
    scores = DATA["scores"]
    values = [np.array([r[i] if i<3 else sum(r[i]) for r in scores]) for i in (1,2,3)]
    names = ["Mécanique","Moteurs","Impression","Électronique","Alimentation",
             "Assemblage","Logiciel","IA","Sécurité","Maintenance","Documentation"]
    angles = np.linspace(0, 2 * np.pi, len(names), endpoint=False)
    fig, ax = plt.subplots(figsize=(10,7.2), subplot_kw={"projection":"polar"})
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    for label,color,v in zip(("r02", "r03", "V5 roulis"), (GRAY,BLUE,TEAL),values):
        ax.plot(np.r_[angles, angles[0]], np.r_[v, v[0]], color=color, linewidth=2, label=label)
        ax.fill(np.r_[angles,angles[0]], np.r_[v,v[0]], color=color, alpha=.08)
    ax.set_xticks(angles, names)
    ax.tick_params(axis="x", pad=12)
    ax.set_rlabel_position(24)
    ax.set_yticks((20,40,60,80))
    ax.grid(color=LIGHT)
    ax.set_ylim(0,100)
    ax.legend(loc="lower center", bbox_to_anchor=(.5,-.21), ncols=3, frameon=False)
    save(fig,"01_radar_maturite.png","Maturité technique sur 100","r02 et r03 publiées. V5 roulis évaluée sur la même structure à quatre critères.")


def compare():
    scores = DATA["scores"]
    fig, ax = plt.subplots(figsize=(10.7,7.4))
    y = np.arange(len(scores))
    for shift, idx, label, color in [(-.24, 1, "r02", GRAY), (0,2,"r03",BLUE), (.24,3,"V5 roulis",TEAL)]:
        vals=[r[idx] if idx<3 else sum(r[idx]) for r in scores]
        bars=ax.barh(y+shift, vals, height=.20, label=label, color=color)
        ax.bar_label(bars,padding=3,fontsize=8)
    ax.set_yticks(y,[r[0] for r in scores])
    ax.invert_yaxis()
    ax.set_xlim(0,100)
    ax.set_xlabel("Points sur 100")
    ax.legend(loc="upper right", frameon=False)
    ax.grid(axis="x",color=LIGHT)
    ax.set_axisbelow(True)
    save(fig,"02_comparaison_notes.png","Notes par domaine","Chaque note est la somme de quatre critères. Les essais physiques V5 restent ouverts.")


def problem_totals():
    hist = DATA["history"]["records"]
    open_now = {id for id,status in hist if status not in (0,5)}
    rows=OLD["problemes"]
    levels = [f"P{i}" for i in range(5)]
    count0=Counter(r["p"] for r in rows)
    count3=Counter(r["p"] for r in rows if r["statut"]!="corrigé numériquement")
    count5=Counter(r["p"] for r in rows if r["id"] in open_now)
    fig, (ax,bx) = plt.subplots(ncols=2,figsize=(12,5.6), gridspec_kw={"width_ratios":(1.5,1)})
    x=np.arange(len(levels))
    for j,(label,color,c) in enumerate(zip(("r02","r03","V5 roulis"),(GRAY,BLUE,TEAL),(count0,count3,count5))):
        bars=ax.bar(x+(j-1)*.26,[c[k] for k in levels],.23,color=color,label=label)
        ax.bar_label(bars,padding=2, fontsize=8)
    ax.set_xticks(x,levels)
    ax.set_title("Cohorte initiale encore ouverte")
    ax.set_ylabel("Problèmes")
    ax.legend(frameon=False)
    ax.grid(axis="y",color=LIGHT)
    ax.set_axisbelow(True)
    current=Counter(r[0] for r in DATA["reprioritized_current"])
    barvalues(bx,[current[k] for k in levels],levels,ORANGE)
    bx.set_ylim(0,max(current.values())+4)
    bx.set_title("Registre V5 par gravité actuelle")
    save(fig,"03_evolution_priorites.png","Problèmes par gravité","À gauche, les mêmes 43 cas et gravités d’origine. À droite, les problèmes du registre courant.")


def statuses():
    names=DATA["history"]["states"]
    counts=Counter(s for _,s in DATA["history"]["records"])
    fig,ax=plt.subplots(figsize=(10,5.5))
    vals=[counts[i] for i in range(len(names))]
    bars=ax.barh(names,vals,color=[TEAL,BLUE,RED,ORANGE,"#aa7a23",GRAY])
    ax.bar_label(bars, padding=5)
    ax.set_xlim(0,max(vals)+4)
    ax.invert_yaxis()
    ax.set_xlabel("Cas du diagnostic initial")
    ax.grid(axis="x",color=LIGHT)
    ax.set_axisbelow(True)
    save(fig,"04_statut_problemes.png","Sort des 43 problèmes du diagnostic initial","Un cas devenu non applicable correspond à une architecture dont le mécanisme spécifique a été retiré.")


def costs():
    d=DATA["budgets"]
    vals=d["hardware"]
    fig, ax=plt.subplots(figsize=(10.4,5.6))
    x=np.arange(len(vals))
    for xvals,costs,color,label in ((x-.2,vals,TEAL,"Matériel selon le panier"),
                                   (x+.2,[x+d["petg_spool"] for x in vals],ORANGE,"Avec 1 kg de PETG à 11,95 €")):
        b=ax.bar(xvals,costs,.35,color=color,label=label)
        ax.bar_label(b,labels=[dec(v) for v in costs],padding=4,fontsize=9)
    ax.axhline(150,color=RED,linestyle="--",linewidth=1.1,label="Plafond de 150 €")
    ax.axhline(100,color=GRAY,linestyle=":",linewidth=1.1,label="Objectif de 100 €")
    ax.set_xticks(x,d["labels"])
    ax.set_ylim(0,190)
    ax.set_ylabel("Montant indicatif (€ TTC)")
    ax.legend(loc="lower right",frameon=True,ncols=2)
    ax.grid(axis="y",color=LIGHT)
    ax.set_axisbelow(True)
    save(fig,"05_evolution_cout.png","Coût des paniers cibles","Hypothèses de livraison et de stock historiques. Les corrections et l’outillage non chiffrés restent à ajouter.")


def masses():
    d=DATA["masses"]
    fig,(ax,bx)=plt.subplots(ncols=2,figsize=(11,5.6),gridspec_kw={"width_ratios":(1.45,1)})
    m=barvalues(ax,d["nominal"],d["labels"],(GRAY,GRAY,BLUE,TEAL),lambda x: dec(x,1))
    m[-1].set_hatch("//")
    ax.set_ylim(0,1270)
    ax.set_ylabel("Masse calculée (g)")
    ax.set_title("Robot à vide, sans lest")
    barvalues(bx,d["printed_solid"],d["solids_labels"],(BLUE,TEAL),lambda x:dec(x,1))
    bx.set_ylim(0,550)
    bx.set_title("PETG plein des pièces CAO")
    save(fig,"06_evolution_masse.png","Masse calculée en PETG plein","r03–r05 publiées. V5 recalculée avec masses de gabarits explicites. Les pièces n’ont pas été pesées.")


def time():
    d=DATA["print_times"]
    fig,(ax,bx)=plt.subplots(ncols=2,figsize=(10.7,5.6),sharey=True)
    for pane,key,title,color in ((ax,"prusa","PrusaSlicer · Profil comparable",BLUE),(bx,"anycubic_r05","Anycubic · r05 selon la machine",TEAL)):
        barvalues(pane,[v/60 for _,v in d[key]],[k for k,_ in d[key]],color,
                       lambda h:f"{int(round(h*60))//60} h {int(round(h*60))%60:02d}")
        pane.set_ylim(0,52)
        pane.set_title(title)
    ax.set_ylabel("Temps calculé (h)")
    save(fig,"07_evolution_temps_impression.png","Durées de tranchage disponibles","Robot seul. Les moteurs de tranchage et profils diffèrent entre panneaux. Durée V5 inconnue.")


def readiness():
    d=DATA["preparation"]
    fig,ax=plt.subplots(figsize=(10.4,5.8))
    y=np.arange(len(d))
    ax.barh(y,[r[2] for r in d],color=LIGHT,height=.62)
    bars=ax.barh(y,[r[1] for r in d],color=TEAL,height=.62)
    ax.bar_label(bars, labels=[f"{r[1]} / {r[2]}" for r in d],padding=5)
    ax.set_yticks(y,[r[0] for r in d])
    ax.invert_yaxis()
    ax.set_xlim(0,23)
    ax.set_xlabel("Points obtenus / poids du domaine")
    ax.grid(axis="x",color="white")
    ax.set_axisbelow(True)
    save(fig,"08_preparation_fabrication.png","Préparation à la fabrication · 17 / 100",
             "Grille d’audit V5. Un blocage dans une étape de sécurité exclut l’autorisation de mise en service.")


if __name__=="__main__":
    for figure in (radar,compare,problem_totals,statuses,costs,masses,time,readiness):
        figure()
