"""
build_mod.py — Empaqueta el mod de Neuquén Capital para Proton Bus Simulator.

Genera: dist/NeuquenCapital_PBSU_v1.0.0.zip con:
  NeuquenCapital/
    LEEME.txt              guía rápida de instalación y estado del proyecto
    MANIFIESTO.json        versión, fecha, sha256 por archivo
    mapas/*.png|.svg       los 4 mapas renderizados
    3d/NeuquenCapital.obj  modelo 3D esquemático (importable a Blender)
    3d/NeuquenCapital.mtl
    datos/*.json           roads, barrios, POIs, líneas COLE, ríos (geo)
    docs/*.md              guías completas (instalación, formato, diseño, desarrollo)
    assets/portada.png     arte de carátula del mod

NOTA (importante): el formato binario interno de mapas de PBSU es propietario
y no está documentado públicamente. Este paquete es la FUENTE COMPLETA del mapa
(relevamiento + geometría + diseño) lista para compilarse/importarse con las
herramientas descritas en docs/02 y docs/04. Ver docs/00-ALCANCE.md.
"""
import hashlib
import json
import os
import sys
import zipfile
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = "1.0.0"
NAME = "NeuquenCapital"
ZIP_NAME = f"{NAME}_PBSU_v{VERSION}.zip"
PREFIX = f"{NAME}/"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def gather():
    """Lista (origen_abs, destino_en_zip)."""
    plan = []
    def add(src_rel, dst_rel=None):
        plan.append((os.path.join(ROOT, src_rel), dst_rel or src_rel))
    for f in sorted(os.listdir(os.path.join(ROOT, "maps"))):
        if f.startswith("_"):
            continue
        add(f"maps/{f}", f"mapas/{f}")
    add("3d/NeuquenCapital.obj")
    add("3d/NeuquenCapital.mtl")
    add("3d/BUILD-INFO.txt")
    for f in sorted(os.listdir(os.path.join(ROOT, "data"))):
        if f.endswith(".json"):
            add(f"data/{f}", f"datos/{f}")
    for f in sorted(os.listdir(os.path.join(ROOT, "data/geo"))):
        if f.endswith(".geojson"):
            add(f"data/geo/{f}", f"datos/geo/{f}")
    for f in sorted(os.listdir(os.path.join(ROOT, "docs"))):
        if f.endswith(".md"):
            add(f"docs/{f}")
    add("README.md")
    add("NOTICE.md")
    if os.path.exists(os.path.join(ROOT, "assets/portada.png")):
        add("assets/portada.png")
    return [(s, PREFIX + d) for s, d in plan]

LEEME = f"""NEUQUÉN CAPITAL — Mapa para Proton Bus Simulator (Android)
Versión {VERSION}
============================================================

Gracias por descargar el proyecto de mapa de Neuquén Capital (Provincia del
Neuquén, Argentina) para Proton Bus Simulator / Proton Bus Sims (Android y PC).

QUÉ ES ESTE PAQUETE
-------------------
Es la FUENTE COMPLETA y documentada del mapa:
  · mapas renderizados (general, detalle del centro, corredores COLE) en PNG/SVG
  · modelo 3D esquemático del ejido (OBJ/MTL): terreno, Limay/Neuquén/Negro,
    red vial, vías FCG Roca, centro LOD1, landmarks (Monumento, Terminal,
    Estación, Puente Carretero, Municipalidad, Hospital, Aeropuerto)
  · datos estructurados (JSON): red vial, 50 barrios, 13 puntos de interés,
    las 30 líneas COLE con frecuencias, geometría real de ríos y límites
  · documentación completa en español (instalación, formato, diseño, desarrollo)

QUÉ NO ES (todavía)
-------------------
No es un binario de mapa "compilado" para el motor del juego: el formato
interno de mapas de PBSU es propietario y no está documentado públicamente.
Para convertir este material en un mapa jugable consultá:
  · docs/02-FORMATO-PBS-Y-PBS-MAP-STUDIO.md
  · docs/04-DISENO-EN-JUEGO.md
  · docs/01-INSTALACION-ANDROID.md  (cómo instalar mapas en Android)

RUTAS SUGERIDAS PARA EL JUEGO
------------------------------
Líneas COLE armadas como corredores (ver mapas/neuquen-rutas-cole.png y
docs/04): L1, L2, L5, L8, L17, L18. Terminal punto de origen para largas
distancias; Puente Carretero como conexión con Cipolletti.

CRÉDITOS Y LICENCIAS
--------------------
· Datos geográficos de ríos y límites: OpenStreetMap vía SpocWiki/America-
  Argentina (CC BY-SA 3.0). Ver NOTICE.md.
· Resto: relevamiento documental propio, fuentes citadas en cada archivo y en
  docs/03-MAPA-REAL-NEUQUEN.md.
· Este trabajo se comparte bajo CC BY-SA 3.0. No afiliado a ViaMep/Proton,
  a la Municipalidad de Neuquén ni a Vialidad Nacional.
"""

def main():
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    zip_path = os.path.join(dist, ZIP_NAME)
    files = gather()
    manifest = {
        "name": "Neuquén Capital — Proton Bus Simulator",
        "version": VERSION,
        "build": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "platform": "Android / Windows (Proton Bus Simulator)",
        "files": {},
        "totals": {},
    }
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr(PREFIX + "LEEME.txt", LEEME)
        for src, dst in files:
            z.write(src, dst)
        for src, dst in files:
            with open(src, "rb") as f:
                manifest["files"][dst] = {"bytes": os.path.getsize(src),
                                          "sha256": sha256(src)}
        manifest["totals"] = {
            "files": len(manifest["files"]) + 2,  # LEEME + este manifiesto
            "uncompressed_bytes": sum(f["bytes"] for f in manifest["files"].values()),
        }
        z.writestr(PREFIX + "MANIFIESTO.json",
                   json.dumps(manifest, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(zip_path) as z:
        bad = z.testzip()
        assert bad is None, f"zip corrupto: {bad}"
        count = len(z.namelist())
    size = os.path.getsize(zip_path) / 1e6
    print(f"OK {zip_path}\n  entradas: {count}\n  tamaño: {size:.2f} MB")
    return 0

if __name__ == "__main__":
    sys.exit(main())
