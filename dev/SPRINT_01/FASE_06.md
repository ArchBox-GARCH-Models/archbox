# Fase 06 — Cap 03: Scripts R e Stata Assimetricos

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os scripts R e Stata equivalentes para o capitulo 03 (GARCH Assimetricos).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/03_garch_assimetricos/`

**Arquivos a criar**:

### 01_egarch.R

EGARCH em R com rugarch:
- `spec <- ugarchspec(variance.model = list(model = "eGARCH", garchOrder = c(1,1)))`
- `fit <- ugarchfit(spec, data)`
- Interpretar `coef(fit)`: alpha1 (magnitude), gamma1 (assimetria)
- `newsimpact(fit)` para NIC
- Comparar com sGARCH

### 02_gjr_garch.R

GJR-GARCH em R com rugarch:
- `spec <- ugarchspec(variance.model = list(model = "gjrGARCH", garchOrder = c(1,1)))`
- `fit <- ugarchfit(spec, data)`
- Interpretar gamma1 como leverage effect
- `newsimpact(fit)`

### 03_aparch.R

APARCH em R com rugarch:
- `spec <- ugarchspec(variance.model = list(model = "apARCH", garchOrder = c(1,1)))`
- `fit <- ugarchfit(spec, data)`
- Interpretar delta (potencia) e gamma (assimetria)

### 01_egarch.do

EGARCH em Stata:
- `arch returns, earch(1) egarch(1)`
- Interpretar coeficientes
- `predict sigma2, variance`

### 02_gjr_garch.do

GJR-GARCH em Stata:
- `arch returns, arch(1) garch(1) tarch(1)`
- tarch(1) captura o efeito leverage
- `estat ic` para comparacao

---

## Instrucoes

1. Scripts R com pacote rugarch
2. Scripts Stata com comandos nativos arch
3. Comentarios em portugues
4. Nota de referencia ao notebook Python equivalente

---

## Criterios de Aceite

- [ ] Arquivo `01_egarch.R` criado com eGARCH via rugarch
- [ ] Arquivo `02_gjr_garch.R` criado com gjrGARCH via rugarch
- [ ] Arquivo `03_aparch.R` criado com apARCH via rugarch
- [ ] Arquivo `01_egarch.do` criado com earch/egarch do Stata
- [ ] Arquivo `02_gjr_garch.do` criado com tarch do Stata
- [ ] Todos com comentarios em portugues

---

**End of Specification**
