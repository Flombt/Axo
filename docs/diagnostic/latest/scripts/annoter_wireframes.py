"""Vues annotées de maillages Fusion, en millimètres et aux poses mesurées."""
from collections import defaultdict
import gzip
import json
from pathlib import Path
import sys

try:
    import matplotlib
    import numpy as np
    import trimesh
except ModuleNotFoundError:
    sys.path.insert(0, str(Path.home() / "AppData/Local/Temp/aura-audit-deps"))
    import matplotlib
    import numpy as np
    import trimesh

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from analyse_mecanique import matrix, point, PORTS

AUDIT = Path("docs/diagnostic/latest")
RAW = AUDIT / "preuves"
OUT = AUDIT / "wireframes"
PALETTE = {"ink":"#233b51", "gray":"#6e8190", "soft":"#abb8c2", "orange":"#ca5831",
           "red":"#ad2943", "green":"#067d71", "gold":"#a8811c", "blue":"#3f6db0"}
plt.rcParams.update({"font.size":10, "text.color":PALETTE["ink"], "axes.edgecolor":"#d5dfe5",
                     "axes.labelcolor":PALETTE["ink"], "xtick.color":PALETTE["ink"], "ytick.color":PALETTE["ink"]})

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


geometry = read(RAW / "fusion_geometrie_neutre.json")
poses = {r["index"]:r for f in RAW.glob("fusion_poses_*.json.gz") for r in
         json.load(gzip.open(f, "rt", encoding="utf-8"))}
for f in RAW.glob("fusion_reprises_*.json.gz"):
    for row in json.load(gzip.open(f, "rt", encoding="utf-8")):
        if "transforms" in row:
            poses[row["index"]] = row
distances = read(RAW / "distances_fusion.json")
parts = geometry["parts"]
meshes = defaultdict(list)
for obj in json.load(gzip.open(RAW / "maillages_visuels_fusion.json.gz", "rt", encoding="utf-8")):
    v = np.array(obj["vertices_local_mm"], float)
    face = np.array(obj["triangles"], int).reshape(-1,3)
    mesh = trimesh.Trimesh(vertices=v, faces=face, process=True)
    adjacency = mesh.face_adjacency_edges[mesh.face_adjacency_angles > .27]
    edge_idx = np.bincount(mesh.edges_unique_inverse, minlength=len(mesh.edges_unique))
    outline = mesh.edges_unique[edge_idx==1]
    edges = np.vstack([adjacency,outline])
    meshes[obj["part"]].append((mesh,edges))


def transform_vertices(vertices, name, pose, frame=None):
    t = matrix(poses[pose]["transforms"][name])
    if frame is not None:
        t = np.linalg.inv(matrix(poses[pose]["transforms"][frame])) @ t
    return vertices @ t[:3,:3].T + t[:3,3]


def projected(ax, keys, pose, dims, color, width=.6, alpha=.6):
    for key in keys:
        for mesh,edges in meshes[key]:
            world = transform_vertices(mesh.vertices,key,pose)
            if len(edges):
                segments = world[edges][:,:,list(dims)]
                ax.add_collection(LineCollection(segments,colors=color,linewidths=width,alpha=alpha))


def section(ax, keys, pose, frame, color, width=1.05):
    for key in keys:
        for mesh, _ in meshes[key]:
            xyz = transform_vertices(mesh.vertices,key,pose,frame)
            solid = trimesh.Trimesh(vertices=xyz,faces=mesh.faces,process=False)
            lines = trimesh.intersections.mesh_plane(solid,[0,1,0],[0,0,0])
            if len(lines):
                ax.add_collection(LineCollection(lines[:,:,[0,2]], colors=color,linewidths=width))


def axes(ax, x, y, limits):
    ax.set_xlim(*limits[0]); ax.set_ylim(*limits[1]); ax.set_xlabel(x); ax.set_ylabel(y)
    ax.set_aspect("equal",adjustable="box")
    ax.grid(color="#e7edf1",linewidth=.7,alpha=.8)
    ax.set_axisbelow(True)


def figure(fig, title, subtitle, name):
    fig.suptitle(title,x=.068,y=.974,ha="left",fontsize=20,fontweight="bold")
    fig.text(.068,.898,subtitle,ha="left",va="top",color=PALETTE["gray"],fontsize=10)
    fig.tight_layout(rect=(.035,.02,.99,.837))
    fig.savefig(OUT/name,dpi=170,facecolor="white")
    plt.close(fig)


def table():
    fig,(a,b)=plt.subplots(1,2,figsize=(13,6.2),sharey=True)
    structures=["01_Platine","02_Palier_J1","05_Tourelle","J2_Chape_Tangage","07_Bras",
                "J3_Chape_Tangage","08_Avant_bras","11_Paume","12_Chape_Pouce"]
    fingers=[c+str(i) for c in "PIMAU" for i in (1,2,3)]
    for ax, idx, name in [(a,0,"Au neutre"),(b,1,"J2 −21° · J3 −32°")]:
        projected(ax, structures, idx, (0,2), PALETTE["ink"])
        projected(ax, fingers, idx,(0,2),PALETTE["red"] if idx else PALETTE["green"])
        ax.axhline(0,color=PALETTE["red"],linestyle="--",linewidth=1.3)
        ax.fill_between((-80,280),-68,0,color=PALETTE["red"],alpha=.07)
        ax.set_title(name,loc="left",fontweight="bold")
        axes(ax,"X (mm)","Z (mm)",((-78,278),(-68,156)))
    z=poses[1]["min_hand_z_mm"]
    b.annotate(f"{abs(z):.2f} mm sous le plan".replace(".",","),xy=(199,z),xytext=(38,-46),
               arrowprops={"arrowstyle":"->","color":PALETTE["red"]},color=PALETTE["red"])
    figure(fig,"La main traverse le plan de table","A01-P0-01 · Projection XZ des maillages du modèle Fusion v1 aux poses 0 et 1.","06_plan_table_annote.png")


def yaw_routing():
    fig,(a,b)=plt.subplots(1,2,figsize=(12.5,6.5))
    fixed=[k for k in parts if k.startswith("Gaine_Socle")]
    mobile=[k for k in parts if k.startswith("Gaine_Colonne")]
    rest=matrix(poses[0]["transforms"]["05_Tourelle"])
    for ax,index in ((a,0),(b,4)):
        projected(ax,("01_Platine","02_Palier_J1"),index,(0,1),PALETTE["soft"],alpha=.42)
        projected(ax,("05_Tourelle","J1_Roue","J1_Pignon"),index,(0,1),PALETTE["gray"],alpha=.35)
        projected(ax,fixed,index,(0,1),PALETTE["blue"],width=.9,alpha=.70)
        projected(ax,mobile,index,(0,1),PALETTE["orange"],width=.9,alpha=.67)
        for name, xyz in PORTS.items():
            s=point(rest,xyz)
            t=point(matrix(poses[index]["transforms"]["05_Tourelle"]),xyz)
            ax.scatter(*s[:2],color=PALETTE["blue"],s=22,zorder=5)
            ax.scatter(*t[:2],color=PALETTE["orange"],s=22,zorder=5)
            ax.plot([s[0],t[0]],[s[1],t[1]],color=PALETTE["red"],ls="--",lw=1)
        ax.scatter(0,0,color=PALETTE["ink"],marker="+",s=60,zorder=7)
        axes(ax,"X (mm)","Y (mm)",((-59,52),(-45,47)))
        ax.set_title("Jonctions au neutre" if index==0 else "Lacet +88° · des extrémités se séparent",loc="left",fontweight="bold")
    b.text(-53,40,"33,31 à 39,45 mm",color=PALETTE["red"],weight="bold")
    a.plot([],[],color=PALETTE["blue"],label="Gaines fixées au socle")
    a.plot([],[],color=PALETTE["orange"],label="Gaines solidaires de la tourelle")
    a.legend(loc="lower left",frameon=True,fontsize=8.6)
    figure(fig,"Les quatre passages souples de J1 sont excentrés",
           "A01-P0-02 · Maillages projetés XY. Les tirets relient les points d’extrémité modélisés.","07_raccords_j1_annote.png")


def collars():
    fig,(a,b)=plt.subplots(1,2,figsize=(12,5.7),sharey=True)
    for ax,name,hub,moving,limits in [(a,"J2R","J2_Chape_Tangage","07_Bras",(4,24)),(b,"J3R","J3_Chape_Tangage","08_Avant_bras",(1.6,22))]:
        section(ax,[hub,"Palier_"+name],0,hub,PALETTE["blue"])
        section(ax,[moving],0,hub,PALETTE["orange"])
        section(ax,["But_"+name],0,hub,PALETTE["red"],width=1.6)
        ax.axhline(0,color=PALETTE["soft"],ls=":")
        axes(ax,"X local (mm)","Z local (mm)",(limits,(-14,14)))
        ax.set_title(f"{name} · coupe axiale Y local = 0",loc="left",fontweight="bold")
        ax.text(limits[0]+.25,-12.9,"Ø15,92 / Ø16,42 mm",color=PALETTE["ink"],fontsize=9)
    a.plot([],[],color=PALETTE["blue"],label="Tourillon et chapeau")
    a.plot([],[],color=PALETTE["orange"],label="Arbre et collier imprimés")
    a.plot([],[],color=PALETTE["red"],label="Butée-goupille")
    a.legend(loc="upper right",fontsize=8,frameon=True)
    figure(fig,"Paliers fendus et butées de roulis","A01-P1-05 et 06 · Coupe des maillages natifs, cotes cylindriques relevées sur les BRep.",
           "08_coupes_paliers_annote.png")


def grip():
    idx=next(i for i,p in poses.items() if p["label"]=="pince 92")
    record=next(r for r in distances if r["pose"]=="pince 92" and r["pair"]==["P3","I3"])
    coords=np.array(record["points_mm"])
    fig,ais=plt.subplots(1,2,figsize=(12.5,5.9))
    for ax,xyd,label,lim in [(ais[0],(0,1),"Vue de dessus",((181,263),(-59,26))),
                             (ais[1],(0,2),"Vue de côté",((181,263),(90,145)))]:
        projected(ax,["11_Paume","12_Chape_Pouce","13_Peigne", "M1","M2","M3","A1","A2","A3",
                      "U1","U2","U3"],idx,xyd,PALETTE["soft"],alpha=.52)
        projected(ax,["P1","P2","P3"],idx,xyd,PALETTE["orange"],width=1.05)
        projected(ax,["I1","I2","I3"],idx,xyd,PALETTE["green"],width=1.05)
        uv=coords[:,list(xyd)]
        ax.plot(*uv.T,color=PALETTE["red"],ls="--",marker="o",ms=4,zorder=8)
        ax.set_title(label,loc="left",fontweight="bold")
        axes(ax,"X (mm)","Y (mm)" if xyd[1]==1 else "Z (mm)",lim)
    ais[0].text(190,-54,"Bout à bout en 3D · 17,68 mm",color=PALETTE["red"],weight="bold")
    figure(fig,"La fermeture maximale laisse un écart de pince","A01-P1-04 · Tambours pouce et index à 92°. Le noyau Fusion donne les deux points les plus proches.",
           "09_pince_annotee.png")


def harness():
    fig,(a,b)=plt.subplots(1,2,figsize=(12.5,5.7))
    groups=[(a,["07_Bras","Coque_Bras"],["Gaine_Bras_J3R_1","Gaine_Bras_J3R_2"],
             "Deux gaines J3R sous la coque du bras",((6,92),(62,138)),"120,63 et 117,25 mm³"),
            (b,["09_Cassette_SG90","Capot_Cassette"],["Faisceau_Cassette"],
             "Tronc électrique sous le capot de cassette",((77,178),(97,144)),"154,52 mm³")]
    for ax,case,wires,title,limit,text in groups:
        projected(ax,case,0,(0,2),PALETTE["gray"],.75,.65)
        projected(ax,wires,0,(0,2),PALETTE["orange"],1.05,.95)
        ax.set_title(title,loc="left",fontweight="bold")
        axes(ax,"X (mm)","Z (mm)",limit)
        ax.text(limit[0][0]+3,limit[1][0]+3,text,color=PALETTE["red"],weight="bold")
    figure(fig,"Les passages souples occupent des volumes en commun","A01-P0-02 et A01-P1-07 · Tracés au neutre. Volumes d’intersection des enveloppes CAO.",
           "10_passages_souples_annote.png")


if __name__=="__main__":
    for view in (table,yaw_routing,collars,grip,harness):
        view()
