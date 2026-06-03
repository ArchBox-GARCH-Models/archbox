# Fase 02 — Cap 07: Notebooks de Previsao

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 4 notebooks do capitulo 07 (Previsao de Volatilidade).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/07_previsao/`

### 01_previsao_analitica.ipynb
- `result.forecast(horizon=1, method='analytic')` — 1 passo a frente
- Expandir: horizon=5, 22 (semana, mes)
- Plot: previsao de volatilidade com intervalo
- Interpretar: convergencia para variancia incondicional

### 02_previsao_simulacao.ipynb
- `result.forecast(horizon=22, method='simulation')`
- Fan charts: percentis 5%, 25%, 50%, 75%, 95%
- Comparar com metodo analitico
- Quando usar simulacao vs analitico

### 03_rolling_window.ipynb
- Rolling window forecast manual:
  - Expanding window (cresce) vs fixed window (250 dias)
  - Para cada janela: fit → forecast 1-step → armazenar
- Metricas: MAE, RMSE, QLIKE
- Ou usar `ArchExperiment.validate_out_of_sample(test_size=0.2)`

### 04_comparacao_modelos.ipynb
- Forecast de GARCH vs EGARCH vs GJR no sp500
- Rolling window para cada modelo
- Tabela: MAE, RMSE, QLIKE por modelo
- Conclusao: qual modelo preve melhor out-of-sample?

---

## Criterios de Aceite

- [ ] Arquivo `01_previsao_analitica.ipynb` criado com horizontes 1, 5, 22
- [ ] Arquivo `02_previsao_simulacao.ipynb` criado com fan charts
- [ ] Arquivo `03_rolling_window.ipynb` criado com expanding e fixed window
- [ ] Arquivo `04_comparacao_modelos.ipynb` criado com 3 modelos comparados

---

**End of Specification**
