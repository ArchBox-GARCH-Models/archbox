********************************************************************************
* full_comparison.do
* Validacao Completa: Modelos Univariados e Multivariados com Stata
*
* Descricao:
*   Script abrangente que estima modelos GARCH(1,1), EGARCH(1,1) e GJR-GARCH(1,1)
*   em retornos do SP500, realiza diagnosticos (ARCH-LM, Ljung-Box), calcula
*   VaR parametrico, estima DCC multivariado em series FX e exporta resultados
*   em CSV para comparacao automatizada com a biblioteca archbox (Python).
*
* Dados:
*   - sp500_returns.csv: retornos diarios do SP500 (coluna: returns)
*   - fx_majors.csv: retornos diarios de 4 pares FX (eurusd, gbpusd, jpyusd, chfusd)
*
* Uso:
*   stata -b do full_comparison.do
*
* Autor: archbox validation suite
* Data: 2026
********************************************************************************

clear all
set more off
set seed 42

* Definir diretorios relativos ao local deste script
local data_dir "../data"
local output_dir "../outputs"

* Criar diretorio de saida caso nao exista
capture mkdir "`output_dir'"

********************************************************************************
* SECAO 1: MODELOS UNIVARIADOS NO SP500
* Estimamos tres especificacoes de volatilidade condicional:
*   - GARCH(1,1): modelo simetrico padrao (Bollerslev, 1986)
*   - EGARCH(1,1): modelo exponencial assimetrico (Nelson, 1991)
*   - GJR-GARCH(1,1): modelo com threshold assimetrico (Glosten et al., 1993)
* Para cada modelo extraimos AIC, BIC e log-likelihood.
********************************************************************************

display _newline
display as text "============================================================"
display as text " SECAO 1: Estimacao de Modelos Univariados - SP500"
display as text "============================================================"

* --- Importar dados do SP500 ---
import delimited "`data_dir'/sp500_returns.csv", clear
display as text "Numero de observacoes SP500: " _N

* Criar variavel de tempo para declarar serie temporal
gen t = _n
tsset t

* --- Modelo 1: GARCH(1,1) com distribuicao Normal ---
* O modelo GARCH(1,1) captura a persistencia na variancia condicional
* sigma2_t = omega + alpha * epsilon2_{t-1} + beta * sigma2_{t-1}
display _newline
display as text "--- Estimando GARCH(1,1) ---"
arch returns, arch(1) garch(1) distribution(normal)
estimates store garch11

* Extrair criterios de informacao e log-likelihood
scalar aic_garch = e(aic)
scalar bic_garch = e(bic)
scalar ll_garch = e(ll)

display as text "GARCH(1,1) - AIC: " aic_garch " | BIC: " bic_garch " | LogLik: " ll_garch

* --- Modelo 2: EGARCH(1,1) com distribuicao Normal ---
* O modelo EGARCH captura assimetria no impacto de choques sobre a volatilidade
* Choques negativos (bad news) tipicamente aumentam mais a volatilidade que
* choques positivos de mesma magnitude (efeito leverage)
* ln(sigma2_t) = omega + alpha * g(z_{t-1}) + beta * ln(sigma2_{t-1})
display _newline
display as text "--- Estimando EGARCH(1,1) ---"
arch returns, earch(1) egarch(1) distribution(normal)
estimates store egarch11

scalar aic_egarch = e(aic)
scalar bic_egarch = e(bic)
scalar ll_egarch = e(ll)

display as text "EGARCH(1,1) - AIC: " aic_egarch " | BIC: " bic_egarch " | LogLik: " ll_egarch

* --- Modelo 3: GJR-GARCH(1,1) com distribuicao Normal ---
* O modelo GJR (ou TARCH) adiciona um termo indicador para choques negativos
* sigma2_t = omega + (alpha + gamma * I_{t-1}) * epsilon2_{t-1} + beta * sigma2_{t-1}
* onde I_{t-1} = 1 se epsilon_{t-1} < 0
display _newline
display as text "--- Estimando GJR-GARCH(1,1) ---"
arch returns, arch(1) garch(1) tarch(1) distribution(normal)
estimates store gjr11

scalar aic_gjr = e(aic)
scalar bic_gjr = e(bic)
scalar ll_gjr = e(ll)

display as text "GJR-GARCH(1,1) - AIC: " aic_gjr " | BIC: " bic_gjr " | LogLik: " ll_gjr

* --- Comparacao formal entre os tres modelos ---
* O comando estimates stats apresenta AIC e BIC lado a lado
display _newline
display as text "--- Comparacao de Modelos (estimates stats) ---"
estimates stats garch11 egarch11 gjr11

********************************************************************************
* SECAO 2: DIAGNOSTICOS POS-ESTIMACAO
* Apos a estimacao, verificamos a adequacao do modelo GARCH(1,1):
*   - Teste ARCH-LM: verifica se ainda ha efeitos ARCH nos residuos
*     H0: nao ha efeitos ARCH remanescentes
*   - Teste Ljung-Box nos residuos padronizados: verifica autocorrelacao
*     H0: residuos padronizados sao ruido branco
********************************************************************************

display _newline
display as text "============================================================"
display as text " SECAO 2: Diagnosticos Pos-Estimacao"
display as text "============================================================"

* Re-estimar o GARCH(1,1) para gerar predicoes e residuos
quietly arch returns, arch(1) garch(1) distribution(normal)

* --- Teste ARCH-LM ---
* Testamos com lags 1, 5 e 10 para capturar dependencia em diferentes horizontes
* Se p-valor > 0.05, nao rejeitamos H0: o modelo capturou os efeitos ARCH
display _newline
display as text "--- Teste ARCH-LM (lags 1, 5, 10) ---"
estat archlm, lags(1 5 10)

* --- Calcular residuos e volatilidade condicional ---
predict double resid_garch, residuals
predict double sigma2_garch, variance

* Residuos padronizados: z_t = epsilon_t / sigma_t
* Se o modelo esta bem especificado, z_t ~ iid N(0,1)
gen double std_resid_garch = resid_garch / sqrt(sigma2_garch)

* --- Teste Ljung-Box nos residuos padronizados ---
* Verifica se os residuos padronizados apresentam autocorrelacao serial
* H0: nao ha autocorrelacao ate lag 10
display _newline
display as text "--- Teste Ljung-Box nos Residuos Padronizados (10 lags) ---"
wntestq std_resid_garch, lags(10)

* --- Estatisticas descritivas dos residuos padronizados ---
* Esperamos media proxima de 0 e desvio padrao proximo de 1
display _newline
display as text "--- Estatisticas Descritivas dos Residuos Padronizados ---"
summarize std_resid_garch, detail

********************************************************************************
* SECAO 3: VALUE-AT-RISK (VaR) PARAMETRICO
* O VaR parametrico e calculado usando a volatilidade condicional estimada
* e os quantis da distribuicao Normal:
*   VaR_alpha = z_alpha * sigma_t
* onde z_alpha e o quantil da Normal padrao ao nivel alpha.
*
* Calculamos VaR aos niveis de 95% e 99% e contamos as violacoes
* (dias em que a perda efetiva excedeu o VaR estimado).
* A taxa de violacao esperada e alpha (5% e 1%, respectivamente).
********************************************************************************

display _newline
display as text "============================================================"
display as text " SECAO 3: Value-at-Risk Parametrico"
display as text "============================================================"

* --- Calcular VaR parametrico ---
* invnormal(0.05) ≈ -1.6449 (quantil 5% da Normal padrao)
* invnormal(0.01) ≈ -2.3263 (quantil 1% da Normal padrao)
gen double var95 = invnormal(0.05) * sqrt(sigma2_garch)
gen double var99 = invnormal(0.01) * sqrt(sigma2_garch)

* --- Contar violacoes ---
* Uma violacao ocorre quando o retorno efetivo e menor que o VaR
* (ou seja, a perda excedeu o limite previsto pelo modelo)
gen viol95 = (returns < var95) if !missing(var95)
gen viol99 = (returns < var99) if !missing(var99)

* --- Resumo das violacoes ---
display _newline
display as text "--- Taxa de Violacao VaR 95% (esperada: 5%) ---"
summarize viol95
display as text "Taxa de violacao VaR 95%: " r(mean) * 100 "%"

display _newline
display as text "--- Taxa de Violacao VaR 99% (esperada: 1%) ---"
summarize viol99
display as text "Taxa de violacao VaR 99%: " r(mean) * 100 "%"

* --- Exportar serie de VaR para comparacao ---
preserve
keep t returns var95 var99 viol95 viol99 sigma2_garch std_resid_garch
export delimited "`output_dir'/stata_var_series.csv", replace
display as text "Serie de VaR exportada para: `output_dir'/stata_var_series.csv"
restore

********************************************************************************
* SECAO 4: DCC MULTIVARIADO
* O modelo DCC (Dynamic Conditional Correlation) de Engle (2002) estima
* correlacoes condicionais variantes no tempo entre multiplas series.
*
* Etapas do DCC:
*   1. Estimar GARCH(1,1) univariado para cada serie
*   2. Padronizar os residuos
*   3. Estimar a dinamica das correlacoes condicionais
*
* Utilizamos 4 series de retornos FX: EUR/USD, GBP/USD, JPY/USD, CHF/USD.
********************************************************************************

display _newline
display as text "============================================================"
display as text " SECAO 4: DCC Multivariado - Series FX"
display as text "============================================================"

* --- Importar dados FX ---
import delimited "`data_dir'/fx_majors.csv", clear
display as text "Numero de observacoes FX: " _N

* Criar variavel de tempo para declarar serie temporal
gen t = _n
tsset t

* --- Estimar DCC(1,1) ---
* O comando mgarch dcc estima simultaneamente os modelos univariados GARCH(1,1)
* e os parametros de correlacao dinamica (a e b do DCC)
* noconstant: nao incluir constante na equacao da media (retornos ja sao demeaned)
display _newline
display as text "--- Estimando DCC(1,1) com 4 series FX ---"
mgarch dcc (eurusd gbpusd jpyusd chfusd = , noconstant), arch(1) garch(1)
estimates store dcc_model

* --- Criterios de informacao do DCC ---
display _newline
display as text "--- Criterios de Informacao do DCC ---"
estat ic

* Guardar escalares do DCC
matrix ic_dcc = r(S)
scalar aic_dcc = ic_dcc[1,5]
scalar bic_dcc = ic_dcc[1,6]
scalar ll_dcc = ic_dcc[1,3]

display as text "DCC - AIC: " aic_dcc " | BIC: " bic_dcc " | LogLik: " ll_dcc

********************************************************************************
* SECAO 5: EXPORTAR RESULTADOS PARA COMPARACAO COM ARCHBOX
* Exportamos os resultados em formato CSV para permitir comparacao
* automatizada entre os resultados do Stata e da biblioteca archbox.
********************************************************************************

display _newline
display as text "============================================================"
display as text " SECAO 5: Exportacao de Resultados"
display as text "============================================================"

* --- Exportar resultados univariados ---
* Criamos um dataset com os criterios de informacao dos tres modelos
clear
set obs 3
gen str20 model = ""
gen double loglik = .
gen double aic = .
gen double bic = .

replace model = "GARCH" in 1
replace loglik = ll_garch in 1
replace aic = aic_garch in 1
replace bic = bic_garch in 1

replace model = "EGARCH" in 2
replace loglik = ll_egarch in 2
replace aic = aic_egarch in 2
replace bic = bic_egarch in 2

replace model = "GJR" in 3
replace loglik = ll_gjr in 3
replace aic = aic_gjr in 3
replace bic = bic_gjr in 3

* Listar resultados no log
display _newline
display as text "--- Tabela de Comparacao Univariada ---"
list model loglik aic bic, clean noobs

export delimited "`output_dir'/stata_full_univariate_comparison.csv", replace
display as text "Resultados univariados exportados para: `output_dir'/stata_full_univariate_comparison.csv"

* --- Exportar resultados DCC ---
* Criamos um dataset com os criterios de informacao do modelo DCC
clear
set obs 1
gen str20 model = "DCC"
gen double loglik = ll_dcc
gen double aic = aic_dcc
gen double bic = bic_dcc

export delimited "`output_dir'/stata_full_dcc_comparison.csv", replace
display as text "Resultados DCC exportados para: `output_dir'/stata_full_dcc_comparison.csv"

********************************************************************************
* RESUMO FINAL
* Este script completou as seguintes etapas:
*   1. Estimacao de GARCH(1,1), EGARCH(1,1) e GJR-GARCH(1,1) no SP500
*   2. Diagnosticos ARCH-LM e Ljung-Box nos residuos padronizados
*   3. Calculo de VaR parametrico (95% e 99%) com contagem de violacoes
*   4. Estimacao de DCC(1,1) em 4 series FX
*   5. Exportacao de todos os resultados em CSV
*
* Os CSVs gerados podem ser comparados com os resultados da biblioteca
* archbox usando o notebook de validacao cruzada.
********************************************************************************

display _newline
display as text "============================================================"
display as text " VALIDACAO STATA CONCLUIDA COM SUCESSO"
display as text "============================================================"
display as text "Arquivos gerados:"
display as text "  - `output_dir'/stata_full_univariate_comparison.csv"
display as text "  - `output_dir'/stata_full_dcc_comparison.csv"
display as text "  - `output_dir'/stata_var_series.csv"
display as text "============================================================"
