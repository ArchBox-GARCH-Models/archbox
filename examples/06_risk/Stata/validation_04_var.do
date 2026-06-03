*******************************************************************************
* validation_04_var.do
* Validacao cruzada: VaR/ES com GARCH - Stata vs archbox (Python)
*
* Objetivo: Estimar GARCH(1,1) com distribuicao normal e t-Student,
*           calcular VaR parametrico (95% e 99%), implementar EWMA,
*           realizar backtesting simples e exportar resultados para CSV.
*
* Dados: sp500_returns.csv (retornos diarios do S&P 500)
* Referencia: archbox examples/06_risk
*******************************************************************************

clear all
set more off
set seed 42

*******************************************************************************
* 1. IMPORTAR DADOS E CONFIGURAR SERIE TEMPORAL
*******************************************************************************

* Importar CSV com retornos do S&P 500
import delimited "../data/sp500_returns.csv", clear

* Criar indice temporal e configurar como serie temporal
gen t = _n
tsset t

* Verificar dados importados
describe
summarize returns, detail
display "Numero de observacoes: " _N

*******************************************************************************
* 2. ESTIMAR GARCH(1,1) COM DISTRIBUICAO NORMAL
*******************************************************************************

* Estimar GARCH(1,1) com inovacoes normais
* Modelo: sigma2_t = omega + alpha * eps_{t-1}^2 + beta * sigma2_{t-1}
arch returns, arch(1) garch(1) distribution(normal)

* Salvar coeficientes do modelo normal
scalar omega_norm = _b[ARCH:_cons]
scalar alpha_norm = _b[ARCH:L.arch]
scalar beta_norm  = _b[ARCH:L.garch]

display "=== GARCH(1,1) Normal ==="
display "omega = " omega_norm
display "alpha = " alpha_norm
display "beta  = " beta_norm
display "alpha + beta = " alpha_norm + beta_norm

* Predizer variancia condicional
predict double sigma2_norm, variance
gen double sigma_norm = sqrt(sigma2_norm)

*******************************************************************************
* 3. CALCULAR VaR PARAMETRICO COM DISTRIBUICAO NORMAL
*******************************************************************************

* VaR 95% (quantil 5% da normal padrao = -1.6449)
* VaR = z_alpha * sigma_t  (valor negativo indica perda)
gen double var95_norm = invnormal(0.05) * sigma_norm

* VaR 99% (quantil 1% da normal padrao = -2.3263)
gen double var99_norm = invnormal(0.01) * sigma_norm

* Expected Shortfall (ES) normal: ES = sigma * phi(z_alpha) / alpha
* onde phi() e a funcao densidade da normal padrao
gen double es95_norm = -sigma_norm * normalden(invnormal(0.05)) / 0.05
gen double es99_norm = -sigma_norm * normalden(invnormal(0.01)) / 0.01

display "=== VaR/ES Normal (ultimas 5 obs) ==="
list var95_norm var99_norm es95_norm es99_norm in -5/l

*******************************************************************************
* 4. ESTIMAR GARCH(1,1) COM DISTRIBUICAO t-STUDENT
*******************************************************************************

* Estimar GARCH(1,1) com inovacoes t-Student
arch returns, arch(1) garch(1) distribution(t)

* Extrair graus de liberdade estimados
scalar df_hat = e(df)
display "Graus de liberdade estimados (t-Student): " df_hat

* Salvar coeficientes do modelo t
scalar omega_t = _b[ARCH:_cons]
scalar alpha_t = _b[ARCH:L.arch]
scalar beta_t  = _b[ARCH:L.garch]

display "=== GARCH(1,1) t-Student ==="
display "omega = " omega_t
display "alpha = " alpha_t
display "beta  = " beta_t
display "df    = " df_hat

* Predizer variancia condicional do modelo t
predict double sigma2_t, variance
gen double sigma_t = sqrt(sigma2_t)

*******************************************************************************
* 5. CALCULAR VaR COM DISTRIBUICAO t-STUDENT
*******************************************************************************

* VaR com t-Student: ajuste pela variancia da t (que e df/(df-2))
* VaR_t = t_{alpha,df} * sigma_t * sqrt((df-2)/df)
* Nota: invttail(df, p) retorna o quantil superior, entao usamos sinal negativo
gen double var95_t = -invttail(df_hat, 0.95) * sigma_t * sqrt((df_hat - 2) / df_hat)
gen double var99_t = -invttail(df_hat, 0.99) * sigma_t * sqrt((df_hat - 2) / df_hat)

* ES com t-Student (formula analitica)
* ES_t = sigma * [f(t_alpha) * (df + t_alpha^2) / ((df-1) * alpha)] * sqrt((df-2)/df)
scalar t_alpha95 = invttail(df_hat, 0.95)
scalar t_alpha99 = invttail(df_hat, 0.99)

* Funcao densidade da t-Student calculada manualmente
* f(x; df) = (1/sqrt(df)) * (1/beta(df/2, 1/2)) * (1 + x^2/df)^(-(df+1)/2)
scalar ft95 = tden(df_hat, t_alpha95)
scalar ft99 = tden(df_hat, t_alpha99)

gen double es95_t = -sigma_t * sqrt((df_hat - 2) / df_hat) * ///
    ft95 * (df_hat + t_alpha95^2) / ((df_hat - 1) * 0.05)
gen double es99_t = -sigma_t * sqrt((df_hat - 2) / df_hat) * ///
    ft99 * (df_hat + t_alpha99^2) / ((df_hat - 1) * 0.01)

display "=== VaR/ES t-Student (ultimas 5 obs) ==="
list var95_t var99_t es95_t es99_t in -5/l

*******************************************************************************
* 6. EWMA (LAMBDA = 0.94)
*******************************************************************************

* EWMA: sigma2_t = lambda * sigma2_{t-1} + (1-lambda) * r_{t-1}^2
* RiskMetrics com lambda = 0.94
scalar lambda_ewma = 0.94

gen double sigma2_ewma = .

* Inicializar com o quadrado do primeiro retorno
replace sigma2_ewma = returns[1]^2 in 1

* Recursao EWMA
replace sigma2_ewma = lambda_ewma * sigma2_ewma[_n-1] + ///
    (1 - lambda_ewma) * returns[_n-1]^2 in 2/l

gen double sigma_ewma = sqrt(sigma2_ewma)

* VaR EWMA (distribuicao normal)
gen double var95_ewma = invnormal(0.05) * sigma_ewma
gen double var99_ewma = invnormal(0.01) * sigma_ewma

* ES EWMA (normal)
gen double es95_ewma = -sigma_ewma * normalden(invnormal(0.05)) / 0.05
gen double es99_ewma = -sigma_ewma * normalden(invnormal(0.01)) / 0.01

display "=== EWMA VaR/ES (ultimas 5 obs) ==="
list var95_ewma var99_ewma es95_ewma es99_ewma in -5/l

*******************************************************************************
* 7. BACKTESTING: CONTAR VIOLACOES
*******************************************************************************

* Violacao: retorno observado < VaR (ambos negativos, entao retorno mais negativo)
* VaR 95% - esperado ~5% de violacoes
gen byte viol95_norm = (returns < var95_norm) if !missing(var95_norm)
gen byte viol95_t    = (returns < var95_t)    if !missing(var95_t)
gen byte viol95_ewma = (returns < var95_ewma) if !missing(var95_ewma)

* VaR 99% - esperado ~1% de violacoes
gen byte viol99_norm = (returns < var99_norm) if !missing(var99_norm)
gen byte viol99_t    = (returns < var99_t)    if !missing(var99_t)
gen byte viol99_ewma = (returns < var99_ewma) if !missing(var99_ewma)

display ""
display "============================================="
display "=== BACKTESTING: TAXA DE VIOLACOES ========="
display "============================================="

* Resumo das violacoes (media = taxa de violacao)
display ""
display "--- VaR 95% (nivel nominal = 5%) ---"
summarize viol95_norm viol95_t viol95_ewma

display ""
display "--- VaR 99% (nivel nominal = 1%) ---"
summarize viol99_norm viol99_t viol99_ewma

* Calcular taxas de violacao e comparar com nivel nominal
quietly {
    * VaR 95%
    summarize viol95_norm
    scalar rate95_norm = r(mean)
    summarize viol95_t
    scalar rate95_t = r(mean)
    summarize viol95_ewma
    scalar rate95_ewma = r(mean)

    * VaR 99%
    summarize viol99_norm
    scalar rate99_norm = r(mean)
    summarize viol99_t
    scalar rate99_t = r(mean)
    summarize viol99_ewma
    scalar rate99_ewma = r(mean)

    * Numero de observacoes usadas
    summarize viol95_norm
    scalar n_obs = r(N)
}

display ""
display "============================================="
display "=== COMPARACAO COM NIVEL NOMINAL ============"
display "============================================="
display ""
display "Metodo          | VaR95 (nom=5%) | VaR99 (nom=1%)"
display "----------------|----------------|----------------"
display "GARCH Normal    | " %6.4f rate95_norm "         | " %6.4f rate99_norm
display "GARCH t-Student | " %6.4f rate95_t    "         | " %6.4f rate99_t
display "EWMA (l=0.94)   | " %6.4f rate95_ewma "         | " %6.4f rate99_ewma
display ""
display "Obs usadas no backtest: " n_obs

* Teste binomial informal: intervalo de confianca 95% para proporcao
* Para VaR 95%: p=0.05, IC ~ 0.05 +/- 1.96*sqrt(0.05*0.95/N)
scalar se95 = sqrt(0.05 * 0.95 / n_obs)
scalar se99 = sqrt(0.01 * 0.99 / n_obs)
display ""
display "Intervalo aceitavel (aprox) VaR 95%: [" ///
    %6.4f (0.05 - 1.96 * se95) ", " %6.4f (0.05 + 1.96 * se95) "]"
display "Intervalo aceitavel (aprox) VaR 99%: [" ///
    %6.4f (0.01 - 1.96 * se99) ", " %6.4f (0.01 + 1.96 * se99) "]"

*******************************************************************************
* 8. EXPORTAR RESULTADOS PARA CSV
*******************************************************************************

* Exportar serie temporal completa com VaR e violacoes
preserve

keep t date returns ///
    sigma_norm var95_norm var99_norm es95_norm es99_norm viol95_norm viol99_norm ///
    sigma_t var95_t var99_t es95_t es99_t viol95_t viol99_t ///
    sigma_ewma var95_ewma var99_ewma es95_ewma es99_ewma viol95_ewma viol99_ewma

export delimited using "../outputs/stata_var_results.csv", replace
display "Resultados exportados para ../outputs/stata_var_results.csv"

restore

* Exportar resumo das taxas de violacao
preserve
clear
set obs 3

gen str20 method = ""
gen double rate_var95 = .
gen double rate_var99 = .
gen double nominal_95 = 0.05
gen double nominal_99 = 0.01

replace method = "GARCH_Normal"    in 1
replace rate_var95 = rate95_norm   in 1
replace rate_var99 = rate99_norm   in 1

replace method = "GARCH_tStudent"  in 2
replace rate_var95 = rate95_t      in 2
replace rate_var99 = rate99_t      in 2

replace method = "EWMA_094"        in 3
replace rate_var95 = rate95_ewma   in 3
replace rate_var99 = rate99_ewma   in 3

export delimited using "../outputs/stata_var_backtest_summary.csv", replace
display "Resumo do backtest exportado para ../outputs/stata_var_backtest_summary.csv"

restore

* Exportar parametros estimados
preserve
clear
set obs 3

gen str20 model = ""
gen double omega = .
gen double alpha = .
gen double beta = .
gen double df = .

replace model = "GARCH_Normal"    in 1
replace omega = omega_norm        in 1
replace alpha = alpha_norm        in 1
replace beta  = beta_norm         in 1

replace model = "GARCH_tStudent"  in 2
replace omega = omega_t           in 2
replace alpha = alpha_t           in 2
replace beta  = beta_t            in 2
replace df    = df_hat            in 2

replace model = "EWMA_094"        in 3
replace omega = 0                 in 3
replace alpha = 0.06              in 3
replace beta  = 0.94              in 3

export delimited using "../outputs/stata_var_parameters.csv", replace
display "Parametros exportados para ../outputs/stata_var_parameters.csv"

restore

*******************************************************************************
* 9. RESUMO FINAL
*******************************************************************************

display ""
display "============================================="
display "=== VALIDACAO CONCLUIDA ====================="
display "============================================="
display ""
display "Modelos estimados:"
display "  1. GARCH(1,1) com distribuicao Normal"
display "  2. GARCH(1,1) com distribuicao t-Student"
display "  3. EWMA (lambda = 0.94)"
display ""
display "Metricas calculadas:"
display "  - VaR 95% e 99% para cada modelo"
display "  - Expected Shortfall (ES) 95% e 99%"
display "  - Violacoes e taxas de violacao"
display ""
display "Arquivos exportados:"
display "  - ../outputs/stata_var_results.csv (serie completa)"
display "  - ../outputs/stata_var_backtest_summary.csv (resumo backtest)"
display "  - ../outputs/stata_var_parameters.csv (parametros estimados)"
display ""
display "Compare estes resultados com os do archbox (Python)"
display "para validacao cruzada."
display "============================================="

log close _all
exit
