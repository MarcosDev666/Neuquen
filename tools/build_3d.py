"""
build_3d.py — Genera el modelo 3D esquemático de Neuquén Capital (OBJ + MTL).

Uso en el juego / Blender:
  3d/NeuquenCapital.obj + 3d/NeuquenCapital.mtl
  Unidades: metros. Y = arriba. Z = norte. Origen ≈ Av. Argentina y Roca.

Contenido: terreno (meseta + barda), ríos (Limay, Neuquén, Negro), red vial
(cintas elevadas), vías FCG Roca, Parque Central, edificios LOD1 del centro,
mahattan del eje, clusters (Alta Barda / Terrazas), Ciudad Industrial,
landmarks (Monumento San Martín, Terminal, Estación, Puente Carretero,
Municipalidad, Hospital Castro Rendón, Aeropuerto Presidente Perón).

Estilo: sin texturas (colores planos por material) → fácil de importar y
optimizar para Android. Ver docs/04-DISENO-EN-JUEGO.md.
"""
import math
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from common import project

random.seed(42)
ROOT = common.ROOT

# ---------------------------------------------------------------- OBJ writer
class OBJ:
    def __init__(self):
        self.verts = []
        self.faces = []
        self.groups = []  # (name, mat, start_face_idx)
        self._cur_group = None
        self._cur_mat = None
    def v(self, x, y, z):
        self.verts.append((x, y, z))
        return len(self.verts)
    def quad(self, a, b, c, d, mat):
        self.faces.append((mat, [a, b, c, d]))
    def tri(self, a, b, c, mat):
        self.faces.append((mat, [a, b, c]))
    def group(self, name, mat):
        self._cur_group = name
    def use(self, mat):
        self._cur_mat = mat
    # ---- autorientación
    def mark(self):
        return len(self.verts), len(self.faces)
    @staticmethod
    def _normal(verts, idxs):
        p0, p1, p2 = (verts[idxs[0] - 1], verts[idxs[1] - 1], verts[idxs[2] - 1])
        ux, uy, uz = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        vx, vy, vz = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
        return (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
    def fix_outward(self, m):
        """Para sólidos convexos: voltea caras cuya normal apunta al interior."""
        v0, f0 = m
        pts = self.verts[v0:]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        cz = sum(p[2] for p in pts) / len(pts)
        for fi in range(f0, len(self.faces)):
            mat, idxs = self.faces[fi]
            nx, ny, nz = self._normal(self.verts, idxs)
            fc = [sum(self.verts[i - 1][k] for i in idxs) / len(idxs) for k in range(3)]
            dot = nx * (fc[0] - cx) + ny * (fc[1] - cy) + nz * (fc[2] - cz)
            if dot < 0:
                self.faces[fi] = (mat, list(reversed(idxs)))
    def fix_up(self, m):
        """Para superficies abiertas casi horizontales: voltea caras que miran hacia abajo."""
        v0, f0 = m
        for fi in range(f0, len(self.faces)):
            mat, idxs = self.faces[fi]
            if self._normal(self.verts, idxs)[1] < 0:
                self.faces[fi] = (mat, list(reversed(idxs)))
    def save(self, obj_path, mtl_name):
        mat_faces = {}
        for mat, idxs in self.faces:
            mat_faces.setdefault(mat, []).append(idxs)
        with open(obj_path, "w") as f:
            f.write("# Neuquén Capital — modelo esquemático para Proton Bus Simulator\n")
            f.write("# Unidades: metros · Y arriba · Z norte · WGS84 vía proyección local (tools/common.py)\n")
            f.write("# Geometría esquelmática ±100-300 m (docs/03, docs/05)\n")
            f.write(f"mtllib {mtl_name}\n")
            for x, y, z in self.verts:
                f.write(f"v {x:.3f} {y:.3f} {z:.3f}\n")
            # agrupar caras por material para reducir cambios de estado
            for mat, fl in mat_faces.items():
                f.write(f"o {mat}\nusemtl {mat}\n")
                for idxs in fl:
                    f.write("f " + " ".join(str(i) for i in idxs) + "\n")
        return len(self.verts), len(self.faces)

MATS = {  # nombre -> (Kd, Ks, Ns)
    "Terrain":   ((0.66, 0.62, 0.44), (0.05, 0.05, 0.05), 12),
    "Water":     ((0.45, 0.62, 0.76), (0.35, 0.35, 0.35), 60),
    "AsphaltT":  ((0.40, 0.38, 0.33), (0.10, 0.10, 0.10), 22),
    "Asphalt":   ((0.44, 0.42, 0.38), (0.10, 0.10, 0.10), 22),
    "Asphalt2":  ((0.49, 0.47, 0.43), (0.10, 0.10, 0.10), 18),
    "Rail":      ((0.19, 0.19, 0.18), (0.25, 0.25, 0.25), 40),
    "Concrete":  ((0.71, 0.69, 0.63), (0.10, 0.10, 0.10), 18),
    "Plaster":   ((0.78, 0.71, 0.61), (0.08, 0.08, 0.08), 14),
    "Brick":     ((0.60, 0.41, 0.26), (0.08, 0.08, 0.08), 14),
    "Light":     ((0.84, 0.82, 0.74), (0.08, 0.08, 0.08), 14),
    "Glass":     ((0.48, 0.63, 0.70), (0.45, 0.45, 0.45), 80),
    "DarkGlass": ((0.33, 0.45, 0.53), (0.50, 0.50, 0.50), 90),
    "Gold":      ((0.78, 0.62, 0.14), (0.60, 0.60, 0.60), 100),
    "Park":      ((0.42, 0.55, 0.29), (0.05, 0.05, 0.05), 12),
    "Trunk":     ((0.40, 0.28, 0.17), (0.05, 0.05, 0.05), 10),
    "Canopy":    ((0.35, 0.47, 0.22), (0.05, 0.05, 0.05), 10),
    "Red":       ((0.62, 0.22, 0.16), (0.10, 0.10, 0.10), 18),
    "Bridge":    ((0.53, 0.50, 0.44), (0.12, 0.12, 0.12), 22),
    "White":     ((0.92, 0.91, 0.87), (0.15, 0.15, 0.15), 30),
}

def write_mtl(path):
    with open(path, "w") as f:
        f.write("# Neuquén Capital PBSU — materiales\n")
        for name, (kd, ks, ns) in MATS.items():
            f.write(f"newmtl {name}\n")
            f.write(f"Kd {kd[0]:.3f} {kd[1]:.3f} {kd[2]:.3f}\n")
            f.write(f"Ka {kd[0]/4:.3f} {kd[1]/4:.3f} {kd[2]/4:.3f}\n")
            f.write(f"Ks {ks[0]:.3f} {ks[1]:.3f} {ks[2]:.3f}\n")
            f.write(f"Ns {ns}\n\n")

# ---------------------------------------------------------------- heights
def smoothstep(a, b, v):
    t = max(0.0, min(1.0, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)

def river_samples():
    pts = []
    for name in ("rio_limay_2", "rio_neuquen_2", "rio_negro_1"):
        feats = common.load_geojson(f"data/geo/{name}.geojson")
        geom = feats[0].get("geometry", feats[0])
        line = geom["coordinates"]
        for seg in common.clip_line_to_box(line, common.BBOX, margin_deg=0.02):
            r = common.resample_line(seg, 60)
            pts.extend(r)
    return pts

RIVER_PTS = river_samples()

def dist_river(x, z):
    best = 1e18
    for px, pz in RIVER_PTS:
        d = (px - x) ** 2 + (pz - z) ** 2
        if d < best:
            best = d
    return math.sqrt(best)

def terrain_h(x, z):
    h = 13.0 + 22.0 * smoothstep(-2600, 6100, z)          # sube hacia la barda (N)
    h += 6.0 * smoothstep(1500, 7500, -x)                  # leve altitud al oeste
    h += 1.7 * math.sin(x * 0.0042 + 1.7) * math.cos(z * 0.0051 + 0.6)
    h += 1.1 * math.sin((x + z) * 0.0023 + 0.9)
    d = dist_river(x, z)
    t = smoothstep(70.0, 300.0, d)                          # canal del río
    return -2.6 + (h + 2.6) * t

# ---------------------------------------------------------------- primitives
def add_terrain(o: OBJ, x0, z0, x1, z1, step=170):
    nx = int((x1 - x0) / step) + 1
    nz = int((z1 - z0) / step) + 1
    idx = {}
    for j in range(nz):
        for i in range(nx):
            x, z = x0 + i * step, z0 + j * step
            idx[(i, j)] = o.v(x, terrain_h(x, z), z)
    m = o.mark()
    for j in range(nz - 1):
        for i in range(nx - 1):
            a, b, c, d = idx[(i, j)], idx[(i, j + 1)], idx[(i + 1, j + 1)], idx[(i + 1, j)]
            o.tri(a, b, c, "Terrain"); o.tri(a, c, d, "Terrain")
    o.fix_up(m)

def add_ribbon(o: OBJ, pts_xz, width, mat, y=None, follow_terrain=True, lift=0.22, closed=False):
    """Cinta horizontal (ruta, río, pista). Si follow_terrain, sigue el terreno."""
    hw = width / 2.0
    n = len(pts_xz)
    left, right = [], []
    for i, (x, z) in enumerate(pts_xz):
        if i == 0:
            dx, dz = pts_xz[1][0] - x, pts_xz[1][1] - z
        elif i == n - 1:
            dx, dz = x - pts_xz[i - 1][0], z - pts_xz[i - 1][1]
        else:
            dx, dz = pts_xz[i + 1][0] - pts_xz[i - 1][0], pts_xz[i + 1][1] - pts_xz[i - 1][1]
        L = math.hypot(dx, dz) or 1.0
        nx, nz = -dz / L, dx / L
        left.append((x + nx * hw, z + nz * hw))
        right.append((x - nx * hw, z - nz * hw))
    li, ri = [], []
    for i in range(n):
        for side, arr, acc in (("L", left, li), ("R", right, ri)):
            x, z = arr[i]
            h = (y if y is not None else terrain_h(x, z) + lift)
            acc.append(o.v(x, h, z))
    m = o.mark()
    for i in range(n - 1):
        a, b, c, d = li[i], ri[i], ri[i + 1], li[i + 1]
        o.tri(a, b, c, mat); o.tri(a, c, d, mat)
    o.fix_up(m)

def add_box(o: OBJ, cx, base_y, cz, sx, sy, sz, mat, ry=0.0):
    m = o.mark()
    hx, hz = sx / 2.0, sz / 2.0
    cs, sn = math.cos(ry), math.sin(ry)
    base = []
    for dx, dz in ((-hx, -hz), (hx, -hz), (hx, hz), (-hx, hz)):
        x = cx + dx * cs + dz * sn
        z = cz - dx * sn + dz * cs
        base.append((x, z))
    top = [o.v(x, base_y + sy, z) for (x, z) in base]
    bot = [o.v(x, base_y, z) for (x, z) in base]
    o.quad(bot[0], bot[3], bot[2], bot[1], mat)      # inferior
    o.quad(top[0], top[1], top[2], top[3], mat)      # superior
    for i in range(4):
        j = (i + 1) % 4
        o.quad(bot[i], bot[j], top[j], top[i], mat)
    o.fix_outward(m)

def add_cyl(o: OBJ, cx, base_y, cz, r, h, mat, seg=14, taper=1.0, cap_top=True, cap_bot=False):
    m = o.mark()
    ring_b, ring_t = [], []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        x, z = cx + r * math.cos(a), cz + r * math.sin(a)
        ring_b.append(o.v(x, base_y, z))
        rt = r * taper
        xt, zt = cx + rt * math.cos(a), cz + rt * math.sin(a)
        ring_t.append(o.v(xt, base_y + h, zt))
    for i in range(seg):
        j = (i + 1) % seg
        o.quad(ring_b[i], ring_b[j], ring_t[j], ring_t[i], mat)
    if cap_top:
        c = o.v(cx, base_y + h, cz)
        for i in range(seg):
            j = (i + 1) % seg
            o.tri(c, ring_t[j], ring_t[i], mat)
    if cap_bot:
        c = o.v(cx, base_y, cz)
        for i in range(seg):
            j = (i + 1) % seg
            o.tri(c, ring_b[i], ring_b[j], mat)
    o.fix_outward(m)

def add_gable(o: OBJ, cx, base_y, cz, length, width, wall_h, roof_h, mat_wall, mat_roof, axis="x"):
    hx, hz = (length / 2, width / 2) if axis == "x" else (width / 2, length / 2)
    y0, y1, y2 = base_y, base_y + wall_h, base_y + wall_h + roof_h
    m = o.mark()
    a = o.v(cx - hx, y0, cz - hz); b = o.v(cx + hx, y0, cz - hz)
    c = o.v(cx + hx, y0, cz + hz); d = o.v(cx - hx, y0, cz + hz)
    a1 = o.v(cx - hx, y1, cz - hz); b1 = o.v(cx + hx, y1, cz - hz)
    c1 = o.v(cx + hx, y1, cz + hz); d1 = o.v(cx - hx, y1, cz + hz)
    r1, r2 = o.v(cx - hx, y2, cz), o.v(cx + hx, y2, cz)
    o.quad(a, b, b1, a1, mat_wall); o.quad(b, c, c1, b1, mat_wall)
    o.quad(c, d, d1, c1, mat_wall); o.quad(d, a, a1, d1, mat_wall)
    o.quad(a1, b1, r2, r1, mat_roof); o.quad(d1, r1, r2, c1, mat_roof)
    o.tri(a1, r1, d1, mat_wall); o.tri(b1, c1, r2, mat_wall)
    o.fix_outward(m)

def loft_hemi(o: OBJ, cx, base_y, cz, radius, length, seg=12, mat="Bridge"):
    """Medio cilindro hueco (techo de arco) con eje a lo largo de X."""
    m = o.mark()
    xr, xl = cx - length / 2, cx + length / 2
    prev_low, prev_up = None, None
    rings = []
    for i in range(seg + 1):
        ang = math.pi * i / seg
        y = base_y + radius * math.sin(ang)
        z = cz + radius * math.cos(ang)
        rings.append((y, z))
    a_ids, b_ids = [], []
    for (y, z) in rings:
        a_ids.append(o.v(xl, y, z))
        b_ids.append(o.v(xr, y, z))
    for i in range(seg):
        o.quad(a_ids[i], b_ids[i], b_ids[i + 1], a_ids[i + 1], mat)
    # tapas planas en los extremos
    for xr_ in (xl, xr):
        c = o.v(xr_, base_y, cz)
        ids = a_ids if xr_ == xl else b_ids
        for i in range(seg):
            if xr_ == xl:
                o.tri(c, ids[i], ids[i + 1], mat)
            else:
                o.tri(c, ids[i + 1], ids[i], mat)
    o.fix_outward(m)

# ================================================================ ESCENA
def main():
    o = OBJ()
    x0, z0, x1, z1 = common.bbox_local()
    X0, X1 = x0 - 400, x1 + 400
    Z0, Z1 = z0 - 400, z1 + 400

    print("· terreno…")
    add_terrain(o, X0, Z0, X1, Z1, step=180)

    print("· agua…")
    for name, wdt in (("rio_limay_2", 165), ("rio_neuquen_2", 150), ("rio_negro_1", 220)):
        feats = common.load_geojson(f"data/geo/{name}.geojson")
        geom = feats[0].get("geometry", feats[0])
        line = geom["coordinates"]
        for seg in common.clip_line_to_box(line, common.BBOX, margin_deg=0.02):
            pts = common.resample_line(seg, 120)
            add_ribbon(o, pts, wdt, "Water", y=0.25, follow_terrain=False, lift=0)

    print("· rutas y vías…")
    roads = common.load_json("data/roads.json")["ways"]
    width_by_class = {"trunk": 17.0, "avenue": 12.0, "primary": 9.0, "secondary": 6.5, "tertiary": 4.5}
    mat_by_class = {"trunk": "AsphaltT", "avenue": "Asphalt", "primary": "Asphalt",
                    "secondary": "Asphalt2", "tertiary": "Asphalt2"}
    for w in roads:
        pts = [tuple(p) for p in w["pts"]]
        if w["class"] == "rail":
            add_ribbon(o, pts, 4.6, "Rail", lift=0.34)
            continue
        add_ribbon(o, pts, width_by_class[w["class"]], mat_by_class[w["class"]], lift=0.24)

    print("· Parque Central y plazas…")
    px, pz = project(-68.0735, -38.9650)
    add_box(o, px, terrain_h(px, pz) + 0.05, pz, 600, 0.35, 400, "Park")
    # árboles del parque (cono + tronco)
    rng = random.Random(7)
    for _ in range(85):
        tx = px + rng.uniform(-280, 280)
        tz = pz + rng.uniform(-175, 175)
        ty = terrain_h(tx, tz)
        add_cyl(o, tx, ty, tz, 0.42, 2.4, "Trunk", seg=6)
        add_cyl(o, tx, ty + 2.2, tz, 2.35, 5.2, "Canopy", seg=8, taper=0.05)

    # monumento: anillo de árboles
    mx, mz = project(-68.0591, -38.9516)
    my = terrain_h(mx, mz)
    for i in range(12):
        a = 2 * math.pi * i / 12
        tx, tz = mx + 17 * math.cos(a), mz + 17 * math.sin(a)
        ty = terrain_h(tx, tz)
        add_cyl(o, tx, ty, tz, 0.4, 2.2, "Trunk", seg=6)
        add_cyl(o, tx, ty + 2.0, tz, 2.1, 4.6, "Canopy", seg=8, taper=0.05)

    print("· Centro: manzanas LOD1…")
    EW = [project(0, -38.9335)[1] + 0,  # placeholder reemplazado abajo
          ]
    # límites reales (latitudes) de las manzanas del centro
    ew_lats = [-38.9442, -38.9482, -38.9516, -38.9550, -38.9568, -38.9600, -38.9645, -38.9685]
    ns_lons = [-68.0885, -68.0745, -68.0675, -68.0591, -68.0535, -68.0475, -68.0418]
    ew_y = [project(0, lat)[1] for lat in ew_lats]
    ns_x = [project(lon, 0)[0] for lon in ns_lons]
    axis_x = project(-68.0591, 0)[0]
    rail_y = project(0, -38.9568)[1]
    inset_ew = {0: 10.0, 1: 8.0, 2: 9.0, 3: 8.0, 5: 9.0, 6: 7.5, 7: 7.5}
    inset_ns = {0: 8.5, 1: 7.5, 2: 8.0, 3: 13.0, 4: 7.5, 5: 7.0, 6: 6.0}
    mats = ["Plaster", "Brick", "Light", "Concrete", "Light", "Plaster"]
    buildings = 0
    for r in range(len(ew_y) - 1):
        y_s, y_n = ew_y[r], ew_y[r + 1]
        y_lo, y_hi = min(y_s, y_n), max(y_s, y_n)
        if abs((y_lo + y_hi) / 2 - rail_y) < 90:
            # franja de vías: galpones ferroviarios aislados
            for ci in range(2, 5):
                if rng.random() < 0.75:
                    gx = (ns_x[ci] + ns_x[ci + 1]) / 2
                    gz = (y_lo + y_hi) / 2
                    add_box(o, gx, terrain_h(gx, gz) + 0.1, gz, 26, 5.5, 12, "Concrete")
                    buildings += 1
            continue
        for c in range(len(ns_x) - 1):
            x_w, x_e = ns_x[c], ns_x[c + 1]
            ins_w = inset_ns.get(c, 7.0); ins_e = inset_ns.get(c + 1, 7.0)
            ins_s = inset_ew.get(r, 7.5); ins_n = inset_ew.get(r + 1, 7.5)
            bx0, bx1 = x_w + ins_w, x_e - ins_e
            bz0, bz1 = y_lo + ins_s, y_hi + ins_n
            if bx1 - bx0 < 18 or bz1 - bz0 < 18:
                continue
            cx, cz = (bx0 + bx1) / 2, (bz0 + bz1) / 2
            dist_axis = abs(cx - axis_x)
            h = 31.0 - dist_axis * 0.038 + rng.uniform(-4, 7)
            h = max(9.0, min(33.0, h))
            xs = [(bx0, bx1)]
            if (bx1 - bx0) > 52 and rng.random() < 0.7:
                mid = (bx0 + bx1) / 2 + rng.uniform(-6, 6)
                xs = [(bx0, mid - 2.2), (mid + 2.2, bx1)]
            zs = [(bz0, bz1)]
            if (bz1 - bz0) > 46 and rng.random() < 0.65:
                midz = (bz0 + bz1) / 2 + rng.uniform(-5, 5)
                zs = [(bz0, midz - 2.2), (midz + 2.2, bz1)]
            for (p0, p1) in xs:
                for (q0, q1) in zs:
                    if p1 - p0 < 11 or q1 - q0 < 11:
                        continue
                    w = p1 - p0 - rng.uniform(1.2, 4.6)
                    d = q1 - q0 - rng.uniform(1.2, 4.6)
                    if w < 7 or d < 7:
                        continue
                    hh = h * rng.uniform(0.72, 1.15)
                    cxp, czp = (p0 + p1) / 2, (q0 + q1) / 2
                    mat = mats[rng.randrange(len(mats))]
                    ty = terrain_h(cxp, czp)
                    add_box(o, cxp, ty + 0.1, czp, w, hh, d, mat)
                    buildings += 1
                    if hh > 20:  # casilla de ascensor
                        add_box(o, cxp, ty + hh, czp, w * 0.35, 2.6, d * 0.32, "Concrete")

    # torres emblemáticas sobre el eje
    for (lat, lon_off, hh, mat) in [(-38.9442, 4.0, 46.0, "DarkGlass"),
                                     (-38.9516, -4.5, 38.0, "Glass"),
                                     (-38.9600, 4.0, 42.0, "DarkGlass")]:
        txx = project(-68.0591, lat)[0] + lon_off * 11.0
        ty = terrain_h(txx, project(-68.0591, lat)[1])
        zc = project(-68.0591, lat)[1]
        add_box(o, txx, ty + 0.1, zc, 19, hh, 19, mat)
        add_box(o, txx, ty + hh, zc, 8, 3.0, 8, "Concrete")
        buildings += 1

    print("· clusters: Alta Barda / Terrazas / Ciudad Industrial…")
    for (lon, lat, w, d, hh) in [(-68.0520, -38.8965, 15, 22, 47), (-68.0558, -38.8995, 17, 24, 39),
                                 (-68.0490, -38.9020, 13, 19, 33), (-68.0602, -38.8950, 12, 18, 29),
                                 (-68.0955, -38.8995, 16, 22, 36), (-68.0922, -38.8975, 14, 20, 31)]:
        cx, cz = project(lon, lat)
        ty = terrain_h(cx, cz)
        add_box(o, cx, ty + 0.1, cz, w, hh, d, "Glass" if hh > 34 else "Light")
        buildings += 1
    # Ciudad Industrial Jaime de Nevares: galpones
    for i in range(6):
        cx, cz = project(-68.1865 + (i % 3) * 0.0028, -38.9035 - (i // 3) * 0.0024)
        ty = terrain_h(cx, cz)
        add_box(o, cx, ty + 0.1, cz, 34, 8.5, 17, "Concrete")
        buildings += 1

    print("· RN 22: equipamiento disperso (O)…")
    for lon in (-68.190, -68.172, -68.155, -68.138, -68.121, -68.104, -68.088):
        lat = -38.9385 + (lon + 68.245) * 0.30  # sigue la alineación aprox.
        side = 1 if rng.random() < 0.5 else -1
        cx, cz = project(lon, lat)
        cx += rng.uniform(-40, 40); cz += side * rng.uniform(17, 26)
        ty = terrain_h(cx, cz)
        add_box(o, cx, ty + 0.1, cz, rng.uniform(11, 19), rng.uniform(6, 11), rng.uniform(9, 14),
                rng.choice(["Brick", "Light", "Concrete"]))
        buildings += 1

    print("· landmarks…")
    # Monumento a San Martín
    add_cyl(o, mx, my + 0.1, mz, 7.2, 1.25, "Concrete", seg=18)
    add_cyl(o, mx, my + 1.35, mz, 5.3, 1.15, "Concrete", seg=18)
    add_cyl(o, mx, my + 2.5, mz, 3.6, 1.05, "White", seg=18)
    add_cyl(o, mx, my + 3.55, mz, 2.05, 8.6, "Light", seg=4, taper=0.62)
    add_cyl(o, mx, my + 12.1, mz, 1.15, 2.5, "Gold", seg=8, taper=0.15)
    for sx in (-1, 1):
        for sz in (-1, 1):
            add_box(o, mx + sx * 9.5, my + 0.1, mz + sz * 9.5, 1.7, 2.5, 1.7, "Concrete")
    # Terminal de Ómnibus (Planas y Solalique)
    tx, tz = project(-68.0665, -38.9562)
    ty = terrain_h(tx, tz)
    add_box(o, tx, ty + 0.1, tz, 62, 5.5, 34, "Light")
    loft_hemi(o, tx, ty + 5.5, tz, 10.5, 60, seg=12, mat="White")
    add_box(o, tx, ty + 0.05, tz - 26, 110, 0.3, 22, "Asphalt2")   # plataforma de colectivos
    # Estación FCG Roca
    ex, ez = project(-68.0591, -38.9568)
    ey = terrain_h(ex, ez)
    add_gable(o, ex, ey + 0.1, ez, 58, 17, 7.5, 5.5, "Brick", "Bridge", axis="x")
    add_box(o, ex, ey + 0.05, ez - 13, 60, 0.3, 5, "Concrete")
    add_box(o, ex, ey + 0.05, ez + 13, 60, 0.3, 5, "Concrete")
    # Puente Carretero sobre el Río Neuquén (dos calzadas)
    ax_, az_ = project(-68.0430, -38.9510)
    bx_, bz_ = project(-68.0300, -38.9515)
    bridge_y = 6.4
    dx, dz = bx_ - ax_, bz_ - az_
    L = math.hypot(dx, dz)
    ry = math.atan2(dz, dx) * -1.0
    cxp, czp = (ax_ + bx_) / 2, (az_ + bz_) / 2
    add_box(o, cxp, bridge_y, czp, L + 26, 1.7, 10.5, "Bridge", ry=ry)
    for i in range(1, 9):
        t = i / 9.0
        px_, pz_ = ax_ + (bx_ - ax_) * t, az_ + (bz_ - az_) * t
        add_cyl(o, px_, -2.4, pz_, 1.35, bridge_y + 2.4, "Concrete", seg=10)
    # Municipalidad
    ux, uz = project(-68.0598, -38.9472)
    uy = terrain_h(ux, uz)
    add_box(o, ux, uy + 0.1, uz, 34, 17, 24, "Light")
    add_cyl(o, ux + 12, uy + 17, uz + 6, 0.24, 15, "Rail", seg=6)
    # Hospital Castro Rendón (cruz en la azotea)
    hx_, hz_ = project(-68.0522, -38.9395)
    hy = terrain_h(hx_, hz_)
    add_box(o, hx_, hy + 0.1, hz_, 44, 21, 30, "White")
    add_box(o, hx_, hy + 21.1, hz_, 9.5, 1.1, 3.0, "Red")
    add_box(o, hx_, hy + 21.1, hz_, 3.0, 1.1, 9.5, "Red")
    # Aeropuerto Presidente Perón (pista 09/27 · 2570 m)
    apx, apz = project(-68.1406, -38.9514)
    ty_ap = terrain_h(apx, apz)
    d_ = (math.sin(math.radians(87)), math.cos(math.radians(87)))  # rumbo 087°
    p0 = (apx - d_[0] * 1285, apz - d_[1] * 1285)
    p1 = (apx + d_[0] * 1285, apz + d_[1] * 1285)
    add_ribbon(o, [p0, p1], 46, "Rail", y=ty_ap + 0.4, follow_terrain=False)
    add_box(o, apx, ty_ap + 0.2, apz - 70, 74, 10, 24, "Light")
    add_cyl(o, apx + 40, ty_ap + 0.2, apz - 70, 2.1, 19, "White", seg=10)
    add_box(o, apx + 40, ty_ap + 19.2, apz - 70, 5.4, 3.1, 5.4, "DarkGlass")
    # Balneario Isla 132: espigón sobre el Limay
    ix, iz = project(-68.1005, -38.9910)
    add_box(o, ix, 0.9, iz - 22, 3.2, 1.0, 42, "Trunk")

    print(f"· edificios colocados: {buildings}")
    nv, nf = o.save(f"{ROOT}/3d/NeuquenCapital.obj", "NeuquenCapital.mtl")
    write_mtl(f"{ROOT}/3d/NeuquenCapital.mtl")
    size_mb = os.path.getsize(f"{ROOT}/3d/NeuquenCapital.obj") / 1e6
    info = (
        "# Neuquén Capital — build 3D\n\n"
        f"- vértices: {nv}\n"
        f"- caras: {nf}\n"
        f"- archivo OBJ: {size_mb:.2f} MB\n"
        f"- edificios: {buildings} + landmarks\n"
        "- materiales: ver 3d/NeuquenCapital.mtl\n"
        "- se genera con: python3 tools/build_3d.py\n"
        "- nota: el OBJ no trae normales de vértice; los windings SÍ son consistentes\n"
        "  (sólidos hacia afuera; terreno/agua/rutas mirando hacia arriba).\n"
        "  En Blender: Importar OBJ, seleccionar todo y Shift+N (Recalcular normales).\n"
        "- ribbons (rutas/ríos) siguen el terreno; para el juego final, splines propias (docs/04).\n"
    )
    with open(f"{ROOT}/3d/BUILD-INFO.txt", "w") as f:
        f.write(info)
    print(info)

if __name__ == "__main__":
    main()
