---
title: Regime-Switching
description: "Modelos Markov-Switching para mudancas de regime em series financeiras — MS-AR, MS-VAR e MS-GARCH."
---

# Regime-Switching

Modelos de regime-switching (Markov-Switching) permitem que os parametros de um modelo econometrico **mudem entre estados discretos** ao longo do tempo, governados por uma cadeia de Markov oculta. A ideia central e que a economia e os mercados financeiros transitam entre regimes distintos — expansao e recessao, alta e baixa volatilidade, bull e bear market — e que um modelo com parametros constantes e fundamentalmente inadequado para capturar essa dinamica.

O framework de Markov-Switching, introduzido por **Hamilton (1989)**, revolucionou a modelagem de series temporais ao permitir que a propria serie "escolha" endogenamente entre regimes, sem a necessidade de especificar *a priori* as datas de mudanca estrutural.

## Por que Parametros Constantes sao Inadequados

Em series financeiras, diversas evidencias indicam que os parametros nao sao estaveis:

- **Crises financeiras**: a volatilidade e as correlacoes mudam abruptamente durante crises (2008, 2020)
- **Ciclos economicos**: o PIB alterna entre periodos de crescimento e recessao com dinamicas distintas
- **Politica monetaria**: mudancas na conducao do banco central alteram a relacao entre variaveis macroeconomicas
- **Estrutura de mercado**: mudancas regulatorias e tecnologicas alteram a microestrutura dos mercados

!!! warning "Testes de estabilidade parametrica"
    Antes de estimar um modelo de regime-switching, verifique se ha evidencia de instabilidade parametrica. Testes como Chow, CUSUM e Bai-Perron podem indicar a presenca de quebras estruturais. Se os parametros sao estaveis, um modelo linear simples e mais parcimonioso e eficiente.

## Modelos Disponiveis

| Modelo | Classe | Caracteristica Principal | Referencia |
|--------|--------|-------------------------|------------|
| [MS-AR](ms-ar.md) | `MarkovSwitchingAR` | Media e variancia regime-dependentes, dinamica AR | Hamilton (1989) |
| [MS-VAR](ms-var.md) | `MarkovSwitchingVAR` | Extensao multivariada com transmissao entre variaveis | Krolzig (1997) |
| [MS-GARCH](ms-garch.md) | `MarkovSwitchingGARCH` | Volatilidade condicional com mudanca de regime | Gray (1996) |

## Cadeia de Markov e Matriz de Transicao

O componente central de todos os modelos de regime-switching e uma **cadeia de Markov de primeira ordem** com $K$ estados. A variavel latente $s_t \in \{0, 1, \ldots, K-1\}$ indica o regime vigente no periodo $t$, e sua dinamica e governada pela **matriz de transicao** $P$:

$$P = \begin{pmatrix} p_{00} & p_{01} & \cdots & p_{0,K-1} \\ p_{10} & p_{11} & \cdots & p_{1,K-1} \\ \vdots & \vdots & \ddots & \vdots \\ p_{K-1,0} & p_{K-1,1} & \cdots & p_{K-1,K-1} \end{pmatrix}$$

onde $p_{ij} = P(s_t = j \mid s_{t-1} = i)$ e a probabilidade de transicao do regime $i$ para o regime $j$, com:

$$\sum_{j=0}^{K-1} p_{ij} = 1 \quad \forall \, i$$

### Propriedades Importantes

**Duracao esperada** de cada regime:

$$E[D_j] = \frac{1}{1 - p_{jj}}$$

Por exemplo, se $p_{00} = 0.97$, o regime 0 dura em media $\frac{1}{1-0.97} \approx 33$ periodos.

**Probabilidades ergoticas** (distribuicao estacionaria):

$$\boldsymbol{\pi} = P' \boldsymbol{\pi}, \quad \sum_j \pi_j = 1$$

As probabilidades ergoticas representam a fracao de tempo que o sistema passa em cada regime no longo prazo.

### Probabilidades Filtradas e Suavizadas

O **Hamilton filter** calcula as probabilidades filtradas $P(s_t = j \mid \mathcal{Y}_t)$ utilizando informacao ate o periodo $t$. O **Kim smoother** refina essas estimativas utilizando toda a amostra, produzindo as probabilidades suavizadas $P(s_t = j \mid \mathcal{Y}_T)$.

```python
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

gdp = load_dataset('us_gdp_quarterly')
model = MarkovSwitchingAR(gdp['growth'], k_regimes=2, order=4)
results = model.fit()

# Probabilidades filtradas e suavizadas
print(f"Filtradas shape: {results.filtered_probs.shape}")
print(f"Suavizadas shape: {results.smoothed_probs.shape}")

# Matriz de transicao estimada
print("\nMatriz de transicao:")
print(results.transition_matrix)

# Duracao esperada de cada regime
durations = results.expected_durations()
for i, d in enumerate(durations):
    print(f"  Regime {i}: {d:.1f} trimestres")
```

## Estimacao: Algoritmo EM

Todos os modelos de regime-switching no ArchBox sao estimados via **algoritmo EM (Expectation-Maximization)**, que alterna entre:

1. **E-step**: Dado os parametros atuais, calcula as probabilidades de regime via Hamilton filter e Kim smoother
2. **M-step**: Dadas as probabilidades de regime, re-estima os parametros por maxima verossimilhanca ponderada

O algoritmo EM e particularmente adequado para modelos de regime-switching porque a funcao de verossimilhanca e multimodal e a otimizacao direta e propensa a convergir para otimos locais.

## Escolhendo um Modelo

| Caracteristica dos Dados | Modelo Recomendado | Justificativa |
|--------------------------|-------------------|---------------|
| Serie univariada com mudancas na media | [MS-AR](ms-ar.md) | Detecta mudancas na media e/ou variancia com dinamica AR |
| Multiplas series com transmissao de choques | [MS-VAR](ms-var.md) | Captura spillover e contagio entre variaveis |
| Volatilidade condicional com mudancas de regime | [MS-GARCH](ms-garch.md) | Combina clustering de volatilidade com mudancas estruturais |
| Quebras estruturais em data conhecida | Modelos lineares com dummies | Mais parcimonioso quando as datas sao conhecidas |

!!! tip "Ponto de partida"
    Comece com o [MS-AR(2)](ms-ar.md) com 2 regimes. Ele e o modelo de regime-switching mais classico e serve como benchmark natural. Avance para MS-VAR se precisar modelar multiplas series, ou MS-GARCH se o foco for a volatilidade condicional.

## Regime-Switching vs. Outras Abordagens

| Aspecto | Regime-Switching | [GARCH](../garch/index.md) | Structural Break |
|---------|-----------------|---------------------------|-----------------|
| Mudancas | Recorrentes (ida e volta) | Continuas (sem descontinuidade) | Unica (irreversivel) |
| Mecanismo | Cadeia de Markov | Autorregressivo | Deterministico |
| Estimacao | EM / MLE | MLE | MLE / OLS |
| Identificacao | Endogena | N/A | Exogena ou testes |
| Uso tipico | Ciclos, crises recorrentes | Clustering de volatilidade | Mudanca de politica |

## Quick Example

```python
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

# Carregar crescimento do PIB
gdp = load_dataset('us_gdp_quarterly')

# MS(2)-AR(4) classico de Hamilton
model = MarkovSwitchingAR(gdp['growth'], k_regimes=2, order=4)
results = model.fit()
print(results.summary())

# Classificar periodos em regimes
regimes = results.classify()
print(f"\nPeriodos em regime 0 (recessao): {(regimes == 0).sum()}")
print(f"Periodos em regime 1 (expansao): {(regimes == 1).sum()}")

# Visualizar regimes
results.plot_regimes(y=gdp['growth'].to_numpy())
```

## See Also

- [MS-AR](ms-ar.md) -- Modelo autorregressivo com mudanca de regime
- [MS-VAR](ms-var.md) -- Modelo VAR com mudanca de regime
- [MS-GARCH](ms-garch.md) -- Modelo GARCH com mudanca de regime
- [GARCH Univariado](../garch/index.md) -- Modelos de volatilidade condicional sem regime
- [Modelos Threshold](../threshold/index.md) -- Alternativa com transicao deterministica

## References

- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357--384.
- Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press. Chapter 22.
- Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching. *Journal of Econometrics*, 60(1-2), 1--22.
- Kim, C.-J., & Nelson, C. R. (1999). *State-Space Models with Regime Switching*. MIT Press.
- Krolzig, H.-M. (1997). *Markov-Switching Vector Autoregressions*. Springer.
- Gray, S. F. (1996). Modeling the Conditional Distribution of Interest Rates as a Regime-Switching Process. *Journal of Financial Economics*, 42(1), 27--62.
