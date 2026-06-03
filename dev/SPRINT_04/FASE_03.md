# Fase 03 — Cap 09 Scripts R/Stata + Cap 10 Notebooks Avancados

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata do cap 09 e os 4 notebooks do cap 10 (Multivariados Avancados).

---

## Descricao Tecnica

### Cap 09 — Scripts

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/09_multivariados_intro/`

#### 01_ccc.R
- rmgarch: `dccspec(dccOrder = c(0, 0))` para CCC
- `dccfit(spec, data)`
- `rcor(fit)` para correlacao constante

#### 02_dcc.R
- rmgarch: `dccspec(dccOrder = c(1, 1))`
- `dccfit(spec, data)`
- `rcor(fit)` para correlacao dinamica

#### 01_dcc.do
- Stata: `mgarch dcc (y1 y2 = , noconstant), arch(1) garch(1)`

### Cap 10 — Notebooks Avancados

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/10_multivariados_avancados/`

#### 01_deco.ipynb
- `from archbox.multivariate import DECO`
- Dados: `load_dataset('sector_indices')` — 5 series
- DECO: equicorrelacao escalar — todas as correlacoes iguais
- Vantagem: altamente escalavel para portfolios grandes
- Interpretar rho_t escalar

#### 02_gogarch.ipynb
- `from archbox.multivariate import GOGARCH`
- Dados: `load_dataset('fx_majors')`
- ICA para fatores independentes
- Mixing matrix: Z = transformacao
- Interpretar fatores latentes

#### 03_escalabilidade.ipynb
- Benchmark de tempo: CCC vs DCC vs BEKK vs DECO vs GO-GARCH
- Para k=2, 3, 5 series
- Tabela: modelo, k, tempo de execucao
- BEKK explode com k; DECO e GO-GARCH escalam bem

#### 04_covariance_decomp.ipynb
- `plot_covariance_decomposition()` com resultado DCC
- Decompor H_t = D_t R_t D_t: volatilidade vs correlacao
- Quando a covariancia muda: por volatilidade ou por correlacao?

---

## Criterios de Aceite

- [ ] Arquivo `09_multivariados_intro/01_ccc.R` criado
- [ ] Arquivo `09_multivariados_intro/02_dcc.R` criado
- [ ] Arquivo `09_multivariados_intro/01_dcc.do` criado
- [ ] Arquivo `10_multivariados_avancados/01_deco.ipynb` criado
- [ ] Arquivo `10_multivariados_avancados/02_gogarch.ipynb` criado
- [ ] Arquivo `10_multivariados_avancados/03_escalabilidade.ipynb` criado
- [ ] Arquivo `10_multivariados_avancados/04_covariance_decomp.ipynb` criado

---

**End of Specification**
