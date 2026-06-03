*==============================================================================
* Validacao Cruzada: GARCH-M e HAR-RV - archbox vs Stata
*==============================================================================
* Este script estima modelos GARCH-M (com variancia e log da variancia na
* equacao da media) e HAR-RV usando comandos nativos do Stata. Os resultados
* sao exportados para CSV para comparacao com a biblioteca archbox (Python).
*
* Modelos estimados:
*   1. GARCH(1,1)-M com sigma^2 na media (opcao archm)
*   2. GARCH(1,1)-M com log(sigma^2) na media (opcao archmexp(log))
*   3. HAR-RV via regressao OLS (regress)
*
* Datasets: sp500_returns.csv, realized_volatility.csv
* Distribuicao: Normal (Gaussiana)
*
* Nota: O Stata nao possui implementacao nativa de FIGARCH, portanto
* a validacao de modelos avancados cobre apenas GARCH-M e HAR-RV.
*
* Uso: stata -b do validation_02_garchm.do
*==============================================================================

clear all
set more off
set seed 42

* Diretorios relativos ao local deste script
local data_dir "../data"
local output_dir "../outputs"

* Criar diretorio de output se nao existir
capture mkdir "`output_dir'"

*==============================================================================
* PARTE 1: GARCH-M (variancia na equacao da media)
*==============================================================================

display _newline(2)
display "============================================================"
display "  VALIDACAO GARCH-M - S&P 500"
display "============================================================"

*----------------------------------------------------------------------
* 1.1 Importar dados SP500 e configurar serie temporal
*----------------------------------------------------------------------

* Importar CSV com retornos do SP500
import delimited "`data_dir'/sp500_returns.csv", clear

* Criar variavel de tempo sequencial para tsset
* (usamos indice numerico pois os dados ja estao ordenados por data)
gen t = _n
tsset t

* Resumo descritivo dos retornos
display _newline
display "--- Estatisticas Descritivas dos Retornos ---"
summarize returns, detail

*----------------------------------------------------------------------
* 1.2 Estimar GARCH(1,1)-M com sigma^2 na media
*----------------------------------------------------------------------

* GARCH-M adiciona a variancia condicional (sigma^2) como regressor
* na equacao da media:
*   r_t = mu + lambda * sigma^2_t + epsilon_t
*   sigma^2_t = omega + alpha * epsilon^2_{t-1} + beta * sigma^2_{t-1}
*
* A opcao `archm` inclui sigma^2_{t} na equacao da media.
* O coeficiente lambda mede o premio de risco: retornos maiores
* quando a volatilidade e maior.

arch returns, arch(1) garch(1) archm distribution(normal)
estimates store garchm

* Extrair parametro lambda (premio de risco)
* ARCHM:L1.sigma2 = coeficiente da variancia condicional na equacao da media
scalar lambda_garchm = _b[ARCHM:L1.sigma2]

* Extrair parametros da equacao da media
scalar mu_garchm = _b[returns:_cons]

* Extrair parametros da equacao da variancia
scalar omega_garchm  = _b[ARCH:_cons]
scalar alpha_garchm  = _b[ARCH:L1.arch]
scalar beta_garchm   = _b[ARCH:L1.garch]

* Estatisticas de ajuste
scalar ll_garchm  = e(ll)
scalar aic_garchm = e(aic)
scalar bic_garchm = e(bic)
scalar nobs_garchm = e(N)

display _newline
display "--- GARCH(1,1)-M (sigma^2) - Parametros ---"
display "mu (intercepto media):         " mu_garchm
display "lambda (premio de risco):      " lambda_garchm
display "omega (constante variancia):   " omega_garchm
display "alpha (ARCH):                  " alpha_garchm
display "beta  (GARCH):                 " beta_garchm
display "alpha + beta (persistencia):   " alpha_garchm + beta_garchm
display "Log-Likelihood:                " ll_garchm
display "AIC:                           " aic_garchm
display "BIC:                           " bic_garchm

* Diagnostico pos-estimacao: Teste ARCH-LM nos residuos
* H0: sem efeitos ARCH remanescentes nos residuos
estat archlm, lags(1 5 10)

* Predizer volatilidade condicional (variancia)
predict double sigma2_garchm, variance

*----------------------------------------------------------------------
* 1.3 Estimar GARCH(1,1)-M com log(sigma^2) na media
*----------------------------------------------------------------------

* Variante que usa log(sigma^2) ao inves de sigma^2 na equacao da media:
*   r_t = mu + lambda * log(sigma^2_t) + epsilon_t
*
* A opcao `archmexp(log)` aplica a transformacao logaritmica.
* Esta especificacao pode ser mais estavel numericamente e
* produzir uma relacao risco-retorno mais linear.

arch returns, arch(1) garch(1) archmexp(log) distribution(normal)
estimates store garchm_log

* Extrair parametro lambda (premio de risco com log)
scalar lambda_garchm_log = _b[ARCHM:L1.sigma2]

* Extrair parametros da equacao da media
scalar mu_garchm_log = _b[returns:_cons]

* Extrair parametros da equacao da variancia
scalar omega_garchm_log  = _b[ARCH:_cons]
scalar alpha_garchm_log  = _b[ARCH:L1.arch]
scalar beta_garchm_log   = _b[ARCH:L1.garch]

* Estatisticas de ajuste
scalar ll_garchm_log  = e(ll)
scalar aic_garchm_log = e(aic)
scalar bic_garchm_log = e(bic)

display _newline
display "--- GARCH(1,1)-M (log sigma^2) - Parametros ---"
display "mu (intercepto media):         " mu_garchm_log
display "lambda (premio risco, log):    " lambda_garchm_log
display "omega (constante variancia):   " omega_garchm_log
display "alpha (ARCH):                  " alpha_garchm_log
display "beta  (GARCH):                 " beta_garchm_log
display "alpha + beta (persistencia):   " alpha_garchm_log + beta_garchm_log
display "Log-Likelihood:                " ll_garchm_log
display "AIC:                           " aic_garchm_log
display "BIC:                           " bic_garchm_log

* Diagnostico pos-estimacao
estat archlm, lags(1 5 10)

* Predizer volatilidade condicional
predict double sigma2_garchm_log, variance

*----------------------------------------------------------------------
* 1.4 Comparacao de modelos GARCH-M
*----------------------------------------------------------------------

display _newline(2)
display "============================================================"
display "  COMPARACAO DE MODELOS GARCH-M"
display "============================================================"

* Tabela comparativa de AIC/BIC
estimates stats garchm garchm_log

*----------------------------------------------------------------------
* 1.5 Exportar resultados GARCH-M para CSV
*----------------------------------------------------------------------

preserve

clear
set obs 2

* Variaveis de identificacao
gen str30 model = ""

* Parametros da equacao da media
gen double mu = .
gen double lambda = .

* Parametros da equacao da variancia
gen double omega = .
gen double alpha = .
gen double beta = .

* Estatisticas de ajuste
gen double loglik = .
gen double aic = .
gen double bic = .
gen double nobs = .

* GARCH-M (sigma^2)
replace model  = "GARCH-M(1,1) sigma2" in 1
replace mu     = mu_garchm in 1
replace lambda = lambda_garchm in 1
replace omega  = omega_garchm in 1
replace alpha  = alpha_garchm in 1
replace beta   = beta_garchm in 1
replace loglik = ll_garchm in 1
replace aic    = aic_garchm in 1
replace bic    = bic_garchm in 1
replace nobs   = nobs_garchm in 1

* GARCH-M (log sigma^2)
replace model  = "GARCH-M(1,1) log" in 2
replace mu     = mu_garchm_log in 2
replace lambda = lambda_garchm_log in 2
replace omega  = omega_garchm_log in 2
replace alpha  = alpha_garchm_log in 2
replace beta   = beta_garchm_log in 2
replace loglik = ll_garchm_log in 2
replace aic    = aic_garchm_log in 2
replace bic    = bic_garchm_log in 2
replace nobs   = nobs_garchm in 2

* Listar resultados no log
list, clean noobs

* Exportar para CSV
export delimited "`output_dir'/stata_validation_garchm.csv", replace

display _newline
display "Resultados GARCH-M exportados para: `output_dir'/stata_validation_garchm.csv"

restore

*----------------------------------------------------------------------
* 1.6 Exportar volatilidade condicional GARCH-M
*----------------------------------------------------------------------

preserve
keep t returns sigma2_garchm sigma2_garchm_log
export delimited "`output_dir'/stata_volatility_garchm.csv", replace
display "Volatilidade GARCH-M exportada para: `output_dir'/stata_volatility_garchm.csv"
restore


*==============================================================================
* PARTE 2: HAR-RV (Heterogeneous Autoregressive Realized Volatility)
*==============================================================================

display _newline(2)
display "============================================================"
display "  VALIDACAO HAR-RV"
display "============================================================"

*----------------------------------------------------------------------
* 2.1 Importar dados de volatilidade realizada
*----------------------------------------------------------------------

* O dataset contem volatilidade realizada em tres horizontes:
*   rv_daily   - RV diaria (1 dia)
*   rv_weekly  - RV semanal (media 5 dias)
*   rv_monthly - RV mensal (media 22 dias)
* Modelo HAR-RV (Corsi, 2009):
*   RV_{t+1} = beta_0 + beta_d * RV^d_t + beta_w * RV^w_t + beta_m * RV^m_t + u_t

import delimited "`data_dir'/realized_volatility.csv", clear

* Criar variavel de tempo
gen t = _n
tsset t

* Resumo descritivo
display _newline
display "--- Estatisticas da Volatilidade Realizada ---"
summarize rv_daily rv_weekly rv_monthly, detail

*----------------------------------------------------------------------
* 2.2 Criar variavel dependente: RV diaria um passo a frente
*----------------------------------------------------------------------

* A variavel dependente e a RV do proximo dia (t+1)
* Usamos a notacao rv_daily[_n+1] para acessar o valor futuro
gen double rv_daily_lead = rv_daily[_n+1]

* Verificar que a variavel foi criada corretamente
display _newline
display "--- RV Daily Lead (primeiras observacoes) ---"
list t rv_daily rv_daily_lead in 1/5, clean

*----------------------------------------------------------------------
* 2.3 Estimar HAR-RV via OLS
*----------------------------------------------------------------------

* Regressao OLS simples:
*   RV_{t+1} = beta_0 + beta_d * RV^d_t + beta_w * RV^w_t + beta_m * RV^m_t
* Nota: a ultima observacao e perdida (rv_daily_lead = missing)

regress rv_daily_lead rv_daily rv_weekly rv_monthly
estimates store har_rv

* Extrair coeficientes HAR
scalar beta0_har    = _b[_cons]
scalar beta_d_har   = _b[rv_daily]
scalar beta_w_har   = _b[rv_weekly]
scalar beta_m_har   = _b[rv_monthly]

* Extrair estatisticas de ajuste
scalar r2_har       = e(r2)
scalar r2_adj_har   = e(r2_a)
scalar rmse_har     = e(rmse)
scalar nobs_har     = e(N)
scalar ll_har       = e(ll)

* Calcular AIC e BIC manualmente para OLS
* AIC = -2*LL + 2*k, BIC = -2*LL + k*ln(N)
* k = numero de parametros (4: constante + 3 regressores)
scalar k_har = e(df_m) + 1
scalar aic_har = -2 * ll_har + 2 * k_har
scalar bic_har = -2 * ll_har + k_har * ln(nobs_har)

display _newline
display "--- HAR-RV - Coeficientes ---"
display "beta_0 (constante):   " beta0_har
display "beta_d (diario):      " beta_d_har
display "beta_w (semanal):     " beta_w_har
display "beta_m (mensal):      " beta_m_har
display ""
display "--- HAR-RV - Ajuste ---"
display "R-squared:            " r2_har
display "Adjusted R-squared:   " r2_adj_har
display "RMSE:                 " rmse_har
display "Log-Likelihood:       " ll_har
display "AIC:                  " aic_har
display "BIC:                  " bic_har
display "N observacoes:        " nobs_har

* Valores preditos para comparacao
predict double rv_hat_har, xb

*----------------------------------------------------------------------
* 2.4 Exportar resultados HAR-RV para CSV
*----------------------------------------------------------------------

preserve

clear
set obs 1

gen str30 model = "HAR-RV"

* Coeficientes
gen double beta0    = beta0_har
gen double beta_d   = beta_d_har
gen double beta_w   = beta_w_har
gen double beta_m   = beta_m_har

* Ajuste
gen double r2       = r2_har
gen double r2_adj   = r2_adj_har
gen double rmse     = rmse_har
gen double loglik   = ll_har
gen double aic      = aic_har
gen double bic      = bic_har
gen double nobs     = nobs_har

* Listar no log
list, clean noobs

* Exportar
export delimited "`output_dir'/stata_validation_har_rv.csv", replace

display _newline
display "Resultados HAR-RV exportados para: `output_dir'/stata_validation_har_rv.csv"

restore

*----------------------------------------------------------------------
* 2.5 Exportar valores ajustados HAR-RV
*----------------------------------------------------------------------

preserve
keep t rv_daily rv_weekly rv_monthly rv_daily_lead rv_hat_har
export delimited "`output_dir'/stata_har_rv_fitted.csv", replace
display "Valores ajustados HAR-RV exportados para: `output_dir'/stata_har_rv_fitted.csv"
restore


*==============================================================================
* PARTE 3: Exportar tabela consolidada
*==============================================================================

display _newline(2)
display "============================================================"
display "  EXPORTANDO RESULTADOS CONSOLIDADOS"
display "============================================================"

* Criar dataset consolidado com todos os modelos
clear
set obs 3

gen str30 model = ""
gen str15 type = ""

* Parametros comuns
gen double param1 = .
gen str30 param1_name = ""
gen double param2 = .
gen str30 param2_name = ""
gen double param3 = .
gen str30 param3_name = ""
gen double param4 = .
gen str30 param4_name = ""
gen double param5 = .
gen str30 param5_name = ""
gen double param6 = .
gen str30 param6_name = ""

* Ajuste
gen double loglik = .
gen double aic = .
gen double bic = .

* GARCH-M (sigma^2)
replace model = "GARCH-M(1,1) sigma2" in 1
replace type  = "GARCH-M" in 1
replace param1 = mu_garchm in 1
replace param1_name = "mu" in 1
replace param2 = lambda_garchm in 1
replace param2_name = "lambda" in 1
replace param3 = omega_garchm in 1
replace param3_name = "omega" in 1
replace param4 = alpha_garchm in 1
replace param4_name = "alpha" in 1
replace param5 = beta_garchm in 1
replace param5_name = "beta" in 1
replace loglik = ll_garchm in 1
replace aic    = aic_garchm in 1
replace bic    = bic_garchm in 1

* GARCH-M (log sigma^2)
replace model = "GARCH-M(1,1) log" in 2
replace type  = "GARCH-M" in 2
replace param1 = mu_garchm_log in 2
replace param1_name = "mu" in 2
replace param2 = lambda_garchm_log in 2
replace param2_name = "lambda" in 2
replace param3 = omega_garchm_log in 2
replace param3_name = "omega" in 2
replace param4 = alpha_garchm_log in 2
replace param4_name = "alpha" in 2
replace param5 = beta_garchm_log in 2
replace param5_name = "beta" in 2
replace loglik = ll_garchm_log in 2
replace aic    = aic_garchm_log in 2
replace bic    = bic_garchm_log in 2

* HAR-RV
replace model = "HAR-RV" in 3
replace type  = "HAR-RV" in 3
replace param1 = beta0_har in 3
replace param1_name = "beta0" in 3
replace param2 = beta_d_har in 3
replace param2_name = "beta_daily" in 3
replace param3 = beta_w_har in 3
replace param3_name = "beta_weekly" in 3
replace param4 = beta_m_har in 3
replace param4_name = "beta_monthly" in 3
replace param5 = r2_har in 3
replace param5_name = "R2" in 3
replace param6 = rmse_har in 3
replace param6_name = "RMSE" in 3
replace loglik = ll_har in 3
replace aic    = aic_har in 3
replace bic    = bic_har in 3

* Listar tabela no log
list model type param1_name param1 param2_name param2 aic bic, clean noobs

* Exportar tabela consolidada
export delimited "`output_dir'/stata_validation_garchm_results.csv", replace

display _newline
display "============================================================"
display "  VALIDACAO CONCLUIDA"
display "============================================================"
display "Arquivos gerados em `output_dir'/:"
display "  - stata_validation_garchm.csv      (parametros GARCH-M)"
display "  - stata_validation_har_rv.csv       (parametros HAR-RV)"
display "  - stata_volatility_garchm.csv       (volatilidade condicional)"
display "  - stata_har_rv_fitted.csv            (valores ajustados HAR-RV)"
display "  - stata_validation_garchm_results.csv (consolidado)"
display "============================================================"

* Fim do script
exit
