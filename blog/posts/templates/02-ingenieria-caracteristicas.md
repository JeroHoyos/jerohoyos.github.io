---
num: II
title: La Alquimia<br>de los Datos
title_en: The Alchemy<br>of Data
kind: Ingeniería
kind_en: Engineering
date: Jun 17, 2026
date_en: Jun 17, 2026
booktitle: Ingeniería de Características
booktitle_en: Feature Engineering
leather: oklch(0.32 0.06 150)
gilt: oklch(0.80 0.12 84)
emblem: net
formula: z = \dfrac{x - \mu}{\sigma}
teaser: No siempre necesitas más datos: a veces necesitas **mejores** datos. Transmuta el espacio de características.
teaser_en: You don't always need more data: sometimes you need **better** data. Transmute the feature space.
---

<!-- es -->

@chapter Transmutar

@date 17 de junio, 2026

# LA ALQUIMIA<br>DE LOS DATOS

## transformar para que el modelo entienda

La **Ingeniería de Características** (*Feature Engineering*) mejora el rendimiento del modelado transformando el *feature space*. Dentro del proceso de descubrimiento de conocimiento (KDD) corresponde a la etapa de **Transformación de datos**, y casi todo proceso de preparación esconde alguna transformación. Tres familias de hechizos:

- **Normalización** — escalar variables a un rango común.
- **Discretización** — convertir variables continuas en categorías.
- **Recodificación** — convertir variables categóricas en numéricas.

! No siempre necesitas un modelo más grande. A veces necesitas características mejor forjadas.

<!-- page -->

@chapter Normalización

# NORMALIZAR<br>LA ESCALA

Normalizar **escala** los features numéricos a un rango más pequeño. Es clave cuando las unidades dificultan comparar variables, en métodos basados en **distancias** (vecinos más cercanos, clustering) y en gradiente descendente. Evita que los atributos de mayor magnitud pesen más solo por su escala. Cuatro métodos:

@math X_{mm} = \dfrac{X - \min(X)}{\max(X) - \min(X)}\quad[0,1]

@math z = \dfrac{X - \mu}{\sigma}\qquad X_{dec} = \dfrac{X}{10^{d}}\qquad X_{r} = \dfrac{X - Q_2}{Q_3 - Q_1}

donde $d$ es el número de dígitos del valor absoluto máximo, y el escalado **robusto** usa mediana ($Q_2$) e IQR para resistir outliers.

<!-- page -->

@fig scaling | fig. 1 — la misma forma, solo cambia el eje: original, Min-Max y Z-Score

La silueta del histograma no cambia: solo se reescala el eje. Con el *Sepal.Length* de Iris (min 4.3, max 7.9, media 5.843, sd 0.828), el valor más corto se mapea a 0 en Min-Max y a **−1.863** en Z-Score; el más largo, a 1 y a **2.484**.

```python
from sklearn.preprocessing import (MinMaxScaler, StandardScaler, RobustScaler)

col = df[["sepal length (cm)"]]
df["minmax"]  = MinMaxScaler().fit_transform(col)
df["zscore"]  = StandardScaler().fit_transform(col)
df["robusto"] = RobustScaler().fit_transform(col)   # mediana e IQR
```

<!-- page -->

@chapter Robustez

# ESCALADOS<br>ROBUSTOS

Si el dataset tiene muchos **valores atípicos**, escalar con media y varianza falla: ambos se dejan arrastrar por los outliers. La salida es usar estimadores **robustos** del centro y del rango —la **mediana** (o un percentil) y el **IQR**— en lugar de media y desviación.

@fig boxplot | fig. 2 — la mediana y el IQR resisten lo que la media no

La caja abarca el 50% central de los datos (de *Q1* a *Q3*) y la línea marca la mediana; los puntos sueltos son atípicos más allá de 1.5·IQR. Por eso mediana e IQR describen centro y dispersión sin dejarse arrastrar por los valores extremos.

<!-- page -->

@chapter Normalidad

# DOMAR<br>EL SESGO

A veces queremos acercar una variable a la normalidad. El sesgo se estima así:

@math \text{sesgo} = \dfrac{3\,(\text{media} - \text{mediana})}{\sigma}

- Si la **media > mediana**, hay sesgo a la **derecha** (sesgo +).
- Si la **media < mediana**, hay sesgo a la **izquierda** (sesgo −).

Para reducirlo aplicamos transformaciones según el caso: **raíz cuadrada**, **logaritmo** o **inversa de la raíz cuadrada**. Cada una comprime la cola larga de forma distinta ($y=x^2$ corrige sesgo a la izquierda; $y=\ln x$ y $y=1/x$, a la derecha).

<!-- page -->

@fig skew | fig. 3 — una cola larga a la derecha que el logaritmo endereza hacia la normalidad

La cola larga a la derecha empuja la media por encima de la mediana (sesgo positivo); el logaritmo comprime esa cola y devuelve una forma casi simétrica, mucho más amable para los modelos que asumen normalidad.

> ⚠ La transformación cambia la unidad de la variable. Recuerda interpretar los resultados en la escala correcta.

<!-- page -->

@chapter Discretización

# DE CONTINUO<br>A ETIQUETAS

**Discretizar** divide el rango de una variable continua en intervalos: pasamos de valores continuos a un número reducido de etiquetas. Simplifica la representación, ayuda a algoritmos que prefieren categorías y reduce el efecto de los outliers.

El **Binning** es *Top-Down* y se basa en un número fijo de *bins*:

- **Igual-Ancho** — intervalos del mismo tamaño sobre el rango (sencillo, pero deja bins vacíos con outliers).
- **Igual-Frecuencia** — la misma cantidad de observaciones por bin (respeta la densidad).
- **K-means** — busca la partición intuitivamente correcta.

Dentro de cada bin se reemplaza por la **media**, la **mediana** o una **etiqueta** entera. No usa la clase: es **no supervisado**.

<!-- page -->

@fig binning | fig. 4 — igual-ancho: el rango se parte en tres tramos y cada punto cae en uno

Cada punto cae en *Low*, *Mid* o *High* según su valor; los duplicados se apilan. Con *igual-ancho* los cortes son fijos sin mirar cuántos datos caen en cada tramo; con *igual-frecuencia*, cada bin recibe el mismo número de observaciones.

```python
from sklearn.preprocessing import KBinsDiscretizer

col = df[["petal length (cm)"]]
ancho = KBinsDiscretizer(3, encode="ordinal", strategy="uniform")   # igual ancho
freq  = KBinsDiscretizer(3, encode="ordinal", strategy="quantile")  # igual frecuencia
df["bin_ancho"] = ancho.fit_transform(col).astype(int)   # 0,1,2 → Bajo,Medio,Alto
```

<!-- page -->

# TOP-DOWN<br>VS BOTTOM-UP

Dos enfoques opuestos para definir los intervalos:

- **Top-Down** — parte del rango completo y lo divide en intervalos. Más sencillo y con control explícito del número de categorías, pero puede no capturar bien la estructura si los cortes no se ajustan.
- **Bottom-Up** — parte de los datos individuales y los agrupa según su distribución (patrones e intervalos naturales). Captura mejor la realidad y es flexible, pero más complejo y con un número variable de intervalos.

<!-- page -->

@chapter Otros binnings

# RANK, CUANTILES<br>Y FUNCIONES

Más formas no supervisadas de discretizar:

- **Rank** — el tamaño relativo de un valor frente a los demás. Ordenamos y asignamos la posición; los iguales reciben el mismo rango.
- **Cuantiles** — mediana, cuartiles, percentiles. Útiles, pero como el rank dependen de la lista.
- **Funciones matemáticas** — por ejemplo `FLOOR(LOG(X))`, eficaz para variables muy sesgadas como el ingreso.

@math \text{Rank}(\{1,1,1,1,1,2,2,11,11,12,12,44\}) = \{1,1,1,1,1,2,2,3,3,4,4,5\}

> ⚠ Rank y cuantiles dependen de la lista: un mismo valor puede tener rangos distintos en listas distintas.

<!-- page -->

@chapter Entropía

# DISCRETIZAR<br>CON ENTROPÍA

La discretización basada en **entropía** es *supervisada* y *Top-Down*: explora la distribución de la clase para elegir el **punto de corte**. La entropía mide la incertidumbre, y buscamos el corte que **maximiza la ganancia de información**:

@math H(Y) = -\sum_{i=1}^{k} p(C_i)\,\log_2 p(C_i)

@math H(Y\mid X,t) = P(X\le t)\,H(Y\mid X\le t) + P(X>t)\,H(Y\mid X>t)

@math \mathrm{IG} = H(Y) - H(Y\mid X,t)

<!-- page -->

@fig entropy | fig. 5 — el corte que parte las clases dejando cada lado lo más puro posible

Los círculos llenos son *Premium* y los vacíos *No Premium*; la línea roja punteada es el corte. **Ejemplo (Edad → Premium):** 8 clientes balanceados, $H(Y)=1$. Para el corte en 30 años, $H(Y\mid X\le 30)=0.918$ y $H(Y\mid X>30)=0.971$, así que la entropía total es $\tfrac{3}{8}\cdot0.918 + \tfrac{5}{8}\cdot0.971 \approx 0.953$. Gana el corte de menor entropía.

<!-- page -->

# ENTROPÍA:<br>O-RING

Segundo ejemplo de las diapositivas — discretizar *Temperature* para predecir *Failure* (7 fallos, 17 no):

@math H(\text{Failure}) = H(7,17) = 0.871

@math H(\text{Fail},\text{Temp}) = \tfrac{3}{24}\cdot 0 + \tfrac{21}{24}\cdot 0.7 = 0.615

@math \mathrm{GI} = 0.871 - 0.615 = 0.256

En el notebook automatizamos esto: buscamos a mano el corte de mayor IG, o entrenamos un árbol con `criterion="entropy"` y leemos sus umbrales.

```python
from sklearn.tree import DecisionTreeClassifier

arbol = DecisionTreeClassifier(criterion="entropy", max_leaf_nodes=4)
arbol.fit(df[["petal length (cm)"]], df["species"])
cortes = arbol.tree_.threshold[arbol.tree_.threshold != -2]   # puntos de corte
```

<!-- page -->

@chapter Recodificar

# DUMMY &<br>ONE-HOT

Algunos métodos —como la regresión— exigen **predictores numéricos**. Recodificamos los descriptores categóricos en variables **Dummy**, **Flags** o **One-Hot encoding**: una columna binaria por categoría. Con dos categorías basta un flag (`sex_flag = 0/1`); con N, una columna 0/1 por cada una.

<!-- page -->

@fig onehot | fig. 6 — una columna categórica estalla en una columna 0/1 por categoría

La columna *region* se reemplaza por una columna por categoría: un **1** marca la categoría presente y **0** el resto. Así un atributo de texto se vuelve numérico sin inventar un orden falso. En regresión se elimina **una** columna de referencia (`drop="first"`) para evitar multicolinealidad perfecta.

```python
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse_output=False, dtype=int)
dummies = ohe.fit_transform(df[["species_name"]])   # setosa, versicolor, virginica
# para regresión: OneHotEncoder(drop="first")  → evita multicolinealidad
```

<!-- page -->

@chapter Ñapa: Gini

# ÑAPA:<br>ÍNDICE GINI

En economía, el **índice de Gini** mide la desigualdad de una distribución (ingreso, riqueza) a partir de la curva de Lorenz. En árboles de decisión se reaprovecha para medir la **impureza** de un nodo:

@math G = 1 - \sum_{i=1}^{k} p_i^{2}

donde $p_i$ es la proporción de la clase $i$ en el nodo y $k$ el número de clases. Va de **0** (nodo perfectamente puro) a su máximo cuando las clases están repartidas por igual. El árbol busca la división que **minimiza** Gini, logrando nodos más puros y homogéneos.

<!-- page -->

@chapter Ñapa: WoE & IV

# WEIGHT OF<br>EVIDENCE

El **Information Value (IV)** es una métrica **supervisada** que mide el poder predictivo de una variable frente a un objetivo **binario**. Viene del *scoring* crediticio y se calcula desde el **Weight of Evidence (WoE)** de cada bin:

@math \text{WoE}_i = \ln\!\left(\dfrac{\%\,\text{eventos}_i}{\%\,\text{no eventos}_i}\right)

@math \mathrm{IV} = \sum_{i=1}^{k} \left(\%\,\text{eventos}_i - \%\,\text{no eventos}_i\right)\cdot \text{WoE}_i

Requisitos: objetivo binario (0/1), predictor **discretizado** en bins, y ningún bin con cero eventos (se usa suavizado).

<!-- page -->

@fig iv | fig. 7 — la escala de Information Value: de inútil a sospechoso

El IV traduce el poder predictivo a una escala intuitiva: **< 0.02** inútil, **0.02–0.1** débil, **0.1–0.3** medio, **0.3–0.5** fuerte y **> 0.5** sospechoso (posible *data leakage*). El WoE además **transforma** variables a una escala lineal con el log-odds, ideal para regresión logística, sin aumentar la dimensión como el one-hot.

```python
import numpy as np
ev, nev = df[t].sum() + 0.5, (1 - df[t]).sum() + 0.5
g = df.groupby(bin)[t].agg(e="sum", n="count")
woe = np.log((g.e/ev) / ((g.n - g.e)/nev))
iv  = (((g.e/ev) - ((g.n - g.e)/nev)) * woe).sum()
```

! Forjar características es mitad ciencia, mitad oficio. Mide siempre: una buena transformación se nota en el modelo, no en la intuición.

! — fin del tomo II

<!-- en -->

@chapter Transmute

@date June 17th, 2026

# THE ALCHEMY<br>OF DATA

## transform so the model understands

**Feature Engineering** improves modeling performance by transforming the *feature space*. Within the knowledge-discovery process (KDD) it is the **Data Transformation** stage, and almost every preparation step hides some transformation. Three families of spells:

- **Normalization** — scale variables to a common range.
- **Discretization** — turn continuous variables into categories.
- **Recoding** — turn categorical variables into numeric ones.

! You don't always need a bigger model. Sometimes you need better-forged features.

<!-- page -->

@chapter Normalization

# NORMALIZE<br>THE SCALE

Normalizing **scales** numeric features to a smaller range. It's key when units make variables hard to compare, in **distance-based** methods (nearest neighbors, clustering) and in gradient descent. It prevents larger-magnitude attributes from dominating just by scale. Four methods:

@math X_{mm} = \dfrac{X - \min(X)}{\max(X) - \min(X)}\quad[0,1]

@math z = \dfrac{X - \mu}{\sigma}\qquad X_{dec} = \dfrac{X}{10^{d}}\qquad X_{r} = \dfrac{X - Q_2}{Q_3 - Q_1}

where $d$ is the number of digits of the largest absolute value, and the **robust** scaler uses median ($Q_2$) and IQR to resist outliers.

<!-- page -->

@fig scaling | fig. 1 — the same shape, only the axis changes: original, Min-Max and Z-Score

The histogram's silhouette doesn't change: only the axis is rescaled. With Iris's *Sepal.Length* (min 4.3, max 7.9, mean 5.843, sd 0.828), the shortest value maps to 0 under Min-Max and **−1.863** under Z-Score; the longest, to 1 and **2.484**.

```python
from sklearn.preprocessing import (MinMaxScaler, StandardScaler, RobustScaler)

col = df[["sepal length (cm)"]]
df["minmax"]  = MinMaxScaler().fit_transform(col)
df["zscore"]  = StandardScaler().fit_transform(col)
df["robust"]  = RobustScaler().fit_transform(col)    # median and IQR
```

<!-- page -->

@chapter Robustness

# ROBUST<br>SCALING

If the dataset has many **outliers**, scaling with mean and variance fails: both get dragged by them. The way out is **robust** estimators of center and spread —the **median** (or a percentile) and the **IQR**— instead of mean and deviation.

@fig boxplot | fig. 2 — the median and IQR resist what the mean cannot

The box spans the central 50% of the data (from *Q1* to *Q3*) and the line marks the median; the loose dots are outliers beyond 1.5·IQR. That's why median and IQR describe center and spread without being dragged by extreme values.

<!-- page -->

@chapter Normality

# TAMING<br>THE SKEW

Sometimes we want to push a variable toward normality. Skew is estimated as:

@math \text{skew} = \dfrac{3\,(\text{mean} - \text{median})}{\sigma}

- If **mean > median**, there is **right** skew (skew +).
- If **mean < median**, there is **left** skew (skew −).

To reduce it we apply transformations to fit the case: **square root**, **logarithm** or **inverse square root**. Each compresses the long tail differently ($y=x^2$ fixes left skew; $y=\ln x$ and $y=1/x$, right skew).

<!-- page -->

@fig skew | fig. 3 — a long right tail that the logarithm straightens toward normality

The long right tail pushes the mean above the median (positive skew); the logarithm compresses that tail and returns an almost symmetric shape, far friendlier to models that assume normality.

> ⚠ The transformation changes the variable's unit. Remember to interpret results on the right scale.

<!-- page -->

@chapter Discretization

# FROM CONTINUOUS<br>TO LABELS

**Discretizing** splits the range of a continuous variable into intervals: continuous values become a small number of labels. It simplifies the representation, helps algorithms that prefer categories, and reduces the effect of outliers.

**Binning** is *Top-Down* and relies on a fixed number of *bins*:

- **Equal-Width** — equal-size intervals across the range (simple, but leaves empty bins with outliers).
- **Equal-Frequency** — the same number of observations per bin (respects density).
- **K-means** — finds the intuitively correct partition.

Inside each bin we replace by the **mean**, the **median**, or an integer **label**. It ignores the class: it's **unsupervised**.

<!-- page -->

@fig binning | fig. 4 — equal-width: the range splits into three bands and each point falls in one

Each point falls into *Low*, *Mid* or *High* by its value; duplicates stack up. With *equal-width* the cuts are fixed regardless of how many points land in each band; with *equal-frequency*, each bin gets the same number of observations.

```python
from sklearn.preprocessing import KBinsDiscretizer

col = df[["petal length (cm)"]]
width = KBinsDiscretizer(3, encode="ordinal", strategy="uniform")    # equal width
freq  = KBinsDiscretizer(3, encode="ordinal", strategy="quantile")   # equal frequency
df["bin_width"] = width.fit_transform(col).astype(int)   # 0,1,2 → Low,Mid,High
```

<!-- page -->

# TOP-DOWN<br>VS BOTTOM-UP

Two opposite approaches to defining the intervals:

- **Top-Down** — starts from the full range and splits it into intervals. Simpler, with explicit control over the number of categories, but may miss the structure if the cuts aren't well fitted.
- **Bottom-Up** — starts from individual data points and groups them by their distribution (natural patterns and intervals). It captures reality better and is flexible, but more complex and with a variable number of intervals.

<!-- page -->

@chapter Other binnings

# RANK, QUANTILES<br>AND FUNCTIONS

More unsupervised ways to discretize:

- **Rank** — the relative size of a value against the rest. We sort and assign the position; equal values get the same rank.
- **Quantiles** — median, quartiles, percentiles. Useful, but like rank they depend on the list.
- **Math functions** — for example `FLOOR(LOG(X))`, effective for heavily skewed variables like income.

@math \text{Rank}(\{1,1,1,1,1,2,2,11,11,12,12,44\}) = \{1,1,1,1,1,2,2,3,3,4,4,5\}

> ⚠ Rank and quantiles depend on the list: the same value can have different ranks in different lists.

<!-- page -->

@chapter Entropy

# DISCRETIZE<br>WITH ENTROPY

Entropy-based discretization is *supervised* and *Top-Down*: it explores the class distribution to choose the **split-point**. Entropy measures uncertainty, and we look for the cut that **maximizes information gain**:

@math H(Y) = -\sum_{i=1}^{k} p(C_i)\,\log_2 p(C_i)

@math H(Y\mid X,t) = P(X\le t)\,H(Y\mid X\le t) + P(X>t)\,H(Y\mid X>t)

@math \mathrm{IG} = H(Y) - H(Y\mid X,t)

<!-- page -->

@fig entropy | fig. 5 — the cut that splits the classes leaving each side as pure as possible

Filled circles are *Premium* and empty ones *Non-Premium*; the dotted red line is the cut. **Example (Age → Premium):** 8 balanced clients, $H(Y)=1$. For the cut at 30, $H(Y\mid X\le 30)=0.918$ and $H(Y\mid X>30)=0.971$, so the total entropy is $\tfrac{3}{8}\cdot0.918 + \tfrac{5}{8}\cdot0.971 \approx 0.953$. The lowest-entropy cut wins.

<!-- page -->

# ENTROPY:<br>O-RING

The slides' second example — discretize *Temperature* to predict *Failure* (7 failures, 17 not):

@math H(\text{Failure}) = H(7,17) = 0.871

@math H(\text{Fail},\text{Temp}) = \tfrac{3}{24}\cdot 0 + \tfrac{21}{24}\cdot 0.7 = 0.615

@math \mathrm{GI} = 0.871 - 0.615 = 0.256

In the notebook we automate this: search by hand for the highest-IG cut, or train a tree with `criterion="entropy"` and read its thresholds.

```python
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(criterion="entropy", max_leaf_nodes=4)
tree.fit(df[["petal length (cm)"]], df["species"])
cuts = tree.tree_.threshold[tree.tree_.threshold != -2]   # split-points
```

<!-- page -->

@chapter Recode

# DUMMY &<br>ONE-HOT

Some methods —like regression— require **numeric predictors**. We recode categorical descriptors into **Dummy**, **Flags** or **One-Hot encoding** variables: one binary column per category. Two categories need a single flag (`sex_flag = 0/1`); N categories, one 0/1 column each.

<!-- page -->

@fig onehot | fig. 6 — one categorical column explodes into a 0/1 column per category

The *region* column is replaced by one column per category: a **1** marks the present category and **0** the rest. A text attribute becomes numeric without inventing a false order. In regression you drop **one** reference column (`drop="first"`) to avoid perfect multicollinearity.

```python
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse_output=False, dtype=int)
dummies = ohe.fit_transform(df[["species_name"]])   # setosa, versicolor, virginica
# for regression: OneHotEncoder(drop="first")  → avoids multicollinearity
```

<!-- page -->

@chapter Bonus: Gini

# BONUS:<br>GINI INDEX

In economics, the **Gini index** measures the inequality of a distribution (income, wealth) from the Lorenz curve. In decision trees it's reused to measure a node's **impurity**:

@math G = 1 - \sum_{i=1}^{k} p_i^{2}

where $p_i$ is the proportion of class $i$ in the node and $k$ the number of classes. It ranges from **0** (a perfectly pure node) to its maximum when the classes are evenly split. The tree looks for the split that **minimizes** Gini, yielding purer, more homogeneous nodes.

<!-- page -->

@chapter Bonus: WoE & IV

# WEIGHT OF<br>EVIDENCE

The **Information Value (IV)** is a **supervised** metric of a variable's predictive power against a **binary** target. It comes from credit scoring and is computed from each bin's **Weight of Evidence (WoE)**:

@math \text{WoE}_i = \ln\!\left(\dfrac{\%\,\text{events}_i}{\%\,\text{non-events}_i}\right)

@math \mathrm{IV} = \sum_{i=1}^{k} \left(\%\,\text{events}_i - \%\,\text{non-events}_i\right)\cdot \text{WoE}_i

Requirements: a binary target (0/1), a predictor **discretized** into bins, and no bin with zero events (use smoothing).

<!-- page -->

@fig iv | fig. 7 — the Information Value scale: from useless to suspicious

IV maps predictive power to an intuitive scale: **< 0.02** useless, **0.02–0.1** weak, **0.1–0.3** medium, **0.3–0.5** strong and **> 0.5** suspicious (possible *data leakage*). WoE also **transforms** variables to a scale linear with the log-odds — ideal for logistic regression, without inflating dimensionality like one-hot.

```python
import numpy as np
ev, nev = df[t].sum() + 0.5, (1 - df[t]).sum() + 0.5
g = df.groupby(bin)[t].agg(e="sum", n="count")
woe = np.log((g.e/ev) / ((g.n - g.e)/nev))
iv  = (((g.e/ev) - ((g.n - g.e)/nev)) * woe).sum()
```

! Forging features is half science, half craft. Always measure: a good transformation shows up in the model, not in your intuition.

! — end of tome II
