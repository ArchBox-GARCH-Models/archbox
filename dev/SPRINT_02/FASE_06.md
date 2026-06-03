# Fase 06 — Cap 06: Scripts R e Stata Diagnosticos

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata equivalentes para o capitulo 06 (Diagnosticos).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/06_diagnosticos/`

### 01_diagnosticos.R
- rugarch pos-estimacao:
  - `nyblom(fit)` — teste de estabilidade de Nyblom
  - `signbias(fit)` — sign bias test
  - `gof(fit, grouping = 20)` — goodness-of-fit
  - `infocriteria(fit)` — criterios de informacao
  - Residuos: `residuals(fit, standardize = TRUE)`
  - Box test: `Box.test(residuals(fit, standardize = TRUE)^2, lag = 10, type = "Ljung-Box")`

### 01_diagnosticos.do
- Stata pos-estimacao:
  - `estat archlm, lags(5)` — teste ARCH-LM
  - `estat bgodfrey, lags(5)` — autocorrelacao
  - `predict resid, residuals`
  - Testes manuais nos residuos

---

## Criterios de Aceite

- [ ] Arquivo `01_diagnosticos.R` criado com nyblom, signbias, gof, Box.test
- [ ] Arquivo `01_diagnosticos.do` criado com estat archlm e bgodfrey
- [ ] Ambos com comentarios em portugues

---

**End of Specification**
