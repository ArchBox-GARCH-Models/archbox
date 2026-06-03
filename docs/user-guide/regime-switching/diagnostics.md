---
title: "Diagnosticos de Regime-Switching"
description: "RCM, testes de numero de regimes, duracao esperada, residuos regime-ponderados e estabilidade parametrica."
---

# Diagnosticos de Regime-Switching

!!! info "Quick Reference"
    **Modulo:** `archbox.regime` + `archbox.diagnostics`
    **Metricas:** RCM, duracao esperada, probabilidades ergoticas
    **Testes:** Davies, estabilidade parametrica, especificacao de regime

## Overview

Apos estimar um modelo Markov-Switching, e essencial avaliar:

1. **Qualidade da classificacao**: os regimes sao bem separados?
2. **Numero de regimes**: $K$ esta correto?
3. **Adequacao do modelo**: os residuos sao bem comportados?
4. **Estabilidade**: os parametros sao estaveis dentro de cada regime?

Diferentemente dos diagnosticos de modelos lineares, os diagnosticos de regime-switching devem considerar a **natureza latente dos regimes** — nao sabemos com certeza em qual regime estamos a cada instante.

## Regime Classification Measure (RCM)

O **RCM** (Ang & Bekaert, 2002) e a metrica mais utilizada para avaliar a qualidade da classificacao de regimes. Ele mede o quao "nitidas" sao as probabilidades suavizadas.

### Formulacao

Para $K = 2$ regimes:

$$\text{RCM} = 400 \cdot \frac{1}{T} \sum_{t=1}^{T} \hat{\xi}_{t|T,1} \cdot \hat{\xi}_{t|T,2}$$

onde $\hat{\xi}_{t|T,j} = P(s_t = j \mid \mathcal{F}_T)$ sao as probabilidades suavizadas.

Para $K$ regimes gerais:

$$\text{RCM}(K) = \frac{K^2}{K-1} \cdot \frac{100}{T} \sum_{t=1}^{T} \left(1 - \sum_{j=0}^{K-1} \hat{\xi}_{t|T,j}^2 \right)$$

### Interpretacao

| RCM | Classificacao | Interpretacao |
|-----|---------------|---------------|
| 0 | Perfeita | Cada observacao pertence a exatamente um regime ($\xi = 0$ ou $1$) |
| 0--25 | Excelente | Regimes bem separados |
| 25--50 | Boa | Separacao adequada para a maioria das aplicacoes |
| 50--75 | Moderada | Regimes pouco distintos; interpretar com cautela |
| 75--100 | Fraca | Regimes quase indistinguiveis; modelo possivelmente inadequado |
| 100 | Nenhuma | Equivalente a classificacao aleatoria ($\xi = 1/K$ para todo $t$) |

### Implementacao

```python
import numpy as np
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()

model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
results = model.fit()

# Calcular RCM
smoothed = results.smoothed_probs  # shape: (T, K)
K = results.k_regimes
T = smoothed.shape[0]

if K == 2:
    rcm = 400.0 / T * np.sum(smoothed[:, 0] * smoothed[:, 1])
else:
    herfindahl = np.sum(smoothed**2, axis=1)  # sum of squared probs
    rcm = K**2 / (K - 1) * 100 / T * np.sum(1 - herfindahl)

print(f"RCM: {rcm:.2f}")
if rcm < 50:
    print("Boa separacao entre regimes")
elif rcm < 75:
    print("Separacao moderada — interpretar com cautela")
else:
    print("Separacao fraca — considerar modelo alternativo")
```

!!! tip "RCM como criterio de selecao"
    O RCM pode ser usado para comparar especificacoes: entre dois modelos com verossimilhanca similar, prefira o que tem menor RCM (regimes mais nitidos). Isso e especialmente util quando o objetivo principal e a datacao de regimes.

## Numero de Regimes

### O Davies Problem

O teste de razao de verossimilhanca (LRT) padrao **nao e valido** para testar $K$ vs. $K+1$ regimes porque:

1. Sob $H_0: K$ regimes, os parametros do regime adicional ($\mu_{K+1}, \sigma_{K+1}$) **nao sao identificados**
2. As probabilidades de transicao para o regime inexistente estao na **fronteira do espaco parametrico**
3. As condicoes de regularidade para a distribuicao $\chi^2$ assintotica **nao sao satisfeitas**

Este e o **Davies problem** (Davies, 1977, 1987).

### Abordagens Praticas

=== "Criterios de Informacao"

    A abordagem mais comum na pratica:

    ```python
    from archbox.regime import MarkovSwitchingAR
    import numpy as np

    results_by_k = {}
    for K in [2, 3, 4]:
        model = MarkovSwitchingAR(growth, k_regimes=K, order=4)
        res = model.fit(n_init=20)
        results_by_k[K] = res
        print(f"K={K}: LogL={res.loglike:.2f}, AIC={res.aic:.2f}, "
              f"BIC={res.bic:.2f}, RCM={res.rcm:.2f}")

    # BIC tende a selecionar modelos mais parcimoniosos
    best_k = min(results_by_k, key=lambda k: results_by_k[k].bic)
    print(f"\nMelhor K por BIC: {best_k}")
    ```

    !!! note "AIC vs. BIC"
        - **BIC** e mais conservador e tende a selecionar menos regimes — recomendado como criterio principal
        - **AIC** pode selecionar mais regimes que o verdadeiro, especialmente em amostras grandes
        - Na pratica, $K = 2$ e quase sempre suficiente para series financeiras e macroeconomicas

=== "Hansen Test (upper bound)"

    Hansen (1992) propoe um *upper bound* para o p-valor do LRT:

    ```python
    from scipy import stats

    # LRT entre K=2 e K=1
    # (K=1 e simplesmente um modelo linear)
    logL_1 = -250.0  # log-verossimilhanca do modelo linear
    logL_2 = results_by_k[2].loglike

    LRT = 2 * (logL_2 - logL_1)
    n_nuisance = 3  # parametros nao identificados sob H0

    # Upper bound conservador de Hansen
    # Usar distribuicao chi2 com graus de liberdade ajustados
    df_adjusted = n_nuisance + 2  # heuristica
    pvalue_upper = 1 - stats.chi2.cdf(LRT, df_adjusted)
    print(f"LRT: {LRT:.4f}")
    print(f"p-valor (upper bound): {pvalue_upper:.4f}")
    ```

=== "Analise Visual"

    Inspeção visual das probabilidades suavizadas:

    ```python
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(3, 1, figsize=(12, 9))

    for idx, K in enumerate([2, 3, 4]):
        res = results_by_k[K]
        for j in range(K):
            axes[idx].plot(
                res.smoothed_probs[:, j],
                label=f'Regime {j}', alpha=0.8,
            )
        axes[idx].set_title(f'K = {K} regimes (BIC = {res.bic:.1f})')
        axes[idx].legend(loc='upper right')
        axes[idx].set_ylim(-0.05, 1.05)

    plt.tight_layout()
    plt.savefig('regime_selection.png', dpi=150, bbox_inches='tight')
    plt.show()
    ```

## Duracao Esperada de Regime

A duracao esperada em cada regime e uma metrica fundamental para avaliar a plausibilidade economica do modelo.

### Formulacao

Para uma cadeia de Markov de primeira ordem, o tempo de permanencia no regime $j$ segue uma distribuicao **geometrica** com parametro $1 - p_{jj}$:

$$P(D_j = d) = p_{jj}^{d-1} (1 - p_{jj}), \quad d = 1, 2, 3, \ldots$$

**Duracao esperada:**

$$E[D_j] = \frac{1}{1 - p_{jj}}$$

**Variancia da duracao:**

$$\text{Var}(D_j) = \frac{p_{jj}}{(1 - p_{jj})^2}$$

### Exemplo

```python
import numpy as np

P = results.transition_matrix

print("=== Duracao Esperada de Regime ===\n")
for j in range(results.k_regimes):
    pjj = P[j, j]
    expected = 1 / (1 - pjj)
    variance = pjj / (1 - pjj)**2
    std = np.sqrt(variance)

    print(f"Regime {j}:")
    print(f"  p_{j}{j} = {pjj:.4f}")
    print(f"  Duracao esperada: {expected:.1f} periodos")
    print(f"  Desvio-padrao: {std:.1f} periodos")
    print(f"  IC 95%: [{max(1, expected - 1.96*std):.1f}, {expected + 1.96*std:.1f}]")
    print()

# Verificar plausibilidade economica
# PIB trimestral: recessao ~3-7 trimestres, expansao ~15-35 trimestres
durations = results.expected_durations()
print("Plausibilidade:")
if 2 < durations[0] < 10 and 10 < durations[1] < 40:
    print("  Duracoes consistentes com ciclos economicos tipicos")
else:
    print("  AVISO: duracoes podem ser implausveis — verificar especificacao")
```

### Duracao Empirica vs. Teorica

```python
import numpy as np

# Duracao empirica: classificar e medir runs
regimes = results.classify()
durations_empirical = {j: [] for j in range(results.k_regimes)}

current_regime = regimes[0]
current_duration = 1

for t in range(1, len(regimes)):
    if regimes[t] == current_regime:
        current_duration += 1
    else:
        durations_empirical[current_regime].append(current_duration)
        current_regime = regimes[t]
        current_duration = 1

# Ultimo run
durations_empirical[current_regime].append(current_duration)

# Comparar
print(f"{'Regime':>8} {'Teorica':>10} {'Empirica':>10} {'N runs':>8}")
print("-" * 40)
for j in range(results.k_regimes):
    d_teorica = results.expected_durations()[j]
    d_empirica = np.mean(durations_empirical[j]) if durations_empirical[j] else 0
    n_runs = len(durations_empirical[j])
    print(f"{j:>8} {d_teorica:>10.1f} {d_empirica:>10.1f} {n_runs:>8}")
```

## Residuos Regime-Ponderados

Em modelos regime-switching, os residuos devem ser calculados levando em conta a **incerteza sobre o regime**. Existem duas abordagens:

### Residuos Classificados

Usar o regime mais provavel para calcular residuos:

```python
import numpy as np

regimes = results.classify()
growth = gdp['growth'].to_numpy()

residuals = np.zeros_like(growth)
for t in range(len(growth)):
    j = regimes[t]
    mu_j = results.regime_params[j]['mu']
    sigma_j = results.regime_params[j]['sigma']
    residuals[t] = (growth[t] - mu_j) / sigma_j

print(f"Media dos residuos: {residuals.mean():.4f}")
print(f"Std dos residuos: {residuals.std():.4f}")
print(f"Assimetria: {float(np.mean(residuals**3) / np.std(residuals)**3):.4f}")
print(f"Curtose: {float(np.mean(residuals**4) / np.std(residuals)**4):.4f}")
```

### Residuos Ponderados por Probabilidade

Usar as probabilidades suavizadas como pesos:

```python
import numpy as np

smoothed = results.smoothed_probs
growth = gdp['growth'].to_numpy()

# Media e variancia condicionais ponderadas
mu_t = np.zeros(len(growth))
sigma2_t = np.zeros(len(growth))

for j in range(results.k_regimes):
    mu_j = results.regime_params[j]['mu']
    sigma_j = results.regime_params[j]['sigma']
    mu_t += smoothed[:, j] * mu_j
    sigma2_t += smoothed[:, j] * (sigma_j**2 + mu_j**2)

sigma2_t -= mu_t**2  # Var = E[X^2] - E[X]^2
sigma_t = np.sqrt(np.maximum(sigma2_t, 1e-12))

# Residuos padronizados
z_t = (growth - mu_t) / sigma_t

print(f"Media: {z_t.mean():.4f}")
print(f"Std: {z_t.std():.4f}")
```

### Testes nos Residuos

```python
from archbox.diagnostics import ljung_box_test, arch_lm_test
from scipy import stats

# Ljung-Box nos residuos
lb = ljung_box_test(z_t, lags=10)
print(f"Ljung-Box Q(10): {lb.statistic:.4f}, p={lb.pvalue:.4f}")

# Ljung-Box nos residuos ao quadrado (ARCH effects)
lb2 = ljung_box_test(z_t**2, lags=10)
print(f"Ljung-Box Q(10) em z^2: {lb2.statistic:.4f}, p={lb2.pvalue:.4f}")

# ARCH-LM
lm = arch_lm_test(z_t, lags=5)
print(f"ARCH-LM(5): {lm.statistic:.4f}, p={lm.pvalue:.4f}")

# Normalidade (Jarque-Bera)
jb_stat, jb_pval = stats.jarque_bera(z_t)
print(f"Jarque-Bera: {jb_stat:.4f}, p={jb_pval:.4f}")
```

!!! tip "Interpretacao dos residuos"
    - **Ljung-Box significativo**: resta autocorrelacao — aumentar ordem AR ou considerar MS-VAR
    - **ARCH-LM significativo**: resta heteroscedasticidade — considerar MS-GARCH
    - **Jarque-Bera significativo**: distribuicao nao-normal — considerar distribuicoes alternativas (Student-t)

## Estabilidade dos Parametros entre Regimes

### Teste de Significancia dos Regimes

Verificar se os parametros sao significativamente diferentes entre regimes:

```python
import numpy as np

# Comparar parametros entre regimes
mu = np.array([results.regime_params[j]['mu'] for j in range(results.k_regimes)])
sigma = np.array([results.regime_params[j]['sigma'] for j in range(results.k_regimes)])

print("=== Diferenca entre Regimes ===")
print(f"Media:    regime 0 = {mu[0]:.4f}, regime 1 = {mu[1]:.4f}")
print(f"  Diferenca: {abs(mu[1] - mu[0]):.4f}")
print(f"  Ratio: {mu[1] / mu[0]:.2f}x" if mu[0] != 0 else "")

print(f"\nSigma:   regime 0 = {sigma[0]:.4f}, regime 1 = {sigma[1]:.4f}")
print(f"  Diferenca: {abs(sigma[1] - sigma[0]):.4f}")
print(f"  Ratio: {sigma[0] / sigma[1]:.2f}x" if sigma[1] != 0 else "")
```

### Estabilidade Temporal

Verificar se os parametros sao estaveis ao longo do tempo estimando o modelo em sub-amostras:

```python
import numpy as np
from archbox.regime import MarkovSwitchingAR

# Dividir amostra em duas metades
T = len(growth)
mid = T // 2

results_1 = MarkovSwitchingAR(growth[:mid], k_regimes=2, order=4).fit(n_init=10)
results_2 = MarkovSwitchingAR(growth[mid:], k_regimes=2, order=4).fit(n_init=10)

print("=== Estabilidade Parametrica ===\n")
print(f"{'Parametro':<15} {'1a metade':>12} {'2a metade':>12} {'Diferenca':>12}")
print("-" * 55)

for j in range(2):
    mu1 = results_1.regime_params[j]['mu']
    mu2 = results_2.regime_params[j]['mu']
    print(f"mu_{j}            {mu1:>12.4f} {mu2:>12.4f} {abs(mu2-mu1):>12.4f}")

for j in range(2):
    s1 = results_1.regime_params[j]['sigma']
    s2 = results_2.regime_params[j]['sigma']
    print(f"sigma_{j}         {s1:>12.4f} {s2:>12.4f} {abs(s2-s1):>12.4f}")

for i in range(2):
    for j in range(2):
        p1 = results_1.transition_matrix[i, j]
        p2 = results_2.transition_matrix[i, j]
        print(f"p_{i}{j}            {p1:>12.4f} {p2:>12.4f} {abs(p2-p1):>12.4f}")
```

## Workflow Completo de Diagnostico

```python
import numpy as np
import matplotlib.pyplot as plt
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test
from scipy import stats

# 1. Carregar e estimar
gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()
dates = gdp.index

model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
results = model.fit(n_init=20)

print("=" * 60)
print("DIAGNOSTICO COMPLETO — REGIME-SWITCHING")
print("=" * 60)

# 2. Convergencia
print("\n--- 1. Convergencia ---")
print(f"  Convergiu: {results.converged}")
print(f"  Iteracoes: {results.n_iter}")
print(f"  Log-verossimilhanca: {results.loglike:.4f}")

# 3. RCM
print("\n--- 2. Regime Classification Measure ---")
smoothed = results.smoothed_probs
rcm = 400.0 / len(growth) * np.sum(smoothed[:, 0] * smoothed[:, 1])
quality = "Excelente" if rcm < 25 else "Boa" if rcm < 50 else "Moderada" if rcm < 75 else "Fraca"
print(f"  RCM: {rcm:.2f} ({quality})")

# 4. Duracao esperada
print("\n--- 3. Duracao Esperada ---")
P = results.transition_matrix
for j in range(results.k_regimes):
    d = 1 / (1 - P[j, j])
    print(f"  Regime {j}: {d:.1f} periodos (p_{j}{j} = {P[j,j]:.4f})")

# 5. Probabilidades ergoticas
print("\n--- 4. Probabilidades Ergoticas ---")
ergodic = results.ergodic_probabilities()
for j, pi in enumerate(ergodic):
    print(f"  Regime {j}: {pi:.4f} ({100*pi:.1f}% do tempo)")

# 6. Residuos
print("\n--- 5. Diagnosticos de Residuos ---")
regimes = results.classify()
residuals = np.zeros_like(growth)
for t in range(len(growth)):
    j = regimes[t]
    mu_j = results.regime_params[j]['mu']
    sigma_j = results.regime_params[j]['sigma']
    residuals[t] = (growth[t] - mu_j) / sigma_j

lb = ljung_box_test(residuals, lags=10)
lb2 = ljung_box_test(residuals**2, lags=10)
lm = arch_lm_test(residuals, lags=5)
jb_stat, jb_pval = stats.jarque_bera(residuals)

print(f"  Ljung-Box Q(10):      {lb.statistic:.4f}  p={lb.pvalue:.4f}  "
      f"{'OK' if lb.pvalue > 0.05 else 'FALHA'}")
print(f"  Ljung-Box Q(10) z^2:  {lb2.statistic:.4f}  p={lb2.pvalue:.4f}  "
      f"{'OK' if lb2.pvalue > 0.05 else 'FALHA'}")
print(f"  ARCH-LM(5):           {lm.statistic:.4f}  p={lm.pvalue:.4f}  "
      f"{'OK' if lm.pvalue > 0.05 else 'FALHA'}")
print(f"  Jarque-Bera:          {jb_stat:.4f}  p={jb_pval:.4f}  "
      f"{'OK' if jb_pval > 0.05 else 'FALHA'}")

# 7. Criterios de informacao
print("\n--- 6. Criterios de Informacao ---")
print(f"  AIC: {results.aic:.4f}")
print(f"  BIC: {results.bic:.4f}")

# 8. Visualizacao
print("\n--- 7. Visualizacao ---")
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Serie com regimes
recession = 0 if results.regime_params[0]['mu'] < results.regime_params[1]['mu'] else 1
axes[0].plot(dates, growth, 'k-', linewidth=0.8)
axes[0].fill_between(
    dates, growth.min(), growth.max(),
    where=smoothed[:, recession] > 0.5,
    color='red', alpha=0.15,
)
axes[0].set_title('Crescimento do PIB com Regimes')
axes[0].set_ylabel('Crescimento (%)')

# Probabilidades suavizadas
axes[1].plot(dates, smoothed[:, recession], 'r-', linewidth=0.8)
axes[1].axhline(0.5, color='gray', linestyle='--', alpha=0.5)
axes[1].set_title(f'P(Recessao) — RCM = {rcm:.1f}')
axes[1].set_ylabel('Probabilidade')
axes[1].set_ylim(-0.05, 1.05)

# Residuos
axes[2].plot(dates, residuals, 'b-', linewidth=0.5, alpha=0.7)
axes[2].axhline(0, color='gray', linestyle='--', alpha=0.5)
axes[2].set_title('Residuos Padronizados')
axes[2].set_ylabel('z_t')

plt.tight_layout()
plt.savefig('regime_diagnostics.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n" + "=" * 60)
```

## Resumo dos Diagnosticos

| Diagnostico | Metrica | Criterio | Acao se falhar |
|-------------|---------|----------|----------------|
| Classificacao | RCM | $< 50$ | Verificar separacao de regimes |
| Numero de regimes | BIC | Minimo entre $K$ | Ajustar $K$ |
| Autocorrelacao | Ljung-Box | $p > 0.05$ | Aumentar ordem AR |
| Efeitos ARCH | ARCH-LM | $p > 0.05$ | Usar MS-GARCH |
| Normalidade | Jarque-Bera | $p > 0.05$ | Distribuicao Student-t |
| Duracao | $E[D_j]$ | Plausivel economicamente | Rever especificacao |
| Estabilidade | Sub-amostras | Parametros similares | Considerar time-varying $P$ |

## References

- Ang, A., & Bekaert, G. (2002). Regime Switches in Interest Rates. *Journal of Business & Economic Statistics*, 20(2), 163--182.
- Davies, R. B. (1977). Hypothesis Testing When a Nuisance Parameter is Present Only Under the Alternative. *Biometrika*, 64(2), 247--254.
- Davies, R. B. (1987). Hypothesis Testing When a Nuisance Parameter is Present Only Under the Alternative. *Biometrika*, 74(1), 33--43.
- Hansen, B. E. (1992). The Likelihood Ratio Test Under Nonstandard Conditions: Testing the Markov Switching Model of GNP. *Journal of Applied Econometrics*, 7(S1), S61--S82.
- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357--384.
- Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press. Chapter 22.
- Psaradakis, Z., & Spagnolo, N. (2003). On the Determination of the Number of Regimes in Markov-Switching Autoregressive Models. *Journal of Time Series Analysis*, 24(2), 237--252.

## See Also

- [Hamilton Filter](hamilton-filter.md) -- Algoritmo de filtragem e probabilidades
- [Estimacao](estimation.md) -- MLE, EM e inicializacao
- [MS-AR](ms-ar.md) -- Modelo autorregressivo com mudanca de regime
- [MS-GARCH](ms-garch.md) -- Volatilidade condicional com mudanca de regime
- [Regime-Switching: Visao Geral](index.md) -- Introducao e comparacao de modelos
