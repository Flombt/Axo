"""Rendus Blender à partir des maillages et matrices d’assemblage natives."""
import gzip
import json
import math
from pathlib import Path
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

ROOT=Path(sys.argv[sys.argv.index("--")+1]).resolve()
PROOF=ROOT/"docs/diagnostic/corrections"
GALLERY=PROOF/"visuels"
D=json.loads((PROOF/"geometrie_neutre.json").read_text(encoding="utf-8"))
P=D["parts"]
SCALE=.001
PALETTE={"structure":(.16,.21,.25,1), "coque":(.36,.45,.52,1), "main":(.80,.74,.63,1),
         "gear":(.09,.38,.40,1),"steel":(.42,.47,.54,1),"servo":(.06,.08,.10,1),
         "cable":(.09,.54,.49,1),"spring":(.82,.43,.16,1),"board":(.11,.29,.25,1)}


def kind(k):
    if P[k].get("flexible"):
        return "spring" if k.startswith("Ressort") else "cable"
    if k.startswith(("Coque","Capot","Garde")):
        return "coque"
    if k.startswith(("Moteur","Distribution")):
        return "servo"
    if k=="Pico":
        return "board"
    if "Roue" in k or "Pignon" in k or k.startswith("Bobine"):
        return "gear"
    if len(k)==2 or k.startswith(("11_","12_","Peigne")):
        return "main"
    return "structure" if P[k].get("print_ref") else "steel"


def material(name,color):
    mat=bpy.data.materials.new(name)
    mat.diffuse_color=color
    mat.use_nodes=True
    n=mat.node_tree.nodes.get("Principled BSDF")
    n.inputs["Base Color"].default_value=color
    n.inputs["Roughness"].default_value=.42 if name!="steel" else .29
    n.inputs["Metallic"].default_value=.66 if name=="steel" else .0
    return mat


def matrix(raw):
    m=Matrix([raw[i:i+4] for i in range(0,16,4)])
    for i in range(3):
        m[i][3]*=.01
    return m


def aim(object, at):
    object.rotation_euler=(Vector(at)-object.location).to_track_quat("-Z","Y").to_euler()


def light(name,origin,target,power,size,color):
    bpy.ops.object.light_add(type="AREA",location=origin)
    obj=bpy.context.object
    obj.name=name
    obj.data.energy=power
    obj.data.shape="DISK"
    obj.data.size=size
    obj.data.color=color
    aim(obj,target)


def camera(origin,target,lens):
    scene=bpy.context.scene
    scene.camera.data.type="ORTHO"
    scene.camera.data.ortho_scale=lens
    scene.camera.location=origin
    aim(scene.camera,target)


def render(scene, name):
    scene.render.filepath=str(GALLERY/name)
    bpy.ops.render.render(write_still=True)


def cutaway(obj):
    world=obj.matrix_world
    normal = world.to_3x3().transposed() @ Vector((0,1,0))
    local = world.inverted() @ Vector((0,0,0))
    bm=bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],
                          dist=1e-7,plane_co=local,plane_no=normal,
                          clear_outer=False,clear_inner=True)
    bm.to_mesh(obj.data)
    bm.free()


def run():
    GALLERY.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.world=bpy.data.worlds.new("Atelier")
    scene.world.use_nodes=True
    scene.world.node_tree.nodes.get("Background").inputs[0].default_value=(.35,.43,.56,1)
    scene.world.node_tree.nodes.get("Background").inputs[1].default_value=.35
    scene.render.engine="CYCLES"
    scene.cycles.samples=22
    scene.cycles.use_denoising=True
    scene.render.resolution_x=1300
    scene.render.resolution_y=880
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    mats={k:material(k,v) for k,v in PALETTE.items()}
    with gzip.open(PROOF/"maillages_natifs.json.gz","rt",encoding="utf-8") as f:
        native=json.load(f)
    solids=[]
    for i,b in enumerate(native):
        k=b["part"]
        if k.startswith("Tendon_"):
            continue
        mesh=bpy.data.meshes.new(k)
        v=[tuple(x*SCALE for x in p) for p in b["v"]]
        triangles=[b["f"][n:n+3] for n in range(0,len(b["f"]),3)]
        mesh.from_pydata(v,[],triangles)
        mesh.update()
        obj=bpy.data.objects.new(k+f".{i:03}",mesh)
        scene.collection.objects.link(obj)
        obj.matrix_world=matrix(P[k]["transform"])
        obj.data.materials.append(mats[kind(k)])
        for poly in mesh.polygons:
            poly.use_smooth=False
        solids.append((k,obj))

    floor=json.loads(D["attributes"]["PlanDeTravail"])["plan_table_mm"]/1000
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,floor-.00025))
    desk=bpy.context.object
    desk.name="Table de banc"
    desk.data.materials.append(material("table",(.20,.25,.29,1)))
    bpy.ops.object.camera_add()
    scene.camera=bpy.context.object
    light("Diffuse principale",(.30,-.44,.75),(.1,0,.05),58,.60,(1,.89,.77))
    light("Remplissage",(-.35,-.02,.38),(.12,0,.04),20,.47,(.74,.85,1))
    light("Contour",(.35,.27,.42),(.14,0,.04),38,.38,(.84,1,.94))
    camera((.53,-.48,.27),(.095,0,.043),.47)
    render(scene,"06_blender_ensemble.png")

    for k,obj in solids:
        if k.startswith(("Coque","Capot","Garde")):
            obj.location.z += .075
        elif P[k].get("flexible"):
            obj.hide_render=True
        elif k.startswith("Moteur") and not k.startswith("Moteur_F"):
            obj.location.y += .035
    camera((.56,-.63,.31),(.105,0,.070),.53)
    render(scene,"07_blender_eclate.png")

    for k,obj in solids:
        obj.matrix_world=matrix(P[k]["transform"])
        obj.hide_render=False
    anim=PROOF/"animation_native.json"
    if anim.is_file():
        poses=json.loads(anim.read_text(encoding="utf-8"))
        scene.render.fps=12
        scene.frame_start=1
        scene.frame_end=len(poses)
        for row in poses:
            frame=row["frame"]+1
            for k,obj in solids:
                obj.rotation_mode="QUATERNION"
                obj.matrix_world=matrix(row["transform"][k])
                obj.keyframe_insert("location",frame=frame)
                obj.keyframe_insert("rotation_quaternion",frame=frame)
        scene.frame_set(1)
        # Les volumes souples du F3D représentent uniquement leur géométrie neutre.
        for k,obj in solids:
            if P[k].get("flexible"):
                obj.hide_render=True
        camera((.53,-.48,.27),(.095,0,.043),.47)
        bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/"fusion/AURA-01-cinematique.blend"),compress=True)

    keep=("01_Platine","02_Palier","03_Porte","05_Tourelle","J1_Roue","R6000",
          "Entretoise_J1","Nut_J1","Appui_J1","Collier","Axe_J1","Faisceau_Socle","Faisceau_Tourelle")
    for k,obj in solids:
        obj.matrix_world=matrix(P[k]["transform"])
        obj.hide_render=not k.startswith(keep)
        if not obj.hide_render and k not in ("Faisceau_Socle_Axe","Faisceau_Tourelle"):
            cutaway(obj)
    camera((.15,-.40,.18),(.004,0,.01),.17)
    render(scene,"08_blender_coupe_j1.png")


if __name__=="__main__":
    run()
