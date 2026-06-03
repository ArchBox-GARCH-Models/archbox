# Fase 03 — Cap 15: Primeiros Notebooks Visualizacao

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 5 primeiros notebooks do capitulo 15 (Visualizacao).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/15_visualizacao/`

### 01_volatilidade.ipynb
- `from archbox.visualization import plot_volatility, plot_variance_persistence`
- `plot_volatility(result)` — retornos + volatilidade condicional
- `plot_variance_persistence(result)` — decomposicao da persistencia
- Customizacao: figsize, cores, titulo

### 02_news_impact.ipynb
- `from archbox.visualization import plot_news_impact, plot_news_impact_comparison`
- NIC para um modelo e para multiplos modelos
- Customizacao de eixos e labels

### 03_diagnosticos_plot.ipynb
- `from archbox.visualization import plot_diagnostics`
- `plot_diagnostics(result, lags=[5, 10])` — painel: ACF, PACF, QQ-plot
- Interpretar cada subplot

### 04_regimes_plot.ipynb
- `from archbox.visualization import plot_regimes, plot_transition_matrix`
- `plot_regimes(result)` — dados + probabilidades filtradas/suavizadas
- `plot_transition_matrix(P)` — heatmap da matriz de transicao

### 05_correlacao.ipynb
- `from archbox.visualization import plot_dynamic_correlation, plot_correlation_heatmap, plot_covariance_decomposition`
- Correlacao dinamica DCC ao longo do tempo
- Heatmap de correlacao em um ponto no tempo
- Decomposicao da covariancia

---

## Criterios de Aceite

- [ ] Arquivo `01_volatilidade.ipynb` criado com plot_volatility
- [ ] Arquivo `02_news_impact.ipynb` criado com NIC plots
- [ ] Arquivo `03_diagnosticos_plot.ipynb` criado com plot_diagnostics
- [ ] Arquivo `04_regimes_plot.ipynb` criado com plot_regimes
- [ ] Arquivo `05_correlacao.ipynb` criado com correlation plots

---

**End of Specification**
