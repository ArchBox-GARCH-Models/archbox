# Fase 02 — Cap 11: Primeiros Notebooks Regime-Switching

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 4 primeiros notebooks do capitulo 11 (Regime-Switching).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/11_regime_switching/`

### 01_ms_mean.ipynb
- `from archbox.regime import MarkovSwitchingMean`
- Dados: `load_dataset('us_gdp')` — PIB trimestral
- `model = MarkovSwitchingMean(data, k_regimes=2)` e `result = model.fit()`
- Interpretar: regime 1 (expansao, media alta) vs regime 2 (recessao, media baixa)
- `result.smoothed_probs` — probabilidade de cada regime
- `plot_regimes(result)` — dados + probabilidades de regime
- `result.transition_matrix` — probabilidades de transicao

### 02_ms_meanvar.ipynb
- `from archbox.regime import MarkovSwitchingMeanVar`
- Media E variancia mudam entre regimes
- Comparar com MS-Mean: variancia constante vs variavel
- Aplicacao: identificar periodos de crise (alta volatilidade + retorno baixo)

### 03_ms_ar.ipynb
- `from archbox.regime import MarkovSwitchingAR`
- `model = MarkovSwitchingAR(data, k_regimes=2, order=4)`
- Replicacao de Hamilton (1989) com dados de PIB
- Interpretar coeficientes AR por regime
- `switching_ar=True` vs `switching_ar=False`

### 04_ms_garch.ipynb
- `from archbox.regime import MarkovSwitchingGARCH`
- Dados: `load_dataset('sp500')`
- `model = MarkovSwitchingGARCH(data, k_regimes=2)` — Gray (1996)
- Regimes de alta e baixa volatilidade com dinamica GARCH em cada
- Interpretar: omega, alpha, beta diferentes por regime

---

## Criterios de Aceite

- [ ] Arquivo `01_ms_mean.ipynb` criado com us_gdp e 2 regimes
- [ ] Arquivo `02_ms_meanvar.ipynb` criado com media e variancia switching
- [ ] Arquivo `03_ms_ar.ipynb` criado com Hamilton (1989) replication
- [ ] Arquivo `04_ms_garch.ipynb` criado com Gray (1996) MS-GARCH

---

**End of Specification**
