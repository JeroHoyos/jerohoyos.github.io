---
slug: estadistica-i-03
title_es: Estimación e Intervalos de Confianza
title_en: Estimation and Confidence Intervals
date_es: Mayo 2025
date_en: May 2025
tags: Estadística, Inferencia, Estimación, Intervalos
excerpt_es: Estimadores puntuales, propiedades deseables y cómo construir intervalos de confianza para la media y la proporción.
excerpt_en: Point estimators, desirable properties, and how to build confidence intervals for the mean and proportion.
read_time: 9 min
series: estadistica-i
series_es: Estadística I
series_en: Statistics I
chapter: 3
---

## Estimación puntual

Un **estimador** $\hat{\theta}$ es una función de la muestra que aproxima un parámetro desconocido $\theta$.

### Propiedades deseables

**Insesgadez:** $E[\hat{\theta}] = \theta$. El estimador no sobreestima ni subestima en promedio.

**Consistencia:** $\hat{\theta} \to \theta$ cuando $n \to \infty$. Con más datos, el estimador converge al valor real.

**Eficiencia:** Entre todos los estimadores insesgados, el eficiente tiene la menor varianza.

### Estimadores comunes

| Parámetro | Estimador | Insesgado |
|---|---|---|
| Media $\mu$ | $\bar{X} = \frac{1}{n}\sum X_i$ | Sí |
| Varianza $\sigma^2$ | $S^2 = \frac{1}{n-1}\sum(X_i - \bar{X})^2$ | Sí |
| Proporción $p$ | $\hat{p} = X/n$ | Sí |

La varianza muestral usa $n-1$ (corrección de Bessel) para ser insesgada.

## Distribución muestral de $\bar{X}$

Si $X_1, \ldots, X_n$ son i.i.d. con media $\mu$ y varianza $\sigma^2$, entonces:

$$\bar{X} \sim \mathcal{N}\!\left(\mu,\, \frac{\sigma^2}{n}\right) \quad \text{(para } n \text{ grande, por el TCL)}$$

El **error estándar** de $\bar{X}$ es $\text{SE} = \sigma/\sqrt{n}$.

## Intervalos de confianza para la media

Un intervalo de confianza al $(1-\alpha)\times 100\%$ es un rango que contiene al parámetro verdadero con esa probabilidad en muestreos repetidos.

### $\sigma$ conocida — distribución Normal

$$\bar{X} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$

donde $z_{\alpha/2}$ es el cuantil de la Normal estándar. Para el 95%: $z_{0.025} = 1.96$.

### $\sigma$ desconocida — distribución $t$

$$\bar{X} \pm t_{\alpha/2,\, n-1} \cdot \frac{S}{\sqrt{n}}$$

La distribución $t$ de Student con $n-1$ grados de libertad tiene colas más pesadas que la Normal. Cuando $n \geq 30$ la diferencia es pequeña.

```python
import numpy as np
from scipy import stats

data = [12.1, 11.8, 13.0, 12.5, 11.9, 12.7, 12.3]
n    = len(data)
xbar = np.mean(data)
s    = np.std(data, ddof=1)

# IC 95% con t de Student
t_crit = stats.t.ppf(0.975, df=n-1)
margin = t_crit * s / np.sqrt(n)

print(f"Media: {xbar:.3f}")
print(f"IC 95%: ({xbar - margin:.3f}, {xbar + margin:.3f})")
```

## Intervalo de confianza para una proporción

$$\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

Válido cuando $n\hat{p} \geq 5$ y $n(1-\hat{p}) \geq 5$.

```python
from statsmodels.stats.proportion import proportion_confint

# 45 éxitos en 120 ensayos
ic = proportion_confint(45, 120, alpha=0.05, method='normal')
print(f"IC 95%: {ic}")
```

## Tamaño de muestra

Para estimar $\mu$ con margen de error $E$ y confianza $(1-\alpha)$:

$$n = \left(\frac{z_{\alpha/2}\,\sigma}{E}\right)^2$$

Para estimar $p$ (sin conocimiento previo, usar $\hat{p} = 0.5$ es conservador):

$$n = \frac{z_{\alpha/2}^2\, \hat{p}(1-\hat{p})}{E^2}$$

<!-- EN -->

## Point Estimation

An **estimator** $\hat{\theta}$ is a function of the sample that approximates an unknown parameter $\theta$.

### Desirable properties

**Unbiasedness:** $E[\hat{\theta}] = \theta$. The estimator neither overestimates nor underestimates on average.

**Consistency:** $\hat{\theta} \to \theta$ as $n \to \infty$. With more data, the estimator converges to the true value.

**Efficiency:** Among all unbiased estimators, the efficient one has the smallest variance.

### Common estimators

| Parameter | Estimator | Unbiased |
|---|---|---|
| Mean $\mu$ | $\bar{X} = \frac{1}{n}\sum X_i$ | Yes |
| Variance $\sigma^2$ | $S^2 = \frac{1}{n-1}\sum(X_i - \bar{X})^2$ | Yes |
| Proportion $p$ | $\hat{p} = X/n$ | Yes |

The sample variance uses $n-1$ (Bessel's correction) to be unbiased.

## Sampling Distribution of $\bar{X}$

If $X_1, \ldots, X_n$ are i.i.d. with mean $\mu$ and variance $\sigma^2$, then:

$$\bar{X} \sim \mathcal{N}\!\left(\mu,\, \frac{\sigma^2}{n}\right) \quad \text{(for large } n \text{, by the CLT)}$$

The **standard error** of $\bar{X}$ is $\text{SE} = \sigma/\sqrt{n}$.

## Confidence Intervals for the Mean

A $(1-\alpha)\times 100\%$ confidence interval is a range that contains the true parameter with that probability over repeated sampling.

### Known $\sigma$ — Normal distribution

$$\bar{X} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$

where $z_{\alpha/2}$ is the quantile of the standard Normal. For 95%: $z_{0.025} = 1.96$.

### Unknown $\sigma$ — $t$ distribution

$$\bar{X} \pm t_{\alpha/2,\, n-1} \cdot \frac{S}{\sqrt{n}}$$

Student's $t$ distribution with $n-1$ degrees of freedom has heavier tails than the Normal. When $n \geq 30$ the difference is small.

```python
import numpy as np
from scipy import stats

data = [12.1, 11.8, 13.0, 12.5, 11.9, 12.7, 12.3]
n    = len(data)
xbar = np.mean(data)
s    = np.std(data, ddof=1)

# 95% CI with Student's t
t_crit = stats.t.ppf(0.975, df=n-1)
margin = t_crit * s / np.sqrt(n)

print(f"Mean: {xbar:.3f}")
print(f"95% CI: ({xbar - margin:.3f}, {xbar + margin:.3f})")
```

## Confidence Interval for a Proportion

$$\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

Valid when $n\hat{p} \geq 5$ and $n(1-\hat{p}) \geq 5$.

```python
from statsmodels.stats.proportion import proportion_confint

# 45 successes in 120 trials
ci = proportion_confint(45, 120, alpha=0.05, method='normal')
print(f"95% CI: {ci}")
```

## Sample Size

To estimate $\mu$ with margin of error $E$ and confidence $(1-\alpha)$:

$$n = \left(\frac{z_{\alpha/2}\,\sigma}{E}\right)^2$$

To estimate $p$ (without prior knowledge, use $\hat{p} = 0.5$ as a conservative choice):

$$n = \frac{z_{\alpha/2}^2\, \hat{p}(1-\hat{p})}{E^2}$$
