---
title: "Testes de Linearidade"
description: "Testes estatisticos para detectar nao-linearidade threshold e STAR — Tsay, Hansen bootstrap, LM de Luukkonen-Saikkonen-Terasvirta e selecao LSTAR vs ESTAR."
---

# Testes de Linearidade

!!! info "Quick Reference"
    **Funcoes:**
    `from archbox.threshold import linearity_test, transition_type_test, tsay_test, hansen_threshold_test`

## Overview

Antes de estimar um modelo [TAR](tar.md), [SETAR](setar.md), [LSTAR](lstar.md) ou [ESTAR](estar.md), e essencial testar se a nao-linearidade e **estatisticamente significativa**. Estimar um modelo nao-linear quando a serie e linear resulta em sobreparametrizacao e perda de eficiencia.

Os testes de linearidade respondem a tres perguntas fundamentais:

1. **A serie e nao-linear?** (H0: linear vs H1: nao-linear)
2. **A nao-linearidade e do tipo threshold?** (H0: linear vs H1: TAR)
3. **Qual tipo de transicao suave?** (LSTAR vs ESTAR)

## Testes Disponiveis

| Teste | Funcao | H0 | H1 | Uso Principal |
|-------|--------|----|----|--------------|
| LM (Luukkonen et al.) | `linearity_test()` | AR linear | STAR (LSTAR ou ESTAR) | Teste geral de nao-linearidade STAR |
| Tipo de transicao | `transition_type_test()` | -- | LSTAR ou ESTAR | Selecao do tipo de modelo STAR |
| Tsay (1989) | `tsay_test()` | AR linear | TAR | Nao-linearidade threshold abrupta |
| Hansen (1996) | `hansen_threshold_test()` | Sem threshold | Com threshold | Bootstrap sup-LM para TAR |

## Fluxo de Trabalho Recomendado

```
                    Serie y_t
                       │
          ┌────────────┴────────────┐
          │                         │
    Teste LM (STAR)          Teste Tsay (TAR)
          │                         │
     p < 0.05?                 p < 0.05?
     ┌────┴────┐               ┌────┴────┐
    Sim       Nao             Sim       Nao
     │         │               │         │
  Tipo de   AR linear        Hansen   AR linear
  transicao                  bootstrap
     │                         │
  ┌──┴──┐                  p < 0.05?
 LSTAR ESTAR              ┌────┴────┐
                         Sim       Nao
                          │         │
                       TAR/SETAR  AR linear
```

!!! tip "Ordem dos testes"
    1. Comece com o **teste LM** (mais geral, cobre STAR)
    2. Se rejeitar, use o **teste de tipo de transicao** para escolher LSTAR vs ESTAR
    3. Se nao rejeitar pelo LM, tente o **teste de Tsay** (especifico para TAR)
    4. Para confirmar threshold com inferencia robusta, use o **teste de Hansen**

## Teste LM de Luukkonen-Saikkonen-Terasvirta (1988)

### Teoria

O teste LM avalia $H_0$: modelo AR linear vs $H_1$: modelo STAR (LSTAR ou ESTAR). O problema fundamental e que sob $H_0$, os parametros de transicao $(\gamma, c)$ nao sao identificados — o que invalida testes padrao como LR e Wald.

**Solucao**: substituir a funcao de transicao $G(z_t; \gamma, c)$ por sua **expansao de Taylor** de terceira ordem em torno de $\gamma = 0$:

$$G(z_t; \gamma, c) \approx b_0 + b_1 z_t + b_2 z_t^2 + b_3 z_t^3$$

O teste entao avalia:

$$H_0: b_1 = b_2 = b_3 = 0$$

### Procedimento

1. Estimar o modelo AR linear: $y_t = \mathbf{x}_t' \boldsymbol{\phi} + e_t$
2. Regressao auxiliar: $e_t = \mathbf{x}_t' \mathbf{b}_0 + \mathbf{x}_t' z_t \mathbf{b}_1 + \mathbf{x}_t' z_t^2 \mathbf{b}_2 + \mathbf{x}_t' z_t^3 \mathbf{b}_3 + u_t$
3. F-test: $H_0: \mathbf{b}_1 = \mathbf{b}_2 = \mathbf{b}_3 = \mathbf{0}$

$$F = \frac{(RSS_0 - RSS_1) / (3k)}{RSS_1 / (T - 4k)} \sim F(3k, T - 4k)$$

onde $k = p + 1$ e o numero de regressores incluindo constante.

### Uso

```python
from archbox.threshold import linearity_test

# Teste LM: H0 = AR linear vs H1 = STAR
test = linearity_test(y, order=1, delay=1)
print(f"Teste: {test.test_name}")
print(f"Estatistica F: {test.statistic:.4f}")
print(f"p-valor: {test.pvalue:.4f}")
print(f"Detalhe: {test.detail}")

if test.pvalue < 0.05:
    print("Rejeita H0: evidencia de nao-linearidade STAR")
else:
    print("Nao rejeita H0: modelo linear pode ser suficiente")
```

### Parametros

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `y` | array-like | obrigatorio | Serie temporal |
| `order` | int | `1` | Ordem AR $p$ |
| `delay` | int | `1` | Delay $d$ para $z_t = y_{t-d}$ |

### Retorno: `TestResult`

| Atributo | Descricao |
|----------|-----------|
| `statistic` | Estatistica F |
| `pvalue` | p-valor |
| `test_name` | `"Luukkonen-Saikkonen-Terasvirta"` |
| `detail` | String com $F(df_1, df_2)$ e p-valor |

## Teste de Tipo de Transicao — Terasvirta (1994)

### Teoria

Apos rejeitar linearidade pelo teste LM, o passo seguinte e determinar se a transicao e **logistica** (LSTAR) ou **exponencial** (ESTAR). Terasvirta (1994) propos uma sequencia de testes F baseados na regressao auxiliar do teste LM.

A partir da regressao auxiliar com termos $\mathbf{b}_1 z_t$, $\mathbf{b}_2 z_t^2$, $\mathbf{b}_3 z_t^3$:

- **$H_{04}$**: $\mathbf{b}_3 = 0$ (dado $\mathbf{b}_1, \mathbf{b}_2$ livres) $\Rightarrow$ p-valor = $p_4$
- **$H_{03}$**: $\mathbf{b}_2 = 0$ (dado $\mathbf{b}_3 = 0$, $\mathbf{b}_1$ livre) $\Rightarrow$ p-valor = $p_3$
- **$H_{02}$**: $\mathbf{b}_1 = 0$ (dado $\mathbf{b}_2 = \mathbf{b}_3 = 0$) $\Rightarrow$ p-valor = $p_2$

### Regra de Decisao

$$\text{Modelo} = \begin{cases} \text{ESTAR} & \text{se } p_3 < \min(p_2, p_4) \\ \text{LSTAR} & \text{caso contrario} \end{cases}$$

**Intuicao**: o termo $z_t^2$ (testado por $H_{03}$) captura simetria — se ele domina, a transicao e simetrica (ESTAR). Se os termos impares ($z_t, z_t^3$) dominam, a transicao e assimetrica (LSTAR).

### Uso

```python
from archbox.threshold import transition_type_test

# Teste de tipo de transicao
result = transition_type_test(y, order=1, delay=1)
print(f"Modelo recomendado: {result['recommended']}")
print(f"p2 = {result['p2']:.4f} (H02: b1=0)")
print(f"p3 = {result['p3']:.4f} (H03: b2=0)")
print(f"p4 = {result['p4']:.4f} (H04: b3=0)")
print(f"F2 = {result['F2']:.4f}")
print(f"F3 = {result['F3']:.4f}")
print(f"F4 = {result['F4']:.4f}")
```

### Parametros

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `y` | array-like | obrigatorio | Serie temporal |
| `order` | int | `1` | Ordem AR $p$ |
| `delay` | int | `1` | Delay $d$ |

### Retorno: `dict`

| Chave | Descricao |
|-------|-----------|
| `recommended` | `"LSTAR"` ou `"ESTAR"` |
| `p2`, `p3`, `p4` | p-valores dos tres testes |
| `F2`, `F3`, `F4` | Estatisticas F dos tres testes |
| `detail` | String com p-valores e recomendacao |

## Teste de Tsay (1989)

### Teoria

O teste de Tsay e especifico para **nao-linearidade do tipo TAR** (transicao abrupta). Utiliza a abordagem de **autorregressao arranjada** (arranged autoregression): ordena as observacoes pela variavel threshold e testa se os termos cruzados $\mathbf{x}_t \cdot z_t$ sao significativos apos controlar pelo efeito linear.

### Procedimento

1. Estimar AR(p): $y_t = \mathbf{x}_t' \boldsymbol{\phi} + e_t$
2. Construir termos cruzados: $\mathbf{z}_{cross} = \mathbf{x}_t \cdot z_t$
3. F-test: $H_0$: os termos cruzados nao sao significativos

$$F = \frac{(RSS_0 - RSS_1) / k}{RSS_1 / (T - 2k)} \sim F(k, T - 2k)$$

### Uso

```python
from archbox.threshold import tsay_test

# Teste de Tsay: H0 = AR linear vs H1 = TAR
test = tsay_test(y, order=1, delay=1)
print(f"Teste: {test.test_name}")
print(f"Estatistica F: {test.statistic:.4f}")
print(f"p-valor: {test.pvalue:.4f}")

if test.pvalue < 0.05:
    print("Rejeita H0: evidencia de nao-linearidade TAR")
else:
    print("Nao rejeita H0: sem evidencia de threshold")
```

### Parametros

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `y` | array-like | obrigatorio | Serie temporal |
| `order` | int | `1` | Ordem AR $p$ |
| `delay` | int | `1` | Delay $d$ |

### Retorno: `TestResult`

| Atributo | Descricao |
|----------|-----------|
| `statistic` | Estatistica F |
| `pvalue` | p-valor |
| `test_name` | `"Tsay"` |
| `detail` | String com $F(df_1, df_2)$ e p-valor |

## Teste de Hansen (1996) — Bootstrap Threshold

### Teoria

O teste de Hansen aborda o problema de **parametro nuisance nao identificado**: sob $H_0$ (sem threshold), o valor de $c$ nao e identificado, o que invalida a distribuicao assintotica padrao da estatistica LR.

**Solucao**: usar a estatistica **sup-LM** (supremo sobre todos os valores candidatos de $c$) e obter a distribuicao nula por **bootstrap**.

### Procedimento

1. Para cada $c$ no grid, calcular a estatistica LM:

$$LM(c) = T \cdot \frac{RSS_0 - RSS(c)}{RSS_0}$$

2. Estatistica do teste: $\text{sup-LM} = \max_c LM(c)$

3. Bootstrap (wild bootstrap com distribuicao de Rademacher):
    - Gerar $\epsilon_b = e_t \cdot v_t$ onde $v_t \in \{-1, +1\}$ com probabilidade 1/2
    - Calcular $\text{sup-LM}^{(b)}$ para cada replicacao bootstrap
    - p-valor = proporcao de $\text{sup-LM}^{(b)} \geq \text{sup-LM}$

### Uso

```python
from archbox.threshold import hansen_threshold_test

# Teste de Hansen: H0 = sem threshold vs H1 = com threshold
test = hansen_threshold_test(y, order=1, delay=1, n_bootstrap=1000, seed=42)
print(f"Teste: {test.test_name}")
print(f"sup-LM: {test.statistic:.4f}")
print(f"Bootstrap p-valor: {test.pvalue:.4f}")

if test.pvalue < 0.05:
    print("Rejeita H0: evidencia de efeito threshold")
else:
    print("Nao rejeita H0: sem evidencia de threshold")
```

### Parametros

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `y` | array-like | obrigatorio | Serie temporal |
| `order` | int | `1` | Ordem AR $p$ |
| `delay` | int | `1` | Delay $d$ |
| `n_bootstrap` | int | `1000` | Numero de replicacoes bootstrap |
| `seed` | int \| None | `None` | Semente para reprodutibilidade |

### Retorno: `TestResult`

| Atributo | Descricao |
|----------|-----------|
| `statistic` | Estatistica sup-LM |
| `pvalue` | p-valor bootstrap |
| `test_name` | `"Hansen Bootstrap Threshold"` |
| `detail` | String com sup-LM, p-valor e numero de replicacoes |

!!! warning "Custo computacional"
    O teste de Hansen e computacionalmente intensivo: para cada replicacao bootstrap, executa um grid search completo. Com `n_bootstrap=1000` e series longas, pode levar alguns segundos. Use `seed` para reprodutibilidade.

## Exemplo Completo: Sequencia de Testes

```python
import numpy as np
from archbox.threshold import (
    linearity_test,
    transition_type_test,
    tsay_test,
    hansen_threshold_test,
    LSTAR,
    ESTAR,
    SETAR,
)

# Dados simulados
rng = np.random.default_rng(42)
n = 500
y = np.zeros(n)
gamma_true, c_true = 5.0, 0.0
for t in range(1, n):
    s = y[t-1]
    G = 1 / (1 + np.exp(-gamma_true * (s - c_true)))
    y[t] = (0.5 + 0.3 * y[t-1]) * (1 - G) + (-0.2 + 0.8 * y[t-1]) * G
    y[t] += rng.standard_normal() * 0.5

# ================================================
# Passo 1: Teste LM de linearidade (STAR)
# ================================================
test_lm = linearity_test(y, order=1, delay=1)
print("=" * 60)
print("PASSO 1: Teste LM de Linearidade")
print(f"  F = {test_lm.statistic:.4f}, p = {test_lm.pvalue:.4f}")
print(f"  {'REJEITA' if test_lm.pvalue < 0.05 else 'NAO REJEITA'} H0 (5%)")
print()

# ================================================
# Passo 2: Teste de Tsay (TAR)
# ================================================
test_tsay = tsay_test(y, order=1, delay=1)
print("PASSO 2: Teste de Tsay")
print(f"  F = {test_tsay.statistic:.4f}, p = {test_tsay.pvalue:.4f}")
print(f"  {'REJEITA' if test_tsay.pvalue < 0.05 else 'NAO REJEITA'} H0 (5%)")
print()

# ================================================
# Passo 3: Tipo de transicao (LSTAR vs ESTAR)
# ================================================
if test_lm.pvalue < 0.05:
    type_test = transition_type_test(y, order=1, delay=1)
    print("PASSO 3: Tipo de Transicao")
    print(f"  p2 = {type_test['p2']:.4f}")
    print(f"  p3 = {type_test['p3']:.4f}")
    print(f"  p4 = {type_test['p4']:.4f}")
    print(f"  Recomendacao: {type_test['recommended']}")
    print()

# ================================================
# Passo 4: Hansen bootstrap (confirmacao)
# ================================================
test_hansen = hansen_threshold_test(y, order=1, delay=1, n_bootstrap=500, seed=42)
print("PASSO 4: Teste de Hansen (Bootstrap)")
print(f"  sup-LM = {test_hansen.statistic:.4f}, p = {test_hansen.pvalue:.4f}")
print(f"  {'REJEITA' if test_hansen.pvalue < 0.05 else 'NAO REJEITA'} H0 (5%)")
print()

# ================================================
# Passo 5: Estimar modelo recomendado
# ================================================
if test_lm.pvalue < 0.05:
    recommended = type_test['recommended']
    print(f"PASSO 5: Estimando {recommended}")
    if recommended == "LSTAR":
        model = LSTAR(y, order=1, delay=1)
    else:
        model = ESTAR(y, order=1, delay=1)
    results = model.fit()
    print(results.summary())
elif test_tsay.pvalue < 0.05:
    print("PASSO 5: Estimando SETAR")
    model = SETAR(y, order=1, n_regimes=2)
    results = model.fit()
    print(results.summary())
else:
    print("PASSO 5: Modelo AR linear e suficiente")
```

## Interpretacao dos Resultados

### Tabela de Decisao

| Teste LM (p) | Teste Tsay (p) | Tipo Transicao | Modelo Recomendado |
|:---:|:---:|:---:|---|
| < 0.05 | < 0.05 | LSTAR | [LSTAR](lstar.md) |
| < 0.05 | < 0.05 | ESTAR | [ESTAR](estar.md) |
| < 0.05 | $\geq$ 0.05 | LSTAR | [LSTAR](lstar.md) |
| < 0.05 | $\geq$ 0.05 | ESTAR | [ESTAR](estar.md) |
| $\geq$ 0.05 | < 0.05 | -- | [TAR](tar.md)/[SETAR](setar.md) |
| $\geq$ 0.05 | $\geq$ 0.05 | -- | AR linear |

### Testando Multiplos Delays

```python
from archbox.threshold import linearity_test, tsay_test

# Testar para diferentes delays
print(f"{'Delay':>5} {'LM F':>10} {'LM p':>10} {'Tsay F':>10} {'Tsay p':>10}")
print("-" * 50)

for d in range(1, 7):
    lm = linearity_test(y, order=1, delay=d)
    tsay = tsay_test(y, order=1, delay=d)
    marker = " *" if lm.pvalue < 0.05 or tsay.pvalue < 0.05 else ""
    print(f"{d:>5} {lm.statistic:>10.4f} {lm.pvalue:>10.4f} "
          f"{tsay.statistic:>10.4f} {tsay.pvalue:>10.4f}{marker}")
```

!!! note "Selecao de delay"
    Se multiplos delays rejeitam linearidade, escolha o delay com menor p-valor ou use o delay que maximiza a evidencia contra $H_0$. O delay tambem pode ser selecionado automaticamente pelo [SETAR](setar.md) via AIC/BIC.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.threshold import linearity_test, tsay_test

    test_lm = linearity_test(y, order=1, delay=1)
    test_tsay = tsay_test(y, order=1, delay=1)
    ```

=== "R (tsDyn)"

    ```r
    library(tsDyn)

    # Teste de linearidade (LM)
    linearity.test <- linearityTest(y, m = 1, d = 1, type = "LM")
    print(linearity.test)

    # Teste de Tsay
    tsay.test <- linearityTest(y, m = 1, d = 1, type = "Tsay")
    print(tsay.test)
    ```

=== "R (apt)"

    ```r
    library(apt)

    # Teste de Hansen (bootstrap)
    hansen.test <- hansen.test(y, p = 1, d = 1, B = 1000)
    print(hansen.test)
    ```

| Funcionalidade | ArchBox | tsDyn (R) |
|---------------|---------|-----------|
| Teste LM | `linearity_test(y, order, delay)` | `linearityTest(y, m, d, type="LM")` |
| Teste Tsay | `tsay_test(y, order, delay)` | `linearityTest(y, m, d, type="Tsay")` |
| Tipo transicao | `transition_type_test(y, order, delay)` | Manual via p-valores |
| Hansen bootstrap | `hansen_threshold_test(y, ..., n_bootstrap)` | `apt::hansen.test(y, B)` |

## References

- Luukkonen, R., Saikkonen, P., & Terasvirta, T. (1988). Testing Linearity Against Smooth Transition Autoregressive Models. *Biometrika*, 75(3), 491--499.
- Tsay, R. S. (1989). Testing and Modeling Threshold Autoregressive Processes. *Journal of the American Statistical Association*, 84(405), 231--240.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of Smooth Transition Autoregressive Models. *Journal of the American Statistical Association*, 89(425), 208--218.
- Hansen, B. E. (1996). Inference When a Nuisance Parameter Is Not Identified Under the Null Hypothesis. *Econometrica*, 64(2), 413--430.
- Hansen, B. E. (1997). Inference in TAR Models. *Studies in Nonlinear Dynamics & Econometrics*, 2(1), 1--14.

## See Also

- [Threshold/STAR: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [TAR](tar.md) -- Modelo threshold com transicao abrupta
- [SETAR](setar.md) -- TAR self-exciting
- [LSTAR](lstar.md) -- Smooth transition logistica
- [ESTAR](estar.md) -- Smooth transition exponencial
