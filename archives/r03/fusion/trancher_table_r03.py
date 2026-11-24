"""Préparer les 3MF PETG r03 et vérifier le tranchage hors impression."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
heritage=HERE.parents[1]/"v3/fusion/Fabrication_r03"
if not heritage.is_dir():
    heritage=HERE/"sources_heritage/AURA_V3/Fabrication_r03"
sys.path.insert(0,str(heritage))
import preparer_plateaux as prusa


def layout(names,sizes):
    """Rangées libres dans un volume de plateau, 6 mm autour de chaque pièce."""
    rows=[]
    for name in sorted(names,key=lambda k:(sizes[k][1],sizes[k][0]),reverse=True):
        match=next((row for row in rows if
                    sum(sizes[x][0]+2*prusa.PAD for x in row)+sizes[name][0]+2*prusa.PAD
                    <=prusa.BED-2*prusa.EDGE),None)
        if match is None:
            rows.append([name])
        else:
            match.append(name)
    return prusa.pack(rows,sizes)


def main(cli):
    build=json.loads((HERE/"Inventaire_CAO_r03.json").read_text(encoding="utf8"))
    meshes={}
    sizes={}
    quantities={}
    for row in build["pieces"]:
        key=row["reference"]
        p=HERE/"STL"/row["fichier"]
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row["sha256"]
        verts,faces,size=prusa.inspect_stl(p,row["dimensions_mm"])
        meshes[key]=(verts,faces)
        sizes[key]=size
        quantities[key]=row["quantite_robot"]
    designs=[
        ("00_Coupons", [k for k,n in quantities.items() if n==0], False),
        ("01_Platine",["01_Platine"],False),
        ("02_Chassis",["02_Socle","03_Tourelle","04_Segment_1","05_Segment_2","P15_Platine_cartes"],True),
        ("03_Poignet_paume",["06_Segment_3","07_Paume","12_Support_Pouce","13_Bride_Poignet","14_Moyeu"],True),
        ("04_Portes_moteurs",["P07_Porte_J2","P08_Porte_J3","08_Capot","09_Capot"],True),
        ("05_Freins_gardes",["P09_Frein_J2","P10_Frein_J3","P11_Garde_J2","P12_Garde_J3"],True),
        ("06_Doigts_transmission",["10_Tambour","11_Palonnier"]+
               [k for k in quantities if k.startswith(("Phalange","Bout"))],True),
        ("07_Guides_et_colliers",[k for k in quantities if k.startswith(("Guide_","Collier_"))],True),
        ("08_Attaches_faisceau",[k for k in quantities if k.startswith("Attache_")],True),
    ]
    out=HERE/"Plateaux_PrusaSlicer"
    out.mkdir(exist_ok=True)
    profile=(HERE/"Profil_PETG_r03.ini").read_text(encoding="utf8")
    print(prusa.run_slicer(cli,"--help").splitlines()[0],flush=True)
    used=Counter()
    reports=[]
    with tempfile.TemporaryDirectory(prefix="AURA009_R03_") as tmp:
        folder=Path(tmp)
        for title, keys, supported in designs:
            names=[k for k in keys for _ in range(max(1,quantities[k]))]
            used.update(names)
            staged=folder/f"{title}_source.3mf"
            prusa.make3mf(staged,layout(names,sizes),meshes)
            prusa.PROFILE=folder/"config_petg.ini"
            prusa.PROFILE.write_text(profile if supported else profile.replace("support_material = 1","support_material = 0"),
                                     encoding="utf8")
            verified=prusa.slice_project(cli,staged,out/(title+".3mf"),len(names),folder)
            with ZipFile(out/verified["fichier"]) as zip_in:
                cfg=zip_in.read(prusa.SETTINGS).decode("utf8")
                assert "; filament_type = PETG" in cfg
            verified["filament_type"]="PETG"
            verified["repartition"]=dict(Counter(names))
            reports.append(verified)
            print(title,verified["instances"],verified["filament_g"],verified["duree"],verified["messages"],flush=True)
    assert used==Counter({k:max(n,1) for k,n in quantities.items()}),(used,quantities)
    report={"plateaux":reports,"references":len(quantities),"pieces_robot":sum(quantities.values()),
            "filament_robot_g":round(sum(x["filament_g"] for x in reports[1:]),3),
            "profil":"PETG, buse 0,4, couches 0,20, plateau virtuel 220 × 220 mm"}
    (HERE/"Verification_Tranchage_r03.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")


if __name__=="__main__":
    main(Path(sys.argv[1]))
