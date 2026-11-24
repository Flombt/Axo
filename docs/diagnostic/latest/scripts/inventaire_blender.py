"""À exécuter dans Blender en arrière-plan avec --disable-autoexec."""
import bpy
import json
from pathlib import Path
import sys

if "--" not in sys.argv:
    raise SystemExit("Passer le chemin du dossier de preuve après --.")

target = Path(sys.argv[sys.argv.index("--") + 1])
source = Path(bpy.data.filepath)
subjects = []
for obj in bpy.data.objects:
    if obj.animation_data or obj.constraints or obj.type == "ARMATURE":
        subjects.append({"name": obj.name, "type": obj.type, "parent": obj.parent.name if obj.parent else None,
                         "action": obj.animation_data.action.name if obj.animation_data and obj.animation_data.action else None,
                         "constraints": [f"{c.type} {c.name}" for c in obj.constraints],
                         "bones": len(obj.data.bones) if obj.type == "ARMATURE" else None})
info = {
    "file": source.name, "saved_with": list(bpy.data.version), "checked_with": bpy.app.version_string,
    "scenes": [{"name": s.name, "range": [s.frame_start, s.frame_end], "fps": s.render.fps / s.render.fps_base}
               for s in bpy.data.scenes],
    "types": {typ: sum(o.type == typ for o in bpy.data.objects) for typ in sorted({o.type for o in bpy.data.objects})},
    "actions": [{"name": a.name, "range": list(a.frame_range)} for a in bpy.data.actions],
    "motion_objects": subjects, "linked_libraries": [l.filepath for l in bpy.data.libraries],
}
target.mkdir(parents=True, exist_ok=True)
(target / f"blender_{source.stem}.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in info.items() if k not in ("motion_objects", "actions")}, ensure_ascii=False))
