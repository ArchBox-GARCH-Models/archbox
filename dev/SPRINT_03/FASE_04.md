# Fase 04 — Cap 08: Notebooks Risco (ES, EWMA, Backtesting, Comparacao, Workflow)

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 5 notebooks restantes do capitulo 08 (Risco).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/08_risco/`

### 04_expected_shortfall.ipynb
- `from archbox.risk import ExpectedShortfall`
- `es = ExpectedShortfall(result, alpha=0.05)`
- 4 metodos: `parametric()`, `historical()`, `filtered_historical()`, `cornish_fisher()`
- ES vs VaR: ES e a perda media alem do VaR (mais conservador)
- Tabela comparativa dos 4 metodos

### 05_ewma_riskmetrics.ipynb
- `from archbox.risk import EWMA`
- `ewma = EWMA(returns, lam=0.94)` (diario) e `lam=0.97` (mensal)
- `ewma_result = ewma.fit()`
- Comparar com GARCH(1,1): plot volatilidade
- Explicar: EWMA = IGARCH com omega=0

### 06_backtesting.ipynb
- `from archbox.risk import VaRBacktest`
- `bt = VaRBacktest(returns, var_series, alpha=0.05)`
- `bt.kupiec_pof()` — Proportion of Failures
- `bt.christoffersen()` — independencia das violacoes
- `bt.basel_traffic_light()` — framework Basel III
- `bt.summary()` — relatorio completo
- `plot_var_backtest()`, `plot_traffic_light()`

### 07_comparacao_metodos.ipynb
- Calcular VaR com 4 metodos: parametrico, historico, FHS, MC
- Backtest de todos
- Tabela: taxa de violacao, Kupiec p-value, Christoffersen p-value, Basel zone
- `plot_var_comparison()` — todos no mesmo grafico
- Conclusao: qual metodo performa melhor para cada serie?

### 08_workflow_risco.ipynb
- Pipeline completo end-to-end:
  1. Carregar dados (sp500)
  2. Ajustar GARCH(1,1) com dist='t'
  3. Calcular VaR e ES (parametrico + FHS)
  4. Backtest completo
  5. Gerar relatorio com ReportManager
- Caso de uso real para um risk analyst

---

## Criterios de Aceite

- [ ] Arquivo `04_expected_shortfall.ipynb` criado com 4 metodos de ES
- [ ] Arquivo `05_ewma_riskmetrics.ipynb` criado com lambda 0.94 e 0.97
- [ ] Arquivo `06_backtesting.ipynb` criado com Kupiec, Christoffersen, Basel
- [ ] Arquivo `07_comparacao_metodos.ipynb` criado com 4 metodos de VaR comparados
- [ ] Arquivo `08_workflow_risco.ipynb` criado com pipeline end-to-end

---

**End of Specification**
