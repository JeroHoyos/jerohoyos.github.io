# jerohoyos.github.io

Sitio personal de Jerónimo Hoyos: [jerohoyos.github.io](https://jerohoyos.github.io). Portafolio bilingüe (ES/EN) con proyectos, arte y contacto.

Sitio estático generado con Python. Todo el contenido se edita en `generator/content.py` y el resultado queda en `docs/`, que es lo que publica GitHub Pages.

## Cómo actualizar

1. Editar `generator/content.py` (bio, proyectos, stack, arte, redes, etc.)
2. Correr `python build.py`
3. Commit y push a `main`

La primera vez: `pip install -r requirements.txt`

## Estructura

| Carpeta/archivo | Qué hace |
|---|---|
| `generator/content.py` | El único archivo que se edita: todo el contenido |
| `build.py` | Genera el sitio completo en `docs/` |
| `generator/` | Plantillas, estilos, scripts y SEO |
| `docs/` | Salida generada (no editar a mano) |
| `docs/dibujos/` | Imágenes de la sección de arte |

## Notas

- Casi todo el contenido tiene versión en español (`_ES`) y en inglés (`_EN`)
- Para previsualizar, abrir `docs/index.html` en el navegador después de correr `build.py`
