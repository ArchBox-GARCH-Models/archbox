---
title: "Hamilton Filter e Kim Smoother"
description: "Algoritmo recursivo para inferencia de regimes — probabilidades filtradas, preditas e suavizadas em modelos Markov-Switching."
---

# Hamilton Filter e Kim Smoother

!!! info "Quick Reference"
    **Modulo:** `archbox.regime`
    **Metodos:** `results.filtered_probs`, `results.smoothed_probs`, `results.predicted_probs`
    **Referencia:** Hamilton (1989), Kim (1994)

## Overview

O **Hamilton filter** e o algoritmo central de todos os modelos Markov-Switching. Ele calcula recursivamente as **probabilidades filtradas** $P(s_t = j \mid \mathcal{F}_t)$ — a probabilidade de estar em cada regime $j$ no instante $t$, dada toda a informacao disponivel ate $t$.

O **Kim smoother** complementa o filtro utilizando a informacao de **toda a amostra** para refinar as estimativas, produzindo as **probabilidades suavizadas** $P(s_t = j \mid \mathcal{F}_T)$.

Juntos, eles fornecem tres tipos de probabilidades:

| Tipo | Notacao | Informacao Utilizada | Uso Principal |
|------|---------|---------------------|---------------|
| Predita | $P(s_t = j \mid \mathcal{F}_{t-1})$ | Ate $t-1$ | Previsao de regime |
| Filtrada | $P(s_t = j \mid \mathcal{F}_t)$ | Ate $t$ | Monitoramento em tempo real |
| Suavizada | $P(s_t = j \mid \mathcal{F}_T)$ | Toda a amostra | Analise historica |

## Hamilton Filter: Algoritmo Passo a Passo

O filtro opera recursivamente, alternando entre dois passos — **previsao** e **atualizacao** — de forma analoga ao filtro de Kalman para modelos de espaco de estado.

### Inicializacao ($t = 0$)

As probabilidades iniciais $P(s_0 = j \mid \mathcal{F}_0)$ podem ser definidas de duas formas:

- **Probabilidades ergoticas** (default): $\boldsymbol{\xi}_{0|0} = \boldsymbol{\pi}$, onde $\boldsymbol{\pi}$ e a distribuicao estacionaria da cadeia de Markov
- **Probabilidades uniformes**: $P(s_0 = j) = 1/K$ para todo $j$

### Passo 1: Previsao

Dadas as probabilidades filtradas do periodo anterior, a probabilidade predita para o periodo $t$ e obtida pela **equacao de Chapman-Kolmogorov**:

$$P(s_t = j \mid \mathcal{F}_{t-1}) = \sum_{i=0}^{K-1} p_{ij} \cdot P(s_{t-1} = i \mid \mathcal{F}_{t-1})$$

Em notacao matricial:

$$\boldsymbol{\xi}_{t|t-1} = P' \boldsymbol{\xi}_{t-1|t-1}$$

onde $P$ e a matriz de transicao com $p_{ij} = P(s_t = j \mid s_{t-1} = i)$ e $\boldsymbol{\xi}_{t|t-1}$ e o vetor de probabilidades preditas.

!!! note "Intuicao"
    O passo de previsao "propaga" as probabilidades de regime de ontem para hoje usando a matriz de transicao. Se ontem tinhamos 90% de chance de estar em expansao e a probabilidade de permanecer em expansao e 0.95, hoje a previsao sera dominada pela expansao.

### Passo 2: Atualizacao (Bayes)

Ao observar $y_t$, atualizamos as probabilidades via **regra de Bayes**:

$$P(s_t = j \mid \mathcal{F}_t) = \frac{f(y_t \mid s_t = j, \mathcal{F}_{t-1}) \cdot P(s_t = j \mid \mathcal{F}_{t-1})}{\sum_{k=0}^{K-1} f(y_t \mid s_t = k, \mathcal{F}_{t-1}) \cdot P(s_t = k \mid \mathcal{F}_{t-1})}$$

Em notacao compacta:

$$\boldsymbol{\xi}_{t|t} = \frac{\boldsymbol{\eta}_t \odot \boldsymbol{\xi}_{t|t-1}}{\mathbf{1}' (\boldsymbol{\eta}_t \odot \boldsymbol{\xi}_{t|t-1})}$$

onde:

- $\boldsymbol{\eta}_t = (f(y_t \mid s_t = 0, \mathcal{F}_{t-1}), \ldots, f(y_t \mid s_t = K-1, \mathcal{F}_{t-1}))'$ e o vetor de densidades condicionais
- $\odot$ denota o produto elemento a elemento (Hadamard)
- O denominador e a **densidade marginal** $f(y_t \mid \mathcal{F}_{t-1})$, usada para calcular a log-verossimilhanca

### Densidade Condicional

Para o caso gaussiano (MS-AR):

$$f(y_t \mid s_t = j, \mathcal{F}_{t-1}) = \frac{1}{\sqrt{2\pi \sigma_j^2}} \exp\left(-\frac{(y_t - \mu_j(t))^2}{2\sigma_j^2}\right)$$

onde $\mu_j(t)$ e a media condicional no regime $j$ (que pode incluir termos AR).

### Log-Verossimilhanca

Um subproduto do filtro e a log-verossimilhanca, calculada como soma dos logs das densidades marginais:

$$\log L(\theta) = \sum_{t=1}^{T} \log f(y_t \mid \mathcal{F}_{t-1}) = \sum_{t=1}^{T} \log \left( \sum_{j=0}^{K-1} f(y_t \mid s_t = j, \mathcal{F}_{t-1}) \cdot P(s_t = j \mid \mathcal{F}_{t-1}) \right)$$

### Resumo do Algoritmo

```
Algoritmo: Hamilton Filter
─────────────────────────────────────
Entrada: y₁, ..., yT; P; θ (parametros)
Saida:   ξ_{t|t}, ξ_{t|t-1} para t = 1,...,T; log L

1. Inicializar ξ_{0|0} = π (ergoticas)
2. log L ← 0
3. Para t = 1, ..., T:
   a. Previsao:   ξ_{t|t-1} = P' ξ_{t-1|t-1}
   b. Densidades: η_t = [f(y_t|s_t=0), ..., f(y_t|s_t=K-1)]
   c. Marginal:   f_t = 1'(η_t ⊙ ξ_{t|t-1})
   d. Atualizacao: ξ_{t|t} = (η_t ⊙ ξ_{t|t-1}) / f_t
   e. log L ← log L + log(f_t)
4. Retornar ξ_{t|t}, ξ_{t|t-1}, log L
```

## Kim Smoother

O **Kim smoother** (Kim, 1994) refina as probabilidades filtradas utilizando informacao futura. Ele opera **backward** (de $T$ para 1), tomando as probabilidades filtradas como entrada.

### Formulacao

Para $t = T-1, T-2, \ldots, 1$:

$$P(s_t = i \mid \mathcal{F}_T) = \sum_{j=0}^{K-1} \frac{p_{ij} \cdot P(s_t = i \mid \mathcal{F}_t)}{P(s_{t+1} = j \mid \mathcal{F}_t)} \cdot P(s_{t+1} = j \mid \mathcal{F}_T)$$

Em notacao matricial:

$$\boldsymbol{\xi}_{t|T} = \boldsymbol{\xi}_{t|t} \odot \left[ P \left( \frac{\boldsymbol{\xi}_{t+1|T}}{\boldsymbol{\xi}_{t+1|t}} \right) \right]$$

onde a divisao e elemento a elemento.

### Resumo do Algoritmo

```
Algoritmo: Kim Smoother
─────────────────────────────────────
Entrada: ξ_{t|t}, ξ_{t|t-1} para t = 1,...,T
Saida:   ξ_{t|T} para t = 1,...,T

1. ξ_{T|T} ← ξ_{T|T}  (inicializar com filtrada)
2. Para t = T-1, T-2, ..., 1:
   a. ξ_{t|T} = ξ_{t|t} ⊙ [P (ξ_{t+1|T} / ξ_{t+1|t})]
3. Retornar ξ_{t|T}
```

!!! tip "Estabilidade numerica"
    Quando $\xi_{t+1|t,j}$ e muito pequeno, a divisao pode causar instabilidade. Na pratica, aplica-se um *floor* (e.g., $10^{-12}$) para evitar divisao por zero.

## Filtrada vs. Suavizada: Comparacao

As probabilidades filtradas e suavizadas diferem em aspectos importantes:

| Aspecto | Filtrada $P(s_t \mid \mathcal{F}_t)$ | Suavizada $P(s_t \mid \mathcal{F}_T)$ |
|---------|--------------------------------------|---------------------------------------|
| Informacao | Ate o instante $t$ | Toda a amostra $T$ |
| Direcao | Forward only | Forward + backward |
| Uso | Tempo real, previsao | Analise historica |
| Volatilidade | Mais ruidosa | Mais suave |
| Datacao de regimes | Aproximada | Mais precisa |
| Disponibilidade | Online | Offline (pos-amostra) |

!!! warning "Qual usar?"
    - **Analise historica** (datacao de ciclos, papers): use **suavizada**
    - **Monitoramento em tempo real** (trading, nowcasting): use **filtrada**
    - **Estimacao** (EM algorithm): o E-step usa **suavizada**

## Exemplo: Probabilidades Filtradas vs. Suavizadas

```python
import numpy as np
import matplotlib.pyplot as plt
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

# 1. Carregar dados
gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()
dates = gdp.index

# 2. Estimar MS(2)-AR(4)
model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
results = model.fit()

# 3. Extrair probabilidades
filtered = results.filtered_probs    # shape: (T, K)
smoothed = results.smoothed_probs    # shape: (T, K)
predicted = results.predicted_probs  # shape: (T, K)

# Identificar regime de recessao (menor media)
mu_0 = results.regime_params[0]['mu']
mu_1 = results.regime_params[1]['mu']
recession = 0 if mu_0 < mu_1 else 1

# 4. Comparar filtrada vs suavizada
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Serie original com shading de regime suavizado
axes[0].plot(dates, growth, 'k-', linewidth=0.8, alpha=0.7)
axes[0].fill_between(
    dates, growth.min(), growth.max(),
    where=smoothed[:, recession] > 0.5,
    color='red', alpha=0.15, label='Recessao (suavizada)',
)
axes[0].set_ylabel('Crescimento (%)')
axes[0].set_title('Crescimento do PIB com Regimes Identificados')
axes[0].legend()

# Probabilidade filtrada
axes[1].plot(dates, filtered[:, recession], 'b-', linewidth=0.8)
axes[1].axhline(0.5, color='gray', linestyle='--', alpha=0.5)
axes[1].set_ylabel('P(Recessao)')
axes[1].set_title('Probabilidade Filtrada (informacao ate t)')
axes[1].set_ylim(-0.05, 1.05)

# Probabilidade suavizada
axes[2].plot(dates, smoothed[:, recession], 'r-', linewidth=0.8)
axes[2].axhline(0.5, color='gray', linestyle='--', alpha=0.5)
axes[2].set_ylabel('P(Recessao)')
axes[2].set_title('Probabilidade Suavizada (toda a amostra)')
axes[2].set_ylim(-0.05, 1.05)

plt.tight_layout()
plt.savefig('hamilton_filter_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
```

### Interpretacao do Grafico

A comparacao visual revela padroes tipicos:

- As **probabilidades suavizadas** sao mais "nitidas" — tendem a valores mais proximos de 0 ou 1
- As **probabilidades filtradas** reagem com um pequeno atraso a mudancas de regime (pois nao usam informacao futura)
- Nos **pontos de transicao**, as suavizadas identificam a mudanca de regime mais cedo que as filtradas

```python
# Quantificar a diferenca
diff = np.abs(smoothed[:, recession] - filtered[:, recession])
print(f"Diferenca media (filtrada vs suavizada): {diff.mean():.4f}")
print(f"Diferenca maxima: {diff.max():.4f}")
print(f"Correlacao: {np.corrcoef(filtered[:, recession], smoothed[:, recession])[0,1]:.4f}")

# Periodos onde as inferencias divergem
divergent = np.where(diff > 0.3)[0]
if len(divergent) > 0:
    print(f"\nPeriodos com divergencia > 0.3:")
    for idx in divergent:
        print(f"  t={idx}: filtrada={filtered[idx, recession]:.3f}, "
              f"suavizada={smoothed[idx, recession]:.3f}")
```

## Exemplo: Probabilidades Preditas e Regime em Tempo Real

```python
# Simular monitoramento em tempo real
# A probabilidade predita P(s_t | F_{t-1}) e a mais relevante para decisoes

print("=== Monitoramento em Tempo Real ===\n")
print(f"{'Periodo':>10} {'P(recessao|F_t-1)':>18} {'P(recessao|F_t)':>16} {'Sinal':>8}")
print("-" * 56)

# Ultimos 20 periodos
for t in range(-20, 0):
    p_pred = predicted[t, recession]
    p_filt = filtered[t, recession]

    if p_pred > 0.7:
        sinal = "ALERTA"
    elif p_pred > 0.5:
        sinal = "atencao"
    else:
        sinal = "normal"

    print(f"{dates[t].strftime('%Y-Q%q') if hasattr(dates[t], 'strftime') else t:>10} "
          f"{p_pred:>18.4f} {p_filt:>16.4f} {sinal:>8}")
```

## Propriedades Teoricas

### Convergencia

O Hamilton filter converge para as probabilidades verdadeiras sob condicoes de regularidade:

1. A cadeia de Markov e **ergodica** ($P$ tem todos os elementos positivos)
2. As densidades condicionais $f(y_t \mid s_t = j)$ sao **distinguiveis** entre regimes
3. A amostra e **suficientemente grande**

### Complexidade Computacional

| Operacao | Complexidade | Nota |
|----------|-------------|------|
| Hamilton filter (forward) | $O(TK^2)$ | Linear em $T$, quadratico em $K$ |
| Kim smoother (backward) | $O(TK^2)$ | Mesmo custo do filtro |
| Total (filtro + smoother) | $O(TK^2)$ | Muito eficiente para $K$ pequeno |

Para $K = 2$ (caso mais comum), cada passo envolve operacoes com vetores e matrizes $2 \times 2$ — extremamente rapido mesmo para amostras grandes.

### Relacao com Outros Filtros

| Filtro | Modelo | Variavel Latente |
|--------|--------|-----------------|
| Hamilton | Markov-Switching | Discreta ($s_t \in \{0, \ldots, K-1\}$) |
| Kalman | Espaco de estado linear | Continua ($\alpha_t \in \mathbb{R}^m$) |
| Kim (1994) | MS + espaco de estado | Discreta + continua |
| Particulas | Nao-linear geral | Continua (geral) |

## Implementacao Didatica

Para fins de compreensao, uma implementacao simplificada do Hamilton filter:

```python
import numpy as np
from scipy.stats import norm

def hamilton_filter(y, mu, sigma, P):
    """
    Hamilton filter para MS(K) com media e variancia switching.

    Parameters
    ----------
    y : ndarray, shape (T,)
        Serie temporal observada.
    mu : ndarray, shape (K,)
        Media de cada regime.
    sigma : ndarray, shape (K,)
        Desvio-padrao de cada regime.
    P : ndarray, shape (K, K)
        Matriz de transicao, P[i,j] = P(s_t=j | s_{t-1}=i).

    Returns
    -------
    filtered : ndarray, shape (T, K)
        Probabilidades filtradas.
    predicted : ndarray, shape (T, K)
        Probabilidades preditas.
    log_lik : float
        Log-verossimilhanca.
    """
    T = len(y)
    K = len(mu)

    filtered = np.zeros((T, K))
    predicted = np.zeros((T, K))
    log_lik = 0.0

    # Inicializacao: probabilidades ergoticas
    # Resolver pi = P' pi, sum(pi) = 1
    A = np.eye(K) - P.T
    A[-1, :] = 1.0
    b = np.zeros(K)
    b[-1] = 1.0
    xi = np.linalg.solve(A, b)

    for t in range(T):
        # Passo 1: Previsao
        if t == 0:
            xi_pred = xi  # ergoticas
        else:
            xi_pred = P.T @ filtered[t - 1]
        predicted[t] = xi_pred

        # Passo 2: Densidades condicionais
        eta = np.array([
            norm.pdf(y[t], loc=mu[j], scale=sigma[j])
            for j in range(K)
        ])

        # Passo 3: Densidade marginal
        f_t = np.dot(eta, xi_pred)

        # Passo 4: Atualizacao (Bayes)
        filtered[t] = (eta * xi_pred) / f_t

        # Acumular log-verossimilhanca
        log_lik += np.log(f_t)

    return filtered, predicted, log_lik


def kim_smoother(filtered, predicted, P):
    """
    Kim smoother para calcular probabilidades suavizadas.

    Parameters
    ----------
    filtered : ndarray, shape (T, K)
        Probabilidades filtradas do Hamilton filter.
    predicted : ndarray, shape (T, K)
        Probabilidades preditas do Hamilton filter.
    P : ndarray, shape (K, K)
        Matriz de transicao.

    Returns
    -------
    smoothed : ndarray, shape (T, K)
        Probabilidades suavizadas.
    """
    T, K = filtered.shape
    smoothed = np.zeros((T, K))
    smoothed[T - 1] = filtered[T - 1]

    for t in range(T - 2, -1, -1):
        # Evitar divisao por zero
        xi_pred = np.maximum(predicted[t + 1], 1e-12)
        smoothed[t] = filtered[t] * (P @ (smoothed[t + 1] / xi_pred))

    return smoothed
```

### Verificacao com ArchBox

```python
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset
import numpy as np

gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()

# Estimar modelo
model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
results = model.fit()

# Comparar com implementacao didatica (sem termos AR para simplificar)
mu = np.array([results.regime_params[j]['mu'] for j in range(2)])
sigma = np.array([results.regime_params[j]['sigma'] for j in range(2)])
P = results.transition_matrix

filt_didatica, pred_didatica, ll_didatica = hamilton_filter(growth, mu, sigma, P)
smooth_didatica = kim_smoother(filt_didatica, pred_didatica, P)

# As probabilidades nao serao identicas (modelo didatico nao tem AR),
# mas a estrutura de regimes deve ser similar
corr = np.corrcoef(results.smoothed_probs[:, 0], smooth_didatica[:, 0])[0, 1]
print(f"Correlacao entre suavizadas (archbox vs didatica): {corr:.4f}")
```

## References

- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357--384.
- Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press. Chapter 22.
- Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching. *Journal of Econometrics*, 60(1-2), 1--22.
- Kim, C.-J., & Nelson, C. R. (1999). *State-Space Models with Regime Switching*. MIT Press.

## See Also

- [Regime-Switching: Visao Geral](index.md) -- Introducao e cadeia de Markov
- [Estimacao](estimation.md) -- MLE, algoritmo EM e inicializacao
- [Diagnosticos](diagnostics.md) -- RCM, testes de regime e especificacao
- [MS-AR](ms-ar.md) -- Modelo autorregressivo com mudanca de regime
