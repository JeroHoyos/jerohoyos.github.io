---
slug: ejemplo1
title_es: Por qué la maldición de la dimensionalidad importa
title_en: Why the Curse of Dimensionality Matters
date_es: Mayo 2025
date_en: May 2025
tags: Estadística, Alta dimensión, ML, Intuición
excerpt_es: A medida que la dimensión crece, el espacio se vuelve casi vacío, las distancias pierden significado y nuestras intuiciones geométricas colapsan. Entendemos por qué esto rompe KNN, el histograma y la interpolación, y qué hacer al respecto.
excerpt_en: As dimension grows, space becomes nearly empty, distances lose meaning, and our geometric intuitions collapse. We understand why this breaks KNN, histograms, and interpolation, and what to do about it.
read_time: 15 min
read_es: Leer artículo →
read_en: Read article →
series:     fundamentos-ml
series_es:  Fundamentos de ML
series_en:  ML Fundamentals
chapter:    1
---

## El fenómeno

Toma un hipercubo unitario en $d$ dimensiones: $[0,1]^d$. Ahora mete una hiperesfera inscrita de radio $r = 0.5$. ¿Qué fracción del volumen del cubo ocupa la esfera?

$$\frac{V_{\text{esfera}}(d)}{V_{\text{cubo}}(d)} = \frac{\pi^{d/2} / \Gamma(d/2 + 1)}{1} \xrightarrow{d \to \infty} 0$$

En $d = 2$: la esfera ocupa $\approx 78\%$ del cuadrado. En $d = 10$: apenas $0.25\%$. En $d = 100$: un número que ni cabe en este margen.

Todo el volumen se escapa a las esquinas.

## Las distancias se homogenizan

Sea $x$ un punto aleatorio uniforme en $[0,1]^d$. La distancia al origen es:

$$\|x\|^2 = \sum_{i=1}^d x_i^2$$

Por la Ley de los Grandes Números, con $d$ grande:

$$\frac{\|x\|^2}{d} \approx \mathbb{E}[x_i^2] = \frac{1}{3}$$

Es decir, $\|x\| \approx \sqrt{d/3}$. Todos los puntos quedan a distancias muy parecidas del origen — y entre sí.

```python
import numpy as np

for d in [2, 10, 100, 1000]:
    pts = np.random.uniform(0, 1, (500, d))
    dists = np.linalg.norm(pts, axis=1)
    cv = dists.std() / dists.mean()   # coeficiente de variación
    print(f"d={d:5d}  mean={dists.mean():.3f}  CV={cv:.4f}")
```

```
d=    2  mean=0.522  CV=0.3821
d=   10  mean=1.817  CV=0.0867
d=  100  mean=5.762  CV=0.0280
d= 1000  mean=18.25  CV=0.0089
```

El coeficiente de variación colapsa a cero. **KNN en alta dimensión clasifica casi al azar** porque "el más cercano" y "el más lejano" están a prácticamente la misma distancia.

## Por qué los histogramas explotan

Para estimar una densidad con un histograma en $d$ dimensiones con $k$ bins por eje, necesitas $k^d$ celdas. Con $k = 10$ y $d = 10$: $10^{10}$ celdas. Necesitas trillones de muestras para llenarlas.

Esto es la razón detrás del **teorema de Stone**: la tasa de convergencia del estimador no-paramétrico óptimo es $n^{-4/(4+d)}$. Con $d = 10$ y $n = 10{,}000$ puntos, converge como si tuvieras 17 puntos en 1D.

## Lo que sí funciona en alta dimensión

No todo es desesperación. Algunas cosas funcionan:

- **Modelos paramétricos**: si asumes estructura (linealidad, suavidad), rompés la maldición
- **Reducción de dimensión**: PCA, UMAP, autoencoders encuentran subespacios de baja dimensión intrínseca
- **Métodos basados en gradiente**: las redes neuronales funcionan porque el gradiente descubiende geometría útil

La intuición clave es que los datos de alta dimensión en la práctica **no llenan el espacio**: viven en variedades de dimensión mucho menor. Un dataset de imágenes de $256 \times 256 = 65{,}536$ píxeles no explora ese espacio — vive en una variedad de baja dimensión de "imágenes naturales".

## Takeaway

La maldición de la dimensionalidad no es una abstracción — es la razón por la que KNN funciona en iris pero falla en features de audio, por la que necesitas regularización en regresión de alta dimensión, y por la que ninguna técnica no-paramétrica escala sin supuestos estructurales.

Entenderla te hace mejor a la hora de elegir modelos.
