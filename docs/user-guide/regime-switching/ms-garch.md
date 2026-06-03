---
title: "MS-GARCH"
description: "Markov-Switching GARCH model - conditional volatility with regime changes and path dependence solutions."
---

# MS-GARCH (Markov-Switching GARCH)

!!! info "Quick Reference"
    **Class:** `archbox.regime.MarkovSwitchingGARCH`
    **Import:** `from archbox.regime import MarkovSwitchingGARCH`
    **R equivalent:** `MSGARCH::fit.msar(y, ms = TRUE)`
    **Python equivalent:** Nao disponivel em pacotes padrao

## Overview

O modelo MS-GARCH (Markov-Switching GARCH) combina a modelagem de **volatilidade condicional** (GARCH) com **mudancas de regime** (Markov-Switching), permitindo que os parametros do processo GARCH variem entre estados discretos. Proposto inicialmente por **Cai (1994)** e **Hamilton e Susmel (1994)**, e formalmente desenvolvido por **Gray (1996)**, o MS-GARCH captura uma caracteristica fundamental dos mercados financeiros: a volatilidade nao apenas se agrupa (clustering), mas o *proprio mecanismo gerador de volatilidade* muda ao longo do tempo.

O MS-GARCH e essencial quando:

- **Crises financeiras**: a volatilidade durante crises tem dinamica fundamentalmente diferente da volatilidade em periodos normais
- **Mercados emergentes**: alternam entre regimes de estabilidade e turbulencia com parametros GARCH distintos
- **Mudancas de politica**: politica monetaria ou cambial altera o processo de volatilidade
- **Caudas da distribuicao**: o GARCH padrao subestima eventos extremos por ignorar mudancas de regime

**Quando usar:**

- Retornos financeiros com evidencia de mudancas no processo de volatilidade
- Quando o GARCH padrao apresenta persistencia estimada muito proxima de 1 ($\hat{\alpha} + \hat{\beta} \approx 1$)
- Mercados emergentes ou commodities com periodos de instabilidade
- Quando se deseja previsao de volatilidade condicionada ao regime

## Formulacao Matematica

### Modelo Geral

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t(s_t) \, z_t, \qquad z_t \sim D(0, 1)$$

onde a **variancia condicional** depende do regime $s_t$:

$$\sigma_t^2(s_t) = \omega_{s_t} + \sum_{i=1}^{q} \alpha_{i,s_t} \, \epsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_{j,s_t} \, h_{t-j}$$

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega_{s_t}$ | Intercepto no regime $s_t$ | $\omega_{s_t} > 0$ |
| $\alpha_{i,s_t}$ | Coeficiente ARCH no regime $s_t$ | $\alpha_{i,s_t} \geq 0$ |
| $\beta_{j,s_t}$ | Coeficiente GARCH no regime $s_t$ | $\beta_{j,s_t} \geq 0$ |
| $p_{ij}$ | Probabilidade de transicao $i \to j$ | $\sum_j p_{ij} = 1$ |

### O Problema de Path Dependence

O desafio central do MS-GARCH e a **dependencia de trajetoria** (path dependence). No GARCH padrao, $\sigma_t^2$ depende de $\sigma_{t-1}^2$, que depende de $\sigma_{t-2}^2$, e assim por diante. No MS-GARCH, $\sigma_t^2$ depende nao apenas de $s_t$, mas de **toda a historia de regimes** $(s_1, s_2, \ldots, s_t)$:

$$\sigma_t^2 = f(s_1, s_2, \ldots, s_t, \epsilon_1, \epsilon_2, \ldots, \epsilon_{t-1})$$

Para $K$ regimes e $T$ observacoes, existem $K^T$ trajetorias possiveis, tornando a estimacao exata computacionalmente intratavel.

!!! warning "Path dependence"
    A path dependence e o que torna o MS-GARCH fundamentalmente mais complexo que o MS-AR. No MS-AR, a verossimilhanca pode ser computada exatamente via Hamilton filter porque a variancia condicional nao depende do regime passado. No MS-GARCH, a dependencia da variancia no regime passado via $\sigma_{t-1}^2$ cria uma explosao combinatoria.

### Solucao de Gray (1996): Collapsing

Gray (1996) propos uma solucao elegante: **colapsar** a variancia condicional a cada periodo, substituindo $\sigma_{t-1}^2$ por uma media ponderada sobre os regimes:

$$h_{t-1} = \sum_{j=0}^{K-1} P(s_{t-1} = j \mid \mathcal{Y}_{t-1}) \, \sigma_{t-1}^2(j)$$

Assim, a variancia condicional no regime $k$ fica:

$$\sigma_t^2(k) = \omega_k + \alpha_k \, \epsilon_{t-1}^2 + \beta_k \, h_{t-1}$$

onde $h_{t-1}$ e a **variancia colapsada** — uma unica quantidade escalar, independente do regime.

**Vantagens:**

- Elimina a path dependence
- Permite o uso do Hamilton filter padrao
- Estimacao via EM e computacionalmente viavel

**Desvantagem:**

- E uma aproximacao; perde informacao sobre a trajetoria de regimes

### Solucao de Klaassen (2002): Collapsing Refinado

Klaassen (2002) propos usar probabilidades condicionais *atualizadas* no collapsing:

$$h_{t-1}^{(k)} = \sum_{j=0}^{K-1} P(s_{t-1} = j \mid s_t = k, \mathcal{Y}_{t-1}) \left[ \sigma_{t-1}^2(j) + (\mu_j - \bar{\mu}_{t-1})^2 \right]$$

onde a probabilidade de $s_{t-1}$ e condicionada ao regime atual $s_t = k$. Isso melhora a aproximacao ao incorporar informacao sobre a transicao.

### Solucao de Haas, Mittnik e Paolella (2004)

Haas et al. (2004) propuseram uma abordagem alternativa onde cada regime tem seu **proprio processo GARCH independente**:

$$\sigma_t^2(k) = \omega_k + \alpha_k \, \epsilon_{t-1}^2 + \beta_k \, \sigma_{t-1}^2(k)$$

Aqui, $\sigma_{t-1}^2(k)$ e a variancia passada *dentro do regime $k$*, nao a variancia colapsada. Isso elimina a path dependence de forma diferente — cada regime mantem sua propria "memoria" de variancia.

### Caso MS(2)-GARCH(1,1) com Collapsing de Gray

$$h_{t-1} = P(s_{t-1}=0 \mid \mathcal{Y}_{t-1}) \, \sigma_{t-1}^2(0) + P(s_{t-1}=1 \mid \mathcal{Y}_{t-1}) \, \sigma_{t-1}^2(1)$$

**Regime 0** (alta volatilidade):
$$\sigma_t^2(0) = \omega_0 + \alpha_0 \, \epsilon_{t-1}^2 + \beta_0 \, h_{t-1}$$

**Regime 1** (baixa volatilidade):
$$\sigma_t^2(1) = \omega_1 + \alpha_1 \, \epsilon_{t-1}^2 + \beta_1 \, h_{t-1}$$

### Interpretacao Economica dos Regimes

| Parametro | Regime 0 (crise) | Regime 1 (normal) |
|-----------|:-----------------:|:-----------------:|
| $\omega$ | Alto | Baixo |
| $\alpha$ | Alto (reacao rapida) | Baixo (reacao moderada) |
| $\beta$ | Baixo (menos persistente) | Alto (mais persistente) |
| Persistencia $\alpha + \beta$ | Moderada | Alta |
| Variancia incondicional | Alta | Baixa |

!!! note "Persistencia espuria"
    Um GARCH(1,1) estimado em dados com mudanca de regime tipicamente apresenta $\hat{\alpha} + \hat{\beta} \approx 1$ (IGARCH espurio). O MS-GARCH resolve isso ao permitir que cada regime tenha sua propria persistencia, tipicamente menor que 1.

## Quick Example

```python
from archbox.regime import MarkovSwitchingGARCH
from archbox.datasets import load_dataset

# Carregar retornos
data = load_dataset('bovespa')
returns = data['returns'].to_numpy()

# MS(2)-GARCH(1,1) com collapsing de Gray
model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    =================================================================
      MS-GARCH Results
    =================================================================
      Observations:    1000
      Regimes:         2
      Parameters:      8
      Log-Likelihood:  2876.4521
      AIC:             -5736.9042
      BIC:             -5697.6234
      Converged:       True
      Iterations:      85
    =================================================================

      Regime Parameters:
    -----------------------------------------------------------------
      Regime 0:
        omega                =     0.000156
        alpha                =     0.145623
        beta                 =     0.712345
      Regime 1:
        omega                =     0.000012
        alpha                =     0.048912
        beta                 =     0.938456

      Transition Matrix P:
    -----------------------------------------------------------------
           Regime 0  Regime 1
      S=0  0.9456    0.0544
      S=1  0.0234    0.9766

      Expected Durations:
    -----------------------------------------------------------------
        Regime 0: 18.38 periods
        Regime 1: 42.74 periods

      Ergodic Probabilities:
    -----------------------------------------------------------------
        Regime 0: 0.3008
        Regime 1: 0.6992
    =================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de retornos, shape (T,) |
| `k_regimes` | int | `2` | Numero de regimes ($K$) |
| `p` | int | `1` | Ordem GARCH (lags de $\sigma^2$) |
| `q` | int | `1` | Ordem ARCH (lags de $\epsilon^2$) |
| `method` | str | `"gray"` | Metodo de collapsing: `"gray"` ou `"haas"` |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `max_iter` | int | `500` | Numero maximo de iteracoes do EM |
| `tol` | float | `1e-8` | Tolerancia para convergencia |
| `n_init` | int | `5` | Numero de inicializacoes |
| `disp` | bool | `True` | Exibir progresso |

### Exemplo: Volatilidade de Mercado Emergente com Crises

```python
import numpy as np
from archbox.regime import MarkovSwitchingGARCH
from archbox import GARCH
from archbox.datasets import load_dataset

# 1. Carregar retornos do Bovespa
data = load_dataset('bovespa')
returns = data['returns'].to_numpy()

# 2. Comparar GARCH padrao vs. MS-GARCH
# GARCH(1,1) padrao
garch = GARCH(returns, p=1, q=1)
garch_res = garch.fit()
print("=== GARCH(1,1) padrao ===")
print(f"alpha + beta = {garch_res.persistence():.6f}")
print(f"AIC: {garch_res.aic:.4f}")
print(f"BIC: {garch_res.bic:.4f}")

# 3. MS(2)-GARCH(1,1)
ms_garch = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
ms_res = ms_garch.fit()

print("\n=== MS(2)-GARCH(1,1) ===")
for k in range(ms_res.k_regimes):
    params = ms_res.regime_params[k]
    alpha = params.get('alpha', 0)
    beta = params.get('beta', 0)
    omega = params.get('omega', 0)
    persistence = alpha + beta
    uncond_vol = np.sqrt(omega / max(1 - persistence, 1e-10))
    print(f"Regime {k}: alpha={alpha:.4f}, beta={beta:.4f}, "
          f"persistence={persistence:.4f}, "
          f"uncond_vol={uncond_vol:.4f}")

print(f"AIC: {ms_res.aic:.4f}")
print(f"BIC: {ms_res.bic:.4f}")

# 4. Identificar regime de crise
params_0 = ms_res.regime_params[0]
params_1 = ms_res.regime_params[1]
omega_0 = params_0.get('omega', 0)
omega_1 = params_1.get('omega', 0)
crisis_regime = 0 if omega_0 > omega_1 else 1

print(f"\nRegime de crise: {crisis_regime}")
crisis_prob = ms_res.smoothed_probs[:, crisis_regime]
print(f"Periodos em crise (P > 0.5): {(crisis_prob > 0.5).sum()}")

# 5. Duracao esperada dos regimes
durations = ms_res.expected_durations()
print(f"Duracao esperada da crise: {durations[crisis_regime]:.1f} dias")
print(f"Duracao esperada da normalidade: "
      f"{durations[1-crisis_regime]:.1f} dias")

# 6. Visualizar
ms_res.plot_regimes(y=returns)
ms_res.plot_probabilities(regime=crisis_regime)
```

### Comparacao de Metodos de Collapsing

```python
# Gray (1996) vs Haas et al. (2004)
for method in ["gray", "haas"]:
    model = MarkovSwitchingGARCH(
        returns, k_regimes=2, p=1, q=1, method=method
    )
    res = model.fit()
    print(f"{method.upper()}: LogL={res.loglike:.2f}, "
          f"AIC={res.aic:.2f}, BIC={res.bic:.2f}")
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Todos os parametros estimados (ndarray) |
| `results.regime_params` | Parametros GARCH por regime (dict) |
| `results.transition_matrix` | Matriz de transicao $P$, shape (K, K) |
| `results.filtered_probs` | Probabilidades filtradas, shape (T, K) |
| `results.smoothed_probs` | Probabilidades suavizadas, shape (T, K) |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |

| Metodo | Descricao |
|--------|-----------|
| `results.summary()` | Tabela formatada de resultados |
| `results.expected_durations()` | Duracao esperada de cada regime |
| `results.ergodic_probabilities()` | Probabilidades ergoticas |
| `results.classify()` | Classificar observacoes em regimes |
| `results.plot_regimes(y)` | Grafico com shading de regimes |
| `results.plot_probabilities(regime)` | Grafico de probabilidades |

## Interpretacao

### Path Dependence: Por que Importa

Para entender o impacto da path dependence, considere um MS(2)-GARCH(1,1). Em $t=100$, existem $2^{100} \approx 10^{30}$ trajetorias possiveis de regime. Cada trajetoria produz uma variancia condicional diferente:

```
Trajetoria A:  s=0,0,0,1,1,1,1,0,0,...  → σ²₁₀₀(A)
Trajetoria B:  s=1,1,0,0,1,1,0,1,1,...  → σ²₁₀₀(B)
Trajetoria C:  s=0,1,0,1,0,1,0,1,0,...  → σ²₁₀₀(C)
    ...             ...                       ...
```

O collapsing de Gray resolve isso produzindo uma **unica** variancia colapsada $h_t$ a cada periodo, eliminando a necessidade de rastrear todas as trajetorias.

### Persistencia Espuria no GARCH

Um dos resultados mais importantes do MS-GARCH e explicar a **persistencia espuria** no GARCH padrao:

$$\underbrace{\hat{\alpha} + \hat{\beta} \approx 1}_{\text{GARCH padrao (IGARCH espurio)}} \quad \Longleftrightarrow \quad \underbrace{\alpha_k + \beta_k < 1 \; \forall k}_{\text{MS-GARCH (estacionario em cada regime)}}$$

Quando o processo gerador de dados tem mudanca de regime, o GARCH padrao compensa as mudancas de nivel na variancia aumentando a persistencia, resultando em estimativas proximas de IGARCH.

!!! note "Teste pratico"
    Se o seu GARCH(1,1) estima $\hat{\alpha} + \hat{\beta} > 0.99$, e provavel que haja mudanca de regime. Estime um MS-GARCH e verifique se a persistencia dentro de cada regime e significativamente menor.

### Variancia Incondicional por Regime

Em cada regime $k$ (assumindo estacionariedade), a variancia incondicional e:

$$\bar{\sigma}_k^2 = \frac{\omega_k}{1 - \alpha_k - \beta_k}$$

A variancia incondicional *global* (ponderada pelas probabilidades ergoticas) e:

$$\bar{\sigma}^2 = \sum_{k=0}^{K-1} \pi_k \, \bar{\sigma}_k^2$$

```python
# Variancia incondicional por regime
ergodic = ms_res.ergodic_probabilities()
global_var = 0.0
for k in range(ms_res.k_regimes):
    params = ms_res.regime_params[k]
    omega = params.get('omega', 0)
    alpha = params.get('alpha', 0)
    beta = params.get('beta', 0)
    uncond_var = omega / max(1 - alpha - beta, 1e-10)
    uncond_vol = np.sqrt(uncond_var)
    global_var += ergodic[k] * uncond_var
    print(f"Regime {k}: σ² = {uncond_var:.6e}, "
          f"σ = {uncond_vol:.4f}, π = {ergodic[k]:.4f}")

print(f"\nGlobal: σ² = {global_var:.6e}, σ = {np.sqrt(global_var):.4f}")
```

### Previsao de Volatilidade

A previsao de volatilidade no MS-GARCH incorpora a incerteza sobre o regime futuro:

$$E[\sigma_{T+1}^2 \mid \mathcal{Y}_T] = \sum_{k=0}^{K-1} P(s_{T+1} = k \mid \mathcal{Y}_T) \, \sigma_{T+1}^2(k)$$

onde $P(s_{T+1} = k \mid \mathcal{Y}_T) = \sum_{j} p_{jk} \, P(s_T = j \mid \mathcal{Y}_T)$.

## Diagnosticos

### GARCH vs. MS-GARCH

```python
# Comparacao formal via criterios de informacao
from archbox import GARCH
from archbox.regime import MarkovSwitchingGARCH

garch_res = GARCH(returns, p=1, q=1).fit()
ms_res = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1).fit()

print(f"GARCH(1,1)      - AIC: {garch_res.aic:.2f}, BIC: {garch_res.bic:.2f}")
print(f"MS(2)-GARCH(1,1) - AIC: {ms_res.aic:.2f}, BIC: {ms_res.bic:.2f}")

delta_bic = garch_res.bic - ms_res.bic
if delta_bic > 10:
    print("Forte evidencia a favor do MS-GARCH")
elif delta_bic > 2:
    print("Evidencia moderada a favor do MS-GARCH")
else:
    print("GARCH padrao pode ser suficiente")
```

### Convergencia e Estabilidade

```python
# Multiplas inicializacoes para verificar robustez
best_loglike = -np.inf
best_results = None

model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
results = model.fit(n_init=10)

print(f"Convergiu: {results.converged}")
print(f"Iteracoes: {results.n_iter}")
```

### Qualidade da Separacao de Regimes

```python
# RCM (Regime Classification Measure)
smoothed = ms_res.smoothed_probs
rcm = 400.0 / ms_res.nobs * np.sum(
    smoothed[:, 0] * smoothed[:, 1]
)
print(f"RCM: {rcm:.2f}")
print("(0 = separacao perfeita, 100 = sem separacao)")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.regime import MarkovSwitchingGARCH

    model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
    results = model.fit()
    print(results.summary())
    ```

=== "R (MSGARCH)"

    ```r
    library(MSGARCH)

    # Especificacao: 2 regimes, GARCH(1,1), Normal
    spec <- CreateSpec(
      variance.spec = list(model = c("sGARCH", "sGARCH")),
      distribution.spec = list(distribution = c("norm", "norm")),
      switch.spec = list(do.mix = FALSE)
    )

    fit <- FitML(spec = spec, data = returns)
    summary(fit)

    # Probabilidades suavizadas
    State(fit)
    ```

=== "R (rugarch + manual)"

    ```r
    # Nao ha implementacao direta em rugarch
    # Use o pacote MSGARCH para MS-GARCH
    library(MSGARCH)

    spec <- CreateSpec(
      variance.spec = list(model = c("sGARCH", "sGARCH")),
      distribution.spec = list(distribution = c("norm", "norm"))
    )
    fit <- FitML(spec, data = returns)
    ```

| Funcionalidade | ArchBox | MSGARCH (R) |
|---------------|---------|-------------|
| Especificacao | `MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)` | `CreateSpec(model=c("sGARCH","sGARCH"))` |
| Collapsing | `method="gray"` ou `"haas"` | `do.mix=FALSE` (Gray) |
| Estimacao | `model.fit()` | `FitML(spec, data)` |
| Probabilidades | `results.smoothed_probs` | `State(fit)` |
| Classificacao | `results.classify()` | Manual via `State` |

## References

- Gray, S. F. (1996). Modeling the Conditional Distribution of Interest Rates as a Regime-Switching Process. *Journal of Financial Economics*, 42(1), 27--62.
- Klaassen, F. (2002). Improving GARCH Volatility Forecasts with Regime-Switching GARCH. *Empirical Economics*, 27(2), 363--394.
- Haas, M., Mittnik, S., & Paolella, M. S. (2004). A New Approach to Markov-Switching GARCH Models. *Journal of Financial Econometrics*, 2(4), 493--530.
- Cai, J. (1994). A Markov Model of Switching-Regime ARCH. *Journal of Business & Economic Statistics*, 12(3), 309--316.
- Hamilton, J. D., & Susmel, R. (1994). Autoregressive Conditional Heteroskedasticity and Changes in Regime. *Journal of Econometrics*, 64(1-2), 307--333.
- Ardia, D., Bluteau, K., Boudt, K., Catania, L., & Trottier, D.-A. (2019). Markov-Switching GARCH Models in R: The MSGARCH Package. *Journal of Statistical Software*, 91(4), 1--38.

## See Also

- [Regime-Switching: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [MS-AR](ms-ar.md) -- Modelo autorregressivo com mudanca de regime
- [MS-VAR](ms-var.md) -- VAR com mudanca de regime
- [GARCH(p,q)](../garch/garch.md) -- Modelo GARCH padrao sem regimes
- [EGARCH](../garch/egarch.md) -- GARCH assimetrico sem regimes
- [IGARCH](../garch/igarch.md) -- GARCH com persistencia unitaria (pode ser espuria)
