# Estratégia de Cobertura de Testes — archbox

> Snapshot gerado em 2026-03-24 com base na execução local dos testes.

---

## 1. Visão geral

| Métrica | Valor |
|---------|-------|
| **Cobertura total** | **89%** (6 685 statements, 725 sem cobertura) |
| **Threshold do CI** | 90% (`--cov-fail-under=90`) |
| **Arquivos de teste** | 86 |
| **Testes executados** | 805 passed, 55 failed, 6 skipped, 3 xfailed |
| **Frameworks** | pytest ≥ 7.0, pytest-cov ≥ 4.0, mutmut (mutation testing) |
| **Python** | 3.11, 3.12 |

---

## 2. Configuração

### 2.1 pytest (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

### 2.2 Coverage (`pyproject.toml`)

```toml
[tool.coverage.run]
source = ["archbox"]
omit = [
    "archbox/datasets/generate_datasets.py",
    "archbox/cli/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "pass",
    "@abstractmethod",
]
```

### 2.3 Mutation testing (`pyproject.toml`)

```toml
[tool.mutmut]
paths_to_mutate = "archbox/core/"
tests_dir = "tests/"
runner = "python -m pytest tests/core/ tests/estimation/ -x --tb=no -q"
```

### 2.4 CI/CD (`.github/workflows/ci.yml`)

```yaml
- name: Test
  run: pytest --cov=archbox --cov-report=xml --cov-fail-under=90

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    file: coverage.xml
```

---

## 3. Estrutura dos testes

```
tests/
├── benchmarks/         # Benchmarks de performance e scaling (3 arquivos)
├── cli/                # Testes do CLI (1 arquivo)
├── core/               # Core: results, volatility_model (2 arquivos)
├── diagnostics/        # Testes estatísticos: ARCH-LM, Ljung-Box, etc. (7 arquivos)
├── distributions/      # Distribuições: normal, student-t, GED, etc. (6 arquivos)
├── estimation/         # MLE (1 arquivo)
├── experiment/         # Experimentos e comparações (2 arquivos)
├── integration/        # Testes end-to-end por subsistema (5 arquivos)
├── models/             # Modelos univariados: GARCH, EGARCH, GJR, etc. (8 arquivos)
├── multivariate/       # Modelos multivariados: CCC, DCC, BEKK, etc. (7 arquivos)
├── property/           # Testes baseados em propriedades — hypothesis (1 arquivo)
├── regime/             # Markov-switching: MS-GARCH, MS-VAR, etc. (10 arquivos)
├── report/             # Exporters, templates, transformers (4 arquivos)
├── risk/               # VaR, ES, EWMA, backtesting (4 arquivos)
├── threshold/          # TAR, SETAR, LSTAR, ESTAR (7 arquivos)
├── utils/              # Utilitários: numba, news impact (3 arquivos)
├── validation/         # Validação cruzada com R (rugarch, rmgarch, mswm) (3 arquivos)
└── visualization/      # Plots: volatilidade, regime, risco, etc. (9 arquivos)
```

### Categorias de teste

| Categoria | Objetivo |
|-----------|----------|
| **Unitários** | Validar lógica isolada de cada componente (`core/`, `models/`, `distributions/`, etc.) |
| **Integração** | Fluxos completos end-to-end por subsistema (`integration/`) |
| **Benchmarks** | Performance e scaling (`benchmarks/`) |
| **Property-based** | Testes com geração aleatória de inputs via hypothesis (`property/`) |
| **Validação cruzada** | Comparação numérica com pacotes R: rugarch, rmgarch, mswm (`validation/`) |
| **Mutation testing** | mutmut aplicado em `archbox/core/` para garantir qualidade dos testes |

---

## 4. Cobertura por módulo

### Módulos com alta cobertura (≥ 90%)

| Módulo | Statements | Miss | Cobertura |
|--------|-----------|------|-----------|
| `core/` | 209 | 2 | **99%** |
| `distributions/` | 411 | 13 | **97%** |
| `diagnostics/` | 283 | 13 | **95%** |
| `risk/` | 284 | 9 | **97%** |
| `visualization/` | 724 | 15 | **98%** |
| `report/` | 367 | 37 | **90%** |
| `utils/` | 238 | 24 | **90%** |
| `models/` | 778 | 87 | **89%** |
| `estimation/` | 109 | 8 | **93%** |
| `threshold/` | 909 | 89 | **90%** |

### Módulos com baixa cobertura (< 90%)

| Módulo | Statements | Miss | Cobertura | Causa principal |
|--------|-----------|------|-----------|-----------------|
| `multivariate/gogarch.py` | 83 | 59 | **29%** | Testes falhando (TypeError) |
| `multivariate/results.py` | 2 | 2 | **0%** | Arquivo novo, sem testes |
| `regime/base.py` | 106 | 48 | **55%** | Classe base abstrata parcialmente testada |
| `experiment/experiment.py` | 148 | 57 | **61%** | Fluxos complexos sem cobertura |
| `multivariate/ccc.py` | 57 | 21 | **63%** | Testes falhando (TypeError) |
| `report/transformers/multivariate.py` | 47 | 17 | **64%** | Depende dos modelos multivariados |
| `experiment/comparison.py` | 35 | 12 | **66%** | Pouca cobertura de branches |
| `multivariate/deco.py` | 98 | 30 | **69%** | Testes falhando (TypeError) |
| `datasets/load.py` | 25 | 7 | **72%** | Paths alternativos não cobertos |
| `multivariate/dcc.py` | 88 | 21 | **76%** | Testes falhando (TypeError) |
| `multivariate/base.py` | 200 | 45 | **78%** | Testes dos filhos falhando |

---

## 5. Testes falhando

### Resumo: 55 falhas concentradas em 3 áreas

| Área | Falhas | Tipo de erro |
|------|--------|--------------|
| `tests/multivariate/` (CCC, DCC, DECO, GO-GARCH, portfolio) | 50 | `TypeError` — provável mudança de interface |
| `tests/benchmarks/` (DCC performance/scaling) | 3 | Dependem dos modelos multivariados |
| `tests/integration/test_dcc_full.py` | 2 | Dependem dos modelos multivariados |

Todas as 55 falhas têm a mesma causa raiz: os modelos multivariados (exceto BEKK) estão com a interface quebrada. Corrigir esse módulo elimina todas as falhas de uma vez.

---

## 6. Plano de ação para atingir ≥ 90%

### Prioridade 1 — Corrigir testes multivariados (impacto: +5-7pp)

Os 55 testes falhando nos modelos CCC, DCC, DECO e GO-GARCH representam o maior gap de cobertura. A causa raiz parece ser uma mudança de interface (`TypeError`). Corrigir esse problema deve:

- Recuperar cobertura de `multivariate/` (de ~60% para ~90%)
- Fazer os testes de integração DCC e benchmarks voltarem a passar
- Elevar a cobertura total para **~93-95%**

### Prioridade 2 — Melhorar cobertura de módulos específicos

| Módulo | Ação |
|--------|------|
| `regime/base.py` (55%) | Adicionar testes para métodos concretos da classe base |
| `experiment/experiment.py` (61%) | Cobrir fluxos de execução e edge cases |
| `experiment/comparison.py` (66%) | Adicionar testes para branches não cobertos |
| `datasets/load.py` (72%) | Testar cenários de fallback e erros de I/O |

### Prioridade 3 — Expandir mutation testing

Atualmente o mutmut cobre apenas `archbox/core/`. Expandir para:

- `archbox/estimation/`
- `archbox/distributions/`
- `archbox/risk/`

---

## 7. Comandos úteis

```bash
# Rodar todos os testes com cobertura
pytest --cov=archbox --cov-report=term-missing

# Cobertura com threshold (usado no CI)
pytest --cov=archbox --cov-report=xml --cov-fail-under=90

# Rodar apenas testes de um módulo
pytest tests/core/ -v

# Mutation testing
mutmut run

# Lint + type check
ruff check archbox/ tests/
pyright archbox/
```
