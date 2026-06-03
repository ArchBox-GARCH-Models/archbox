# Fase 02 — Cap 14: Notebooks Experimentos

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 5 notebooks do capitulo 14 (Experimentos e Comparacao de Modelos).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/14_experimentos/`

### 01_experiment_basico.ipynb
- `from archbox.experiment import ArchExperiment`
- `exp = ArchExperiment(returns, mean='constant')`
- `exp.fit_all_models(model_specs)` com lista de especificacoes
- model_specs: GARCH(1,1), EGARCH(1,1), GJR(1,1), APARCH(1,1), etc.

### 02_comparacao.ipynb
- `comparison = exp.compare_models()`
- Tabela automatica: loglike, AIC, BIC, num_params por modelo
- Ranking: melhor por AIC, melhor por BIC
- `ComparisonResult` com metodos de acesso

### 03_out_of_sample.ipynb
- `validation = exp.validate_out_of_sample(test_size=0.2)`
- Metricas out-of-sample: MAE, RMSE, QLIKE
- Comparar ranking in-sample (AIC) vs out-of-sample (RMSE)
- `ValidationResult` com metricas detalhadas

### 04_risk_analysis.ipynb
- `risk = exp.risk_analysis(alpha=0.05)`
- VaR e ES automatizados para todos os modelos
- Backtesting automatizado
- `RiskAnalysisResult` com sumario

### 05_workflow_completo.ipynb
- Pipeline end-to-end:
  1. Carregar dados (sp500)
  2. Criar experimento com 6 modelos
  3. Comparar in-sample
  4. Validar out-of-sample
  5. Analisar risco
  6. Selecionar melhor modelo
  7. Diagnosticar
  8. Gerar relatorio final

---

## Criterios de Aceite

- [ ] Arquivo `01_experiment_basico.ipynb` criado com ArchExperiment
- [ ] Arquivo `02_comparacao.ipynb` criado com tabela comparativa
- [ ] Arquivo `03_out_of_sample.ipynb` criado com validacao OOS
- [ ] Arquivo `04_risk_analysis.ipynb` criado com VaR/ES automatizado
- [ ] Arquivo `05_workflow_completo.ipynb` criado com pipeline end-to-end

---

**End of Specification**
