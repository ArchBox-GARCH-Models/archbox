*==============================================================================
* Validacao Cruzada: Markov-Switching - archbox vs Stata
*==============================================================================
* Este script estima modelos Markov-Switching usando o comando `mswitch`
* nativo do Stata (versao 14+). Os resultados sao exportados para CSV
* para comparacao com os obtidos pela biblioteca archbox (Python) e R.
*
* Modelos estimados:
*   1. MS(2) sem AR - Dynamic Regression com variancia regime-dependente
*   2. MS(2)-AR(1) - Autoregressive com 2 estados e variancia variavel
*
* Dataset: us_gdp_growth.csv (crescimento trimestral do PIB dos EUA)
*
* Uso: stata -b do validation_03_ms.do
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
* PARTE 1: Importar dados e configurar serie temporal
*==============================================================================

display _newline(2)
display "============================================================"
display "  VALIDACAO MARKOV-SWITCHING - PIB EUA"
display "============================================================"

*----------------------------------------------------------------------
* 1.1 Importar us_gdp_growth.csv e configurar tsset
*----------------------------------------------------------------------

* Importar CSV com crescimento do PIB
import delimited "`data_dir'/us_gdp_growth.csv", clear

* Criar variavel de tempo sequencial para tsset
* (usamos indice numerico pois os dados ja estao ordenados por data)
gen t = _n
tsset t

* Resumo descritivo da serie
display _newline
display "--- Estatisticas Descritivas: GDP Growth ---"
summarize gdp_growth, detail

* Numero de observacoes
scalar nobs = r(N)
display "Observacoes: " nobs

*==============================================================================
* PARTE 2: MS(2) sem AR - Dynamic Regression
*==============================================================================

display _newline(2)
display "============================================================"
display "  MODELO 1: MS(2) - Dynamic Regression"
display "============================================================"

*----------------------------------------------------------------------
* 2.1 Estimar MS(2) com `mswitch dr`
*----------------------------------------------------------------------

* mswitch dr: Markov-Switching Dynamic Regression
* states(2): dois regimes (ex: recessao e expansao)
* varswitch: variancia pode diferir entre regimes
* O modelo estima:
*   - Media condicional por regime: mu_1, mu_2
*   - Variancia por regime: sigma^2_1, sigma^2_2
*   - Matriz de transicao: p11, p12, p21, p22
mswitch dr gdp_growth, states(2) varswitch
estimates store ms2_dr

* Salvar estatisticas de ajuste do modelo DR
scalar ll_dr  = e(ll)
scalar aic_dr = e(aic)
scalar bic_dr = e(bic)

display _newline
display "--- MS(2) DR - Estatisticas de Ajuste ---"
display "Log-Likelihood: " ll_dr
display "AIC:            " aic_dr
display "BIC:            " bic_dr

*----------------------------------------------------------------------
* 2.2 Matriz de transicao e duracao esperada
*----------------------------------------------------------------------

* Matriz de transicao estimada
* p_ij = P(S_t = j | S_{t-1} = i)
* Mostra as probabilidades de transicao entre regimes
display _newline
display "--- Matriz de Transicao ---"
estat transition

* Duracao esperada de cada regime
* D_i = 1 / (1 - p_ii)
* Indica quantos periodos em media o processo permanece em cada regime
display _newline
display "--- Duracao Esperada dos Regimes ---"
estat duration

*----------------------------------------------------------------------
* 2.3 Extrair parametros do modelo DR
*----------------------------------------------------------------------

* Media por regime
* State1:_cons e State2:_cons sao as medias condicionais
scalar mu1_dr = _b[State1:_cons]
scalar mu2_dr = _b[State2:_cons]

* Desvio padrao por regime (log-parametrizacao no Stata)
* O Stata parametriza ln(sigma) na equacao Sigma
* sigma = exp(ln_sigma), entao sigma^2 = exp(2 * ln_sigma)
scalar lnsigma1_dr = _b[Sigma:State1:_cons]
scalar lnsigma2_dr = _b[Sigma:State2:_cons]
scalar sigma1_dr = exp(lnsigma1_dr)
scalar sigma2_dr = exp(lnsigma2_dr)

* Probabilidades de transicao
* p11 e p21 sao parametrizadas via logit no Stata
* Extraimos os valores transformados da matriz e(b)
matrix trans_dr = e(b)

display _newline
display "--- MS(2) DR - Parametros por Regime ---"
display "Regime 1 (baixo crescimento/recessao):"
display "  mu_1    = " mu1_dr
display "  sigma_1 = " sigma1_dr
display "Regime 2 (alto crescimento/expansao):"
display "  mu_2    = " mu2_dr
display "  sigma_2 = " sigma2_dr

*==============================================================================
* PARTE 3: MS(2)-AR(1) - Autoregressive
*==============================================================================

display _newline(2)
display "============================================================"
display "  MODELO 2: MS(2)-AR(1)"
display "============================================================"

*----------------------------------------------------------------------
* 3.1 Estimar MS(2)-AR(1) com `mswitch ar`
*----------------------------------------------------------------------

* mswitch ar: Markov-Switching Autoregressive
* ar(1): componente autoregressivo de ordem 1
* states(2): dois regimes
* varswitch: variancia regime-dependente
* O modelo estima:
*   - Media por regime: mu_1, mu_2
*   - Coeficiente AR(1): phi (comum entre regimes)
*   - Variancia por regime: sigma^2_1, sigma^2_2
*   - Matriz de transicao
mswitch ar gdp_growth, ar(1) states(2) varswitch
estimates store ms2_ar1

* Salvar estatisticas de ajuste do modelo AR
scalar ll_ar  = e(ll)
scalar aic_ar = e(aic)
scalar bic_ar = e(bic)

display _newline
display "--- MS(2)-AR(1) - Estatisticas de Ajuste ---"
display "Log-Likelihood: " ll_ar
display "AIC:            " aic_ar
display "BIC:            " bic_ar

*----------------------------------------------------------------------
* 3.2 Matriz de transicao e duracao esperada
*----------------------------------------------------------------------

display _newline
display "--- Matriz de Transicao ---"
estat transition

display _newline
display "--- Duracao Esperada dos Regimes ---"
estat duration

*----------------------------------------------------------------------
* 3.3 Extrair parametros do modelo AR
*----------------------------------------------------------------------

* Media por regime
scalar mu1_ar = _b[State1:_cons]
scalar mu2_ar = _b[State2:_cons]

* Coeficiente AR(1)
scalar phi1_ar = _b[gdp_growth:L1.gdp_growth]

* Desvio padrao por regime
scalar lnsigma1_ar = _b[Sigma:State1:_cons]
scalar lnsigma2_ar = _b[Sigma:State2:_cons]
scalar sigma1_ar = exp(lnsigma1_ar)
scalar sigma2_ar = exp(lnsigma2_ar)

display _newline
display "--- MS(2)-AR(1) - Parametros por Regime ---"
display "Regime 1 (baixo crescimento/recessao):"
display "  mu_1    = " mu1_ar
display "  sigma_1 = " sigma1_ar
display "Regime 2 (alto crescimento/expansao):"
display "  mu_2    = " mu2_ar
display "  sigma_2 = " sigma2_ar
display "AR(1) coeficiente:"
display "  phi_1   = " phi1_ar

*----------------------------------------------------------------------
* 3.4 Probabilidades suavizadas
*----------------------------------------------------------------------

* Predizer probabilidades suavizadas (smoothed) para cada regime
* smethod(smooth): usa informacao de toda a amostra (Kim smoother)
* state(1): probabilidade de estar no regime 1
* state(2): probabilidade de estar no regime 2
predict double pr1, pr smethod(smooth) state(1)
predict double pr2, pr smethod(smooth) state(2)

display _newline
display "--- Probabilidades Suavizadas (primeiras 10 obs) ---"
list t gdp_growth pr1 pr2 in 1/10, clean

* Estatisticas das probabilidades suavizadas
display _newline
display "--- Estatisticas das Probabilidades Suavizadas ---"
summarize pr1 pr2

*==============================================================================
* PARTE 4: Comparacao de Modelos
*==============================================================================

display _newline(2)
display "============================================================"
display "  COMPARACAO DE MODELOS"
display "============================================================"

* Tabela comparativa AIC/BIC
estimates stats ms2_dr ms2_ar1

display _newline
display "--- Comparacao Direta ---"
display "MS(2) DR:     AIC=" aic_dr  "  BIC=" bic_dr  "  LL=" ll_dr
display "MS(2)-AR(1):  AIC=" aic_ar  "  BIC=" bic_ar  "  LL=" ll_ar

*==============================================================================
* PARTE 5: Exportar Resultados
*==============================================================================

display _newline(2)
display "============================================================"
display "  EXPORTANDO RESULTADOS"
display "============================================================"

*----------------------------------------------------------------------
* 5.1 Exportar parametros por regime para CSV
*----------------------------------------------------------------------

* Salvar dados atuais para restaurar depois
preserve

* Criar dataset com parametros de ambos os modelos
clear
set obs 4

gen str20 model = ""
gen int regime = .
gen double mu = .
gen double sigma = .
gen double phi = .
gen double loglik = .
gen double aic = .
gen double bic = .

* MS(2) DR - Regime 1
replace model  = "MS(2)-DR" in 1
replace regime = 1 in 1
replace mu     = mu1_dr in 1
replace sigma  = sigma1_dr in 1
replace phi    = . in 1
replace loglik = ll_dr in 1
replace aic    = aic_dr in 1
replace bic    = bic_dr in 1

* MS(2) DR - Regime 2
replace model  = "MS(2)-DR" in 2
replace regime = 2 in 2
replace mu     = mu2_dr in 2
replace sigma  = sigma2_dr in 2
replace phi    = . in 2
replace loglik = ll_dr in 2
replace aic    = aic_dr in 2
replace bic    = bic_dr in 2

* MS(2)-AR(1) - Regime 1
replace model  = "MS(2)-AR(1)" in 3
replace regime = 1 in 3
replace mu     = mu1_ar in 3
replace sigma  = sigma1_ar in 3
replace phi    = phi1_ar in 3
replace loglik = ll_ar in 3
replace aic    = aic_ar in 3
replace bic    = bic_ar in 3

* MS(2)-AR(1) - Regime 2
replace model  = "MS(2)-AR(1)" in 4
replace regime = 2 in 4
replace mu     = mu2_ar in 4
replace sigma  = sigma2_ar in 4
replace phi    = phi1_ar in 4
replace loglik = ll_ar in 4
replace aic    = aic_ar in 4
replace bic    = bic_ar in 4

* Listar tabela no log
display _newline
display "--- Tabela de Resultados ---"
list, clean noobs

* Exportar para CSV
export delimited "`output_dir'/stata_validation_ms_results.csv", replace

display _newline
display "Parametros exportados para: `output_dir'/stata_validation_ms_results.csv"

restore

*----------------------------------------------------------------------
* 5.2 Exportar probabilidades suavizadas para CSV
*----------------------------------------------------------------------

* Exportar serie completa de probabilidades para comparacao visual
preserve
keep t gdp_growth pr1 pr2
export delimited "`output_dir'/stata_ms_smoothed_probabilities.csv", replace
display "Probabilidades suavizadas exportadas para: `output_dir'/stata_ms_smoothed_probabilities.csv"
restore

*==============================================================================
* RESUMO FINAL
*==============================================================================

display _newline(2)
display "============================================================"
display "  VALIDACAO MARKOV-SWITCHING CONCLUIDA"
display "============================================================"
display "Modelos estimados:"
display "  1. MS(2) Dynamic Regression (mswitch dr)"
display "  2. MS(2)-AR(1) (mswitch ar)"
display ""
display "Arquivos gerados em `output_dir'/:"
display "  - stata_validation_ms_results.csv (parametros por regime)"
display "  - stata_ms_smoothed_probabilities.csv (prob. suavizadas)"
display ""
display "Para comparacao com archbox e R:"
display "  - Verificar medias por regime (mu_1, mu_2)"
display "  - Verificar desvios padrao por regime (sigma_1, sigma_2)"
display "  - Verificar probabilidades de transicao (p11, p22)"
display "  - Verificar coeficiente AR(1) no modelo MS-AR"
display "  - Comparar probabilidades suavizadas visualmente"
display "============================================================"

* Fim do script
exit
