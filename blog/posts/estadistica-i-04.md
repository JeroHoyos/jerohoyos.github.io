---
slug: estadistica-i-04
title_es: Pruebas de Hipótesis
title_en: Hypothesis Testing
date_es: Mayo 2025
date_en: May 2025
tags: Estadística, Hipótesis, p-valor, Error Tipo I
excerpt_es: Cómo plantear y resolver pruebas de hipótesis para la media y la proporción, con p-valor y regiones de rechazo.
excerpt_en: How to set up and solve hypothesis tests for the mean and proportion, with p-value and rejection regions.
read_time: 11 min
series: estadistica-i
series_es: Estadística I
series_en: Statistics I
chapter: 4
---

## Estructura de una prueba de hipótesis

Toda prueba sigue el mismo esquema:

1. **Plantear hipótesis:** $H_0$ (nula) vs. $H_1$ (alternativa)
2. **Elegir nivel de significancia** $\alpha$ (típicamente 0.05 o 0.01)
3. **Calcular el estadístico de prueba** a partir de los datos
4. **Tomar decisión:** rechazar $H_0$ si el estadístico cae en la región de rechazo, o si el $p$-valor $< \alpha$

### Tipos de error

| | $H_0$ verdadera | $H_0$ falsa |
|---|---|---|
| **No rechazar $H_0$** | ✓ Correcto | Error Tipo II ($\beta$) |
| **Rechazar $H_0$** | Error Tipo I ($\alpha$) | ✓ Correcto (Potencia) |

El **nivel de significancia** $\alpha$ es la probabilidad máxima de cometer un error tipo I que estamos dispuestos a tolerar.

## Prueba para la media ($\sigma$ conocida)

$$H_0: \mu = \mu_0 \quad \text{vs.} \quad H_1: \mu \neq \mu_0$$

**Estadístico:**

$$Z = \frac{\bar{X} - \mu_0}{\sigma / \sqrt{n}} \sim \mathcal{N}(0, 1) \text{ bajo } H_0$$

**Regla de decisión (bilateral):** rechazar $H_0$ si $|Z| > z_{\alpha/2}$.

## Prueba $t$ para la media ($\sigma$ desconocida)

$$T = \frac{\bar{X} - \mu_0}{S / \sqrt{n}} \sim t_{n-1} \text{ bajo } H_0$$

```python
from scipy import stats
import numpy as np

data = [9.8, 10.2, 9.5, 10.1, 10.4, 9.9, 10.3]
mu0  = 10.0

t_stat, p_valor = stats.ttest_1samp(data, mu0)

print(f"t = {t_stat:.4f}")
print(f"p-valor = {p_valor:.4f}")

alpha = 0.05
if p_valor < alpha:
    print("Rechazar H₀")
else:
    print("No rechazar H₀")
```

## El $p$-valor

El $p$-valor es la probabilidad de obtener un resultado tan extremo o más que el observado, **asumiendo que $H_0$ es verdadera**.

$$p\text{-valor} = P(\text{estadístico} \geq |t_{\text{obs}}| \mid H_0)$$

- $p < \alpha$: evidencia suficiente para rechazar $H_0$
- $p \geq \alpha$: no hay evidencia suficiente para rechazar $H_0$

> Un $p$-valor no mide la probabilidad de que $H_0$ sea verdadera — mide qué tan compatible son los datos con $H_0$.

## Prueba para una proporción

$$H_0: p = p_0 \quad \text{vs.} \quad H_1: p \neq p_0$$

$$Z = \frac{\hat{p} - p_0}{\sqrt{p_0(1-p_0)/n}}$$

```python
from statsmodels.stats.proportion import proportions_ztest

# 38 éxitos en 100 ensayos, H0: p = 0.5
count = 38
nobs  = 100
p0    = 0.5

z_stat, p_valor = proportions_ztest(count, nobs, value=p0)
print(f"z = {z_stat:.4f}, p-valor = {p_valor:.4f}")
```

## Prueba $t$ de dos muestras

Compara las medias de dos grupos independientes:

$$H_0: \mu_1 = \mu_2 \quad \text{vs.} \quad H_1: \mu_1 \neq \mu_2$$

```python
from scipy import stats

grupo_a = [85, 88, 90, 84, 87, 92]
grupo_b = [78, 82, 80, 75, 83, 79]

t_stat, p_valor = stats.ttest_ind(grupo_a, grupo_b)
print(f"t = {t_stat:.4f}, p-valor = {p_valor:.4f}")
```

## Relación con intervalos de confianza

Un IC al $(1-\alpha)\times 100\%$ y una prueba bilateral al nivel $\alpha$ son equivalentes:

- Si $\mu_0$ **no cae** dentro del IC → se rechaza $H_0$
- Si $\mu_0$ **cae** dentro del IC → no se rechaza $H_0$

<!-- EN -->

## Structure of a Hypothesis Test

Every test follows the same scheme:

1. **State hypotheses:** $H_0$ (null) vs. $H_1$ (alternative)
2. **Choose significance level** $\alpha$ (typically 0.05 or 0.01)
3. **Compute the test statistic** from the data
4. **Make a decision:** reject $H_0$ if the statistic falls in the rejection region, or if the $p$-value $< \alpha$

### Types of error

| | $H_0$ true | $H_0$ false |
|---|---|---|
| **Fail to reject $H_0$** | ✓ Correct | Type II error ($\beta$) |
| **Reject $H_0$** | Type I error ($\alpha$) | ✓ Correct (Power) |

The **significance level** $\alpha$ is the maximum probability of a Type I error we are willing to tolerate.

## Test for the Mean (known $\sigma$)

$$H_0: \mu = \mu_0 \quad \text{vs.} \quad H_1: \mu \neq \mu_0$$

**Test statistic:**

$$Z = \frac{\bar{X} - \mu_0}{\sigma / \sqrt{n}} \sim \mathcal{N}(0, 1) \text{ under } H_0$$

**Decision rule (two-sided):** reject $H_0$ if $|Z| > z_{\alpha/2}$.

## $t$-test for the Mean (unknown $\sigma$)

$$T = \frac{\bar{X} - \mu_0}{S / \sqrt{n}} \sim t_{n-1} \text{ under } H_0$$

```python
from scipy import stats
import numpy as np

data = [9.8, 10.2, 9.5, 10.1, 10.4, 9.9, 10.3]
mu0  = 10.0

t_stat, p_value = stats.ttest_1samp(data, mu0)

print(f"t = {t_stat:.4f}")
print(f"p-value = {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print("Reject H₀")
else:
    print("Fail to reject H₀")
```

## The $p$-value

The $p$-value is the probability of obtaining a result as extreme or more extreme than the one observed, **assuming $H_0$ is true**.

$$p\text{-value} = P(\text{statistic} \geq |t_{\text{obs}}| \mid H_0)$$

- $p < \alpha$: sufficient evidence to reject $H_0$
- $p \geq \alpha$: insufficient evidence to reject $H_0$

> A $p$-value does not measure the probability that $H_0$ is true — it measures how compatible the data are with $H_0$.

## Test for a Proportion

$$H_0: p = p_0 \quad \text{vs.} \quad H_1: p \neq p_0$$

$$Z = \frac{\hat{p} - p_0}{\sqrt{p_0(1-p_0)/n}}$$

```python
from statsmodels.stats.proportion import proportions_ztest

# 38 successes in 100 trials, H0: p = 0.5
count = 38
nobs  = 100
p0    = 0.5

z_stat, p_value = proportions_ztest(count, nobs, value=p0)
print(f"z = {z_stat:.4f}, p-value = {p_value:.4f}")
```

## Two-Sample $t$-test

Compares the means of two independent groups:

$$H_0: \mu_1 = \mu_2 \quad \text{vs.} \quad H_1: \mu_1 \neq \mu_2$$

```python
from scipy import stats

group_a = [85, 88, 90, 84, 87, 92]
group_b = [78, 82, 80, 75, 83, 79]

t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t = {t_stat:.4f}, p-value = {p_value:.4f}")
```

## Relationship with Confidence Intervals

A $(1-\alpha)\times 100\%$ CI and a two-sided test at level $\alpha$ are equivalent:

- If $\mu_0$ **falls outside** the CI → reject $H_0$
- If $\mu_0$ **falls inside** the CI → fail to reject $H_0$
