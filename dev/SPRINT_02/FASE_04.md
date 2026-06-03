# Fase 04 — Cap 05: Scripts R e Stata Distribuicoes

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata equivalentes para o capitulo 05 (Distribuicoes Condicionais).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/05_distribuicoes/`

### 01_distribuicoes.R
- rugarch com diferentes distribution.model:
  - `"norm"` (Normal)
  - `"std"` (Student-t)
  - `"ged"` (GED)
  - `"sstd"` (Skewed Student-t)
- Ajustar GARCH(1,1) com cada distribuicao
- `infocriteria(fit)` para comparacao
- `plot(fit, which = 9)` para QQ-plot

### 01_distribuicoes.do
- Stata: `arch returns, arch(1) garch(1) distribution(t df(8))`
- Comparar Normal vs Student-t
- `estat ic` para AIC/BIC

---

## Criterios de Aceite

- [ ] Arquivo `01_distribuicoes.R` criado com 4 distribuicoes do rugarch
- [ ] Arquivo `01_distribuicoes.do` criado com Normal vs Student-t no Stata
- [ ] Ambos com comentarios em portugues

---

**End of Specification**
