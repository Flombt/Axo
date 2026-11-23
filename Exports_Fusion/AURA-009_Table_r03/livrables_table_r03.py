"""Exports natifs, solides imprimables et tessellation de l'assemblage r03."""

import gzip
from hashlib import sha256
import json
from pathlib import Path

import adsk.core as core
import adsk.fusion as fusion

from construire_table_r03 import TITLE, ORIENTATIONS
from geometrie import frame
from verification_table_r03 import ExistingTable, active, HOME
from construire_montage import camera, get_design

HERE=Path(__file__).resolve().parent
NATIVE="AURA-009_Table_r03"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def save_project():
    app=core.Application.get()
    rig=active()
    original=next(doc for doc in app.documents if doc.dataFile and doc.dataFile.versionNumber==1
                  and doc.name.startswith("AURA-01 — V3 articulée — Montage r02"))
    rig.position(HOME)
    if rig.root.motionLinks.count==0:
        rig.link_fingers()
    assert rig.root.motionLinks.count==16
    camera(app)
    doc=rig.doc
    if doc.isSaved:
        assert doc.name.startswith(TITLE) and doc.dataFile.id!=original.dataFile.id
        if doc.isModified:
            assert doc.save("AURA-009 table r03 : vérifications et pose HOME.")
    else:
        assert doc.saveAs(TITLE,original.dataFile.parentFolder,
                          "Refonte éditable AURA-009, table r03. Prototype à qualifier.","AURA-009 r03")
    df=doc.dataFile
    print("Document",doc.name,doc.isSaved,doc.isModified,df.versionNumber,df.id)
    print("R02",original.name,original.dataFile.versionNumber,original.isModified)


def export_prints(rig,app):
    target=HERE/"STL"
    target.mkdir(exist_ok=True)
    definitions={}
    for code, (occ,name,_) in rig.prints.items():
        group=rig.print_groups[code]
        definitions.setdefault(group,[]).append((code,occ.component.bRepBodies.itemByName(name)))
    work=app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
    work.name="AURA-009 r03 — export de fabrication"
    try:
        design=get_design(work)
        design.designType=fusion.DesignTypes.DirectDesignType
        ex=design.exportManager
        f=rig.forms
        rows=[]
        variants=[(group,entries[0][0],entries[0][1],len(entries)) for group,entries in definitions.items()]
        variants.extend((group,group,shape,0) for group,shape in (
            ("Coupon_01_Axes_horizontaux",f.horizontal_coupon()),
            ("Coupon_02_Pilotes_bagues_ecrous",f.fixing_coupon()),
            ("Coupon_03_Encombrement_MG996R",f.motor_coupon()),
        ))
        for group,code,source,quantity in variants:
            shape=f.manager.copy(source)
            prototype=f.place(shape,frame(**ORIENTATIONS.get(code,{})))
            box=prototype.boundingBox
            lo,hi=box.minPoint,box.maxPoint
            f.place(prototype,frame((-(lo.x+hi.x)*5,-(lo.y+hi.y)*5,-10*lo.z)))
            b=design.rootComponent.bRepBodies.add(prototype)
            b.name=group
            output=target/(group+".stl")
            opt=ex.createSTLExportOptions(b,str(output))
            opt.isBinaryFormat=True
            opt.meshRefinement=fusion.MeshRefinementSettings.MeshRefinementHigh
            assert ex.execute(opt),group
            rows.append({"reference":group,"fichier":output.name,"quantite_robot":quantity,
                         "dimensions_mm":[round((a-b)*10,4) for a,b in zip(hi.asArray(),lo.asArray())],
                         "volume_cm3":round(source.volume,6),
                         "reperes":[c for c,_ in definitions[group]] if quantity else [],
                         "orientation_deg":ORIENTATIONS.get(code,{}),"sha256":digest(output)})
        return rows
    finally:
        work.close(False)
        rig.doc.activate()


def tessellate(rig, path):
    parts=[]
    for key,occ in rig.occ.items():
        tx=occ.transform2
        for body in occ.component.bRepBodies:
            if body.name.startswith("Repère de liaison"):
                continue
            calc=body.meshManager.createMeshCalculator()
            calc.surfaceTolerance=.007
            mesh=calc.calculate()
            points=[]
            for p in mesh.nodeCoordinates:
                xyz=p.copy()
                xyz.transformBy(tx)
                points.append(tuple(round(t/100,7) for t in xyz.asArray()))
            indices=list(mesh.nodeIndices)
            faces=[indices[i:i+3] for i in range(0,len(indices),3)]
            if not faces:
                raise RuntimeError(f"Pas de facettes pour {body.name}.")
            try:
                finish=body.appearance.name
            except AttributeError:
                finish=""
            parts.append({"code":key,"parent":rig.stage.get(key,""),
                          "nom":body.name,"finish":finish,"vertices":points,"faces":faces})
    with gzip.open(path,"wt",encoding="utf8") as fp:
        json.dump(parts,fp,ensure_ascii=False,separators=(",",":"))
    return len(parts)


def export_all():
    app=core.Application.get()
    rig=active()
    rig.position(HOME)
    ex=rig.design.exportManager
    f3d=HERE/(NATIVE+".f3d")
    assert ex.execute(ex.createFusionArchiveExportOptions(str(f3d)))
    report={"fusion":app.version,"occurrences":len(rig.occ),"liaisons":rig.root.asBuiltJoints.count,
            "pivots":len(rig.joints),"couplages":rig.root.motionLinks.count,
            "esquisses":sum(o.component.sketches.count for o in rig.root.occurrences),
            "nombre_parametres":rig.design.userParameters.count,
            "f3d_sha256":digest(f3d),
            "pieces":export_prints(rig,app)}
    report["maillages_rendu"]=tessellate(rig,HERE/"Source_Rendu_r03.json.gz")
    (HERE/"Inventaire_CAO_r03.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("Archives",report["occurrences"],report["liaisons"],report["couplages"],
          "références",len(report["pieces"]),"maillages",report["maillages_rendu"],
          "SHA-256",report["f3d_sha256"])


def export_step():
    rig=active()
    rig.position(HOME)
    app=core.Application.get()
    out=HERE/(NATIVE+".step")
    ex=rig.design.exportManager
    ok=ex.execute(ex.createSTEPExportOptions(str(out),rig.root))
    mode="racine native"
    if not ok or out.stat().st_size<1024:
        mode="assemblage distinct en solides, à HOME, sans repères de liaisons"
        scratch=app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
        scratch.name="AURA-009 r03 — traduction STEP"
        try:
            design=get_design(scratch)
            design.designType=fusion.DesignTypes.DirectDesignType
            manager=rig.forms.manager
            for key,occ in rig.occ.items():
                comp=design.rootComponent.occurrences.addNewComponent(occ.transform2).component
                comp.name=occ.component.name
                for native in occ.component.bRepBodies:
                    if native.name!="Repère de liaison":
                        body=comp.bRepBodies.add(manager.copy(native))
                        body.name=native.name
            replica=design.exportManager
            assert replica.execute(replica.createSTEPExportOptions(str(out),design.rootComponent))
        finally:
            scratch.close(False)
            rig.doc.activate()
    text=out.read_text(encoding="ascii")
    assert "MANIFOLD_SOLID_BREP" in text and text.strip().endswith("END-ISO-10303-21;")
    p=HERE/"Inventaire_CAO_r03.json"
    report=json.loads(p.read_text(encoding="utf8"))
    report["step_sha256"]=digest(out)
    report["step_mode"]=mode
    report["step_solides"]=text.count("MANIFOLD_SOLID_BREP(")
    p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("STEP",mode,out.stat().st_size,report["step_solides"],report["step_sha256"])


def reopen():
    app=core.Application.get()
    saved=active()
    im=app.importManager
    temp=im.importToNewDocument(im.createFusionArchiveImportOptions(str(HERE/(NATIVE+".f3d"))))
    assert temp
    try:
        r=ExistingTable(temp)
        assert len(r.occ)==len(saved.occ)
        assert r.root.motionLinks.count==16
        param=r.design.userParameters.itemByName("EpaisseurPlatine")
        part=r.occ["01_Platine"].component.bRepBodies.itemByName("FDM · 01_Platine")
        before=part.boundingBox.maxPoint.z-part.boundingBox.minPoint.z
        param.expression="6.5 mm"
        assert r.design.computeAll()
        after=part.boundingBox.maxPoint.z-part.boundingBox.minPoint.z
        assert abs(after-before-.05)<.001
        param.expression="6 mm"
        assert r.design.computeAll()
        r.position((0,5,7,12,.3))
        print("F3D réimporté",len(r.occ),"occurrences",r.root.asBuiltJoints.count,
              "liaisons","paramètre platine",before*10,after*10,"mm","pose pilotée",r.angle("04_Segment_1"))
    finally:
        temp.close(False)
        saved.doc.activate()
