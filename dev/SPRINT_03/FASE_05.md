# Fase 05 — Cap 08: Scripts R e Stata Risco

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata equivalentes para o capitulo 08 (Risco).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/08_risco/`

### 01_var.R
- rugarch:
  - Ajustar GARCH(1,1): `fit <- ugarchfit(spec, data)`
  - VaR parametrico: `quantile(ugarchforecast(fit), probs = 0.05)`
  - Rolling VaR: `ugarchroll(spec, data, forecast.length = 500)`
  - VaR backtest: `VaRTest(alpha = 0.05, actual = returns, VaR = var_series)`
  - Kupiec e Christoffersen tests

### 01_var.do
- Stata:
  - `arch returns, arch(1) garch(1)`
  - `predict sigma2, variance`
  - VaR manual: `gen var_95 = -1.645 * sqrt(sigma2)`
  - Backtest manual: contar violacoes

---

## Criterios de Aceite

- [ ] Arquivo `01_var.R` criado com VaR, rolling, e backtesting via rugarch
- [ ] Arquivo `01_var.do` criado com VaR manual e backtest
- [ ] Ambos com comentarios em portugues

---

**End of Specification**
