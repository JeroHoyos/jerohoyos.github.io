---
slug: ejemplo2
title_es: Gradient Descent desde cero
title_en: Gradient Descent from Scratch
date_es: Abril 2025
date_en: April 2025
tags: ML, Optimización, Python, Matemáticas
excerpt_es: Implementamos gradient descent y sus variantes (SGD, momentum, Adam) desde cero en NumPy. Entendemos la geometría detrás de cada paso y por qué Adam converge donde SGD se atasca.
excerpt_en: We implement gradient descent and its variants (SGD, momentum, Adam) from scratch in NumPy. We understand the geometry behind each step and why Adam converges where SGD gets stuck.
read_time: 12 min
read_es: Leer artículo →
read_en: Read article →
series:     fundamentos-ml
series_es:  Fundamentos de ML
series_en:  ML Fundamentals
chapter:    2
---

## El problema que resuelve

Entrenar una red neuronal es, en esencia, resolver un problema de minimización:

$$\theta^* = \arg\min_\theta \mathcal{L}(\theta)$$

donde $\mathcal{L}$ es la función de pérdida y $\theta$ son los parámetros del modelo. El gradiente nos dice en qué dirección *sube* la pérdida, así que nos movemos en la dirección opuesta.

## Gradient Descent básico

La actualización es simple:

$$\theta_{t+1} = \theta_t - \alpha \nabla_\theta \mathcal{L}(\theta_t)$$

donde $\alpha$ es el *learning rate*. En código:

```python
import numpy as np

def gradient_descent(grad_fn, theta_init, lr=0.01, n_steps=1000):
    theta = theta_init.copy()
    history = [theta.copy()]
    for _ in range(n_steps):
        grad = grad_fn(theta)
        theta -= lr * grad
        history.append(theta.copy())
    return theta, np.array(history)
```

El problema con GD puro es que usa **todos los datos** en cada paso — caro con datasets grandes.

## SGD con momentum

Stochastic Gradient Descent usa un mini-batch aleatorio en cada paso, introduciendo ruido pero siendo mucho más rápido. El momentum suaviza la trayectoria acumulando un promedio exponencial de gradientes pasados:

$$v_{t+1} = \beta v_t + (1 - \beta) \nabla \mathcal{L}$$
$$\theta_{t+1} = \theta_t - \alpha v_{t+1}$$

```python
def sgd_momentum(grad_fn, theta_init, lr=0.01, beta=0.9, n_steps=1000):
    theta = theta_init.copy()
    v = np.zeros_like(theta)
    for _ in range(n_steps):
        grad = grad_fn(theta)
        v = beta * v + (1 - beta) * grad
        theta -= lr * v
    return theta
```

Con $\beta = 0.9$, el gradiente de hace 10 pasos todavía contribuye con $0.9^{10} \approx 0.35$ del peso original.

## Adam: momento + escala adaptativa

Adam combina momentum con una escala adaptativa por parámetro. Mantiene dos momentos:

- **Primer momento** $m_t$: media exponencial de gradientes (dirección)
- **Segundo momento** $v_t$: media exponencial de gradientes al cuadrado (magnitud)

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$

Con corrección de sesgo (importante en los primeros pasos):

$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$

$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

```python
def adam(grad_fn, theta_init, lr=1e-3, beta1=0.9, beta2=0.999, eps=1e-8, n_steps=1000):
    theta = theta_init.copy()
    m = np.zeros_like(theta)
    v = np.zeros_like(theta)
    for t in range(1, n_steps + 1):
        g = grad_fn(theta)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g**2
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        theta -= lr * m_hat / (np.sqrt(v_hat) + eps)
    return theta
```

## ¿Cuándo usar qué?

| Optimizador | Cuándo usarlo |
|---|---|
| GD | Problemas pequeños, análisis teórico |
| SGD + momentum | Visión por computador, quieres control total |
| Adam | Default razonable para casi todo |
| AdaGrad | NLP con features esparsos |

## La intuición geométrica

Imagina la superficie de pérdida como un paisaje montañoso. GD básico da pasos iguales en todas las direcciones. Adam, en cambio, da pasos **grandes** en direcciones donde la pérdida varía poco (gradientes históricos pequeños) y **pequeños** donde varía mucho — se adapta a la geometría local.

Esto explica por qué Adam suele converger más rápido en práctica, aunque GD con buen learning rate puede generalizar mejor en algunos problemas de visión.
