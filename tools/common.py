"""
common.py — Utilidades compartidas del proyecto Neuquén Capital PBSU.

Proyección local equirectangular centrada en el centro de la ciudad.
  Origen: (lon0, lat0) = (-68.0591, -38.9516)  ≈ Av. Argentina y Roca
  Unidades: metros.  +x = este,  +y = norte.

NOTA DE PRECISIÓN: la geometría de vías/barrios es un relevamiento
ESQUEMÁTICO (±100-300 m) para uso en mapas de juego / documentación.
Los ríos y límites provinciales SÍ provienen de datos reales (ver
docs/05-DESARROLLO.md y NOTICE.md).
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LAT0, LON0 = -38.9516, -68.0591
M_LAT = 110574.0
M_LON = 111320.0 * math.cos(math.radians(LAT0))

def project(lon, lat):
    """WGS84 lon/lat -> metros locales (x este, y norte)."""
    return ((lon - LON0) * M_LON, (lat - LAT0) * M_LAT)

def unproject(x, y):
    """Metros locales -> WGS84 lon/lat."""
    return (LON0 + x / M_LON, LAT0 + y / M_LAT)

# Límites del ejido urbano relevado (lon/lat)
BBOX = (-68.205, -39.015, -67.985, -38.878)  # lon_min, lat_min, lon_max, lat_max

def bbox_local():
    xs, ys = [], []
    for lon, lat in [(BBOX[0], BBOX[1]), (BBOX[2], BBOX[1]),
                     (BBOX[2], BBOX[3]), (BBOX[0], BBOX[3])]:
        x, y = project(lon, lat)
        xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)

def load_json(path):
    with open(os.path.join(ROOT, path)) as f:
        return json.load(f)

def dump_json(path, obj, indent=2):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)

def load_geojson(path):
    d = load_json(path)
    if "features" in d:
        return [f for f in d["features"]]
    return [d]

def coords_of(geom):
    """Devuelve lista de listas de puntos (lon/lat) para LineString/MultiPolygon/Polygon/MultiLineString."""
    t = geom["type"]
    c = geom["coordinates"]
    if t == "LineString":
        return [c]
    if t == "MultiLineString":
        return c
    if t == "Polygon":
        return c
    if t == "MultiPolygon":
        out = []
        for poly in c:
            out.extend(poly)
        return out
    raise ValueError("Tipo de geometría no soportado: " + t)

def resample_line(line_lonlat, max_step_m=120):
    """Re-muestrea una polilínea (lon/lat) a ~max_step_m en metros (para render suave)."""
    pts = [project(*p[:2]) for p in line_lonlat]
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        dist = math.dist(a, b)
        n = max(1, int(dist // max_step_m))
        for i in range(1, n + 1):
            t = i / n
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out

def clip_line_to_box(line_lonlat, box_lonlat, margin_deg=0.02):
    """Recorta una polilínea (lon/lat) a una caja ampliando con margen; devuelve lista de segmentos."""
    lon_min, lat_min, lon_max, lat_max = box_lonlat
    lon_min -= margin_deg; lat_min -= margin_deg
    lon_max += margin_deg; lat_max += margin_deg
    def inside(p):
        return lon_min <= p[0] <= lon_max and lat_min <= p[1] <= lat_max
    segs, cur = [], []
    for p in line_lonlat:
        if inside(p):
            cur.append(p)
        else:
            if len(cur) >= 2:
                segs.append(cur)
            cur = []
    if len(cur) >= 2:
        segs.append(cur)
    return segs
