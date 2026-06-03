# Fase 03 — Cap 04 Scripts R/Stata + Cap 05 Notebooks Distribuicoes

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata do cap 04 e os 5 notebooks do cap 05 (Distribuicoes Condicionais).

---

## Descricao Tecnica

### Cap 04 — Scripts R e Stata

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/04_garch_avancados/`

#### 01_igarch.R
- rugarch: `ugarchspec(variance.model = list(model = "iGARCH"))` com bitcoin
- Comparar com EWMA manual

#### 02_figarch.R
- rugarch: `ugarchspec(variance.model = list(model = "fiGARCH"))` com sp500
- Parametro d fracionario

#### 03_garch_m.R
- rugarch: `ugarchspec(mean.model = list(archm = TRUE, archpow = 2))` com sp500
- archpow: 1 (volatility), 2 (variance)

#### 01_igarch.do
- Stata: IGARCH com constraint de persistencia unitaria

### Cap 05 — Notebooks Distribuicoes

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/05_distribuicoes/`

#### 01_normal_vs_t.ipynb
- GARCH(1,1) com dist='normal' vs dist='t'
- QQ-plot dos residuos padronizados
- Comparar loglike, AIC — Student-t quase sempre ganha
- Funcionalidades: `GARCH(endog, dist='normal')`, `GARCH(endog, dist='t')`

#### 02_ged.ipynb
- GARCH(1,1) com dist='ged': `from archbox.distributions import GeneralizedError`
- Parametro de forma: > 2 (caudas leves), < 2 (caudas pesadas), = 2 (normal)
- Plot da densidade GED para diferentes parametros

#### 03_skewed_t.ipynb
- GARCH(1,1) com dist='skewt': `from archbox.distributions import SkewedT`
- Parametros: nu (graus de liberdade), lambda (assimetria)
- Aplicacao em ibovespa e usdbrl — mercados emergentes com assimetria
- Plot: densidade simetrica vs assimetrica

#### 04_mixture_normal.ipynb
- GARCH(1,1) com MixtureNormal
- Parametros: peso da mistura, razao de volatilidade
- Interpretacao: "regime calmo" + "regime turbulento" misturados
- Plot: densidade bimodal

#### 05_comparacao_completa.ipynb
- Todas as 5 distribuicoes no sp500
- Tabela: loglike, AIC, BIC, num_params para cada
- QQ-plot de cada uma
- Conclusao: qual distribuicao selecionar?
- Funcionalidades: `plot_distribution_fit()`

---

## Criterios de Aceite

- [ ] Arquivo `04_garch_avancados/01_igarch.R` criado
- [ ] Arquivo `04_garch_avancados/02_figarch.R` criado
- [ ] Arquivo `04_garch_avancados/03_garch_m.R` criado
- [ ] Arquivo `04_garch_avancados/01_igarch.do` criado
- [ ] Arquivo `05_distribuicoes/01_normal_vs_t.ipynb` criado
- [ ] Arquivo `05_distribuicoes/02_ged.ipynb` criado
- [ ] Arquivo `05_distribuicoes/03_skewed_t.ipynb` criado
- [ ] Arquivo `05_distribuicoes/04_mixture_normal.ipynb` criado
- [ ] Arquivo `05_distribuicoes/05_comparacao_completa.ipynb` criado

---

**End of Specification**
