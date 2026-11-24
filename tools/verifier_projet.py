"""Contrôle AURA-01. Lecture seule, y compris avec --complet."""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/architecture/revision.json"
SKIP = {".git", ".obsidian", ".local", ".venv"}
CACHE = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "tmp", "temp"}
TEMP_SUFFIX = {".pyc", ".pyo", ".tmp", ".part", ".log", ".bgcode"}
EXPORT_TYPES = {".stl", ".3mf", ".step", ".stp", ".gcode", ".bgcode"}
CODE_TYPES = {".py", ".ino", ".c", ".cpp", ".h", ".uf2", ".mpy"}
VAULT = ROOT / "AURA-01_Obsidian/AURA-01_Obsidian"

LINKS = (
    re.compile(r"\]\(\s*(<[^>\n]+>|(?:\\.|[^\s()<>])+)"),
    re.compile(r"^\s{0,3}\[[^]\n]+\]:\s*(<[^>\n]+>|(?:\\.|[^\s()<>])+)"),
    re.compile(r"\b(?:src|href)\s*=\s*[\"']([^\"'\n]+)[\"']", re.I),
)
WIKI = re.compile(r"\[\[([^]|\n]+)(?:\|[^]\n]*)?\]\]")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.M)
ID = re.compile(r'\b(?:id|name)=["\x27]([^"\x27]+)["\x27]')


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def path_in_repo(value: str) -> Path:
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"Chemin hors projet : {value}")
    return path


def walk(full):
    for folder, dirs, files in os.walk(ROOT):
        parent = Path(folder)
        dirs[:] = sorted(name for name in dirs if name not in SKIP and
                         (full or parent != ROOT or name != "archives"))
        yield parent, dirs, sorted(files)


def repo_rel(path):
    return path.relative_to(ROOT).as_posix()


def slug(value):
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\- ]", "", value.casefold())
    return value.replace(" ", "-")


def anchors(path, cache):
    if path not in cache:
        txt = path.read_text(encoding="utf-8-sig")
        headings = set(HEADING.findall(txt))
        slugs = defaultdict(int)
        known = set(ID.findall(txt)) | headings
        for head in HEADING.findall(txt):
            label = slug(head)
            slot = slugs[label]
            known.add(label if slot == 0 else f"{label}-{slot}")
            slugs[label] += 1
        cache[path] = known
    return cache[path]


def verify_link(from_path, value, found):
    raw = value.strip("<>")
    if raw.startswith(("http:", "https:", "mailto:", "data:")):
        return None
    parsed = urlsplit(raw)
    if parsed.scheme or raw.startswith("/"):
        return "Chemin non portable " + raw
    rel = unquote(parsed.path).replace("\\", "/")
    to_path = (from_path.parent / rel).resolve() if rel else from_path
    if not to_path.is_relative_to(ROOT):
        return "Lien hors du projet " + raw
    if not to_path.exists():
        return "Chemin manquant " + raw
    section = unquote(parsed.fragment)
    if section and to_path.is_file() and to_path.suffix.lower() == ".md":
        if section not in anchors(to_path, found) and slug(section) not in anchors(to_path, found):
            return "Section introuvable " + raw
    return None


def wiki_target(source, value, lookup):
    path, _, section = value.partition("#")
    if not path:
        return source, section
    target = Path(path)
    candidates = [VAULT / target, source.parent / target]
    if not target.suffix:
        candidates += [p.with_suffix(".md") for p in candidates]
    for candidate in candidates:
        if candidate.is_file():
            return candidate, section
    options = lookup.get(target.name.casefold(), [])
    if not options and not target.suffix:
        options = lookup.get(target.with_suffix(".md").name.casefold(), [])
    return (options[0] if len(options) == 1 else None), section


def verify_docs(markdown, errors, warnings):
    anchor_cache = {}
    names = defaultdict(list)
    if VAULT.is_dir():
        for path in VAULT.rglob("*"):
            if path.is_file() and ".obsidian" not in path.relative_to(VAULT).parts:
                names[path.name.casefold()].append(path)
    for source in markdown:
        code_fence = None
        for line_no, line in enumerate(source.read_text(encoding="utf-8-sig").splitlines(), 1):
            fence = re.match(r"^\s*(" + chr(96) * 3 + r"|~~~)", line)
            if fence:
                token = fence.group(1)
                code_fence = None if code_fence == token else token
                continue
            if code_fence is not None:
                continue
            for parser in LINKS:
                for match in parser.finditer(line):
                    issue = verify_link(source, match.group(1), anchor_cache)
                    if issue:
                        # Les fragments des documents archivés sont présentés sans masquer les fichiers absents.
                        notices = warnings if issue.startswith("Section introuvable") else errors
                        notices.append(f"{repo_rel(source)}:{line_no} · {issue}")
            if source.is_relative_to(VAULT):
                for value in WIKI.findall(line):
                    target, section = wiki_target(source, value, names)
                    if target is None:
                        errors.append(f"{repo_rel(source)}:{line_no} · Wikilien introuvable {value}")
                    elif section and target.suffix == ".md" and section not in anchors(target, anchor_cache):
                        warnings.append(f"{repo_rel(source)}:{line_no} · Section Obsidian à contrôler {value}")


def verify_revision(errors, warnings):
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    revision = data["revision"]
    for rel in data["required"]:
        if not path_in_repo(rel).is_file():
            errors.append(f"Fichier de référence absent · {rel}")
    for rel in data["revision_documents"]:
        path = path_in_repo(rel)
        if path.is_file() and revision not in path.read_text(encoding="utf-8"):
            errors.append(f"Identifiant de révision manquant · {rel}")
    cad_path = path_in_repo(data["fusion"]["path"])
    cad_hash = digest(cad_path) if cad_path.is_file() else None
    if cad_hash != data["fusion"]["sha256"]:
        errors.append(f"Empreinte CAO différente du manifeste · {repo_rel(cad_path)}")
    for key, file_field, directory, types in (
        ("fabrication", "exports", "manufacturing", EXPORT_TYPES),
        ("firmware", "files", "firmware", CODE_TYPES),
    ):
        current = data[key]
        listed = {}
        for row in current[file_field]:
            file = path_in_repo(row["path"])
            listed[file] = row
            if not file.is_file():
                errors.append(f"Livrable déclaré manquant · {row['path']}")
                continue
            if row["revision"] != revision or row.get("source_sha256") != cad_hash:
                errors.append(f"Provenance périmée · {row['path']}")
            if row.get("sha256") and digest(file) != row["sha256"]:
                errors.append(f"Empreinte de livrable différente · {row['path']}")
        for path in (ROOT / directory).rglob("*"):
            if path.is_file() and path.suffix.lower() in types and path not in listed:
                errors.append(f"Fichier actif sans provenance déclarée · {repo_rel(path)}")
        if current["status"] in {"bloquee","a_developper"}:
            warnings.append(f"{key.capitalize()} · {current['status']} pour {revision}")
        elif not listed:
            errors.append(f"Livrables absents pour le statut {current['status']} · {key}")
    if data["budget_max_eur"] != 150:
        errors.append("Le plafond budgétaire du projet doit être de 150 €.")
    return revision


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complet", action="store_true", help="Inclure les archives et leurs doublons.")
    parser.add_argument("--json", action="store_true", help="Rendre le résultat en JSON.")
    args = parser.parse_args()
    errors, warnings, docs = [], [], []
    sizes = defaultdict(list)
    revision = verify_revision(errors, warnings)
    for folder, dirs, files in walk(args.complet):
        for name in dirs:
            if name in CACHE:
                warnings.append(f"Cache local · {repo_rel(folder / name)}")
        for name in files:
            path = folder / name
            if path.suffix.lower() in TEMP_SUFFIX and not path.is_relative_to(ROOT / "archives"):
                warnings.append(f"Fichier intermédiaire · {repo_rel(path)}")
            if path.suffix.lower() == ".md":
                docs.append(path)
            sizes[path.stat().st_size].append(path)
    verify_docs(docs, errors, warnings)
    by_hash = defaultdict(list)
    for group in sizes.values():
        if len(group) > 1:
            for path in group:
                by_hash[digest(path)].append(repo_rel(path))
    duplicates = [v for v in by_hash.values() if len(v) > 1]
    result = {"revision":revision,"documents":len(docs),"erreurs":sorted(set(errors)),
              "points_ouverts":sorted(set(warnings)),"doublons_exacts":duplicates}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{revision} · {len(docs)} documents · {len(set(errors))} erreurs · "
              f"{len(set(warnings))} points ouverts · {len(duplicates)} groupes de doublons")
        for issue in result["erreurs"]:
            print("ERREUR", issue)
        for issue in result["points_ouverts"]:
            print("À CONTRÔLER", issue)
        if duplicates:
            print("Doublons conservés pour la restauration ou à examiner. Les chemins sont disponibles avec --json.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
