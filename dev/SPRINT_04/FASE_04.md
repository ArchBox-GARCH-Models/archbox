# Fase 04 — Cap 10 Scripts R + Cap 13 Notebooks Portfolio

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R do cap 10 e os 5 notebooks do cap 13 (Portfolio e Risco Multivariado).

---

## Descricao Tecnica

### Cap 10 — Scripts R

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/10_multivariados_avancados/`

#### 01_gogarch.R
- rmgarch: `gogarchspec(mean.model = "constant")` e `gogarchfit(spec, data)`

#### 02_deco.R
- rmgarch: `dccspec(dccOrder = c(1, 1), model = "DCC")` com type DECO

### Cap 13 — Notebooks Portfolio

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/13_portfolio/`

#### 01_portfolio_variance.ipynb
- `from archbox.multivariate.portfolio import portfolio_variance, portfolio_volatility`
- Pesos fixos: equal-weight (1/k) e custom
- Calcular variancia e volatilidade do portfolio ao longo do tempo
- Plot: volatilidade do portfolio vs volatilidade individual de cada ativo

#### 02_min_variance.ipynb
- `from archbox.multivariate.portfolio import minimum_variance_weights`
- Pesos otimos estaticos (usando H medio)
- `minimum_variance_weights_dynamic()` — pesos que mudam ao longo do tempo
- Plot: evolucao dos pesos ao longo do tempo

#### 03_risk_decomposition.ipynb
- `from archbox.multivariate.portfolio import risk_contribution, marginal_risk_contribution, risk_decomposition`
- Atribuicao de risco: quanto cada ativo contribui para o risco total
- Plot: stacked bar chart de contribuicao de risco

#### 04_dynamic_allocation.ipynb
- Alocacao dinamica com DCC:
  1. Ajustar DCC em 3 ativos
  2. Para cada t: calcular H_t → minimum_variance_weights(H_t)
  3. Plot: pesos dinamicos ao longo do tempo
  4. Backtest: retorno do portfolio com pesos dinamicos vs estaticos

#### 05_caso_pratico.ipynb
- Caso completo end-to-end:
  1. 5 ativos: `load_dataset('sector_indices')`
  2. Ajustar DCC
  3. Pesos dinamicos
  4. Risk decomposition
  5. Backtest do portfolio: retorno acumulado, Sharpe ratio
  6. Comparar com equal-weight

---

## Criterios de Aceite

- [ ] Arquivo `10_multivariados_avancados/01_gogarch.R` criado
- [ ] Arquivo `10_multivariados_avancados/02_deco.R` criado
- [ ] Arquivo `13_portfolio/01_portfolio_variance.ipynb` criado
- [ ] Arquivo `13_portfolio/02_min_variance.ipynb` criado
- [ ] Arquivo `13_portfolio/03_risk_decomposition.ipynb` criado
- [ ] Arquivo `13_portfolio/04_dynamic_allocation.ipynb` criado
- [ ] Arquivo `13_portfolio/05_caso_pratico.ipynb` criado

---

**End of Specification**
