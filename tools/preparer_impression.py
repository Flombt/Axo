"""Orienter les solides natifs, créer les 3MF et trancher avec Anycubic Slicer Next."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

import numpy as np
import trimesh

PROOF = Path("docs/diagnostic/corrections")
OUTPUT = Path("manufacturing")
MODELS = {"Kobra_3": ("Anycubic Kobra 3",2.5,2.5,250,250,260),
          "Kobra_X":("Anycubic Kobra X",0,0,260,260,260),
          "Kobra_3_Max":("Anycubic Kobra 3 Max",3,0,420,420,500)}
XML_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
SLICER_PRESETS = {"wall_generator":"arachne","wall_loops":"4",
                  "top_shell_layers":"5","bottom_shell_layers":"5",
                  "sparse_infill_pattern":"gyroid","sparse_infill_density":"25%",
                  "outer_wall_speed":"45","inner_wall_speed":"75","initial_layer_speed":"22",
                  "bridge_speed":"24","skirt_loops":"0","enable_prime_tower":"0",
                  "support_type":"normal(auto)","support_on_build_plate_only":"0",
                  "support_threshold_angle":"35","support_expansion":"0",
                  "support_top_z_distance":"0.24","support_interface_spacing":"0.50",
                  "brim_type":"auto_brim"}


def dump(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def native_dump():
    geom=json.loads((PROOF/"geometrie_neutre.json").read_text(encoding="utf-8"))
    with gzip.open(PROOF/"maillages_natifs.json.gz","rt",encoding="utf-8") as f:
        meshes=json.load(f)
    return geom,meshes


def stand(mesh, key):
    axis=np.eye(3)
    if key.startswith(("J2_Chape","J3_Chape","Support_Service_J3","Coque_Bras","Coque_Epaule")):
        axis=np.array([[1,0,0],[0,0,1],[0,-1,0]])
    elif key.startswith(("P1", "P2", "P3", "I1","I2","I3","M1","M2","M3","A1","A2","A3","U1","U2","U3")):
        # Pivots et conduits sont vérifiés à la couche dans cette orientation.
        axis=np.eye(3)
    mesh.vertices=mesh.vertices @ axis.T
    lower,upper=mesh.bounds
    mesh.apply_translation((-float((lower[0]+upper[0])/2), -float((lower[1]+upper[1])/2), -float(lower[2])))
    return axis.tolist()


def indiv_3mf(mesh,file):
    model=ET.Element("model",{"unit":"millimeter","xmlns":XML_NS})
    resources=ET.SubElement(model,"resources")
    obj=ET.SubElement(resources,"object",{"id":"1","type":"model","name":file.stem})
    component=ET.SubElement(obj,"mesh")
    points=ET.SubElement(component,"vertices")
    for row in mesh.vertices:
        ET.SubElement(points,"vertex", dict(zip(("x","y","z"),(f"{x:.5f}" for x in row))))
    triangles=ET.SubElement(component,"triangles")
    for row in mesh.faces:
        ET.SubElement(triangles,"triangle",dict(zip(("v1","v2","v3"),map(str,row))))
    ET.SubElement(ET.SubElement(model,"build"),"item",{"objectid":"1"})
    with ZipFile(file,"w",ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",'<?xml version="1.0"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
                   '</Types>')
        z.writestr("_rels/.rels",'<?xml version="1.0"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
                   'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr("3D/3dmodel.model",ET.tostring(model,encoding="utf-8",xml_declaration=True))
    with ZipFile(file) as archive:
        if archive.testzip() is not None:
            raise ValueError("CRC invalide " + file.name)
        shape=ET.fromstring(archive.read("3D/3dmodel.model"))
    v=np.array([[float(node.attrib[k]) for k in ("x","y","z")] for node in shape.findall(".//{*}vertex")])
    f=np.array([[int(node.attrib[k]) for k in ("v1","v2","v3")] for node in shape.findall(".//{*}triangle")])
    if not np.allclose(v,mesh.vertices,atol=.0001) or not np.array_equal(f,mesh.faces):
        raise ValueError("Réouverture 3MF différente "+file.name)


def family(k):
    if len(k)==2 or k.startswith(("11_","12_","Retenue","Peigne","Capot_Paume","Bobine")):
        return "Main"
    if k.startswith(("01_","02_","03_","04_","05_","06_","J1_","Pied_","Rehausse_","Entretoise","Coque_Socle","Coque_Pico")):
        return "Socle"
    if k.startswith("Coupon"):
        return "Coupons"
    return "Bras"


def close_tessellation(mesh):
    changes=[]
    if mesh.is_volume:
        return changes
    # Le noyau peut livrer deux triangles opposés sur une même couture submicronique.
    _, index, count = np.unique(np.sort(mesh.faces,axis=1),axis=0,return_inverse=True,return_counts=True)
    keep=np.ones(len(mesh.faces),dtype=bool)
    for multiple in np.flatnonzero(count==2):
        pair=np.flatnonzero(index==multiple)
        if (max(mesh.area_faces[pair]) < .001
                and np.dot(*mesh.face_normals[pair]) < -.99):
            keep[pair]=False
    if not np.all(keep):
        changes.append({"type":"paires de triangles opposés","triangles":int((~keep).sum())})
        mesh.update_faces(keep)
        mesh.remove_unreferenced_vertices()
    if mesh.is_volume:
        return changes

    # Une couture en T conserve exactement les mêmes sommets de surface.
    boundary=mesh.edges_unique[np.bincount(mesh.edges_unique_inverse)==1]
    if len(boundary)<3:
        return changes
    for vertices in trimesh.graph.connected_components(boundary, min_len=3):
        if len(vertices)!=3:
            continue
        seam=boundary[np.isin(boundary,vertices).all(axis=1)]
        if len(seam)!=3:
            continue
        lengths=np.linalg.norm(mesh.vertices[seam[:,0]]-mesh.vertices[seam[:,1]],axis=1)
        index=int(np.argmax(lengths))
        if 2*lengths[index]-lengths.sum() > -1e-5:
            a,b=seam[index]
            w=next(v for v in vertices if v!=a and v!=b)
            matches=np.flatnonzero((mesh.faces==a).any(axis=1)&(mesh.faces==b).any(axis=1))
            if len(matches)==1:
                i=int(matches[0])
                face=mesh.faces[i].tolist()
                if face[(face.index(a)+1)%3]!=b:
                    a,b=b,a
                c=next(v for v in face if v!=a and v!=b)
                mesh.faces=np.vstack([np.delete(mesh.faces,i,axis=0),[a,w,c],[w,b,c]])
                changes.append({"type":"couture T fermée sans ajout de point","triangles":1})
    return changes


def export_parts():
    geom, meshes=native_dump()
    meta=geom["parts"]
    slots={}
    for data in meshes:
        key=data["part"]
        if meta[key]["print_ref"]:
            slots.setdefault(key,[]).append(data)
    coupon_file=PROOF/"coupons_natifs.json"
    if coupon_file.is_file():
        for d in json.loads(coupon_file.read_text(encoding="utf-8")):
            slots[d["part"]]=[d]
            meta[d["part"]]={"print_ref":d["part"],"name":d["part"],
                             "volume_mm3":d["volume_mm3"], "coupon":True}

    inventory=[]
    variants={}
    for key,records in slots.items():
        p=meta[key]
        parts=[trimesh.Trimesh(vertices=d["v"],faces=np.asarray(d["f"]).reshape(-1,3),
                               process=True,validate=True) for d in records]
        mesh=trimesh.util.concatenate(parts)
        changes=close_tessellation(mesh)
        rel=abs(mesh.volume-p["volume_mm3"])/p["volume_mm3"]
        tolerance=.033 if p.get("coupon") else geom["mesh_tolerance_mm"]
        if not mesh.is_volume or rel>.03 or abs(mesh.volume-p["volume_mm3"])>mesh.area*tolerance:
            raise ValueError(f"Maillage {key} fermeture={mesh.is_watertight}, erreur volume={rel:.4f}")
        axes=stand(mesh,key)
        dims=(mesh.bounds[1]-mesh.bounds[0]).round(4).tolist()
        fingerprint=hashlib.sha256(np.unique(np.round(mesh.vertices,3),axis=0).tobytes()).hexdigest()
        group=p["print_ref"]
        by_shape=variants.setdefault(group,{})
        if fingerprint in by_shape:
            by_shape[fingerprint]["parts"].append(key)
            continue
        slug=group if not by_shape else f"{group}_{len(by_shape)+1}"
        if key.startswith("Pied_Rehausse"):
            slug=group
        stl=OUTPUT/"STL"/(slug+".stl")
        file=OUTPUT/"3MF"/(slug+".3mf")
        for path in (stl,file):
            path.parent.mkdir(parents=True,exist_ok=True)
        mesh.export(stl)
        indiv_3mf(mesh,file)
        row={"ref":slug,"parts":[key],"dims_mm":dims,"orientation":axes,"mesh_volume_mm3":round(mesh.volume,4),
             "brep_volume_mm3":round(p["volume_mm3"],4),"relative_error_volume":rel,
             "tris":len(mesh.faces),"corrections_tessellation":changes,"stl":stl.as_posix(),"3mf":file.as_posix(),"stl_sha256":sha(stl),
             "3mf_sha256":sha(file),"family":family(key)}
        inventory.append(row)
        by_shape[fingerprint]=row
    dump(OUTPUT/"inventaire.json",{"revision":"V5-stabilisation","fusion_sha256":sha(Path("fusion/AURA-01.f3d")),
                                  "stl_unit":"mm","references":inventory})
    return inventory


def profile(profiles, kind, name):
    path=profiles/kind/(name+".json")
    item=json.loads(path.read_text(encoding="utf-8-sig"))
    parent=item.get("inherits","")
    return (profile(profiles,kind,parent)|item) if parent else item


def config(exe, target, key, cohort):
    name,x,y,w,h,z=MODELS[key]
    root=exe.parent/"resources/profiles/Anycubic"
    nozzle=name+" 0.4 nozzle"
    machine=profile(root,"machine",nozzle)
    machine.update(printable_area=[f"{x}x{y}",f"{x+w}x{y}",f"{x+w}x{y+h}",f"{x}x{y+h}"],
                   printable_height=str(z))
    process_name="0.20mm Standard @"+nozzle
    proc=profile(root,"process",process_name)|SLICER_PRESETS
    proc.update(name=f"AURA V5 PETG {key} {cohort}", enable_support="0" if cohort=="Coupons" else "1",
                layer_height="0.16" if cohort in {"Main","Doigt"} else "0.20",
                sparse_infill_density="30%" if cohort in {"Bras","Socle"} else "25%")
    if key=="Kobra_3" and cohort=="Socle":
        proc.update(wall_generator="classic",line_width="0.42",outer_wall_line_width="0.42",
                    inner_wall_line_width="0.45",support_line_width="0.42")
    proc["from"]="user"
    material=profile(root,"filament","Anycubic PETG @"+nozzle)
    material.update(textured_plate_temp=["60"],textured_plate_temp_initial_layer=["60"],
                    hot_plate_temp=["60"],hot_plate_temp_initial_layer=["60"])
    paths=[target/(s+".json") for s in ("machine","process","filament")]
    for p,data in zip(paths,(machine,proc,material)):
        dump(p,data)
    return paths


def metadata(node):
    return {n.get("key"):n.get("value") for n in node.findall("metadata")}


def audit_3mf(path,key,labels,filament="PETG"):
    with ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError("CRC 3MF")
        cfg=json.loads(z.read("Metadata/project_settings.config"))
        if cfg["printer_model"]!=MODELS[key][0] or cfg["nozzle_diameter"]!=["0.4"] or cfg["filament_type"]!=[filament]:
            raise ValueError("Profil appliqué inattendu")
        settings=ET.fromstring(z.read("Metadata/slice_info.config"))
        plates=[]
        names=[]
        for plate in settings.findall("plate"):
            info=metadata(plate)
            ordinal=int(info["index"])
            if info["outside"]!="false":
                raise ValueError(f"Plateau {ordinal} hors zone")
            names.extend(n.get("name") for n in plate.findall("object") if n.get("skipped")=="false")
            raw=z.read(f"Metadata/plate_{ordinal}.gcode")
            stats=json.loads(z.read(f"Metadata/plate_{ordinal}.json"))
            bounds=stats.get("bbox_all")
            if b";TYPE:Outer wall" not in raw:
                raise ValueError("G-code sans périmètre extérieur")
            printable_area=MODELS[key][1:-1]
            x,y,w,h=printable_area
            if bounds and not (x-.1<=bounds[0]<=bounds[2]<=x+w+.1 and y-.1<=bounds[1]<=bounds[3]<=y+h+.1):
                raise ValueError(f"Emprise hors volume nominal {bounds}")
            plates.append(dict(ordinal=ordinal,seconds=int(info["prediction"]),grams=float(info["weight"]),
                               bounds=bounds,object_bounds={obj["name"]:obj["bbox"] for obj in stats["bbox_objects"]},layers=raw.count(b";LAYER_CHANGE"),supports=info.get("support_used"),
                               warnings=[n.attrib for n in plate.findall("warning")]))
        if Counter(Path(s).stem for s in names)!=Counter(labels):
            raise ValueError(f"Objets tranchés différents {names} au lieu de {labels}")
        return plates


def invoke(exe,work,name,args):
    work.mkdir(parents=True,exist_ok=True)
    log=work/"tranchage.log"
    with log.open("wb") as out:
        run=subprocess.run([str(exe),"--debug","2","--outputdir",str(work),*args,
                            "--slice","0","--export-3mf",name],cwd=exe.parent,
                           stdout=out,stderr=subprocess.STDOUT,timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
    path=work/name
    if run.returncode or not path.is_file():
        msg=log.read_text(encoding="utf8",errors="replace").splitlines()[-18:]
        raise RuntimeError(f"{name} code {run.returncode} "+ " | ".join(msg))
    return path


def portable(source,process,dest):
    with ZipFile(source) as native, ZipFile(dest,"w",ZIP_DEFLATED) as archive:
        config=json.loads(native.read("Metadata/project_settings.config"))
        p=json.loads(process.read_text(encoding="utf-8"))
        p.update(print_settings_id=config.get("print_settings_id",p["name"]),version=config.get("version","2.0.0.3"))
        for key in native.namelist():
            if key!="Metadata/project_settings.config" and not key.startswith("Metadata/process_settings_"):
                archive.writestr(key,native.read(key))
        archive.writestr("Metadata/project_settings.config",json.dumps(config))
        archive.writestr("Metadata/process_settings_1.json",json.dumps(p))


def slice_task(exe, temp, key, stem, cohort, rows):
    work=temp/key/stem
    work.mkdir(parents=True,exist_ok=True)
    machine,process,material=config(exe,work,key,cohort)
    paths=[]
    for row,key_part in rows:
        target=work/(key_part+".stl")
        shutil.copyfile(row["stl"],target)
        paths.append(str(target))
    labels=[p for _,p in rows]
    name="AURA_V5_"+stem+".3mf"
    native=invoke(exe,work,name,["--load-settings",str(machine)+";"+str(process),
                                "--load-filaments",str(material),"--arrange","1",*paths])
    candidate=work/("controle_"+name)
    portable(native,process,candidate)
    first=audit_3mf(candidate,key,labels)
    again=invoke(exe,work/"reouverture",name,["--arrange","0",str(candidate)])
    second=audit_3mf(again,key,labels)
    if len(first)!=len(second) or any(
            not np.allclose(a["bounds"],b["bounds"],atol=.02,rtol=0)
            or set(a["object_bounds"])!=set(b["object_bounds"])
            or any(not np.allclose(x,b["object_bounds"][k],atol=.02,rtol=0) for k,x in a["object_bounds"].items())
            for a,b in zip(first,second)):
        raise ValueError("Emprises différentes après réouverture")
    folder=OUTPUT/"Anycubic"/key
    folder.mkdir(parents=True,exist_ok=True)
    destination=folder/name
    shutil.copyfile(candidate,destination)
    return dict(machine=key,group=cohort,files=len(labels),path=destination.as_posix(),plates=first,sha256=sha(destination))


def jobs(rows,keys):
    for key in keys:
        for fam in ("Coupons","Doigt","Socle","Bras","Main"):
            selected=[(r,k) for r in rows if r["family"]==fam for k in r["parts"]]
            if fam=="Coupons":
                selected+= [(r,"Eprouvette_"+r["ref"]) for r in rows if set(r["parts"]) & {"J2_Pignon","J2_Roue","J3_Pignon","J3_Roue"}]
            if fam=="Doigt":
                selected=[(r,"Eprouvette_P3") for r in rows if "P3" in r["parts"]]
            if selected:
                yield key,fam,fam,selected


def check_individuals(exe,rows):
    def info(file,row):
        result=subprocess.run([str(exe),"--debug","2","--info",str(file.resolve())],
                              cwd=exe.parent,capture_output=True,text=True,errors="replace",
                              creationflags=subprocess.CREATE_NO_WINDOW,timeout=30,check=True)
        report={}
        for line in result.stdout.splitlines():
            if " = " in line:
                key,value=line.split(" = ",1)
                report[key.strip()]=value.strip()
        dims=[float(report["size_"+axis]) for axis in "xyz"]
        if report.get("manifold")!="yes" or not np.allclose(dims,row["dims_mm"],atol=.03,rtol=0):
            raise ValueError(f"Réouverture Anycubic différente pour {file.name}")
        return {"path":file.as_posix(),"triangles":int(report["number_of_facets"]),
                "size_mm":dims,"volume_mm3":float(report["volume"]),"manifold":True}

    with ThreadPoolExecutor(max_workers=3) as pool:
        submitted=[pool.submit(info,Path(row[k]),row) for row in rows for k in ("stl","3mf")]
        proof=[task.result() for task in submitted]
    dump(OUTPUT/"Anycubic"/"individuels.json",
         {"source_sha256":sha(Path("fusion/AURA-01.f3d")),"reader":"Anycubic Slicer Next 2.0.0.3","files":proof})
    print("Maillages réouverts",len(proof),flush=True)


def run():
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",type=Path)
    ap.add_argument("--machine",choices=tuple(MODELS)+("all",),default="all")
    ap.add_argument("--group",action="append",choices=("Coupons","Doigt","Socle","Bras","Main"))
    ap.add_argument("--info-only",action="store_true")
    ap.add_argument("--assets-only",action="store_true")
    ap.add_argument("--skip-assets",action="store_true")
    ns=ap.parse_args()
    rows=json.loads((OUTPUT/"inventaire.json").read_text(encoding="utf-8"))["references"] if ns.skip_assets else export_parts()
    print("Références",len(rows),"occurrences imprimées",sum(len(r["parts"]) for r in rows),flush=True)
    if ns.assets_only:
        return
    if not ns.exe or not ns.exe.is_file():
        ap.error("--exe requis pour le tranchage")
    if ns.info_only:
        check_individuals(ns.exe,rows)
        return
    work=Path(tempfile.gettempdir())/"aura-stabilisation"/"tranchage"
    verify=OUTPUT/"Anycubic"/"verification.json"
    old=json.loads(verify.read_text(encoding="utf8")) if verify.is_file() else {}
    keys=MODELS if ns.machine=="all" else [ns.machine]
    selection=[j for j in jobs(rows,keys) if not ns.group or j[2] in ns.group]
    chosen={j[:2] for j in selection}
    keep=old.get("source_sha256")==sha(Path("fusion/AURA-01.f3d"))
    results=[x for x in old.get("profiles",[]) if keep and (x["machine"],x["group"]) not in chosen]
    errors=[x for x in old.get("errors",[]) if keep and (x["machine"],x["plate"]) not in chosen]
    with ThreadPoolExecutor(max_workers=2) as pool:
        tasks={pool.submit(slice_task,ns.exe,work,*j):j[:2] for j in selection}
        for task in as_completed(tasks):
            key,stem=tasks[task]
            try:
                val=task.result()
                results.append(val)
                print(key,stem,len(val["plates"]),sum(p["grams"] for p in val["plates"]),flush=True)
            except Exception as e:
                errors.append(dict(machine=key,plate=stem,erreur=str(e)))
                print(key,stem,str(e),flush=True)
    dump(OUTPUT/"Anycubic"/"verification.json",{"source_sha256":sha(Path("fusion/AURA-01.f3d")),
                                               "profiles":sorted(results,key=lambda q:q["path"]),"errors":errors})
    if errors:
        raise SystemExit(1)


if __name__=="__main__":
    run()
