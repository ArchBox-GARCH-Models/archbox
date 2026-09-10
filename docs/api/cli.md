---
title: CLI API
description: Interface de linha de comando da archbox - estimate, risk, backtest, regime
---

# CLI API

!!! info "Instalacao"
    ```bash
    pip install garchbox
    ```
    A distribuicao no PyPI chama-se `garchbox` (o pacote Python importado e
    `archbox`). O executavel `archbox` fica disponivel automaticamente apos a
    instalacao.

## Visao Geral

A archbox inclui uma interface de linha de comando (CLI) para operacoes
comuns sem necessidade de escrever codigo Python:

| Comando | Descricao |
|---------|-----------|
| `archbox estimate` | Ajustar modelo GARCH/EGARCH/GJR/etc |
| `archbox risk` | Calcular VaR e Expected Shortfall |
| `archbox backtest` | Backtesting de VaR (Kupiec, Christoffersen) |
| `archbox regime` | Ajustar modelo regime-switching |

Todos os comandos leem dados de um arquivo CSV e gravam os resultados em JSON.

!!! warning "`--model` e `--data` sao obrigatorios"
    Em **todos** os quatro subcomandos, `--model` e `--data` sao argumentos
    obrigatorios: nao ha modelo default. Omitir qualquer um dos dois faz o
    `argparse` encerrar com erro.

---

## Uso Geral

```bash
archbox <comando> [opcoes]
```

```bash
# Versao
archbox --version

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

Ajusta um modelo de volatilidade condicional e grava os resultados.

### Sintaxe

```bash
archbox estimate --model <modelo> --data <arquivo.csv> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--model` | `str` | **obrigatorio** | Tipo de modelo |
| `--data` | `str` | **obrigatorio** | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna de retornos |
| `--p` | `int` | `1` | Ordem GARCH ($p$) |
| `--q` | `int` | `1` | Ordem ARCH ($q$) |
| `--dist` | `str` | `"normal"` | Distribuicao condicional |
| `--mean` | `str` | `"constant"` | Especificacao da media (`constant` ou `zero`) |
| `--variance-targeting` | flag | desligado | Fixa $\omega$ pela variancia amostral |
| `--output` | `str` | `"results.json"` | Arquivo JSON de saida |

### Modelos Disponiveis

| Valor `--model` | Classe Python | Descricao |
|-----------------|---------------|-----------|
| `garch` | `GARCH` | GARCH(p,q) padrao |
| `egarch` | `EGARCH` | EGARCH exponencial |
| `gjr` | `GJRGARCH` | GJR-GARCH assimetrico |
| `aparch` | `APARCH` | Asymmetric Power ARCH |
| `figarch` | `FIGARCH` | GARCH fracionario |
| `igarch` | `IGARCH` | GARCH integrado |
| `garch-m` | `GARCHM` | GARCH-in-Mean |
| `component` | `ComponentGARCH` | Component GARCH |
| `har-rv` | `HARRV` | HAR-RV (volatilidade realizada) |

### Distribuicoes

| Valor `--dist` | Descricao |
|----------------|-----------|
| `normal` | Normal padrao |
| `student-t` | Student-$t$ |
| `skewed-t` | Skewed Student-$t$ |
| `ged` | Generalized Error Distribution |

!!! note "`skewed-t`, nao `skew-t`"
    O valor aceito e `skewed-t`. Qualquer outra grafia e rejeitada pelo
    `argparse` com a lista de escolhas validas.

### Exemplos

```bash
# GARCH(1,1) basico
archbox estimate --model garch --data retornos.csv --p 1 --q 1

# EGARCH com distribuicao Student-t
archbox estimate --model egarch --data retornos.csv --dist student-t

# GJR-GARCH(2,1) salvando resultado
archbox estimate --model gjr --data retornos.csv --p 2 --q 1 \
    --output resultado.json

# Media zero + variance targeting
archbox estimate --model garch --data retornos.csv \
    --mean zero --variance-targeting

# Especificar a coluna de retornos
archbox estimate --model garch --data dados.csv --column log_returns
```

### Output JSON

```json
{
    "model": "garch",
    "p": 1,
    "q": 1,
    "distribution": "normal",
    "nobs": 2500,
    "parameters": {
        "omega": 1.29e-06,
        "alpha[1]": 0.0773,
        "beta[1]": 0.9155
    },
    "loglikelihood": 3456.78,
    "aic": -6905.56,
    "bic": -6882.27,
    "persistence": 0.9928
}
```

As chaves de `parameters` sao `results.param_names`; distribuicoes nao-normais
acrescentam seus proprios parametros ao final (por exemplo `nu` para Student-$t$,
`nu` e `lambda` para skewed-$t$).

---

## archbox risk

::: archbox.cli.risk.run_risk
    options:
      show_root_heading: true
      show_source: true

Calcula Value-at-Risk e Expected Shortfall.

### Sintaxe

```bash
archbox risk --model <modelo> --data <arquivo.csv> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--model` | `str` | **obrigatorio** | Modelo de volatilidade |
| `--data` | `str` | **obrigatorio** | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna de retornos |
| `--p` | `int` | `1` | Ordem GARCH ($p$) |
| `--q` | `int` | `1` | Ordem ARCH ($q$) |
| `--dist` | `str` | `"normal"` | Distribuicao condicional |
| `--var-method` | `str` | `"parametric"` | Metodo de calculo do VaR |
| `--alpha` | `float` | `0.05` | Nivel de significancia |
| `--output` | `str` | `"risk.json"` | Arquivo JSON de saida |

!!! warning "A flag chama-se `--var-method`"
    Nao existe `--method` neste subcomando.

`--model` aceita os mesmos valores de `estimate`, **exceto `har-rv`**:
`garch`, `egarch`, `gjr`, `aparch`, `figarch`, `igarch`, `garch-m`, `component`.

### Metodos de VaR

| Valor `--var-method` | Descricao |
|----------------------|-----------|
| `parametric` | VaR parametrico (distribuicao assumida) |
| `historical` | Simulacao historica |
| `filtered-hs` | Simulacao historica filtrada (FHS) |
| `monte-carlo` | Simulacao Monte Carlo |

### Exemplos

```bash
# VaR parametrico 95%
archbox risk --model garch --data retornos.csv --alpha 0.05 --var-method parametric

# VaR 99% com simulacao historica filtrada
archbox risk --model garch --data retornos.csv --alpha 0.01 --var-method filtered-hs

# VaR Monte Carlo com distribuicao Student-t
archbox risk --model garch --data retornos.csv --var-method monte-carlo --dist student-t

# Salvar resultado
archbox risk --model egarch --data retornos.csv --output risco.json
```

### Output JSON

```json
{
    "model": "garch",
    "method": "parametric",
    "alpha": 0.05,
    "nobs": 2500,
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
archbox backtest --model <modelo> --data <arquivo.csv> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--model` | `str` | **obrigatorio** | Modelo de volatilidade |
| `--data` | `str` | **obrigatorio** | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna de retornos |
| `--p` | `int` | `1` | Ordem GARCH ($p$) |
| `--q` | `int` | `1` | Ordem ARCH ($q$) |
| `--dist` | `str` | `"normal"` | Distribuicao condicional |
| `--alpha` | `float` | `0.05` | Nivel de significancia |
| `--window` | `int` | `250` | Tamanho da janela rolante |
| `--output` | `str` | `"backtest.json"` | Arquivo JSON de saida |

!!! note "Sem `--method` aqui"
    O subcomando `backtest` nao aceita metodo de VaR; ele usa o modelo ajustado
    e a janela definida por `--window`.

### Exemplos

```bash
# Backtest basico
archbox backtest --model garch --data retornos.csv

# Backtest com VaR 99%
archbox backtest --model garch --data retornos.csv --alpha 0.01

# Backtest com EGARCH e janela de 500 observacoes
archbox backtest --model egarch --data retornos.csv --window 500

# Salvar resultado
archbox backtest --model garch --data retornos.csv --output backtest.json
```

### Output JSON

```json
{
    "model": "garch",
    "alpha": 0.05,
    "window": 250,
    "violations": 12,
    "expected_violations": 12.5,
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
archbox regime --model <modelo> --data <arquivo.csv> [opcoes]
```

### Opcoes

| Flag | Tipo | Default | Descricao |
|------|------|---------|-----------|
| `--model` | `str` | **obrigatorio** | Tipo de modelo regime-switching |
| `--data` | `str` | **obrigatorio** | Caminho do arquivo CSV |
| `--column` | `str` | `"returns"` | Nome da coluna |
| `--k-regimes` | `int` | `2` | Numero de regimes |
| `--order` | `int` | `1` | Ordem AR |
| `--method` | `str` | `"em"` | Estimacao: `em` ou `mle` |
| `--output` | `str` | `"regime.json"` | Arquivo JSON de saida |

!!! warning "`--k-regimes` e `--order`"
    Nao existem `--n-regimes` nem `--ar-order`.

### Modelos Disponiveis

| Valor `--model` | Classe Python | Descricao |
|-----------------|---------------|-----------|
| `ms-mean` | `MarkovSwitchingMean` | Markov-Switching na media |
| `ms-ar` | `MarkovSwitchingAR` | Markov-Switching AR |
| `ms-var` | `MarkovSwitchingVAR` | Markov-Switching VAR |
| `ms-garch` | `MarkovSwitchingGARCH` | Markov-Switching GARCH |

### Exemplos

```bash
# MS-Mean com 2 regimes
archbox regime --model ms-mean --data pib.csv --k-regimes 2

# MS-AR(2) com 3 regimes
archbox regime --model ms-ar --data desemprego.csv --order 2 --k-regimes 3

# MS-GARCH estimado por MLE
archbox regime --model ms-garch --data retornos.csv --method mle --output regime.json
```

### Output JSON

```json
{
    "model": "ms-mean",
    "k_regimes": 2,
    "order": 1,
    "method": "em",
    "nobs": 250,
    "loglikelihood": -456.78,
    "aic": 925.56,
    "bic": 948.12,
    "transition_matrix": [
        [0.975, 0.025],
        [0.035, 0.965]
    ],
    "regime_params": {
        "mu_0": 0.015,
        "mu_1": -0.005
    }
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
archbox estimate --model egarch --data retornos.csv --output modelo.json

# 2. Calcular risco
archbox risk --model egarch --data retornos.csv --alpha 0.01 --output risco.json

# 3. Backtesting
archbox backtest --model egarch --data retornos.csv --alpha 0.01 --output bt.json

# 4. Regime-switching
archbox regime --model ms-garch --data retornos.csv --output regime.json
```

!!! tip "Integracao com scripts"
    Os outputs JSON facilitam integracao com pipelines de dados:
    ```bash
    # Processar com jq
    archbox estimate --model garch --data ret.csv --output ret.json
    jq '.persistence' ret.json

    # Loop sobre modelos
    for model in garch egarch gjr; do
        archbox estimate --model "$model" --data ret.csv --output "${model}.json"
    done
    ```

---

## Ver Tambem

- [Core](core.md) -- Classes base utilizadas internamente
- [GARCH](garch.md) -- Documentacao detalhada dos modelos
- [Risk](risk.md) -- VaR e ES com mais opcoes via Python
- [Experiment](experiment.md) -- Workflow completo via Python
- [Datasets](datasets.md) -- Dados para teste
