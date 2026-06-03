---
title: "LSTAR"
description: "Logistic Smooth Transition Autoregressive model — transicao suave assimetrica com funcao logistica e parametro gamma."
---

# LSTAR (Logistic Smooth Transition AR)

!!! info "Quick Reference"
    **Class:** `archbox.threshold.LSTAR`
    **Import:** `from archbox.threshold import LSTAR`
    **R equivalent:** `tsDyn::lstar(y, m=p, d=d)`
    **Python equivalent:** Nao disponivel em pacotes padrao

## Overview

O modelo LSTAR (Logistic Smooth Transition Autoregressive), proposto por **Terasvirta (1994)**, generaliza o [TAR](tar.md)/[SETAR](setar.md) ao substituir a funcao de transicao abrupta (indicadora) por uma **funcao logistica suave**. A transicao entre regimes ocorre de forma gradual, controlada pelo parametro $\gamma$ (velocidade de transicao) e pelo limiar $c$ (localizacao).

O LSTAR e o modelo STAR mais utilizado na pratica porque:

- **Transicao suave**: captura mudancas graduais, mais realistas que transicoes abruptas
- **Assimetria**: comportamento diferente acima e abaixo do threshold (diferente do [ESTAR](estar.md))
- **Generalidade**: inclui o modelo linear ($\gamma \to 0$) e o TAR ($\gamma \to \infty$) como casos especiais
- **Ciclos assimetricos**: expansoes lentas e recessoes rapidas (ou vice-versa)

O LSTAR e adequado quando:

- **Ciclos economicos assimetricos**: expansao e recessao tem velocidades diferentes
- **Efeitos direcionais**: a resposta depende da direcao do choque (positivo vs. negativo)
- **Gradualismo**: a transicao entre regimes nao e instantanea
- **O teste de tipo de transicao sugere LSTAR** (ver [testes de linearidade](linearity-tests.md))

## Formulacao Matematica

### Modelo Geral

$$y_t = \boldsymbol{\phi}_1' \mathbf{x}_t \cdot (1 - G(z_t; \gamma, c)) + \boldsymbol{\phi}_2' \mathbf{x}_t \cdot G(z_t; \gamma, c) + \epsilon_t$$

onde $\mathbf{x}_t = (1, y_{t-1}, \ldots, y_{t-p})'$ e $z_t = y_{t-d}$.

### Funcao de Transicao Logistica

$$G(z_t; \gamma, c) = \frac{1}{1 + \exp(-\gamma(z_t - c))}$$

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\gamma$ | Velocidade de transicao | $\gamma > 0$ |
| $c$ | Localizacao do threshold | Percentis 15%--85% de $z_t$ |
| $\boldsymbol{\phi}_1$ | Parametros AR do regime 1 ($G \approx 0$) | -- |
| $\boldsymbol{\phi}_2$ | Parametros AR do regime 2 ($G \approx 1$) | -- |

### Propriedades de $G(z_t; \gamma, c)$

A funcao logistica tem propriedades cruciais para a interpretacao:

- **Midpoint**: $G(c; \gamma, c) = 0.5$ — no ponto $z_t = c$, os dois regimes contribuem igualmente
- **Monotonicidade**: $G$ e estritamente crescente em $z_t$ para $\gamma > 0$
- **Limites**:
    - $\gamma \to 0$: $G \to 0.5$ para todo $z_t$ $\Rightarrow$ modelo linear
    - $\gamma \to \infty$: $G \to I(z_t > c)$ $\Rightarrow$ modelo TAR/SETAR
- **Assimetria**: $G(c + \delta) \neq 1 - G(c - \delta)$ em termos de impacto no modelo (os regimes tem parametros diferentes)

### O Parametro $\gamma$: Velocidade de Transicao

O parametro $\gamma$ controla a **suavidade** da transicao:

| $\gamma$ | Transicao | Comportamento |
|----------|-----------|---------------|
| $\gamma < 1$ | Muito suave | Quase linear, regimes pouco diferenciados |
| $\gamma \approx 1$--$5$ | Moderada | Transicao gradual entre regimes |
| $\gamma \approx 5$--$20$ | Rapida | Transicao visivel em uma faixa estreita |
| $\gamma > 50$ | Quase abrupta | Aproxima-se do TAR |

!!! warning "Identificacao de gamma"
    Valores muito altos de $\gamma$ (> 100) indicam que a transicao e essencialmente abrupta. Nesse caso, um TAR/SETAR pode ser mais parcimonioso. Valores muito baixos (< 0.1) indicam que a nao-linearidade e fraca e o modelo linear pode ser suficiente.

### Estimacao: Grid Search + NLS

A estimacao do LSTAR segue um procedimento em dois estagios:

1. **Grid search** sobre $(\gamma, c)$ com OLS concentrado:
    - Para cada par $(\gamma_j, c_k)$, calcula $G(z_t; \gamma_j, c_k)$
    - Estima $\boldsymbol{\phi}_1, \boldsymbol{\phi}_2$ por OLS concentrado:

    $$\min_{\boldsymbol{\phi}_1, \boldsymbol{\phi}_2} \sum_t \left[ y_t - \boldsymbol{\phi}_1' \mathbf{x}_t (1 - G_t) - \boldsymbol{\phi}_2' \mathbf{x}_t G_t \right]^2$$

    - Seleciona $(\gamma^{(0)}, c^{(0)})$ com menor RSS

2. **Refinamento NLS** (Nelder-Mead) a partir dos valores iniciais:
    - Otimiza $\log(\gamma)$ e $c$ para garantir $\gamma > 0$
    - Concentra OLS em $(\boldsymbol{\phi}_1, \boldsymbol{\phi}_2)$ a cada avaliacao

## Quick Example

```python
import numpy as np
from archbox.threshold import LSTAR

# Dados simulados com transicao logistica
rng = np.random.default_rng(42)
n = 1000
y = np.zeros(n)
gamma_true, c_true = 5.0, 0.0

for t in range(1, n):
    s = y[t-1]
    G = 1 / (1 + np.exp(-gamma_true * (s - c_true)))
    y[t] = (0.5 + 0.3 * y[t-1]) * (1 - G) + (-0.2 + 0.8 * y[t-1]) * G
    y[t] += rng.standard_normal() * 0.5

# Estimar LSTAR
model = LSTAR(y, order=1, delay=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                                  Model: LSTAR
                           Observations: 999
                            AR Order (p): 1
                              Delay (d): 1
                     Number of Regimes: 2
                         Log-Likelihood: -698.4567
                                    AIC: 1408.9134
                                    BIC: 1438.3456
    ----------------------------------------------------------------------
                          Threshold (c): 0.012345
    ----------------------------------------------------------------------
    Transition Parameters:
                                 gamma: 4.987654
                                     c: 0.012345
    ----------------------------------------------------------------------
    regime_1:
                                 const: 0.498765
                                 phi_1: 0.301234
    regime_2:
                                 const: -0.198765
                                 phi_1: 0.799012
    ----------------------------------------------------------------------
    Variance per Regime:
                              regime_1: 0.251234
                              regime_2: 0.249876
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie temporal, shape (T,) |
| `order` | int | `1` | Ordem AR $p$ |
| `delay` | int | `1` | Delay $d$: $z_t = y_{t-d}$ |
| `gamma_grid` | int | `50` | Pontos no grid de $\gamma$ (log-espacados, 0.1 a 100) |
| `c_grid` | int | `50` | Pontos no grid de $c$ (percentis 15%--85%) |
| `refine` | bool | `True` | Refinar via NLS apos grid search |

### Parametros de `fit()`

O metodo `fit()` nao requer parametros adicionais. A estimacao e automatica via grid search + NLS.

### Exemplo: Ciclos Economicos Assimetricos

```python
import numpy as np
from archbox.threshold import LSTAR, linearity_test, transition_type_test

# Simular ciclos assimetricos
# Expansao lenta (regime 1) vs recessao rapida (regime 2)
rng = np.random.default_rng(123)
n = 800
y = np.zeros(n)
gamma_true, c_true = 3.0, 0.0

for t in range(1, n):
    s = y[t-1]
    G = 1 / (1 + np.exp(-gamma_true * (s - c_true)))
    # Regime 1 (G~0): expansao lenta, alta persistencia
    # Regime 2 (G~1): recessao rapida, baixa persistencia
    y[t] = (0.1 + 0.9 * y[t-1]) * (1 - G) + (-0.5 + 0.4 * y[t-1]) * G
    y[t] += rng.standard_normal() * 0.3

# 1. Teste de linearidade
test_lm = linearity_test(y, order=1, delay=1)
print(f"LM test: F = {test_lm.statistic:.4f}, p = {test_lm.pvalue:.4f}")

# 2. Teste de tipo de transicao (LSTAR vs ESTAR)
type_test = transition_type_test(y, order=1, delay=1)
print(f"Recomendacao: {type_test['recommended']}")
print(f"  p2={type_test['p2']:.4f}, p3={type_test['p3']:.4f}, "
      f"p4={type_test['p4']:.4f}")

# 3. Estimar LSTAR
model = LSTAR(y, order=1, delay=1)
results = model.fit()
print(results.summary())

# 4. Interpretar gamma
gamma_est = results.transition_params['gamma']
c_est = results.transition_params['c']
print(f"\nGamma estimado: {gamma_est:.4f}")
print(f"c estimado: {c_est:.4f}")
if gamma_est > 50:
    print("Transicao quase abrupta -> considere TAR/SETAR")
elif gamma_est < 0.5:
    print("Transicao muito suave -> modelo quase linear")
else:
    print("Transicao suave com velocidade moderada")

# 5. Visualizar
results.plot_regimes()
results.plot_transition()
```

### Visualizando a Funcao de Transicao Estimada

```python
import numpy as np
from archbox.threshold import logistic_transition, plot_transition

# Comparar transicao estimada com diferentes gammas
s_range = np.linspace(-3, 3, 500)
gamma_est = results.transition_params['gamma']
c_est = results.transition_params['c']

# Funcao de transicao estimada vs alternativas
fig = plot_transition(
    s_range,
    gamma_values=[0.5, gamma_est, 50.0],
    c=c_est,
    transition_type="logistic"
)
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros por regime (dict) |
| `results.threshold` | Threshold estimado $\hat{c}$ |
| `results.delay` | Delay $d$ |
| `results.transition_params` | `{'gamma': ..., 'c': ...}` |
| `results.params_regime1` | Coeficientes AR: regime 1, $G \approx 0$ (ndarray) |
| `results.params_regime2` | Coeficientes AR: regime 2, $G \approx 1$ (ndarray) |
| `results.transition_values` | $G(z_t; \hat{\gamma}, \hat{c})$ para cada $t$ (ndarray) |
| `results.resid` | Residuos (ndarray) |
| `results.sigma2` | Variancia por regime (dict) |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | AIC |
| `results.bic` | BIC |

| Metodo | Descricao |
|--------|-----------|
| `results.summary()` | Tabela formatada |
| `results.plot_regimes()` | Serie com coloracao de regimes |
| `results.plot_transition()` | Valores de $G(z_t)$ ao longo do tempo |
| `results.plot_phase_diagram()` | Diagrama de fase $y_t$ vs $y_{t-1}$ |
| `results.plot_fit()` | Observado vs ajustado |
| `results.forecast(horizon)` | Previsao $h$ passos a frente |

## Interpretacao

### Regimes no LSTAR

No LSTAR, os "regimes" nao sao discretos — sao um **continuo** entre dois extremos:

- **$G \approx 0$** (regime 1): predominam os parametros $\boldsymbol{\phi}_1$
- **$G \approx 0.5$** (transicao): mistura equilibrada dos dois conjuntos de parametros
- **$G \approx 1$** (regime 2): predominam os parametros $\boldsymbol{\phi}_2$

A observacao $t$ esta "mais no regime 1" ou "mais no regime 2" dependendo do valor de $G(z_t)$.

### Assimetria no LSTAR

A assimetria do LSTAR manifesta-se no fato de que o comportamento **acima** de $c$ e qualitativamente diferente do comportamento **abaixo** de $c$. Exemplos:

- **Ciclos economicos**: expansoes com alta persistencia ($\phi_{1,1} \approx 0.9$) e recessoes com reversao rapida ($\phi_{1,2} \approx 0.4$)
- **Taxa de juros**: ajuste assimetrico — subidas rapidas, descidas lentas
- **Volatilidade**: retornos negativos tem impacto diferente de retornos positivos

### LSTAR vs TAR: Quando a Suavidade Importa

```python
from archbox.threshold import LSTAR, SETAR

# Comparar LSTAR vs SETAR (TAR)
lstar = LSTAR(y, order=1, delay=1)
setar = SETAR(y, order=1, delay=1)

res_lstar = lstar.fit()
res_setar = setar.fit()

print(f"LSTAR: AIC={res_lstar.aic:.2f}, BIC={res_lstar.bic:.2f}")
print(f"SETAR: AIC={res_setar.aic:.2f}, BIC={res_setar.bic:.2f}")

gamma = res_lstar.transition_params['gamma']
if gamma > 50:
    print("Gamma alto -> SETAR pode ser mais parcimonioso")
else:
    print("Transicao suave -> LSTAR e mais adequado")
```

## Diagnosticos

```python
from archbox.threshold import LSTAR, linearity_test
import numpy as np

# 1. Teste de linearidade (pre-estimacao)
test = linearity_test(y, order=1, delay=1)
print(f"LM test: p = {test.pvalue:.4f}")

# 2. Qualidade do ajuste
results = LSTAR(y, order=1, delay=1).fit()
print(f"AIC: {results.aic:.4f}")
print(f"BIC: {results.bic:.4f}")
print(f"Variancia regime 1: {results.sigma2['regime_1']:.6f}")
print(f"Variancia regime 2: {results.sigma2['regime_2']:.6f}")

# 3. Proporcao em cada regime
g = results.transition_values
print(f"\nObs com G < 0.25 (forte regime 1): {(g < 0.25).sum()}")
print(f"Obs com 0.25 <= G <= 0.75 (transicao): {((g >= 0.25) & (g <= 0.75)).sum()}")
print(f"Obs com G > 0.75 (forte regime 2): {(g > 0.75).sum()}")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.threshold import LSTAR

    model = LSTAR(y, order=1, delay=1)
    results = model.fit()
    print(results.summary())
    results.plot_transition()
    ```

=== "R (tsDyn)"

    ```r
    library(tsDyn)

    # LSTAR com delay=1
    fit <- lstar(y, m = 1, d = 1)
    summary(fit)
    plot(fit)

    # Funcao de transicao
    plot(fit, which = "transition")
    ```

=== "R (smooth)"

    ```r
    library(smooth)

    # STAR com transicao logistica
    # (pacote tsDyn e mais direto para LSTAR)
    ```

| Funcionalidade | ArchBox | tsDyn (R) |
|---------------|---------|-----------|
| Especificacao | `LSTAR(y, order=1, delay=1)` | `lstar(y, m=1, d=1)` |
| Grid search | `gamma_grid=50, c_grid=50` | Automatico |
| Refinamento | `refine=True` | Automatico |
| Gamma | `results.transition_params['gamma']` | `coef(fit)['gamma']` |
| Transicao | `results.transition_values` | `regime(fit)` |
| Plot | `results.plot_transition()` | `plot(fit, which="transition")` |

## References

- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of Smooth Transition Autoregressive Models. *Journal of the American Statistical Association*, 89(425), 208--218.
- van Dijk, D., Terasvirta, T., & Franses, P. H. (2002). Smooth Transition Autoregressive Models -- A Survey of Recent Developments. *Econometric Reviews*, 21(1), 1--47.
- Luukkonen, R., Saikkonen, P., & Terasvirta, T. (1988). Testing Linearity Against Smooth Transition Autoregressive Models. *Biometrika*, 75(3), 491--499.
- Granger, C. W. J., & Terasvirta, T. (1993). *Modelling Nonlinear Economic Relationships*. Oxford University Press.

## See Also

- [Threshold/STAR: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [ESTAR](estar.md) -- Alternativa com transicao simetrica
- [TAR](tar.md) -- Transicao abrupta (caso limite do LSTAR)
- [SETAR](setar.md) -- TAR self-exciting
- [Testes de Linearidade](linearity-tests.md) -- Teste LM e selecao LSTAR vs ESTAR
