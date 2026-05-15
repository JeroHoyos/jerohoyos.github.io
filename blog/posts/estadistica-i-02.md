---
slug: estadistica-i-02
title_es: Distribuciones de Probabilidad
title_en: Probability Distributions
date_es: Mayo 2025
date_en: May 2025
tags: Estadística, Distribuciones, Binomial, Poisson
excerpt_es: Binomial, Poisson y exponencial — las distribuciones más usadas y cuándo aplicar cada una.
excerpt_en: Binomial, Poisson, and exponential — the most used distributions and when to apply each.
read_time: 10 min
series: estadistica-i
series_es: Estadística I
series_en: Statistics I
chapter: 2
---

## Distribución Binomial

Modela el número de éxitos en $n$ ensayos independientes, cada uno con probabilidad de éxito $p$.

$$X \sim \text{Bin}(n, p)$$

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \ldots, n$$

**Parámetros:**

- $E[X] = np$
- $\text{Var}(X) = np(1-p)$

### Cuándo usarla

- Número fijo de ensayos $n$
- Cada ensayo es independiente
- Solo dos resultados posibles (éxito / fracaso)
- $p$ constante en todos los ensayos

```python
from scipy.stats import binom

n, p = 10, 0.3
X = binom(n, p)

print(X.pmf(3))      # P(X = 3)
print(X.cdf(4))      # P(X <= 4)
print(X.mean())      # np = 3.0
print(X.std())       # sqrt(np(1-p))
```

## Distribución de Poisson

Modela el número de eventos que ocurren en un intervalo fijo de tiempo o espacio, con tasa promedio $\lambda$.

$$X \sim \text{Pois}(\lambda)$$

$$P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \ldots$$

**Parámetros:**

- $E[X] = \lambda$
- $\text{Var}(X) = \lambda$

La media y la varianza son iguales — una forma rápida de verificar si Poisson es adecuada.

### Aproximación Binomial → Poisson

Cuando $n$ es grande y $p$ es pequeña, $\text{Bin}(n, p) \approx \text{Pois}(\lambda)$ con $\lambda = np$.

```python
from scipy.stats import poisson

lam = 4.5
X = poisson(lam)

print(X.pmf(3))      # P(X = 3)
print(X.cdf(6))      # P(X <= 6)
print(X.mean())      # 4.5
```

## Distribución Exponencial

Modela el tiempo entre eventos de un proceso de Poisson. Si los eventos ocurren a tasa $\lambda$, el tiempo entre eventos es $\text{Exp}(\lambda)$.

$$f(x) = \lambda e^{-\lambda x}, \quad x \geq 0$$

$$F(x) = 1 - e^{-\lambda x}$$

**Parámetros:**

- $E[X] = \frac{1}{\lambda}$
- $\text{Var}(X) = \frac{1}{\lambda^2}$

### Propiedad de falta de memoria

$$P(X > s + t \mid X > s) = P(X > t)$$

El tiempo restante no depende del tiempo ya transcurrido — la distribución exponencial es la única continua con esta propiedad.

```python
from scipy.stats import expon

# tasa lambda = 2 (media = 1/2)
X = expon(scale=1/2)

print(X.pdf(1))      # densidad en x=1
print(X.cdf(1))      # P(X <= 1)
print(X.ppf(0.9))    # percentil 90
```

## Resumen comparativo

| Distribución | Soporte | $E[X]$ | $\text{Var}(X)$ | Uso típico |
|---|---|---|---|---|
| Binomial$(n,p)$ | $\{0,\ldots,n\}$ | $np$ | $np(1-p)$ | Conteo de éxitos en $n$ ensayos |
| Poisson$(\lambda)$ | $\{0,1,2,\ldots\}$ | $\lambda$ | $\lambda$ | Eventos raros en tiempo/espacio |
| Exponencial$(\lambda)$ | $[0,\infty)$ | $1/\lambda$ | $1/\lambda^2$ | Tiempo entre eventos |

<!-- EN -->

## Binomial Distribution

Models the number of successes in $n$ independent trials, each with success probability $p$.

$$X \sim \text{Bin}(n, p)$$

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \ldots, n$$

**Parameters:**

- $E[X] = np$
- $\text{Var}(X) = np(1-p)$

### When to use it

- Fixed number of trials $n$
- Each trial is independent
- Only two outcomes (success / failure)
- Constant $p$ across all trials

```python
from scipy.stats import binom

n, p = 10, 0.3
X = binom(n, p)

print(X.pmf(3))      # P(X = 3)
print(X.cdf(4))      # P(X <= 4)
print(X.mean())      # np = 3.0
print(X.std())       # sqrt(np(1-p))
```

## Poisson Distribution

Models the number of events occurring in a fixed interval of time or space, with average rate $\lambda$.

$$X \sim \text{Pois}(\lambda)$$

$$P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \ldots$$

**Parameters:**

- $E[X] = \lambda$
- $\text{Var}(X) = \lambda$

Mean and variance are equal — a quick check for whether Poisson is appropriate.

### Binomial → Poisson approximation

When $n$ is large and $p$ is small, $\text{Bin}(n, p) \approx \text{Pois}(\lambda)$ with $\lambda = np$.

```python
from scipy.stats import poisson

lam = 4.5
X = poisson(lam)

print(X.pmf(3))      # P(X = 3)
print(X.cdf(6))      # P(X <= 6)
print(X.mean())      # 4.5
```

## Exponential Distribution

Models the time between events in a Poisson process. If events occur at rate $\lambda$, the time between events is $\text{Exp}(\lambda)$.

$$f(x) = \lambda e^{-\lambda x}, \quad x \geq 0$$

$$F(x) = 1 - e^{-\lambda x}$$

**Parameters:**

- $E[X] = \frac{1}{\lambda}$
- $\text{Var}(X) = \frac{1}{\lambda^2}$

### Memoryless property

$$P(X > s + t \mid X > s) = P(X > t)$$

The remaining time does not depend on time already elapsed — the exponential is the only continuous distribution with this property.

```python
from scipy.stats import expon

# rate lambda = 2 (mean = 1/2)
X = expon(scale=1/2)

print(X.pdf(1))      # density at x=1
print(X.cdf(1))      # P(X <= 1)
print(X.ppf(0.9))    # 90th percentile
```

## Comparative Summary

| Distribution | Support | $E[X]$ | $\text{Var}(X)$ | Typical use |
|---|---|---|---|---|
| Binomial$(n,p)$ | $\{0,\ldots,n\}$ | $np$ | $np(1-p)$ | Count of successes in $n$ trials |
| Poisson$(\lambda)$ | $\{0,1,2,\ldots\}$ | $\lambda$ | $\lambda$ | Rare events in time/space |
| Exponential$(\lambda)$ | $[0,\infty)$ | $1/\lambda$ | $1/\lambda^2$ | Time between events |
