# Fase 02 — Cap 01: Notebooks de Introducao

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 3 notebooks Jupyter do capitulo 01 (Introducao) que apresentam a biblioteca ao usuario pela primeira vez.

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/01_introducao/`

**Arquivos a criar**:

### 01_quickstart.ipynb

Notebook introdutorio com o fluxo minimo:
- Celula Markdown: titulo "Quickstart — Primeiro modelo com archbox", explicacao do que sera feito
- Import: `from archbox import GARCH` e `from archbox.datasets import load_dataset`
- Carregar dados: `data = load_dataset('sp500')` e explorar com `.head()`, `.describe()`, plot dos retornos
- Ajustar modelo: `model = GARCH(data['returns'].values)` e `result = model.fit()`
- Resultados: `result.summary()` — explicar cada parametro (omega, alpha, beta)
- Visualizacao: `result.plot()` — volatilidade condicional
- Metricas: `result.persistence()`, `result.half_life()`, `result.unconditional_variance()`
- Celula final: resumo do que foi aprendido
- Texto em portugues, codigo em ingles

### 02_datasets.ipynb

Exploracao de todos os datasets built-in:
- Celula Markdown: titulo "Datasets Built-in do archbox"
- Import: `from archbox.datasets import load_dataset, list_datasets`
- Listar: `list_datasets()` — mostrar todos os 11 disponiveis
- Para cada grupo de datasets:
  - **Financeiros** (sp500, ftse100, bitcoin, ibovespa, usdbrl): carregar, mostrar shape, estatisticas descritivas, plot
  - **Multivariados** (fx_majors, sector_indices): carregar, mostrar colunas, correlacao, plot conjunto
  - **Realized Volatility** (realized_vol): carregar, mostrar componentes (daily, weekly, monthly)
  - **Macroeconomicos** (us_gdp, us_unemployment, industrial_production): carregar, plot temporal
- Texto em portugues explicando cada dataset e seu uso tipico

### 03_configuracao.ipynb

Configuracao global da biblioteca:
- Celula Markdown: titulo "Configuracao do archbox"
- Import: `from archbox.core.config import ArchBoxConfig`
- Mostrar configuracao default
- Alterar optimizer, maxiter, tolerance
- Demonstrar efeito de `disp=True` vs `disp=False` no fit
- Demonstrar `variance_targeting=True`
- Texto em portugues

---

## Instrucoes

1. Crie cada notebook como arquivo `.ipynb` valido (formato JSON do Jupyter)
2. Cada notebook deve ter celulas alternando Markdown (explicacao) e Code (execucao)
3. Celulas de codigo devem ter `outputs: []` (serao preenchidos na execucao)
4. Use kernel `python3` no metadata
5. Texto explicativo em portugues, codigo e nomes de funcoes em ingles

---

## Criterios de Aceite

- [ ] Arquivo `01_quickstart.ipynb` criado com celulas Markdown + Code alternadas
- [ ] Arquivo `02_datasets.ipynb` criado cobrindo todos os 11 datasets
- [ ] Arquivo `03_configuracao.ipynb` criado com exemplos de ArchBoxConfig
- [ ] Todos os notebooks com metadata kernel python3 valido
- [ ] Todos os notebooks com texto explicativo em portugues

---

**End of Specification**
