"""Vérifie les STL en mm et tranche le bras à phalanges sur trois plateaux."""

import json
from hashlib import sha256
from pathlib import Path
import sys
import tempfile


OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "AURA_V3" / "Fabrication_r03"))

from preparer_plateaux import inspect_stl, make3mf, pack, run_slicer, slice_project


def main(slicer):
    data = json.loads((OUT/"Verification_Fusion.json").read_text(encoding="utf-8"))
    if data["erreurs"]:
        raise RuntimeError("Les collisions doivent être résolues avant de constituer les plateaux.")
    meshes = {}
    for part in data["nomenclature"]:
        file = OUT/"STL"/part["stl"]
        if sha256(file.read_bytes()).hexdigest() != part["sha256"]:
            raise RuntimeError(f"Maillage modifié : {file.name}.")
        meshes[part["reference"]] = inspect_stl(file, part["dimensions_mm"])
    rows = [
        ("01_Platine_socle_tourelle", (("01_Platine",), ("02_Socle", "03_Tourelle"))),
        ("02_Segments_transmission", (("04_Segment_1", "05_Segment_2", "06_Segment_3"),
                                     ("08_Capot", "09_Capot", "10_Tambour", "11_Palonnier"))),
        ("03_Main_blanche_articulee",
         [("07_Paume",)] + [(f"Phalange_pouce_{i}", *([f"Phalange_doigt_{i}"]*4))
                            for i in range(1, 4)]),
    ]
    dims = {name: shape[2] for name, shape in meshes.items()}
    output = OUT/"Plateaux_PrusaSlicer"
    output.mkdir(exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="Aura008_") as path:
        area = Path(path)
        for name, parts in rows:
            source = area/"source.3mf"
            plan = pack(parts, dims)
            make3mf(source, plan, meshes)
            result = slice_project(slicer, source, output/(name+".3mf"), len(plan), area)
            result["pieces"] = [code for code, _, _ in plan]
            results.append(result)
            print(result, flush=True)
    assert sum(r["instances"] for r in results) == data["pieces_fdm"] == 26
    summary = {"trancheur": next(line for line in run_slicer(slicer, "--help").splitlines()
                                 if line.startswith("PrusaSlicer")),
               "profil": "PETG · 0,20 mm · buse 0,4 mm",
               "quantites": {"stl": len(meshes), "pieces": data["pieces_fdm"]},
               "filament_g": round(sum(p["filament_g"] for p in results), 2),
               "plateaux": results}
    (OUT/"Verification_Tranchage.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n",
                                                  encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
