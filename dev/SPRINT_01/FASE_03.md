# Fase 03 — Cap 01: Scripts R e Stata

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os scripts equivalentes em R e Stata para o capitulo 01 (Introducao), permitindo comparacao direta com o notebook Python.

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/01_introducao/`

**Arquivos a criar**:

### 01_quickstart.R

Script R equivalente ao notebook quickstart:
- Comentarios em portugues explicando cada etapa
- Carregar pacote rugarch: `library(rugarch)`
- Carregar dados SP500 (usar `data(sp500ret)` do rugarch ou ler CSV exportado)
- Especificar modelo: `spec <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1,1)), mean.model = list(armaOrder = c(0,0), include.mean = TRUE), distribution.model = "norm")`
- Ajustar: `fit <- ugarchfit(spec, data)`
- Resultados: `show(fit)`, `coef(fit)`, `persistence(fit)`, `halflife(fit)`, `uncvariance(fit)`
- Plot: `plot(fit, which = 3)` — volatilidade condicional
- Comentario final comparando com archbox

### 01_quickstart.do

Script Stata equivalente:
- Comentarios em portugues
- Carregar dados: `import delimited "sp500.csv", clear` (ou gerar dados sinteticos)
- Ajustar GARCH(1,1): `arch returns, arch(1) garch(1)`
- Resultados: exibir coeficientes
- Pos-estimacao: `predict sigma2, variance` e `predict resid, residuals`
- Plot: `tsline sigma2, title("Volatilidade Condicional")`
- Estatisticas: `estat ic` para AIC/BIC

---

## Instrucoes

1. Scripts R devem ser arquivos `.R` validos com comentarios `#`
2. Scripts Stata devem ser arquivos `.do` validos com comentarios `//` ou `*`
3. Ambos devem replicar o fluxo do notebook Python o mais proximo possivel
4. Incluir nota no inicio explicando que e o equivalente do notebook Python

---

## Criterios de Aceite

- [ ] Arquivo `01_quickstart.R` criado com rugarch equivalente ao notebook Python
- [ ] Arquivo `01_quickstart.do` criado com comandos arch do Stata
- [ ] Ambos com comentarios em portugues
- [ ] Ambos com nota de referencia ao notebook Python equivalente

---

**End of Specification**
