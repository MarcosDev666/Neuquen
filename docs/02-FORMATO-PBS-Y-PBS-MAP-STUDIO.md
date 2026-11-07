# 02 · Qué sabemos del formato de mapas de PBSU (y cómo se compila uno)

> Resumen honesto, investigado en 2026-11. El motor de Proton Bus Simulator es
> cerrado; este documento refleja **información pública de la comunidad**.
> Lo que no está confirmado está marcado como tal.

## Cómo distribuye mapas PBSU

- Los mapas se publican como archivos **.zip** que el instalador del juego
  (botón "+" en la pantalla de selección de mapas) extrae y registra.
- En Android viven en `Android/data/com.viamep.<variante>/files/maps/`; en PC
  en `Documentos/Proton Bus Mods/maps/`.
- Buenos ejemplos públicos: "Ponaex City" (Rusia), "Uruguay", "Map Ceará
  Extremo II", "Motor Depot" — todos por modders independientes, con pesos de
  decenas de MB (texturas comprimidas y LOD propio).
- Los paquetes mezclan **meshes/escenas** del motor del juego y **texturas
  móviles optimizadas**. La estructura interna (nombre de assets, escenas,
  archivos de configuración) **no está documentada oficialmente**; la comunidad
  los estudia con descompiladores de Unity y prueba en el juego.

## Lo que NO existe (todavía)

- Un SDK público de mapas de ViaMep.
- Un compilador abierto y estable de escenas PBSU.
- Documentación oficial del formato binario.

## PBS Map Studio (terceros, la vía práctica)

Herramienta independiente **no oficial**: **PBS Map Studio** (rts-darkzone-gaming,
itch.io, plataforma Windows, estado "Paid Beta", desarrollo activo; v0.9.6 al
2026-11). Según su propia descripción pública:

- Editor de rutas con pendientes, terreno automático a lo largo de las vías,
  caminos para tráfico IA, paradas y líneas de colectivo, biblioteca de assets
  PBS (.3ds), gizmo de mover/rotar/escalar, vegetación y pasto desde texturas,
  generación de objetos al borde de ruta, colisiones, **validación y export de
  paquetes PBS**.
- Trial gratuito: 1 hora por PC (requiere conexión a internet y fecha/hora
  correctas). Límites del trial: **250 m por ruta, 1 000 m de red total y
  20 rutas** — adecuado para probar, insuficiente para una ciudad completa.
- Licencia: suscripción mensual/anual (precio publicado en ARS/EUR). Cada
  export debe ser **validado y probado en el juego** por cuenta y riesgo.
- El autor no reclama afiliación con ViaMep.

## Estrategia recomendada para Neuquén Capital

1. **Validar escala en el trial**: reconstruir SOLO el eje Av. Argentina
   (≈ 7 km) y el recorrido COLE L5 (circular) con el trial. Si el juego los
   acepta, el pipeline funciona.
2. **Versión completa**: adquirir PBS Map Studio (o esperar herramienta oficial)
   y construir el mapa completo desde este repositorio (orden en
   `docs/04-DISENO-EN-JUEGO.md`).
3. **QA en juego**: cada export debe probarse en PBSU Android (o PC), en un
   dispositivo real, con al menos: recorrido completo L1, cruce del Puente
   Carretero, terminal → centro por el Bajo.
4. **Publicación**: si el resultado es jugable, proponerlo en
   protonbusmods.com y/o el canal de Bus Simulation Channel.

## Alternativa: mapa existente como base

Si ViaMep o la comunidad publica/ermite usar un mapa de base (un zip del juego),
este repositorio aporta: silueta de ríos, topología vial, landmarks y datos COLE
para re-texturizar/re-modelar sin investigación. En ese caso:

1. Copiar la silueta de ríos como arcos/meshes del mapa base.
2. Re-colocar edificios según los centroides y manzanas LOD1 de `3d/`.
3. Re-señalizar con nombres reales (datos de `data/`).

## Lo que el motor (probablemente) espera de un paquete de mapa

Expectativa razonable basada en la comunidad (no confirmada por ViaMep):

- Escenas/meshes con convención de unidades en metros, ejes Y-arriba,
  1 unidad = 1 m.
- Materiales con texturas comprimidas (móvil) y pocos materiales por mesh.
- Colisores simplificados separados de la malla visual.
- Datos de tráfico/paradas en archivos internos del paquete.
- Nombre único de mapa (evitar choque con mapas instalados).

Por eso este proyecto modela en metros, con Z-norte y Y-arriba, y mantiene
landmarks reconocibles: es compatible con cualquier pipeline tipo Blender →
exportador.

## Riesgos y límites honestos

- El exportador puede rechazar mallas demasiado densas: el OBJ provisto es un
  *blockout*; para el juego final hace falta retopología/LOD (ver `docs/04`).
- Los ríos reales traen curvas de OSM: suavizar antes de crear splines en el
  editor (pocos puntos por curva → kinks en conducción suave). Este proyecto
  re-muestrea a 40–60 m; aun así el editor querrá arcos/curvas nativas.
- Nada garantiza aprobación por parte de ViaMep ni de los catálogos: depende
  del resultado jugable.
