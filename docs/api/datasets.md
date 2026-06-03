---
title: Datasets API
description: Datasets sinteticos incluidos na archbox para exemplos e testes
---

# Datasets API

!!! info "Modulo"
    ```python
    from archbox.datasets import load_dataset, list_datasets
    ```

## Visao Geral

O modulo `archbox.datasets` fornece datasets sinteticos com propriedades
realistas de series financeiras (clusters de volatilidade, caudas pesadas,
regime-switching). Sao uteis para exemplos, tutoriais e testes.

```python
from archbox.datasets import list_datasets

print(list_datasets())
# ['bitcoin', 'ftse100', 'fx_majors', 'ibovespa', 'industrial_production',
#  'realized_vol', 'sector_indices', 'sp500', 'us_gdp',
#  'us_unemployment', 'usdbrl']
```

---

## Funcoes

### load_dataset()

::: archbox.datasets.load.load_dataset
    options:
      show_root_heading: true
      show_source: true

Carrega um dataset built-in pelo nome.

```python
load_dataset(name) -> pd.DataFrame
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `name` | `str` | -- | Nome do dataset (ver tabela abaixo) |

**Retorna**: `pd.DataFrame` com os dados do dataset.

**Levanta**: `ValueError` se o nome nao for encontrado.

### list_datasets()

::: archbox.datasets.load.list_datasets
    options:
      show_root_heading: true
      show_source: true

Lista todos os datasets disponiveis.

```python
list_datasets() -> list[str]
```

### Exemplo

```python
from archbox.datasets import load_dataset, list_datasets

# Ver datasets disponiveis
print(list_datasets())

# Carregar S&P 500
data = load_dataset("sp500")
print(data.head())
print(f"Shape: {data.shape}")
print(f"Colunas: {data.columns.tolist()}")
```

---

## Datasets Disponiveis

### Univariados - Acoes e Indices

#### sp500

Dataset do indice S&P 500 com retornos diarios simulados via GARCH(1,1).

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2500 |
| **Frequencia** | Diaria |
| **Colunas** | `returns` |
| **Caracteristicas** | Clusters de volatilidade, assimetria moderada |
| **Uso recomendado** | Modelos GARCH univariados, VaR |

```python
data = load_dataset("sp500")
returns = data["returns"].values
```

#### ftse100

Dataset do indice FTSE 100 com propriedades de mercado europeu.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2500 |
| **Frequencia** | Diaria |
| **Colunas** | `returns` |
| **Caracteristicas** | Volatilidade moderada, clusters persistentes |
| **Uso recomendado** | GARCH, EGARCH, comparacao de modelos |

```python
data = load_dataset("ftse100")
```

#### ibovespa

Dataset do indice Ibovespa (mercado brasileiro).

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2500 |
| **Frequencia** | Diaria |
| **Colunas** | `returns` |
| **Caracteristicas** | Alta volatilidade, caudas pesadas, efeito leverage |
| **Uso recomendado** | EGARCH, GJR-GARCH, analise de risco |

```python
data = load_dataset("ibovespa")
```

---

### Univariados - Criptomoedas e Cambio

#### bitcoin

Dataset de retornos de Bitcoin com caudas pesadas.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2000 |
| **Frequencia** | Diaria |
| **Colunas** | `returns` |
| **Caracteristicas** | Caudas extremamente pesadas, alta curtose, clusters de volatilidade |
| **Uso recomendado** | Distribuicoes Student-$t$, GARCH com caudas pesadas |

```python
data = load_dataset("bitcoin")
```

#### usdbrl

Dataset de taxa de cambio USD/BRL.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2500 |
| **Frequencia** | Diaria |
| **Colunas** | `returns` |
| **Caracteristicas** | Volatilidade variavel, regime-switching |
| **Uso recomendado** | GARCH, regime-switching, analise de risco cambial |

```python
data = load_dataset("usdbrl")
```

---

### Multivariados

#### fx_majors

Tres pares de moedas com correlacao dinamica.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2000 |
| **Frequencia** | Diaria |
| **Series** | 3 pares de moedas |
| **Caracteristicas** | Correlacao variante no tempo, spillover |
| **Uso recomendado** | DCC-GARCH, CCC-GARCH, BEKK |

```python
data = load_dataset("fx_majors")
```

#### sector_indices

Cinco indices setoriais correlacionados.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2000 |
| **Frequencia** | Diaria |
| **Series** | 5 setores |
| **Caracteristicas** | Correlacao heterogenea, contagio |
| **Uso recomendado** | GO-GARCH, DECO, analise de portfolio |

```python
data = load_dataset("sector_indices")
```

---

### Volatilidade Realizada

#### realized_vol

Dataset com volatilidade realizada para modelos HAR-RV.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~2000 |
| **Frequencia** | Diaria |
| **Colunas** | Volatilidade realizada e componentes |
| **Caracteristicas** | Memoria longa, componentes de frequencia |
| **Uso recomendado** | HAR-RV, FIGARCH |

```python
data = load_dataset("realized_vol")
```

---

### Macroeconomicos (Regime-Switching)

#### us_gdp

PIB dos EUA com regimes de crescimento.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~300 |
| **Frequencia** | Trimestral |
| **Colunas** | Crescimento do PIB |
| **Caracteristicas** | 2 regimes (expansao/recessao) |
| **Uso recomendado** | Markov-Switching Mean |

```python
data = load_dataset("us_gdp")
```

#### us_unemployment

Taxa de desemprego dos EUA com regime-switching.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~300 |
| **Frequencia** | Mensal |
| **Colunas** | Taxa de desemprego |
| **Caracteristicas** | Regimes de alta/baixa, transicoes abruptas |
| **Uso recomendado** | MS-AR, MS-Mean |

```python
data = load_dataset("us_unemployment")
```

#### industrial_production

Producao industrial com comportamento threshold.

| Propriedade | Valor |
|-------------|-------|
| **Observacoes** | ~300 |
| **Frequencia** | Mensal |
| **Colunas** | Crescimento da producao |
| **Caracteristicas** | Nao-linearidade SETAR, assimetria ciclica |
| **Uso recomendado** | SETAR, TAR, LSTAR |

```python
data = load_dataset("industrial_production")
```

---

## Tabela Resumo

| Dataset | Obs. | Freq. | Series | Tipo | Uso Principal |
|---------|------|-------|--------|------|---------------|
| `sp500` | ~2500 | Diaria | 1 | Retornos | GARCH, VaR |
| `ftse100` | ~2500 | Diaria | 1 | Retornos | GARCH, comparacao |
| `ibovespa` | ~2500 | Diaria | 1 | Retornos | EGARCH, GJR |
| `bitcoin` | ~2000 | Diaria | 1 | Retornos | Student-$t$, caudas |
| `usdbrl` | ~2500 | Diaria | 1 | Retornos | FX, regime-switching |
| `fx_majors` | ~2000 | Diaria | 3 | Retornos | DCC, CCC |
| `sector_indices` | ~2000 | Diaria | 5 | Retornos | GO-GARCH, portfolio |
| `realized_vol` | ~2000 | Diaria | 1+ | Vol. realizada | HAR-RV |
| `us_gdp` | ~300 | Trimestral | 1 | Crescimento | MS-Mean |
| `us_unemployment` | ~300 | Mensal | 1 | Taxa | MS-AR |
| `industrial_production` | ~300 | Mensal | 1 | Crescimento | SETAR, TAR |

---

## Exemplo Completo

```python
from archbox.datasets import load_dataset, list_datasets
from archbox.models import GARCH, EGARCH
from archbox.experiment import ArchExperiment

# Listar todos os datasets
print("Datasets disponiveis:")
for name in list_datasets():
    data = load_dataset(name)
    print(f"  {name}: {data.shape[0]} obs, {data.shape[1]} colunas")

# Workflow com dataset sp500
data = load_dataset("sp500")
returns = data["returns"].values

exp = ArchExperiment(returns)
exp.fit_all_models([
    ("GARCH", {"p": 1, "q": 1}),
    ("EGARCH", {"p": 1, "q": 1}),
], disp=False)

comp = exp.compare_models()
print(f"\nMelhor modelo para S&P 500: {comp.best_model('aic')}")

# Workflow com dataset multivariado
fx_data = load_dataset("fx_majors")
print(f"\nFX Majors: {fx_data.columns.tolist()}")
```

---

## Ver Tambem

- [Experiment](experiment.md) -- `ArchExperiment` para workflow completo
- [Core](core.md) -- Modelos que consomem os datasets
- [GARCH](garch.md) -- Modelos univariados
- [Multivariado](multivariate.md) -- Modelos multivariados para `fx_majors` e `sector_indices`
- [Regime-Switching](regime-switching.md) -- Modelos para dados macroeconomicos
