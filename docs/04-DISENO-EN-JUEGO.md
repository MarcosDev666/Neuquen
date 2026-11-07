# 04 · Cómo llevar Neuquén Capital al PBSU (diseño jugable)

## 1 · Objetivos de diseño

1. Que un colectivero reconozca Neuquén de un vistazo: el eje Argentina,
   la grilla, las vías, el bajo, los ríos, el puente y la barda.
2. Que COLE sea jugable: líneas con corredores reales y cabeceras terminales.
3. Que rinda en gama media de Android: draw calls bajos, LOD agresivo.
   El juego prioriza 30 fps estables sobre fidelidad.

## 2 · Marco de referencia del proyecto

| Parámetro | Valor |
|---|---|
| Proyección | Plano local tangente; **1 unidad = 1 m**; Y-arriba (3D), Norte = +Z (OBJ) |
| Origen | Av. Argentina y Roca (centro cívico) = (0, 0) |
| Límites del modelo 3D | lon −68.205..−67.985 · lat −39.015..−38.878 (~22 km de lado, con margen rural) |
| Núcleo urbano útil | ≈ 6.8 km E-O (Argentina/Oeste → puente) × 6.0 km N-S (barda → Limay) |
| Alturas | Centro ≈ 220 m; confluencia ≈ nivel del agua; barda ≈ 265 m |
| Datum | El juego trabaja en su propio espacio; anclar a coordenadas reales solo importa para la gente, no para el motor |

## 3 · Área jugable sugerida (Android)

Dos opciones:

- **A — Compacta (recomendada v1)**: 13.5 × 13.5 km centrado en Argentina y
  Roca. Incluye todo el urbano + Limay/Neuquén/Negro + puente + Acceso Oeste
  parcial + barda de fondo. Tráfico IA fluido.
- **B — Ampliada (v1.1)**: 20 × 20 km con Valentinas y el Limay completo hasta
  el dique; requiere +50 % de assets y texturizado; SOLO si el perfil de gama
  media lo soporta.

## 4 · Orden de construcción (fases)

### Fase 1 — Terreno y agua (base)
- Malla del terreno fuera del motor (Blender: plano subdividido, desplazado
  por altura real; exportar como heightmap o mesh).
- Fuentes de agua como planos a cota única con estilo de juego (gloss).
  En PBSU: terreno + ríos se resuelven con el terreno automático del editor
  y las mallas de agua; ver `docs/02`.
- Barda: acantilado suavizado N (nunca vertical: el juego odia paredes
  de 100 m sin LOD).

### Fase 2 — Troncales (esqueleto)
1. **Av. Argentina/Olascoaga** (Eje Cívico): 4 carriles + boulevard central
   con palmeras/tipas; doble sentido; ciclovía.
2. **RN 22 / Av. del Trabajador + Puente Carretero**: ingreso del O,
   bajo, cruce del río; el puente como pieza clave (colisiones correctas).
3. **Av. del Oeste** y **Acceso Oeste**: anillo occidental.
4. **Vías FCG Roca**: plataforma de 1 vía (sin electrificar) + catenarias
   dummy + Estación Terminal como hito (sin servicio de pasajeros).
5. Rotondas principales (Argentina × Independencia; RN22 × Huillén).

### Fase 3 — Centro (manzanas y circulación)
- Grilla del centro con sentido vial real (sentido único por cuadra —
  en el juego: doble mano solo en troncales; la grilla secundaria como
  "evitación" del tráfico IA).
- Núcleo de altura: 8.000–11.000 hab./km²; edificios 8–15 pisos en el
  triángulo Argentina–Independencia–Belgrano (ver LOD1 de `3d/`).
- Bajo (RN22): galpones, corralones, estaciones de servicio, terminales
  de carga — textura industrial.

### Fase 4 — Barrios (completitud visual)
- Cada uno de los 50 barrios: silueta, 4–8 volúmenes representativos,
  cartelería con nombre. No hace falta modelar todas las casas:
  hileras instanciadas con 2–3 tipos de vivienda (monotipo, duplex, palomera).
- Parque Central: plazoleta + senderos + arboleda instanciada (85 + perímetro).

### Fase 5 — Landmarks (los 8 del modelo)
- **Monumento a San Martín**: obelisco ~20 m sobre plazoleta con fuente.
- **Terminal**: volúmen de concreto + marquesina + banderas E.T.O.N.;
  playas de autos,dársenas para 12–15 unidades COLE.
- **Estación FCG Roca**: nave de galpón con hastial + chimenea.
- **Puente Carretero**: puente viejo (arcos dobles) + nuevo paralelo
  (vigas pretensadas); ambos con colisiones.
- **Municipalidad**: torre de vidrio + banderas.
- **Hospital Castro Rendón**: bloque + cruz en la cubierta.
- **Aeropuerto Presidente Perón**: pista 09/27, terminal austera
  (panel de publicidad Vaca Muerta),torre de control baja, WC de combustible.
- **Balneario Isla 132**: muelle/costanera con palapas y puestos.

### Fase 6 — Paradas y líneas COLE (el corazón jugable)
Paradas sugeridas por corredor (8 por línea, esquinas reales; respetar
sentido único):

| Línea | Cabeceras | Intermedio sugerido |
|---|---|---|
| L1 | Gran Neuquén Norte ↔ Área Centro Sur | Godoy/Petagna → Godoy/Ruta 22 → Argentina/Independencia → Argentina/Roca → San Martín/Brown → Zelaya/Belgrano |
| L2 | Sapere ↔ C. Industrial J. Nevares | Sapere → Argentina/Ruta 22 → Argentina/Independencia → Zelaya → Planas y Solalique → C. Industrial |
| L5 | Gran Neuquén ↔ Confluencia | Gran Neuquén → Argentina/Godoy → Argentina/Independencia → San Martín → Villa Farrell → Confluencia |
| L8 | Gran Neuquén Sur ↔ Área Centro | Gran Neuquén Sur → Huillén/Ruta 22 → Argentina/Ruta 22 → Argentina/Independencia → Zelaya |
| L17 | Sapere ↔ Altos del Limay | Sapere → Huillén → Oeste/Ruta 22 → Zelaya/Argentina → San Martín/Ruta 22 → Limay |
| L18 | Confluencia ↔ Área Centro Este | Confluencia → Planas/Solalique → Argentina/Zelaya → Argentina/Roca → Independencia |
Trazado completo: `data/cole_lines.json` + `maps/neuquen-rutas-cole.png`.
Cada parada: marquesina + cartel línea + 0–3 NPC. Las filas de espera en
horarios puntas (7–9, 12–14, 16–19).

### Fase 7 — Tráfico y vida urbana
- Spawn en Terminal (arranque de servicio; boarding de pasajeros).
- IA: troncales con flujo "alto" (1 vehículo cada 8–12 s en hora pico
  virtual), secundarias "medio" (cada 20–30 s).
- Taxis y remises en Terminal; camiones RN22 con agrupamiento en cola
  cerca del puente (sí, el embotellamiento del puente es parte del color
  local — úselo con moderación: 2–3 camiones, no 20).

### Fase 8 — Optimización y LOD
| Presupuesto | Meta |
|---|---|
| Triángulos por escena | ≤ 150 000 (motor PBSU + Android gama media) |
| Draw calls | ≤ 120 visibles |
| Texturas | atlas ≤ 2048², RGB565 o ETC2; un atlas por "distrito" (centro, bajo, barda, barrios) |
| LOD | 3 niveles: 0–150 m (full), 150–600 m (bloques simples), > 600 m (impostor/billboard) |
| Colisiones | cajas/cascos simples; SIN trimesh en edificios |
| Transparencia | evitar; usar máscara solo en vidrios de torres del centro |

## 5 · QA antes de publicar

- [ ] Recorrido completo L1 cronometrado (debe caber en 35–45 min con tráfico).
- [ ] Cruce del Puente Carretero sin z-fighting ni caídas.
- [ ] Terminal: boarding + al menos 3 salidas IA funcionando.
- [ ] Sin errores en el visor de colisiones del editor.
- [ ] Exported + import test en PBSU (Android real, no emulador).
- [ ] 60 min de juego continuo sin cuelgues (leaks de mallas).
- [ ] Créditos visibles en la descripción del mapa en protonbusmods.com.

## 6 · Créditos y licencia del producto final

El mapa compilado, si se publica, debe retener: atribución OSM (ODbL),
aviso CC BY-SA 3.0 de SpocWiki, atribución de los proveedores de imágenes
(satelital usada como referencia de construcción, si se usa), y este
aviso dentro del paquete (`LEEME.txt`).
