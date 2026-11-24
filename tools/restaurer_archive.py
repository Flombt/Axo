"""Restaurer une vidéo publiée ou le miroir USB dans un dossier séparé."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "archives/RESTORE_ASSETS.json"


def restore_file(dest, expected, source):
    if dest.exists():
        raise FileExistsError(f"Le fichier de destination existe : {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp = dest.with_name(dest.name + ".part")
    with temp.open("xb") as output:
        try:
            with source() as stream:
                shutil.copyfileobj(stream, output, 1024 * 1024)
        except BaseException:
            output.close()
            temp.unlink()
            raise
    with temp.open("rb") as stream:
        computed = hashlib.file_digest(stream, "sha256").hexdigest()
    if computed != expected["sha256"] or temp.stat().st_size != expected["size"]:
        temp.unlink()
        raise ValueError(f"Empreinte ou taille différente : {dest.name}")
    temp.rename(dest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--video", help="Nom exact dans archives/RESTORE_ASSETS.json.")
    mode.add_argument("--miroir-usb", action="store_true")
    args = parser.parse_args()
    data = json.loads(ASSETS.read_text(encoding="utf-8"))
    destination = args.destination.resolve()
    if destination.is_relative_to(ROOT):
        parser.error("Choisir un dossier de restauration à l’extérieur du projet.")
    if args.video:
        row = data["videos_r03"].get(args.video)
        if row is None:
            parser.error("Vidéo inconnue du manifeste.")
        restore_file(destination / args.video, row, lambda: urlopen(row["url"], timeout=60))
        print(f"Vidéo vérifiée · {args.video}")
        return
    files = [(name, row, (destination / name).resolve()) for name, row in data["miroir_usb"].items()]
    if any(not target.is_relative_to(destination) or target.exists() for _, _, target in files):
        parser.error("Le miroir contient un chemin interdit ou une destination existante.")
    for name, row, target in files:
        source = (ROOT / row["path"]).resolve()
        if not source.is_relative_to(ROOT) or not source.is_file():
            raise FileNotFoundError(f"Source de restauration manquante : {name}")
        restore_file(target, row, lambda: source.open("rb"))
    print(f"{len(files)} copies USB restaurées et vérifiées.")


if __name__ == "__main__":
    main()
