"""Point d'entrée Fusion pour l'intégration mécatronique AURA-01."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import traceback
from zipfile import ZipFile

import adsk.core as core
import adsk.fusion as fusion
import adsk


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROOF = ROOT / "Verification_Fusion.json"
V3 = ROOT.parent / "AURA_V3"
R03 = V3 / "Fabrication_r03/AURA-01_V3_FDM_r03.f3d"
R03_SHA256 = "d38022761fa19056245025fe9375998c66fc1983c6b01918c6e7a26e85b234cb"
BRANCH = ROOT / "AURA-01 — V3 — Intégration mécatronique.f3d"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def digest(file):
    return sha256(file.read_bytes()).hexdigest()


def write(report):
    tmp = PROOF.with_suffix(".tmp")
    tmp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n", encoding="utf-8")
    tmp.replace(PROOF)


def import_archive(app, source):
    manager = app.importManager
    doc = manager.importToNewDocument(manager.createFusionArchiveImportOptions(str(source)))
    if not doc:
        raise RuntimeError(f"Fusion ne peut pas ouvrir {source.name}.")
    return doc


def get_design(doc):
    design = fusion.Design.cast(doc.products.itemByProductType("DesignProductType"))
    if not design:
        raise RuntimeError("Document de conception absent.")
    return design


def export_archive(design, location):
    tmp = location.with_name(location.stem+"_en_cours.f3d")
    export = design.exportManager
    if not export.execute(export.createFusionArchiveExportOptions(str(tmp))):
        raise RuntimeError(f"Échec d'export Fusion pour {location.name}.")
    with ZipFile(tmp) as z:
        if z.testzip():
            raise RuntimeError("Archive incomplète.")
    tmp.replace(location)


def reopen_and_branch(app, proof):
    if digest(R03) != R03_SHA256:
        raise RuntimeError("L'archive r03 diffère de l'empreinte de référence.")
    if proof.get("reprise",{}).get("sha256_source") == R03_SHA256 and BRANCH.exists():
        return
    document = import_archive(app,R03)
    design = get_design(document)
    root = design.rootComponent
    counts = (root.occurrences.count,root.asBuiltJoints.count)
    if counts != (23,22):
        raise RuntimeError(f"Occurrences et pivots de r03 inattendus : {counts}.")
    refs=[]
    for occ in root.occurrences:
        if any(b.name.startswith("Enveloppe servo") for b in occ.bRepBodies):
            refs.append(occ.name)
    if len(refs)!=18:
        raise RuntimeError("Inventaire des enveloppes r03 incomplet.")
    root.attributes.add("AURA-01","Branche","AURA-01 — V3 — Intégration mécatronique")
    root.attributes.add("AURA-01","Source_r03",R03_SHA256)
    export_archive(design,BRANCH)
    proof["reprise"]={"source":R03.name,"sha256_source":R03_SHA256,"r03_rouverte_dans_fusion":True,
                      "pivots":counts[1],"occurrences":counts[0],"enveloppes_moteur":refs,
                      "branche":BRANCH.name,"sha256_branche":digest(BRANCH)}
    proof["etape"]="R03 rouverte et branche indépendante sauvegardée"
    write(proof)
    document.close(False)


def run(_context):
    app = core.Application.get()
    proof = json.loads(PROOF.read_text(encoding="utf-8")) if PROOF.exists() else {}
    proof.pop("erreur",None)
    proof["fusion"] = app.version
    try:
        reopen_and_branch(app,proof)
        for module_name in ("doigt","epaule","integration","controle"):
            source = HERE/(module_name+".py")
            if source.is_file():
                part = load(source,"aura_integration_"+module_name)
                revision = getattr(part,"REVISION",1)
                previous = proof.get(module_name,{})
                if previous.get("termine") and previous.get("revision_modele",1) == revision:
                    continue
                proof["etape"] = "Contrôle Fusion "+module_name
                write(proof)
                base = load(V3/"Generateur_AURA_V3/geometrie.py","aura_geometrie_base")
                util = load(HERE/"atelier.py","aura_atelier")
                errors = proof.setdefault("erreurs_par_phase",{})
                try:
                    part.build(app,base,util,proof,write,export_archive,import_archive,get_design)
                    proof[module_name]["revision_modele"] = revision
                    errors.pop(module_name,None)
                except Exception:
                    errors[module_name] = traceback.format_exc()
                    adsk.log(errors[module_name])
                write(proof)
    except Exception:
        proof["erreur"] = traceback.format_exc()
        write(proof)
        adsk.log(proof["erreur"])
