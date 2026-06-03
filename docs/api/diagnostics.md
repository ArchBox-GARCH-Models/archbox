---
title: Diagnostics API
description: Testes diagnosticos para modelos GARCH - ARCH-LM, Ljung-Box, Sign Bias, Nyblom, Engle-Sheppard e Hong
---

# Diagnostics API

!!! info "Modulo"
    ```python
    from archbox.diagnostics import (
        arch_lm_test, ljung_box_squared, sign_bias_test,
        nyblom_test, engle_sheppard_test, hong_spillover_test,
        full_diagnostics, DiagnosticReport
    )
    ```

## Visao Geral

O modulo `archbox.diagnostics` fornece testes estatisticos para validar
modelos de volatilidade condicional:

| Funcao / Classe | Descricao | Hipotese Nula |
|-----------------|-----------|---------------|
| `arch_lm_test()` | Teste ARCH-LM (Engle, 1982) | Sem efeitos ARCH nos residuos |
| `ljung_box_squared()` | Ljung-Box em $z_t^2$ | Sem autocorrelacao em residuos quadrados |
| `sign_bias_test()` | Sign Bias (Engle & Ng, 1993) | Sem assimetria na volatilidade |
| `nyblom_test()` | Nyblom (1989) | Parametros estaveis ao longo do tempo |
| `engle_sheppard_test()` | Engle-Sheppard (2001) | Correlacao constante (CCC vs DCC) |
| `hong_spillover_test()` | Hong (2001) | Sem spillover de volatilidade |
| `full_diagnostics()` | Suite completa | Executa todos os testes acima |
| `DiagnosticReport` | Container de resultados | -- |

---

## Tipos de Resultado

### TestResult

::: archbox.diagnostics.arch_lm.TestResult
    options:
      show_root_heading: true
      show_source: true

Container basico retornado por `arch_lm_test()`.

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `statistic` | `float` | Estatistica do teste |
| `pvalue` | `float` | p-valor |
| `test_name` | `str` | Nome do teste |
| `lags` | `int` | Numero de lags utilizados |

### LjungBoxResult

::: archbox.diagnostics.ljung_box.LjungBoxResult
    options:
      show_root_heading: true
      show_source: true

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `statistic` | `float` | Estatistica $Q$ de Ljung-Box |
| `pvalue` | `float` | p-valor ($\chi^2$) |
| `lags` | `int` | Numero de lags |

### SignBiasResult

::: archbox.diagnostics.sign_bias.SignBiasResult
    options:
      show_root_heading: true
      show_source: true

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `sign_bias` | `tuple[float, float]` | (t-stat, p-valor) para viés de sinal |
| `neg_sign_bias` | `tuple[float, float]` | (t-stat, p-valor) para viés negativo |
| `pos_sign_bias` | `tuple[float, float]` | (t-stat, p-valor) para viés positivo |
| `joint` | `tuple[float, float]` | (F-stat, p-valor) teste conjunto |

### NyblomResult

::: archbox.diagnostics.nyblom.NyblomResult
    options:
      show_root_heading: true
      show_source: true

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `joint_statistic` | `float` | Estatistica conjunta |
| `individual_statistics` | `ndarray` | Estatisticas individuais por parametro |
| `critical_values_joint` | `dict` | Valores criticos conjuntos |
| `critical_values_individual` | `dict` | Valores criticos individuais |
| `num_params` | `int` | Numero de parametros |

### DiagnosticReport

::: archbox.diagnostics.diagnostics.DiagnosticReport
    options:
      show_root_heading: true
      show_source: true
      members:
        - summary

Container agregado retornado por `full_diagnostics()`.

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `arch_lm` | `dict[int, TestResult]` | Resultados ARCH-LM por lag |
| `sign_bias` | `SignBiasResult \| None` | Resultado do Sign Bias |
| `ljung_box_sq` | `dict[int, LjungBoxResult]` | Resultados Ljung-Box por lag |
| `nyblom` | `NyblomResult \| None` | Resultado do Nyblom |
| `jarque_bera` | `tuple[float, float] \| None` | (estatistica, p-valor) Jarque-Bera |

#### `summary()`

Gera tabela formatada com todos os resultados diagnosticos.

```python
report.summary(significance=0.05) -> str
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `significance` | `float` | `0.05` | Nivel de significancia para conclusoes |

---

## Testes Univariados

### arch_lm_test()

::: archbox.diagnostics.arch_lm.arch_lm_test
    options:
      show_root_heading: true
      show_source: true

Teste ARCH-LM de Engle (1982) para heterocedasticidade condicional.

$H_0$: Nao ha efeitos ARCH nos residuos.

Regride $\hat{z}_t^2$ em $\hat{z}_{t-1}^2, \ldots, \hat{z}_{t-q}^2$ e
calcula a estatistica $LM = T \cdot R^2$:

$$
LM = T \cdot R^2 \sim \chi^2(q)
$$

onde $T$ e o numero de observacoes e $q$ o numero de lags.

```python
arch_lm_test(resids, lags=5) -> TestResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `resids` | `array-like` | -- | Residuos padronizados do modelo |
| `lags` | `int` | `5` | Numero de lags na regressao auxiliar |

!!! tip "Interpretacao"
    - p-valor $> 0.05$: Modelo captura adequadamente os efeitos ARCH
    - p-valor $\leq 0.05$: Efeitos ARCH remanescentes -- considere aumentar a ordem do modelo

### Exemplo

```python
from archbox.models import GARCH
from archbox.diagnostics import arch_lm_test
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# Teste ARCH-LM com 5 lags
test = arch_lm_test(result.resid, lags=5)
print(f"Estatistica: {test.statistic:.4f}")
print(f"p-valor: {test.pvalue:.4f}")
print(f"Conclusao: {'Sem efeitos ARCH' if test.pvalue > 0.05 else 'Efeitos ARCH presentes'}")
```

---

### ljung_box_squared()

::: archbox.diagnostics.ljung_box.ljung_box_squared
    options:
      show_root_heading: true
      show_source: true

Teste de Ljung-Box aplicado aos residuos padronizados ao quadrado $z_t^2$.
Testa autocorrelacao serial na variancia condicional.

$H_0$: Nao ha autocorrelacao em $z_t^2$ ate o lag $m$.

$$
Q(m) = T(T+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2}{T-k} \sim \chi^2(m)
$$

onde $\hat{\rho}_k$ e a autocorrelacao amostral de $z_t^2$ no lag $k$.

```python
ljung_box_squared(std_resids, lags=10) -> LjungBoxResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `std_resids` | `array-like` | -- | Residuos padronizados $z_t$ |
| `lags` | `int` | `10` | Numero maximo de lags |

### Exemplo

```python
from archbox.models import GARCH
from archbox.diagnostics import ljung_box_squared
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

lb = ljung_box_squared(result.resid, lags=10)
print(f"Q({lb.lags}) = {lb.statistic:.4f}, p-valor = {lb.pvalue:.4f}")
```

---

### sign_bias_test()

::: archbox.diagnostics.sign_bias.sign_bias_test
    options:
      show_root_heading: true
      show_source: true

Teste de Sign Bias de Engle & Ng (1993). Verifica se choques negativos e
positivos afetam a volatilidade de forma diferente (assimetria).

Estima a regressao auxiliar:

$$
\hat{z}_t^2 = c_0 + c_1 S_{t-1}^- + c_2 S_{t-1}^- \varepsilon_{t-1} + c_3 S_{t-1}^+ \varepsilon_{t-1} + u_t
$$

onde $S_{t-1}^- = \mathbb{1}(\varepsilon_{t-1} < 0)$ e $S_{t-1}^+ = 1 - S_{t-1}^-$.

```python
sign_bias_test(resids, std_resids) -> SignBiasResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `resids` | `array-like` | -- | Residuos nao-padronizados |
| `std_resids` | `array-like` | -- | Residuos padronizados $z_t$ |

!!! warning "Quando usar"
    Se o Sign Bias for significativo, considere modelos assimetricos como
    **EGARCH** ou **GJR-GARCH** que capturam o efeito leverage.

### Exemplo

```python
from archbox.models import GARCH
from archbox.diagnostics import sign_bias_test
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

sb = sign_bias_test(result.resid, result.resid)
print(f"Sign Bias: t={sb.sign_bias[0]:.3f}, p={sb.sign_bias[1]:.4f}")
print(f"Neg Sign Bias: t={sb.neg_sign_bias[0]:.3f}, p={sb.neg_sign_bias[1]:.4f}")
print(f"Pos Sign Bias: t={sb.pos_sign_bias[0]:.3f}, p={sb.pos_sign_bias[1]:.4f}")
print(f"Joint test: F={sb.joint[0]:.3f}, p={sb.joint[1]:.4f}")
```

---

### nyblom_test()

::: archbox.diagnostics.nyblom.nyblom_test
    options:
      show_root_heading: true
      show_source: true

Teste de estabilidade de parametros de Nyblom (1989). Verifica se os
parametros do modelo sao constantes ao longo do tempo.

$H_0$: Parametros sao estaveis (nao variam no tempo).

A estatistica conjunta testa se **todos** os parametros sao estaveis
simultaneamente, enquanto as estatisticas individuais testam cada parametro
separadamente.

```python
nyblom_test(scores) -> NyblomResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `scores` | `array-like` | -- | Matriz de scores $(T \times k)$ -- gradiente da log-verossimilhanca |

!!! note "Valores criticos"
    Os valores criticos dependem do numero de parametros $k$. O teste
    usa valores tabulados para niveis de significancia 1%, 5% e 10%.

### Exemplo

```python
from archbox.diagnostics import nyblom_test
import numpy as np

# scores: gradiente da log-verossimilhanca (T x k)
scores = np.random.randn(1000, 3)

nyb = nyblom_test(scores)
print(f"Estatistica conjunta: {nyb.joint_statistic:.4f}")
print(f"Valores criticos: {nyb.critical_values_joint}")
print(f"Estatisticas individuais: {nyb.individual_statistics}")
```

---

## Testes Multivariados

### engle_sheppard_test()

::: archbox.diagnostics.engle_sheppard.engle_sheppard_test
    options:
      show_root_heading: true
      show_source: true

Teste de Engle & Sheppard (2001) para correlacao condicional constante.

$H_0$: A correlacao condicional e constante (CCC e adequado).

$H_1$: A correlacao condicional varia no tempo (DCC e necessario).

$$
T_{\text{ES}} = T \cdot R^2 \sim \chi^2(q)
$$

onde a regressao auxiliar testa se os produtos cruzados dos residuos
padronizados possuem estrutura de autocorrelacao.

```python
engle_sheppard_test(std_resids, lags=1) -> EngleSheppardResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `std_resids` | `array-like` | -- | Residuos padronizados multivariados $(T \times k)$ |
| `lags` | `int` | `1` | Numero de lags |

### Exemplo

```python
from archbox.diagnostics import engle_sheppard_test
import numpy as np

np.random.seed(42)
# Residuos padronizados de 2 series
std_resids = np.random.randn(500, 2)

es = engle_sheppard_test(std_resids, lags=1)
print(f"Estatistica: {es.statistic:.4f}")
print(f"p-valor: {es.pvalue:.4f}")
print(f"CCC adequado: {'Sim' if es.pvalue > 0.05 else 'Nao -- use DCC'}")
```

---

### hong_spillover_test()

::: archbox.diagnostics.hong_spillover.hong_spillover_test
    options:
      show_root_heading: true
      show_source: true

Teste de spillover de volatilidade de Hong (2001). Verifica se a volatilidade
de uma serie transmite informacao para outra.

$H_0$: Nao ha spillover de volatilidade entre as series.

Utiliza kernel de Bartlett para ponderar as correlacoes cruzadas dos
residuos padronizados ao quadrado:

$$
Q = \frac{T \sum_{j=1}^{M} k^2(j/M) \hat{\rho}_{12}^2(j) - C_M}{\sqrt{2 D_M}} \xrightarrow{d} N(0,1)
$$

onde $k(\cdot)$ e o kernel de Bartlett e $M$ a largura de banda.

```python
hong_spillover_test(std_resids_1, std_resids_2, bandwidth=None) -> HongSpilloverResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `std_resids_1` | `array-like` | -- | Residuos padronizados da serie 1 |
| `std_resids_2` | `array-like` | -- | Residuos padronizados da serie 2 |
| `bandwidth` | `int \| None` | `None` | Largura de banda (auto se `None`) |

### Exemplo

```python
from archbox.diagnostics import hong_spillover_test
import numpy as np

np.random.seed(42)
resids_1 = np.random.randn(500)
resids_2 = np.random.randn(500)

hong = hong_spillover_test(resids_1, resids_2)
print(f"Estatistica: {hong.statistic:.4f}")
print(f"p-valor: {hong.pvalue:.4f}")
print(f"Bandwidth: {hong.bandwidth}")
```

---

## Suite Completa

### full_diagnostics()

::: archbox.diagnostics.diagnostics.full_diagnostics
    options:
      show_root_heading: true
      show_source: true

Executa a suite completa de testes diagnosticos em um unico comando.

```python
full_diagnostics(results, lags=10, arch_lm_lags=None, lb_lags=None) -> DiagnosticReport
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de um modelo ajustado |
| `lags` | `int` | `10` | Numero de lags padrao |
| `arch_lm_lags` | `list[int] \| None` | `None` | Lags para ARCH-LM (default: `[1, 5, 10]`) |
| `lb_lags` | `list[int] \| None` | `None` | Lags para Ljung-Box (default: `[5, 10, 20]`) |

**Testes executados:**

1. **ARCH-LM** em multiplos lags
2. **Ljung-Box** em $z_t^2$ em multiplos lags
3. **Sign Bias** (se residuos nao-padronizados disponiveis)
4. **Nyblom** (se scores disponiveis)
5. **Jarque-Bera** para normalidade dos residuos

### Exemplo Completo

```python
from archbox.models import GARCH
from archbox.diagnostics import full_diagnostics
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# Ajustar modelo
model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# Diagnosticos completos
report = full_diagnostics(result)

# Resumo formatado
print(report.summary())

# Acessar resultados individuais
for lag, test in report.arch_lm.items():
    print(f"ARCH-LM({lag}): stat={test.statistic:.4f}, p={test.pvalue:.4f}")

for lag, test in report.ljung_box_sq.items():
    print(f"Ljung-Box({lag}): Q={test.statistic:.4f}, p={test.pvalue:.4f}")

if report.sign_bias:
    sb = report.sign_bias
    print(f"Sign Bias joint: F={sb.joint[0]:.3f}, p={sb.joint[1]:.4f}")

if report.jarque_bera:
    jb_stat, jb_pval = report.jarque_bera
    print(f"Jarque-Bera: stat={jb_stat:.4f}, p={jb_pval:.4f}")
```

---

## Workflow Tipico

```python
from archbox.models import GARCH, EGARCH
from archbox.diagnostics import full_diagnostics, arch_lm_test, sign_bias_test
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# 1. Ajustar modelo inicial
garch = GARCH(returns, p=1, q=1)
result = garch.fit(disp=False)

# 2. Diagnosticos rapidos
report = full_diagnostics(result)
print(report.summary())

# 3. Se Sign Bias significativo -> tentar EGARCH
if report.sign_bias and report.sign_bias.joint[1] < 0.05:
    print("\nAssimetria detectada -- ajustando EGARCH...")
    egarch = EGARCH(returns, p=1, q=1)
    result_eg = egarch.fit(disp=False)
    report_eg = full_diagnostics(result_eg)
    print(report_eg.summary())

# 4. Verificar se ARCH-LM passou
for lag, test in report.arch_lm.items():
    status = "OK" if test.pvalue > 0.05 else "FALHOU"
    print(f"ARCH-LM({lag}): {status} (p={test.pvalue:.4f})")
```

---

## Referencias

- Engle, R.F. (1982). Autoregressive Conditional Heteroscedasticity with
  Estimates of the Variance of United Kingdom Inflation.
  *Econometrica*, 50(4), 987-1007.
- Ljung, G.M. & Box, G.E.P. (1978). On a Measure of Lack of Fit in
  Time Series Models. *Biometrika*, 65(2), 297-303.
- Engle, R.F. & Ng, V.K. (1993). Measuring and Testing the Impact of
  News on Volatility. *Journal of Finance*, 48(5), 1749-1778.
- Nyblom, J. (1989). Testing for the Constancy of Parameters Over Time.
  *Journal of the American Statistical Association*, 84(405), 223-230.
- Engle, R.F. & Sheppard, K. (2001). Theoretical and Empirical Properties
  of Dynamic Conditional Correlation Multivariate GARCH.
  *NBER Working Paper* No. 8554.
- Hong, Y. (2001). A Test for Volatility Spillover with Application to
  Exchange Rates. *Journal of Econometrics*, 103(1-2), 183-224.

---

## Ver Tambem

- [Core](core.md) -- `ArchResults` usado como input dos testes
- [GARCH](garch.md) -- Modelos univariados de volatilidade
- [Multivariado](multivariate.md) -- Modelos DCC/CCC para Engle-Sheppard
- [Visualization](visualization.md) -- `plot_diagnostics()` para visualizacao dos testes
