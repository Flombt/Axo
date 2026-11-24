"""Vérifier la commande historique sans écrire dans firmware/ ni ouvrir de port."""
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path.cwd()
SOURCE = ROOT / "archives/r05/firmware"
OUT = ROOT / "docs/diagnostic/latest/preuves"
MPY = Path.home() / "AppData/Local/Temp/aura-audit-mpy/mpy_cross/mpy-cross.exe"


def run():
    text = (SOURCE / "controle.py").read_text(encoding="utf-8")
    code = compile(text, str(SOURCE / "controle.py"), "exec")
    ctrl = {}
    exec(code, ctrl)
    compile((SOURCE / "main.py").read_text(encoding="utf-8"), str(SOURCE / "main.py"), "exec")
    tests = {}
    parse, Motion, pulse = ctrl["parse"], ctrl["Motion"], ctrl["pulse_us"]
    diff = lambda a, b: a - b
    controller = Motion()
    for command in ("ARM", "MOVE J2=1"):
        try:
            controller.command(command, 0)
        except ValueError as exc:
            tests[f"boot_{command}"] = str(exc)
    for command in ("MOVE I=NaN", "MOVE J2=-22", "MOVE J1=1 J1=2", "STOP x",
                    "MOVE J2R=10", "MOVE J3R=10", "MOVE J7=10", "MOVE A=10", "MOVE U=10"):
        try:
            parse(command)
        except ValueError as exc:
            tests[command] = str(exc)
    controller = Motion(True)
    controller.command("ARM", 0)
    controller.command("MOVE J2=-18 J3=-22 I=92", 0)
    for now in range(20, 5001, 20):
        if now % 100 == 0:
            controller.command("PING", now)
        controller.tick(now, diff)
    tests["commande_combinée_acceptée"] = dict(zip(ctrl["AXES"], controller.position))
    tests["rail_externe_absent_de_l_interface"] = controller.armed
    tests["avant_timeout"] = controller.tick(5349, diff) is not None
    tests["au_timeout"] = {"output": controller.tick(5350, diff), "reason": controller.reason}
    controller.command("ARM", 5400)
    tests["au_réarmement"] = list(controller.position)
    controller.command("STOP", 5420)
    tests["après_STOP"] = controller.tick(5420, diff)
    profile = [(1500, 9, 500, 2500)] * len(ctrl["AXES"])
    tests["conversion_pulse_us"] = {axis: [pulse(degree, i, profile) for degree in ctrl["BOUNDS"][i]]
                                  for i, axis in enumerate(ctrl["AXES"])}
    build = {}
    if MPY.is_file():
        build["version"] = subprocess.check_output([str(MPY), "--version"], text=True, stderr=subprocess.STDOUT).strip()
        with tempfile.TemporaryDirectory(prefix="aura-firmware-audit-") as folder:
            for path in (SOURCE / "main.py", SOURCE / "controle.py"):
                dest = Path(folder) / f"{path.stem}.mpy"
                job = subprocess.run([str(MPY), "-o", str(dest), str(path)], capture_output=True, text=True)
                build[path.name] = {"result": job.returncode, "bytes": dest.stat().st_size if dest.exists() else 0,
                                    "stderr": job.stderr.strip().replace(path.as_posix(), path.relative_to(ROOT).as_posix())}
    evidence = {"axes": ctrl["AXES"], "bounds": ctrl["BOUNDS"], "ratio": ctrl["DRIVE_RATIO"],
                "rates": ctrl["RATES"], "accelerations": ctrl["ACCELERATIONS"], "tests": tests,
                "compilation_mpy_cross": build}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "firmware_r05.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False))


if __name__ == "__main__":
    run()
