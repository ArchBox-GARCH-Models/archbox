---
title: "Expected Shortfall (ES / CVaR)"
description: "Expected Shortfall: medida coerente de risco com formulacao analitica para Normal e Student-t."
---

# Expected Shortfall (ES / CVaR)

!!! info "Quick Reference"
    **Class:** `archbox.risk.es.ExpectedShortfall`
    **Import:** `from archbox.risk import ExpectedShortfall`
    **R equivalent:** `rugarch::ugarchroll()` + `ES()` (PerformanceAnalytics)
    **Python equivalent:** Manual computation from `arch` forecast

## Overview

O **Expected Shortfall (ES)**, tambem conhecido como **Conditional Value-at-Risk (CVaR)** ou **Tail VaR**, e uma medida de risco que responde a pergunta: *"Dado que a perda excedeu o VaR, qual e a perda media esperada?"*

Proposta formalmente por **Artzner, Delbaen, Eber e Heath (1999)** como exemplo de **medida coerente de risco**, o ES supera a principal deficiencia do VaR: a incapacidade de capturar a magnitude das perdas extremas (tail risk).

**Quando usar:**

- Relatorios regulatorios sob **Basel III/IV** (metrica principal desde FRTB)
- Analise de portfolios com **caudas pesadas** (fat tails)
- Otimizacao de carteira com restricoes de risco (ES e convexo)
- Quando a **subaditividade** e importante (diversificacao deve reduzir risco)

!!! note "Basel III: de VaR para ES"
    O **Fundamental Review of the Trading Book (FRTB)** substituiu o VaR a 99% pelo ES a 97.5% como metrica principal para requisitos de capital. A razao: o ES captura o que acontece **alem** do quantil, enquanto o VaR ignora completamente a severidade das perdas extremas.

## Formulacao Matematica

### Definicao Formal

O Expected Shortfall ao nivel $\alpha$ e definido como:

$$ES_\alpha = E[L \mid L > \text{VaR}_\alpha] = \frac{1}{1-\alpha} \int_\alpha^1 \text{VaR}_u \, du$$

onde $L = -r_t$ e a perda. Equivalentemente, em termos de retornos:

$$ES_\alpha = -E[r_t \mid r_t < \text{VaR}_\alpha]$$

### Propriedades de Medida Coerente

O ES satisfaz os quatro axiomas de Artzner et al. (1999):

| Propriedade | Definicao | Significado |
|-------------|-----------|-------------|
| **Monotonicidade** | $X \leq Y \Rightarrow \rho(X) \geq \rho(Y)$ | Retornos maiores $\rightarrow$ menos risco |
| **Invariancia por translacao** | $\rho(X + c) = \rho(X) - c$ | Adicionar caixa reduz risco |
| **Homogeneidade positiva** | $\rho(\lambda X) = \lambda \rho(X)$ | Dobrar posicao dobra risco |
| **Subaditividade** | $\rho(X + Y) \leq \rho(X) + \rho(Y)$ | Diversificacao reduz risco |

!!! warning "VaR viola subaditividade"
    O VaR **nao** satisfaz a subaditividade. Isso significa que juntar duas carteiras pode **aumentar** o VaR total, um resultado que contradiz o principio fundamental da diversificacao. O ES resolve esse problema.

### ES Parametrico: Distribuicao Normal

Para retornos condicionalmente normais $r_t \mid \mathcal{F}_{t-1} \sim N(\mu_t, \sigma_t^2)$:

$$ES_{\alpha,t} = \mu_t - \sigma_t \cdot \frac{\phi(\Phi^{-1}(\alpha))}{\alpha}$$

onde $\phi(\cdot)$ e a funcao densidade e $\Phi^{-1}(\cdot)$ e o quantil da Normal padrao.

!!! tip "Relacao ES/VaR para Normal"
    Para a distribuicao Normal, a razao $ES/VaR$ depende apenas de $\alpha$. A 5%: $ES \approx 1.28 \times VaR$. A 1%: $ES \approx 1.15 \times VaR$.

### ES Parametrico: Distribuicao Student-t

Para retornos com distribuicao Student-t padronizada com $\nu$ graus de liberdade:

$$ES_{\alpha,t} = \mu_t - \sigma_t \cdot \frac{f_\nu(t_\nu^{-1}(\alpha))}{\alpha} \cdot \frac{\nu + (t_\nu^{-1}(\alpha))^2}{\nu - 1} \cdot \sqrt{\frac{\nu - 2}{\nu}}$$

onde:

- $f_\nu(\cdot)$ e a funcao densidade da Student-t com $\nu$ g.l.
- $t_\nu^{-1}(\alpha)$ e o quantil $\alpha$ da Student-t
- O fator $\sqrt{(\nu-2)/\nu}$ ajusta para variancia unitaria

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\alpha$ | Nivel de significancia | $0 < \alpha < 1$ |
| $\nu$ | Graus de liberdade (Student-t) | $\nu > 2$ |
| $\sigma_t$ | Volatilidade condicional (GARCH) | $\sigma_t > 0$ |
| $\mu_t$ | Media condicional | Livre |

### ES Historico

Media dos retornos abaixo do VaR em janela rolante:

$$ES_{\alpha,t}^{HS} = \frac{1}{|\{i : r_i \leq \text{VaR}_\alpha\}|} \sum_{r_i \leq \text{VaR}_\alpha} r_i$$

### ES por Filtered Historical Simulation

Combinando GARCH e distribuicao empirica dos residuos:

1. Padronizar: $z_t = (r_t - \mu) / \sigma_t$
2. $ES_{\alpha,t}^{FHS} = \mu + \sigma_t \cdot E[z \mid z < q_\alpha^z]$

## Quick Example

```python
from archbox import GARCH
from archbox.risk import ExpectedShortfall
from archbox.datasets import load_dataset

# Estimar GARCH(1,1)
sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()

# ES parametrico a 5% (Normal)
es = ExpectedShortfall(results, alpha=0.05)
es_series = es.parametric(dist='normal')
print(f"ES medio: {es_series.mean():.6f}")
print(f"ES minimo (pior dia): {es_series.min():.6f}")
```

??? example "Output esperado"
    ```
    ES medio: -0.023012
    ES minimo (pior dia): -0.082145
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | ArchResults | obrigatorio | Resultados de um modelo ajustado |
| `alpha` | float | `0.05` | Nivel de significancia |

### Metodos

| Metodo | Parametros | Descricao |
|--------|-----------|-----------|
| `parametric(dist, nu)` | `dist='normal'`, `nu=8.0` | ES parametrico (Normal ou Student-t) |
| `historical(window)` | `window=250` | ES por simulacao historica |
| `filtered_historical()` | -- | ES por FHS |

### Exemplo Completo: GARCH + Student-t

```python
import numpy as np
from archbox import GARCH
from archbox.risk import ValueAtRisk, ExpectedShortfall
from archbox.datasets import load_dataset

# 1. Estimar GARCH(1,1)
sp500 = load_dataset('sp500')
returns = sp500['returns']
model = GARCH(returns, p=1, q=1)
results = model.fit()

# 2. ES com diferentes distribuicoes
es = ExpectedShortfall(results, alpha=0.05)

# Normal
es_normal = es.parametric(dist='normal')
print("=== ES Parametrico (Normal) ===")
print(f"  Media: {es_normal.mean():.6f}")

# Student-t (caudas pesadas)
es_t = es.parametric(dist='studentt', nu=6.0)
print("\n=== ES Parametrico (Student-t, nu=6) ===")
print(f"  Media: {es_t.mean():.6f}")

# Historico
es_hist = es.historical(window=250)
valid = ~np.isnan(es_hist)
print("\n=== ES Historico (window=250) ===")
print(f"  Media: {es_hist[valid].mean():.6f}")

# Filtered Historical Simulation
es_fhs = es.filtered_historical()
valid_fhs = ~np.isnan(es_fhs)
print("\n=== ES FHS ===")
print(f"  Media: {es_fhs[valid_fhs].mean():.6f}")

# 3. Comparacao VaR vs ES
var = ValueAtRisk(results, alpha=0.05)
var_normal = var.parametric(dist='normal')

ratio = es_normal.mean() / var_normal.mean()
print(f"\nRazao ES/VaR (Normal): {ratio:.4f}")
print(f"ES captura {(ratio - 1) * 100:.1f}% mais risco que o VaR")
```

### Comparacao VaR vs ES

| Propriedade | VaR | ES |
|-------------|-----|-----|
| Definicao | Quantil da distribuicao de perdas | Media das perdas alem do VaR |
| Coerencia | Nao (viola subaditividade) | Sim (satisfaz os 4 axiomas) |
| Tail risk | Ignora magnitude das perdas extremas | Captura a magnitude media |
| Regulacao | Basel II (principal), Basel III (backtesting) | Basel III/IV (principal) |
| Interpretacao | "Perda maxima com X% de confianca" | "Perda media nos piores cenarios" |
| Otimizacao | Nao-convexa | Convexa (facilita otimizacao de portfolio) |
| Backtesting | Testes formais (Kupiec, Christoffersen) | Mais dificil de backtestear |
| Sensibilidade | Insensivel a caudas | Sensivel a forma da cauda |

```
Distribuicao de Perdas
    │
    │                         ┌─────────────────────┐
    │                         │   Regiao capturada   │
    │                         │   pelo ES (CVaR)     │
    │    ╱╲                   │                     │
    │   ╱  ╲                  └─────────┐           │
    │  ╱    ╲                           │           │
    │ ╱      ╲                          │           │
    │╱        ╲           ╱╲            │           │
    ├──────────╲─────────╱──╲───────────┼───────────┤
    │           ╲       ╱    ╲          │           │
    │            ╲     ╱      ╲         │           │
    │             ╲   ╱        ╲        │           │
    │              ╲ ╱          ╲───────┘           │
    │               ╳            ────────────────────
    ├───────────────┼────────────┼──────────────────>
                   VaR          ES         Perdas
                (quantil)   (media da cauda)
```

!!! tip "Escolha pratica"
    Use **VaR** para comunicacao (facil de explicar: "perda maxima de X%") e **ES** para decisoes de alocacao e capital regulatorio (captura o *quanto* se perde nos cenarios adversos).

## Interpretacao

### Leitura do ES

Um ES de $-0.035$ a $\alpha = 0.05$ significa:

> "Nos 5% piores cenarios, a perda media esperada e de 3.5% do valor da posicao."

### Impacto dos Graus de Liberdade

Quanto menor $\nu$, mais pesadas as caudas e maior o ES:

```python
es = ExpectedShortfall(results, alpha=0.05)

for nu in [4, 6, 8, 12, 30]:
    es_t = es.parametric(dist='studentt', nu=nu)
    es_n = es.parametric(dist='normal')
    ratio = es_t.mean() / es_n.mean()
    print(f"  nu={nu:2d}: ES_t/ES_normal = {ratio:.4f}")
```

??? example "Output esperado"
    ```
      nu= 4: ES_t/ES_normal = 1.6412
      nu= 6: ES_t/ES_normal = 1.2834
      nu= 8: ES_t/ES_normal = 1.1723
      nu=12: ES_t/ES_normal = 1.0956
      nu=30: ES_t/ES_normal = 1.0312
    ```

!!! note "Convergencia para Normal"
    Quando $\nu \to \infty$, a Student-t converge para a Normal e $ES_t \to ES_{Normal}$. Para $\nu \leq 6$ (comum em dados financeiros), a diferenca e substancial.

## Diagnosticos

### Validacao do ES

Diferentemente do VaR, o backtesting formal do ES e mais desafiador. Abordagens praticas:

```python
import numpy as np
from archbox import GARCH
from archbox.risk import ExpectedShortfall, ValueAtRisk, VaRBacktest
from archbox.datasets import load_dataset

# 1. Modelo
sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()
returns = sp500['returns']

# 2. Calcular VaR e ES
var = ValueAtRisk(results, alpha=0.05)
es = ExpectedShortfall(results, alpha=0.05)

var_series = var.parametric(dist='normal')
es_series = es.parametric(dist='normal')

# 3. Backtesting via VaR (indiretamente valida o ES)
bt = VaRBacktest(returns, var_series, alpha=0.05)
print(bt.summary())

# 4. Verificacao empirica do ES
violations = returns < var_series
if violations.sum() > 0:
    avg_loss_given_violation = returns[violations].mean()
    avg_es_given_violation = es_series[violations].mean()
    print(f"\nPerda media nas violacoes:  {avg_loss_given_violation:.6f}")
    print(f"ES medio nas violacoes:     {avg_es_given_violation:.6f}")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCH
    from archbox.risk import ExpectedShortfall

    model = GARCH(returns, p=1, q=1)
    results = model.fit()

    es = ExpectedShortfall(results, alpha=0.05)
    es_normal = es.parametric(dist='normal')
    es_t = es.parametric(dist='studentt', nu=6.0)
    es_hist = es.historical(window=250)
    es_fhs = es.filtered_historical()
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)
    library(PerformanceAnalytics)

    spec <- ugarchspec(
      variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
      distribution.model = "std"  # Student-t
    )
    fit <- ugarchfit(spec, data = returns)

    # ES via quantile da distribuicao condicional
    sigma <- sigma(fit)
    shape <- coef(fit)["shape"]
    ES_t <- fitted(fit) + sigma * (dt(qt(0.05, shape), shape) / 0.05) *
            ((shape + qt(0.05, shape)^2) / (shape - 1)) *
            sqrt((shape - 2) / shape)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model
    from scipy import stats
    import numpy as np

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='Normal')
    res = am.fit()

    # ES manual (Normal)
    sigma = res.conditional_volatility
    z_alpha = stats.norm.ppf(0.05)
    phi_z = stats.norm.pdf(z_alpha)
    es = res.params['mu'] - sigma * phi_z / 0.05
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| ES Parametrico | `es.parametric()` | Manual | Manual |
| ES Historico | `es.historical()` | `ES()` (PerformanceAnalytics) | Manual |
| ES FHS | `es.filtered_historical()` | Manual | Manual |
| ES Student-t | `es.parametric(dist='studentt')` | Manual via `qdist()` | Manual |

## References

- Artzner, P., Delbaen, F., Eber, J.-M., & Heath, D. (1999). Coherent Measures of Risk. *Mathematical Finance*, 9(3), 203--228.
- McNeil, A.J., Frey, R., & Embrechts, P. (2015). *Quantitative Risk Management*. 2nd ed. Princeton University Press. Cap. 2.
- Acerbi, C., & Tasche, D. (2002). On the Coherence of Expected Shortfall. *Journal of Banking & Finance*, 26(7), 1487--1503.
- Basel Committee on Banking Supervision (2019). *Minimum Capital Requirements for Market Risk*. Bank for International Settlements.

## See Also

- [Value-at-Risk (VaR)](var.md) -- Metrica base para backtesting
- [EWMA / RiskMetrics](ewma.md) -- Volatilidade rapida para ES
- [Gestao de Risco: Overview](index.md) -- Pipeline completo de risco
- [Distribuicoes Condicionais](../distributions/index.md) -- Student-t para caudas pesadas
