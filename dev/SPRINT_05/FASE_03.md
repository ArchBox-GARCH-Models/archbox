# Fase 03 — Cap 11: Notebooks Restantes Regime-Switching

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 5 notebooks restantes do capitulo 11 cobrindo MS-VAR, Hamilton filter, EM, selecao de regimes e matriz de transicao.

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/11_regime_switching/`

### 05_ms_var.ipynb
- `from archbox.regime import MarkovSwitchingVAR`
- Dados multivariados (2-3 series macro)
- Spillovers entre variaveis em diferentes regimes
- Interpretar: como choques se propagam de forma diferente por regime

### 06_hamilton_filter.ipynb
- `from archbox.regime import HamiltonFilter, KimSmoother`
- Detalhamento do algoritmo:
  1. `HamiltonFilter.filter()` — probabilidades filtradas P(S_t|Y_t)
  2. `KimSmoother.smooth()` — probabilidades suavizadas P(S_t|Y_T)
  3. Diferenca: filtradas (tempo real) vs suavizadas (retrospectivo)
- `HamiltonFilter.ergodic_probabilities()` — probabilidades de longo prazo
- Plot: filtradas vs suavizadas ao longo do tempo

### 07_em_algorithm.ipynb
- `from archbox.regime import EMEstimator`
- `em = EMEstimator()` e `result = em.fit(model, maxiter=500, tol=1e-8, verbose=True)`
- Mostrar convergencia: log-likelihood a cada iteracao
- Discutir: multiplos pontos iniciais, maximos locais
- Comparar com MLE direto (se disponivel)

### 08_n_regimes.ipynb
- Comparar 2 vs 3 regimes no mesmo dataset
- AIC/BIC para selecao do numero de regimes
- Cuidados: identificabilidade, convergencia mais dificil com mais regimes
- Regra pratica: comecar com 2 e so aumentar se AIC/BIC melhorar significativamente

### 09_transicao.ipynb
- Foco na matriz de transicao:
  - `result.transition_matrix` — P(S_t=j | S_{t-1}=i)
  - Duracao esperada de cada regime: 1/(1-p_ii)
  - Probabilidades ergoticas: `HamiltonFilter.ergodic_probabilities(P)`
- `plot_transition_matrix()` — heatmap
- Interpretar economicamente: quanto tempo dura uma recessao em media?

---

## Criterios de Aceite

- [ ] Arquivo `05_ms_var.ipynb` criado com MS-VAR multivariado
- [ ] Arquivo `06_hamilton_filter.ipynb` criado com filtro e suavizador detalhados
- [ ] Arquivo `07_em_algorithm.ipynb` criado com convergencia do EM
- [ ] Arquivo `08_n_regimes.ipynb` criado com selecao 2 vs 3 regimes
- [ ] Arquivo `09_transicao.ipynb` criado com analise da matriz de transicao

---

**End of Specification**
