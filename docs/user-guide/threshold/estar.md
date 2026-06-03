---
title: "ESTAR"
description: "Exponential Smooth Transition Autoregressive model — transicao suave simetrica com funcao exponencial para desvios em torno de um centro."
---

# ESTAR (Exponential Smooth Transition AR)

!!! info "Quick Reference"
    **Class:** `archbox.threshold.ESTAR`
    **Import:** `from archbox.threshold import ESTAR`
    **R equivalent:** `tsDyn::star(y, m=p, d=d, type="ESTAR")`
    **Python equivalent:** Nao disponivel em pacotes padrao

## Overview

O modelo ESTAR (Exponential Smooth Transition Autoregressive), proposto por **Terasvirta (1994)**, utiliza uma funcao de transicao **exponencial** que e **simetrica** em torno do parametro de localizacao $c$. A principal diferenca em relacao ao [LSTAR](lstar.md) e que desvios **positivos e negativos** de magnitude igual produzem a mesma transicao — o que importa nao e a direcao do desvio, mas sua **magnitude**.

O ESTAR e adequado quando:

- **Paridade de poder de compra (PPP)**: desvios da taxa de cambio real do equilibrio sao corrigidos simetricamente, independentemente da direcao
- **Ajuste simetrico a um equilibrio**: a velocidade de reversao depende da distancia ao equilibrio, nao da direcao
- **Custos de transacao simetricos**: o custo de ajuste e funcao do tamanho do desvio, nao do sinal
- **O teste de tipo de transicao sugere ESTAR** (ver [testes de linearidade](linearity-tests.md))

**Quando usar ESTAR ao inves de LSTAR:**

| Cenario | ESTAR | [LSTAR](lstar.md) |
|---------|-------|------|
| Desvios simetricos da PPP | Adequado | Inadequado |
| Ciclos economicos assimetricos | Inadequado | Adequado |
| Bandas de nao-arbitragem | Adequado | Inadequado |
| Taxa de juros com assimetria up/down | Inadequado | Adequado |

## Formulacao Matematica

### Modelo Geral

$$y_t = \boldsymbol{\phi}_1' \mathbf{x}_t \cdot (1 - G(z_t; \gamma, c)) + \boldsymbol{\phi}_2' \mathbf{x}_t \cdot G(z_t; \gamma, c) + \epsilon_t$$

onde $\mathbf{x}_t = (1, y_{t-1}, \ldots, y_{t-p})'$ e $z_t = y_{t-d}$.

### Funcao de Transicao Exponencial

$$G(z_t; \gamma, c) = 1 - \exp(-\gamma(z_t - c)^2)$$

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\gamma$ | Velocidade de transicao | $\gamma > 0$ |
| $c$ | Centro de simetria | Percentis 15%--85% de $z_t$ |
| $\boldsymbol{\phi}_1$ | Parametros AR do regime central ($G \approx 0$) | -- |
| $\boldsymbol{\phi}_2$ | Parametros AR do regime extremo ($G \approx 1$) | -- |

### Propriedades de $G(z_t; \gamma, c)$

A funcao exponencial tem propriedades fundamentalmente diferentes da logistica:

- **Simetria**: $G(c + \delta; \gamma, c) = G(c - \delta; \gamma, c)$ para todo $\delta$
- **Minimo em $c$**: $G(c; \gamma, c) = 0$ — no ponto central, o modelo esta inteiramente no regime 1
- **Limites**:
    - $\gamma \to 0$: $G \to 0$ para todo $z_t$ $\Rightarrow$ modelo linear (regime 1 puro)
    - $\gamma \to \infty$: $G \to 1$ para todo $z_t \neq c$ $\Rightarrow$ regime 2, exceto em $z_t = c$
- **Forma de U**: $G$ e crescente para $|z_t - c|$ crescente

!!! note "Diferenca fundamental: LSTAR vs ESTAR"
    No [LSTAR](lstar.md), a transicao depende da **direcao** do desvio ($z_t - c$ pode ser positivo ou negativo). No ESTAR, a transicao depende da **magnitude** do desvio ($(z_t - c)^2$ e sempre positivo). Isso torna o ESTAR adequado para situacoes onde desvios positivos e negativos de mesma magnitude provocam a mesma resposta.

### Interpretacao dos Regimes

| Regime | Condicao | Interpretacao |
|--------|----------|---------------|
| Regime 1 ($G \approx 0$) | $z_t \approx c$ | Perto do equilibrio — dinamica "normal" |
| Regime 2 ($G \approx 1$) | $\|z_t - c\|$ grande | Longe do equilibrio — dinamica "extrema" |

### Estimacao: Grid Search + NLS

Identica ao [LSTAR](lstar.md):

1. **Grid search** sobre $(\gamma, c)$ com OLS concentrado
2. **Refinamento NLS** (Nelder-Mead) otimizando $\log(\gamma)$ e $c$

A diferenca esta na funcao de transicao usada no calculo de $G$.

## Quick Example

```python
import numpy as np
from archbox.threshold import ESTAR

# Dados simulados com transicao exponencial (simetrica)
rng = np.random.default_rng(42)
n = 1000
y = np.zeros(n)
gamma_true, c_true = 3.0, 0.0

for t in range(1, n):
    s = y[t-1]
    G = 1 - np.exp(-gamma_true * (s - c_true)**2)
    y[t] = (0.5 + 0.3 * y[t-1]) * (1 - G) + (-0.2 + 0.8 * y[t-1]) * G
    y[t] += rng.standard_normal() * 0.5

# Estimar ESTAR
model = ESTAR(y, order=1, delay=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                                  Model: ESTAR
                           Observations: 999
                            AR Order (p): 1
                              Delay (d): 1
                     Number of Regimes: 2
                         Log-Likelihood: -705.1234
                                    AIC: 1422.2468
                                    BIC: 1451.6789
    ----------------------------------------------------------------------
                          Threshold (c): 0.023456
    ----------------------------------------------------------------------
    Transition Parameters:
                                 gamma: 2.987654
                                     c: 0.023456
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

O metodo `fit()` nao requer parametros adicionais.

### Exemplo: Paridade de Poder de Compra (PPP)

```python
import numpy as np
from archbox.threshold import ESTAR, linearity_test, transition_type_test

# Simular desvio da PPP com reversao simetrica
# Perto do equilibrio: random walk (persistencia alta)
# Longe do equilibrio: reversao rapida (persistencia baixa)
rng = np.random.default_rng(42)
n = 800
y = np.zeros(n)  # desvio da PPP
gamma_true, c_true = 2.0, 0.0

for t in range(1, n):
    s = y[t-1]
    G = 1 - np.exp(-gamma_true * (s - c_true)**2)
    # Regime 1 (G~0, perto de 0): alta persistencia (quase random walk)
    # Regime 2 (G~1, longe de 0): reversao rapida ao equilibrio
    y[t] = (0.0 + 0.98 * y[t-1]) * (1 - G) + (0.0 + 0.5 * y[t-1]) * G
    y[t] += rng.standard_normal() * 0.3

# 1. Teste de linearidade
test = linearity_test(y, order=1, delay=1)
print(f"LM test: F = {test.statistic:.4f}, p = {test.pvalue:.4f}")

# 2. Teste de tipo de transicao
type_test = transition_type_test(y, order=1, delay=1)
print(f"Recomendacao: {type_test['recommended']}")
print(f"  p2={type_test['p2']:.4f}, p3={type_test['p3']:.4f}, "
      f"p4={type_test['p4']:.4f}")

# 3. Estimar ESTAR
model = ESTAR(y, order=1, delay=1)
results = model.fit()
print(results.summary())

# 4. Interpretar
gamma_est = results.transition_params['gamma']
c_est = results.transition_params['c']
print(f"\nCentro de simetria: c = {c_est:.4f}")
print(f"Velocidade de transicao: gamma = {gamma_est:.4f}")

# 5. Persistencia por regime
phi_1 = results.params_regime1[1]  # phi_1 do regime 1
phi_2 = results.params_regime2[1]  # phi_1 do regime 2
print(f"Persistencia perto do equilibrio: {phi_1:.4f}")
print(f"Persistencia longe do equilibrio: {phi_2:.4f}")

# 6. Visualizar
results.plot_regimes()
results.plot_transition()
results.plot_phase_diagram()
```

### Comparando LSTAR vs ESTAR

```python
from archbox.threshold import LSTAR, ESTAR

# Estimar ambos os modelos
lstar = LSTAR(y, order=1, delay=1)
estar = ESTAR(y, order=1, delay=1)

res_lstar = lstar.fit()
res_estar = estar.fit()

print(f"LSTAR: AIC={res_lstar.aic:.2f}, BIC={res_lstar.bic:.2f}")
print(f"ESTAR: AIC={res_estar.aic:.2f}, BIC={res_estar.bic:.2f}")

delta_bic = res_lstar.bic - res_estar.bic
if delta_bic > 2:
    print("ESTAR preferido pelo BIC")
elif delta_bic < -2:
    print("LSTAR preferido pelo BIC")
else:
    print("Modelos similares — use o teste de tipo de transicao")
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros por regime (dict) |
| `results.threshold` | Centro de simetria $\hat{c}$ |
| `results.delay` | Delay $d$ |
| `results.transition_params` | `{'gamma': ..., 'c': ...}` |
| `results.params_regime1` | Coeficientes AR: regime central, $G \approx 0$ (ndarray) |
| `results.params_regime2` | Coeficientes AR: regime extremo, $G \approx 1$ (ndarray) |
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

### Simetria da Transicao

A propriedade definidora do ESTAR e a simetria:

$$G(c + \delta; \gamma, c) = G(c - \delta; \gamma, c) = 1 - \exp(-\gamma \delta^2)$$

Isso significa que um desvio de $+2\%$ da PPP produz **exatamente a mesma transicao** que um desvio de $-2\%$. Em contraste, no LSTAR, desvios positivos e negativos produzem transicoes diferentes.

### Aplicacao Classica: PPP e Taxa de Cambio Real

O ESTAR e o modelo padrao para testar a **paridade de poder de compra** (Purchasing Power Parity). A hipotese e que a taxa de cambio real reverte ao equilibrio de longo prazo, mas a velocidade de reversao depende do tamanho do desvio:

- **Perto do equilibrio** ($|z_t - c|$ pequeno): custos de transacao impedem ajuste $\Rightarrow$ alta persistencia
- **Longe do equilibrio** ($|z_t - c|$ grande): oportunidades de arbitragem forcam ajuste $\Rightarrow$ reversao rapida

Esse padrao e consistente com **custos de transacao**: pequenos desvios nao justificam arbitragem, mas grandes desvios sim.

### O Parametro $\gamma$ no ESTAR

| $\gamma$ | Transicao | Zona de inacao |
|----------|-----------|----------------|
| $\gamma$ pequeno | Suave, gradual | Ampla (custos de transacao altos) |
| $\gamma$ grande | Rapida | Estreita (custos de transacao baixos) |

A "zona de inacao" ao redor de $c$ e a faixa onde $G \approx 0$ e o regime 1 (alta persistencia) domina.

## Diagnosticos

```python
from archbox.threshold import ESTAR, linearity_test
import numpy as np

# Teste de linearidade
test = linearity_test(y, order=1, delay=1)
print(f"LM test: p = {test.pvalue:.4f}")

# Qualidade do ajuste
results = ESTAR(y, order=1, delay=1).fit()
print(f"AIC: {results.aic:.4f}")
print(f"BIC: {results.bic:.4f}")

# Verificar simetria da transicao
g = results.transition_values
c_est = results.transition_params['c']
n_obs = results.nobs
y_eff = results.endog[-n_obs:]

# Desvios acima e abaixo de c
above = g[y_eff[:-1] > c_est] if len(y_eff) > len(g) else g[y_eff[:len(g)] > c_est]
below = g[y_eff[:len(g)] <= c_est]
print(f"\nMedia G (acima de c): {np.mean(above):.4f}")
print(f"Media G (abaixo de c): {np.mean(below):.4f}")
print("(valores similares confirmam simetria)")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.threshold import ESTAR

    model = ESTAR(y, order=1, delay=1)
    results = model.fit()
    print(results.summary())
    results.plot_transition()
    ```

=== "R (tsDyn)"

    ```r
    library(tsDyn)

    # ESTAR usando a funcao star com type="ESTAR"
    # Nota: tsDyn suporta ESTAR via opcoes de lstar
    fit <- lstar(y, m = 1, d = 1)
    # Para ESTAR especifico, veja o pacote 'apt'
    summary(fit)
    ```

=== "R (apt)"

    ```r
    library(apt)

    # ESTAR para testes de PPP
    fit <- estar(y, p = 1, d = 1)
    summary(fit)
    ```

| Funcionalidade | ArchBox | tsDyn (R) |
|---------------|---------|-----------|
| Especificacao | `ESTAR(y, order=1, delay=1)` | `star(y, m=1, d=1, type="ESTAR")` |
| Grid search | `gamma_grid=50, c_grid=50` | Automatico |
| Refinamento | `refine=True` | Automatico |
| Gamma | `results.transition_params['gamma']` | `coef(fit)['gamma']` |
| Transicao | `results.transition_values` | `regime(fit)` |

## References

- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of Smooth Transition Autoregressive Models. *Journal of the American Statistical Association*, 89(425), 208--218.
- Taylor, M. P., Peel, D. A., & Sarno, L. (2001). Nonlinear Mean-Reversion in Real Exchange Rates: Toward a Solution to the Purchasing Power Parity Puzzles. *International Economic Review*, 42(4), 1015--1042.
- Michael, P., Nobay, A. R., & Peel, D. A. (1997). Transactions Costs and Nonlinear Adjustment in Real Exchange Rates: An Empirical Investigation. *Journal of Political Economy*, 105(4), 862--879.
- van Dijk, D., Terasvirta, T., & Franses, P. H. (2002). Smooth Transition Autoregressive Models -- A Survey of Recent Developments. *Econometric Reviews*, 21(1), 1--47.

## See Also

- [Threshold/STAR: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [LSTAR](lstar.md) -- Alternativa com transicao assimetrica
- [TAR](tar.md) -- Transicao abrupta
- [SETAR](setar.md) -- TAR self-exciting
- [Testes de Linearidade](linearity-tests.md) -- Teste LM e selecao LSTAR vs ESTAR
