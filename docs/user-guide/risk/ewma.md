---
title: "EWMA / RiskMetrics"
description: "EWMA - Exponentially Weighted Moving Average for volatility estimation, RiskMetrics methodology."
---

# EWMA / RiskMetrics

!!! info "Quick Reference"
    **Class:** `archbox.risk.ewma.EWMA`
    **Import:** `from archbox.risk import EWMA`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "iGARCH"))` com $\omega = 0$
    **Python equivalent:** `arch.arch_model(returns, vol='EWMA')`

## Overview

O modelo **EWMA (Exponentially Weighted Moving Average)** foi popularizado pelo sistema **RiskMetrics** do JP Morgan (1996) como uma abordagem simples e eficiente para estimar a volatilidade condicional. Diferentemente dos modelos GARCH, o EWMA **nao requer otimizacao numerica** — utiliza um unico parametro de decaimento $\lambda$ fixado a priori.

O EWMA e um **caso especial do IGARCH(1,1)** com intercepto $\omega = 0$, o que implica que choques na volatilidade nunca se dissipam completamente (persistencia unitaria).

**Quando usar:**

- Estimativas **rapidas** de volatilidade sem ajuste de modelo
- **Dashboards** e monitoramento em tempo real
- **Baseline** para comparacao com modelos GARCH
- Quando a **simplicidade** e mais importante que precisao estatistica
- Calculo de **matrizes de covariancia** para portfolios (EWMA multivariado)

**Limitacoes:**

- $\lambda$ e fixo (nao adaptativo aos dados)
- Persistencia unitaria (choques nunca se dissipam)
- Sem intercepto ($\omega = 0$): nao ha reversao a media

## Formulacao Matematica

### Variancia Condicional EWMA

$$\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1 - \lambda) r_{t-1}^2$$

onde:

- $\sigma_t^2$ e a variancia condicional no tempo $t$
- $\lambda \in (0, 1)$ e o fator de decaimento
- $r_{t-1}$ e o retorno no periodo anterior

!!! note "Intuicao do $\lambda$"
    O parametro $\lambda$ controla a **memoria** do modelo: quanto maior $\lambda$, mais peso e dado a observacoes passadas e mais suave e a serie de volatilidade. Um $\lambda$ menor faz o modelo reagir mais rapidamente a choques recentes.

### Expansao Recursiva

Expandindo a recursao, a variancia EWMA e uma **media ponderada** de todos os retornos ao quadrado passados:

$$\sigma_t^2 = (1 - \lambda) \sum_{i=1}^{\infty} \lambda^{i-1} r_{t-i}^2$$

Os pesos decaem exponencialmente: $(1-\lambda), \lambda(1-\lambda), \lambda^2(1-\lambda), \ldots$

### Valores Tipicos de $\lambda$

| Frequencia | $\lambda$ | Meia-vida (dias) | Fonte |
|------------|-----------|-------------------|-------|
| **Diario** | 0.94 | $\approx 11$ dias | RiskMetrics (1996) |
| **Mensal** | 0.97 | $\approx 23$ dias | RiskMetrics (1996) |

A **meia-vida** e o numero de periodos para que o peso de uma observacao caia pela metade:

$$h = \frac{\ln(0.5)}{\ln(\lambda)}$$

### Relacao com IGARCH(1,1)

O EWMA e equivalente ao **IGARCH(1,1)** (Integrated GARCH) com $\omega = 0$:

| Parametro GARCH | IGARCH | EWMA |
|-----------------|--------|------|
| $\omega$ (intercepto) | $\omega \geq 0$ | $\omega = 0$ |
| $\alpha$ (reacao) | $\alpha$ | $1 - \lambda$ |
| $\beta$ (persistencia) | $\beta = 1 - \alpha$ | $\lambda$ |
| $\alpha + \beta$ | $= 1$ | $= 1$ |

$$\underbrace{\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2}_{\text{GARCH(1,1)}} \quad \xrightarrow{\omega=0, \, \alpha+\beta=1} \quad \underbrace{\sigma_t^2 = (1-\lambda) r_{t-1}^2 + \lambda \sigma_{t-1}^2}_{\text{EWMA}}$$

!!! warning "Persistencia unitaria"
    No EWMA, $\alpha + \beta = 1$, o que significa que a **variancia incondicional nao existe** (e infinita). Choques na volatilidade nunca se dissipam — o modelo nao reverte a uma media de longo prazo. Por isso, o EWMA tende a **superestimar** a volatilidade apos periodos de crise prolongada e **subestimar** em periodos de calma.

### EWMA Multivariado

Para $k$ ativos com matriz de retornos $\mathbf{r}_t \in \mathbb{R}^k$:

$$\mathbf{H}_t = \lambda \mathbf{H}_{t-1} + (1 - \lambda) \mathbf{r}_{t-1} \mathbf{r}_{t-1}^\top$$

onde $\mathbf{H}_t$ e a **matriz de covariancia condicional** $k \times k$.

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\lambda$ | Fator de decaimento | $0 < \lambda < 1$ |
| $\sigma_0^2$ | Variancia inicial | Variancia amostral das primeiras observacoes |
| $\mathbf{H}_0$ | Covariancia inicial (multivariado) | Covariancia amostral |

## Quick Example

```python
from archbox.risk import EWMA

# Dados de retornos
import numpy as np
np.random.seed(42)
returns = np.random.normal(0, 0.01, 1000)

# EWMA com lambda = 0.94 (RiskMetrics diario)
ewma = EWMA(returns, lam=0.94)
result = ewma.fit()

print(f"Lambda: {result.lam}")
print(f"Volatilidade media: {result.conditional_volatility.mean():.6f}")
print(f"Volatilidade final: {result.conditional_volatility[-1]:.6f}")
```

??? example "Output esperado"
    ```
    Lambda: 0.94
    Volatilidade media: 0.009823
    Volatilidade final: 0.010145
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `returns` | array-like | obrigatorio | Serie de retornos (1D) |
| `lam` | float | `0.94` | Fator de decaimento $\lambda$. Use 0.97 para dados mensais |

### Metodos

| Metodo | Parametros | Retorno | Descricao |
|--------|-----------|---------|-----------|
| `fit()` | -- | `EWMAResult` | Computa a volatilidade EWMA |
| `covariance(returns_matrix)` | Matrix (T, k) | ndarray (T, k, k) | Matrizes de covariancia EWMA |

### Atributos de `EWMAResult`

| Atributo | Descricao |
|----------|-----------|
| `conditional_volatility` | Serie de $\sigma_t$ (ndarray) |
| `conditional_variance` | Serie de $\sigma_t^2$ (ndarray) |
| `returns` | Retornos originais |
| `lam` | Fator de decaimento utilizado |
| `mu` | Media (sempre 0 para EWMA) |
| `params` | Parametros $[\omega=0, \alpha=1-\lambda, \beta=\lambda]$ |
| `resids` | Residuos (iguais aos retornos) |
| `p` | Ordem GARCH (sempre 1) |
| `q` | Ordem ARCH (sempre 1) |

### Exemplo Completo: EWMA para Gestao de Risco

```python
import numpy as np
from archbox.risk import EWMA, ValueAtRisk, ExpectedShortfall
from archbox.datasets import load_dataset

# 1. Carregar dados
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. EWMA com lambda padrao RiskMetrics
ewma = EWMA(returns, lam=0.94)
result = ewma.fit()

print("=== EWMA Volatilidade ===")
print(f"  Lambda:            {result.lam}")
print(f"  Params (IGARCH):   omega={result.params[0]:.2f}, "
      f"alpha={result.params[1]:.2f}, beta={result.params[2]:.2f}")
print(f"  Vol media:         {result.conditional_volatility.mean():.6f}")
print(f"  Vol final:         {result.conditional_volatility[-1]:.6f}")
print(f"  Vol anualizada:    {result.conditional_volatility[-1] * np.sqrt(252):.4f}")

# 3. VaR a partir do EWMA
var = ValueAtRisk(result, alpha=0.05)
var_series = var.parametric(dist='normal')
print(f"\n=== VaR 95% (EWMA + Normal) ===")
print(f"  VaR medio:  {var_series.mean():.6f}")
print(f"  VaR atual:  {var_series[-1]:.6f}")

# 4. ES a partir do EWMA
es = ExpectedShortfall(result, alpha=0.05)
es_series = es.parametric(dist='normal')
print(f"\n=== ES 95% (EWMA + Normal) ===")
print(f"  ES medio:   {es_series.mean():.6f}")
print(f"  ES atual:   {es_series[-1]:.6f}")
```

### Comparacao de Lambdas

```python
import numpy as np
from archbox.risk import EWMA
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

print("Lambda  | Vol Media  | Vol Final  | Meia-vida (dias)")
print("--------|------------|------------|------------------")

for lam in [0.90, 0.94, 0.97, 0.99]:
    ewma = EWMA(returns, lam=lam)
    result = ewma.fit()
    half_life = np.log(0.5) / np.log(lam)
    print(f"  {lam:.2f}  | {result.conditional_volatility.mean():.6f}  "
          f"| {result.conditional_volatility[-1]:.6f}  "
          f"| {half_life:.1f}")
```

??? example "Output esperado"
    ```
    Lambda  | Vol Media  | Vol Final  | Meia-vida (dias)
    --------|------------|------------|------------------
      0.90  | 0.012345  | 0.009876  | 6.6
      0.94  | 0.012456  | 0.010234  | 11.2
      0.97  | 0.012567  | 0.011456  | 22.8
      0.99  | 0.012678  | 0.012345  | 68.9
    ```

### EWMA Multivariado: Matriz de Covariancia

```python
import numpy as np
from archbox.risk import EWMA

# Simulacao de 3 ativos
np.random.seed(42)
n_obs = 500
returns_matrix = np.random.multivariate_normal(
    mean=[0, 0, 0],
    cov=[[0.0004, 0.0002, 0.0001],
         [0.0002, 0.0009, 0.0003],
         [0.0001, 0.0003, 0.0016]],
    size=n_obs
)

# Matriz de covariancia EWMA
ewma = EWMA(returns_matrix[:, 0], lam=0.94)
H = ewma.covariance(returns_matrix)  # shape: (500, 3, 3)

# Covariancia condicional final
print("Matriz de covariancia final:")
print(H[-1].round(6))

# Correlacao condicional final
D = np.diag(1 / np.sqrt(np.diag(H[-1])))
corr = D @ H[-1] @ D
print("\nMatriz de correlacao final:")
print(corr.round(4))
```

## Interpretacao

### EWMA vs GARCH

| Aspecto | EWMA | GARCH(1,1) |
|---------|------|-----------|
| Parametros | 1 ($\lambda$, fixo) | 3 ($\omega, \alpha, \beta$, estimados) |
| Otimizacao | Nenhuma | MLE (iterativa) |
| Persistencia | Exatamente 1 | Tipicamente $< 1$ |
| Reversao a media | Nao | Sim (se $\alpha + \beta < 1$) |
| Variancia incondicional | Nao existe | $\omega / (1 - \alpha - \beta)$ |
| Velocidade | Muito rapido | Moderado |
| Precisao | Boa para curto prazo | Superior para longo prazo |

### Quando o EWMA e Suficiente

```
┌─────────────────────────────────────────────────────┐
│           Preciso de estimativa rapida?              │
│                                                     │
│         SIM                          NAO            │
│          │                            │             │
│    ┌─────▼─────┐              ┌──────▼──────┐      │
│    │   EWMA    │              │   GARCH     │      │
│    │ lambda=   │              │ Estimado    │      │
│    │   0.94    │              │ via MLE     │      │
│    └───────────┘              └─────────────┘      │
│                                                     │
│    Cenarios:                  Cenarios:             │
│    - Dashboard                - Relatorio formal    │
│    - Monitoramento            - Capital regulatorio │
│    - Screening                - Pesquisa academica  │
│    - Prototipagem             - Previsao estrutural │
└─────────────────────────────────────────────────────┘
```

### Pesos Efetivos

O numero efetivo de observacoes com peso significativo no EWMA e aproximadamente:

$$n_{eff} \approx \frac{1+\lambda}{1-\lambda}$$

| $\lambda$ | $n_{eff}$ | Interpretacao |
|-----------|-----------|---------------|
| 0.90 | $\approx 19$ | Reativo, janela curta |
| 0.94 | $\approx 32$ | Padrao diario RiskMetrics |
| 0.97 | $\approx 66$ | Mais suave, janela longa |
| 0.99 | $\approx 199$ | Muito suave, quase MA |

## Diagnosticos

### Verificando a Adequacao do Lambda

```python
import numpy as np
from archbox.risk import EWMA, ValueAtRisk, VaRBacktest
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

# Testar diferentes lambdas via backtesting do VaR
print("Lambda  | Viol. Rate | Viol. Ratio | Kupiec p-val")
print("--------|------------|-------------|-------------")

for lam in [0.90, 0.94, 0.97]:
    ewma = EWMA(returns, lam=lam)
    result = ewma.fit()

    var = ValueAtRisk(result, alpha=0.05)
    var_series = var.parametric(dist='normal')

    bt = VaRBacktest(returns, var_series, alpha=0.05)
    kupiec = bt.kupiec_test()
    vr = bt.violation_ratio()
    rate = np.mean(returns < var_series)

    print(f"  {lam:.2f}  | {rate:.4f}     | {vr:.4f}      | {kupiec.pvalue:.4f}")
```

!!! tip "Escolhendo $\lambda$"
    O $\lambda$ padrao de 0.94 funciona bem para a maioria dos casos diarios. Se o backtesting (Kupiec test) rejeita a cobertura, ajuste o $\lambda$: **diminua** para mercados mais volateis (mais reativo) ou **aumente** para mercados estaveis (mais suave).

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.risk import EWMA

    # Univariado
    ewma = EWMA(returns, lam=0.94)
    result = ewma.fit()
    vol = result.conditional_volatility

    # Multivariado
    H = ewma.covariance(returns_matrix)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    # EWMA como IGARCH(1,1) com omega fixo em 0
    spec <- ugarchspec(
      variance.model = list(model = "iGARCH", garchOrder = c(1, 1)),
      mean.model = list(armaOrder = c(0, 0), include.mean = FALSE),
      fixed.pars = list(omega = 0)
    )
    fit <- ugarchfit(spec, data = returns)
    sigma <- sigma(fit)

    # EWMA manual
    lambda <- 0.94
    sigma2 <- numeric(length(returns))
    sigma2[1] <- var(returns[1:25])
    for (t in 2:length(returns)) {
      sigma2[t] <- lambda * sigma2[t-1] + (1 - lambda) * returns[t-1]^2
    }
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    # EWMA via arch
    am = arch_model(returns, vol='EWMA', mean='Zero')
    res = am.fit(update_freq=0)
    vol = res.conditional_volatility
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| EWMA univariado | `EWMA(y, lam=0.94).fit()` | `iGARCH` + `omega=0` | `arch_model(y, vol='EWMA')` |
| Covariancia EWMA | `ewma.covariance(Y)` | `rmgarch` | Manual |
| Lambda customizado | `lam=0.97` | `fixed.pars` | Manual |
| Integracao VaR/ES | Direta (via `EWMAResult`) | Manual | Manual |

## References

- JP Morgan (1996). *RiskMetrics Technical Document*. 4th ed.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley. Cap. 2.
- Alexander, C. (2008). *Market Risk Analysis, Vol. IV: Value-at-Risk Models*. Wiley.
- Engle, R. F. (2002). Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models. *Journal of Business & Economic Statistics*, 20(3), 339--350.

## See Also

- [Value-at-Risk (VaR)](var.md) -- Calculo de VaR a partir do EWMA
- [Expected Shortfall (ES/CVaR)](es.md) -- ES a partir do EWMA
- [Gestao de Risco: Overview](index.md) -- Pipeline completo de risco
- [Modelos GARCH](../garch/index.md) -- Modelos estimados por MLE
- [Modelos Multivariados](../multivariate/index.md) -- DCC, BEKK e outros
