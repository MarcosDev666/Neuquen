# 03 · Neuquén Capital — Ficha real para el diseño del mapa

> Fuentes citadas al final de cada sección. Los datos "±" son aproximados;
> ver `data/sources.json` y `NOTICE.md`.

## 1 · Ficha geográfica

| Ítem | Dato |
|---|---|
| Nombre oficial | Ciudad de Neuquén (Capital de la provincia del Neuquén) |
| País / Provincia | Argentina · Neuquén |
| Departamento | Confluencia |
| Coordenadas del centro | ≈ 38°57′S, 68°04′O (Av. Argentina y Roca) — el juego usa proyección local; ver `tools/common.py` |
| Altitud | ≈ 220–270 m s.n.m. (centro ≈ 220 m; la barda norte ≈ 260–280 m) |
| Ríos | Limay (S/SO), Neuquén (E/NE), Negro (nace en la confluencia, hacia el E) |
| Punto de confluencia | ≈ 38.975°S, 68.014°O — **dato real** (geometría OSM en `data/geo/`) |
| Clima | Árido a semiárido patagónico: veranos cálidos y secos, inviernos frescos; vientos fuertes predominantes del O/SO (ráfagas); precipitación escasa (~200 mm/año) |
| Población | El núcleo urbano más poblado de la Patagonia (varias centenas de miles de habitantes en el área metropolitana; exactitud: verificar Censo 2022) |
| Superficie urbana | ≈ 100–130 km² la mancha urbana; el ejido supera ampliamente eso |

### La confluencia (hecho urbano central)

El **Limay** baja desde el NO (Nahuel Huapi; embalses de El Chocón aguas arriba)
y el **Neuquén** baja desde el N/NE (Cordillera del Viento; Cerros Colorados).
Se unen al este de la ciudad y forman el **Río Negro**, que sigue hacia el
Atlántico. La ciudad está en el ángulo noroeste de la unión — de ahí su nombre
histórico ("la Confluencia") y el nombre del departamento.

## 2 · Breve síntesis histórica (para color de mapa)

- Fines del s. XIX: la Buenos Aires al Pacífico llega al valle; la estación
  define "el bajo" y el trazado.
- 1904: el gobierno nacional establece aquí la capital del Territorio Nacional
  del Neuquén (la ex capital era Chos Malal); gestión de Manuel Olascoaga.
- El plano fundacional despliega la cuadrícula a ambos lados de las vías;
  la Av. Argentina nace como eje monumental N–S para unir el Limay con el Neuquén.
- 1937: se inaugura el **Puente Carretero** sobre el Río Neuquén (464 m,
  9 tramos de arcos atirantados de hormigón armado; Vialidad Nacional;
  20-feb-1937). En 1997 se lo dobla con un segundo puente (1997, vigas
  pretensadas): el viejo sirve hacia Río Negro y el nuevo hacia Neuquén.
- 1990s–presente: crecimiento demográfico explosivo (Vaca Muerta, servicios),
  expansión hacia el O (Valentinas, Gran Neuquén) y la barda (Alta Barda).
- 1-feb-2023: debuta el sistema **COLE** (Ko-Ko S.R.L. + Expreso Tigre Iguazú,
  Grupo Vía Bariloche), 30 líneas urbanas + interurbanas complementarias.

## 3 · Límites y vecindad

- **S**: Río Limay (provincia de Río Negro del otro lado; puente vial NO existe
  para autos en el radio urbano: el cruce vehicular relevante es al E).
- **E**: Río Neuquén (del otro lado, Cipolletti, Río Negro — 198.000–110.000
  hab., segundo polo urbano del Alto Valle).
- **NE/N**: barda/meseta; al N, la zona rural (Rincón de Emilio, Rincón del Río).
- **O**: meseta aluvial; plots rurales (Colonia Nueva Esperanza, Valentina);
  Plottier y Centenario hacia el W/NW (Neuquén prov.).

## 4 · Vialidad y accesos

| Eje | Recorrido | Notas |
|---|---|---|
| **Av. Argentina (N) / Av. Olascoaga (S)** | Eje monumental N–S de la ciudad; las **vías del BAP dividen** el tramo (Argentina al N, Olascoaga al S) | El eje organiza la numeración (cero en Argentina) y el centro cívico/comercial |
| **RN 22 (ex) / Av. del Trabajador** | Ingresa del O (Plottier–Centenario), atraviesa el Bajo al S de las vías y **cruza el Río Neuquén por el Puente Carretero** hacia Cipolletti y General Roca | Bajo = distrito comercial/mayorista; kilómetro 1286 aprox. en el puente |
| **Av. del Oeste** | Anillo oeste N–S (Acceso Oeste) | Arteria oeste de Gran Neuquén/Valentinas |
| **Av. Huillén** | N–S oeste-céntrica | Arterial oeste |
| **Av. Bouquet Roldán** | E–O norte del centro | Arterial oeste–este |
| **Vías F.C. Gral. Roca (BAP)** | Ramal Bahía Blanca–Neuquén; cruza la ciudad al S del centro; la **Estación Terminal** está en el eje (Olascoaga) | Servicio de cargas; pasajeros suspendidos hace años |
| **Acceso aeropuerto** | Derivación desde RN 22/Planas hacia el Aeropuerto Presidente Perón (7 km) | Valentina |

Salidas interurbanas: W → Centenario/Plottier (RN 22), NW → Zapala (RN 22/RN 40),
E → Cipolletti/General Roca (puente), N → zonas rurales/Añelo (vía local).

## 5 · Infraestructura mayor

| Infra | Detalle |
|---|---|
| **Aeropuerto Int. Presidente Perón (NQN/SAZN)** | ≈ 38.9514°S, 68.1406°O (7 km al O del centro); pista 09/27 de 2 570 m; vuelos nacionales e internacionales (Chile) |
| **Terminal de Ómnibus** | Planas (ex Ruta 22) y Solalique; ETON; 24 h; larga distancia y combis |
| **Estación Terminal (FCG Roca)** | Sobre el eje en las vías; histórica del BAP; cargas |
| **Hospital Castro Rendón** | Principal hospital público; al este del eje, N del Bajo |
| **UNCo – Centro Regional Comahue** | Universidad Nacional del Comahue; campus/facultades en barda N |
| **Puente Carretero** | 1937, arcos de hormigón, 464 m, 9 tramos; ver histórico |
| **Isla Jordán** | Isla en el cauce del Río Neuquén junto al puente |
| **Balneario Isla 132** | Sobre el Limay, al S del Parque Central |
| **Parque Central** | Ex aeródromo; gran parque del centro-sur |

## 6 · Transporte urbano — COLE (desde 1-feb-2023)

Sistema regulado por el municipio; concesionarias **Ko-Ko S.R.L.** y
**Expreso Tigre Iguazú S.A.** (grupo Vía Bariloche). 30 líneas urbanas, pago con
tarjeta SUBE; transbordo gratis dentro de los 60 min. Circulación aprox.
5:00–24:00. Frecuencias = faja central diurna en días hábiles.

| L | Recorrido | Frec. (min) | Obs. |
|---|---|---|---|
| 1 | Gran Neuquén Norte ↔ Área Centro Sur | 17 | |
| 2 | Sapere ↔ Área Centro Sur ↔ C. Industrial J. Nevares | 33 | |
| 3 | Rincón de Emilio ↔ La Sirena ↔ Río Grande | 55 | extiende a Parque Agreste |
| 4 | Villa Ceferino ↔ Área Centro Este ↔ La Sirena | 26 | extiende a Ciudad Deportiva |
| 5 | Gran Neuquén ↔ Confluencia (circular, horario) | 23 | ex 5A |
| 6 | Cuenca XV ↔ Área Centro Sur | 18 | 3 servicios de madrugada |
| 7 | Cuenca XV ↔ Área Centro Sur | 17 | |
| 8 | Gran Neuquén Sur ↔ Área Centro Sur | 14 | 4 servicios de madrugada |
| 9 | Cuenca XV ↔ Área Centro | 15 | |
| 10 | Gran Neuquén Sur ↔ Área Centro Este | 43 | |
| 11 | Gran Neuquén ↔ Área Centro Este | 30 | |
| 12 | Valentina Norte Rural (Los Hornos) ↔ Mariano Moreno | 12 | |
| 13 | Gran Neuquén Sur ↔ Santa Genoveva ↔ Mariano Moreno | 25 | |
| 14 | Valentina Norte Rural (Los Hornos) ↔ Río Grande | 45 | |
| 15 | Confluencia Rural ↔ Terrazas del Neuquén | 38 | |
| 16 | Esfuerzo (Cuenca XVI) ↔ Mariano Moreno | 40 | |
| 17 | Sapere ↔ Área Centro Este ↔ Altos del Limay | 19 | |
| 18 | Confluencia ↔ Área Centro Este | 27 | |
| 19 | Gran Neuquén ↔ Terrazas del Neuquén ↔ Área Centro Este | 43 | |
| 20 | Confluencia Rural ↔ Área Centro Este | 40 | |
| 21 | Valentina Sur Urbana ↔ Área Centro Este | 28 | ex 101 |
| 22 | Las Perlas ↔ Área Centro Este | 36 | ex 102 |
| 23 | C. Industrial J. Nevares ↔ Área Centro Sur | 25 | |
| 24 | Colonia Nueva Esperanza ↔ C. Industrial J. Nevares | 70 | |
| 25 | Cuenca XV ↔ Confluencia Rural (circular, antihorario) | 24 | |
| 26 | Colonia Nueva Esperanza ↔ Canal V | 50 | |
| 27 | Toma Norte 2 ↔ Área Centro Sur | 43 | |
| 28 | Valentina Norte Urbana ↔ Sapere | 60 | |
| 29 | Valentina Norte Rural ↔ Área Centro Sur | 73 | |
| 30 | 14 de Octubre ↔ Confluencia Urbana | 25 | |

### Interurbanas (complementan el sistema)

| Línea | Empresa | Recorrido |
|---|---|---|
| 50A / 50B | Autobuses Neuquén | Neuquén ↔ Plottier |
| 20 | Expreso Colonia | Neuquén ↔ Centenario |
| 914 | Expreso Tigre Iguazú | Neuquén ↔ Cipolletti / General Roca |

### Cole en cifras

30 líneas · ~759 km de recorrido total · ~1 732 servicios/día · ~100
servicios/hora (hora pico) — datos del estreno (feb-2023); verificar en la app
**COLE** / Moovit / sitio municipal para operación actual.

## 7 · Barrios (49 oficiales SITUN + Balcón de la Ciudad)

Agrupados por zona (centroides aproximados en `data/neighborhoods.json`):

- **Noroeste**: Cuenca XV, Esfuerzo (XVI), Ciudad Industrial Jaime de Nevares,
  Nueva Esperanza (colonia rural), Gran Neuquén Norte, Valentina Norte Rural/Urbana,
  Canal V, HIBEPA (Hi.Be.Pa), Terrazas del Neuquén.
- **Norte / barda**: Alta Barda, Rincón de Emilio, Bardas Soleadas, Cumelén,
  Balcón de la Ciudad, Huiliches, Provincias Unidas.
- **Centro**: Área Centro Oeste, Área Centro Este, Área Centro Sur, 14 de
  Octubre, Islas Malvinas, Villa Florencia, Unión de Mayo, Melipal.
- **Centro-este / río**: San Lorenzo Norte/Sur, Gregorio Álvarez, Villa Ceferino,
  Mariano Moreno, Villa Farrell, Confluencia Urbana/Rural.
- **Oeste**: Gran Neuquén Sur, Bouquet Roldán, Santa Genoveva, Militar,
  El Progreso, Sapere (Aníbal Sapere), Valentin Sur Rural/Urbana.
- **Suroeste / Limay**: La Sirena, Río Grande, Villa María, Don Bosco II/III,
  Manuel Belgrano, Altos del Limay, Limay, Barrio Nuevo.

## 8 · Landmarks (coordenadas en `data/pois.json`)

1 Monumento a San Martín (Argentina y Roca) · 2 Terminal de Ómnibus ·
3 Estación FCG Roca · 4 Puente Carretero · 5 Aeropuerto (NQN) ·
6 Municipalidad · 7 Hospital Castro Rendón · 8 Parque Central ·
9 Balneario Isla 132 · 10 Isla Jordán · 11 UNCo Comahue ·
12 Ciudad Deportiva · 13 Tribunales / Ciudad Judicial.

## 9 · Verificación pendiente (para v1.1)

- Frecuencias y recorridos COLE contra la app oficial (feb-2023 → hoy).
- Posición exacta de: Municipalidad, Hospital, UNCo, Ciudad Deportiva,
  Tribunales, Isla Jordán (todos `approx`).
- Límite exacto del ejido urbano y denominación actual del Balcón de la Ciudad.
- Altitud SRTM de la barda para el terreno 3D (hoy: perfil estilizado).

## Fuentes

- Río geométrico: OSM vía SpocWiki (CC BY-SA 3.0) — `data/geo/`.
- Wikipedia: Anexo:Transporte urbano (COLE) · Ruta_Nacional_22_(Argentina) ·
  Anexo:Barrios · Aeropuerto_Internacional_Presidente_Perón · Neuquén (ciudad).
- neuquencapital.gov.ar — Puente Carretero; callejero SITUN.
- neuquennews.com.ar (119.º aniversario Av. Argentina) · neuquenalinstante.com.ar ·
  rionegro.com.ar · masneuquen.com · kupi.com · omnilineas.com.ar ·
  terminaldeomnibus-neuquen.com · skyvector.com (SAZN) · moovitapp.com.
- Mapas Wikimedia Commons "Barrios de la ciudad de Neuquén" (SITUN).
