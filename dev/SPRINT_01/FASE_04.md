# Fase 04 — Cap 02: Notebooks GARCH Classico

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 6 notebooks Jupyter do capitulo 02 (GARCH Classico) explorando o modelo GARCH(p,q) em profundidade.

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/02_garch_classico/`

**Arquivos a criar**:

### 01_garch_basico.ipynb

GARCH(1,1) basico com multiplas series:
- Ajustar GARCH(1,1) em 3 series: sp500, bitcoin, usdbrl
- Comparar parametros (omega, alpha, beta) entre as series
- Interpretar: qual mercado tem maior persistencia? maior variancia incondicional?
- Plot de volatilidade condicional das 3 series lado a lado
- Funcionalidades: `GARCH(endog, p=1, q=1)`, `.fit()`, `.summary()`, `.plot()`

### 02_ordens_pq.ipynb

Comparacao de ordens GARCH(p,q):
- Ajustar GARCH(1,1), GARCH(1,2), GARCH(2,1), GARCH(2,2) no sp500
- Tabela comparativa: loglike, AIC, BIC, HQIC, num_params
- Interpretar: qual ordem e selecionada por cada criterio?
- Discussao sobre parcimonia vs ajuste
- Funcionalidades: `result.aic`, `result.bic`, `result.hqic`, `result.loglike`

### 03_media_condicional.ipynb

Opcoes de media condicional:
- Ajustar GARCH(1,1) com mean='zero', mean='constant', mean='ar'
- Comparar parametros de volatilidade: mudam com a especificacao da media?
- Interpretar: quando usar cada opcao
- Funcionalidades: `GARCH(endog, mean='zero')`, `GARCH(endog, mean='constant')`, `GARCH(endog, mean='ar')`

### 04_variance_targeting.ipynb

Variance targeting:
- Ajustar GARCH(1,1) com e sem variance_targeting
- Comparar: parametros, standard errors, convergencia
- Explicar: omega fixado na variancia amostral, beneficios numericos
- Funcionalidades: `model.fit(variance_targeting=True)`

### 05_persistencia.ipynb

Persistencia e metricas derivadas:
- Ajustar GARCH(1,1) em sp500 e bitcoin
- Calcular: `persistence()` (alpha + beta), `half_life()`, `unconditional_variance()`
- Interpretar economicamente: o que significa persistencia de 0.98 vs 0.85?
- Plot: decaimento de um choque ao longo do tempo (impulse response)
- Funcionalidades: `result.persistence()`, `result.half_life()`, `result.unconditional_variance()`

### 06_simulacao.ipynb

Simulacao de processos GARCH:
- Ajustar GARCH(1,1) no sp500 e obter parametros estimados
- Simular 5 paths: `model.simulate(n=1000, params=result.params)`
- Plot: retornos simulados e volatilidade simulada
- Comparar estatisticas descritivas: dados reais vs simulados
- Aplicacao: stress testing, bootstrap
- Funcionalidades: `model.simulate(n, params, seed)`

---

## Instrucoes

1. Cada notebook deve ter celulas alternando Markdown (explicacao) e Code (execucao)
2. Usar `from archbox import GARCH` e `from archbox.datasets import load_dataset`
3. Texto explicativo em portugues, codigo em ingles
4. Outputs vazios (serao preenchidos na execucao)

---

## Criterios de Aceite

- [ ] Arquivo `01_garch_basico.ipynb` criado com 3 series comparadas
- [ ] Arquivo `02_ordens_pq.ipynb` criado com tabela comparativa AIC/BIC
- [ ] Arquivo `03_media_condicional.ipynb` criado com 3 opcoes de media
- [ ] Arquivo `04_variance_targeting.ipynb` criado com comparacao targeting on/off
- [ ] Arquivo `05_persistencia.ipynb` criado com metricas de persistencia
- [ ] Arquivo `06_simulacao.ipynb` criado com simulacao de paths
- [ ] Todos os notebooks com metadata kernel python3 valido

---

**End of Specification**
