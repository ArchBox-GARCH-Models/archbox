# Fase 06 — Cap 12: Scripts R e Stata Threshold

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar scripts R e Stata equivalentes para o capitulo 12 (Threshold/STAR).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/12_threshold_star/`

### 01_setar.R
- tsDyn: `library(tsDyn)`
- `setar(data, m = 4, d = 1, steps = 2)` — SETAR com auto-selecao
- `summary()` e `plot()`
- Comparar com archbox

### 02_star.R
- tsDyn:
  - `lstar(data, m = 4, d = 1)` — LSTAR
  - `summary()`, plot da funcao de transicao
  - Comparar gamma e c com archbox

### 01_threshold.do
- Stata: modelos threshold com dados de painel ou series temporais
- Comandos basicos de threshold regression

---

## Criterios de Aceite

- [ ] Arquivo `01_setar.R` criado com SETAR via tsDyn
- [ ] Arquivo `02_star.R` criado com LSTAR via tsDyn
- [ ] Arquivo `01_threshold.do` criado com threshold regression do Stata
- [ ] Todos com comentarios em portugues

---

**End of Specification**
