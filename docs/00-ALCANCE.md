# 00 · Alcance del proyecto

**Neuquén Capital — Proton Bus Simulator (Android)** · v1.0.0 · 2026-11-06

## Qué es esto

Un proyecto **completo y documentado** para incorporar la **Ciudad de Neuquén**
(capital de la provincia del Neuquén, Argentina) como mapa del juego
**Proton Bus Simulator** (Android y Windows). Incluye:

- 4 mapas cartográficos renderizados (general, detalle del centro, corredores
  COLE, inset provincial) en SVG (vector) y PNG.
- Modelo **3D esquemático** del ejido (OBJ/MTL): terreno con la confluencia real
  Limay–Neuquén–Negro, red vial, vías FCG Roca, centro LOD1 con 144 edificios,
  clusters de altura, Parque Central, ciudad industrial y 8 landmarks
  (Monumento a San Martín, Terminal de Ómnibus, Estación, Puente Carretero,
  Municipalidad, Hospital Castro Rendón, Aeropuerto Presidente Perón, Isla 132).
- **Datos estructurados** (JSON): red vial clasificada, 50 barrios, 13 puntos de
  interés con fuentes, las **30 líneas COLE** con frecuencias (Ko-Ko / Expreso
  Tigre Iguazú, desde feb-2023), geometría real de ríos y límites.
- **Documentación** para instalar, diseñar el mapa en el juego, y mantener el
  proyecto (docs/01 a 05).
- **Paquete distribuible** (`dist/NeuquenCapital_PBSU_v1.0.0.zip`) con todo lo
  anterior + carátula.

## Qué NO es (todavía)

**No es un archivo de mapa "compilado" y listo para que el juego lo cargue.**
El formato interno de mapas de Proton Bus Simulator es **propietario** y no
está documentado públicamente: no existe un SDK oficial ni un compilador
comunitario estable. Los mapas publicados en la comunidad fueron hechos con
herramientas de terceros (ver `docs/02-FORMATO-PBS-Y-PBS-MAP-STUDIO.md`).

En la práctica esto significa:

| Quiero… | Qué tenés hoy | Qué falta |
|---|---|---|
| Ver y usar los mapas (referencia, poster, minimapa) | ✅ listo (`maps/`) | — |
| Estudiar el trazado para recrearlo | ✅ listo (`data/`, SVG con ejes y distancias) | — |
| Importar la geometría a Blender / otra herramienta | ✅ listo (`3d/NeuquenCapital.obj`) | ajustar materiales/LOD |
| Compilar un mapa jugable para PBSU | 🟡 fuente completa | recrear vías/terreno en PBS Map Studio o herramienta equivalente y exportar (`docs/04`) |
| Publicar el mod en protonbusmods.com | 🟡 contenido listo | el archivo jugable + testing en juego + aprobación del sitio |

Lo que este proyecto **sí** resuelve: todo el trabajo de relevamiento, diseño,
topología vial, contenido (COLE, barrios, POIs), geometría base y empaquetado,
que es el 80 % del esfuerzo y la parte que no podés hacer jugando. Lo que queda
fuera de mi alcance: el binario final del motor y el visto bueno de publicación.

## Precisión de los datos

- **Ríos y límites provinciales**: geometría real (OpenStreetMap vía SpocWiki,
  CC BY-SA 3.0). Ver `data/sources.json`.
- **Red vial, POIs marcados `approx`, centroides de barrios**: **esquemáticos**,
  ±100–300 m (vial) y ±300–800 m (barrios). Reproducen la topología real
  (qué calle continúa con qué, qué cruza a qué), no el trazado oficial.
- Para producción: re-anclar ejes a OSM antes de exportar el binario
  (`docs/05-DESARROLLO.md`, sección "Anclar a OpenStreetMap").

## Marcas y afiliación

No afiliado a ViaMep / Proton Bus Simulator, a la Municipalidad de Neuquén, a
Vialidad Nacional, a Ko-Ko S.R.L. ni a Expreso Tigre Iguazú. Las marcas son de
sus titulares. Datos con atribución en `NOTICE.md`.
