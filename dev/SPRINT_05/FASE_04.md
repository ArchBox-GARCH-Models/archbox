# Fase 04 — Cap 11 Scripts R/Stata + Cap 12 Primeiros Notebooks Threshold

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata do cap 11 e os 4 primeiros notebooks do cap 12 (Threshold/STAR).

---

## Descricao Tecnica

### Cap 11 — Scripts

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/11_regime_switching/`

#### 01_ms_mean.R
- MSwM: `library(MSwM)` e `msmFit(lm_model, k = 2, sw = c(TRUE, TRUE))`
- Comparar com archbox: probabilidades suavizadas e parametros

#### 02_ms_ar.R
- MSwM: `msmFit(ar_model, k = 2, sw = rep(TRUE, 6))`
- Hamilton (1989) replication em R

#### 01_ms_mean.do
- Stata: `mswitch dr gdp_growth, states(2) varswitch`
- Interpretar output do Stata

### Cap 12 — Primeiros Notebooks

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/12_threshold_star/`

#### 01_testes_linearidade.ipynb
- `from archbox.threshold import linearity_test, tsay_test, hansen_threshold_test`
- Aplicar em us_unemployment e industrial_production
- Interpretar: p-valor < 0.05 = rejeita linearidade → modelo nao-linear justificado
- Quando cada teste e mais apropriado

#### 02_transition_type.ipynb
- `from archbox.threshold import transition_type_test`
- Determinar LSTAR vs ESTAR:
  - H04 rejeitada → LSTAR
  - H03 rejeitada → ESTAR
- Sequencia de testes de Terasvirta (1994)

#### 03_tar.ipynb
- `from archbox.threshold import TAR`
- Dados: us_unemployment com threshold exogeno
- `model = TAR(data, order=1, delay=1, threshold_var=external)`
- Grid search para threshold c
- Interpretar: coeficientes diferentes acima/abaixo do threshold

#### 04_setar.ipynb
- `from archbox.threshold import SETAR`
- Dados: industrial_production
- `model = SETAR(data, order=1, d_max=6, ic='aic')`
- Auto-selecao de delay d
- 2 regimes e 3 regimes (2 thresholds)
- Plot: dados com regioes de regime marcadas

---

## Criterios de Aceite

- [ ] Arquivo `11_regime_switching/01_ms_mean.R` criado com MSwM
- [ ] Arquivo `11_regime_switching/02_ms_ar.R` criado com MSwM
- [ ] Arquivo `11_regime_switching/01_ms_mean.do` criado com mswitch
- [ ] Arquivo `12_threshold_star/01_testes_linearidade.ipynb` criado
- [ ] Arquivo `12_threshold_star/02_transition_type.ipynb` criado
- [ ] Arquivo `12_threshold_star/03_tar.ipynb` criado
- [ ] Arquivo `12_threshold_star/04_setar.ipynb` criado

---

**End of Specification**
