# Fase 03 — Cap 07 Scripts R/Stata + Cap 08 Primeiros Notebooks Risco

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata do cap 07 e os primeiros 3 notebooks do cap 08 (VaR).

---

## Descricao Tecnica

### Cap 07 — Scripts

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/07_previsao/`

#### 01_previsao.R
- rugarch: `ugarchforecast(fit, n.ahead = 22)` — previsao multi-passos
- `ugarchroll(spec, data, n.ahead = 1, forecast.length = 500)` — rolling forecast
- Plot forecast

#### 01_previsao.do
- Stata: `arch returns, arch(1) garch(1)` seguido de `predict sigma2, variance`
- Forecast estatico

### Cap 08 — Primeiros Notebooks

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/08_risco/`

#### 01_var_parametrico.ipynb
- `from archbox.risk import ValueAtRisk`
- `var = ValueAtRisk(result, alpha=0.05)`
- `var.parametric(dist='normal')` e `var.parametric(dist='t', nu=8.0)`
- VaR 1% e 5%
- Plot: retornos com linhas de VaR

#### 02_var_historico.ipynb
- `var.historical()` — VaR historico simples
- `var.filtered_historical()` — Filtered Historical Simulation (FHS)
- Comparar: FHS adapta-se a mudancas de volatilidade, historico nao
- Barone-Adesi et al. (1999)

#### 03_var_montecarlo.ipynb
- `var.montecarlo(n_sims=10000)`
- Efeito do numero de simulacoes: 1000, 5000, 10000, 50000
- Convergencia do VaR estimado
- Quando usar MC vs parametrico

---

## Criterios de Aceite

- [ ] Arquivo `07_previsao/01_previsao.R` criado
- [ ] Arquivo `07_previsao/01_previsao.do` criado
- [ ] Arquivo `08_risco/01_var_parametrico.ipynb` criado com Normal e Student-t
- [ ] Arquivo `08_risco/02_var_historico.ipynb` criado com HS e FHS
- [ ] Arquivo `08_risco/03_var_montecarlo.ipynb` criado com convergencia

---

**End of Specification**
