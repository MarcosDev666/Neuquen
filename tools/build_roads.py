"""
build_roads.py — Genera data/roads.json: red vial de Neuquén Capital (esquemática).

Fuentes: relevamiento documental (ver docs/03-MAPA-REAL-NEUQUEN.md).
AVISO: geometrías ±100-300 m. Para export final a motor/PBS se recomienda
re-anclar los ejes a OpenStreetMap (docs/05-DESARROLLO.md).

Clases: trunk (autovía/ex RN 22) · avenue · primary · secondary · tertiary · residential
"""
import math
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

P = common.project

# Puntos de control conocidos (lon, lat)
def LL(lon, lat):
    x, y = P(lon, lat)
    return [round(x, 1), round(y, 1)]

# Los caminos se definen en lon/lat y se guardan proyectados (metros locales).
# y positivo = norte; el renderer SVG puede invertirlo.

WAYS = []

def way(name, cls, pts_lonlat, oneway=False, bridge=False, ref=None, source="relevamiento"):
    WAYS.append({
        "id": f"W{len(WAYS)+1:04d}",
        "name": name,
        "ref": ref,
        "class": cls,
        "oneway": oneway,
        "bridge": bridge,
        "pts": [LL(lon, lat) for lon, lat in pts_lonlat],
        "pts_lonlat": [[round(lon, 6), round(lat, 6)] for lon, lat in pts_lonlat],
        "source": source,
        "accuracy": "±100-300 m (esquemático)",
    })

# ---------------------------------------------------------------- ejes troncales
# RN 22 (ex) / Av. del Trabajador — corredor oeste-este con Puente Carretero
way("RN 22 (ex) / Av. del Trabajador", "trunk", [
    (-68.2450, -38.9355), (-68.2100, -38.9375), (-68.1800, -38.9410),
    (-68.1500, -38.9435), (-68.1200, -38.9460), (-68.0950, -38.9500),
    (-68.0750, -38.9545), (-68.0591, -38.9575), (-68.0480, -38.9545),
    (-68.0430, -38.9515),
], ref="RN 22", source="Wikipedia RN 22; neuquencapital.gov.ar (Puente Carretero)")
# Puente Carretero (viejo, 1937 -> Río Negro) y Puente nuevo (1997 -> Neuquén)
way("Puente Carretero (Río Neuquén, 1937)", "trunk", [
    (-68.0430, -38.9515), (-68.0365, -38.9510), (-68.0300, -38.9515),
], ref="RN 22", bridge=True, source="neuquencapital.gov.ar; Wikipedia RN 22")
way("Puente RN 22 nuevo (1997)", "trunk", [
    (-68.0430, -38.9525), (-68.0365, -38.9520), (-68.0300, -38.9525),
], ref="RN 22", bridge=True, source="Wikipedia RN 22")
way("RN 22 -> Cipolletti (Río Negro)", "trunk", [
    (-68.0300, -38.9520), (-68.0100, -38.9570), (-67.9850, -38.9620),
], ref="RN 22", source="relevamiento")
# Acceso Aeropuerto Presidente Perón
way("Acceso Aeropuerto Presidente Perón", "primary", [
    (-68.1440, -38.9440), (-68.1406, -38.9514),
], source="Wikipedia Aeropuerto Presidente Perón")

# ------------------------------------------------- eje principal norte-sur (N-S)
way("Av. Argentina (N) / Av. Olascoaga (S) — Eje monumental", "avenue", [
    (-68.0591, -38.8830), (-68.0591, -38.9100), (-68.0591, -38.9365),
    (-68.0591, -38.9568),  # las vías / estación
    (-68.0591, -38.9750), (-68.0591, -38.9905),  # hacia el Limay
], source="neuquennews.com.ar; kupi.com; guianeuquen.com")

# -------------------------------------------------------------------- avenidas
way("Av. del Oeste (ring oeste)", "avenue", [
    (-68.1295, -38.9020), (-68.1295, -38.9300), (-68.1295, -38.9600),
    (-68.1295, -38.9900), (-68.1295, -39.0000),
], source="relevamiento")
way("Av. Huillén", "primary", [
    (-68.1010, -38.9055), (-68.1010, -38.9300), (-68.1010, -38.9600),
    (-68.1010, -38.9850), (-68.1010, -38.9970),
], source="neuquen.wikimapia.org (callejero)")
way("Av. Bouquet Roldán", "avenue", [
    (-68.1100, -38.9365), (-68.0850, -38.9365), (-68.0591, -38.9365),
    (-68.0350, -38.9365), (-68.0150, -38.9365),
], source="neuquen.wikimapia.org (callejero); neuquennews.com.ar")

# ---------------------------------------------------- colaterales O-E de centros
way("Antártida Argentina", "primary", [
    (-68.1150, -38.9055), (-68.0850, -38.9055), (-68.0550, -38.9055),
    (-68.0300, -38.9055),
], source="neuquen.wikimapia.org (callejero)")
way("Godoy", "primary", [
    (-68.1150, -38.9160), (-68.0850, -38.9160), (-68.0591, -38.9160),
    (-68.0300, -38.9160),
], source="argentino.com.ar (recorridos COLE)")
way("Novela", "secondary", [
    (-68.1150, -38.9215), (-68.0850, -38.9215), (-68.0591, -38.9215),
    (-68.0350, -38.9215),
], source="argentino.com.ar (recorridos COLE)")
way("1º de Mayo", "secondary", [
    (-68.1150, -38.9265), (-68.0850, -38.9265), (-68.0591, -38.9265),
    (-68.0350, -38.9265),
], source="argentino.com.ar (recorridos COLE)")
way("Collón Cura", "secondary", [
    (-68.1200, -38.9315), (-68.0850, -38.9315), (-68.0591, -38.9315),
    (-68.0350, -38.9315),
], source="argentino.com.ar (recorridos COLE)")
way("Independencia (cero)", "primary", [
    (-68.1200, -38.9442), (-68.0850, -38.9442), (-68.0591, -38.9442),
    (-68.0300, -38.9442),
], source="guianeuquen.com (numeración); neuquenalinstante.com.ar")
way("San Martín", "secondary", [
    (-68.1150, -38.9482), (-68.0850, -38.9482), (-68.0591, -38.9482),
    (-68.0300, -38.9482),
], source="guianeuquen.com (numeración); masneuquen.com")
way("Roca", "primary", [
    (-68.1250, -38.9516), (-68.0950, -38.9516), (-68.0591, -38.9516),
    (-68.0300, -38.9516),
], source="kupi.com (Monumento a San Martín, Argentina y Roca)")
way("Mitre", "secondary", [
    (-68.1150, -38.9550), (-68.0850, -38.9550), (-68.0591, -38.9550),
    (-68.0300, -38.9550),
], source="argentino.com.ar (recorridos COLE)")
way("Sarmiento", "primary", [
    (-68.1150, -38.9600), (-68.0850, -38.9600), (-68.0591, -38.9600),
    (-68.0300, -38.9600),
], source="argentino.com.ar (recorridos COLE); masneuquen.com")
way("Ignacio Rivas", "secondary", [
    (-68.1100, -38.9645), (-68.0800, -38.9645), (-68.0591, -38.9645),
    (-68.0350, -38.9645),
], source="argentino.com.ar (recorridos COLE)")
way("Durán", "secondary", [
    (-68.1100, -38.9685), (-68.0800, -38.9685), (-68.0591, -38.9685),
    (-68.0350, -38.9685),
], source="argentino.com.ar (recorridos COLE)")
way("Anaya", "tertiary", [
    (-68.1100, -38.9725), (-68.0800, -38.9725), (-68.0591, -38.9725),
    (-68.0400, -38.9725),
], source="argentino.com.ar (recorridos COLE)")

# -------------------------------------------------------- calles N-S de centros
way("Salta", "primary", [
    (-68.0885, -38.8950), (-68.0885, -38.9200), (-68.0885, -38.9450),
    (-68.0885, -38.9700), (-68.0885, -38.9980),
], source="masneuquen.com (calle Salta); relevamiento")
way("Belgrano", "secondary", [
    (-68.0745, -38.9055), (-68.0745, -38.9300), (-68.0745, -38.9550),
    (-68.0745, -38.9850),
], source="guianeuquen.com; argentino.com.ar (recorridos COLE)")
way("Buenos Aires", "secondary", [
    (-68.0675, -38.9055), (-68.0675, -38.9300), (-68.0675, -38.9550),
    (-68.0675, -38.9850),
], source="neuquen.wikimapia.org (callejero)")
way("Alderete", "secondary", [
    (-68.0535, -38.9100), (-68.0535, -38.9350), (-68.0535, -38.9550),
    (-68.0535, -38.9750),
], source="argentino.com.ar (recorridos COLE)")
way("Tucumán", "secondary", [
    (-68.0475, -38.9055), (-68.0475, -38.9300), (-68.0475, -38.9500),
    (-68.0475, -38.9700),
], source="argentino.com.ar (recorridos COLE)")
way("Tierra del Fuego", "tertiary", [
    (-68.0418, -38.9100), (-68.0418, -38.9300), (-68.0418, -38.9500),
    (-68.0418, -38.9650),
], source="argentino.com.ar (recorridos COLE)")

# -------------------------------------------------------- vías del ferrocarril
# FCG Roca — Buenos Aires al Pacífico: entra del O-NO por Gran Neuquén Norte,
# pasa por la Estación (eje y vías) y sigue al E hacia Cipolletti.
way("Vías F.C. Gral. Roca (BAP)", "rail", [
    (-68.2250, -38.9050), (-68.1900, -38.9130), (-68.1600, -38.9220),
    (-68.1300, -38.9340), (-68.1000, -38.9450), (-68.0800, -38.9525),
    (-68.0591, -38.9568), (-68.0400, -38.9585), (-68.0300, -38.9625),
], source="masneuquen.com (estación); relevamiento")

# ---------------------------------------------------------------- conexiones
# Bajo: puente viejo dirección Río Negro; nudo con Av. del Trabajador
way("Diagonal España (esquemática)", "secondary", [
    (-68.0680, -38.9590), (-68.0560, -38.9475), (-68.0440, -38.9350),
], source="relevamiento (diagonal esquemática)")

# Conexión barda norte (Alta Barda) con el eje
way("Av. Antártida Argentina - acceso Alta Barda", "secondary", [
    (-68.0591, -38.9055), (-68.0520, -38.8950), (-68.0400, -38.8860),
], source="relevamiento")

doc = {
    "meta": {
        "name": "Red vial de Neuquén Capital (esquemática)",
        "generator": "tools/build_roads.py",
        "count": len(WAYS),
        "note": "Geometrías ±100-300 m. Ver docs/03 y docs/05. Coordenadas en metros locales (ver tools/common.py).",
        "classes": ["trunk", "avenue", "primary", "secondary", "tertiary", "rail"],
    },
    "ways": WAYS,
}
common.dump_json("data/roads.json", doc)
n = len(WAYS)
print(f"OK data/roads.json — {n} vías")
for w in WAYS:
    print(f"  {w['id']}  {w['class']:9s} {'BRIDGE' if w['bridge'] else '':6s} {w['name'][:60]}")
