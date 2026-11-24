"""Outillage Fusion partagé par les deux bancs."""

import math
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile

import adsk
import adsk.core as core
import adsk.fusion as fusion


ROOT=Path(__file__).resolve().parents[1]


def digest(file):
    return sha256(file.read_bytes()).hexdigest()


class Bench:
    def __init__(self,app,base,get_design,label):
        self.app=app
        self.base=base
        self.get_design=get_design
        self.doc=app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
        self.design=get_design(self.doc)
        self.design.designType=fusion.DesignTypes.ParametricDesignType
        self.root=self.design.rootComponent
        self.root.attributes.add("AURA-01","Sous_ensemble",label)
        self.g=base.Solids(self.design)
        self.parts={}
        self.prints={}
        self.joints={}

    def part(self,key,label,shape,finish="metal",origin=(0,0,0),axis=None,print_face=None,typed=None,placement=None):
        occ=self.root.occurrences.addNewComponent(placement or self.base.frame(origin))
        comp=occ.component
        comp.name=label
        if typed:
            comp.attributes.add("AURA-01","Référence",typed)
        feature=comp.features.baseFeatures.add()
        feature.name="Définition des solides"
        feature.startEdit()
        body=comp.bRepBodies.add(shape,feature)
        body.name=key
        body.appearance=self.g.appearances[finish]
        if axis:
            mark=comp.bRepBodies.add(self.g.pivot(axis,.28,1.6),feature)
            mark.name="Repère local"
        feature.finishEdit()
        if print_face is not None:
            native=next(b for b in comp.bRepBodies if b.name==key)
            if not native.isSolid or native.lumps.count!=1:
                raise RuntimeError(f"Le solide imprimable {key} comporte {native.lumps.count} volumes.")
            self.prints[key]=(native,print_face)
        if axis:
            next(b for b in occ.bRepBodies if b.name=="Repère local").isLightBulbOn=False
        self.parts[key]=occ
        return occ

    def rigid(self,child,parent):
        inp=self.root.asBuiltJoints.createInput(self.parts[child],self.parts[parent],None)
        if not inp or not inp.setAsRigidJointMotion():
            raise RuntimeError(f"Encastrement refusé {child}.")
        j=self.root.asBuiltJoints.add(inp)
        j.name=child+" sur "+parent
        j.isLightBulbOn=False
        return j

    def pivot(self,key,rotor,stator,origin_key=None):
        occ=self.parts[origin_key or rotor]
        mark=next(b for b in occ.bRepBodies if b.name=="Repère local")
        edge=next(e for e in mark.edges if core.Circle3D.cast(e.geometry))
        origin=fusion.JointGeometry.createByCurve(edge,fusion.JointKeyPointTypes.CenterKeyPoint)
        inp=self.root.asBuiltJoints.createInput(self.parts[rotor],self.parts[stator],origin)
        if not inp or not inp.setAsRevoluteJointMotion(fusion.JointDirections.ZAxisJointDirection):
            raise RuntimeError(f"Pivot refusé {key}.")
        joint=self.root.asBuiltJoints.add(inp)
        joint.name=key
        joint.isLightBulbOn=False
        self.joints[key]=joint
        return joint

    def ring(self,x,z,y0,y1,ext,inner):
        return self.g.cut(self.g.cyl((x,y0,z),(x,y1,z),ext),
                          self.g.cyl((x,y0-.5,z),(x,y1+.5,z),inner))

    def measure(self,omit=(),keys=None):
        inputs=core.ObjectCollection.create()
        for key,occ in self.parts.items():
            if key not in omit and (keys is None or key in keys):
                inputs.add(next(b for b in occ.bRepBodies if b.name==key))
        options=self.design.createInterferenceInput(inputs)
        options.areCoincidentFacesIncluded=False
        report=self.design.analyzeInterference(options)
        result=[]
        for hit in report:
            if hit.interferenceBody.volume*1000>.002:
                result.append({"a":hit.entityOne.name,"b":hit.entityTwo.name,"mm3":round(hit.interferenceBody.volume*1000,4)})
        return result

    def camera(self,target,eye,width,image):
        self.doc.activate()
        viewport=self.app.activeViewport
        cam=viewport.camera
        cam.cameraType=core.CameraTypes.OrthographicCameraType
        cam.isSmoothTransition=False
        cam.target=self.base.point(target)
        cam.eye=self.base.point(eye)
        cam.upVector=self.base.vector((0,0,1))
        cam.viewExtents=width/10
        viewport.camera=cam
        viewport.refresh()
        adsk.doEvents()
        if not viewport.saveAsImageFile(str(image),1400,900):
            raise RuntimeError(f"Impossible de capturer {image.name}.")

    def export_prints(self,out):
        context=self.app.documents.add(core.DocumentTypes.FusionDesignDocumentType)
        files=[]
        try:
            design=self.get_design(context)
            design.designType=fusion.DesignTypes.DirectDesignType
            for key,(native,roll) in self.prints.items():
                temp=self.g.manager.copy(native)
                if roll and not self.g.manager.transform(temp,self.base.frame(roll=roll)):
                    raise RuntimeError(f"Orientation impossible pour {key}.")
                b=temp.boundingBox
                x,y,z=b.minPoint.asArray()
                x1,y1,z1=b.maxPoint.asArray()
                self.g.manager.transform(temp,self.base.frame((-(x+x1)*5,-(y+y1)*5,-z*10)))
                comp=design.rootComponent.occurrences.addNewComponent(core.Matrix3D.create()).component
                comp.name=key
                n=comp.bRepBodies.add(temp)
                n.name=key
                entry={"reference":key,"dimensions_mm":[round((x1-x)*10,3),round((y1-y)*10,3),round((z1-z)*10,3)],
                       "volume_cm3":round(n.volume,3)}
                for extension in ("3mf","step"):
                    file=out/(key+"."+extension)
                    export=design.exportManager
                    opt=export.createC3MFExportOptions(n,str(file)) if extension=="3mf" else export.createSTEPExportOptions(str(file),comp)
                    if extension=="3mf":
                        opt.meshRefinement=fusion.MeshRefinementSettings.MeshRefinementHigh
                    if not export.execute(opt) or not file.is_file():
                        raise RuntimeError(f"Export {file.name} refusé.")
                    if extension=="3mf":
                        with ZipFile(file) as zf:
                            assert zf.testzip() is None
                    entry[extension]={"fichier":file.name,"sha256":digest(file)}
                files.append(entry)
        finally:
            context.close(False)
        return files


def apply_pose(motion,angle,zero,sign=1):
    expected=zero+math.radians(angle*sign)
    motion.rotationValue=expected
    if abs(math.remainder(motion.rotationValue-expected,math.tau))>math.radians(.10):
        raise RuntimeError(f"Le solveur n'a pas atteint {angle}°.")
