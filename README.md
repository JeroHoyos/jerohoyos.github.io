# jerohoyos.github.io

Mi sitio personal: [jerohoyos.github.io](https://jerohoyos.github.io)

Es un sitio estático escrito a mano, sin paso de build. GitHub Pages sirve la carpeta `docs/`:

| Archivo | Qué hay |
| --- | --- |
| `docs/index.html` | Todo el contenido. Cada texto traducible aparece dos veces, con `lang="en"` y `lang="es"`. |
| `docs/static/style.css` | Estilos (paleta, widgets, posts, responsive). |
| `docs/static/main.js` | Selector ES/EN, lightbox, copiar email y las animaciones en canvas: juego de la vida, atractor de Lorenz, tabla de Galton, algoritmos de ordenamiento, tabla de multiplicar modular, triangulación de Delaunay y las portadas animadas de los proyectos. |
| `docs/static/oneko.js` | El gato que persigue el cursor ([oneko.js](https://github.com/adryd325/oneko.js)). |

Para verlo localmente basta con abrir `docs/index.html` en el navegador.

GitHub Pages cachea los archivos 10 minutos. Al cambiar `style.css`, `main.js` o una imagen, sube el `?v=` con el que se enlazan en `index.html` para que nadie vea el HTML nuevo con el CSS/JS viejo.
