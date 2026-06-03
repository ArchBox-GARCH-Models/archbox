---
title: CLI API
description: Interface de linha de comando da archbox - estimate, risk, backtest, regime
---

# CLI API

!!! info "Instalacao"
    ```bash
    pip install archbox
    ```
    A CLI fica disponivel automaticamente apos a instalacao.

## Visao Geral

A archbox inclui uma interface de linha de comando (CLI) para operacoes
comuns sem necessidade de escrever codigo Python:

| Comando | Descricao |
|---------|-----------|
| `archbox estimate` | Ajustar modelo GARCH/EGARCH/GJR/etc |
| `archbox risk` | Calcular VaR e Expected Shortfall |
| `archbox backtest` | Backtesting de VaR (Kupiec, Christoffersen) |
| `archbox regime` | Ajustar modelo regime-switching |

Todos os comandos aceitam dados via arquivo CSV e retornam resultados
em formato JSON.

---

## Uso Geral

```bash
archbox <comando> [opcoes]
```

```bash
# Ajuda geral
archbox --help

# Ajuda de um comando
archbox estimate --help
```

---

## archbox estimate

::: archbox.cli.estimate.run_estimate
    options:
      show_root_heading: true
      show_source: true

Ajusta um modelo de volatilidade condicional e exibe os resultados.

### Sintaxe

```bash
archbox estimate --data <arquivo.csv> --model <modelo> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--data` | `str` | -- | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna de retornos |
| `--model` | `str` | `"garch"` | Tipo de modelo |
| `--p` | `int` | `1` | Ordem ARCH ($p$) |
| `--q` | `int` | `1` | Ordem GARCH ($q$) |
| `--dist` | `str` | `"normal"` | Distribuicao condicional |
| `--mean` | `str` | `"constant"` | Especificacao da media |
| `--output` | `str` | `None` | Arquivo JSON de saida |

### Modelos Disponiveis

| Valor `--model` | Classe | Descricao |
|-----------------|--------|-----------|
| `garch` | `GARCH` | GARCH(p,q) padrao |
| `egarch` | `EGARCH` | EGARCH exponencial |
| `gjr` | `GJR_GARCH` | GJR-GARCH assimetrico |
| `aparch` | `APARCH` | Asymmetric Power ARCH |
| `figarch` | `FIGARCH` | GARCH fracionario |
| `igarch` | `IGARCH` | GARCH integrado |
| `garch-m` | `GARCH_M` | GARCH-in-Mean |
| `component` | `ComponentGARCH` | GARCH de componente |
| `har-rv` | `HAR_RV` | HAR-RV (volatilidade realizada) |

### Distribuicoes

| Valor `--dist` | Descricao |
|----------------|-----------|
| `normal` | Normal padrao |
| `student-t` | Student-$t$ |
| `skew-t` | Skewed Student-$t$ |
| `ged` | Generalized Error Distribution |

### Exemplos

```bash
# GARCH(1,1) basico
archbox estimate --data retornos.csv --model garch --p 1 --q 1

# EGARCH com distribuicao Student-t
archbox estimate --data retornos.csv --model egarch --dist student-t

# GJR-GARCH(2,1) salvando resultado
archbox estimate --data retornos.csv --model gjr --p 2 --q 1 \
    --output resultado.json

# Especificar coluna
archbox estimate --data dados.csv --column log_returns --model garch
```

### Output JSON

```json
{
    "model": "GARCH(1,1)",
    "distribution": "normal",
    "params": {
        "omega": 1.23e-06,
        "alpha": 0.085,
        "beta": 0.905
    },
    "loglikelihood": 3456.78,
    "aic": -6907.56,
    "bic": -6891.23,
    "persistence": 0.990,
    "convergence": true
}
```

---

## archbox risk

::: archbox.cli.risk.run_risk
    options:
      show_root_heading: true
      show_source: true

Calcula Value-at-Risk e Expected Shortfall.

### Sintaxe

```bash
archbox risk --data <arquivo.csv> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--data` | `str` | -- | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna de retornos |
| `--model` | `str` | `"garch"` | Modelo de volatilidade |
| `--method` | `str` | `"parametric"` | Metodo de calculo do VaR |
| `--alpha` | `float` | `0.05` | Nivel de significancia |
| `--dist` | `str` | `"normal"` | Distribuicao condicional |
| `--output` | `str` | `None` | Arquivo JSON de saida |

### Metodos de VaR

| Valor `--method` | Descricao |
|------------------|-----------|
| `parametric` | VaR parametrico (distribuicao assumida) |
| `historical` | Simulacao historica |
| `filtered-hs` | Simulacao historica filtrada (FHS) |
| `monte-carlo` | Simulacao Monte Carlo |

### Exemplos

```bash
# VaR parametrico 95%
archbox risk --data retornos.csv --alpha 0.05 --method parametric

# VaR 99% com simulacao historica filtrada
archbox risk --data retornos.csv --alpha 0.01 --method filtered-hs

# VaR Monte Carlo com distribuicao Student-t
archbox risk --data retornos.csv --method monte-carlo --dist student-t

# Salvar resultado
archbox risk --data retornos.csv --output risco.json
```

### Output JSON

```json
{
    "method": "parametric",
    "alpha": 0.05,
    "distribution": "normal",
    "var_last": -0.0156,
    "es_last": -0.0195,
    "var_mean": -0.0142,
    "es_mean": -0.0178,
    "var_min": -0.0312,
    "var_max": -0.0087
}
```

---

## archbox backtest

::: archbox.cli.backtest.run_backtest
    options:
      show_root_heading: true
      show_source: true

Backtesting de VaR com testes de Kupiec e Christoffersen.

### Sintaxe

```bash
archbox backtest --data <arquivo.csv> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--data` | `str` | -- | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna de retornos |
| `--model` | `str` | `"garch"` | Modelo de volatilidade |
| `--method` | `str` | `"parametric"` | Metodo de VaR |
| `--alpha` | `float` | `0.05` | Nivel de significancia |
| `--output` | `str` | `None` | Arquivo JSON de saida |

### Exemplos

```bash
# Backtest basico
archbox backtest --data retornos.csv

# Backtest com VaR 99%
archbox backtest --data retornos.csv --alpha 0.01

# Backtest com EGARCH + FHS
archbox backtest --data retornos.csv --model egarch --method filtered-hs

# Salvar resultado
archbox backtest --data retornos.csv --output backtest.json
```

### Output JSON

```json
{
    "model": "GARCH(1,1)",
    "method": "parametric",
    "alpha": 0.05,
    "n_observations": 1000,
    "n_violations": 48,
    "expected_violations": 50,
    "violation_ratio": 0.96,
    "kupiec": {
        "statistic": 0.082,
        "pvalue": 0.775,
        "reject": false
    },
    "christoffersen": {
        "statistic": 1.234,
        "pvalue": 0.267,
        "reject": false
    },
    "traffic_light": "green"
}
```

!!! tip "Interpretacao do Backtest"
    - **Kupiec**: testa se a frequencia de violacoes e consistente com $\alpha$
    - **Christoffersen**: testa se as violacoes sao independentes
    - **Traffic light**: semaforo de Basileia III (verde/amarelo/vermelho)

---

## archbox regime

::: archbox.cli.regime.run_regime
    options:
      show_root_heading: true
      show_source: true

Ajusta modelo de regime-switching.

### Sintaxe

```bash
archbox regime --data <arquivo.csv> --model <modelo> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--data` | `str` | -- | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna |
| `--model` | `str` | `"ms-mean"` | Tipo de modelo regime-switching |
| `--n-regimes` | `int` | `2` | Numero de regimes |
| `--ar-order` | `int` | `1` | Ordem AR (para MS-AR) |
| `--output` | `str` | `None` | Arquivo JSON de saida |

### Modelos Disponiveis

| Valor `--model` | Descricao |
|-----------------|-----------|
| `ms-mean` | Markov-Switching na media |
| `ms-ar` | Markov-Switching AR |
| `ms-var` | Markov-Switching na variancia |
| `ms-garch` | Markov-Switching GARCH |

### Exemplos

```bash
# MS-Mean com 2 regimes
archbox regime --data pib.csv --model ms-mean --n-regimes 2

# MS-AR(2) com 3 regimes
archbox regime --data desemprego.csv --model ms-ar --ar-order 2 --n-regimes 3

# MS-GARCH
archbox regime --data retornos.csv --model ms-garch --output regime.json
```

### Output JSON

```json
{
    "model": "MS-Mean(2)",
    "n_regimes": 2,
    "transition_matrix": [
        [0.975, 0.025],
        [0.035, 0.965]
    ],
    "regime_params": {
        "regime_0": {"mu": 0.015, "sigma": 0.008},
        "regime_1": {"mu": -0.005, "sigma": 0.022}
    },
    "loglikelihood": -456.78,
    "aic": 925.56,
    "bic": 948.12
}
```

---

## Formato de Dados

A CLI espera arquivos CSV com uma coluna de retornos:

```csv
date,returns
2020-01-02,0.0032
2020-01-03,-0.0015
2020-01-06,0.0028
...
```

!!! warning "Formato"
    - O CSV deve ter header
    - Use `--column` para especificar a coluna de retornos se nao for `"returns"`
    - Retornos devem ser em decimal (0.01 = 1%), nao em porcentagem

---

## Pipeline no Terminal

```bash
# 1. Ajustar modelo
archbox estimate --data retornos.csv --model egarch --output modelo.json

# 2. Calcular risco
archbox risk --data retornos.csv --model egarch --alpha 0.01 --output risco.json

# 3. Backtesting
archbox backtest --data retornos.csv --model egarch --alpha 0.01 --output bt.json

# 4. Regime-switching
archbox regime --data retornos.csv --model ms-garch --output regime.json
```

!!! tip "Integracao com scripts"
    Os outputs JSON facilitam integracao com pipelines de dados:
    ```bash
    # Processar com jq
    archbox estimate --data ret.csv --model garch | jq '.persistence'

    # Loop sobre modelos
    for model in garch egarch gjr; do
        archbox estimate --data ret.csv --model $model --output ${model}.json
    done
    ```

---

## Ver Tambem

- [Core](core.md) -- Classes base utilizadas internamente
- [GARCH](garch.md) -- Documentacao detalhada dos modelos
- [Risk](risk.md) -- VaR e ES com mais opcoes via Python
- [Experiment](experiment.md) -- Workflow completo via Python
- [Datasets](datasets.md) -- Dados para teste
