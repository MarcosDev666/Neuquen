"""
validate.py — Verificación integral del proyecto. Sale con código 1 si algo falla.
"""
import json
import math
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILURES = []

def check(label, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(label)

def load(p):
    with open(os.path.join(ROOT, p)) as f:
        return json.load(f)

def main():
    # --- JSON de datos
    roads = load("data/roads.json")["ways"]
    ok = True
    for w in roads:
        if len(w["pts"]) < 2:
            ok = False
        for x, y in w["pts"]:
            if not (-22000 < x < 10000 and -10000 < y < 11000):
                ok = False
    check(f"roads.json: {len(roads)} vías, geometría en rango", ok and len(roads) >= 25)
    classes = {w["class"] for w in roads}
    check("roads.json: clases válidas", classes <= {"trunk", "avenue", "primary", "secondary", "tertiary", "rail"})
    check("roads.json: incluye puente carretero", any(w.get("bridge") for w in roads))

    nb = load("data/neighborhoods.json")["neighborhoods"]
    check(f"neighborhoods.json: {len(nb)} barrios (>=45)", len(nb) >= 45)

    pois = load("data/pois.json")["pois"]
    check(f"pois.json: {len(pois)} POIs (>=10)", len(pois) >= 10)
    check("pois.json: ids únicos", len({p["id"] for p in pois}) == len(pois))

    cole = load("data/cole_lines.json")
    check("cole_lines.json: 30 líneas urbanas", len(cole["lines"]) == 30)
    check("cole_lines.json: frecuencias positivas",
          all(isinstance(l["frequency_min"], (int, float)) and l["frequency_min"] > 0 for l in cole["lines"]))
    check("cole_lines.json: numeración 1..30", sorted(l["number"] for l in cole["lines"]) == list(range(1, 31)))

    # --- GeoJSON ríos
    for f in os.listdir(os.path.join(ROOT, "data/geo")):
        if f.endswith(".geojson"):
            load(f"data/geo/{f}")
    check("data/geo: GeoJSON ríos/límites parseables", True)

    # --- OBJ / MTL
    obj_path = os.path.join(ROOT, "3d/NeuquenCapital.obj")
    mtl_path = os.path.join(ROOT, "3d/NeuquenCapital.mtl")
    n_v = n_f = 0
    face_ids = []
    used_mats = set()
    with open(obj_path) as f:
        for line in f:
            if line.startswith("v "):
                n_v += 1
            elif line.startswith("f "):
                n_f += 1
                ids = [int(t.split("/")[0]) for t in line.split()[1:]]
                face_ids.append(max(ids))
            elif line.startswith("usemtl "):
                used_mats.add(line.split()[1])
    min_id = 1
    with open(obj_path) as f:
        for line in f:
            if line.startswith("f "):
                min_id = min(min_id, min(int(t.split("/")[0]) for t in line.split()[1:]))
    check(f"OBJ: {n_v} vértices, {n_f} caras", n_v > 5000 and n_f > 10000)
    check("OBJ: índices de caras válidos (1..n)", min_id >= 1 and max(face_ids) <= n_v)
    mtl_text = open(mtl_path).read()
    mtl_mats = set(re.findall(r"newmtl\s+(\S+)", mtl_text))
    check(f"MTL: {len(mtl_mats)} materiales; todos los usemtl definidos",
          used_mats <= mtl_mats, f"faltan: {sorted(used_mats - mtl_mats) or 'ninguno'}")

    # --- SVG bien formados
    for f in sorted(os.listdir(os.path.join(ROOT, "maps"))):
        if f.endswith(".svg"):
            try:
                ET.parse(os.path.join(ROOT, "maps", f))
                ok = True
            except ET.ParseError:
                ok = False
            check(f"SVG válido: {f}", ok)

    # --- PNG presentes y legibles
    try:
        from PIL import Image
        for f in sorted(os.listdir(os.path.join(ROOT, "maps"))):
            if f.endswith(".png"):
                im = Image.open(os.path.join(ROOT, "maps", f))
                check(f"PNG legible: {f} {im.size}", im.size[0] >= 800 and im.size[1] >= 600)
    except ImportError:
        check("Pillow disponible para validar PNG", False, "pip install pillow")

    # --- ZIP del mod
    dist = os.path.join(ROOT, "dist")
    zips = [f for f in os.listdir(dist)] if os.path.isdir(dist) else []
    if zips:
        zp = os.path.join(dist, zips[0])
        try:
            with zipfile.ZipFile(zp) as z:
                bad = z.testzip()
                names = z.namelist()
            check(f"ZIP íntegro: {zips[0]} ({len(names)} entradas)", bad is None)
            check("ZIP incluye LEEME, manifiesto, mapas, 3d y datos",
                  any("LEEME.txt" in n for n in names)
                  and any("MANIFIESTO.json" in n for n in names)
                  and any(n.endswith(".obj") for n in names)
                  and any("roads.json" in n for n in names))
        except zipfile.BadZipFile:
            check(f"ZIP íntegro: {zips[0]}", False)
    else:
        check("dist/*.zip presente (correr tools/build_mod.py primero)", False)

    print()
    if FAILURES:
        print(f"RESULTADO: {len(FAILURES)} falla(s): {FAILURES}")
        return 1
    print("RESULTADO: todo OK ✔")
    return 0

if __name__ == "__main__":
    sys.exit(main())
