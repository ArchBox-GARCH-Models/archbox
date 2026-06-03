*==============================================================================
* Validacao Cruzada: GARCH Univariado - archbox vs Stata
*==============================================================================
* Este script estima modelos GARCH(1,1), EGARCH(1,1) e GJR-GARCH(1,1)
* usando o comando `arch` nativo do Stata. Os resultados sao exportados
* para CSV para comparacao com os obtidos pela biblioteca archbox (Python).
*
* Datasets: sp500_returns.csv, ibovespa_returns.csv
* Distribuicao: Normal (Gaussiana)
*
* Uso: stata -b do validation_01_garch.do
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
* PARTE 1: S&P 500
*==============================================================================

display _newline(2)
display "============================================================"
display "  VALIDACAO GARCH - S&P 500"
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
summarize returns, detail

*----------------------------------------------------------------------
* 1.2 Estimar GARCH(1,1) com distribuicao normal
*----------------------------------------------------------------------

* O comando arch estima a equacao da media e da variancia conjuntamente
* arch(1) = termo ARCH de ordem 1 (alpha * epsilon^2_{t-1})
* garch(1) = termo GARCH de ordem 1 (beta * sigma^2_{t-1})
* Modelo: sigma^2_t = omega + alpha * epsilon^2_{t-1} + beta * sigma^2_{t-1}
arch returns, arch(1) garch(1) distribution(normal)
estimates store garch11_sp500

* Extrair parametros da equacao da variancia
* A matriz e(b) contem todos os coeficientes estimados
matrix b_garch = e(b)
matrix list b_garch

* Salvar parametros em scalars para exportacao posterior
* Nota: a posicao dos coeficientes depende da especificacao do modelo
* Equacao da media: _cons (intercepto)
* Equacao ARCH: L1.arch (alpha), L1.garch (beta), _cons (omega)
scalar omega_garch_sp = _b[ARCH:_cons]
scalar alpha_garch_sp = _b[ARCH:L1.arch]
scalar beta_garch_sp  = _b[ARCH:L1.garch]

* Salvar estatisticas de ajuste
scalar ll_garch_sp  = e(ll)
scalar aic_garch_sp = e(aic)
scalar bic_garch_sp = e(bic)
scalar nobs_garch_sp = e(N)

display _newline
display "--- GARCH(1,1) SP500 - Parametros ---"
display "omega (constante variancia): " omega_garch_sp
display "alpha (ARCH):                " alpha_garch_sp
display "beta  (GARCH):               " beta_garch_sp
display "alpha + beta:                 " alpha_garch_sp + beta_garch_sp
display "Log-Likelihood:               " ll_garch_sp
display "AIC:                          " aic_garch_sp
display "BIC:                          " bic_garch_sp

* Diagnostico pos-estimacao: Teste ARCH-LM
* Testa se ainda ha efeitos ARCH nos residuos (H0: sem efeitos ARCH)
estat archlm, lags(1 5 10)

* Predizer volatilidade condicional (variancia)
predict double sigma2_garch_sp500, variance

*----------------------------------------------------------------------
* 1.3 Estimar EGARCH(1,1) com distribuicao normal
*----------------------------------------------------------------------

* EGARCH modela o log da variancia condicional
* earch(1) = efeito de magnitude dos choques (alpha)
* egarch(1) = persistencia no log da variancia (beta)
* O modelo captura assimetria: choques negativos podem ter efeito
* diferente dos positivos na volatilidade
arch returns, earch(1) egarch(1) distribution(normal)
estimates store egarch11_sp500

* Extrair parametros EGARCH
* Equacao ARCH: L1.earch (efeito tamanho), L1.egarch (persistencia),
*               L1.earch_a (efeito assimetria/leverage), _cons (omega)
scalar omega_egarch_sp = _b[ARCH:_cons]
scalar alpha_egarch_sp = _b[ARCH:L1.earch]
scalar beta_egarch_sp  = _b[ARCH:L1.egarch]
scalar gamma_egarch_sp = _b[ARCH:L1.earch_a]

scalar ll_egarch_sp  = e(ll)
scalar aic_egarch_sp = e(aic)
scalar bic_egarch_sp = e(bic)

display _newline
display "--- EGARCH(1,1) SP500 - Parametros ---"
display "omega (constante):    " omega_egarch_sp
display "alpha (magnitude):    " alpha_egarch_sp
display "beta  (persistencia): " beta_egarch_sp
display "gamma (assimetria):   " gamma_egarch_sp
display "Log-Likelihood:       " ll_egarch_sp
display "AIC:                  " aic_egarch_sp
display "BIC:                  " bic_egarch_sp

* Diagnostico pos-estimacao
estat archlm, lags(1 5 10)

* Predizer volatilidade condicional
predict double sigma2_egarch_sp500, variance

*----------------------------------------------------------------------
* 1.4 Estimar GJR-GARCH(1,1) / TARCH com distribuicao normal
*----------------------------------------------------------------------

* GJR-GARCH adiciona um termo asimetrico ao GARCH padrao
* tarch(1) = termo threshold/assimetrico (gamma * I_{t-1} * epsilon^2_{t-1})
* onde I_{t-1} = 1 se epsilon_{t-1} < 0 (choque negativo)
* Modelo: sigma^2_t = omega + alpha*eps^2_{t-1} + gamma*I*eps^2_{t-1} + beta*sigma^2_{t-1}
arch returns, arch(1) garch(1) tarch(1) distribution(normal)
estimates store gjr11_sp500

* Extrair parametros GJR-GARCH
scalar omega_gjr_sp = _b[ARCH:_cons]
scalar alpha_gjr_sp = _b[ARCH:L1.arch]
scalar beta_gjr_sp  = _b[ARCH:L1.garch]
scalar gamma_gjr_sp = _b[ARCH:L1.tarch]

scalar ll_gjr_sp  = e(ll)
scalar aic_gjr_sp = e(aic)
scalar bic_gjr_sp = e(bic)

display _newline
display "--- GJR-GARCH(1,1) SP500 - Parametros ---"
display "omega (constante):   " omega_gjr_sp
display "alpha (ARCH):        " alpha_gjr_sp
display "beta  (GARCH):       " beta_gjr_sp
display "gamma (assimetria):  " gamma_gjr_sp
display "Log-Likelihood:      " ll_gjr_sp
display "AIC:                 " aic_gjr_sp
display "BIC:                 " bic_gjr_sp

* Diagnostico pos-estimacao
estat archlm, lags(1 5 10)

* Predizer volatilidade condicional
predict double sigma2_gjr_sp500, variance

*----------------------------------------------------------------------
* 1.5 Comparacao de modelos SP500
*----------------------------------------------------------------------

display _newline(2)
display "============================================================"
display "  COMPARACAO DE MODELOS - SP500"
display "============================================================"

* Tabela comparativa de AIC/BIC gerada pelo Stata
estimates stats garch11_sp500 egarch11_sp500 gjr11_sp500

*----------------------------------------------------------------------
* 1.6 Exportar resultados SP500 para CSV
*----------------------------------------------------------------------

* Preservar dados atuais para restaurar depois
preserve

* Criar dataset com resultados dos tres modelos
clear
set obs 3

* Variaveis de identificacao
gen str20 dataset = "SP500"
gen str20 model = ""

* Variaveis de parametros
gen double omega = .
gen double alpha = .
gen double beta = .
gen double gamma = .

* Variaveis de ajuste
gen double loglik = .
gen double aic = .
gen double bic = .

* GARCH(1,1)
replace model  = "GARCH(1,1)" in 1
replace omega  = omega_garch_sp in 1
replace alpha  = alpha_garch_sp in 1
replace beta   = beta_garch_sp in 1
replace gamma  = . in 1
replace loglik = ll_garch_sp in 1
replace aic    = aic_garch_sp in 1
replace bic    = bic_garch_sp in 1

* EGARCH(1,1)
replace model  = "EGARCH(1,1)" in 2
replace omega  = omega_egarch_sp in 2
replace alpha  = alpha_egarch_sp in 2
replace beta   = beta_egarch_sp in 2
replace gamma  = gamma_egarch_sp in 2
replace loglik = ll_egarch_sp in 2
replace aic    = aic_egarch_sp in 2
replace bic    = bic_egarch_sp in 2

* GJR-GARCH(1,1)
replace model  = "GJR-GARCH(1,1)" in 3
replace omega  = omega_gjr_sp in 3
replace alpha  = alpha_gjr_sp in 3
replace beta   = beta_gjr_sp in 3
replace gamma  = gamma_gjr_sp in 3
replace loglik = ll_gjr_sp in 3
replace aic    = aic_gjr_sp in 3
replace bic    = bic_gjr_sp in 3

* Exportar para CSV
export delimited "`output_dir'/stata_validation_garch_sp500.csv", replace

display _newline
display "Resultados SP500 exportados para: `output_dir'/stata_validation_garch_sp500.csv"

restore

*----------------------------------------------------------------------
* 1.7 Exportar volatilidade condicional SP500
*----------------------------------------------------------------------

* Exportar serie de volatilidade para comparacao visual com archbox
preserve
keep t returns sigma2_garch_sp500 sigma2_egarch_sp500 sigma2_gjr_sp500
export delimited "`output_dir'/stata_volatility_sp500.csv", replace
display "Volatilidade SP500 exportada para: `output_dir'/stata_volatility_sp500.csv"
restore


*==============================================================================
* PARTE 2: IBOVESPA
*==============================================================================

display _newline(2)
display "============================================================"
display "  VALIDACAO GARCH - IBOVESPA"
display "============================================================"

*----------------------------------------------------------------------
* 2.1 Importar dados Ibovespa e configurar serie temporal
*----------------------------------------------------------------------

import delimited "`data_dir'/ibovespa_returns.csv", clear

gen t = _n
tsset t

summarize returns, detail

*----------------------------------------------------------------------
* 2.2 Estimar GARCH(1,1) com distribuicao normal
*----------------------------------------------------------------------

arch returns, arch(1) garch(1) distribution(normal)
estimates store garch11_ibov

* Extrair parametros
scalar omega_garch_ibov = _b[ARCH:_cons]
scalar alpha_garch_ibov = _b[ARCH:L1.arch]
scalar beta_garch_ibov  = _b[ARCH:L1.garch]

scalar ll_garch_ibov  = e(ll)
scalar aic_garch_ibov = e(aic)
scalar bic_garch_ibov = e(bic)

display _newline
display "--- GARCH(1,1) IBOVESPA - Parametros ---"
display "omega: " omega_garch_ibov
display "alpha: " alpha_garch_ibov
display "beta:  " beta_garch_ibov
display "alpha + beta: " alpha_garch_ibov + beta_garch_ibov
display "Log-Likelihood: " ll_garch_ibov
display "AIC: " aic_garch_ibov
display "BIC: " bic_garch_ibov

* Teste ARCH-LM pos-estimacao
estat archlm, lags(1 5 10)

* Volatilidade condicional
predict double sigma2_garch_ibov, variance

*----------------------------------------------------------------------
* 2.3 Estimar EGARCH(1,1) com distribuicao normal
*----------------------------------------------------------------------

arch returns, earch(1) egarch(1) distribution(normal)
estimates store egarch11_ibov

scalar omega_egarch_ibov = _b[ARCH:_cons]
scalar alpha_egarch_ibov = _b[ARCH:L1.earch]
scalar beta_egarch_ibov  = _b[ARCH:L1.egarch]
scalar gamma_egarch_ibov = _b[ARCH:L1.earch_a]

scalar ll_egarch_ibov  = e(ll)
scalar aic_egarch_ibov = e(aic)
scalar bic_egarch_ibov = e(bic)

display _newline
display "--- EGARCH(1,1) IBOVESPA - Parametros ---"
display "omega: " omega_egarch_ibov
display "alpha: " alpha_egarch_ibov
display "beta:  " beta_egarch_ibov
display "gamma: " gamma_egarch_ibov
display "Log-Likelihood: " ll_egarch_ibov
display "AIC: " aic_egarch_ibov
display "BIC: " bic_egarch_ibov

estat archlm, lags(1 5 10)

predict double sigma2_egarch_ibov, variance

*----------------------------------------------------------------------
* 2.4 Estimar GJR-GARCH(1,1) com distribuicao normal
*----------------------------------------------------------------------

arch returns, arch(1) garch(1) tarch(1) distribution(normal)
estimates store gjr11_ibov

scalar omega_gjr_ibov = _b[ARCH:_cons]
scalar alpha_gjr_ibov = _b[ARCH:L1.arch]
scalar beta_gjr_ibov  = _b[ARCH:L1.garch]
scalar gamma_gjr_ibov = _b[ARCH:L1.tarch]

scalar ll_gjr_ibov  = e(ll)
scalar aic_gjr_ibov = e(aic)
scalar bic_gjr_ibov = e(bic)

display _newline
display "--- GJR-GARCH(1,1) IBOVESPA - Parametros ---"
display "omega: " omega_gjr_ibov
display "alpha: " alpha_gjr_ibov
display "beta:  " beta_gjr_ibov
display "gamma: " gamma_gjr_ibov
display "Log-Likelihood: " ll_gjr_ibov
display "AIC: " aic_gjr_ibov
display "BIC: " bic_gjr_ibov

estat archlm, lags(1 5 10)

predict double sigma2_gjr_ibov, variance

*----------------------------------------------------------------------
* 2.5 Comparacao de modelos Ibovespa
*----------------------------------------------------------------------

display _newline(2)
display "============================================================"
display "  COMPARACAO DE MODELOS - IBOVESPA"
display "============================================================"

estimates stats garch11_ibov egarch11_ibov gjr11_ibov

*----------------------------------------------------------------------
* 2.6 Exportar resultados Ibovespa para CSV
*----------------------------------------------------------------------

preserve

clear
set obs 3

gen str20 dataset = "IBOVESPA"
gen str20 model = ""
gen double omega = .
gen double alpha = .
gen double beta = .
gen double gamma = .
gen double loglik = .
gen double aic = .
gen double bic = .

* GARCH(1,1)
replace model  = "GARCH(1,1)" in 1
replace omega  = omega_garch_ibov in 1
replace alpha  = alpha_garch_ibov in 1
replace beta   = beta_garch_ibov in 1
replace gamma  = . in 1
replace loglik = ll_garch_ibov in 1
replace aic    = aic_garch_ibov in 1
replace bic    = bic_garch_ibov in 1

* EGARCH(1,1)
replace model  = "EGARCH(1,1)" in 2
replace omega  = omega_egarch_ibov in 2
replace alpha  = alpha_egarch_ibov in 2
replace beta   = beta_egarch_ibov in 2
replace gamma  = gamma_egarch_ibov in 2
replace loglik = ll_egarch_ibov in 2
replace aic    = aic_egarch_ibov in 2
replace bic    = bic_egarch_ibov in 2

* GJR-GARCH(1,1)
replace model  = "GJR-GARCH(1,1)" in 3
replace omega  = omega_gjr_ibov in 3
replace alpha  = alpha_gjr_ibov in 3
replace beta   = beta_gjr_ibov in 3
replace gamma  = gamma_gjr_ibov in 3
replace loglik = ll_gjr_ibov in 3
replace aic    = aic_gjr_ibov in 3
replace bic    = bic_gjr_ibov in 3

export delimited "`output_dir'/stata_validation_garch_ibovespa.csv", replace

display _newline
display "Resultados Ibovespa exportados para: `output_dir'/stata_validation_garch_ibovespa.csv"

restore

*----------------------------------------------------------------------
* 2.7 Exportar volatilidade condicional Ibovespa
*----------------------------------------------------------------------

preserve
keep t returns sigma2_garch_ibov sigma2_egarch_ibov sigma2_gjr_ibov
export delimited "`output_dir'/stata_volatility_ibovespa.csv", replace
display "Volatilidade Ibovespa exportada para: `output_dir'/stata_volatility_ibovespa.csv"
restore


*==============================================================================
* PARTE 3: Exportar tabela consolidada (ambos datasets)
*==============================================================================

display _newline(2)
display "============================================================"
display "  EXPORTANDO RESULTADOS CONSOLIDADOS"
display "============================================================"

* Criar dataset consolidado com resultados de ambos os indices
clear
set obs 6

gen str20 dataset = ""
gen str20 model = ""
gen double omega = .
gen double alpha = .
gen double beta = .
gen double gamma = .
gen double loglik = .
gen double aic = .
gen double bic = .

* SP500
replace dataset = "SP500" in 1/3
replace model  = "GARCH(1,1)" in 1
replace omega  = omega_garch_sp in 1
replace alpha  = alpha_garch_sp in 1
replace beta   = beta_garch_sp in 1
replace loglik = ll_garch_sp in 1
replace aic    = aic_garch_sp in 1
replace bic    = bic_garch_sp in 1

replace model  = "EGARCH(1,1)" in 2
replace omega  = omega_egarch_sp in 2
replace alpha  = alpha_egarch_sp in 2
replace beta   = beta_egarch_sp in 2
replace gamma  = gamma_egarch_sp in 2
replace loglik = ll_egarch_sp in 2
replace aic    = aic_egarch_sp in 2
replace bic    = bic_egarch_sp in 2

replace model  = "GJR-GARCH(1,1)" in 3
replace omega  = omega_gjr_sp in 3
replace alpha  = alpha_gjr_sp in 3
replace beta   = beta_gjr_sp in 3
replace gamma  = gamma_gjr_sp in 3
replace loglik = ll_gjr_sp in 3
replace aic    = aic_gjr_sp in 3
replace bic    = bic_gjr_sp in 3

* IBOVESPA
replace dataset = "IBOVESPA" in 4/6
replace model  = "GARCH(1,1)" in 4
replace omega  = omega_garch_ibov in 4
replace alpha  = alpha_garch_ibov in 4
replace beta   = beta_garch_ibov in 4
replace loglik = ll_garch_ibov in 4
replace aic    = aic_garch_ibov in 4
replace bic    = bic_garch_ibov in 4

replace model  = "EGARCH(1,1)" in 5
replace omega  = omega_egarch_ibov in 5
replace alpha  = alpha_egarch_ibov in 5
replace beta   = beta_egarch_ibov in 5
replace gamma  = gamma_egarch_ibov in 5
replace loglik = ll_egarch_ibov in 5
replace aic    = aic_egarch_ibov in 5
replace bic    = bic_egarch_ibov in 5

replace model  = "GJR-GARCH(1,1)" in 6
replace omega  = omega_gjr_ibov in 6
replace alpha  = alpha_gjr_ibov in 6
replace beta   = beta_gjr_ibov in 6
replace gamma  = gamma_gjr_ibov in 6
replace loglik = ll_gjr_ibov in 6
replace aic    = aic_gjr_ibov in 6
replace bic    = bic_gjr_ibov in 6

* Listar tabela no log
list, clean noobs

* Exportar tabela consolidada
export delimited "`output_dir'/stata_validation_garch_results.csv", replace

display _newline
display "============================================================"
display "  VALIDACAO CONCLUIDA"
display "============================================================"
display "Arquivos gerados em `output_dir'/:"
display "  - stata_validation_garch_sp500.csv"
display "  - stata_validation_garch_ibovespa.csv"
display "  - stata_validation_garch_results.csv (consolidado)"
display "  - stata_volatility_sp500.csv"
display "  - stata_volatility_ibovespa.csv"
display "============================================================"

* Fim do script
exit
