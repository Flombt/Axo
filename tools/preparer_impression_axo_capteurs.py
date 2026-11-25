"""Tranche et relit le plateau de quatre pièces de la variante Axo Capteurs."""

import argparse
import json
import tempfile
from pathlib import Path

import numpy as np
import trimesh

from preparer_impression import (
    MODELS, SLICER_PRESETS, audit_3mf, dump, invoke, portable, profile, sha,
)

ROOT = Path(__file__).resolve().parents[1] / "Axo bras final - Capteurs"
KEY = "Kobra_3_Max"
PRINT = ROOT / "Impression 3D"
TITLE = "Axo_Capteurs_Kobra_3_Max_PLA.3mf"
ANGLES = {"01_Bac_Pi5": 0, "02_Couvercle": 0, "03_Coque_Camera": -90, "04_Dos_Camera": 90}


def settings(exe, temporary):
    name, x, y, width, depth, z = MODELS[KEY]
    presets = exe.parent / "resources/profiles/Anycubic"
    nozzle = name + " 0.4 nozzle"
    machine = profile(presets, "machine", nozzle)
    machine.update(printable_area=[f"{x}x{y}", f"{x+width}x{y}", f"{x+width}x{y+depth}", f"{x}x{y+depth}"],
                   printable_height=str(z))
    process = profile(presets, "process", "0.20mm Standard @" + nozzle) | SLICER_PRESETS
    process.update({"name": "Axo Capteurs PLA 0.20", "from": "user", "enable_support": "1",
                    "support_on_build_plate_only": "1", "layer_height": "0.20"})
    filament = profile(presets, "filament", "Anycubic PLA @" + nozzle)
    filament.update(textured_plate_temp=["60"], textured_plate_temp_initial_layer=["60"])
    paths = [temporary / (key + ".json") for key in ("machine", "process", "filament")]
    for path, data in zip(paths, (machine, process, filament)):
        dump(path, data)
    return paths


def prepare_stls(temporary, proof):
    files = []
    mesh_stats = {}
    for key, angle in ANGLES.items():
        native = PRINT / "STL" / (key + ".stl")
        mesh = trimesh.load(native, force="mesh")
        assert mesh.is_volume and len(mesh.split(only_watertight=False)) == 1, native.name
        native_volume = proof["pieces_imprimables"][key]["volume_mm3"]
        assert abs(mesh.volume - native_volume) / native_volume < .01, key
        mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(angle), (0, 1, 0)))
        mesh.apply_translation(-(mesh.bounds[0] + mesh.bounds[1]) * [0.5, 0.5, 0]
                               - mesh.bounds[0] * [0, 0, 1])
        path = temporary / native.name
        mesh.export(path)
        files.append(str(path))
        mesh_stats[key] = {"sha256": sha(native), "volume_mm3": round(mesh.volume, 2),
                           "orientation_deg_autour_y": angle, "dimensions_orientees_mm": mesh.extents.tolist()}
    return files, mesh_stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slicer", type=Path, required=True)
    args = parser.parse_args()
    proof = json.loads((ROOT / "Contrôles" / "validation_fusion.json").read_text(encoding="utf-8"))
    final = PRINT / TITLE
    with tempfile.TemporaryDirectory(prefix="axo-capteurs-tranchage-") as temp:
        tmp = Path(temp)
        machine, process, filament = settings(args.slicer.resolve(), tmp)
        parts, mesh_stats = prepare_stls(tmp, proof)
        project = invoke(args.slicer, tmp / "premier", TITLE,
                         ["--load-settings", f"{machine};{process}", "--load-filaments", str(filament),
                          "--arrange", "1", *parts])
        ready = tmp / TITLE
        portable(project, process, ready)
        labels = list(ANGLES)
        first = audit_3mf(ready, KEY, labels, "PLA")
        again = invoke(args.slicer, tmp / "reouverture", TITLE, ["--arrange", "0", str(ready)])
        second = audit_3mf(again, KEY, labels, "PLA")
        assert len(first) == len(second) == 1
        assert set(first[0]["object_bounds"]) == set(second[0]["object_bounds"])
        assert all(np.allclose(box, second[0]["object_bounds"][key], atol=.02, rtol=0)
                   for key, box in first[0]["object_bounds"].items())
        final.write_bytes(ready.read_bytes())
    dump(ROOT / "Contrôles" / "validation_impression.json",
         {"f3d_sha256": proof["archive_sha256"], "plateau_sha256": sha(final),
          "imprimante": MODELS[KEY][0], "buse_mm": .4, "filament": "PLA",
          "maillages": mesh_stats, "plateaux": first, "reouverture_et_retranchage": True})
    print(final)


if __name__ == "__main__":
    main()
