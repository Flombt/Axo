"""Ajoute les maillages natifs du module à une copie de la scène Axo animée."""

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "Axo bras final - Capteurs"
DATA = DEST / "Contrôles" / "maillages_capteurs.json"
GABARITS = {"Pi_5", "USB_1", "USB_2", "Ethernet", "Refroidisseur", "PCB_Camera"}


def setup_camera(eye, target, scale, name):
    camera = bpy.context.scene.camera
    camera.location = eye
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = scale
    camera.name = name


def render(filename):
    scene = bpy.context.scene
    scene.render.filepath = str(DEST / "Images" / filename)
    bpy.ops.render.render(write_still=True)


def add_meshes():
    scene = bpy.context.scene
    housing = bpy.data.collections.new("Module fixe · Vision et audio")
    electronics = bpy.data.collections.new("Gabarits électroniques")
    scene.collection.children.link(housing)
    housing.children.link(electronics)
    material = {"01_Bac_Pi5": "structure", "02_Couvercle": "coque",
                "03_Coque_Camera": "coque", "04_Dos_Camera": "structure",
                "Pi_5": "board", "Refroidisseur": "structure", "PCB_Camera": "board",
                "Micro_USB": "structure"}
    lens = bpy.data.materials.new("Optique · verre sombre")
    shader = lens.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (.008, .018, .030, 1)
    shader.inputs["Metallic"].default_value = .28
    shader.inputs["Roughness"].default_value = .16
    parts = {}
    for name, record in json.loads(DATA.read_text(encoding="utf-8")).items():
        corners = record["triangles"]
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata([tuple(x / 1000 for x in p) for p in record["sommets_mm"]],
                         [], [tuple(corners[i:i + 3]) for i in range(0, len(corners), 3)])
        assert not mesh.validate(verbose=False), name
        mesh.update()
        mesh.materials.append(lens if name == "Objectif"
                              else bpy.data.materials[material.get(name, "steel")])
        item = bpy.data.objects.new(name, mesh)
        (electronics if name in GABARITS else housing).objects.link(item)
        parts[name] = item
    return parts


def main():
    scene = bpy.context.scene
    scene.frame_set(1)
    parts = add_meshes()
    for obj in scene.objects:
        if obj.type == "MESH" and (obj in parts.values() or obj.name.startswith(("Coque_", "Capot_"))):
            for face in obj.data.polygons:
                face.use_smooth = True
            obj.data.set_sharp_from_angle(angle=math.radians(36))
    camera = bpy.data.objects.new("Présentation Capteurs", bpy.data.cameras.new("Présentation Capteurs"))
    scene.collection.objects.link(camera)
    scene.camera = camera
    for marker in scene.timeline_markers:
        if marker.camera is not None:
            marker.camera = camera
    (DEST / "Images").mkdir(exist_ok=True)
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.resolution_x = 1680
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.eevee.taa_render_samples = 128
    scene.view_settings.exposure = -.35
    setup_camera((-.36, .70, .39), (.052, 0, .062), .420, "Vue d’ensemble")
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(DEST / "Axo bras final - Capteurs.blend"))
    render("01_Ensemble.png")
    setup_camera((-.43, .26, .24), (-.101, 0, .030), .205, "Vue du module")
    render("02_Camera_et_micro.png")

    for key, z in {"02_Couvercle": .049, "03_Coque_Camera": .049,
                   "04_Dos_Camera": .049, "PCB_Camera": .049, "Objectif": .049}.items():
        parts[key].location.z += z
    setup_camera((-.43, .44, .36), (-.105, 0, .046), .238, "Vue ouverte du boîtier")
    render("03_Acces_Raspberry_Pi.png")


if __name__ == "__main__":
    main()
