# Fase 06 — Cap 17: Validacao Cruzada com R

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 3 notebooks e 3 scripts R do capitulo 17 (Validacao Cruzada com R).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/17_validacao_cruzada/`

### Notebooks Python (comparacao)

#### 01_vs_rugarch.ipynb
- Ajustar GARCH(1,1), EGARCH(1,1), GJR(1,1) com archbox
- Carregar resultados de referencia do rugarch (gerados pelo script R)
- Comparar: parametros, standard errors, log-likelihood
- Tolerancia numerica: |archbox - rugarch| < 1e-3
- Tabela: parametro, archbox, rugarch, diferenca

#### 02_vs_rmgarch.ipynb
- Ajustar CCC e DCC com archbox
- Carregar resultados de referencia do rmgarch
- Comparar: correlacoes, parametros DCC (a, b), log-likelihood
- Plot: correlacao dinamica archbox vs rmgarch sobrepostas

#### 03_vs_mswm.ipynb
- Ajustar MS-Mean e MS-AR com archbox
- Carregar resultados de referencia do MSwM
- Comparar: probabilidades suavizadas, parametros por regime, matriz de transicao
- Plot: probabilidades archbox vs MSwM sobrepostas

### Scripts R (benchmark)

#### 01_rugarch_benchmark.R
- Script completo para gerar resultados de referencia:
  - Carregar dados (mesmo CSV usado no archbox)
  - GARCH(1,1): `ugarchspec` + `ugarchfit` → salvar coef, se, loglik em CSV
  - EGARCH(1,1): idem
  - GJR(1,1): idem
  - Salvar resultados em `rugarch_results.csv`

#### 02_rmgarch_benchmark.R
- Script completo para gerar resultados de referencia:
  - Carregar dados multivariados
  - CCC: `dccspec(dccOrder=c(0,0))` + `dccfit` → salvar R, loglik
  - DCC: `dccspec(dccOrder=c(1,1))` + `dccfit` → salvar correlacoes, params
  - Salvar resultados em `rmgarch_results.csv`

#### 03_mswm_benchmark.R
- Script completo para gerar resultados de referencia:
  - Carregar dados macro
  - MS-Mean: `msmFit(lm_model, k=2)` → salvar params, probs, P
  - MS-AR: `msmFit(ar_model, k=2)` → salvar params, probs, P
  - Salvar resultados em `mswm_results.csv`

---

## Instrucoes

1. Notebooks Python devem esperar arquivos CSV de referencia gerados pelos scripts R
2. Scripts R devem ser auto-contidos e gerar CSVs no mesmo diretorio
3. Incluir instrucoes de como rodar os scripts R antes dos notebooks

---

## Criterios de Aceite

- [ ] Arquivo `01_vs_rugarch.ipynb` criado com comparacao GARCH/EGARCH/GJR
- [ ] Arquivo `02_vs_rmgarch.ipynb` criado com comparacao CCC/DCC
- [ ] Arquivo `03_vs_mswm.ipynb` criado com comparacao MS-Mean/MS-AR
- [ ] Arquivo `01_rugarch_benchmark.R` criado e auto-contido
- [ ] Arquivo `02_rmgarch_benchmark.R` criado e auto-contido
- [ ] Arquivo `03_mswm_benchmark.R` criado e auto-contido

---

**End of Specification**
