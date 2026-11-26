---
name: portada-blog
description: Diseña y genera la imagen de portada (PNG 1600×686, 21:9) de un post del blog de jerohoyos.github.io con el estilo de la web (papel sobre tinta, cuadrícula, Bebas Neue / DM Serif Display / Space Mono) y un motivo matemático o generativo que cuente de qué trata el post, y la conecta al post (posts/img/ + `cover:` en el front matter). Úsala siempre que pidan una portada, imagen de cabecera, cover, banner o miniatura para un post o artículo del blog, aunque no digan «portada» (p. ej. «hazle una imagen al post de Krylov», «el post nuevo no tiene cover», «ponle algo bonito arriba al post»). No es para el README de GitHub ni para imágenes dentro del texto.
---

# Portada de un post

Las portadas del blog viven en `posts/img/` y el post las enlaza con `cover: img/<archivo>.png` en su front matter. El editor (`npm run escribir`) solo permite **subir** una portada; esta skill es la forma de **crearla**. El resultado debe sentirse de la misma familia que las portadas animadas de los proyectos de la web: trazos claros sobre fondo casi negro, cuadrícula sutil, matemáticas o algoritmos dibujados con precisión, sin fotos ni ilustración genérica.

## Flujo

1. **Lee el post** (`posts/<slug>.md`): título, resumen, etiquetas y el cuerpo. La portada tiene que contar la idea central del post, así que busca el objeto matemático o el algoritmo que mejor la represente (ver «Ideas de motivo»). Si el post aún está vacío, usa el título y pregunta solo si no hay forma razonable de adivinar el tema.
2. **Copia la plantilla** `assets/plantilla.html` a la carpeta temporal de trabajo (scratchpad), no al repo, y edítala: cambia el motivo SVG/canvas y los textos. Mantén el lienzo de 1600×686 y la paleta.
3. **Renderiza**:
   ```bash
   node .claude/skills/portada-blog/scripts/render.mjs <ruta/portada.html> posts/img/<slug>-portada.png
   ```
   El script usa Chrome o Edge sin ventana, espera a que carguen las fuentes y deja un PNG de 1600×686.
4. **Mira el PNG** (ábrelo con la herramienta de lectura de imágenes) y corrige lo que se vea mal: texto cortado, motivo demasiado pequeño o recargado, contraste bajo. Itera hasta que se vea bien de verdad; normalmente basta con 1–2 vueltas.
5. **Conéctalo al post**: en el front matter pon `cover: img/<slug>-portada.png` (reemplaza un `cover:` anterior si existía). No toques nada más del post.
6. Cuenta en una línea qué motivo elegiste y por qué, y dónde quedó el archivo. No hagas commit salvo que te lo pidan.

## Estilo (por qué así)

La web es negra/papel con tipografía Bebas Neue (títulos), DM Serif Display (nombres) y Space Mono (texto). Las portadas de los proyectos son dibujos técnicos animados en papel sobre tinta. Una portada que respete eso hace que el blog parezca parte de la web y no un pegote.

- **Fondo** `#050505` con la cuadrícula de 16 px en `rgba(244,244,239,.08)` (ya viene en la plantilla).
- **Trazo y texto** en papel `#f4f4ef` con distintas opacidades (`.15`–`1`) para dar profundidad. Un solo color de acento como mucho, y solo si ayuda a leer el motivo: `#ffb35c` (ámbar) o `#d97757` (arcilla).
- **Motivo** grande, ocupando el 60–80 % del alto, preferentemente a la derecha o centrado; con aire alrededor.
- **Texto**: opcional y poco. Si lo hay, una etiqueta pequeña en Space Mono (p. ej. `softmax(QKᵀ/√d)`, `pos 128`, `k = 7`) como si fuera una anotación del dibujo, no el título del post: el título ya sale debajo de la portada en la web. Evita frases largas.
- **La portada se recorta**: en el inicio se ve a 21:9, pero en miniaturas a 16:9 (se recortan los lados) y en la lista a 120×68. Deja lo importante en el centro (los 1200 px centrales) y que se entienda pequeño.
- Nada de degradados de colores, emojis, fotos de stock ni «IA genérica» (cerebros brillantes, robots). Si dudas, más simple.

## Ideas de motivo

Elige según el tema; combina si el post toca varias cosas.

| Tema del post | Motivo |
| --- | --- |
| Transformers, atención | matriz de atención triangular (máscara causal) con celdas de distinta opacidad; arcos de atención entre palabras |
| Embeddings posicionales, Fourier | senos/cosenos de frecuencias distintas apilados; una línea vertical marcando una posición |
| Álgebra lineal, Krylov, autovectores | vectores que convergen (método de la potencia), matrices en mosaico, una transformación de una rejilla |
| GPU, CUDA, paralelismo | bloques/tiles de una matriz coloreados por hilo, warps como filas |
| Probabilidad, estadística | tabla de Galton con su campana, histograma que converge, nube de puntos con su regresión |
| Redes neuronales | capas de nodos con pesos como grosor de línea |
| Rust, sistemas, compiladores | grafo de dependencias, árbol sintáctico, memoria como celdas con punteros |
| Gráficos por computador | malla de triángulos (Delaunay), cubo en alambre, rayos |
| Charlas, comunidad | onda de voz/ecualizador, escenario minimalista con una diapositiva |
| Algoritmos | ordenamiento a medio terminar en barras, grafo con el camino más corto resaltado |

Calcula el dibujo con JavaScript en la plantilla (bucles, funciones reales) en vez de dibujar coordenadas a mano: queda más preciso y es más fácil de ajustar. Usa una semilla fija (`hash` de la plantilla) para que el resultado sea reproducible.

## Archivos

- `assets/plantilla.html`: lienzo 1600×686 con fondo, cuadrícula, fuentes y un `<svg>` donde dibujar con JS. Incluye un ejemplo (matriz de atención) para reemplazar.
- `scripts/render.mjs`: HTML → PNG con Chrome/Edge sin ventana. Opcional: `--w`, `--h`, `--espera <ms>`.
