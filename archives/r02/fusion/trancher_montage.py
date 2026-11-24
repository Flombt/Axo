"""Contrôle individuel des pièces et constitution des plateaux de la r02."""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import tempfile

OUT = Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent/"AURA_V3"/"Fabrication_r03"))
import preparer_plateaux as prusa


def flat_area(mesh):
    vertices, triangles, _ = mesh
    area = 0
    for face in triangles:
        a,b,c = [vertices[i] for i in face]
        if max(abs(p[2]) for p in (a,b,c)) <= 0.021:
            area += abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
    return round(area,2)


def inspect_slice(cli, name, mesh, profiles, staging):
    with tempfile.TemporaryDirectory(prefix=name+"_",dir=staging) as area:
        dest = Path(area)
        src = dest/(name+".3mf")
        prusa.make3mf(src, [(name,110,110)], {name:mesh})
        raw = dest/"test.gcode"
        supportless = (name.startswith(("Phalange_", "Bout_"))
                       or name in {"01_Platine","08_Capot","09_Capot","10_Tambour",
                                   "11_Palonnier","15_Coupon_Jeux"})
        for use_support in ((False, True) if supportless else (True,)):
            log = prusa.run_slicer(cli,"--load",profiles[use_support],"--dont-arrange",
                                  "--export-gcode","--output",raw,src)
            alerts = [line for line in log.splitlines()
                      if re.search(r"warning|floating|detached|may not be stable",line,re.I)]
            if alerts and not use_support:
                continue
            gcode = raw.read_text(encoding="utf-8",errors="replace")
            assert re.search(r"(?m)^G1\s+.*\bE[-0-9]",gcode), name
            support = bool(re.search(r"(?m)^;TYPE:Support material",gcode))
            grams = re.search(r"(?m)^; filament used \[g\] = ([0-9.]+)",gcode)
            seconds = re.search(r"(?m)^; estimated printing time \(normal mode\) = (.+)",gcode)
            assert grams and seconds, name
            return {"reference":name, "appui_stl_mm2":flat_area(mesh),
                    "profil_supports_actif":use_support,"supports_generes":support,
                    "filament_g":float(grams.group(1)), "duree":seconds.group(1).strip(),
                    "ponts":len(re.findall(r"(?m)^;TYPE:(?:Internal bridge|Bridge infill)",gcode)),
                    "alertes":alerts}


def main(cli):
    data = json.loads((OUT/"Verification_Montage.json").read_text(encoding="utf-8"))
    assert not data["global"]["interferences"] and not any(p["interferences"] for p in data["montage"])
    meshes = {}
    quantities = {}
    for item in data["nomenclature"]:
        stl = OUT/"STL"/item["stl"]
        assert sha256(stl.read_bytes()).hexdigest()==item["sha256"]
        key = item["reference"]
        meshes[key] = prusa.inspect_stl(stl,item["dimensions_mm"])
        quantities[key] = item["quantite_robot"]
    group_fingers = [key for key in meshes if key.startswith(("Phalange_","Bout_"))]
    plates = [
        ("00_Coupon_Jeux", (("15_Coupon_Jeux",),)),
        ("01_Chassis", (("01_Platine",),("02_Socle","03_Tourelle"))),
        ("02_Bras_Poignet", (("04_Segment_1","05_Segment_2","06_Segment_3"),
                            ("08_Capot","09_Capot","13_Bride_Poignet","14_Moyeu"))),
        ("03_Paume_Pouce_Transmission", (("07_Paume","12_Support_Pouce","10_Tambour","11_Palonnier"),)),
        ("04_Phalanges", [tuple([key]*quantities[key]) for key in group_fingers]),
    ]
    bed = {k:v[2] for k,v in meshes.items()}
    output = OUT/"Plateaux_PrusaSlicer"
    output.mkdir(exist_ok=True)
    individual, results, inventory = {}, [], Counter()
    with tempfile.TemporaryDirectory(prefix="AURA009_Prusa_") as work:
        temp = Path(work)
        with_support = prusa.PROFILE
        without_support = temp/"PETG_sans_supports.ini"
        ini = with_support.read_text(encoding="utf-8-sig")
        without_support.write_text(re.sub(r"(?m)^support_material = 1\s*$",
                                          "support_material = 0",ini),encoding="utf-8")
        profiles = {False:without_support, True:with_support}
        with ThreadPoolExecutor(max_workers=3) as workers:
            checks = [workers.submit(inspect_slice,cli,name,mesh,profiles,temp)
                      for name,mesh in meshes.items()]
            for result in checks:
                check = result.result()
                individual[check["reference"]] = check
                print(check,flush=True)
        for name, rows in plates:
            layout = prusa.pack(rows, bed)
            source = temp/"plateau.3mf"
            prusa.make3mf(source,layout,meshes)
            support = any(individual[key]["profil_supports_actif"] for key,_,_ in layout)
            prusa.PROFILE = profiles[support]
            dest = output/(name+".3mf")
            proof = prusa.slice_project(cli,source,dest,len(layout),temp)
            proof["repartition"] = dict(Counter(key for key,_,_ in layout))
            results.append(proof)
            inventory.update(proof["repartition"])
        prusa.PROFILE = with_support
    assert inventory==Counter({key:max(1,n) for key,n in quantities.items()})
    totals = [p for p in results if not p["fichier"].startswith("00_")]
    report = {
        "trancheur":next(line for line in prusa.run_slicer(cli,"--help").splitlines()
                        if line.startswith("PrusaSlicer")),
        "profil":"PETG · buse 0,4 mm · couche 0,20 mm",
        "pieces_robot":sum(quantities.values()),"references_robot":len(meshes)-1,
        "filament_robot_g":round(sum(p["filament_g"] for p in totals),2),
        "preuves_individuelles":list(individual.values()),"plateaux":results,
    }
    (OUT/"Verification_Tranchage.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",
                                                  encoding="utf-8")
    print([(p["fichier"],p["instances"],p["supports"],p["filament_g"],p["duree"],p["messages"])
           for p in results],flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
