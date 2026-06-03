---
title: "EGARCH"
description: "Exponential GARCH model - models the log of conditional variance, capturing the leverage effect without parameter sign constraints."
---

# EGARCH

!!! info "Quick Reference"
    **Class:** `archbox.models.egarch.EGARCH`
    **Import:** `from archbox import EGARCH`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "eGARCH", garchOrder = c(1,1)))`
    **Python equivalent:** `arch.arch_model(returns, vol='EGARCH', p=1, q=1)`

## Overview

O modelo EGARCH (Exponential GARCH), proposto por **Nelson (1991)**, modela o **logaritmo** da variancia condicional ao inves da variancia diretamente. Esta formulacao traz duas vantagens fundamentais sobre o GARCH simetrico:

1. **Positividade garantida**: Como $\log(\sigma_t^2)$ pode assumir qualquer valor real, $\sigma_t^2 = \exp(\log(\sigma_t^2)) > 0$ automaticamente -- nao ha necessidade de impor restricoes de nao-negatividade nos parametros.
2. **Efeito de alavancagem (leverage effect)**: O modelo captura a assimetria empirica onde choques negativos (quedas de preco) aumentam mais a volatilidade que choques positivos de mesma magnitude. Este fenomeno, documentado por Black (1976), e ubiquo em mercados acionarios.

**Quando usar:**

- Series financeiras onde choques negativos geram mais volatilidade que positivos
- Quando se deseja evitar restricoes de positividade nos parametros
- Modelagem de indices de acoes e ativos com forte efeito leverage
- Quando o sign bias test rejeita simetria no modelo GARCH padrao

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

onde $r_t$ sao os retornos, $\mu$ e a media condicional, $\sigma_t$ e o desvio-padrao condicional, e $z_t$ sao inovacoes padronizadas.

### Equacao da Variancia Condicional

$$\log(\sigma_t^2) = \omega + \sum_{i=1}^{q} \left[\alpha_i z_{t-i} + \gamma_i \left(|z_{t-i}| - E|z_{t-i}|\right)\right] + \sum_{j=1}^{p} \beta_j \log(\sigma_{t-j}^2)$$

onde:

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto (nivel base do log-variancia) | Nenhuma (pode ser negativo) |
| $\alpha_i$ | Coeficientes de assimetria (efeito do sinal do choque) | Nenhuma |
| $\gamma_i$ | Coeficientes de magnitude (efeito do tamanho do choque) | Nenhuma |
| $\beta_j$ | Coeficientes de persistencia | $\|\beta_j\| < 1$ |
| $p$ | Ordem GARCH (lags do log-variancia) | $p \geq 1$ |
| $q$ | Ordem ARCH (lags dos choques) | $q \geq 1$ |

Para a distribuicao Normal, $E|z_t| = \sqrt{2/\pi} \approx 0.7979$.

**Condicao de estacionariedade:** $\sum_{j=1}^{p} |\beta_j| < 1$

### Caso Especial: EGARCH(1,1)

O caso mais utilizado na pratica:

$$\log(\sigma_t^2) = \omega + \alpha z_{t-1} + \gamma (|z_{t-1}| - E|z_{t-1}|) + \beta \log(\sigma_{t-1}^2)$$

**Interpretacao do efeito leverage:**

- Para um choque **negativo** ($z_{t-1} < 0$): o impacto e $(\gamma - \alpha)|z_{t-1}|$
- Para um choque **positivo** ($z_{t-1} > 0$): o impacto e $(\gamma + \alpha)|z_{t-1}|$
- Se $\alpha < 0$, choques negativos aumentam mais a volatilidade -- efeito leverage

### News Impact Curve

A **News Impact Curve** (NIC) mostra como a volatilidade condicional $\sigma_t^2$ responde a choques de diferentes sinais e magnitudes, mantendo a informacao passada constante. Para o EGARCH(1,1):

$$\sigma_t^2 = A \cdot \exp\left((\gamma + \alpha) z_{t-1}\right), \quad z_{t-1} > 0$$

$$\sigma_t^2 = A \cdot \exp\left((\gamma - \alpha) z_{t-1}\right), \quad z_{t-1} < 0$$

onde $A = \exp\left(\omega + \beta \log(\sigma_{t-1}^2) - \gamma E|z_{t-1}|\right)$ e uma constante.

```
Volatilidade (σ²)
     │
     │    ╲                EGARCH
     │     ╲             ╱
     │      ╲          ╱
     │       ╲       ╱    GARCH simetrico
     │        ╲    ╱    ╱
     │         ╲ ╱   ╱
     │          ╳  ╱
     │        ╱ ╲╱
     │      ╱
     │    ╱
     │  ╱
     ├──────────────────────── Choque (ε)
   Negativo    0    Positivo
```

!!! note "Interpretacao da NIC"
    No GARCH simetrico, a NIC e uma parabola simetrica: choques positivos e negativos de mesma magnitude geram o mesmo aumento de volatilidade.
    No EGARCH, a curva e **assimetrica e exponencial**: o lado esquerdo (choques negativos) e mais ingreme, refletindo o efeito leverage. A resposta exponencial tambem significa que choques muito grandes tem impacto proporcionalmente maior do que no GARCH padrao.

## Quick Example

```python
from archbox import EGARCH
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar EGARCH(1,1)
model = EGARCH(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            EGARCH
    Distribution:     Normal
    Observations:     2000
    Log-Likelihood:   3148.2341
    AIC:              -6288.4682
    BIC:              -6265.8923
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega            -0.125432     0.031245      -4.0145       0.0001
    alpha[1]         -0.098765     0.018432      -5.3578       0.0000
    gamma[1]          0.142345     0.023456       6.0686       0.0000
    beta[1]           0.982456     0.005678     173.0482       0.0000
    ----------------------------------------------------------------------
    Persistence:      0.982456
    Half-life:        38.96 periods
    Uncond. Variance: 8.543e-04
    Uncond. Vol:      2.923e-02
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de retornos |
| `p` | int | `1` | Ordem GARCH (lags de $\log(\sigma^2)$) |
| `q` | int | `1` | Ordem ARCH (lags dos choques padronizados) |
| `mean` | str | `"constant"` | Modelo de media: `"constant"` ou `"zero"` |
| `dist` | str | `"normal"` | Distribuicao condicional: `"normal"` |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"mle"` | Metodo de estimacao |
| `starting_values` | ndarray | `None` | Valores iniciais customizados |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Exemplo Completo

```python
from archbox import EGARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test, sign_bias_test

# 1. Carregar dados
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. Estimar EGARCH(1,1)
model = EGARCH(returns, p=1, q=1)
results = model.fit()

# 3. Extrair parametros
print(f"omega:  {results.params[0]:.6f}")
print(f"alpha:  {results.params[1]:.6f}")  # efeito de sinal (assimetria)
print(f"gamma:  {results.params[2]:.6f}")  # efeito de magnitude
print(f"beta:   {results.params[3]:.6f}")  # persistencia

# 4. Metricas de volatilidade
print(f"\nPersistencia: {results.persistence():.6f}")
print(f"Meia-vida: {results.half_life():.1f} periodos")
print(f"Variancia incondicional: {results.unconditional_variance():.6e}")

# 5. Previsao
forecast = results.forecast(horizon=10)
print("\nVolatilidade prevista (proximos 10 dias):")
print(forecast['volatility'])
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros estimados (ndarray) |
| `results.se` | Erros-padrao robustos (Bollerslev-Wooldridge) |
| `results.tvalues` | Estatisticas t |
| `results.pvalues` | p-valores bilaterais |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |
| `results.conditional_volatility` | Serie de $\sigma_t$ |
| `results.resid` | Residuos padronizados ($z_t = \epsilon_t / \sigma_t$) |

| Metodo | Descricao |
|--------|-----------|
| `results.persistence()` | $\beta$ (persistencia no log-variancia) |
| `results.half_life()` | Meia-vida dos choques de volatilidade |
| `results.unconditional_variance()` | Variancia incondicional de longo prazo |
| `results.forecast(horizon)` | Previsao de variancia/volatilidade |
| `results.summary()` | Tabela formatada de resultados |
| `results.plot("volatility")` | Grafico de retornos e volatilidade |
| `results.plot("residuals")` | Grafico de residuos padronizados |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### Efeito Leverage (Parametro $\alpha$)

O parametro $\alpha$ captura a **assimetria** na resposta da volatilidade:

| Valor de $\alpha$ | Interpretacao |
|-------------------|---------------|
| $\alpha < 0$ | Efeito leverage: choques negativos aumentam mais a volatilidade |
| $\alpha = 0$ | Sem assimetria (equivalente a modelo simetrico) |
| $\alpha > 0$ | Efeito inverso (raro em acoes, possivel em commodities) |

Para um EGARCH(1,1) com $\alpha = -0.10$ e $\gamma = 0.14$:

- **Choque negativo** de magnitude 1: impacto no log-variancia = $0.14 - (-0.10) = 0.24$
- **Choque positivo** de magnitude 1: impacto no log-variancia = $0.14 + (-0.10) = 0.04$
- Choques negativos tem **6x mais impacto** que positivos neste exemplo

### Persistencia

No EGARCH, a persistencia e controlada diretamente por $\beta$:

$$\text{Persistencia} = |\beta|$$

| Valor | Interpretacao |
|-------|---------------|
| $< 0.95$ | Persistencia moderada |
| $0.95 - 0.999$ | Alta persistencia -- tipico de retornos diarios |
| $\approx 1.0$ | Persistencia unitaria (IEGARCH) |

### Meia-Vida

$$\text{Meia-vida} = \frac{\ln(0.5)}{\ln(|\beta|)}$$

```python
persistence = results.persistence()
hl = results.half_life()
print(f"Persistencia: {persistence:.6f}")
print(f"Meia-vida: {hl:.1f} periodos")
```

### Comparacao EGARCH vs GJR-GARCH

| Criterio | EGARCH | GJR-GARCH |
|----------|--------|-----------|
| **Formulacao** | Log-variancia (aditiva) | Variancia (multiplicativa) |
| **Restricoes** | Nenhuma restricao de sinal | $\omega > 0$, $\alpha \geq 0$, $\beta \geq 0$ |
| **Leverage** | Via parametro $\alpha$ | Via parametro $\gamma$ e indicadora |
| **NIC** | Exponencial assimetrica | Linear por partes (piecewise) |
| **Choques extremos** | Resposta exponencial (maior impacto) | Resposta quadratica |
| **Interpretacao** | Mais complexa | Mais intuitiva |
| **Quando preferir** | Fortes assimetrias, sem problemas de restricao | Interpretacao direta do leverage |

!!! tip "Regra pratica"
    - Use **EGARCH** quando o sign bias test indica forte assimetria e voce quer flexibilidade maxima sem se preocupar com restricoes de positividade.
    - Use **GJR-GARCH** quando a interpretacao economica do parametro de leverage e importante e as restricoes de positividade nao sao problematicas.

## Diagnosticos

### Ljung-Box nos Residuos Padronizados ao Quadrado

```python
from archbox.diagnostics import ljung_box_test

lb_result = ljung_box_test(results.resid**2, lags=10)
print(f"Ljung-Box Q(10): {lb_result.statistic:.4f}")
print(f"p-valor: {lb_result.pvalue:.4f}")
# p > 0.05 -> modelo capturou a dinamica da variancia
```

### Teste ARCH-LM

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(results.resid, lags=5)
print(f"ARCH-LM(5): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
```

### Sign Bias Test

Apos estimar o EGARCH, o sign bias test deve **nao rejeitar** -- indicando que o modelo capturou a assimetria:

```python
from archbox.diagnostics import sign_bias_test

sb_result = sign_bias_test(results.resid)
print(sb_result)
# p > 0.05 -> assimetria capturada pelo EGARCH
```

!!! tip "Interpretacao"
    Se o sign bias test **rejeita** mesmo apos o EGARCH, considere:

    - Aumentar a ordem (p,q)
    - Usar distribuicao de caudas pesadas (`dist="studentt"`)
    - Verificar se ha mudancas estruturais na serie

### Workflow Completo de Diagnostico

```python
from archbox import EGARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test, sign_bias_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = EGARCH(sp500['returns'], p=1, q=1)
results = model.fit()

# 2. Residuos padronizados
z = results.resid

# 3. Diagnosticos
print("=== Ljung-Box (z^2) ===")
lb = ljung_box_test(z**2, lags=10)
print(f"  Q(10) = {lb.statistic:.4f}, p = {lb.pvalue:.4f}")

print("\n=== ARCH-LM ===")
lm = arch_lm_test(z, lags=5)
print(f"  LM(5) = {lm.statistic:.4f}, p = {lm.pvalue:.4f}")

print("\n=== Sign Bias ===")
sb = sign_bias_test(z)
print(f"  {sb}")

# 4. Visualizacao
results.plot("volatility")
results.plot("residuals")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import EGARCH
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = EGARCH(sp500['returns'], p=1, q=1)
    results = model.fit()
    print(results.summary())

    # Previsao
    forecast = results.forecast(horizon=10)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "eGARCH", garchOrder = c(1, 1)),
      mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
      distribution.model = "norm"
    )

    fit <- ugarchfit(spec = spec, data = returns)
    show(fit)

    # News impact curve
    ni <- newsimpact(fit)
    plot(ni)

    # Previsao
    forecast <- ugarchforecast(fit, n.ahead = 10)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    am = arch_model(returns, vol='EGARCH', p=1, q=1, dist='Normal')
    res = am.fit()
    print(res.summary())

    # Previsao
    forecast = res.forecast(horizon=10)
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `EGARCH(y, p=1, q=1)` | `ugarchspec(model="eGARCH")` | `arch_model(y, vol='EGARCH')` |
| Estimacao | `model.fit()` | `ugarchfit(spec, data)` | `am.fit()` |
| Previsao | `results.forecast(h)` | `ugarchforecast(fit, n.ahead=h)` | `res.forecast(horizon=h)` |
| Persistencia | `results.persistence()` | `persistence(fit)` | Manual |
| Meia-vida | `results.half_life()` | Manual | Manual |
| News Impact | `results.plot("nic")` | `newsimpact(fit)` | Manual |

## References

- Nelson, D. B. (1991). Conditional Heteroskedasticity in Asset Returns: A New Approach. *Econometrica*, 59(2), 347--370.
- Black, F. (1976). Studies of Stock Market Volatility Changes. *Proceedings of the American Statistical Association, Business and Economic Statistics Section*, 177--181.
- Engle, R. F., & Ng, V. K. (1993). Measuring and Testing the Impact of News on Volatility. *The Journal of Finance*, 48(5), 1749--1778.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo simetrico padrao
- [GJR-GARCH](gjr-garch.md) -- Modelo assimetrico com indicadora
- [APARCH](aparch.md) -- Modelo assimetrico de potencia generalizada
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: Sign Bias](../../diagnostics/sign-bias.md) -- Teste de assimetria nos residuos
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
