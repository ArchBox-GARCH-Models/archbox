# Fase 05 — Cap 13: Script R Portfolio

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar script R equivalente para o capitulo 13 (Portfolio).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/13_portfolio/`

### 01_portfolio.R
- rmgarch:
  - Ajustar DCC: `dccfit(spec, data)`
  - Extrair H_t: `rcov(fit)`
  - Pesos min-variance: resolver quadprog
  - Risk contribution: `wmargin("H", w, cov = sigma)` (se disponivel no rmgarch)
  - Comparar equal-weight vs min-variance

---

## Criterios de Aceite

- [ ] Arquivo `01_portfolio.R` criado com DCC + min-variance + risk contribution
- [ ] Comentarios em portugues

---

**End of Specification**
