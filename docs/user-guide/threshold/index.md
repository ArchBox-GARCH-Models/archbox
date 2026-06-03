---
title: Threshold/STAR Models
description: "Modelos Threshold e Smooth Transition Autoregressive — TAR, SETAR, LSTAR, ESTAR e testes de linearidade."
---

# Threshold/STAR Models

Modelos threshold e STAR (Smooth Transition Autoregressive) capturam **nao-linearidades deterministicas** em series temporais. Diferentemente dos modelos [regime-switching](../regime-switching/index.md) (transicao estocastica via cadeia de Markov), aqui a transicao entre regimes e **determinada por uma variavel observavel** — tipicamente um lag da propria serie.

A ideia fundamental e que a dinamica de uma serie temporal pode mudar dependendo de uma condicao observavel: se a taxa de juros excede um limiar, se o PIB esta acima ou abaixo de uma tendencia, ou se a taxa de cambio se desvia da paridade. Esses modelos foram introduzidos por **Tong (1978)** para o caso de transicao abrupta (TAR) e generalizados por **Terasvirta (1994)** para transicao suave (STAR).

## Nao-Linearidade Deterministica vs. Estocastica

A distincao central entre modelos threshold/STAR e modelos regime-switching e o **mecanismo de transicao**:

| Aspecto | Threshold/STAR | [Regime-Switching](../regime-switching/index.md) |
|---------|---------------|------------------------------------------------|
| Mecanismo de transicao | Variavel observavel $z_t$ | Cadeia de Markov latente $s_t$ |
| Natureza | Deterministica | Estocastica |
| Regime atual | Conhecido (dado $z_t$) | Probabilistico (inferido) |
| Velocidade de transicao | Abrupta (TAR) ou suave (STAR) | Instantanea (Markov) |
| Previsibilidade | Regime e funcao de observaveis | Regime e inferido ex post |
| Uso tipico | Assimetrias ciclicas, bandas | Crises, mudancas estruturais |

!!! warning "Quando usar threshold vs. regime-switching"
    Se voce acredita que a mudanca de regime e desencadeada por uma variavel observavel (ex: taxa de juros cruza um limiar), use modelos threshold/STAR. Se a mudanca e governada por um processo latente nao observavel (ex: transicao expansao/recessao), use [regime-switching](../regime-switching/index.md).

## Modelos Disponiveis

| Modelo | Classe | Transicao | Caracteristica Principal | Referencia |
|--------|--------|-----------|-------------------------|------------|
| [TAR](tar.md) | `TAR` | Indicadora $I(z_t > c)$ | Transicao abrupta, variavel threshold externa | Tong (1978) |
| [SETAR](setar.md) | `SETAR` | Indicadora $I(y_{t-d} > c)$ | Self-exciting, delay automatico | Tong & Lim (1980) |
| [LSTAR](lstar.md) | `LSTAR` | Logistica $G(z_t; \gamma, c)$ | Transicao suave assimetrica | Terasvirta (1994) |
| [ESTAR](estar.md) | `ESTAR` | Exponencial $G(z_t; \gamma, c)$ | Transicao suave simetrica | Terasvirta (1994) |

## Funcoes de Transicao

O elemento que diferencia cada modelo e a **funcao de transicao** $G(z_t)$ que governa a passagem entre regimes. Todos os modelos compartilham a forma geral:

$$y_t = \boldsymbol{\phi}_1' \mathbf{x}_t \cdot (1 - G(z_t)) + \boldsymbol{\phi}_2' \mathbf{x}_t \cdot G(z_t) + \epsilon_t$$

onde $\mathbf{x}_t = (1, y_{t-1}, \ldots, y_{t-p})'$ e o vetor de regressores e $G(z_t) \in [0, 1]$ e a funcao de transicao.

### Indicadora (TAR/SETAR)

$$G(z_t; c) = I(z_t > c) = \begin{cases} 0 & \text{se } z_t \leq c \\ 1 & \text{se } z_t > c \end{cases}$$

Transicao **abrupta**: a serie esta inteiramente em um regime ou outro, sem estados intermediarios.

### Logistica (LSTAR)

$$G(z_t; \gamma, c) = \frac{1}{1 + \exp(-\gamma(z_t - c))}$$

Transicao **suave e assimetrica**: o comportamento acima e abaixo de $c$ pode ser qualitativamente diferente. Quando $\gamma \to \infty$, converge para a funcao indicadora (TAR). Quando $\gamma \to 0$, converge para o modelo linear.

### Exponencial (ESTAR)

$$G(z_t; \gamma, c) = 1 - \exp(-\gamma(z_t - c)^2)$$

Transicao **suave e simetrica**: $G(c - \delta) = G(c + \delta)$ para todo $\delta$. Os desvios simetricos em relacao a $c$ produzem a mesma transicao, independentemente da direcao.

```python
import numpy as np
from archbox.threshold import logistic_transition, exponential_transition
from archbox.threshold import plot_transition

# Visualizar funcoes de transicao
s = np.linspace(-3, 3, 500)
gamma_values = [0.5, 1.0, 5.0, 50.0]

# Transicao logistica (LSTAR)
fig_log = plot_transition(s, gamma_values, c=0.0, transition_type="logistic")

# Transicao exponencial (ESTAR)
fig_exp = plot_transition(s, gamma_values, c=0.0, transition_type="exponential")
```

## Quando Usar Cada Modelo

| Caracteristica dos Dados | Modelo Recomendado | Justificativa |
|--------------------------|-------------------|---------------|
| Assimetria direcional clara (ex: expansao vs. recessao) | [LSTAR](lstar.md) | Transicao assimetrica captura dinamicas diferentes acima/abaixo do threshold |
| Ajuste simetrico (ex: desvio da paridade de poder de compra) | [ESTAR](estar.md) | Transicao simetrica: desvios positivos e negativos tem o mesmo efeito |
| Threshold abrupto com variavel externa | [TAR](tar.md) | Transicao instantanea definida por variavel observavel |
| Threshold abrupto com lags da propria serie | [SETAR](setar.md) | Self-exciting: $z_t = y_{t-d}$ com selecao automatica de $d$ |
| Incerteza sobre o tipo de nao-linearidade | [Testes de Linearidade](linearity-tests.md) | Use testes estatisticos para guiar a escolha |

!!! tip "Fluxo de trabalho recomendado"
    1. Aplique o [teste LM de linearidade](linearity-tests.md) para verificar se ha nao-linearidade
    2. Se rejeitar linearidade, use o [teste de tipo de transicao](linearity-tests.md) para escolher entre LSTAR e ESTAR
    3. Estime o modelo escolhido e avalie diagnosticos
    4. Compare com alternativas via AIC/BIC

## Quick Example

```python
from archbox.threshold import SETAR, linearity_test

# Dados simulados com threshold
import numpy as np
rng = np.random.default_rng(42)
n = 500
y = np.zeros(n)
for t in range(1, n):
    if y[t-1] <= 0:
        y[t] = 0.5 + 0.3 * y[t-1] + rng.standard_normal() * 0.5
    else:
        y[t] = -0.2 + 0.8 * y[t-1] + rng.standard_normal() * 0.5

# 1. Testar linearidade
test = linearity_test(y, order=1, delay=1)
print(f"Teste LM: F = {test.statistic:.4f}, p = {test.pvalue:.4f}")

# 2. Estimar SETAR
model = SETAR(y, order=1, n_regimes=2)
results = model.fit()
print(results.summary())

# 3. Visualizar
results.plot_regimes()
```

## Hierarquia de Modelos

Os modelos threshold/STAR formam uma hierarquia natural baseada na funcao de transicao:

```
Modelo Linear (AR)
    │
    ├── TAR (transicao abrupta, z_t externo)
    │     └── SETAR (caso especial: z_t = y_{t-d})
    │
    └── STAR (transicao suave)
          ├── LSTAR (logistica, assimetrica)
          └── ESTAR (exponencial, simetrica)
```

- Quando $\gamma \to 0$ nos modelos STAR, recuperamos o modelo linear
- Quando $\gamma \to \infty$ no LSTAR, recuperamos o SETAR/TAR
- O SETAR e um caso especial do TAR com $z_t = y_{t-d}$

## See Also

- [TAR](tar.md) -- Threshold Autoregressive
- [SETAR](setar.md) -- Self-Exciting TAR
- [LSTAR](lstar.md) -- Logistic Smooth Transition AR
- [ESTAR](estar.md) -- Exponential Smooth Transition AR
- [Testes de Linearidade](linearity-tests.md) -- Tsay, Hansen, LM tests
- [Regime-Switching](../regime-switching/index.md) -- Alternativa com transicao estocastica
- [GARCH](../garch/index.md) -- Modelos de volatilidade condicional

## References

- Tong, H. (1978). On a Threshold Model. In *Pattern Recognition and Signal Processing*, Sijthoff & Noordhoff.
- Tong, H., & Lim, K. S. (1980). Threshold Autoregression, Limit Cycles and Cyclical Data. *Journal of the Royal Statistical Society, Series B*, 42(3), 245--292.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of Smooth Transition Autoregressive Models. *Journal of the American Statistical Association*, 89(425), 208--218.
- Hansen, B. E. (1996). Inference When a Nuisance Parameter Is Not Identified Under the Null Hypothesis. *Econometrica*, 64(2), 413--430.
- Luukkonen, R., Saikkonen, P., & Terasvirta, T. (1988). Testing Linearity Against Smooth Transition Autoregressive Models. *Biometrika*, 75(3), 491--499.
- van Dijk, D., Terasvirta, T., & Franses, P. H. (2002). Smooth Transition Autoregressive Models -- A Survey of Recent Developments. *Econometric Reviews*, 21(1), 1--47.
