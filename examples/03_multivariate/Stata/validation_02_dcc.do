********************************************************************************
* validation_02_dcc.do
*
* Validacao cruzada: DCC-GARCH multivariado usando Stata
* Compara CCC vs DCC para 4 pares de moedas (EUR/USD, GBP/USD, JPY/USD, CHF/USD)
*
* Objetivo:
*   - Estimar CCC-GARCH(1,1) e DCC-GARCH(1,1) para retornos FX
*   - Extrair parametros DCC (lambda1, lambda2)
*   - Comparar modelos via AIC/BIC
*   - Predizer covariancias condicionais
*   - Exportar resultados para validacao contra archbox (Python)
*
* Uso: stata -b do validation_02_dcc.do
********************************************************************************

clear all
set more off
capture log close
log using "validation_02_dcc.log", replace

********************************************************************************
* ETAPA 1: Importar dados e configurar serie temporal
********************************************************************************

* Importar os retornos FX do CSV
import delimited "../data/fx_majors.csv", clear

* Escalar retornos para porcentagem (melhor convergencia numerica)
replace eurusd = eurusd * 100
replace gbpusd = gbpusd * 100
replace jpyusd = jpyusd * 100
replace chfusd = chfusd * 100

* Criar variavel de tempo e configurar tsset
gen t = _n
tsset t

* Resumo descritivo dos dados
summarize eurusd gbpusd jpyusd chfusd
correlate eurusd gbpusd jpyusd chfusd

display "Numero de observacoes: " _N

********************************************************************************
* ETAPA 2: Estimar modelo CCC-GARCH(1,1)
********************************************************************************

* CCC: Constant Conditional Correlation GARCH
* Estima volatilidades individuais GARCH(1,1) e correlacao constante
display _newline(2)
display "================================================================"
display "  MODELO CCC-GARCH(1,1)"
display "================================================================"

mgarch ccc (eurusd gbpusd jpyusd chfusd =, noconstant), arch(1) garch(1)
estimates store ccc_model

* Criterios de informacao para CCC
estat ic
matrix ic_ccc = r(S)
scalar aic_ccc = ic_ccc[1,5]
scalar bic_ccc = ic_ccc[1,6]
scalar ll_ccc  = ic_ccc[1,3]
scalar npar_ccc = ic_ccc[1,4]

display _newline
display "CCC - Log-Likelihood: " ll_ccc
display "CCC - AIC:            " aic_ccc
display "CCC - BIC:            " bic_ccc
display "CCC - N parametros:   " npar_ccc

********************************************************************************
* ETAPA 3: Estimar modelo DCC-GARCH(1,1)
********************************************************************************

* DCC: Dynamic Conditional Correlation GARCH
* Estima volatilidades individuais + correlacoes dinamicas
display _newline(2)
display "================================================================"
display "  MODELO DCC-GARCH(1,1)"
display "================================================================"

mgarch dcc (eurusd gbpusd jpyusd chfusd =, noconstant), arch(1) garch(1)
estimates store dcc_model

* Criterios de informacao para DCC
estat ic
matrix ic_dcc = r(S)
scalar aic_dcc = ic_dcc[1,5]
scalar bic_dcc = ic_dcc[1,6]
scalar ll_dcc  = ic_dcc[1,3]
scalar npar_dcc = ic_dcc[1,4]

display _newline
display "DCC - Log-Likelihood: " ll_dcc
display "DCC - AIC:            " aic_dcc
display "DCC - BIC:            " bic_dcc
display "DCC - N parametros:   " npar_dcc

********************************************************************************
* ETAPA 4: Extrair parametros DCC (lambda1 e lambda2)
********************************************************************************

* Os parametros DCC sao:
*   lambda1 (a): peso da inovacao padronizada (ajuste)
*   lambda2 (b): peso da correlacao passada (persistencia)
*
* No Stata, estes sao armazenados como Adjustment:lambda1 e Adjustment:lambda2

display _newline(2)
display "================================================================"
display "  PARAMETROS DCC"
display "================================================================"

estimates restore dcc_model

* Extrair lambda1 e lambda2 da equacao Adjustment
scalar lambda1 = _b[Adjustment:lambda1]
scalar lambda2 = _b[Adjustment:lambda2]
scalar persistence_dcc = lambda1 + lambda2

display "DCC lambda1 (a):     " lambda1
display "DCC lambda2 (b):     " lambda2
display "DCC persistencia:    " persistence_dcc

* Extrair parametros ARCH/GARCH individuais de cada equacao
display _newline
display "Parametros GARCH individuais (DCC):"
display "-----------------------------------"

foreach var in eurusd gbpusd jpyusd chfusd {
    scalar omega_`var' = _b[ARCH_`var':_cons]
    scalar alpha_`var' = _b[ARCH_`var':L.arch_`var']
    scalar beta_`var'  = _b[ARCH_`var':L.garch_`var']
    display "`var' - omega: " omega_`var' " alpha: " alpha_`var' " beta: " beta_`var'
}

********************************************************************************
* ETAPA 5: Comparar modelos CCC vs DCC
********************************************************************************

display _newline(2)
display "================================================================"
display "  COMPARACAO CCC vs DCC"
display "================================================================"

* Tabela comparativa formal
estimates stats ccc_model dcc_model

* Teste de preferencia
display _newline
display "Diferenca AIC (CCC - DCC): " aic_ccc - aic_dcc
display "Diferenca BIC (CCC - DCC): " bic_ccc - bic_dcc

if aic_dcc < aic_ccc {
    display "=> DCC preferido pelo AIC"
}
else {
    display "=> CCC preferido pelo AIC"
}

if bic_dcc < bic_ccc {
    display "=> DCC preferido pelo BIC"
}
else {
    display "=> CCC preferido pelo BIC"
}

********************************************************************************
* ETAPA 6: Predizer covariancias condicionais
********************************************************************************

display _newline(2)
display "================================================================"
display "  COVARIANCIAS CONDICIONAIS"
display "================================================================"

* Restaurar modelo DCC para predicao
estimates restore dcc_model

* predict H*, variance gera:
*   H_eurusd_eurusd  H_eurusd_gbpusd  H_eurusd_jpyusd  H_eurusd_chfusd
*   H_gbpusd_gbpusd  H_gbpusd_jpyusd  H_gbpusd_chfusd
*   H_jpyusd_jpyusd  H_jpyusd_chfusd
*   H_chfusd_chfusd
predict H*, variance

* Resumo das variancias condicionais (diagonal)
summarize H_eurusd_eurusd H_gbpusd_gbpusd H_jpyusd_jpyusd H_chfusd_chfusd

* Resumo de algumas covariancias (fora da diagonal)
summarize H_eurusd_gbpusd H_eurusd_jpyusd H_eurusd_chfusd

********************************************************************************
* ETAPA 7: Exportar resultados para CSV
********************************************************************************

display _newline(2)
display "================================================================"
display "  EXPORTANDO RESULTADOS"
display "================================================================"

* --- 7a: Exportar parametros ---
capture file close fh
file open fh using "../outputs/stata_dcc_parameters.csv", write replace

* Cabecalho
file write fh "parameter,value" _newline

* Parametros DCC
file write fh "lambda1," (lambda1) _newline
file write fh "lambda2," (lambda2) _newline
file write fh "persistence," (persistence_dcc) _newline

* Parametros GARCH individuais
foreach var in eurusd gbpusd jpyusd chfusd {
    file write fh "omega_`var'," (omega_`var') _newline
    file write fh "alpha_`var'," (alpha_`var') _newline
    file write fh "beta_`var'," (beta_`var') _newline
}

* Criterios de informacao
file write fh "aic_ccc," (aic_ccc) _newline
file write fh "bic_ccc," (bic_ccc) _newline
file write fh "ll_ccc," (ll_ccc) _newline
file write fh "npar_ccc," (npar_ccc) _newline
file write fh "aic_dcc," (aic_dcc) _newline
file write fh "bic_dcc," (bic_dcc) _newline
file write fh "ll_dcc," (ll_dcc) _newline
file write fh "npar_dcc," (npar_dcc) _newline

file close fh
display "Parametros exportados para: ../outputs/stata_dcc_parameters.csv"

* --- 7b: Exportar covariancias condicionais ---
* Exportar serie temporal de variancias/covariancias condicionais
preserve

* Manter apenas as variaveis relevantes
keep t H_*

* Exportar
export delimited using "../outputs/stata_dcc_conditional_covariances.csv", replace

display "Covariancias exportadas para: ../outputs/stata_dcc_conditional_covariances.csv"

restore

* --- 7c: Exportar correlacoes condicionais ---
* Calcular correlacoes a partir das covariancias: rho_ij = H_ij / sqrt(H_ii * H_jj)
gen rho_eurusd_gbpusd = H_eurusd_gbpusd / sqrt(H_eurusd_eurusd * H_gbpusd_gbpusd)
gen rho_eurusd_jpyusd = H_eurusd_jpyusd / sqrt(H_eurusd_eurusd * H_jpyusd_jpyusd)
gen rho_eurusd_chfusd = H_eurusd_chfusd / sqrt(H_eurusd_eurusd * H_chfusd_chfusd)
gen rho_gbpusd_jpyusd = H_gbpusd_jpyusd / sqrt(H_gbpusd_gbpusd * H_jpyusd_jpyusd)
gen rho_gbpusd_chfusd = H_gbpusd_chfusd / sqrt(H_gbpusd_gbpusd * H_chfusd_chfusd)
gen rho_jpyusd_chfusd = H_jpyusd_chfusd / sqrt(H_jpyusd_jpyusd * H_chfusd_chfusd)

* Resumo das correlacoes dinamicas
summarize rho_*

preserve
keep t rho_*
export delimited using "../outputs/stata_dcc_conditional_correlations.csv", replace
display "Correlacoes exportadas para: ../outputs/stata_dcc_conditional_correlations.csv"
restore

********************************************************************************
* RESUMO FINAL
********************************************************************************

display _newline(3)
display "================================================================"
display "  RESUMO - VALIDACAO DCC-GARCH"
display "================================================================"
display _newline
display "Dados: fx_majors.csv (4 series FX, " _N " obs)"
display _newline
display "CCC-GARCH(1,1):"
display "  Log-Likelihood: " ll_ccc
display "  AIC:            " aic_ccc
display "  BIC:            " bic_ccc
display _newline
display "DCC-GARCH(1,1):"
display "  Log-Likelihood: " ll_dcc
display "  AIC:            " aic_dcc
display "  BIC:            " bic_dcc
display "  lambda1 (a):    " lambda1
display "  lambda2 (b):    " lambda2
display "  Persistencia:   " persistence_dcc
display _newline
display "Arquivos gerados:"
display "  ../outputs/stata_dcc_parameters.csv"
display "  ../outputs/stata_dcc_conditional_covariances.csv"
display "  ../outputs/stata_dcc_conditional_correlations.csv"
display _newline
display "Use estes resultados para comparar com archbox (Python)."
display "================================================================"

log close
exit
