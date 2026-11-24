"""Faisceau AURA-009 r03. Les guides se referment par des pivots natifs dans Fusion."""

import json
import math

import adsk.core as core
import adsk.fusion as fusion

from geometrie import frame, point, vector


AXES={
    "J1":("02_Socle","03_Tourelle","01_Platine",(0,0,1),49.,-1,1.65),
    "J2":("03_Tourelle","04_Segment_1","01_Platine",(0,1,0),28.,1,1.50),
    "J3":("04_Segment_1","05_Segment_2","01_Platine",(0,1,0),28.,1,1.35),
    "J7":("06_Segment_3","07_Paume","07_Paume",(1,0,0),44.,-1,1.15),
}
BEND=5.
LAYER=5.8
OLD=("CAB_J1","CAB_J2","CAB_J3","CAB_J7","PLUG_CC","PLUG_J2","PLUG_J3","PLUG_J7","PLUG_T1")
MARKER="Repère de liaison · Faisceau"


def plus(a,b,scale=1.):
    return tuple(x+scale*y for x,y in zip(a,b))


def direction(a,b):
    d=plus(b,a,-1)
    return tuple(x/math.hypot(*d) for x in d)


def transform(xyz,matrix):
    p=point(xyz)
    p.transformBy(matrix)
    return tuple(x*10 for x in p.asArray())


def local(xyz,occ):
    tm=occ.transform2.copy()
    assert tm.invert()
    return transform(xyz,tm)


def unit_cross(a,b):
    v=vector(a).crossProduct(vector(b))
    assert v.normalize()
    return tuple(v.asArray())


def vector_transformed(uvw,occ):
    v=vector(uvw)
    v.transformBy(occ.transform2)
    return tuple(v.asArray())


def frame_axes(xyz,u,n):
    m=core.Matrix3D.create()
    assert m.setWithCoordinateSystem(point(xyz),vector(u),vector(unit_cross(n,u)),vector(n))
    return m


def minimum_radius(points):
    radii=[]
    for a,b,c in zip(points,points[1:],points[2:]):
        ab,bc=plus(b,a,-1),plus(c,b,-1)
        area=vector(ab).crossProduct(vector(bc)).length
        if area>1e-6:
            radii.append(math.hypot(*ab)*math.hypot(*bc)*math.dist(a,c)/(2*area))
    return min(radii,default=1000.0)


def rounding(points,rad,max_trim=None):
    """Tangentes et arcs circulaires aux coudes d'un chemin de pose."""
    result=[points[0]]
    for a,b,c in zip(points,points[1:],points[2:]):
        u,v=direction(a,b),direction(b,c)
        cos=max(-1.,min(1.,sum(x*y for x,y in zip(u,v))))
        if cos>.9998:
            continue
        alpha=math.acos(cos)
        trim=min(rad*math.tan(alpha/2), .47*math.dist(a,b), .47*math.dist(b,c))
        if max_trim is not None:
            trim=min(trim,max_trim)
        radius=trim/math.tan(alpha/2)
        q=plus(b,u,-trim)
        w=direction((0.,0.,0.),plus(v,u,-cos))
        samples=max(3,math.ceil(alpha/.25))
        for i in range(samples+1):
            angle=alpha*i/samples
            result.append(plus(plus(q,u,radius*math.sin(angle)),w,radius*(1-math.cos(angle))))
    result.append(points[-1])
    return result


def hinge_cable(length):
    # Le câble suit la normale à chaque interface et ne se décentre pas à la rotation.
    curve=[(0.,0.,0.)]
    for i in range(7):
        t=math.pi*i/12
        curve.append((BEND*(1-math.cos(t)),0.,LAYER-BEND+BEND*math.sin(t)))
    return curve+[(length-x,y,z) for x,y,z in reversed(curve)]


class Harness:
    def __init__(self,rig):
        self.rig=rig
        self.f=rig.forms
        if not hasattr(self.f,"appearances"):
            names={"dark":"AURA - Graphite profond","ice":"AURA - Gris perle",
                   "white":"AURA - Blanc céramique","rubber":"AURA - Anthracite",
                   "metal":"AURA - Métal satiné","accent":"AURA - Bleu pétrole"}
            self.f.appearances={k:rig.design.appearances.itemByName(name) for k,name in names.items()}
        self.seams=[]
        self.mounts=[]
        self.joints={}
        self.spans={}
        self.tails=[]
        self.wires={}
        self.clearances={}
        self.courses={}
        self.clips=[]

    def tube(self,radius,route):
        f=self.f
        body=f.cyl(route[0],route[1],radius)
        for a,b in zip(route[1:],route[2:]):
            f.union(body,f.manager.createSphere(point(a),radius/10),f.cyl(a,b,radius))
        return body

    def register(self,code,at,parts,*,label,print_group=None,parent=None,orientation=0):
        rig=self.rig
        occ=rig.add(code,label,at,parts,print_orientation=orientation if print_group else None)
        comp=occ.component
        comp.partNumber="AURA009-R03-"+code
        comp.attributes.add("AURA-01","Repere",code)
        if print_group:
            rig.print_groups[code]=print_group
            comp.attributes.add("AURA-01","Impression",print_group)
        if parent:
            rig.stage[code]=parent
            comp.attributes.add("AURA-01","Parent",parent)
        assert comp.bRepBodies.count==len(parts),(code,comp.bRepBodies.count,len(parts))
        for b,(_,finish,name) in zip(comp.bRepBodies,parts):
            b.name=name
            b.appearance=self.f.appearances[finish]
            if name.startswith(MARKER):
                b.isLightBulbOn=False
        return occ

    def fixed(self,code,parent):
        rig=self.rig
        rig.fixed(parent,code)
        rig.stage[code]=parent
        rig.occ[code].component.attributes.add("AURA-01","Parent",parent)

    def joint(self,name,one,two,ref,index):
        rig=self.rig
        body=rig.occ[ref].bRepBodies.itemByName(f"{MARKER} {index}")
        edge=next(e for e in body.edges if core.Circle3D.cast(e.geometry))
        geometry=fusion.JointGeometry.createByCurve(edge,fusion.JointKeyPointTypes.CenterKeyPoint)
        spec=rig.root.asBuiltJoints.createInput(rig.occ[one],rig.occ[two],geometry)
        assert spec.setAsRevoluteJointMotion(fusion.JointDirections.ZAxisJointDirection)
        joint=rig.root.asBuiltJoints.add(spec)
        joint.name=name
        joint.isLightBulbOn=False
        return joint

    def add_seam(self,name,c1,c2,world):
        r=self.rig
        self.seams.append({"nom":name,"a":c1,"b":c2,
                           "point_a":local(world,r.occ[c1]),"point_b":local(world,r.occ[c2])})

    def guides(self,axis,a,b,n):
        parent,child,ref,_,total,fold,radius=AXES[axis]
        length=total/2
        u=direction(a,b)
        h=math.sqrt(length**2-(math.dist(a,b)/2)**2)
        c=plus(a,plus(b,a,-1),.5)
        c=plus(c,unit_cross(n,u),fold*h)
        codes=(f"G_{axis}_A",f"G_{axis}_B")
        for i,(start,end) in enumerate(((a,c),(c,b))):
            f=self.f
            name=codes[i]
            at=frame_axes(start,direction(start,end),tuple((-1)**i*x for x in n))
            bowl=f.box(0,length,-4.1,4.1,4.45,7.25)
            f.union(bowl,*(f.hole_z(x,0,0.025,6.45,4.18) for x in (0,length)))
            curve=hinge_cable(length)
            f.cut(bowl,self.tube(radius+.36,curve),
                  f.box(4.9,length-4.9,-radius-.40,radius+.40,LAYER-.05,7.5),
                  *(f.hole_z(x,0,-.15,1.45,2.28) for x in (0,length)),
                  *(f.hole_z(x,0,1.00,1.57,2.53) for x in (0,length)))
            key=f"Guide_{length:g}mm_{axis}"
            wire=self.tube(radius,curve)
            f.cut(wire,f.box(-5,length+5,-5,5,-5,0.0))
            parts=[(bowl,"accent","FDM · "+name),(wire,"rubber",f"[{name}] conducteur guidé")]
            parts.extend((f.hole_z(x,0,0,.14,.55),"metal",f"{MARKER} {j}")
                         for j,x in enumerate((0,length)))
            self.register(name,at,parts,label=f"{axis} · guide articulé {'amont' if i==0 else 'aval'}",
                          print_group=key,parent=(parent,child)[i])
        self.joint(f"Faisceau {axis} · Amont",codes[0],f"S_{axis}_A",codes[0],0)
        fold_joint=self.joint(f"Faisceau {axis} · Repli",codes[1],codes[0],codes[1],0)
        motion=fold_joint.jointMotion
        origin=motion.rotationValue
        limits=motion.rotationLimits
        limits.minimumValue=origin-math.radians(64)
        limits.maximumValue=origin+math.radians(64)
        limits.isMinimumValueEnabled=True
        limits.isMaximumValueEnabled=True
        self.joint(f"Faisceau {axis} · Aval",codes[1],f"S_{axis}_B",codes[1],1)
        for i,(center,guide) in enumerate(zip((a,c,b),(codes[0],codes[0],codes[1])),1):
            key=f"BAG_{axis}_{i}"
            at=frame_axes(center,u,n)
            collar=f.hole_z(0,0,-1.07,1.07,2.19)
            f.union(collar,f.hole_z(0,0,-1.40,-1.01,2.43),f.hole_z(0,0,1.01,1.40,2.43))
            f.cut(collar,f.hole_z(0,0,-1.45,1.45,radius+.25))
            self.register(key,at,[(collar,"metal",f"[{key}] Axe creux Ø4,38")],
                          label=f"{axis} · axe creux de guide {i}",parent=guide)
            self.fixed(key,guide)
        self.add_seam(axis+" amont",f"S_{axis}_A",codes[0],a)
        self.add_seam(axis+" repli",codes[0],codes[1],c)
        self.add_seam(axis+" aval",codes[1],f"S_{axis}_B",b)

    def layout(self):
        r=self.rig
        guard=lambda axis,xyz: transform(xyz,r.occ[f"P{int(axis[1])+9:02}_Garde_{axis}"].transform2)
        rotor=lambda axis,xyz: transform(xyz,r.occ[f"ROT_{axis}"].transform2)
        palm=lambda xyz: transform(xyz,r.occ["07_Paume"].transform2)
        return {
            "J1":(
                ((24.,43.,25.),(-9.,36.,25.)),
                (((29.,38.,6.035),(29.,38.,12.),(24.,43.,21.)),
                 ((-9.,20.,43.075),(-9.,20.,46.3),(-9.,37.,46.3),(-9.,37.,31.))),
            ),
            "J2":(
                (guard("J2",(-13.7,46.,0.)),rotor("J2",(9.,46.,-3.8))),
                ((guard("J2",(-13.7,30.54,0.)),guard("J2",(-13.7,41.8,0.))),
                 tuple(rotor("J2",p) for p in ((17.5,36.75,0),(17.5,54,0),(9,54,-3.8),(9,50,-3.8)))),
            ),
            "J3":(
                (guard("J3",(-13.7,46.,0.)),rotor("J3",(8.,46.,6.0))),
                ((guard("J3",(-13.7,30.54,0.)),guard("J3",(-13.7,41.8,0.))),
                 tuple(rotor("J3",p) for p in ((17.5,36.75,0),(17.5,54,0),(8,54,6),(8,50,6)))),
            ),
            "J7":(
                (palm((-2.,23.,-15.)),palm((-2.,24.,12.))),
                (tuple(palm(p) for p in ((-6.3,13.83,-9.30),(-6.3,17.,-11.25),(-6.0,23.,-15.))),
                 tuple(palm(p) for p in ((15.,18.,4.555),(15.,18.,9.5),(4.,24.,12.),(2.,24.,12.)))),
            ),
        }

    def anchor(self,axis,index,center,n,leg,parent,radius):
        f=self.f
        code=f"S_{axis}_{'AB'[index]}"
        n=tuple((-1)**(index+1)*v for v in n)
        ref=tuple(float(i==min(range(3),key=lambda j:abs(n[j]))) for i in range(3))
        u=unit_cross(ref,n)
        at=frame_axes(center,u,n)
        inv=at.copy()
        assert inv.invert()
        points=tuple(transform(p,inv) for p in leg)
        socket=f.hole_z(0,0,.035,5.25,4.18)
        if math.dist(points[-1],(0,0,4.3))>.20:
            points+=((0,0,4.3),)
        stalk=self.tube(2.9,points)
        f.union(socket,stalk)
        f.cut(socket,f.hole_z(0,0,-.1,7.20,2.28),f.hole_z(0,0,1.0,1.58,2.53))
        wire_code={
            "J1":("FIL_BASE","FIL_TOUR"),"J2":("FIL_TOUR","FIL_BRAS"),
            "J3":("FIL_BRAS","FIL_AVANT"),"J7":("FIL_AVANT","FIL_MAIN"),
        }[axis][index]
        if wire_code in self.clearances:
            relief=f.manager.copy(self.clearances[wire_code])
            assert f.manager.transform(relief,inv)
            ok=f.manager.booleanOperation(socket,relief,fusion.BooleanTypes.DifferenceBooleanType)
            assert ok and socket.lumps.count==1,(code,socket.lumps.count)
        if code=="S_J7_B":
            self.contour(socket,"07_Paume",inv)
        self.register(code,at,[(socket,"ice","FDM · "+code)],label=f"{axis} · attache de faisceau {'amont' if index==0 else 'aval'}",
                      print_group=f"Attache_{axis}_{'AB'[index]}",parent=parent)
        self.fixed(code,parent)
        self.mounts.append({"repere":code,"parent":parent,"pied_mm":local(leg[0],self.rig.occ[parent])})

    def install(self,poses=None,fixed_cables=True):
        r=self.rig
        layout=self.layout()
        for axis,(ends,_) in layout.items():
            _,_,ref,axis_vector,total,_,radius=AXES[axis]
            self.spans[axis]=(*ends,vector_transformed(axis_vector,r.occ[ref]),total/2,radius)
        if fixed_cables:
            self.prepare_tails()
        for axis,(ends,legs) in layout.items():
            parent,child,_,_,_,_,radius=AXES[axis]
            n=self.spans[axis][2]
            for i,(a,leg,key) in enumerate(zip(ends,legs,(parent,child))):
                self.anchor(axis,i,a,n,leg,key,radius)
            self.guides(axis,*ends,n)
        if fixed_cables:
            self.install_tails()
            self.service_ports()
            self.install_clips()
        self.save_manifest()

    def save_manifest(self):
        r=self.rig
        motions={j.name:j.jointMotion.rotationValue for j in r.root.asBuiltJoints if j.name.startswith("Faisceau ")}
        data={"interfaces":self.seams,"attaches":self.mounts,"traverses":self.tails,"colliers":self.clips,
              "pivots_neutre_rad":motions,"rayon_guide_mm":BEND,"decalage_guide_mm":LAYER}
        r.root.attributes.add("AURA-01","Faisceau",json.dumps(data,ensure_ascii=False))

    def remove_previous(self):
        r=self.rig
        for j in list(r.root.asBuiltJoints):
            if j.name.removeprefix("Fixation · ") in OLD:
                assert j.deleteMe()
        for key in OLD:
            if key in r.occ:
                assert r.occ[key].deleteMe()
                del r.occ[key]
                r.stage.pop(key,None)

    def prepare_tails(self):
        r=self.rig
        a1,b1,n1,_,_=self.spans["J1"]
        a2,b2,n2,_,_=self.spans["J2"]
        a3,b3,n3,_,_=self.spans["J3"]
        a7,b7,n7,_,_=self.spans["J7"]
        palm=lambda xyz:transform(xyz,r.occ["07_Paume"].transform2)
        motor=lambda name,xyz:transform(xyz,r.occ[name].transform2)
        p2=(-24.,-65.,72.15)
        p3=motor("SERVO_J3",(10.02,-9.,-11.8))
        p7=motor("SERVO_J7",(9.,6.12,-20.))
        pt=motor("SERVO_T1",(13.,6.12,-5.8))
        p3a=motor("SERVO_J3",(15.6,-9.,-11.8))
        p7a=motor("SERVO_J7",(9.,19.0,-20.))
        pta=motor("SERVO_T1",(13.,16.2,-5.8))
        arms=(
            ("FIL_BASE", "02_Socle", 1.65,
             ((12.,59.47,12.4),(12.,51.0,12.4),plus(a1,n1,-10.8),a1),
             (("TTL",(12.,59.47,12.4)),("S_J1_A",a1)),()),
            ("FIL_TOUR", "03_Tourelle", 1.50,
             (b1,plus(b1,n1,12.),(-13.7,41.,60.),plus(a2,n2,-10.7),a2),
             (("S_J1_B",b1),("S_J2_A",a2)),
             ((1.08,(-14.,40.,62.),
               ((-17.8,36.,55.8),(-17.8,17.,56.),(-17.8,-22.,56.),(-22.,-52.,58.),
                (-24.,-65.,64.),p2),"SERVO_J2"),)),
            ("FIL_BRAS", "04_Segment_1", 1.35,
             (b2,plus(b2,n2,12.8),(a3[0]-8.0,58.8,a3[2]-6.),
              (a3[0]-8.0,38.4,a3[2]-6.),plus(a3,n3,-10.0),a3),
             (("S_J2_B",b2),("S_J3_A",a3)),
             ((.95,(a3[0]-5.,51.5,a3[2]-6.),
               ((6.5,47.,114.),(9.,23.5,118.),(9.,-17.5,118.),(-3.,-32.,123.),(-2.8,-46.85,122.),
                p3a,p3),"SERVO_J3"),)),
            ("FIL_AVANT", "05_Segment_2", 1.15,
             (b3,plus(b3,n3,12.0),(b3[0]+11.,58.,b3[2]+4.7),
              (b3[0]+21.,40.,b3[2]+9.0),(64.,17.,136.),
              plus(a7,n7,-13.),a7),
             (("S_J3_B",b3),("S_J7_A",a7)),
             ((.9,(64.,17.,136.),(p7a,p7),"SERVO_J7"),)),
            ("FIL_MAIN", "07_Paume", 1.15,
             (b7,plus(b7,n7,10.),
              *(palm(x) for x in ((18.,28.55,12.),(31.,28.8,-9.),(30.,23.0,-26.85))),
              pta,pt),
             (("S_J7_B",b7),("SERVO_T1",pt)),()),
        )
        for code,parent,radius,controls,ends,branches in arms:
            curve=rounding(controls,7.2)
            self.courses[code]=(radius,curve)
            cable=self.tube(radius,curve)
            clearance=self.tube(radius+.36,curve)
            for r_branch,junction,points,device in branches:
                meeting=min(curve,key=lambda xyz:math.dist(xyz,junction))
                spur=rounding((meeting,*points),7.2)
                self.courses[device]=(r_branch,spur)
                self.f.union(cable,self.tube(r_branch,spur))
                self.f.union(clearance,self.tube(r_branch+.36,spur))
                self.tails.append({"cable":code,"branche":device,
                                   "rayon_min_mm":round(minimum_radius(spur),3),
                                   "longueur_mm":round(sum(math.dist(a,b) for a,b in zip(spur,spur[1:])),3)})
            self.wires[code]=(parent,cable,ends,branches)
            self.clearances[code]=clearance
            self.tails.append({"cable":code,"rayon_min_mm":round(minimum_radius(curve),3),
                              "longueur_mm":round(sum(math.dist(a,b) for a,b in zip(curve,curve[1:])),3)})

    def install_tails(self):
        for code,(parent,cable,ends,branches) in self.wires.items():
            label={"FIL_BASE":"Alimentation et commande · embase",
                   "FIL_TOUR":"Faisceau tourelle · dérivation J2",
                   "FIL_BRAS":"Faisceau bras supérieur · dérivation DYNAMIXEL",
                   "FIL_AVANT":"Faisceau avant-bras · dérivation J7",
                   "FIL_MAIN":"Faisceau paume · terminaison T1"}[code]
            self.register(code,frame(),[(cable,"rubber",f"[{code}] {label}")],
                          label=label,parent=parent)
            self.fixed(code,parent)
            for other,terminal in ends:
                self.add_seam(f"{code} vers {other}",code,other,terminal)
            for _,_,points,device in branches:
                self.add_seam(f"{code} vers {device}",code,device,points[-1])

    def service_ports(self):
        """Deux fenêtres de passage, conservées dans les STL des supports concernés."""
        r,f=self.rig,self.f
        data=[]
        for code,tool in (
            ("06_Segment_3", f.manager.copy(self.clearances["FIL_AVANT"])),
            ("P08_Porte_J3", f.place(f.box(9.98,16.2,-12.75,-5.25,-14.45,-9.15),
                                  r.occ["SERVO_J3"].transform2)),
        ):
            occ=r.occ[code]
            comp=occ.component
            tm=occ.transform2.copy()
            assert tm.invert() and f.manager.transform(tool,tm)
            feature=comp.features.baseFeatures.item(0)
            body=next(b for b in comp.bRepBodies if b.name=="FDM · "+code)
            revised=f.manager.copy(body)
            initial=revised.volume
            assert f.manager.booleanOperation(revised,tool,fusion.BooleanTypes.DifferenceBooleanType)
            assert revised.lumps.count==1
            delta=(initial-revised.volume)*1000
            assert 1.<delta<200.,(code,delta)
            assert feature.startEdit()
            try:
                source=next(b for b in feature.bodies if b.name=="FDM · "+code)
                assert feature.updateBody(source,revised)
            finally:
                assert feature.finishEdit()
            data.append({"piece":code,"matiere_enlevee_mm3":round(delta,3)})
        self.tails.extend(data)

    def contour(self,shape,host,inv):
        f=self.f
        substrate=next(b for b in self.rig.occ[host].bRepBodies if b.name.startswith("FDM · "))
        tool=f.manager.copy(substrate)
        assert f.manager.transform(tool,inv)
        assert f.manager.booleanOperation(shape,tool,fusion.BooleanTypes.DifferenceBooleanType)
        assert shape.lumps.count==1

    def locate(self,course,near):
        _,curve=self.courses[course]
        options=[]
        for a,b in zip(curve,curve[1:]):
            d=plus(b,a,-1)
            rel=plus(near,a,-1)
            t=min(1.,max(0.,sum(x*y for x,y in zip(d,rel))/sum(x*x for x in d)))
            fit=plus(a,d,t)
            options.append((math.dist(fit,near),fit,direction(a,b)))
        return min(options)[1:]

    def install_clips(self):
        palm=self.rig.occ["07_Paume"]
        orders=(
            ("SERVO_J2",(-17.8,11.,56.),"03_Tourelle"),
            ("SERVO_J2",(-17.8,-11.,56.),"03_Tourelle"),
            ("SERVO_J3",(9.,11.,118.),"04_Segment_1"),
            ("SERVO_J3",(9.,-11.,118.),"04_Segment_1"),
            ("FIL_AVANT",(77.,20.,122.),"06_Segment_3"),
            ("FIL_MAIN",transform((28.,29.,2.),palm.transform2),"07_Paume"),
        )
        f=self.f
        measure=core.Application.get().measureManager
        for rank,(course,near,host) in enumerate(orders,1):
            center,axis=self.locate(course,near)
            body=next(b for b in self.rig.occ[host].bRepBodies if b.name.startswith("FDM · "))
            distance=measure.measureMinimumDistance(point(center),body)
            target=max((distance.positionOne,distance.positionTwo),key=lambda x:x.distanceTo(point(center)))
            foot=tuple(v*10 for v in target.asArray())
            assert math.dist(center,foot)<12.5,(course,host,center,foot)
            d=plus(foot,center,-1)
            x=direction((0,0,0),plus(d,axis,-sum(v*w for v,w in zip(d,axis))))
            at=frame_axes(center,x,axis)
            inv=at.copy()
            assert inv.invert()
            pad=transform(plus(foot,direction(center,foot),.85),inv)
            radius=self.courses[course][0]
            clip=f.hole_z(0,0,-1.75,1.75,radius+1.22)
            f.union(clip,f.cyl((0,0,0),pad,2.15),f.manager.createSphere(point(pad),.235))
            f.cut(clip,f.hole_z(0,0,-6,6,radius+.24),
                  f.box(-radius-2.,-.4,-radius*.66,radius*.66,-4.,4.))
            self.contour(clip,host,inv)
            code=f"ATT_F_{rank:02}"
            self.register(code,at,[(clip,"ice","FDM · "+code)],
                          label="Collier de maintien · "+str(rank),
                          print_group=f"Collier_faisceau_{rank:02}",parent=host)
            self.fixed(code,host)
            self.clips.append({"collier":code,"host":host,"circuit":course,
                               "distance_mm":round(math.dist(center,foot),3)})
