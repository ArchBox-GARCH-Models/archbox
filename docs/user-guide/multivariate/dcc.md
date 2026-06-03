---
title: "DCC-GARCH"
description: "Dynamic Conditional Correlation GARCH — modelo de correlacao dinamica escalavel para portfolios multivariados."
---

# DCC-GARCH (Dynamic Conditional Correlation)

!!! info "Quick Reference"
    **Class:** `archbox.multivariate.DCC`
    **Import:** `from archbox.multivariate import DCC`
    **R equivalent:** `rmgarch::dccspec(uspec, dccOrder = c(1, 1))`
    **Python equivalent:** Nao disponivel no pacote `arch`

## Overview

O modelo DCC (Dynamic Conditional Correlation), proposto por **Engle (2002)**, e o modelo multivariado mais popular em financas empiricas. Ele combina a flexibilidade de volatilidades dinamicas individuais com uma estrutura parcimoniosa para a correlacao condicional.

A ideia central e a **estimacao em dois passos**:

1. **Passo 1**: Estimar um modelo GARCH univariado para cada serie, obtendo as volatilidades condicionais $\sigma_{i,t}$ e os residuos padronizados $z_{i,t} = \epsilon_{i,t} / \sigma_{i,t}$
2. **Passo 2**: Modelar a dinamica da correlacao entre os residuos padronizados usando uma recursao tipo GARCH

Essa abordagem torna o DCC **escalavel** para dezenas ou centenas de ativos, pois o numero de parametros de correlacao e fixo (apenas 2: $a$ e $b$), independentemente do numero de series.

**Quando usar:**

- Portfolio com 5+ ativos onde correlacoes variam ao longo do tempo
- Hedge ratios dinamicos entre multiplos ativos
- Value-at-Risk de portfolio com correlacoes condicionais
- Estudo de contágio e spillover entre mercados

## Formulacao Matematica

### Decomposicao da Covariancia

A matriz de covariancia condicional e decomposta como:

$$H_t = D_t R_t D_t$$

onde $D_t = \text{diag}(\sigma_{1,t}, \ldots, \sigma_{k,t})$ e a matriz diagonal de volatilidades condicionais (estimadas no Passo 1) e $R_t$ e a matriz de correlacao condicional dinamica.

### Recursao DCC

A correlacao dinamica e modelada atraves de uma matriz auxiliar $Q_t$:

$$Q_t = (1 - a - b)\bar{Q} + a \, z_{t-1} z_{t-1}' + b \, Q_{t-1}$$

onde:

| Simbolo | Descricao |
|---------|-----------|
| $Q_t$ | Matriz de pseudo-correlacao (nao necessariamente normalizada) |
| $\bar{Q}$ | Correlacao incondicional dos residuos padronizados: $\bar{Q} = \frac{1}{T}\sum_{t=1}^{T} z_t z_t'$ |
| $z_t$ | Vetor de residuos padronizados $(z_{1,t}, \ldots, z_{k,t})'$ |
| $a$ | Parametro de reacao: impacto dos choques recentes na correlacao |
| $b$ | Parametro de persistencia: suavizacao da correlacao |

### Normalizacao

Como $Q_t$ nao e necessariamente uma matriz de correlacao valida, ela e normalizada:

$$R_t = \text{diag}(Q_t)^{-1/2} \, Q_t \, \text{diag}(Q_t)^{-1/2}$$

Isso garante que $R_t$ tenha uns na diagonal e elementos entre $-1$ e $1$.

### Restricoes

| Parametro | Restricao | Justificativa |
|-----------|-----------|---------------|
| $a$ | $a > 0$ | Correlacao reage a choques |
| $b$ | $b > 0$ | Correlacao e persistente |
| $a + b$ | $a + b < 1$ | Estacionariedade da correlacao |

### Log-Verossimilhanca

A log-verossimilhanca do DCC pode ser decomposta em duas partes:

$$\ell(\theta) = \ell_{\text{vol}}(\theta_1) + \ell_{\text{corr}}(\theta_2)$$

onde:

$$\ell_{\text{vol}}(\theta_1) = -\frac{1}{2} \sum_{t=1}^{T} \left( k \ln(2\pi) + 2 \ln|D_t| + \epsilon_t' D_t^{-2} \epsilon_t \right)$$

$$\ell_{\text{corr}}(\theta_2) = -\frac{1}{2} \sum_{t=1}^{T} \left( \ln|R_t| + z_t' R_t^{-1} z_t - z_t' z_t \right)$$

## Quick Example

```python
import numpy as np
from archbox.multivariate import DCC
from archbox.datasets import load_dataset

# Carregar retornos de portfolio de acoes
returns = load_dataset('equity_portfolio')
endog = returns[['PETR4', 'VALE3', 'ITUB4']].values

# Estimar DCC-GARCH(1,1)
model = DCC(endog, univariate_model="GARCH", univariate_order=(1, 1))
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
              Multivariate Volatility Model Results - DCC
    ======================================================================
    Model:            DCC-GARCH(1,1)
    Method:           Two-step
    Series:           3
    Observations:     2000
    Log-Likelihood:   9876.5432
    AIC:              -19741.0864
    BIC:              -19708.2345
    ----------------------------------------------------------------------
    Correlation Parameters
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    a                0.045123     0.008765       5.1481       0.0000
    b                0.938456     0.012345      76.0191       0.0000
    ----------------------------------------------------------------------
    Persistence (a+b): 0.983579

    Univariate GARCH Results
    ----------------------------------------------------------------------
    Series 0: omega=1.2e-05, alpha=0.0854, beta=0.9012
    Series 1: omega=1.5e-05, alpha=0.0923, beta=0.8945
    Series 2: omega=8.7e-06, alpha=0.0712, beta=0.9156
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | ndarray $(T, k)$ | obrigatorio | Matriz de retornos com $k$ series e $T$ observacoes |
| `univariate_model` | str | `"GARCH"` | Modelo GARCH univariado para o Passo 1 |
| `univariate_order` | tuple | `(1, 1)` | Ordem $(p, q)$ do GARCH univariado |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"two_step"` | Metodo de estimacao |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Estimacao em Dois Passos

```python
from archbox.multivariate import DCC

# Passo 1: GARCH univariado e estimado automaticamente
# Passo 2: Parametros DCC (a, b) sao estimados por MLE condicional
model = DCC(endog)
results = model.fit()

# Acessar resultados univariados
for i, univ in enumerate(results.univariate_results):
    print(f"Serie {i}: {univ.params}")
```

### Correlacao Dinamica

```python
# Matriz de correlacao condicional em cada ponto do tempo
R_t = results.dynamic_correlation  # shape: (T, k, k)

# Correlacao entre serie 0 e serie 1 ao longo do tempo
corr_01 = R_t[:, 0, 1]
print(f"Correlacao media: {corr_01.mean():.4f}")
print(f"Correlacao min:   {corr_01.min():.4f}")
print(f"Correlacao max:   {corr_01.max():.4f}")

# Visualizar
results.plot_correlation(0, 1)
```

### Covariancia Condicional e Portfolio

```python
import numpy as np

# Matriz de covariancia condicional H_t = D_t R_t D_t
H_t = results.dynamic_covariance  # shape: (T, k, k)

# Volatilidade do portfolio
weights = np.array([0.4, 0.3, 0.3])  # 40% PETR4, 30% VALE3, 30% ITUB4
port_vol = results.portfolio_volatility(weights)
print(f"Volatilidade media do portfolio: {port_vol.mean():.4f}")

# Pesos de minima variancia dinamicos
from archbox.multivariate.portfolio import minimum_variance_weights_dynamic

mvp_weights = minimum_variance_weights_dynamic(H_t)  # shape: (T, k)
print(f"Pesos MVP no ultimo dia: {mvp_weights[-1]}")
```

### Previsao

```python
# Previsao de covariancia para os proximos 10 dias
forecast = model.forecast(results, horizon=10)
print("Covariancia prevista (h=1):")
print(forecast['covariance'][0])

print("\nCorrelacao prevista (h=1):")
print(forecast['correlation'][0])
```

### Decomposicao de Risco

```python
from archbox.multivariate.portfolio import risk_decomposition

weights = np.array([0.4, 0.3, 0.3])
H_last = H_t[-1]  # Covariancia do ultimo dia

decomp = risk_decomposition(weights, H_last)
print(f"Variancia do portfolio: {decomp['portfolio_variance']:.6f}")
print(f"Volatilidade do portfolio: {decomp['portfolio_volatility']:.4f}")
print(f"Contribuicao de risco: {decomp['risk_contribution']}")
```

## Interpretacao

### Parametros DCC

| Parametro | Valor Tipico | Interpretacao |
|-----------|:---:|---------------|
| $a$ | 0.01 -- 0.10 | **Reatividade**: quanto maior, mais rapido a correlacao reage a choques recentes |
| $b$ | 0.85 -- 0.99 | **Persistencia**: quanto maior, mais lenta a reversao da correlacao |
| $a + b$ | 0.95 -- 0.99 | **Persistencia total**: proximo de 1 indica correlacao muito persistente |

!!! tip "Interpretacao Pratica"
    - **$a$ alto, $b$ baixo**: Correlacao muda rapido, volatil — tipico de mercados emergentes em crise
    - **$a$ baixo, $b$ alto**: Correlacao muda lentamente, estavel — tipico de mercados desenvolvidos
    - **$a + b \approx 1$**: Choques na correlacao sao quase permanentes (IGARCH-like)

### Correlacao Incondicional

A correlacao de longo prazo entre as series e dada por $\bar{Q}$. Compare com a correlacao amostral para verificar a consistencia:

```python
# Correlacao incondicional (de longo prazo)
Q_bar = np.corrcoef(results.std_resids.T)
print("Correlacao incondicional:")
print(Q_bar)
```

### Meia-Vida da Correlacao

A meia-vida dos choques na correlacao e:

$$\text{Meia-vida} = \frac{\ln(0.5)}{\ln(b)}$$

```python
a, b = results.params
half_life = np.log(0.5) / np.log(b)
print(f"Meia-vida dos choques na correlacao: {half_life:.1f} periodos")
```

## Diagnosticos

### Verificacao dos Residuos Padronizados

```python
from archbox.diagnostics import ljung_box_test, arch_lm_test

# Residuos padronizados multivariados
z = results.std_resids  # shape: (T, k)

# Testar cada serie individualmente
for i in range(z.shape[1]):
    lb = ljung_box_test(z[:, i]**2, lags=10)
    print(f"Serie {i} - Ljung-Box Q(10): {lb.statistic:.4f}, p={lb.pvalue:.4f}")
```

### Positiva-Definitividade

```python
from archbox.multivariate.utils import is_positive_definite

# Verificar se todas as matrizes H_t sao positiva-definidas
H_t = results.dynamic_covariance
n_non_pd = sum(not is_positive_definite(H_t[t]) for t in range(H_t.shape[0]))
print(f"Matrizes nao positiva-definidas: {n_non_pd} de {H_t.shape[0]}")
```

### Comparacao de Criterios de Informacao

```python
from archbox.multivariate import DCC, CCC

# DCC vs CCC
dcc_results = DCC(endog).fit()
ccc_results = CCC(endog).fit()

print(f"DCC - AIC: {dcc_results.aic:.4f}, BIC: {dcc_results.bic:.4f}")
print(f"CCC - AIC: {ccc_results.aic:.4f}, BIC: {ccc_results.bic:.4f}")
# AIC/BIC menor -> modelo preferido
```

Consulte [Diagnosticos Multivariados](diagnostics.md) para testes mais detalhados.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.multivariate import DCC

    model = DCC(endog, univariate_model="GARCH", univariate_order=(1, 1))
    results = model.fit()
    print(results.summary())

    # Correlacao dinamica
    results.plot_correlation(0, 1)

    # Previsao
    forecast = model.forecast(results, horizon=10)
    ```

=== "R (rmgarch)"

    ```r
    library(rugarch)
    library(rmgarch)

    # Passo 1: Especificacao univariada
    uspec <- ugarchspec(
      variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
      mean.model = list(armaOrder = c(0, 0))
    )
    mspec <- multispec(replicate(3, uspec))

    # Passo 2: Especificacao DCC
    dccspec <- dccspec(uspec = mspec, dccOrder = c(1, 1),
                       distribution = "mvnorm")

    # Estimacao
    dccfit <- dccfit(dccspec, data = returns)
    show(dccfit)

    # Correlacao dinamica
    rcor <- rcor(dccfit)

    # Previsao
    dccforecast <- dccforecast(dccfit, n.ahead = 10)
    ```

| Funcionalidade | ArchBox | rmgarch (R) |
|---------------|---------|-------------|
| Especificacao | `DCC(endog)` | `dccspec(mspec, dccOrder=c(1,1))` |
| Estimacao | `model.fit()` | `dccfit(spec, data)` |
| Correlacao | `results.dynamic_correlation` | `rcor(fit)` |
| Covariancia | `results.dynamic_covariance` | `rcov(fit)` |
| Previsao | `model.forecast(results, h)` | `dccforecast(fit, n.ahead=h)` |
| Plot correlacao | `results.plot_correlation(i, j)` | `plot(fit, which=3)` |
| Portfolio vol | `results.portfolio_volatility(w)` | Manual |

## References

- Engle, R. F. (2002). Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models. *Journal of Business & Economic Statistics*, 20(3), 339--350.
- Engle, R. F., & Sheppard, K. (2001). Theoretical and Empirical Properties of Dynamic Conditional Correlation Multivariate GARCH. *NBER Working Paper* No. 8554.
- Aielli, G. P. (2013). Dynamic Conditional Correlation: On Properties and Estimation. *Journal of Business & Economic Statistics*, 31(3), 282--299.
- Cappiello, L., Engle, R. F., & Sheppard, K. (2006). Asymmetric Dynamics in the Correlations of Global Equity and Bond Returns. *Journal of Financial Econometrics*, 4(4), 537--572.

## See Also

- [CCC](ccc.md) — Caso especial com correlacao constante
- [DECO](deco.md) — Extensao com equicorrelacao para muitos ativos
- [BEKK](bekk.md) — Alternativa que estima $H_t$ diretamente
- [Diagnosticos Multivariados](diagnostics.md) — Testes de especificacao
- [Guia de Selecao](choosing-model.md) — Quando usar DCC vs. alternativas
- [GARCH Univariado](../garch/garch.md) — Modelo do Passo 1
