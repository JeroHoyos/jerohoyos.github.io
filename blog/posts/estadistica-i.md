---
slug: estadistica-i-01
title_es: Probabilidad y Variables Aleatorias
title_en: Probability and Random Variables
date_es: Mayo 2025
date_en: May 2025
tags: Estadística, Probabilidad, Distribuciones
excerpt_es: Probabilidad, variables aleatorias y las distribuciones más importantes del curso.
excerpt_en: Probability, random variables, and the most important distributions of the course.
read_time: 8 min
series: estadistica-i
series_es: Estadística I
series_en: Statistics I
series_desc_es: Notas y apuntes del curso de Estadística I.
series_desc_en: Notes and summaries from the Statistics I course.
series_about_es: En esta serie cubrimos los conceptos esenciales de la estadística inferencial. Partimos de los axiomas de probabilidad y las variables aleatorias, exploramos las distribuciones más usadas —Normal, Binomial, Poisson y Exponencial— y terminamos con las herramientas de inferencia: estimación por intervalos y pruebas de hipótesis. || Cada capítulo es un resumen conciso pensado para repasar antes de un parcial, con las fórmulas clave y ejemplos en Python usando scipy y statsmodels.
series_about_en: This series covers the essential concepts of inferential statistics. We start from the axioms of probability and random variables, explore the most commonly used distributions —Normal, Binomial, Poisson, and Exponential— and finish with inference tools: interval estimation and hypothesis testing. || Each chapter is a concise summary designed for pre-exam review, with key formulas and Python examples using scipy and statsmodels.
chapter: 1
---

## Espacio muestral y probabilidad

Un **espacio muestral** $\Omega$ es el conjunto de todos los posibles resultados de un experimento aleatorio. Un **evento** $A$ es cualquier subconjunto de $\Omega$.

La probabilidad cumple tres axiomas (Kolmogorov):

1. $P(A) \geq 0$ para todo evento $A$
2. $P(\Omega) = 1$
3. Si $A \cap B = \emptyset$, entonces $P(A \cup B) = P(A) + P(B)$

### Probabilidad condicional

La probabilidad de $A$ dado que ocurrió $B$ es:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$$

Dos eventos son **independientes** si $P(A \cap B) = P(A) \cdot P(B)$.

## Variables aleatorias

Una variable aleatoria $X$ asigna un número real a cada resultado del espacio muestral.

- **Discreta**: toma valores contables. Su distribución se describe con una función de masa de probabilidad $p(x) = P(X = x)$.
- **Continua**: toma valores en un intervalo. Se describe con una función de densidad $f(x)$ donde $P(a \leq X \leq b) = \int_a^b f(x)\,dx$.

### Esperanza y varianza

$$E[X] = \sum_x x \cdot p(x) \qquad \text{(discreta)}$$

$$\text{Var}(X) = E[X^2] - (E[X])^2$$

## Distribución Normal

La distribución más importante del curso. $X \sim \mathcal{N}(\mu, \sigma^2)$ tiene densidad:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

Para calcular probabilidades se **estandariza**: $Z = \frac{X - \mu}{\sigma}$, donde $Z \sim \mathcal{N}(0,1)$.

En Python:

```python
from scipy import stats

mu, sigma = 5, 2
X = stats.norm(mu, sigma)

print(X.mean(), X.std())       # 5.0  2.0
print(X.pdf(5))                # densidad en x=5
print(X.cdf(7))                # P(X <= 7)
print(X.ppf(0.95))             # percentil 95
```

<!-- EN -->

## Sample Space and Probability

A **sample space** $\Omega$ is the set of all possible outcomes of a random experiment. An **event** $A$ is any subset of $\Omega$.

Probability satisfies three axioms (Kolmogorov):

1. $P(A) \geq 0$ for every event $A$
2. $P(\Omega) = 1$
3. If $A \cap B = \emptyset$, then $P(A \cup B) = P(A) + P(B)$

### Conditional Probability

The probability of $A$ given that $B$ occurred is:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$$

Two events are **independent** if $P(A \cap B) = P(A) \cdot P(B)$.

## Random Variables

A random variable $X$ assigns a real number to each outcome in the sample space.

- **Discrete**: takes countable values. Described by a probability mass function $p(x) = P(X = x)$.
- **Continuous**: takes values in an interval. Described by a density function $f(x)$ where $P(a \leq X \leq b) = \int_a^b f(x)\,dx$.

### Expected Value and Variance

$$E[X] = \sum_x x \cdot p(x) \qquad \text{(discrete)}$$

$$\text{Var}(X) = E[X^2] - (E[X])^2$$

## Normal Distribution

The most important distribution in the course. $X \sim \mathcal{N}(\mu, \sigma^2)$ has density:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

To compute probabilities, **standardize**: $Z = \frac{X - \mu}{\sigma}$, where $Z \sim \mathcal{N}(0,1)$.

In Python:

```python
from scipy import stats

mu, sigma = 5, 2
X = stats.norm(mu, sigma)

print(X.mean(), X.std())       # 5.0  2.0
print(X.pdf(5))                # density at x=5
print(X.cdf(7))                # P(X <= 7)
print(X.ppf(0.95))             # 95th percentile
```
