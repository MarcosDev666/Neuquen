# 01 · Cómo instalar mapas en Proton Bus Simulator (Android)

## Antes de empezar

Proton Bus Simulator (en adelante PBSU) guarda los mods dentro de la carpeta
de datos de la app:

```
<Almacenamiento interno>/Android/data/com.viamep.protonbussimulator/files/
├── buses/
└── maps/        ← acá van los mapas
```

(Algunas variantes del juego usan `com.viamep.pbsu` u otro `com.viamep.*`;
buscá `Android/data/com.viamep*`. En PC: `Documentos/Proton Bus Mods/maps`.)

## Método recomendado (juego actualizado): instalador "+"

1. Copiá el archivo `.zip` del mapa a una carpeta **dentro de `Download`**
   (por ejemplo `Download/Mods/NeuquenCapital_PBSU_v1.0.0.zip`).
   ⚠️ Android 11+ no deja que las apps lean directamente
   `Android/data/...`. Por eso el instalador interno pide el zip desde
   `Download` o `Documentos`. Además, **no descomprimas el zip a mano**:
   el juego lo extrae él solo en el destino correcto.
2. Abrí PBSU → pestaña **Mapas**.
3. Tocá el botón **"+"** (arriba o abajo a la derecha, según versión).
4. Navegá hasta el zip y seleccionalo.
5. Esperá unos segundos/minutos según el tamaño. El juego instala y muestra
   el mapa en la lista de mapas (ícono y nombre).
6. Seleccionalo y tocá **Jugar**.
7. Para desinstalarlo: botón **"−"** en el mismo selector de mapas
   (elimina la copia dentro del juego, no el zip de `Download`).

Requisitos y problemas frecuentes:

- **El juego no detecta el zip**: que sea `.zip` plano (sin contraseña),
  no `.rar` / `.7z`. Si está en rar, extraelo a una carpeta temporal y volvé
  a comprimir esa carpeta como `.zip`.
- **No aparece `Android/data/com.viamep.protonbussimulator`**: la carpeta se
  crea al primer arranque del juego. Abrí y cerrá PBSU una vez.
- **Android 11+**: si no podés abrir la carpeta con el gestor de archivos,
  usá el método "+" (no hace falta tocar `Android/data`). Con
  "Archivos de Google" o "Material Files" sí podés navegar
  `Android/data` con permisos especiales.
- **Versión del juego**: instalá el OBB de la versión correcta desde la
  ficha de Google Play; sin él el juego no arranca.
- **Espacio**: el instalador descomprime; dejá libre al menos 3× el tamaño
  del zip.

## Método alternativo (Android ≤ 10 o PC): extracción manual

1. Descomprimí el zip preservando la carpeta raíz del mod.
2. Copiá la carpeta `NeuquenCapital/` dentro de
   `.../com.viamep.protonbussimulator/files/maps/`
2. En PC: `.../Documentos/Proton Bus Mods/maps/NeuquenCapital/`.
3. Reiniciá el juego y buscá "Neuquén Capital" en la lista de mapas.

## Cómo instalar ESTE paquete (la fuente del proyecto)

`dist/NeuquenCapital_PBSU_v1.0.0.zip` **no** es (todavía) un binario de mapa
del motor. Usalo así:

- Como **referencia de diseño**: abrí los PNG de `mapas/` y el SVG en
  cualquier visor; imprimilos si vas a armar el mapa con teclado y mouse.
- Como **fuente 3D**: importá `3d/NeuquenCapital.obj` en Blender
  (Archivo → Importar → Wavefront (.obj)). Encontrarás: terreno, agua,
  vías, parque, 144 edificios, landmarks. Usalo como base de bloques;
  reemplazá materiales y LOD según `docs/04-DISENO-EN-JUEGO.md`.
- Para el paso final en PBS: `docs/02-FORMATO-PBS-Y-PBS-MAP-STUDIO.md` y
  `docs/04-DISENO-EN-JUEGO.md`.

## Si ya tenés un mapa de Neuquén en el juego y querés actualizarlo

Reemplazá los archivos del mapa dentro de `maps/<carpeta-del-mapa>/` por los
que generes con las herramientas. Hacé un respaldo del original antes.

## Desinstalar

- Método "+": botón "−" en el selector de mapas.
- Manual: borrá la carpeta `maps/NeuquenCapital/` dentro de la carpeta de
  datos del juego. En Android 11+, puede requerir el mismo gestor con permisos.

## Canales de soporte de la comunidad

- protonbusmods.com (catálogo y guías de instalación PBSU)
- YouTube: "Bus Simulation Channel" (gameplays y tutoriales de mods)
- Fandom: protonbussimulator.fandom.com (wikis y tutoriales comunitarios)
