---
title: "Value-at-Risk (VaR)"
description: "Value-at-Risk: parametric, historical simulation, filtered historical and Monte Carlo approaches."
---

# Value-at-Risk (VaR)

!!! info "Quick Reference"
    **Class:** `archbox.risk.var.ValueAtRisk`
    **Import:** `from archbox.risk import ValueAtRisk`
    **R equivalent:** `rugarch::ugarchroll(..., VaR.alpha = 0.05)`
    **Python equivalent:** Manual computation from `arch` forecast

## Overview

O **Value-at-Risk (VaR)** e a metrica de risco de mercado mais amplamente utilizada na industria financeira. Introduzido pelo JP Morgan no sistema RiskMetrics (1996), tornou-se o padrao regulatorio sob Basel II e permanece central para backtesting sob Basel III/IV.

O VaR responde a pergunta: *"Qual e a perda maxima esperada em um horizonte de tempo, com um dado nivel de confianca?"*

**Quando usar:**

- Comunicacao de risco com stakeholders (interpretacao intuitiva)
- Definicao de limites de risco (trading desks, carteiras)
- Backtesting regulatorio (Basel traffic light system)
- Comparacao entre estrategias ou ativos

**Limitacoes:**

- Nao e uma **medida coerente de risco** (viola subaditividade)
- Nao informa sobre a **magnitude** das perdas alem do quantil
- Pode **subestimar tail risk** em distribuicoes de caudas pesadas

!!! warning "VaR nao e subaditividade"
    O VaR pode violar a propriedade de subaditividade: $\text{VaR}(A + B) > \text{VaR}(A) + \text{VaR}(B)$. Isso significa que diversificacao pode aparentemente *aumentar* o risco medido pelo VaR — um resultado contraintuitivo e indesejavel. Para uma medida coerente, utilize o [Expected Shortfall](es.md).

## Formulacao Matematica

### Definicao Formal

O VaR ao nivel de confianca $\alpha$ e definido como:

$$P(L_t > \text{VaR}_\alpha) = 1 - \alpha$$

ou equivalentemente, como o quantil $\alpha$ da distribuicao de perdas:

$$\text{VaR}_\alpha = -\inf\{x : P(r_t \leq x) > \alpha\} = -F_r^{-1}(\alpha)$$

onde $r_t$ sao os retornos e $L_t = -r_t$ sao as perdas.

### VaR Parametrico

Combinando o modelo GARCH com uma distribuicao condicional:

$$\text{VaR}_{\alpha,t} = -(\mu_t + q_\alpha \cdot \sigma_t)$$

onde $q_\alpha$ e o quantil $\alpha$ da distribuicao padronizada e $\sigma_t$ e a volatilidade condicional do modelo GARCH.

| Distribuicao | Quantil $q_\alpha$ | Formula |
|-------------|---------------------|---------|
| Normal | $q_\alpha = \Phi^{-1}(\alpha)$ | $\text{VaR}_{\alpha,t} = \mu_t + \sigma_t \cdot \Phi^{-1}(\alpha)$ |
| Student-t($\nu$) | $q_\alpha = t_\nu^{-1}(\alpha) \cdot \sqrt{\frac{\nu-2}{\nu}}$ | $\text{VaR}_{\alpha,t} = \mu_t + \sigma_t \cdot t_\nu^{-1}(\alpha) \cdot \sqrt{\frac{\nu-2}{\nu}}$ |

!!! note "Convencao de sinal"
    No archbox, o VaR e retornado como **valor negativo** para perdas. Um VaR de $-0.025$ significa que a perda maxima esperada e de 2.5% do valor da posicao.

### VaR Historico

Baseado no quantil empirico dos retornos observados em uma janela rolante:

$$\text{VaR}_{\alpha,t}^{HS} = \text{Quantil}(r_{t-W+1}, \ldots, r_t; \alpha)$$

onde $W$ e o tamanho da janela (tipicamente 250 dias $\approx$ 1 ano).

### VaR por Filtered Historical Simulation (FHS)

Combinacao da dinamica GARCH com a distribuicao empirica dos residuos padronizados (Barone-Adesi et al., 1999):

1. Padronizar os residuos: $z_t = \frac{r_t - \mu}{\sigma_t}$
2. Calcular o quantil empirico dos $z$: $q_\alpha^z = \text{Quantil}(z_1, \ldots, z_{t-1}; \alpha)$
3. Re-escalar: $\text{VaR}_{\alpha,t}^{FHS} = \mu + \sigma_t \cdot q_\alpha^z$

!!! tip "Vantagem do FHS"
    O FHS combina o melhor dos dois mundos: a **dinamica temporal** do GARCH com a **distribuicao empirica** dos residuos (sem necessidade de assumir Normal ou Student-t).

### VaR por Monte Carlo

1. Estimar o modelo GARCH e extrair os parametros
2. Simular $N$ caminhos de $\sigma^2_{T+h}$ e $r_{T+h}$
3. $\text{VaR}_{\alpha} = \text{Quantil}(\{r_{T+h}^{(1)}, \ldots, r_{T+h}^{(N)}\}; \alpha)$

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\alpha$ | Nivel de significancia | $0 < \alpha < 1$ (tipico: 0.01 ou 0.05) |
| $W$ | Janela para VaR historico | $W \geq 30$ (tipico: 250) |
| $N$ | Numero de simulacoes MC | $N \geq 1000$ (tipico: 10000) |
| $\nu$ | Graus de liberdade (Student-t) | $\nu > 2$ |

## Quick Example

```python
from archbox import GARCH
from archbox.risk import ValueAtRisk
from archbox.datasets import load_dataset

# Estimar GARCH(1,1)
sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()

# VaR parametrico a 5%
var = ValueAtRisk(results, alpha=0.05)
var_series = var.parametric(dist='normal')
print(f"VaR medio: {var_series.mean():.6f}")
print(f"VaR minimo (pior dia): {var_series.min():.6f}")
```

??? example "Output esperado"
    ```
    VaR medio: -0.018234
    VaR minimo (pior dia): -0.065412
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | ArchResults | obrigatorio | Resultados de um modelo ajustado (GARCH, EGARCH, GJR-GARCH, EWMA) |
| `alpha` | float | `0.05` | Nivel de significancia (0.05 = VaR a 95%) |

### Metodos

| Metodo | Parametros | Descricao |
|--------|-----------|-----------|
| `parametric(dist, nu)` | `dist='normal'`, `nu=8.0` | VaR parametrico (Normal ou Student-t) |
| `historical(window)` | `window=250` | VaR por simulacao historica |
| `filtered_historical()` | -- | VaR por FHS (Barone-Adesi et al.) |
| `monte_carlo(n_sims, horizon, seed)` | `n_sims=10000`, `horizon=1` | VaR por Monte Carlo |

### Exemplo Completo: Tres Abordagens

```python
import numpy as np
from archbox import GARCH
from archbox.risk import ValueAtRisk
from archbox.datasets import load_dataset

# 1. Estimar modelo de volatilidade
sp500 = load_dataset('sp500')
returns = sp500['returns']
model = GARCH(returns, p=1, q=1)
results = model.fit()

# 2. Inicializar calculadora de VaR
var = ValueAtRisk(results, alpha=0.05)

# 3a. VaR Parametrico (Normal)
var_normal = var.parametric(dist='normal')
print("=== VaR Parametrico (Normal) ===")
print(f"  Media:  {var_normal[~np.isnan(var_normal)].mean():.6f}")
print(f"  Min:    {np.nanmin(var_normal):.6f}")

# 3b. VaR Parametrico (Student-t)
var_t = var.parametric(dist='studentt', nu=6.0)
print("\n=== VaR Parametrico (Student-t, nu=6) ===")
print(f"  Media:  {var_t[~np.isnan(var_t)].mean():.6f}")
print(f"  Min:    {np.nanmin(var_t):.6f}")

# 3c. VaR Historico
var_hist = var.historical(window=250)
valid = ~np.isnan(var_hist)
print("\n=== VaR Historico (window=250) ===")
print(f"  Media:  {var_hist[valid].mean():.6f}")
print(f"  Min:    {var_hist[valid].min():.6f}")

# 3d. VaR Filtered Historical Simulation
var_fhs = var.filtered_historical()
valid_fhs = ~np.isnan(var_fhs)
print("\n=== VaR FHS ===")
print(f"  Media:  {var_fhs[valid_fhs].mean():.6f}")
print(f"  Min:    {var_fhs[valid_fhs].min():.6f}")

# 3e. VaR Monte Carlo (proximo periodo)
var_mc = var.monte_carlo(n_sims=10000, horizon=1, seed=42)
print(f"\n=== VaR Monte Carlo (1 dia) ===")
print(f"  VaR:    {var_mc[0]:.6f}")
```

### Comparacao das Abordagens

| Abordagem | Vantagens | Desvantagens | Uso Tipico |
|-----------|-----------|-------------|------------|
| **Parametrico** | Rapido, forward-looking, aproveitando GARCH | Depende da distribuicao assumida | Relatorios diarios, monitoramento |
| **Historico** | Nao-parametrico, simples | Backward-looking, sensivel a janela | Baseline, validacao cruzada |
| **FHS** | Dinamica GARCH + distribuicao empirica | Requer modelo GARCH bem ajustado | Melhor pratica para fat tails |
| **Monte Carlo** | Flexivel, multi-horizonte | Computacionalmente caro | Derivativos, portfolios complexos |

## Interpretacao

### Leitura do VaR

Um VaR de $-0.025$ a $\alpha = 0.05$ significa:

> "Com 95% de confianca, a perda diaria nao excedera 2.5% do valor da posicao."

Equivalentemente: "Em 1 a cada 20 dias de negociacao, esperamos uma perda **maior** que 2.5%."

### Niveis de Confianca Tipicos

| Nivel $1 - \alpha$ | $\alpha$ | Uso |
|---------------------|----------|-----|
| 95% | 0.05 | Gestao interna, limites de mesa |
| 99% | 0.01 | Basel II/III (regulatorio) |
| 97.5% | 0.025 | Basel III (ES correspondente) |

### VaR Condicional vs Incondicional

```python
# VaR Condicional: varia no tempo (usa sigma_t do GARCH)
var_cond = var.parametric(dist='normal')  # serie temporal

# VaR Incondicional: constante (usa volatilidade amostral)
import numpy as np
from scipy import stats
vol_sample = np.std(returns)
var_uncond = stats.norm.ppf(0.05) * vol_sample
print(f"VaR incondicional: {var_uncond:.6f}")
print(f"VaR condicional (media): {var_cond.mean():.6f}")
```

!!! note "VaR condicional e superior"
    O VaR condicional baseado em GARCH **adapta-se** a periodos de alta e baixa volatilidade, produzindo estimativas de risco mais precisas que o VaR incondicional (constante).

## Backtesting do VaR

O backtesting e essencial para validar se o modelo de VaR esta calibrado corretamente. O archbox fornece tres testes:

### Kupiec (1995) - Proportion of Failures

Testa se a taxa de violacoes observada e consistente com $\alpha$:

$$H_0: \hat{\pi} = \alpha \qquad \text{vs} \qquad H_1: \hat{\pi} \neq \alpha$$

$$LR_{POF} = -2\left[x \ln(\alpha) + (n-x)\ln(1-\alpha) - x\ln(\hat{\pi}) - (n-x)\ln(1-\hat{\pi})\right] \sim \chi^2(1)$$

### Christoffersen (1998) - Conditional Coverage

Testa cobertura E independencia das violacoes:

$$LR_{CC} = LR_{POF} + LR_{ind} \sim \chi^2(2)$$

### Basel Traffic Light

| Zona | Violacoes (250 dias, 1%) | Penalidade |
|------|--------------------------|-----------|
| Verde | 0--4 | Nenhuma |
| Amarelo | 5--9 | Multiplicador de capital aumentado |
| Vermelho | 10+ | Investigacao regulatoria |

### Exemplo de Backtesting

```python
from archbox import GARCH
from archbox.risk import ValueAtRisk, VaRBacktest
from archbox.datasets import load_dataset

# 1. Modelo e VaR
sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()

var = ValueAtRisk(results, alpha=0.05)
var_series = var.parametric(dist='normal')

# 2. Backtesting
bt = VaRBacktest(sp500['returns'], var_series, alpha=0.05)

# Testes individuais
kupiec = bt.kupiec_test()
print(f"Kupiec POF: stat={kupiec.statistic:.4f}, p={kupiec.pvalue:.4f}")

chris = bt.christoffersen_test()
print(f"Christoffersen CC: stat={chris.statistic:.4f}, p={chris.pvalue:.4f}")

# Basel traffic light
traffic = bt.basel_traffic_light()
print(f"Basel Traffic Light: {traffic}")

# Violation ratio (1.0 = perfeito)
vr = bt.violation_ratio()
print(f"Violation ratio: {vr:.4f}")

# Relatorio completo
print(bt.summary())
```

??? example "Output esperado"
    ```
    ============================================================
    VaR Backtest Summary
    ============================================================
      Observations:      2000
      VaR level (alpha): 0.0500
      Violations:        98
      Violation rate:    0.0490
      Violation ratio:   0.9800

    ------------------------------------------------------------
    Statistical Tests
    ------------------------------------------------------------
      Kupiec POF: statistic=0.0412, pvalue=0.8391
      Christoffersen CC: statistic=0.5234, pvalue=0.7698

    ------------------------------------------------------------
      Basel Traffic Light: GREEN
    ============================================================
    ```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCH
    from archbox.risk import ValueAtRisk, VaRBacktest

    model = GARCH(returns, p=1, q=1)
    results = model.fit()

    var = ValueAtRisk(results, alpha=0.05)
    var_param = var.parametric(dist='normal')
    var_hist = var.historical(window=250)
    var_fhs = var.filtered_historical()
    var_mc = var.monte_carlo(n_sims=10000, seed=42)

    bt = VaRBacktest(returns, var_param, alpha=0.05)
    print(bt.summary())
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
      distribution.model = "norm"
    )

    # Rolling VaR forecast
    roll <- ugarchroll(
      spec, data = returns,
      n.ahead = 1, forecast.length = 500,
      refit.every = 25, refit.window = "moving",
      VaR.alpha = c(0.01, 0.05)
    )

    # Backtest
    report(roll, type = "VaR", VaR.alpha = 0.05, conf.level = 0.95)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model
    import numpy as np
    from scipy import stats

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='Normal')
    res = am.fit()

    # VaR manual a partir do forecast
    cond_vol = res.conditional_volatility
    var_95 = res.params['mu'] + stats.norm.ppf(0.05) * cond_vol
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| VaR Parametrico | `var.parametric()` | `quantile(roll, 0.05)` | Manual |
| VaR Historico | `var.historical()` | Manual | Manual |
| VaR FHS | `var.filtered_historical()` | `ugarchboot()` | Manual |
| VaR Monte Carlo | `var.monte_carlo()` | `ugarchsim()` + quantil | Manual |
| Kupiec Test | `bt.kupiec_test()` | `VaRTest()` (GAS) | Manual |
| Christoffersen | `bt.christoffersen_test()` | `VaRTest()` (GAS) | Manual |
| Basel Traffic | `bt.basel_traffic_light()` | Manual | Manual |

## References

- JP Morgan (1996). *RiskMetrics Technical Document*. 4th ed.
- Barone-Adesi, G., Giannopoulos, K., & Vosper, L. (1999). VaR Without Correlations for Portfolios of Derivative Securities. *Journal of Futures Markets*, 19(5), 583--602.
- McNeil, A.J., Frey, R., & Embrechts, P. (2015). *Quantitative Risk Management*. 2nd ed. Princeton University Press.
- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk Measurement Models. *Journal of Derivatives*, 3(2), 73--84.
- Christoffersen, P.F. (1998). Evaluating Interval Forecasts. *International Economic Review*, 39(4), 841--862.
- Basel Committee on Banking Supervision (2019). *Minimum Capital Requirements for Market Risk*. Bank for International Settlements.

## See Also

- [Expected Shortfall (ES/CVaR)](es.md) -- Medida coerente que captura tail risk
- [EWMA / RiskMetrics](ewma.md) -- Volatilidade sem otimizacao
- [Gestao de Risco: Overview](index.md) -- Pipeline completo de risco
- [Modelos GARCH](../garch/index.md) -- Modelos de volatilidade condicional
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao
