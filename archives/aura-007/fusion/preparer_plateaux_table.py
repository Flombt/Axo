"""Vérifie les STL de la r01 et tranche trois projets 3MF locaux."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "AURA_V3" / "Fabrication_r03"))

from preparer_plateaux import inspect_stl, make3mf, pack, run_slicer, slice_project


def main(cli):
    report = json.loads((OUT / "Verification_Fusion.json").read_text(encoding="utf-8"))
    if report["interferences"]:
        raise RuntimeError("La révision contient des interférences Fusion.")
    meshes = {}
    for part in report["nomenclature"]:
        file = OUT / "STL" / part["stl"]
        if sha256(file.read_bytes()).hexdigest() != part["sha256"]:
            raise RuntimeError(f"Export modifié : {file.name}")
        meshes[part["reference"]] = inspect_stl(file, part["dimensions_mm"])
    base, socle, tourelle, bras, avant, bout, main, capot1, capot2 = meshes
    configurations = (
        ("01_Platine_socle_tourelle", ((base,), (socle, tourelle))),
        ("02_Segments_et_capots", ((bras, avant, bout), (capot1, capot2))),
        ("03_Main_blanche", ((main,),)),
    )
    sizes = {name: mesh[2] for name, mesh in meshes.items()}
    destination = OUT / "Plateaux_PrusaSlicer"
    destination.mkdir(exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="AURA007_slicer_") as work:
        work = Path(work)
        for name, rows in configurations:
            layout = pack(rows, sizes)
            source = work / "source.3mf"
            make3mf(source, layout, meshes)
            output = destination / (name + ".3mf")
            check = slice_project(cli, source, output, len(layout), work)
            check["pieces"] = [name for name, _, _ in layout]
            results.append(check)
            print(check, flush=True)
    summary = {
        "prusa": next(line for line in run_slicer(cli, "--help").splitlines() if line.startswith("PrusaSlicer")),
        "plateau_mm": [220, 220, 250],
        "buse_mm": 0.4,
        "couche_mm": 0.2,
        "materiau": "PETG",
        "pieces_verifiees": len(meshes),
        "filament_total_g": round(sum(p["filament_g"] for p in results), 2),
        "plateaux": results,
    }
    (OUT / "Verification_Tranchage.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
