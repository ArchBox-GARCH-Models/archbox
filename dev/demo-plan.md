# Planejamento de Demonstracao — archbox

> Documento de planejamento para criacao de exemplos demonstrativos da biblioteca archbox.
> Cada capitulo aborda um tema, com notebooks Jupyter (Python), scripts R e scripts Stata.

---

## Estrutura de pastas

```
examples/
└── capitulos/
    ├── 01_introducao/
    ├── 02_garch_classico/
    ├── 03_garch_assimetricos/
    ├── 04_garch_avancados/
    ├── 05_distribuicoes/
    ├── 06_diagnosticos/
    ├── 07_previsao/
    ├── 08_risco/
    ├── 09_multivariados_intro/
    ├── 10_multivariados_avancados/
    ├── 11_regime_switching/
    ├── 12_threshold_star/
    ├── 13_portfolio/
    ├── 14_experimentos/
    ├── 15_visualizacao/
    ├── 16_relatorios/
    └── 17_validacao_cruzada/
```

---

## Capitulo 01 — Introducao

**Objetivo:** Apresentar a biblioteca, instalar, carregar dados e ajustar o primeiro modelo.

| Arquivo | Conteudo |
|---------|----------|
| `01_quickstart.ipynb` | Instalacao, import, load_dataset('sp500'), GARCH(1,1).fit(), summary(), plot |
| `02_datasets.ipynb` | Explorar todos os 11 datasets built-in: sp500, ftse100, bitcoin, ibovespa, usdbrl, fx_majors, sector_indices, realized_vol, us_gdp, us_unemployment, industrial_production |
| `03_configuracao.ipynb` | ArchBoxConfig, opcoes de otimizador, tolerancia, verbose |
| `01_quickstart.R` | Equivalente R usando rugarch: ugarchspec + ugarchfit no mesmo dataset |
| `01_quickstart.do` | Equivalente Stata usando arch command |

**Funcionalidades cobertas:**
- `GARCH`, `load_dataset`, `list_datasets`
- `ArchBoxConfig`
- `ArchResults.summary()`, `ArchResults.plot()`

---

## Capitulo 02 — GARCH Classico

**Objetivo:** Explorar o modelo GARCH(p,q) em profundidade.

| Arquivo | Conteudo |
|---------|----------|
| `01_garch_basico.ipynb` | GARCH(1,1) com diferentes series: sp500, bitcoin, usdbrl. Interpretacao de omega, alpha, beta |
| `02_ordens_pq.ipynb` | Comparacao GARCH(1,1), GARCH(1,2), GARCH(2,1), GARCH(2,2). Selecao via AIC/BIC |
| `03_media_condicional.ipynb` | Opcoes de media: mean='zero', 'constant', 'ar'. Efeito na estimacao |
| `04_variance_targeting.ipynb` | fit(variance_targeting=True) vs False. Quando usar e impacto nos parametros |
| `05_persistencia.ipynb` | persistence(), half_life(), unconditional_variance(). Interpretacao economica |
| `06_simulacao.ipynb` | simulate(n, params). Geracao de cenarios e paths de volatilidade |
| `01_garch_basico.R` | rugarch: sGARCH com ugarchspec/ugarchfit |
| `02_ordens_pq.R` | Comparacao de ordens em rugarch com infocriteria() |
| `01_garch_basico.do` | Stata: arch y, arch(1) garch(1) |
| `02_ordens_pq.do` | Stata: comparacao de ordens com estat ic |

**Funcionalidades cobertas:**
- `GARCH(endog, p, q, mean, dist)`
- `ArchResults`: params, persistence, half_life, unconditional_variance, aic, bic, hqic
- `VolatilityModel.simulate()`

---

## Capitulo 03 — GARCH Assimetricos

**Objetivo:** Modelos que capturam o efeito alavancagem (leverage effect).

| Arquivo | Conteudo |
|---------|----------|
| `01_egarch.ipynb` | EGARCH(1,1) no sp500. Parametro gamma e assimetria. Comparacao com GARCH |
| `02_gjr_garch.ipynb` | GJR-GARCH(1,1). Indicadora I(e<0) e efeito de choques negativos |
| `03_aparch.ipynb` | APARCH(1,1). Parametro de potencia delta e assimetria gamma |
| `04_comparacao_assimetricos.ipynb` | GARCH vs EGARCH vs GJR vs APARCH no mesmo dataset. News impact curves lado a lado |
| `05_news_impact.ipynb` | news_impact_curve() detalhado. Interpretacao visual do efeito alavancagem |
| `01_egarch.R` | rugarch: eGARCH com ugarchspec(variance.model=list(model="eGARCH")) |
| `02_gjr_garch.R` | rugarch: gjrGARCH |
| `03_aparch.R` | rugarch: apARCH |
| `01_egarch.do` | Stata: arch y, earch(1) egarch(1) |
| `02_gjr_garch.do` | Stata: arch y, arch(1) garch(1) tarch(1) |

**Funcionalidades cobertas:**
- `EGARCH`, `GJRGARCH`, `APARCH`
- `news_impact_curve()`, `compare_news_impact()`
- `plot_news_impact()`, `plot_news_impact_comparison()`

---

## Capitulo 04 — GARCH Avancados

**Objetivo:** Modelos especializados para fenomenos especificos.

| Arquivo | Conteudo |
|---------|----------|
| `01_igarch.ipynb` | IGARCH no bitcoin. Persistencia unitaria, variancia infinita. Comparacao com EWMA |
| `02_figarch.ipynb` | FIGARCH no sp500. Memoria longa em volatilidade. Parametro d e truncation_lag |
| `03_garch_m.ipynb` | GARCH-M com risk_premium='variance', 'volatility', 'log_variance'. Premio de risco no retorno |
| `04_component_garch.ipynb` | ComponentGARCH. Decomposicao permanente (q_t) vs transitoria (h_t). variance_decomposition() |
| `05_har_rv.ipynb` | HAR-RV com realized_vol dataset. Componentes diaria, semanal, mensal |
| `01_igarch.R` | rugarch: iGARCH |
| `02_figarch.R` | rugarch: fiGARCH |
| `03_garch_m.R` | rugarch: GARCH-in-mean |
| `01_igarch.do` | Stata: arch y, arch(1) garch(1) constraint(persistence=1) |

**Funcionalidades cobertas:**
- `IGARCH`, `FIGARCH`, `GARCHM`, `ComponentGARCH`, `HARRV`
- `ComponentGARCH.variance_decomposition()`
- `HARRVResults.summary()`, `HARRVResults.forecast()`

---

## Capitulo 05 — Distribuicoes Condicionais

**Objetivo:** Comparar distribuicoes para inovacoes e seu impacto na estimacao e risco.

| Arquivo | Conteudo |
|---------|----------|
| `01_normal_vs_t.ipynb` | GARCH(1,1) com dist='normal' vs dist='t'. QQ-plot, loglike, AIC |
| `02_ged.ipynb` | Distribuicao GED. Parametro de forma e caudas |
| `03_skewed_t.ipynb` | Skewed-t de Hansen. Assimetria e curtose. Aplicacao em mercados emergentes (ibovespa, usdbrl) |
| `04_mixture_normal.ipynb` | MixtureNormal. Peso da mistura e razao de volatilidade. Bimodalidade |
| `05_comparacao_completa.ipynb` | Todas as 5 distribuicoes no mesmo dataset. Tabela comparativa AIC/BIC. Selecao de distribuicao |
| `01_distribuicoes.R` | rugarch: distribution.model = "norm", "std", "ged", "sstd" |
| `01_distribuicoes.do` | Stata: arch y, arch(1) garch(1) distribution(t) |

**Funcionalidades cobertas:**
- Distribuicoes: `Normal`, `StudentT`, `GeneralizedError`, `SkewedT`, `MixtureNormal`
- Metodos: `loglikelihood()`, `ppf()`, `cdf()`, `simulate()`
- `plot_distribution_fit()`

---

## Capitulo 06 — Diagnosticos

**Objetivo:** Validar a adequacao do modelo ajustado.

| Arquivo | Conteudo |
|---------|----------|
| `01_arch_lm.ipynb` | arch_lm_test() antes e depois do ajuste. Verificar se ARCH effects foram capturados |
| `02_ljung_box.ipynb` | ljung_box_squared() nos residuos padronizados. Autocorrelacao residual |
| `03_sign_bias.ipynb` | sign_bias_test(). Detectar assimetria nao capturada pelo modelo |
| `04_nyblom.ipynb` | nyblom_test(). Estabilidade dos parametros ao longo do tempo |
| `05_diagnostico_completo.ipynb` | full_diagnostics(results). Relatorio PASS/FAIL completo. Fluxo de decisao: modelo inadequado → proximo passo |
| `06_engle_sheppard.ipynb` | engle_sheppard_test() para residuos multivariados |
| `07_hong_spillover.ipynb` | hong_spillover_test() entre pares de series |
| `08_workflow_diagnostico.ipynb` | Workflow completo: ajustar → diagnosticar → reajustar. Exemplo pratico de iteracao |
| `01_diagnosticos.R` | rugarch: nyblom(), signbias(), gof() |
| `01_diagnosticos.do` | Stata: estat archlm, estat bgodfrey |

**Funcionalidades cobertas:**
- `arch_lm_test()`, `ljung_box_squared()`, `sign_bias_test()`, `nyblom_test()`
- `engle_sheppard_test()`, `hong_spillover_test()`
- `full_diagnostics()`, `DiagnosticReport.summary()`
- `plot_diagnostics()`

---

## Capitulo 07 — Previsao

**Objetivo:** Previsao de volatilidade multi-passos e avaliacao out-of-sample.

| Arquivo | Conteudo |
|---------|----------|
| `01_previsao_analitica.ipynb` | forecast(horizon, method='analytic'). 1, 5, 22 passos a frente |
| `02_previsao_simulacao.ipynb` | forecast(method='simulation'). Fan charts e intervalos de confianca |
| `03_rolling_window.ipynb` | Rolling window forecast. Expanding vs fixed window. MAE, RMSE, QLIKE |
| `04_comparacao_modelos.ipynb` | Forecast de GARCH vs EGARCH vs GJR. Diebold-Mariano implícito via metricas |
| `01_previsao.R` | rugarch: ugarchforecast, ugarchroll |
| `01_previsao.do` | Stata: arch y, arch(1) garch(1) ; predict sigma2, variance |

**Funcionalidades cobertas:**
- `ArchResults.forecast(horizon, method)`
- `ArchResults.conditional_volatility`
- Out-of-sample via `ArchExperiment.validate_out_of_sample()`

---

## Capitulo 08 — Risco (VaR e ES)

**Objetivo:** Medicao e backtesting de risco de mercado.

| Arquivo | Conteudo |
|---------|----------|
| `01_var_parametrico.ipynb` | ValueAtRisk.parametric() com dist='normal' e 't'. VaR 1% e 5% |
| `02_var_historico.ipynb` | VaR historico simples e filtered historical simulation |
| `03_var_montecarlo.ipynb` | VaR via Monte Carlo. Numero de simulacoes e convergencia |
| `04_expected_shortfall.ipynb` | ExpectedShortfall: parametric, historical, filtered, cornish_fisher |
| `05_ewma_riskmetrics.ipynb` | EWMA(lambda=0.94). Comparacao com GARCH. RiskMetrics approach |
| `06_backtesting.ipynb` | VaRBacktest: kupiec_pof(), christoffersen(), basel_traffic_light(). Relatorio completo |
| `07_comparacao_metodos.ipynb` | VaR parametrico vs historico vs FHS vs MC. Backtest de todos. Qual performa melhor? |
| `08_workflow_risco.ipynb` | Pipeline completo: dados → modelo → VaR/ES → backtest → relatorio. Caso de uso real |
| `01_var.R` | rugarch: quantile(ugarchforecast), VaRTest() |
| `01_var.do` | Stata: var e backtesting manual |

**Funcionalidades cobertas:**
- `ValueAtRisk`: parametric, historical, filtered_historical, montecarlo
- `ExpectedShortfall`: parametric, historical, filtered_historical, cornish_fisher
- `EWMA(returns, lam)`
- `VaRBacktest`: kupiec_pof, christoffersen, basel_traffic_light, summary
- `plot_var_backtest()`, `plot_traffic_light()`, `plot_var_comparison()`

---

## Capitulo 09 — Multivariados: Introducao

**Objetivo:** Introducao a modelos multivariados de volatilidade.

| Arquivo | Conteudo |
|---------|----------|
| `01_ccc_garch.ipynb` | CCC-GARCH com fx_majors. Correlacao constante. Interpretacao da matriz R |
| `02_dcc_garch.ipynb` | DCC-GARCH. Correlacao dinamica. Parametros a, b. Comparacao com CCC |
| `03_bekk_garch.ipynb` | BEKK diagonal e full. Garantia de positividade. Curse of dimensionality |
| `04_ccc_vs_dcc.ipynb` | Comparacao CCC vs DCC: loglike, AIC, correlacao ao longo do tempo |
| `01_ccc.R` | rmgarch: dccspec(dccOrder=c(0,0)) para CCC, dccfit |
| `02_dcc.R` | rmgarch: dccspec(dccOrder=c(1,1)), dccfit |
| `01_dcc.do` | Stata: mgarch dcc |

**Funcionalidades cobertas:**
- `CCC`, `DCC`, `BEKK`
- `MultivariateVolatilityModel.fit()`
- `plot_dynamic_correlation()`, `plot_correlation_heatmap()`

---

## Capitulo 10 — Multivariados: Avancados

**Objetivo:** Modelos avancados e escalabilidade.

| Arquivo | Conteudo |
|---------|----------|
| `01_deco.ipynb` | DECO com sector_indices (5 series). Equicorrelacao escalar. Escalabilidade |
| `02_gogarch.ipynb` | GO-GARCH com fx_majors. ICA, fatores independentes, mixing matrix |
| `03_escalabilidade.ipynb` | Comparacao de tempo: CCC vs DCC vs BEKK vs DECO vs GO-GARCH para k=2,3,5,10 |
| `04_covariance_decomp.ipynb` | plot_covariance_decomposition(). Entender fontes de covariancia |
| `01_gogarch.R` | rmgarch: gogarchspec, gogarchfit |
| `02_deco.R` | rmgarch: dccspec com type="DECO" |

**Funcionalidades cobertas:**
- `DECO`, `GOGARCH`
- `plot_covariance_decomposition()`

---

## Capitulo 11 — Regime-Switching

**Objetivo:** Modelos Markov-Switching para mudancas estruturais.

| Arquivo | Conteudo |
|---------|----------|
| `01_ms_mean.ipynb` | MarkovSwitchingMean com us_gdp. 2 regimes: expansao vs recessao |
| `02_ms_meanvar.ipynb` | MarkovSwitchingMeanVar. Media e variancia mudam. Identificacao de crises |
| `03_ms_ar.ipynb` | MarkovSwitchingAR(order=4) com us_gdp. Hamilton (1989) replication |
| `04_ms_garch.ipynb` | MarkovSwitchingGARCH com sp500. Regimes de alta e baixa volatilidade |
| `05_ms_var.ipynb` | MarkovSwitchingVAR multivariado. Spillovers entre regimes |
| `06_hamilton_filter.ipynb` | HamiltonFilter detalhado. Probabilidades filtradas vs suavizadas. Kim smoother |
| `07_em_algorithm.ipynb` | EMEstimator passo a passo. Convergencia e inicializacao |
| `08_n_regimes.ipynb` | Comparacao 2 vs 3 regimes. Selecao via AIC/BIC. Cuidados |
| `09_transicao.ipynb` | Matriz de transicao. Duracao esperada de cada regime. Probabilidades ergoticas |
| `01_ms_mean.R` | MSwM: msmFit() |
| `02_ms_ar.R` | MSwM: msmFit com modelo AR |
| `01_ms_mean.do` | Stata: mswitch dr y, states(2) |

**Funcionalidades cobertas:**
- `MarkovSwitchingMean`, `MarkovSwitchingMeanVar`, `MarkovSwitchingAR`
- `MarkovSwitchingGARCH`, `MarkovSwitchingVAR`
- `HamiltonFilter.filter()`, `HamiltonFilter.ergodic_probabilities()`
- `KimSmoother.smooth()`
- `EMEstimator.fit()`
- `RegimeResults`: filtered_probs, smoothed_probs, regime_path, transition_matrix
- `plot_regimes()`, `plot_transition_matrix()`

---

## Capitulo 12 — Modelos Threshold e STAR

**Objetivo:** Modelos nao-lineares com transicao de regime baseada em threshold.

| Arquivo | Conteudo |
|---------|----------|
| `01_testes_linearidade.ipynb` | linearity_test(), tsay_test(), hansen_threshold_test(). Detectar nao-linearidade |
| `02_transition_type.ipynb` | transition_type_test(). LSTAR vs ESTAR: como escolher |
| `03_tar.ipynb` | TAR com us_unemployment. Threshold exogeno e grid search |
| `04_setar.ipynb` | SETAR com industrial_production. Auto-selecao de delay. 2 e 3 regimes |
| `05_lstar.ipynb` | LSTAR. Transicao logistica suave. Parametro gamma e velocidade de transicao |
| `06_estar.ipynb` | ESTAR. Transicao exponencial. Simetria em torno do threshold |
| `07_funcoes_transicao.ipynb` | logistic_transition(), exponential_transition(). Visualizacao e interpretacao |
| `08_comparacao.ipynb` | TAR vs SETAR vs LSTAR vs ESTAR no mesmo dataset. Selecao de modelo |
| `01_setar.R` | tsDyn: setar() |
| `02_star.R` | tsDyn: lstar(), estar() |
| `01_threshold.do` | Stata: threshold y, threshvar(y) |

**Funcionalidades cobertas:**
- `linearity_test()`, `transition_type_test()`, `tsay_test()`, `hansen_threshold_test()`
- `TAR`, `SETAR`, `LSTAR`, `ESTAR`
- `logistic_transition()`, `exponential_transition()`
- `ThresholdResults`: summary, plot_transition, regime_probabilities
- `plot_transition_function()`, `plot_phase_diagram()`

---

## Capitulo 13 — Portfolio e Risco Multivariado

**Objetivo:** Aplicacoes de modelos multivariados em gestao de portfolio.

| Arquivo | Conteudo |
|---------|----------|
| `01_portfolio_variance.ipynb` | portfolio_variance(), portfolio_volatility() com pesos fixos |
| `02_min_variance.ipynb` | minimum_variance_weights(). Pesos otimos estaticos e dinamicos |
| `03_risk_decomposition.ipynb` | risk_contribution(), marginal_risk_contribution(), risk_decomposition(). Atribuicao de risco |
| `04_dynamic_allocation.ipynb` | minimum_variance_weights_dynamic(). Alocacao dinamica ao longo do tempo |
| `05_caso_pratico.ipynb` | Caso completo: 5 ativos → DCC → pesos dinamicos → backtest do portfolio |
| `01_portfolio.R` | rmgarch: wmargin() para risk contribution |

**Funcionalidades cobertas:**
- `portfolio_variance()`, `portfolio_volatility()`
- `minimum_variance_weights()`, `minimum_variance_weights_dynamic()`
- `risk_contribution()`, `marginal_risk_contribution()`, `risk_decomposition()`

---

## Capitulo 14 — Experimentos e Comparacao de Modelos

**Objetivo:** Workflow automatizado de comparacao e selecao de modelos.

| Arquivo | Conteudo |
|---------|----------|
| `01_experiment_basico.ipynb` | ArchExperiment(returns). fit_all_models() com lista de especificacoes |
| `02_comparacao.ipynb` | compare_models(). Tabela AIC/BIC/loglike. Ranking de modelos |
| `03_out_of_sample.ipynb` | validate_out_of_sample(test_size=0.2). Metricas de previsao |
| `04_risk_analysis.ipynb` | risk_analysis(alpha=0.05). VaR/ES automatizado para todos os modelos |
| `05_workflow_completo.ipynb` | Pipeline end-to-end: dados → experimento → selecao → diagnostico → risco → relatorio |

**Funcionalidades cobertas:**
- `ArchExperiment`: fit_all_models, compare_models, validate_out_of_sample, risk_analysis
- `ComparisonResult`, `ValidationResult`, `RiskAnalysisResult`

---

## Capitulo 15 — Visualizacao

**Objetivo:** Todas as capacidades de visualizacao da biblioteca.

| Arquivo | Conteudo |
|---------|----------|
| `01_volatilidade.ipynb` | plot_volatility(), plot_variance_persistence(). Volatilidade condicional |
| `02_news_impact.ipynb` | plot_news_impact(), plot_news_impact_comparison(). Curvas de impacto |
| `03_diagnosticos_plot.ipynb` | plot_diagnostics(). ACF, PACF, QQ-plot dos residuos |
| `04_regimes_plot.ipynb` | plot_regimes(), plot_transition_matrix(). Probabilidades de regime |
| `05_correlacao.ipynb` | plot_dynamic_correlation(), plot_correlation_heatmap(), plot_covariance_decomposition() |
| `06_distribuicao.ipynb` | plot_distribution_fit(). Histograma + distribuicao ajustada |
| `07_risco_plot.ipynb` | plot_var_backtest(), plot_traffic_light(), plot_var_comparison() |
| `08_transicao_plot.ipynb` | plot_transition_function(), plot_phase_diagram() |
| `09_temas.ipynb` | get_theme(). Temas: professional, seaborn, minimal. Customizacao |
| `10_exportacao.ipynb` | export_png(), export_pdf(), export_svg(). Figuras para publicacao |

**Funcionalidades cobertas:**
- Todos os 15+ tipos de grafico
- `get_theme()`, `export_png()`, `export_pdf()`, `export_svg()`

---

## Capitulo 16 — Relatorios Automatizados

**Objetivo:** Geracao de relatorios profissionais em multiplos formatos.

| Arquivo | Conteudo |
|---------|----------|
| `01_relatorio_html.ipynb` | ReportManager.generate(fmt='html'). Relatorio GARCH interativo |
| `02_relatorio_latex.ipynb` | ReportManager.generate(fmt='latex'). Saida para papers academicos |
| `03_relatorio_markdown.ipynb` | ReportManager.generate(fmt='markdown'). Integracao com docs |
| `04_tipos_relatorio.ipynb` | report_type: 'garch', 'multivariate', 'regime', 'risk'. Todos os 4 tipos |
| `05_customizacao.ipynb` | Temas, titulos customizados, output_path. CSS manager |

**Funcionalidades cobertas:**
- `ReportManager.generate(results, report_type, fmt, theme, output_path, title)`
- Tipos: garch, multivariate, regime, risk
- Formatos: html, latex, markdown
- `CSSManager`, `TemplateManager`

---

## Capitulo 17 — Validacao Cruzada com R

**Objetivo:** Comparar resultados do archbox com pacotes de referencia em R.

| Arquivo | Conteudo |
|---------|----------|
| `01_vs_rugarch.ipynb` | GARCH, EGARCH, GJR: archbox vs rugarch. Tolerancia numerica |
| `02_vs_rmgarch.ipynb` | CCC, DCC: archbox vs rmgarch. Correlacoes dinamicas |
| `03_vs_mswm.ipynb` | MS-Mean, MS-AR: archbox vs MSwM. Probabilidades de regime |
| `01_rugarch_benchmark.R` | Script R completo para gerar resultados de referencia do rugarch |
| `02_rmgarch_benchmark.R` | Script R completo para gerar resultados de referencia do rmgarch |
| `03_mswm_benchmark.R` | Script R completo para gerar resultados de referencia do MSwM |

**Funcionalidades cobertas:**
- Validacao numerica dos estimadores
- Comparacao de log-likelihood, parametros, e standard errors

---

## Resumo quantitativo

| Metrica | Total |
|---------|-------|
| **Capitulos** | 17 |
| **Notebooks (.ipynb)** | 93 |
| **Scripts R (.R)** | 22 |
| **Scripts Stata (.do)** | 12 |
| **Total de arquivos** | **127** |

### Distribuicao por capitulo

| Capitulo | .ipynb | .R | .do |
|----------|--------|-----|------|
| 01 Introducao | 3 | 1 | 1 |
| 02 GARCH Classico | 6 | 2 | 2 |
| 03 GARCH Assimetricos | 5 | 3 | 2 |
| 04 GARCH Avancados | 5 | 3 | 1 |
| 05 Distribuicoes | 5 | 1 | 1 |
| 06 Diagnosticos | 8 | 1 | 1 |
| 07 Previsao | 4 | 1 | 1 |
| 08 Risco | 8 | 1 | 1 |
| 09 Multivariados Intro | 4 | 2 | 1 |
| 10 Multivariados Avancados | 4 | 2 | 0 |
| 11 Regime-Switching | 9 | 2 | 1 |
| 12 Threshold/STAR | 8 | 2 | 1 |
| 13 Portfolio | 5 | 1 | 0 |
| 14 Experimentos | 5 | 0 | 0 |
| 15 Visualizacao | 10 | 0 | 0 |
| 16 Relatorios | 5 | 0 | 0 |
| 17 Validacao Cruzada | 3 | 3 | 0 |

---

## Convencoes

- **Notebooks:** Cada celula com explicacao em Markdown antes do codigo. Outputs visiveis (graficos, tabelas).
- **Scripts R:** Comentarios em portugues. Usar pacotes rugarch, rmgarch, MSwM, tsDyn como referencia.
- **Scripts Stata:** Comentarios em portugues. Usar comandos nativos arch, mgarch, mswitch.
- **Datasets:** Usar os datasets built-in do archbox. Quando necessario, exportar CSV para R e Stata.
- **Numeracao:** Arquivos numerados sequencialmente dentro de cada capitulo (01_, 02_, ...).
- **Idioma:** Texto em portugues, nomes de variaveis e funcoes em ingles (seguindo a API).
