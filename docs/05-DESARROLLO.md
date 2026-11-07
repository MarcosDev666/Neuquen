# 05 · Desarrollo del proyecto

## 1 · Estructura del repositorio

```
Neuquen/
├── README.md                  presentación del proyecto
├── NOTICE.md                  atribuciones y licencias
├── LICENSE?                   CC BY-SA 3.0 (aviso en NOTICE.md; link oficial)
├── data/
│   ├── roads.json             red vial clasificada (31 vías, ejes en coords metros)
│   ├── neighborhoods.json     50 barrios con centroide y zona
│   ├── pois.json              13 landmarks con fuente (approx salvo aeropuerto)
│   ├── cole_lines.json        30 líneas COLE + interurbanas + frecuencias
│   ├── sources.json           registro de fuentes (legible por máquinas)
│   └── geo/                   ríos Limay/Neuquén/Negro + límites (OSM, CC BY-SA 3.0)
├── maps/                      4 mapas SVG+PNG (renderizados)
├── 3d/
│   ├── NeuquenCapital.obj     modelo 3D esquemático (metros, Y-arriba, Z-norte)
│   ├── NeuquenCapital.mtl
│   └── BUILD-INFO.txt
├── assets/portada.png         carátula (IA, ilustrativa)
├── docs/                      00..05 (este árbol de documentación)
├── tools/
│   ├── common.py              proyección local (origen Av. Argentina y Roca)
│   ├── build_roads.py         construye data/roads.json (una sola vez)
│   ├── scene.py               mini-motor de escenas SVG+PNG
│   ├── render_map.py          renderiza los 4 mapas
│   ├── build_3d.py            construye el OBJ/MTL + BUILD-INFO.txt
│   ├── build_mod.py           empaqueta dist/*.zip + MANIFIESTO.json
│   └── validate.py            verificación integral (CI-friendly)
├── dist/                      paquete zip final + checksums
└── .github/workflows/validate.yml   CI: corre validate.py en cada push/PR
```

## 2 · Requisitos y regeneración

Requisitos: **Python 3.10+**; para los PNG: `pip install pillow`.
Nada más: los mapas no requieren geodatabases ni GDAL.

```bash
python3 -m venv .venv && . .venv/bin/activate   # opcional pero recomendado
pip install pillow
python3 tools/render_map.py     # maps/*.svg + maps/*.png
python3 tools/build_3d.py       # 3d/NeuquenCapital.obj + .mtl + BUILD-INFO.txt
python3 tools/build_mod.py      # dist/NeuquenCapital_PBSU_v1.0.0.zip
python3 tools/validate.py       # verificación integral
```

`build_roads.py` solo hace falta si cambia la topología de vías.

## 3 · Fuentes de datos y licencias (resumen)

| Capa | Fuente | Licencia | Precisión |
|---|---|---|---|
| Ríos y límites | OSM vía SpocWiki/America-Argentina (GitHub) | CC BY-SA 3.0 / ODbL | alta |
| Hechos (Puente, COLE, barrios, POIs) | municipalidad, Wikipedia, periodismo | hechos públicos; redacción propia | alta (hechos) |
| Coordenadas aeropuerto | SkyVector + AIP | AIP pública | alta |
| Red vial, POIs `approx`, barrios | elaboración propia | CC BY-SA 3.0 | esquemática (±100–800 m) |
| Terreno y manzanas LOD1 | elaboración propia | CC BY-SA 3.0 | esquemática |
| Carátula | IA generativa | CC BY-SA 3.0 | ilustrativa |

Registro completo y legible por máquinas: `data/sources.json`.
Atribución requerida al redistribuir (ODbL + CC BY-SA): ver `NOTICE.md`.

## 4 · Anclar a OpenStreetMap y a elevaciones reales (roadmap v1.1)

Hoy la red vial es esquemática (topológicamente correcta, posicionada a ojo).
Para producción se recomienda:

1. Descargar el extracto OSM del área (bbox lon −68.21..−67.98, lat −39.02..−38.87)
   desde Geofabrik o Overpass (no se distribuye en este repo por licencia y tamaño;
   ODbL permite el uso con atribución).
2. Extraer ejes viales principales (highway=primary|secondary|trunk|motorway)
   con `osmium`/`osmconvert` o Overpass Turbo → GeoJSON.
3. Reproyectar con el mismo origen (lon0 −68.0591, lat0 −38.9516) y reemplazar
   la geometría en `data/roads.json` conservando el atributo `class`.
4. Reemplazar alturas del terreno por SRTM/NASADEM (30 m) recortado al bbox;
   regenerar el OBJ.
5. Re-correr `render_map.py`, `build_3d.py`, `build_mod.py`, `validate.py`.

## 5 · Convenciones

- Español rioplatense para contenidos, español neutro para código y mensajes.
- JSON con `indent=2`, UTF-8, claves en inglés (`id`, `zone`, `lon`, `lat`),
  valores de nombres en español con mayúsculas de palabra.
- Coordenadas: `[lon, lat]` (orden GeoJSON) en los archivos de datos;
  metros locales `[x_este, y_norte]` en `data/roads.json` y en el OBJ.
- Clases viales: `trunk` (ruta), `avenue` (troncal urbana), `primary`,
  `secondary`, `tertiary`, `rail`.
- Contribuciones: PR a `arena/0d0c6875-neuquen` (o fork), describiendo la
  fuente del dato; para rutas COLE se aceptan solo cambios verificables.

## 6 · Validación (qué chequea validate.py)

- JSON parseable; nº de vías ≥ 25 y todas con ≥ 2 puntos dentro del bbox.
- Clases viales válidas; existe al menos un tramo con `bridge=true`.
- ≥ 45 barrios; ≥ 10 POIs con ids únicos; 30 líneas COLE numeradas 1..30,
  frecuencias positivas.
- OBJ: vértices/caras mínimos; todos los índices de cara en rango; todos los
  `usemtl` definidos en el MTL.
- Los 4 SVG parsean; los PNG son legibles por Pillow con tamaño mínimo.
- El zip en `dist/` pasa `testzip()` e incluye LEEME, MANIFIESTO.json, el OBJ
  y roads.json.

## 7 · Versionado

- v1.0.0 (2026-11-06): fuente completa + mapas + modelo 3D esquemático + zip.
- v1.1.0 (planeada): anclaje OSM + SRTM; alturas reales; correcciones COLE.
- v2.0.0 (planeada): binario jugable (requiere PBS Map Studio o herramienta
  oficial) + publicación en protonbusmods.com.
