---
title: "Diagnosticos Multivariados"
description: "Testes de especificacao e avaliacao de modelos GARCH multivariados — Hosking, Li-McLeod, positiva-definitividade e residuos padronizados."
---

# Diagnosticos Multivariados

!!! info "Quick Reference"
    **Modulo:** `archbox.diagnostics` + `archbox.multivariate.utils`
    **Import:** `from archbox.diagnostics import ljung_box_test, engle_sheppard_test`
    **Complemento:** `from archbox.multivariate.utils import is_positive_definite`

## Overview

Apos estimar um modelo GARCH multivariado, e essencial verificar se ele captura adequadamente a dinamica conjunta das volatilidades e correlacoes. Os diagnosticos multivariados avaliam:

1. **Autocorrelacao residual multivariada**: os residuos padronizados sao i.i.d.?
2. **Correlacao constante**: a estrutura de correlacao e estavel?
3. **Positiva-definitividade**: todas as matrizes $H_t$ sao validas?
4. **Adequacao da distribuicao**: os residuos seguem a distribuicao assumida?

Diferentemente dos diagnosticos univariados (que testam cada serie isoladamente), os testes multivariados avaliam a **estrutura conjunta** dos residuos.

## Residuos Padronizados Multivariados

O ponto de partida de qualquer diagnostico e o vetor de residuos padronizados:

$$z_t = D_t^{-1} \epsilon_t = (\sigma_{1,t}^{-1} \epsilon_{1,t}, \ldots, \sigma_{k,t}^{-1} \epsilon_{k,t})'$$

Se o modelo esta bem especificado, $z_t$ deve ser:

- Serialmente nao correlacionado (individualmente e cruzadamente)
- Com variancia unitaria
- Independente (sob a distribuicao assumida)

```python
from archbox.multivariate import DCC

model = DCC(endog)
results = model.fit()

# Residuos padronizados
z = results.std_resids  # shape: (T, k)
print(f"Shape: {z.shape}")
print(f"Media por serie: {z.mean(axis=0)}")
print(f"Std por serie: {z.std(axis=0)}")  # Deve ser ~1
```

## Teste de Hosking (Autocorrelacao Multivariada)

O teste de **Hosking (1980)** e a generalizacao multivariada do Ljung-Box. Ele testa se as **matrizes de autocorrelacao cruzada** dos residuos sao conjuntamente zero.

### Hipoteses

$$H_0: C_1 = C_2 = \cdots = C_m = 0$$
$$H_1: \text{pelo menos uma } C_h \neq 0$$

onde $C_h = \text{Cov}(z_t, z_{t-h})$ e a matriz de autocovariancia cruzada no lag $h$.

### Estatistica

$$Q_H(m) = T^2 \sum_{h=1}^{m} \frac{1}{T-h} \text{tr}(\hat{C}_h' \hat{C}_0^{-1} \hat{C}_h \hat{C}_0^{-1})$$

Sob $H_0$: $Q_H(m) \sim \chi^2(k^2 m)$

### Implementacao

```python
import numpy as np

def hosking_test(residuals, lags=10):
    """Teste de Hosking para autocorrelacao multivariada."""
    T, k = residuals.shape
    C0 = residuals.T @ residuals / T
    C0_inv = np.linalg.inv(C0)

    Q = 0.0
    for h in range(1, lags + 1):
        Ch = residuals[h:].T @ residuals[:-h] / T
        Q += np.trace(Ch.T @ C0_inv @ Ch @ C0_inv) / (T - h)

    Q *= T * T
    df = k * k * lags

    from scipy import stats
    pvalue = 1 - stats.chi2.cdf(Q, df)
    return Q, pvalue, df

# Aplicar
z = results.std_resids
Q, pvalue, df = hosking_test(z, lags=10)
print(f"Hosking Q({10}): {Q:.4f}")
print(f"p-valor: {pvalue:.4f}")
print(f"Graus de liberdade: {df}")
```

!!! tip "Interpretacao"
    - **p > 0.05**: Nao rejeita $H_0$ — sem autocorrelacao multivariada residual. Modelo adequado.
    - **p < 0.05**: Rejeita $H_0$ — resta dependencia serial nos residuos. Considere aumentar a ordem do modelo ou usar um modelo diferente.

## Teste de Li-McLeod

O teste de **Li & McLeod (1981)** e uma variante do Hosking com uma correcao que melhora o desempenho em amostras finitas.

### Estatistica

$$Q_{LM}(m) = T \sum_{h=1}^{m} \text{tr}(\hat{C}_h' \hat{C}_0^{-1} \hat{C}_h \hat{C}_0^{-1}) + \frac{k^2 m(m+1)}{2T}$$

Sob $H_0$: $Q_{LM}(m) \sim \chi^2(k^2 m)$

### Implementacao

```python
import numpy as np

def li_mcleod_test(residuals, lags=10):
    """Teste de Li-McLeod para autocorrelacao multivariada."""
    T, k = residuals.shape
    C0 = residuals.T @ residuals / T
    C0_inv = np.linalg.inv(C0)

    Q = 0.0
    for h in range(1, lags + 1):
        Ch = residuals[h:].T @ residuals[:-h] / T
        Q += np.trace(Ch.T @ C0_inv @ Ch @ C0_inv)

    Q = T * Q + k * k * lags * (lags + 1) / (2 * T)
    df = k * k * lags

    from scipy import stats
    pvalue = 1 - stats.chi2.cdf(Q, df)
    return Q, pvalue, df

# Aplicar
Q_lm, pvalue_lm, df = li_mcleod_test(z, lags=10)
print(f"Li-McLeod Q({10}): {Q_lm:.4f}")
print(f"p-valor: {pvalue_lm:.4f}")
```

## Teste de Correlacao Constante (Engle & Sheppard)

O teste de **Engle & Sheppard (2001)** avalia se a correlacao condicional e de fato constante (CCC) ou dinamica (DCC). E o teste fundamental para decidir entre CCC e DCC.

### Hipoteses

$$H_0: R_t = R \quad \forall t \quad \text{(correlacao constante)}$$
$$H_1: R_t \text{ e dinamica}$$

### Estatistica

Sob $H_0$, a regressao auxiliar:

$$\text{vech}(z_t z_t' - \bar{R}) = \gamma_0 + \sum_{h=1}^{m} \gamma_h \text{vech}(z_{t-h} z_{t-h}') + u_t$$

deve ter $\gamma_1 = \cdots = \gamma_m = 0$. A estatistica LM e:

$$LM = T \cdot R^2_{aux} \sim \chi^2\left(\frac{mk(k-1)}{2}\right)$$

### Implementacao

```python
from archbox.diagnostics import engle_sheppard_test

# Testar correlacao constante
z = results.std_resids
es_result = engle_sheppard_test(z, lags=5)
print(f"Engle-Sheppard LM({5}): {es_result.statistic:.4f}")
print(f"p-valor: {es_result.pvalue:.4f}")
```

!!! warning "Decisao CCC vs. DCC"
    - **p > 0.05**: Nao rejeita $H_0$ — correlacao constante adequada → use [CCC](ccc.md)
    - **p < 0.05**: Rejeita $H_0$ — correlacao dinamica → use [DCC](dcc.md) ou [DECO](deco.md)

## Avaliacao de Positiva-Definitividade

Toda matriz de covariancia $H_t$ deve ser **positiva-definida** para ser valida. Isso garante que:

- Todas as variancias sao positivas
- Nenhuma combinacao linear dos retornos tem variancia negativa
- A inversa de $H_t$ existe (necessaria para a verossimilhanca)

### Verificacao

```python
from archbox.multivariate.utils import is_positive_definite

H_t = results.dynamic_covariance  # shape: (T, k, k)

# Verificar cada H_t
n_total = H_t.shape[0]
n_pd = sum(is_positive_definite(H_t[t]) for t in range(n_total))
n_non_pd = n_total - n_pd

print(f"Total de matrizes H_t: {n_total}")
print(f"Positiva-definidas: {n_pd} ({100*n_pd/n_total:.1f}%)")
print(f"Nao positiva-definidas: {n_non_pd}")
```

### Diagnostico de Autovalores

```python
import numpy as np

# Menor autovalor de cada H_t
min_eigenvalues = np.array([
    np.linalg.eigvalsh(H_t[t]).min()
    for t in range(H_t.shape[0])
])

print(f"Menor autovalor (minimo): {min_eigenvalues.min():.2e}")
print(f"Menor autovalor (media):  {min_eigenvalues.mean():.2e}")

# Se algum autovalor e muito proximo de zero, pode causar instabilidade
if min_eigenvalues.min() < 1e-10:
    print("AVISO: Autovalores muito pequenos detectados!")
    print("Considere: regularizacao ou modelo com PD por construcao (BEKK)")
```

!!! note "PD por Modelo"
    | Modelo | Positiva-definitividade |
    |--------|------------------------|
    | BEKK | Garantida por construcao |
    | CCC | Garantida se $R$ e PD |
    | DCC | Garantida pela normalizacao de $Q_t$ |
    | GO-GARCH | Garantida se $Z$ e invertivel |
    | DECO | Garantida se $\rho_t > -1/(k-1)$ |

## Diagnosticos Univariados por Serie

Alem dos testes multivariados, e importante verificar cada serie individualmente:

```python
from archbox.diagnostics import ljung_box_test, arch_lm_test

z = results.std_resids
k = z.shape[1]

print("=== Diagnosticos por Serie ===\n")
for i in range(k):
    zi = z[:, i]

    # Ljung-Box nos residuos ao quadrado
    lb = ljung_box_test(zi**2, lags=10)

    # ARCH-LM
    lm = arch_lm_test(zi, lags=5)

    status = "OK" if lb.pvalue > 0.05 and lm.pvalue > 0.05 else "FALHA"

    print(f"Serie {i}: LB(10) p={lb.pvalue:.4f}, "
          f"ARCH-LM(5) p={lm.pvalue:.4f} [{status}]")
```

## Teste de Normalidade Multivariada

Se o modelo assume normalidade multivariada, teste a hipotese:

```python
import numpy as np
from scipy import stats

z = results.std_resids
T, k = z.shape

# Mardia's test para assimetria e curtose multivariada
# Assimetria multivariada
S_inv = np.linalg.inv(np.cov(z.T))
skew_vals = []
for i in range(T):
    for j in range(T):
        d = z[i] - z.mean(axis=0)
        e = z[j] - z.mean(axis=0)
        skew_vals.append((d @ S_inv @ e) ** 3)
b1 = np.mean(skew_vals)
stat_skew = T * b1 / 6
pval_skew = 1 - stats.chi2.cdf(stat_skew, k*(k+1)*(k+2)/6)

# Curtose multivariada
kurt_vals = []
for i in range(T):
    d = z[i] - z.mean(axis=0)
    kurt_vals.append((d @ S_inv @ d) ** 2)
b2 = np.mean(kurt_vals)
stat_kurt = (b2 - k*(k+2)) / np.sqrt(8*k*(k+2)/T)
pval_kurt = 2 * (1 - stats.norm.cdf(abs(stat_kurt)))

print(f"Assimetria multivariada: stat={stat_skew:.4f}, p={pval_skew:.4f}")
print(f"Curtose multivariada: stat={stat_kurt:.4f}, p={pval_kurt:.4f}")
```

## Workflow Completo de Diagnostico

```python
import numpy as np
from archbox.multivariate import DCC, CCC
from archbox.diagnostics import ljung_box_test, arch_lm_test, engle_sheppard_test
from archbox.multivariate.utils import is_positive_definite

# 1. Estimar modelo
model = DCC(endog)
results = model.fit()
z = results.std_resids
H_t = results.dynamic_covariance
T, k = z.shape

print("=" * 60)
print("DIAGNOSTICOS MULTIVARIADOS")
print("=" * 60)

# 2. Autocorrelacao univariada (por serie)
print("\n--- Ljung-Box por Serie (z^2, lags=10) ---")
all_ok = True
for i in range(k):
    lb = ljung_box_test(z[:, i]**2, lags=10)
    status = "OK" if lb.pvalue > 0.05 else "FALHA"
    if lb.pvalue <= 0.05:
        all_ok = False
    print(f"  Serie {i}: Q={lb.statistic:.4f}, p={lb.pvalue:.4f} [{status}]")
print(f"  Resultado: {'PASS' if all_ok else 'FAIL'}")

# 3. ARCH-LM por serie
print("\n--- ARCH-LM por Serie (lags=5) ---")
all_ok = True
for i in range(k):
    lm = arch_lm_test(z[:, i], lags=5)
    status = "OK" if lm.pvalue > 0.05 else "FALHA"
    if lm.pvalue <= 0.05:
        all_ok = False
    print(f"  Serie {i}: LM={lm.statistic:.4f}, p={lm.pvalue:.4f} [{status}]")
print(f"  Resultado: {'PASS' if all_ok else 'FAIL'}")

# 4. Teste de correlacao constante
print("\n--- Teste de Correlacao Constante (Engle-Sheppard) ---")
es = engle_sheppard_test(z, lags=5)
print(f"  LM({5}) = {es.statistic:.4f}, p = {es.pvalue:.4f}")
print(f"  Resultado: {'CCC adequado' if es.pvalue > 0.05 else 'DCC necessario'}")

# 5. Positiva-definitividade
print("\n--- Positiva-Definitividade ---")
n_pd = sum(is_positive_definite(H_t[t]) for t in range(T))
print(f"  PD: {n_pd}/{T} ({100*n_pd/T:.1f}%)")
print(f"  Resultado: {'PASS' if n_pd == T else 'FAIL'}")

# 6. Criterios de informacao
print("\n--- Criterios de Informacao ---")
ccc_results = CCC(endog).fit()
print(f"  DCC: AIC={results.aic:.4f}, BIC={results.bic:.4f}")
print(f"  CCC: AIC={ccc_results.aic:.4f}, BIC={ccc_results.bic:.4f}")
preferred = "DCC" if results.bic < ccc_results.bic else "CCC"
print(f"  Preferido (BIC): {preferred}")

print("\n" + "=" * 60)
```

## Resumo dos Testes

| Teste | $H_0$ | Rejeicao indica | Acao |
|-------|--------|-----------------|------|
| Hosking | Sem autocorrelacao multivariada | Modelo incompleto | Aumentar ordem ou trocar modelo |
| Li-McLeod | Sem autocorrelacao multivariada | Modelo incompleto | Aumentar ordem ou trocar modelo |
| Engle-Sheppard | Correlacao constante | Correlacao dinamica | Trocar CCC por DCC |
| Ljung-Box (por serie) | Sem autocorrelacao em $z_i^2$ | GARCH univariado inadequado | Trocar modelo univariado |
| ARCH-LM (por serie) | Sem efeitos ARCH residuais | GARCH univariado inadequado | Aumentar ordem |
| PD check | $H_t$ PD | Problemas numericos | Regularizar ou usar BEKK |

## References

- Hosking, J. R. M. (1980). The Multivariate Portmanteau Statistic. *Journal of the American Statistical Association*, 75(371), 602--608.
- Li, W. K., & McLeod, A. I. (1981). Distribution of the Residual Autocorrelations in Multivariate ARMA Time Series Models. *Journal of the Royal Statistical Society: Series B*, 43(2), 231--239.
- Engle, R. F., & Sheppard, K. (2001). Theoretical and Empirical Properties of Dynamic Conditional Correlation Multivariate GARCH. *NBER Working Paper* No. 8554.
- Tse, Y. K. (2000). A Test for Constant Correlations in a Multivariate GARCH Model. *Journal of Econometrics*, 98(1), 107--127.
- Lütkepohl, H. (2005). *New Introduction to Multiple Time Series Analysis*. Springer. Chapter 4.

## See Also

- [DCC](dcc.md) — Modelo com correlacao dinamica
- [CCC](ccc.md) — Modelo com correlacao constante
- [BEKK](bekk.md) — Modelo com PD garantida
- [Guia de Selecao](choosing-model.md) — Usar diagnosticos para escolher modelo
- [Diagnosticos Univariados](../../diagnostics/index.md) — Testes para modelos de uma serie
