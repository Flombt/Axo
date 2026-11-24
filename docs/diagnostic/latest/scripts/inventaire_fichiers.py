"""Contrôles STL, 3MF, archives Fusion, STEP et Blender. Exécuter depuis Aura."""
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys
from xml.etree import ElementTree as ET
import zipfile

try:
    import numpy as np
    import trimesh
except ModuleNotFoundError:
    sys.path.insert(0, str(Path.home() / "AppData/Local/Temp/aura-audit-deps"))
    import numpy as np
    import trimesh

ROOT = Path.cwd()
OUT = ROOT / "docs/diagnostic/latest/preuves"
EXTENSIONS = {".f3d", ".f3z", ".stl", ".step", ".stp", ".3mf", ".blend", ".mp4"}
WORK = Path("D:/")
SOURCES = [ROOT] + sorted(p for p in WORK.glob("AURA-01-*20261124") if p.is_dir())
VOLUMES = {"Kobra_3": (250, 250, 260), "Kobra_X": (260, 260, 260), "Kobra_3_Max": (420, 420, 500)}
THREE_MF_UNITS = {"micron": .001, "millimeter": 1, "centimeter": 10, "inch": 25.4, "foot": 304.8, "meter": 1000}
NS = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"


def round_list(values):
    return np.round(values, 4).tolist()


def mesh_record(v, f):
    if not len(v) or not len(f) or not np.isfinite(v).all() or f.min() < 0 or f.max() >= len(v):
        raise ValueError("Maillage vide, coordonnées ou indices invalides.")
    mesh = trimesh.Trimesh(vertices=v, faces=f, process=False)
    mesh.merge_vertices(digits_vertex=5)
    return {
        "triangles": len(f), "vertices": len(mesh.vertices),
        "bounds_mm": round_list(mesh.bounds), "size_mm": round_list(mesh.extents),
        "watertight": bool(mesh.is_watertight), "consistent_winding": bool(mesh.is_winding_consistent),
        "degenerate": int(len(f) - np.count_nonzero(mesh.nondegenerate_faces(height=1e-7))),
        "volume_mm3": round(mesh.volume, 4),
    }


def stl_record(path):
    with path.open("rb") as stream:
        header = stream.read(84)
    binary = len(header) == 84 and path.stat().st_size == 84 + 50 * struct.unpack("<I", header[80:])[0]
    mesh = trimesh.load_mesh(path, file_type="stl", process=False)
    report = mesh_record(mesh.vertices, mesh.faces)
    report.update(binary=binary, reading_unit="mm (STL sans unité)")
    return report


def transform(vertices, value):
    if not value:
        return vertices
    matrix = np.asarray(value.split(), float).reshape(4, 3)
    return vertices @ matrix[:3] + matrix[3, :]


def xml_items(node, tag):
    return node.iter(f"{NS}{tag}")


def read_3mf(path):
    with zipfile.ZipFile(path) as archive:
        container_error = archive.testzip()
        if container_error:
            raise ValueError(f"Intégrité ZIP en échec pour {container_error}.")
        paths = set(archive.namelist())
        models = sorted(p for p in paths if p.lower().endswith(".model"))
        if not models:
            raise ValueError("Aucun modèle XML 3MF.")
        main = next((p for p in models if p.lower() == "3d/3dmodel.model"), models[0])
        nodes = {name: ET.fromstring(archive.read(name)) for name in models}
        definitions = {(name, obj.attrib["id"]): obj for name, node in nodes.items()
                       for obj in xml_items(node, "object")}
        unit = nodes[main].get("unit", "millimeter")
        scale = THREE_MF_UNITS[unit]
        mesh_points, meshes = {}, {}
        for key, obj in definitions.items():
            if obj.find(f"{NS}mesh") is None:
                continue
            v = np.array([[float(p.attrib[c]) for c in "xyz"] for p in xml_items(obj, "vertex")])
            f = np.array([[int(t.attrib[k]) for k in ("v1", "v2", "v3")] for t in xml_items(obj, "triangle")])
            mesh_points[key] = v
            meshes["|".join(key)] = mesh_record(v * scale, f)
        setting_file = "Metadata/project_settings.config"
        settings = json.loads(archive.read(setting_file)) if setting_file in paths else {}
        fields = ("printer_settings_id", "print_settings_id", "filament_type", "nozzle_diameter",
                  "layer_height", "wall_loops", "sparse_infill_density", "enable_support",
                  "support_on_build_plate_only", "support_type", "printable_area", "printable_height")
        profile = {k: settings[k] for k in fields if k in settings}
        cfg_path = "Metadata/model_settings.config"
        names = {}
        if cfg_path in paths:
            cfg = ET.fromstring(archive.read(cfg_path))
            for obj in cfg.findall("./object"):
                names[obj.attrib["id"]] = next((m.attrib["value"] for m in obj.findall("metadata")
                                               if m.attrib.get("key") == "name"), "")
        def resolved_points(name, ident, seen=()):
            key = (name, ident)
            if key in seen:
                raise ValueError(f"Cycle de composants 3MF {key}.")
            if key in mesh_points:
                return mesh_points[key]
            obj = definitions[key]
            parts = []
            for component in xml_items(obj, "component"):
                child_file = next((v.lstrip("/") for k, v in component.attrib.items() if k.endswith("}path")), name)
                parts.append(transform(resolved_points(child_file, component.get("objectid"), (*seen, key)),
                                       component.get("transform")))
            if not parts:
                raise ValueError(f"Objet 3MF sans maillage pour {key}.")
            return np.concatenate(parts)

        build = []
        for item in xml_items(nodes[main], "item"):
            ident = item.attrib["objectid"]
            object_file = next((v.lstrip("/") for k, v in item.attrib.items() if k.endswith("}path")), main)
            v = transform(resolved_points(object_file, ident), item.get("transform")) * scale
            build.append({"id": ident, "name": names.get(ident, ""), "bounds_mm": round_list([v.min(axis=0), v.max(axis=0)]),
                          "transform": item.get("transform")})
        footprint = None
        if build:
            bounds = np.array([obj["bounds_mm"] for obj in build])
            footprint = round_list([bounds[:, 0, :].min(axis=0), bounds[:, 1, :].max(axis=0)])
        gcode = [p for p in paths if p.lower().endswith(".gcode")]
        slice_info = {}
        if "Metadata/slice_info.config" in paths:
            sliced = ET.fromstring(archive.read("Metadata/slice_info.config"))
            for plate in sliced.findall("./plate"):
                short = {m.get("key"): m.get("value") for m in plate.findall("metadata")}
                filaments = [f.attrib for f in plate.findall("filament")]
                slice_info[short.get("index", str(len(slice_info) + 1))] = {"metadata": short, "filament": filaments}
        return {"unit": unit, "build": build, "meshes": meshes, "footprint_mm": footprint,
                "profile": profile, "gcode_count": len(gcode), "slice_info": slice_info}


def revision(path):
    if path == ROOT / "fusion/AURA-01.f3d":
        return "V5 roulis"
    label = str(path).casefold()
    if "roulis" in label and ("v5" in label or "20261124" in label):
        if path.name.startswith("Phase0_"):
            return "V5 revue (source phase 0)"
        return "V5 roulis"
    if "v5" in label:
        if path.name.startswith("Phase0_"):
            return "r05 (source phase 0)"
        return "V5 revue"
    if "r05" in label:
        return "r05"
    if "r04" in label:
        return "r04"
    if "table_r03" in label or "cinematique-r03" in label:
        return "table r03"
    if any(t in label for t in ("notice_montage", "aura-009_montage")):
        return "table r02"
    return "autres archives"


def path_label(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = sorted(p for base in SOURCES for p in base.rglob("*")
                   if p.suffix.lower() in EXTENSIONS
                   and ".git" not in p.parts and "latest" not in p.parts and p.is_file())
    inventory = []
    geometry = {}
    failures = []
    for path in paths:
        data = {"path": path_label(path), "revision": revision(path), "type": path.suffix.lower(),
                "bytes": path.stat().st_size}
        try:
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            data["sha256"] = digest
            if digest not in geometry:
                if path.suffix.lower() == ".stl":
                    geometry[digest] = stl_record(path)
                elif path.suffix.lower() == ".3mf":
                    geometry[digest] = read_3mf(path)
                elif path.suffix.lower() in (".f3d", ".f3z"):
                    with zipfile.ZipFile(path) as archive:
                        geometry[digest] = {"zip_ok": archive.testzip() is None, "members": len(archive.namelist())}
                else:
                    with path.open("rb") as stream:
                        head = stream.read(96)
                    if path.suffix.lower() in (".step", ".stp"):
                        geometry[digest] = {"step_header": head.startswith(b"ISO-10303-21"), "schema_check": "en-tête"}
                    elif path.suffix.lower() == ".blend":
                        geometry[digest] = {"header_hex": head[:15].hex()}
            item = geometry.get(digest, {})
            data.update({k: item[k] for k in ("size_mm", "watertight", "consistent_winding", "degenerate", "volume_mm3",
                                             "unit", "footprint_mm", "gcode_count") if k in item})
            if "profile" in item:
                data["printer"] = item["profile"].get("printer_settings_id", "")
            if path.suffix.lower() == ".3mf":
                model = next((k for k in VOLUMES if k in path.parts), None)
                if model and item["footprint_mm"]:
                    lo, hi = item["footprint_mm"]
                    data["official_bed"] = model
                    data["fits_official_bed"] = all(a >= -.1 and b <= c + .1 for a, b, c in zip(lo, hi, VOLUMES[model]))
        except (ValueError, RuntimeError, OSError, KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
            data["error"] = str(exc)
            failures.append(data["path"])
        inventory.append(data)
    (OUT / "inventaire_fichiers.json").write_text(json.dumps({"files": inventory, "by_sha256": geometry},
                                                            ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "inventaire_fichiers.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        fields = sorted({k for x in inventory for k in x})
        writer = csv.DictWriter(stream, fields, delimiter=";")
        writer.writeheader()
        writer.writerows(inventory)
    print(json.dumps({"count":len(inventory), "unique":len({d.get("sha256") for d in inventory}),
                      "extensions":{ext:sum(d["type"] == ext for d in inventory) for ext in sorted(EXTENSIONS)},
                      "errors":failures}, ensure_ascii=False))


if __name__ == "__main__":
    run()
