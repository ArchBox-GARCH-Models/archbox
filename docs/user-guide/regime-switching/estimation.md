---
title: "Estimacao de Modelos Regime-Switching"
description: "MLE, algoritmo EM, inicializacao, convergencia e label switching em modelos Markov-Switching."
---

# Estimacao de Modelos Regime-Switching

!!! info "Quick Reference"
    **Metodo:** `model.fit(max_iter=500, tol=1e-8, n_init=5)`
    **Algoritmo:** EM (Expectation-Maximization)
    **Alternativa:** MLE direta via otimizacao numerica

## Overview

A estimacao de modelos Markov-Switching e desafiadora porque a **variavel de regime $s_t$ nao e observada**. A funcao de verossimilhanca envolve uma soma sobre todas as possiveis sequencias de regime, o que torna a otimizacao direta complexa e propensa a **maximos locais**.

O **algoritmo EM** (Dempster, Laird & Rubin, 1977) e a abordagem padrao, pois:

- Garante aumento monotonico da verossimilhanca a cada iteracao
- Lida naturalmente com variaveis latentes (os regimes)
- E numericamente estavel em comparacao com otimizacao direta

## Log-Verossimilhanca

### Verossimilhanca Completa

Se observassemos os regimes $\{s_t\}$, a log-verossimilhanca completa seria:

$$\log L_c(\theta) = \log P(s_0) + \sum_{t=1}^{T} \log p_{s_{t-1}, s_t} + \sum_{t=1}^{T} \log f(y_t \mid s_t, \mathcal{F}_{t-1}; \theta)$$

Os tres termos correspondem a:

1. **Probabilidade inicial** do regime em $t = 0$
2. **Probabilidades de transicao** — contribuicao da cadeia de Markov
3. **Densidades condicionais** — contribuicao das observacoes dado o regime

### Verossimilhanca Observada

Como $s_t$ nao e observado, a verossimilhanca observada marginaliza sobre todos os regimes:

$$\log L(\theta) = \sum_{t=1}^{T} \log \left( \sum_{j=0}^{K-1} f(y_t \mid s_t = j, \mathcal{F}_{t-1}; \theta) \cdot P(s_t = j \mid \mathcal{F}_{t-1}; \theta) \right)$$

Esta e a verossimilhanca calculada como subproduto do [Hamilton filter](hamilton-filter.md).

!!! warning "Multimodalidade"
    A verossimilhanca de modelos regime-switching e tipicamente **multimodal**. Diferentes configuracoes de parametros podem produzir valores de verossimilhanca semelhantes, especialmente quando os regimes nao sao bem separados. Por isso, **multiplas inicializacoes** sao essenciais.

## Algoritmo EM

O EM alterna entre dois passos ate convergencia:

### E-Step (Expectation)

Dado o vetor de parametros atual $\theta^{(m)}$, calcula as **probabilidades suavizadas** e as **probabilidades de transicao conjuntas** usando o [Hamilton filter e Kim smoother](hamilton-filter.md):

1. Executar o Hamilton filter forward para obter $\xi_{t|t}$ e $\xi_{t|t-1}$
2. Executar o Kim smoother backward para obter $\xi_{t|T}$
3. Calcular as probabilidades de transicao conjuntas:

$$P(s_t = j, s_{t-1} = i \mid \mathcal{F}_T; \theta^{(m)}) = \frac{p_{ij} \cdot \xi_{t-1|t-1,i} \cdot f(y_t \mid s_t = j) \cdot \xi_{t|T,j}}{\xi_{t|t,j} \cdot \xi_{t|t-1,j}}$$

Simplificadamente:

$$\hat{\xi}_{ij,t} = \frac{p_{ij} \cdot \xi_{t-1|t-1,i} \cdot \eta_{t,j}}{\xi_{t|t-1,j}} \cdot \frac{\xi_{t+1|T,j}}{\xi_{t|t,j}} \cdot \xi_{t|t,j}$$

### M-Step (Maximization)

Dado as probabilidades suavizadas $\xi_{t|T}$, re-estima os parametros maximizando a **verossimilhanca completa esperada**:

**Probabilidades de transicao:**

$$\hat{p}_{ij} = \frac{\sum_{t=1}^{T} P(s_t = j, s_{t-1} = i \mid \mathcal{F}_T)}{\sum_{t=1}^{T} P(s_{t-1} = i \mid \mathcal{F}_T)}$$

**Media do regime $j$** (caso sem AR):

$$\hat{\mu}_j = \frac{\sum_{t=1}^{T} P(s_t = j \mid \mathcal{F}_T) \cdot y_t}{\sum_{t=1}^{T} P(s_t = j \mid \mathcal{F}_T)}$$

**Variancia do regime $j$:**

$$\hat{\sigma}_j^2 = \frac{\sum_{t=1}^{T} P(s_t = j \mid \mathcal{F}_T) \cdot (y_t - \hat{\mu}_j)^2}{\sum_{t=1}^{T} P(s_t = j \mid \mathcal{F}_T)}$$

!!! tip "Intuicao do M-step"
    O M-step e essencialmente uma **media ponderada**: cada observacao contribui para os parametros do regime $j$ proporcionalmente a probabilidade $P(s_t = j \mid \mathcal{F}_T)$ de que aquela observacao pertenca ao regime $j$. Quando as probabilidades sao proximas de 0 ou 1, o M-step se aproxima de uma estimacao OLS separada para cada regime.

### Algoritmo Completo

```
Algoritmo: EM para Modelos Markov-Switching
──────────────────────────────────────────────────
Entrada: y₁, ..., yT; K regimes; θ⁰ (inicializacao)
Saida:   θ* (parametros estimados)

1. Inicializar θ⁽⁰⁾ (ver secao de Inicializacao)
2. m ← 0
3. Repetir:
   a. E-STEP:
      - Hamilton filter: calcular ξ_{t|t}, ξ_{t|t-1}
      - Kim smoother: calcular ξ_{t|T}
      - Log-verossimilhanca: log L⁽ᵐ⁾
   b. M-STEP:
      - Atualizar P: p̂ᵢⱼ via contagem ponderada
      - Atualizar μⱼ: media ponderada
      - Atualizar σⱼ: variancia ponderada
      - (Se AR) Atualizar φⱼ: OLS ponderado
   c. m ← m + 1
   d. Verificar convergencia:
      |log L⁽ᵐ⁾ - log L⁽ᵐ⁻¹⁾| < tol
      OU m ≥ max_iter
4. Retornar θ⁽ᵐ⁾
```

### Propriedades do EM

| Propriedade | Descricao |
|-------------|-----------|
| Monotonicidade | $\log L(\theta^{(m+1)}) \geq \log L(\theta^{(m)})$ sempre |
| Convergencia | Converge para um ponto estacionario (maximo local ou sela) |
| Velocidade | Convergencia linear (pode ser lenta perto do otimo) |
| Estabilidade | Mais estavel que otimizacao direta de Newton-Raphson |

## MLE Direta

Uma alternativa ao EM e a maximizacao direta da log-verossimilhanca via otimizacao numerica:

$$\hat{\theta} = \arg\max_\theta \log L(\theta)$$

### Comparacao EM vs. MLE Direta

| Aspecto | EM | MLE Direta |
|---------|-----|------------|
| Implementacao | Mais simples | Requer gradientes (analiticos ou numericos) |
| Convergencia | Sempre aumenta $L$ | Pode divergir |
| Velocidade | Linear (lenta perto do otimo) | Quadratica (Newton) se bem condicionado |
| Restricoes | Naturalmente satisfeitas | Requerem reparametrizacao |
| Maximos locais | Sensivel (como MLE) | Sensivel |

No ArchBox, o EM e o metodo padrao. Para problemas onde a convergencia do EM e muito lenta, pode-se usar o EM para obter bons valores iniciais e depois refinar com MLE direta.

## Inicializacao

A escolha de valores iniciais e **critica** para a qualidade da estimacao. Uma inicializacao ruim pode levar a:

- Convergencia para um maximo local inferior
- Convergencia extremamente lenta
- Regimes degenerados (um regime "absorve" todas as observacoes)

### Estrategias de Inicializacao

=== "K-Means (default)"

    Classificar as observacoes em $K$ grupos via K-means e usar as estatisticas de cada grupo como valores iniciais:

    ```python
    from archbox.regime import MarkovSwitchingAR

    model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
    # K-means e a estrategia padrao
    results = model.fit()
    ```

=== "Multiplas Inicializacoes"

    Rodar o EM com varias inicializacoes aleatorias e selecionar a que produz a maior verossimilhanca:

    ```python
    # 20 inicializacoes aleatorias
    results = model.fit(n_init=20)
    print(f"Melhor log-verossimilhanca: {results.loglike:.4f}")
    print(f"Inicializacao vencedora: {results.best_init}")
    ```

=== "Manual"

    Especificar valores iniciais baseados em conhecimento do dominio:

    ```python
    import numpy as np

    # Valores iniciais baseados em conhecimento economico
    init_params = {
        'mu': np.array([-1.0, 1.5]),        # recessao vs expansao
        'sigma': np.array([2.0, 0.8]),       # alta vs baixa vol
        'P': np.array([[0.90, 0.10],         # regime persistente
                       [0.05, 0.95]]),
    }

    results = model.fit(init_params=init_params)
    ```

=== "Quantis"

    Dividir os dados em quantis para definir regimes:

    ```python
    import numpy as np

    # Dividir por quantis
    q = np.percentile(growth, [33, 67])

    init_params = {
        'mu': np.array([growth[growth < q[0]].mean(),
                        growth[growth > q[1]].mean()]),
        'sigma': np.array([growth[growth < q[0]].std(),
                           growth[growth > q[1]].std()]),
    }

    results = model.fit(init_params=init_params)
    ```

### Exemplo: Impacto da Inicializacao

```python
import numpy as np
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()

model = MarkovSwitchingAR(growth, k_regimes=2, order=4)

# Comparar diferentes numeros de inicializacoes
for n in [1, 5, 10, 20, 50]:
    results = model.fit(n_init=n)
    print(f"n_init={n:>2d}: logL={results.loglike:.4f}, "
          f"iter={results.n_iter:>3d}, "
          f"converged={results.converged}")
```

!!! tip "Regra pratica"
    Use `n_init=10` para analises exploratoriass e `n_init=50` para resultados finais de publicacao. O custo computacional adicional e pequeno comparado ao risco de ficar preso em um maximo local.

## Convergencia

### Criterios de Convergencia

O EM para quando um dos criterios e atingido:

1. **Mudanca na verossimilhanca**: $|\log L^{(m)} - \log L^{(m-1)}| < \texttt{tol}$
2. **Mudanca nos parametros**: $\|\theta^{(m)} - \theta^{(m-1)}\| < \texttt{tol}$
3. **Numero maximo de iteracoes**: $m \geq \texttt{max\_iter}$

```python
# Configurar criterios de convergencia
results = model.fit(
    max_iter=1000,  # maximo de iteracoes
    tol=1e-10,      # tolerancia rigorosa
    disp=True,      # exibir progresso
)

if not results.converged:
    print("AVISO: EM nao convergiu!")
    print(f"  Iteracoes: {results.n_iter}")
    print(f"  Ultima mudanca em logL: {results.last_delta_loglike:.2e}")
```

### Problemas Comuns de Convergencia

!!! danger "Regime degenerado"
    Se um regime tem probabilidade ergotica muito baixa ($\pi_j < 0.01$), ele pode "colapsar" — pouquissimas observacoes sao atribuidas a ele, e os parametros ficam mal estimados. Solucoes:

    - Reduzir o numero de regimes
    - Usar inicializacao mais informativa
    - Impor restricoes nos parametros

!!! danger "Variancia tendendo a zero"
    Se $\sigma_j \to 0$ para algum regime, a verossimilhanca diverge para $+\infty$. Isso acontece quando um regime se "ajusta" perfeitamente a poucas observacoes. Solucoes:

    - Impor um *floor* na variancia: $\sigma_j \geq \sigma_{\min}$
    - Usar prior bayesiano (penalizar variancias pequenas)
    - Verificar se os dados tem outliers

!!! warning "Convergencia lenta"
    O EM pode convergir muito lentamente quando:

    - Os regimes sao pouco distinguiveis (medias e variancias semelhantes)
    - A amostra e pequena
    - A matriz de transicao tem elementos proximos de 0.5 (regimes nao persistentes)

    Nesses casos, considere:

    - Aumentar `max_iter`
    - Usar EM acelerado (Aitken acceleration)
    - Iniciar com EM e refinar com MLE direta

## Restricoes na Estimacao

### Probabilidades de Transicao

As restricoes naturais da matriz de transicao sao:

$$p_{ij} \geq 0 \quad \text{e} \quad \sum_{j=0}^{K-1} p_{ij} = 1 \quad \forall \, i$$

No M-step do EM, essas restricoes sao automaticamente satisfeitas pela formula de atualizacao. Para MLE direta, usa-se a **reparametrizacao logistica**:

$$p_{ij} = \frac{\exp(\gamma_{ij})}{\sum_k \exp(\gamma_{ik})}$$

### Identificacao

Para que os parametros sejam identificaveis, e necessario impor restricoes que quebrem a simetria entre os regimes. Abordagens comuns:

- **Ordenar as medias**: $\mu_0 < \mu_1 < \cdots < \mu_{K-1}$
- **Ordenar as variancias**: $\sigma_0 > \sigma_1 > \cdots > \sigma_{K-1}$
- **Pos-estimacao**: reordenar os regimes apos a convergencia

```python
# ArchBox reordena automaticamente por media
results = model.fit()

# Verificar ordenacao
for j in range(results.k_regimes):
    print(f"Regime {j}: mu={results.regime_params[j]['mu']:.4f}, "
          f"sigma={results.regime_params[j]['sigma']:.4f}")
# Regime 0 tera a menor media (recessao)
```

## Label Switching Problem

O **label switching** e o problema fundamental de identificacao em modelos de mistura e regime-switching: se trocarmos os rotulos dos regimes (regime 0 vira regime 1 e vice-versa), a verossimilhanca permanece inalterada.

### O Problema

Para $K = 2$ regimes com parametros $(\mu_0, \sigma_0, \mu_1, \sigma_1, p_{00}, p_{11})$, a permutacao:

$$(\mu_0, \sigma_0, \mu_1, \sigma_1, p_{00}, p_{11}) \leftrightarrow (\mu_1, \sigma_1, \mu_0, \sigma_0, p_{11}, p_{00})$$

produz **exatamente a mesma verossimilhanca**. Isso significa que:

- A funcao de verossimilhanca tem pelo menos $K!$ maximos equivalentes
- O EM pode convergir para qualquer um deles
- Rodadas diferentes podem produzir "regimes" com rotulos trocados

### Consequencias Praticas

| Situacao | Impacto | Risco |
|----------|---------|-------|
| Estimacao unica | Nenhum (parametros sao os mesmos) | Baixo |
| Comparacao entre modelos | Regimes podem ter rotulos diferentes | Medio |
| Bootstrap / simulacao | Mistura de rotulacoes invalida IC | Alto |
| Estimacao bayesiana (MCMC) | Cadeia pode saltar entre modos | Alto |

### Solucoes

=== "Restricao de ordenacao"

    A abordagem mais simples e robusta: impor $\mu_0 < \mu_1$:

    ```python
    # ArchBox aplica reordenacao automatica
    results = model.fit()

    # Regime 0 sempre tera a menor media
    assert results.regime_params[0]['mu'] < results.regime_params[1]['mu']
    ```

=== "Pos-processamento"

    Reordenar os regimes apos a estimacao:

    ```python
    import numpy as np

    # Extrair medias
    mus = np.array([results.regime_params[j]['mu'] for j in range(2)])

    # Reordenar se necessario
    if mus[0] > mus[1]:
        # Trocar rotulos
        print("Label switching detectado — reordenando regimes")
        # ArchBox faz isso automaticamente
    ```

=== "Pivoting (MCMC)"

    Para estimacao bayesiana, usar pivoting constraints ou post-processing:

    ```python
    # Nao aplicavel ao EM do ArchBox,
    # mas relevante para extensoes bayesianas
    # Ver Fruhwirth-Schnatter (2006) para detalhes
    ```

!!! warning "Cuidado com bootstrap"
    Ao fazer bootstrap para intervalos de confianca, cada replicacao pode convergir com rotulos diferentes. Sempre aplique a mesma restricao de ordenacao em todas as replicacoes antes de agregar os resultados.

## Exemplo Completo: Estimacao com Diagnostico

```python
import numpy as np
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

# 1. Carregar dados
gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()

# 2. Estimar com multiplas inicializacoes
model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
results = model.fit(n_init=20, tol=1e-10, max_iter=1000, disp=True)

# 3. Verificar convergencia
print("=== Convergencia ===")
print(f"Convergiu: {results.converged}")
print(f"Iteracoes: {results.n_iter}")
print(f"Log-verossimilhanca: {results.loglike:.4f}")

# 4. Parametros estimados
print("\n=== Parametros por Regime ===")
for j in range(results.k_regimes):
    p = results.regime_params[j]
    print(f"Regime {j}: mu={p['mu']:.4f}, sigma={p['sigma']:.4f}")

# 5. Matriz de transicao
print("\n=== Matriz de Transicao ===")
P = results.transition_matrix
print(P)

# 6. Duracao esperada
durations = results.expected_durations()
print("\n=== Duracao Esperada ===")
for j, d in enumerate(durations):
    print(f"Regime {j}: {d:.1f} periodos")

# 7. Probabilidades ergoticas
ergodic = results.ergodic_probabilities()
print("\n=== Probabilidades Ergoticas ===")
for j, pi in enumerate(ergodic):
    print(f"Regime {j}: {pi:.4f} ({100*pi:.1f}% do tempo)")

# 8. Criterios de informacao
print(f"\nAIC: {results.aic:.4f}")
print(f"BIC: {results.bic:.4f}")
```

## Comparacao de Especificacoes

```python
import numpy as np
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()

# Comparar diferentes especificacoes
specs = {
    'MS(2)-AR(1) mean-sw': dict(k_regimes=2, order=1, switching_mean=True, switching_variance=False),
    'MS(2)-AR(1) full-sw': dict(k_regimes=2, order=1, switching_mean=True, switching_variance=True),
    'MS(2)-AR(4) mean-sw': dict(k_regimes=2, order=4, switching_mean=True, switching_variance=False),
    'MS(2)-AR(4) full-sw': dict(k_regimes=2, order=4, switching_mean=True, switching_variance=True),
    'MS(3)-AR(4) full-sw': dict(k_regimes=3, order=4, switching_mean=True, switching_variance=True),
}

print(f"{'Modelo':<25} {'LogL':>10} {'AIC':>10} {'BIC':>10} {'Conv':>6} {'Iter':>5}")
print("-" * 70)

for name, spec in specs.items():
    model = MarkovSwitchingAR(growth, **spec)
    res = model.fit(n_init=10)
    print(f"{name:<25} {res.loglike:>10.2f} {res.aic:>10.2f} "
          f"{res.bic:>10.2f} {str(res.converged):>6} {res.n_iter:>5d}")
```

## References

- Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977). Maximum Likelihood from Incomplete Data via the EM Algorithm. *Journal of the Royal Statistical Society: Series B*, 39(1), 1--38.
- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357--384.
- Hamilton, J. D. (1990). Analysis of Time Series Subject to Changes in Regime. *Journal of Econometrics*, 45(1-2), 39--70.
- Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press. Chapter 22.
- Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching. *Journal of Econometrics*, 60(1-2), 1--22.
- Fruhwirth-Schnatter, S. (2006). *Finite Mixture and Markov Switching Models*. Springer.

## See Also

- [Hamilton Filter](hamilton-filter.md) -- Algoritmo de filtragem e suavizacao
- [Diagnosticos](diagnostics.md) -- Avaliacao da qualidade do modelo estimado
- [MS-AR](ms-ar.md) -- Modelo autorregressivo com mudanca de regime
- [Regime-Switching: Visao Geral](index.md) -- Introducao e comparacao de modelos
