"""Vérifie les STL et produit les projets 3MF à partir des cotes de Fusion.

Usage : python preparer_plateaux.py CHEMIN_PRUSASLICER_CONSOLE
Le tranchage est local. Les G-codes restent dans le dossier temporaire.
"""

from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


OUT = Path(__file__).resolve().parent
REPORT = OUT / "Verification_FDM_r03.json"
PROFILE = OUT / "Profil_FDM_PETG_virtuel.ini"
MODEL = "3D/3dmodel.model"
SETTINGS = "Metadata/Slic3r_PE.config"
NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
ET.register_namespace("", NS)
BED, EDGE, PAD = 220, 3, 6


def tag(name):
    return "{" + NS + "}" + name


def inspect_stl(file, dimensions):
    raw = file.read_bytes()
    count = struct.unpack_from("<I", raw, 80)[0]
    if 84 + 50 * count != len(raw):
        raise ValueError(f"STL binaire invalide {file.name}.")
    vertices, index, facets, edges, neighbors = [], {}, [], Counter(), defaultdict(list)
    for t in range(count):
        triangle = []
        for xyz in range(3):
            p = tuple(round(n, 5) for n in struct.unpack_from("<3f", raw, 84 + t * 50 + 12 + 12 * xyz))
            if p not in index:
                index[p] = len(vertices)
                vertices.append(p)
            triangle.append(index[p])
        if len(set(triangle)) != 3:
            raise ValueError(f"Triangle dégénéré dans {file.name}.")
        facets.append(triangle)
        for a,b in zip(triangle, triangle[1:] + triangle[:1]):
            key = (min(a,b), max(a,b))
            edges[key] += 1
            neighbors[key].append(t)
    if any(n != 2 for n in edges.values()):
        raise ValueError(f"Arêtes non fermées dans {file.name}: {Counter(edges.values())}.")
    graph = [[] for _ in facets]
    for a,b in neighbors.values():
        graph[a].append(b)
        graph[b].append(a)
    stack, visited = [0], {0}
    while stack:
        for neighbor in graph[stack.pop()]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    if len(visited) != count:
        raise ValueError(f"Composants de maillage séparés dans {file.name}.")
    cols = list(zip(*vertices))
    span = [round(max(c)-min(c), 4) for c in cols]
    if any(abs(a-b)>.06 for a,b in zip(span, dimensions)) or abs(min(cols[2]))>.035:
        raise ValueError(f"Échelle ou plan d'impression divergent dans {file.name}: {span}.")
    return vertices, facets, span


def pack(rows, sizes):
    total_height = sum(max(sizes[name][1] for name in row)+2*PAD for row in rows)
    if total_height > BED-2*EDGE:
        raise ValueError(f"Rangées trop hautes: {total_height} mm")
    layout, y = [], (BED-total_height)/2
    for row in rows:
        total_width = sum(sizes[name][0]+2*PAD for name in row)
        if total_width > BED-2*EDGE:
            raise ValueError(f"Rangée trop large: {row}, {total_width} mm")
        x = (BED-total_width)/2
        row_height = max(sizes[name][1] for name in row)+2*PAD
        for name in row:
            wide = sizes[name][0]+2*PAD
            layout.append((name, round(x+wide/2,4), round(y+row_height/2,4)))
            x += wide
        y += row_height
    return layout


def make3mf(file, layout, meshes):
    selected = list(dict.fromkeys(name for name,_,_ in layout))
    ids = {name:str(i+1) for i,name in enumerate(selected)}
    model = ET.Element(tag("model"),{"unit":"millimeter"})
    r = ET.SubElement(model,tag("resources"))
    b = ET.SubElement(model,tag("build"))
    for name in selected:
        obj = ET.SubElement(r,tag("object"),{"id":ids[name],"name":name,"type":"model"})
        msh = ET.SubElement(obj,tag("mesh"))
        coords = ET.SubElement(msh,tag("vertices"))
        for v in meshes[name][0]:
            ET.SubElement(coords,tag("vertex"),dict(zip("xyz",map(str,v))))
        triangles = ET.SubElement(msh,tag("triangles"))
        for facet in meshes[name][1]:
            ET.SubElement(triangles,tag("triangle"),dict(zip(("v1","v2","v3"),map(str,facet))))
    for name,x,y in layout:
        ET.SubElement(b,tag("item"),{"objectid":ids[name],"transform":f"1 0 0 0 1 0 0 0 1 {x} {y} 0"})
    types = ('<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
             '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" '
            'Target="/3D/3dmodel.model"/></Relationships>')
    with ZipFile(file,"w",compression=ZIP_DEFLATED) as zip_out:
        zip_out.writestr("[Content_Types].xml",types)
        zip_out.writestr("_rels/.rels",rels)
        zip_out.writestr(MODEL,ET.tostring(model,encoding="utf-8",xml_declaration=True))


def run_slicer(cli, *args):
    args = [str(cli),*map(str,args)]
    run = subprocess.run(args,capture_output=True,encoding="utf-8",errors="replace",timeout=100)
    log = run.stdout+"\n"+run.stderr
    if run.returncode or re.search(r"\[error\]|conflicts found|outside the print bed|overlap detected", log, re.I):
        raise RuntimeError(f"PrusaSlicer {run.returncode}.\n{log[-4700:]}")
    return log


def slice_project(cli, source, output, expected_count, temporary):
    raw = temporary/"export_slicer.3mf"
    raw.unlink(missing_ok=True)
    run_slicer(cli,"--load",PROFILE,"--dont-arrange","--export-3mf","--output",raw,source)
    config = temporary/"slicer.ini"
    run_slicer(cli,"--load",PROFILE,"--save",config)
    prefixed = "".join("; "+l+"\n" for l in config.read_text(encoding="utf-8-sig").splitlines()
                       if " = " in l and not l.startswith("#"))
    candidate = temporary/output.name
    with ZipFile(raw) as z, ZipFile(candidate,"w",compression=ZIP_DEFLATED) as dest:
        for entry in z.infolist():
            if entry.filename!=SETTINGS:
                dest.writestr(entry.filename,z.read(entry))
        dest.writestr(SETTINGS,prefixed.encode("utf-8"))
    with ZipFile(candidate) as z:
        assert z.testzip() is None
        root = ET.fromstring(z.read(MODEL))
        items = root.find(tag("build"))
        assert len(items)==expected_count and root.attrib["unit"]=="millimeter"
    work = temporary/"controle.gcode"
    log = run_slicer(cli,"--dont-arrange","--export-gcode","--output",work,candidate)
    gcode=work.read_text(encoding="utf-8",errors="replace")
    for setting in ("bed_shape = 0x0,220x0,220x220,0x220","support_material_buildplate_only = 1","layer_height = 0.2"):
        if "; "+setting not in gcode:
            raise RuntimeError(f"Réglage intégré non repris : {setting}")
    if not re.search(r"(?m)^G1\s+.*\bE[-0-9]",gcode):
        raise RuntimeError("Tranchage sans extrusion.")
    weight = re.search(r"(?m)^; filament used \[g\] = ([0-9.]+)",gcode)
    duration = re.search(r"(?m)^; estimated printing time \(normal mode\) = (.+)",gcode)
    if not weight or not duration:
        raise RuntimeError("Le slicer n'a pas fourni la masse et la durée.")
    supports=bool(re.search(r"(?m)^;TYPE:Support material",gcode))
    bridges=len(re.findall(r"(?m)^;TYPE:(?:Internal bridge|Bridge infill)",gcode))
    warnings=[line for line in log.splitlines() if re.search(r"warning|floating|detached",line,re.I)]
    output.write_bytes(candidate.read_bytes())
    work.unlink()
    return {"fichier":output.name,"instances":expected_count,"filament_g":float(weight.group(1)),
            "duree":duration.group(1).strip(),"supports":supports,"sections_de_pont":bridges,
            "messages":warnings,"sha256":sha256(output.read_bytes()).hexdigest()}


def main(cli):
    report=json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("etape")!="CAO et exports FDM contrôlés":
        raise RuntimeError("La géométrie Fusion n'a pas achevé ses contrôles.")
    meshes={}
    names=[]
    for part in report["nomenclature"]:
        file=OUT/"STL_orientes"/part["stl"]
        if sha256(file.read_bytes()).hexdigest()!=part["sha256"]:
            raise ValueError(f"L'empreinte a changé {file.name}.")
        name=part["reference"]
        meshes[name]=inspect_stl(file,part["dimensions_mm"])
        names.append(name)
    base,turret,upper,middle,lower,yaw,pitch,palm,first,second,tip=names
    specs=[
        ("01_Socle",[[base]]),
        ("02_Trois_segments",[[upper],[middle],[lower]]),
        ("03_Tourelle_et_poignet",[[turret,yaw],[pitch]]),
        ("04_Paume",[[palm]]),
        ("05_Phalanges_proximales_et_moyennes",[[first,second] for _ in range(5)]),
        ("06_Bouts_de_doigts",[[tip,tip,tip],[tip,tip]]),
    ]
    destination=OUT/"Plateaux_PrusaSlicer"
    destination.mkdir(exist_ok=True)
    placed=Counter()
    proofs=[]
    sizes={key:data[2] for key,data in meshes.items()}
    with tempfile.TemporaryDirectory(prefix="AURA_FDM_Prusa_") as folder:
        folder=Path(folder)
        for name,rows in specs:
            positions=pack(rows,sizes)
            out=destination/(name+".3mf")
            source=folder/"positions.3mf"
            make3mf(source,positions,meshes)
            result=slice_project(cli,source,out,len(positions),folder)
            result["repartitions"]=Counter(ref for ref,_,_ in positions)
            proofs.append(result)
            placed.update(result["repartitions"])
            print(name,result,flush=True)
    expected=Counter({x["reference"]:x["quantite"] for x in report["nomenclature"]})
    if placed!=expected:
        raise RuntimeError(f"Le nombre de pièces diffère: {placed}.")
    banner=next(line for line in run_slicer(cli,"--help").splitlines() if line.startswith("PrusaSlicer"))
    report["tranchage"]={"prusa":banner,"plateau_mm":[220,220,250],
                         "maillages_fermes_et_connectes":len(meshes),"plateaux":proofs,
                         "filament_total_g":round(sum(p["filament_g"] for p in proofs),2)}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    main(Path(sys.argv[1]).resolve(strict=True))
