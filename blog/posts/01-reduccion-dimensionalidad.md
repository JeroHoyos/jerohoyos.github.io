---
num: I
title: La Maldición<br>de la Dimensión
title_en: The Curse<br>of Dimension
kind: Reducción
kind_en: Reduction
date: Jun 17, 2026
date_en: Jun 17, 2026
booktitle: Reducción de Dimensionalidad
booktitle_en: Dimensionality Reduction
leather: oklch(0.30 0.06 264)
gilt: oklch(0.80 0.12 84)
emblem: overfit
formula: \Sigma\,v = \lambda\,v
teaser: Cuantas más dimensiones, más vacío el espacio. Aprende a **podar** el ruido antes de que te devore.
teaser_en: The more dimensions, the emptier the space. Learn to **prune** the noise before it devours you.
---

<!-- es -->

@chapter La maldición

@date 17 de junio, 2026

# LA MALDICIÓN<br>DE LA DIMENSIÓN

## introducción a la minería de datos · semana 7

Un solo *tweet* puede describirse con **más de 100 dimensiones**: datos básicos, del usuario, entidades, geolocalización, hashtags, urls, símbolos, media. Cuando el número de características crece frente al número de muestras, despierta la *maldición de la dimensionalidad*.

No es una sola cosa, sino un séquito de problemas que llegan juntos:

- **Espacio disperso** — a más dimensiones, las muestras quedan cada vez más lejos entre sí y los patrones se diluyen.
- **Visualización imposible** — vivimos en tres dimensiones; más de tres no se grafican directamente.
- **Sobreajuste** — modelos más complejos se ajustan al *ruido* en lugar del patrón real.
- **Costo computacional** — almacenar y procesar alta dimensión es caro; el tiempo de cómputo se dispara.
- **Algoritmos menos eficientes** — algunos se vuelven inviables o devuelven resultados subóptimos.

<!-- page -->

@fig curse | fig. 1 — los mismos 7 puntos, cada vez más solos a medida que sube la dimensión

Fíjate cómo los puntos, idénticos en número, pasan de amontonarse en la recta a perderse en el cubo: ese vacío creciente es la maldición en acción, y por eso las distancias dejan de significar lo que creemos.

> ⚠ Más columnas no es más información. A menudo es más ruido disfrazado de señal.

<!-- page -->

@chapter Dos caminos

# DOS<br>ESTRATEGIAS

Ante el exceso de datos hay dos rutas, y conviene no confundirlas:

- **Reducción de dimensionalidad** — *remover atributos que no aportan*. Aquí viven PCA, los pares correlacionados, la importancia de variables (VarImp) y el escalado multidimensional.
- **Reducción de datos** — *representar los datos con modelos más compactos*: histogramas, clustering, muestreo, agregación por *data cube*, discretización.

Este tomo recorre el primer camino con cinco estrategias: datos faltantes, varianza baja, pares correlacionados, importancia con Random Forest y PCA.

! La pregunta no es "¿puedo quitar esta columna?", sino "¿qué pierdo si la quito?".

<!-- page -->

@chapter El hilo: Iris

# EL DATASET<br>IRIS

## 150 flores, 4 medidas, 3 especies

Para ver cada técnica en acción usamos **Iris**: 150 observaciones, 4 variables numéricas (largo y ancho de sépalo y pétalo, en cm) y una clase de 3 especies — *setosa*, *versicolor* y *virginica*. Aunque Iris es un dataset limpio, **simularemos** condiciones reales (nulos, redundancia, sesgo) para cada método.

```python
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["species"] = iris.target          # 0,1,2
df.shape                             # (150, 5)  ·  4 features + clase
```

<!-- page -->

@chapter Filtros simples

# FILTROS<br>SIMPLES

Antes de invocar maquinaria pesada, hay dos guadañas baratas y efectivas.

**Eliminar columnas con datos faltantes.** Si una variable está dominada por vacíos y no se puede imputar de forma confiable, se elimina. La diapositiva sugiere conservar solo atributos con menos del 5–10% de nulos; en la práctica el umbral se ajusta al problema (en el laboratorio usamos 40%). Aplica a variables numéricas y categóricas.

```python
# elimina columnas con más del 40% de valores nulos
umbral = 0.40
df = df.loc[:, df.isnull().mean() < umbral]
```

<!-- page -->

# LOW VARIANCE<br>FILTER

La **varianza** mide cuánta información carga una columna. En el límite, una columna constante tiene **varianza 0** y no discrimina nada; se calcula la varianza de cada atributo y se eliminan los que caen bajo un umbral.

@math \operatorname{Var}[x] = p\,(1-p)\quad(\text{Bernoulli})

> ⚠ Normaliza los rangos **antes** de comparar varianzas: si no, el atributo con la escala más grande gana siempre, aunque no diga nada.

```python
from sklearn.preprocessing import MinMaxScaler

X = MinMaxScaler().fit_transform(df[iris.feature_names])   # 1º normalizar
var = pd.DataFrame(X, columns=iris.feature_names).var()
keep = var[var >= 0.01].index            # descarta varianza < umbral
```

<!-- page -->

@chapter Pares correlacionados

# PARES<br>CORRELACIONADOS

Dos atributos muy correlacionados introducen **redundancia**: dicen casi lo mismo y complican el modelado sin agregar información. Se puede eliminar uno del par sin perder casi nada. El procedimiento parte de la matriz de correlaciones:

- Se fija un umbral (por ejemplo, 0.7 en la diapositiva; 0.80 en el laboratorio).
- Se seleccionan los pares por encima del umbral.
- Entre los dos, se conserva el que en promedio esté **menos correlacionado** con el resto.

En las diapositivas, con umbral 0.7, *Cylinders* (corr. promedio 0.71) cae frente a *Displacement* (0.67). En Iris, *petal length* y *petal width* están correlacionadas a **≈ 0.96**: una de las dos sobra.

<!-- page -->

@fig corrmatrix | fig. 2 — la matriz de correlaciones: las casillas rojas intensas son pares redundantes

Cada celda es la correlación entre dos variables; cuanto más roja, más se parecen, y cuanto más azul, más se oponen. Los bloques intensos delatan información repetida que conviene podar dejando solo una del par. Sirve para variables continuas (Pearson) o discretas (χ² de Pearson).

```python
corr = df[iris.feature_names].corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape), 1).astype(bool))
# de cada par > umbral, descarta la de mayor correlación promedio
```

<!-- page -->

@chapter Prueba χ²

# χ² CONTRA<br>EL RUIDO

La prueba **chi-cuadrado** mide la *dependencia* entre cada variable y la clase. Conservamos las de estadístico más alto: las que más dependen de la respuesta. Las independientes son irrelevantes para la clasificación y se descartan. Aplica a variables **categóricas y no-negativas** (booleanos, frecuencias, conteos). El coeficiente **V de Cramér** la normaliza:

@math v = \sqrt{\dfrac{\chi^{2}}{n\,m}}\,,\quad 0 \le v \le 1

donde $n$ es la cantidad de instancias y $m = \min(\text{filas}-1,\ \text{columnas}-1)$.

```python
from sklearn.feature_selection import chi2, SelectKBest

# X: variables no negativas · y: la clase
chi_scores, p_values = chi2(X, y)
top = X.columns[SelectKBest(chi2, k=5).fit(X, y).get_support()]
```

<!-- page -->

@chapter Importancia (RF)

# VARIABLES<br>IMPORTANTES

Un **Random Forest** construye muchos **árboles de decisión**, cada uno sobre una muestra *bootstrap* (con reemplazo) y eligiendo en cada nodo un subconjunto aleatorio de características. Esa doble aleatoriedad hace los árboles menos correlacionados y al bosque más robusto. La predicción final es la clase con **más votos** (clasificación) o el **promedio** (regresión).

Un árbol parte de la **raíz** (toda la información), se ramifica en **nodos internos** (cada uno una pregunta sobre una variable) por **ramas** (sí/no) hasta las **hojas** (la decisión final).

<!-- page -->

@fig tree | fig. 3 — un árbol de decisión: preguntas en los nodos, decisiones en las hojas

El bosque hereda de los árboles una **medida interna de importancia**. La más común es el *Mean Decrease in Impurity*: cuánta impureza —**Gini** o **entropía** en clasificación, varianza en regresión— elimina cada variable, sumada y promediada sobre todos los nodos y árboles.

@math G = 1 - \sum_{i=1}^{k} p_i^{2}\qquad(\text{índice Gini})

<!-- page -->

@fig varimp | fig. 4 — el bosque mide cuánto aporta cada variable (Mean Decrease in Impurity)

Cada barra mide cuánta impureza elimina una variable a lo largo de todo el bosque. Las de arriba cargan casi toda la señal predictiva; las de abajo apenas mueven la aguja y suelen poder descartarse. En Iris, *petal length* y *petal width* dominan; *sepal width* casi no aporta.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(df[iris.feature_names], df["species"])
imp = pd.Series(rf.feature_importances_, index=iris.feature_names)
imp.sort_values(ascending=False)        # Mean Decrease in Impurity
```

<!-- page -->

@chapter Envolturas

# BACKWARD<br>& FORWARD

Los métodos *wrapper* usan un modelo de aprendizaje como juez del subconjunto de variables.

- **Eliminación Backward** — empieza con *todas* las variables y, en cada paso, quita la peor (la que menos aumenta el error al irse). Repite hasta que no quede nada que eliminar.
- **Selección Forward** — empieza con el conjunto *vacío*, agrega la mejor variable, y en cada paso suma la mejor de las restantes.

<!-- page -->

@fig featsel | fig. 5 — crecer desde el vacío (forward) o podar desde el todo (backward)

Arriba, *forward* arranca de cero y suma la mejor variable en cada paso; abajo, *backward* empieza con todas y descarta la peor. Dos caminos opuestos hacia el mismo subconjunto útil, pero pagan muchas evaluaciones del modelo por el camino.

> ⚠ Son **prohibitivamente lentos** en alta dimensión: muchísimas iteraciones. Úsalos solo después de podar con métodos más baratos.

<!-- page -->

@chapter PCA

# PCA: UN NUEVO<br>SISTEMA DE EJES

El **Análisis de Componentes Principales** busca una proyección que capture la mayor *varianza* posible, proyectando los datos en un espacio más pequeño definido por los **autovectores de la matriz de covarianza**. Es una **transformación**, no una selección: las componentes ya no son interpretables como las variables originales.

- **Estandarizar** (media 0, desviación 1) — PCA es sensible a la escala.
- Calcular la **matriz de covarianza**.
- Obtener **valores y vectores propios**: el vector marca la dirección; el valor, cuánta varianza hay en ella.
- **Ordenar y seleccionar** los primeros componentes.
- **Proyectar** los datos sobre ellos.

<!-- page -->

# PCA<br>PASO A PASO

Ejemplo de las diapositivas con dos variables estandarizadas. La matriz de covarianza y su descomposición:

@math \Sigma = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix},\quad \lambda_1 = 2,\ \lambda_2 = 0

@math v_1 = \begin{bmatrix} 0.707 \\ 0.707 \end{bmatrix},\quad v_2 = \begin{bmatrix} -0.707 \\ 0.707 \end{bmatrix}

El primer componente (mayor valor propio) define la proyección. Para cada muestra:

@math \mathrm{CP}_1 = 0.707\,X_1 + 0.707\,X_2,\quad \mathrm{CP}_2 = -0.707\,X_1 + 0.707\,X_2

<!-- page -->

@fig pca | fig. 6 — los datos giran hacia sus ejes de máxima varianza (PC1, PC2)

Los ejes originales *X*, *Y* no siguen la forma de la nube; **PC1** apunta hacia donde los datos más varían y **PC2** recoge lo que queda. Proyectar sobre PC1 conserva casi toda la información en una sola dimensión — el truco de la reducción.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

Xz = StandardScaler().fit_transform(df[iris.feature_names])
pca = PCA().fit(Xz)
pca.explained_variance_ratio_          # varianza por componente
```

<!-- page -->

@fig scree | fig. 7 — scree plot: con 2 componentes Iris ya explica ≈ 95.8% de la varianza

Las barras son la varianza que explica cada componente; la línea roja, la varianza **acumulada**. En Iris, PC1 explica ≈ 73% y PC2 ≈ 23%: con solo **2 de 4** componentes se conserva el 95.8% de la información, y los datos se vuelven graficables.

<!-- page -->

@chapter El veredicto

# EL<br>VEREDICTO

Ningún método gana siempre; depende del dato y del objetivo. Un resumen clásico (KDnuggets) sobre el mismo problema:

- **Baseline** (todas las variables) — 73% accuracy.
- **Missing Values Ratio** — 71% de reducción, 76%.
- **Low Variance Filter** — 73% de reducción, 82% (solo numéricas).
- **High Correlation Filter** — 74% de reducción, 79%.
- **Random Forest** — 86% de reducción, 76%.
- **PCA** — 62% de reducción, 74% (solo numéricas).

@math \text{Backward + missing} \to 99\%\ \text{de reducción},\ 94\%\quad(\text{pero brutalmente lento})

! Reducir dimensión no es tirar columnas al azar: es conservar la señal y dejar ir el ruido. Elige el ritual según tus datos.

! — fin del tomo I

<!-- en -->

@chapter The curse

@date June 17th, 2026

# THE CURSE<br>OF DIMENSION

## introduction to data mining · week 7

A single *tweet* can be described by **more than 100 dimensions**: basic data, user data, entities, geolocation, hashtags, urls, symbols, media. When the number of features grows against the number of samples, the *curse of dimensionality* awakens.

It isn't one thing but a retinue of troubles that arrive together:

- **Sparse space** — with more dimensions, samples drift further apart and patterns dissolve.
- **Impossible visualization** — we live in three dimensions; beyond three you can't plot directly.
- **Overfitting** — more complex models fit the *noise* instead of the real pattern.
- **Computational cost** — storing and processing high dimension is expensive; runtime blows up.
- **Less efficient algorithms** — some become infeasible or return suboptimal results.

<!-- page -->

@fig curse | fig. 1 — the same 7 points, lonelier as the dimension grows

Notice how the points — identical in number — go from huddling on the line to getting lost in the cube: that growing emptiness is the curse in action, and it's why distances stop meaning what we think.

> ⚠ More columns is not more information. Often it's more noise dressed up as signal.

<!-- page -->

@chapter Two roads

# TWO<br>STRATEGIES

Facing too much data there are two routes, and they shouldn't be confused:

- **Dimensionality reduction** — *remove attributes that don't help*. Here live PCA, correlated pairs, variable importance (VarImp) and multidimensional scaling.
- **Data reduction** — *represent the data with more compact models*: histograms, clustering, sampling, data-cube aggregation, discretization.

This tome walks the first road with five strategies: missing data, low variance, correlated pairs, Random Forest importance and PCA.

! The question isn't "can I drop this column?", but "what do I lose if I drop it?".

<!-- page -->

@chapter The thread: Iris

# THE IRIS<br>DATASET

## 150 flowers, 4 measures, 3 species

To see every technique in action we use **Iris**: 150 observations, 4 numeric variables (sepal and petal length and width, in cm) and a 3-class target — *setosa*, *versicolor* and *virginica*. Although Iris is a clean dataset, we'll **simulate** real conditions (nulls, redundancy, skew) for each method.

```python
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["species"] = iris.target          # 0,1,2
df.shape                             # (150, 5)  ·  4 features + class
```

<!-- page -->

@chapter Cheap filters

# CHEAP<br>FILTERS

Before summoning heavy machinery, there are two cheap and effective scythes.

**Drop columns with missing data.** If a variable is dominated by gaps and can't be reliably imputed, remove it. The slides suggest keeping only attributes with less than 5–10% missing; in practice the threshold fits the problem (in the lab we used 40%). It applies to numeric and categorical variables.

```python
# drop columns with more than 40% missing values
threshold = 0.40
df = df.loc[:, df.isnull().mean() < threshold]
```

<!-- page -->

# LOW VARIANCE<br>FILTER

**Variance** measures how much information a column carries. In the limit, a constant column has **variance 0** and discriminates nothing; compute each attribute's variance and drop those below a threshold.

@math \operatorname{Var}[x] = p\,(1-p)\quad(\text{Bernoulli})

> ⚠ Normalize the ranges **before** comparing variances: otherwise the attribute with the largest scale always wins, even when it says nothing.

```python
from sklearn.preprocessing import MinMaxScaler

X = MinMaxScaler().fit_transform(df[iris.feature_names])   # normalize first
var = pd.DataFrame(X, columns=iris.feature_names).var()
keep = var[var >= 0.01].index            # drop variance < threshold
```

<!-- page -->

@chapter Correlated pairs

# CORRELATED<br>PAIRS

Two highly correlated attributes introduce **redundancy**: they say almost the same thing and complicate modeling without adding information. You can drop one of the pair and lose almost nothing. The procedure starts from the correlation matrix:

- Set a threshold (e.g. 0.7 in the slides; 0.80 in the lab).
- Select the pairs above the threshold.
- Between the two, keep the one that is on average **less correlated** with the rest.

In the slides, with threshold 0.7, *Cylinders* (avg corr. 0.71) falls against *Displacement* (0.67). In Iris, *petal length* and *petal width* are correlated at **≈ 0.96**: one of them is redundant.

<!-- page -->

@fig corrmatrix | fig. 2 — the correlation matrix: deep-red cells are redundant pairs

Each cell is the correlation between two variables; the redder, the more alike, the bluer, the more opposed. Intense blocks reveal repeated information worth pruning by keeping just one of the pair. Works for continuous variables (Pearson) or discrete ones (Pearson's χ²).

```python
corr = df[iris.feature_names].corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape), 1).astype(bool))
# of each pair > threshold, drop the one with higher average correlation
```

<!-- page -->

@chapter The χ² test

# χ² AGAINST<br>THE NOISE

The **chi-squared** test measures the *dependence* between each variable and the class. We keep the highest-statistic ones: those that most depend on the response. Independent ones are irrelevant for classification and get discarded. It applies to **categorical, non-negative** variables (booleans, frequencies, counts). **Cramér's V** normalizes it:

@math v = \sqrt{\dfrac{\chi^{2}}{n\,m}}\,,\quad 0 \le v \le 1

where $n$ is the number of instances and $m = \min(\text{rows}-1,\ \text{columns}-1)$.

```python
from sklearn.feature_selection import chi2, SelectKBest

# X: non-negative features · y: the class
chi_scores, p_values = chi2(X, y)
top = X.columns[SelectKBest(chi2, k=5).fit(X, y).get_support()]
```

<!-- page -->

@chapter Importance (RF)

# IMPORTANT<br>VARIABLES

A **Random Forest** builds many **decision trees**, each on a *bootstrap* sample (with replacement) and choosing a random subset of features at each node. That double randomness makes the trees less correlated and the forest more robust. The final prediction is the class with **most votes** (classification) or the **average** (regression).

A tree starts at the **root** (all the information), branches into **internal nodes** (each a question about a variable) through **branches** (yes/no) down to the **leaves** (the final decision).

<!-- page -->

@fig tree | fig. 3 — a decision tree: questions at the nodes, decisions at the leaves

The forest inherits an **internal importance measure** from its trees. The most common is *Mean Decrease in Impurity*: how much impurity —**Gini** or **entropy** in classification, variance in regression— each variable removes, summed and averaged over every node and tree.

@math G = 1 - \sum_{i=1}^{k} p_i^{2}\qquad(\text{Gini index})

<!-- page -->

@fig varimp | fig. 4 — the forest measures how much each variable contributes (Mean Decrease in Impurity)

Each bar measures how much impurity a variable removes across the whole forest. The top ones carry almost all the predictive signal; the bottom ones barely move the needle and can usually be dropped. In Iris, *petal length* and *petal width* dominate; *sepal width* barely contributes.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(df[iris.feature_names], df["species"])
imp = pd.Series(rf.feature_importances_, index=iris.feature_names)
imp.sort_values(ascending=False)        # Mean Decrease in Impurity
```

<!-- page -->

@chapter Wrappers

# BACKWARD<br>& FORWARD

*Wrapper* methods use a learning model as the judge of the variable subset.

- **Backward Elimination** — starts with *all* variables and, at each step, removes the worst one (the one that least increases the error when it leaves). Repeat until nothing is left to remove.
- **Forward Selection** — starts with the *empty* set, adds the best variable, and at each step adds the best of the remaining ones.

<!-- page -->

@fig featsel | fig. 5 — grow from the empty set (forward) or prune from the full set (backward)

Top: *forward* starts from scratch and adds the best variable at each step; bottom: *backward* starts with all and discards the worst. Two opposite roads toward the same useful subset, both paying with many model evaluations along the way.

> ⚠ They are **prohibitively slow** in high dimension: a huge number of iterations. Use them only after pruning with cheaper methods.

<!-- page -->

@chapter PCA

# PCA: A NEW<br>SET OF AXES

**Principal Component Analysis** looks for a projection that captures as much *variance* as possible, projecting the data into a smaller space defined by the **eigenvectors of the covariance matrix**. It's a **transformation**, not a selection: the components are no longer interpretable like the original variables.

- **Standardize** (mean 0, deviation 1) — PCA is scale-sensitive.
- Compute the **covariance matrix**.
- Get **eigenvalues and eigenvectors**: the vector marks the direction; the value, how much variance lies along it.
- **Sort and select** the first components.
- **Project** the data onto them.

<!-- page -->

# PCA<br>STEP BY STEP

The slides' example with two standardized variables. The covariance matrix and its decomposition:

@math \Sigma = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix},\quad \lambda_1 = 2,\ \lambda_2 = 0

@math v_1 = \begin{bmatrix} 0.707 \\ 0.707 \end{bmatrix},\quad v_2 = \begin{bmatrix} -0.707 \\ 0.707 \end{bmatrix}

The first component (largest eigenvalue) defines the projection. For each sample:

@math \mathrm{PC}_1 = 0.707\,X_1 + 0.707\,X_2,\quad \mathrm{PC}_2 = -0.707\,X_1 + 0.707\,X_2

<!-- page -->

@fig pca | fig. 6 — the data rotates toward its axes of maximum variance (PC1, PC2)

The original *X*, *Y* axes don't follow the cloud's shape; **PC1** points where the data varies most and **PC2** captures the rest. Projecting onto PC1 keeps almost all the information in a single dimension — the trick behind the reduction.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

Xz = StandardScaler().fit_transform(df[iris.feature_names])
pca = PCA().fit(Xz)
pca.explained_variance_ratio_          # variance per component
```

<!-- page -->

@fig scree | fig. 7 — scree plot: with 2 components Iris already explains ≈ 95.8% of the variance

The bars are the variance each component explains; the red line, the **cumulative** variance. In Iris, PC1 explains ≈ 73% and PC2 ≈ 23%: with just **2 of 4** components you keep 95.8% of the information, and the data becomes plottable.

<!-- page -->

@chapter The verdict

# THE<br>VERDICT

No method always wins; it depends on the data and the goal. A classic summary (KDnuggets) on the same problem:

- **Baseline** (all variables) — 73% accuracy.
- **Missing Values Ratio** — 71% reduction, 76%.
- **Low Variance Filter** — 73% reduction, 82% (numeric only).
- **High Correlation Filter** — 74% reduction, 79%.
- **Random Forest** — 86% reduction, 76%.
- **PCA** — 62% reduction, 74% (numeric only).

@math \text{Backward + missing} \to 99\%\ \text{reduction},\ 94\%\quad(\text{but brutally slow})

! Reducing dimension isn't dropping columns at random: it's keeping the signal and letting the noise go. Choose the ritual to fit your data.

! — end of tome I
