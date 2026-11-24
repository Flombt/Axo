"""Vues fixes de la tessellation Fusion r03, rendu Blender hors session interactive."""

import argparse
import gzip
import json
from pathlib import Path
import sys

import bmesh
import bpy
from mathutils import Vector


HERE=Path(__file__).resolve().parent
PALETTE={
    "Graphite":(.032,.047,.063, .26,.40),
    "perle":(.25,.31,.37, .28,.39),
    "Blanc":(.69,.72,.70, .02,.42),
    "Anthracite":(.030,.039,.042, .04,.55),
    "Métal":(.28,.35,.43, .72,.27),
    "pétrole":(.010,.19,.21, .24,.38),
}
HERO=("01_trois_quarts",(.90,-1.55,.83),(.040,0,.064),.375)
VIEWS=(
    HERO,
    ("02_face",(1,0,.10),(.050,0,.068),.285),
    ("03_lateral",(0,-1,.07),(.067,0,.057),.333),
    ("04_arriere",(-1,.045,.14),(.027,0,.067),.292),
    ("05_assemble",(.49,1.27,.53),(.047,0,.065),.361),
    ("06_epaule",(.56,-1.0,.51),(.002,-.011,.081),.165),
    ("07_coude",(.76,1.05,.62),(.027,.007,.120),.131),
    ("08_poignet",(.93,-1.02,.89),(.104,.002,.119),.107),
    ("09_main",(1.03,-.64,1.09),(.161,-.003,.112),.132),
)


def material(name,color,metallic=0.0,roughness=.37,alpha=1.0):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    m.diffuse_color=(*color,alpha)
    bsdf=m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value=(*color,1)
    bsdf.inputs["Metallic"].default_value=metallic
    bsdf.inputs["Roughness"].default_value=roughness
    bsdf.inputs["Alpha"].default_value=alpha
    if alpha<1:
        m.surface_render_method="DITHERED"
    return m


def look_at(obj,p):
    obj.rotation_euler=(Vector(p)-obj.location).to_track_quat("-Z","Y").to_euler()


class Studio:
    def __init__(self,root,width,engine):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.root=root
        self.renders=root/"docs/renders/r03"
        self.technical=root/"docs/wireframes/r03"
        for d in (self.renders,self.technical):
            d.mkdir(parents=True,exist_ok=True)
        self.scene=bpy.context.scene
        self.scene.render.engine=engine
        self.scene.cycles.samples=16
        self.scene.cycles.use_denoising=True
        self.scene.render.resolution_x=width
        self.scene.render.resolution_y=round(width*.72)
        self.scene.render.resolution_percentage=100
        self.scene.render.image_settings.file_format="PNG"
        self.scene.render.image_settings.color_mode="RGB"
        self.scene.render.image_settings.compression=18
        self.scene.view_settings.view_transform="AgX"
        self.scene.view_settings.look="AgX - Medium High Contrast"
        world=bpy.data.worlds.new("Studio AURA")
        world.use_nodes=True
        world.node_tree.nodes["Background"].inputs[0].default_value=(.34,.46,.57,1.0)
        world.node_tree.nodes["Background"].inputs[1].default_value=.39
        self.scene.world=world
        self.mats={key:material(key,val[:3],val[3],val[4]) for key,val in PALETTE.items()}
        self.faint=material("Enveloppes PETG translucides",(.12,.38,.44),.02,.32,.21)
        self.line=material("Lignes de contour",(.12,.65,.76),0,.55)
        bsdf=self.line.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Emission Color"].default_value=(.085,.48,.61,1)
        bsdf.inputs["Emission Strength"].default_value=.6
        self.cut=material("Plans de coupe",(.57,.16,.029),.04,.42)
        self.source={}
        self.objects=[]
        self.technical_objects=[]
        self.floor=self.make_floor()
        self.camera_setup()
        self.light("Source principale",(.07,-.42,.55),24,.34)
        self.light("Remplissage",(.25,.21,.32),7,.34)
        self.light("Contre-jour",(-.23,.32,.33),17,.27)
        self.light("Liseré main",(.42,-.05,.26),5,.24)
        self.populate()

    def make_floor(self):
        bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0111))
        floor=bpy.context.object
        floor.name="Fond studio"
        floor.data.materials.append(material("Fond studio minéral",(.105,.15,.196),roughness=.61))
        return floor

    def camera_setup(self):
        data=bpy.data.cameras.new("Optique orthographique")
        self.camera=bpy.data.objects.new("Optique orthographique",data)
        self.scene.collection.objects.link(self.camera)
        self.scene.camera=self.camera
        data.type="ORTHO"
        data.clip_end=15
        data.clip_start=.001

    def light(self,name,xyz,power,size):
        d=bpy.data.lights.new(name,"AREA")
        d.energy=power
        d.size=size
        o=bpy.data.objects.new(name,d)
        o.location=xyz
        look_at(o,(.045,0,.04))
        self.scene.collection.objects.link(o)

    def populate(self):
        with gzip.open(HERE/"Source_Rendu_r03.json.gz","rt",encoding="utf8") as handle:
            parts=json.load(handle)
        col=bpy.data.collections.new("AURA-009 · Solides Fusion r03")
        self.scene.collection.children.link(col)
        for source in parts:
            mesh=bpy.data.meshes.new(source["nom"])
            mesh.from_pydata(source["vertices"],[],source["faces"])
            mesh.update()
            mesh.polygons.foreach_set("use_smooth",[True]*len(mesh.polygons))
            mesh.set_sharp_from_angle(angle=.48)
            o=bpy.data.objects.new(source["nom"],mesh)
            mat=next((m for k,m in self.mats.items() if k in source["finish"]),self.mats["Métal"])
            mesh.materials.append(mat)
            col.objects.link(o)
            self.objects.append(o)
            self.source[o]=(source["code"],source["parent"],mat)

    def reset(self):
        for o in list(self.technical_objects):
            bpy.data.objects.remove(o,do_unlink=True)
        self.technical_objects.clear()
        for o in self.objects:
            o.hide_render=False
            o.location=(0,0,0)
            o.data.materials[0]=self.source[o][2]
        self.floor.hide_render=False

    def shot(self,folder,key,eye,target,scale):
        self.camera.location=Vector(target)+Vector(eye).normalized()*.72
        look_at(self.camera,target)
        self.camera.data.ortho_scale=scale
        self.scene.render.filepath=str(folder/(key+".png"))
        print("AURA_RENDER",key,flush=True)
        bpy.ops.render.render(write_still=True)

    def exploded(self):
        for o in self.objects:
            code,parent,_=self.source[o]
            dx,dy,dz=0.,0.,0.
            if code.startswith(("FIL_","G_J","S_J","BAG_J","ATT_F_")):
                o.location=(0,.020,0)
                continue
            if code.startswith(("SERVO_J2","P07_","DOG_J2","CORNE_J2","PALIER_J2_G")):
                dy=-.038
            elif code.startswith(("SERVO_J3","P08_","DOG_J3","CORNE_J3","PALIER_J3_G")):
                dy=-.043
                dx=.015
            elif code.startswith(("P09_","P11_","STAT_J2","ROT_J2","PALIER_J2_D")):
                dy=.032 if "P09_" in code else .056
            elif code.startswith(("P10_","P12_","STAT_J3","ROT_J3","PALIER_J3_D")):
                dy=.039 if "P10_" in code else .063
                dx=.016
            elif code.startswith(("07_","12_","10_","11_","SERVO_T1","T2_","ROD","Retenue_","Vis_Support","Guide_")) or (
                len(code)==2 and code[0] in "PIMAU" and code[1].isdigit()) or code.startswith("Vis_"):
                dx=.036
                if code.startswith("12_"):
                    dy=-.012
                if len(code)==2 and code[1].isdigit():
                    dx+=.005*int(code[1])
            elif code.startswith(("14_","RLT_","DOG_J7","ENT_J7")):
                dx=.024
            elif code.startswith(("J7","13_","SERVO_J7")) or "Bride" in code:
                dx=.015
            elif code.startswith("LEST"):
                dz=-.017
            elif code.startswith(("08_","09_")):
                dz=.016
            o.location=(dx,dy,dz)
        self.floor.hide_render=True

    def transparent(self):
        for o in self.objects:
            code,_,_=self.source[o]
            if code.startswith(("01_","02_","03_","04_","05_","06_","07_","P07_","P08_","P09_","P10_",
                               "P11_","P12_","08_","09_","13_")):
                o.data.materials[0]=self.faint

    def outline_all(self):
        for obj in self.objects:
            obj.hide_render=True
        self.floor.hide_render=True
        curve=bpy.data.curves.new("Arêtes après soudure des sommets","CURVE")
        curve.dimensions="3D"
        curve.bevel_resolution=1
        curve.bevel_depth=.000145
        curve.resolution_u=1
        for obj in self.objects:
            bm=bmesh.new()
            bm.from_mesh(obj.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000007)
            for edge in bm.edges:
                if edge.calc_length()<.00011:
                    continue
                if edge.is_boundary or (edge.is_manifold and edge.calc_face_angle(0.0)>.45):
                    spline=curve.splines.new("POLY")
                    spline.points.add(1)
                    for p,v in zip(spline.points,edge.verts):
                        p.co=(*v.co,1)
            bm.free()
        lines=bpy.data.objects.new("Arêtes géométriques Fusion",curve)
        curve.materials.append(self.line)
        self.scene.collection.objects.link(lines)
        self.technical_objects.append(lines)

    def section(self,normal,xyz,accepted):
        for obj in self.objects:
            obj.hide_render=True
            if not accepted(self.source[obj][0]):
                continue
            bm=bmesh.new()
            bm.from_mesh(obj.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000007)
            geom=list(bm.verts)+list(bm.edges)+list(bm.faces)
            result=bmesh.ops.bisect_plane(bm,geom=geom,dist=.000002,
                                        plane_co=Vector(xyz),plane_no=Vector(normal),
                                        clear_outer=True,clear_inner=False)
            edges=[e for e in result["geom_cut"] if isinstance(e,bmesh.types.BMEdge) and e.is_valid and e.is_boundary]
            if edges:
                for face in bmesh.ops.holes_fill(bm,edges=edges,sides=0)["faces"]:
                    face.material_index=1
            if bm.faces:
                dest=bpy.data.meshes.new(obj.name+" · section")
                bm.to_mesh(dest)
                dest.materials.append(self.source[obj][2])
                dest.materials.append(self.cut)
                rendered=bpy.data.objects.new(dest.name,dest)
                self.scene.collection.objects.link(rendered)
                self.technical_objects.append(rendered)
            bm.free()
        self.floor.hide_render=True

    def run(self):
        for args in VIEWS:
            self.shot(self.renders,*args)
        self.exploded()
        self.shot(self.renders,"10_eclate",(.83,-1.41,.79),(.08,0,.060),.410)
        self.reset()
        self.transparent()
        self.shot(self.renders,"11_mecanismes_transparents",(.54,1.34,.73),(.053,0,.065),.358)
        self.reset()
        self.outline_all()
        self.shot(self.technical,"01_filaire",(.85,-1.35,.84),(.040,0,.067),.372)
        self.reset()
        self.exploded()
        self.shot(self.technical,"02_eclate_fixations",(.55,1.40,.94),(.08,0,.070),.402)
        self.reset()
        self.transparent()
        self.shot(self.technical,"03_faisceau_et_cartes",(-.34,1.45,1.20),(.042,0,.058),.370)
        self.reset()
        self.section((0,0,1),(0,0,.082),lambda c:"J2" in c or c in ("03_Tourelle","04_Segment_1"))
        self.shot(self.technical,"04_coupe_epaule",(.10,-.20,1),(.008,-.020,.082),.150)
        self.reset()
        self.section((0,0,1),(.0263,0,.121),lambda c:"J3" in c or c in ("04_Segment_1","05_Segment_2"))
        self.shot(self.technical,"05_coupe_coude",(.27,-.27,1),(.035,-.007,.121),.146)
        self.reset()
        self.section((0,0,1),(.106,0,.121),lambda c:"J7" in c or c in
                     ("06_Segment_3","07_Paume","13_Bride_Poignet","14_Moyeu"))
        self.shot(self.technical,"06_coupe_poignet",(.08,-.30,1),(.105,0,.121),.117)
        self.reset()
        self.transparent()
        self.floor.hide_render=True
        self.shot(self.technical,"07_tendons_et_traverse",(.24,.45,-1),(.152,0,.111),.132)
        self.reset()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("root",type=Path)
    parser.add_argument("--width",type=int,default=2000)
    parser.add_argument("--engine",default="BLENDER_EEVEE")
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    Studio(args.root,args.width,args.engine).run()


if __name__=="__main__":
    main()
