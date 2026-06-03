# Fase 02 — Cap 09: Notebooks Multivariados Intro

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 4 notebooks do capitulo 09 (Multivariados: Introducao).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/09_multivariados_intro/`

### 01_ccc_garch.ipynb
- `from archbox.multivariate import CCC`
- Dados: `load_dataset('fx_majors')` — USD/EUR, USD/GBP, USD/JPY
- `model = CCC(data.values)` e `result = model.fit()`
- Interpretar: matriz R constante, volatilidades univariadas
- Plot: `plot_correlation_heatmap()`

### 02_dcc_garch.ipynb
- `from archbox.multivariate import DCC`
- `model = DCC(data.values)` e `result = model.fit()`
- Parametros a, b da dinamica de correlacao
- Plot: `plot_dynamic_correlation()` — correlacao variando no tempo
- Comparar com CCC: quando a correlacao muda significativamente?

### 03_bekk_garch.ipynb
- `from archbox.multivariate import BEKK`
- `model = BEKK(data.values, variant='diagonal')` e `variant='full'`
- Discutir: curse of dimensionality (k^2 parametros na versao full)
- Garantia de positividade da matriz de covariancia

### 04_ccc_vs_dcc.ipynb
- Ajustar CCC e DCC nos mesmos dados
- Comparar: loglike, AIC, correlacoes
- Plot: correlacao CCC (linha reta) vs DCC (variando) ao longo do tempo
- Conclusao: DCC superior quando ha mudancas de regime na correlacao

---

## Criterios de Aceite

- [ ] Arquivo `01_ccc_garch.ipynb` criado com CCC e fx_majors
- [ ] Arquivo `02_dcc_garch.ipynb` criado com DCC e correlacao dinamica
- [ ] Arquivo `03_bekk_garch.ipynb` criado com BEKK diagonal e full
- [ ] Arquivo `04_ccc_vs_dcc.ipynb` criado com comparacao direta

---

**End of Specification**
