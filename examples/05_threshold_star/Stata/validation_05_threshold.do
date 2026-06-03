*==============================================================================
* Validacao Cruzada: Modelos Threshold (SETAR) - archbox vs Stata
*==============================================================================
* Este script estima um modelo SETAR (Self-Exciting Threshold Autoregressive)
* usando grid search manual sobre o valor do threshold. O Stata nao possui
* comando nativo para SETAR, entao a estimacao e feita via regressoes
* condicionais (reg ... if lag1 <= c / lag1 > c) para cada candidato c.
*
* Alem disso, implementa um teste de nao-linearidade tipo Tsay, usando
* termos quadraticos e cubicos do lag como regressores auxiliares.
*
* Dataset: us_gdp_growth.csv (crescimento trimestral do PIB dos EUA, sintetico)
* Colunas: date, y, true_regime
*
* Uso: stata -b do validation_05_threshold.do
*==============================================================================

clear all
set more off
set seed 42

* Diretorios relativos ao local deste script
local data_dir "../data"
local output_dir "../outputs"

* Criar diretorio de output se nao existir
capture mkdir "`output_dir'"

display _newline(2)
display "============================================================"
display "  VALIDACAO THRESHOLD (SETAR) - US GDP GROWTH"
display "============================================================"

*==============================================================================
* PARTE 1: Importar dados e configurar serie temporal
*==============================================================================

* Importar CSV com crescimento do PIB
import delimited "`data_dir'/us_gdp_growth.csv", clear

* Criar variavel de tempo sequencial e declarar como serie temporal
gen t = _n
tsset t

* Gerar lag da variavel dependente (variavel de threshold)
gen lag1 = L.y

* Resumo descritivo
display _newline
display "--- Estatisticas Descritivas de y ---"
summarize y, detail

display _newline
display "--- Estatisticas Descritivas de lag1 (L.y) ---"
summarize lag1, detail

* Salvar percentis do lag para definir grid de busca
* Usamos trim de 15% para garantir observacoes suficientes em cada regime
quietly summarize lag1, detail
local p15 = r(p10)
local p85 = r(p90)
local lag_min = r(min)
local lag_max = r(max)

display _newline
display "Range do lag1: [`lag_min', `lag_max']"
display "Grid search entre percentis 10-90: [`p15', `p85']"

* Numero de observacoes validas (sem missing do lag)
quietly count if !missing(lag1)
local nobs_valid = r(N)
display "Observacoes validas (sem missing): `nobs_valid'"

*==============================================================================
* PARTE 2: Grid search para encontrar threshold otimo (SETAR)
*==============================================================================

display _newline(2)
display "============================================================"
display "  GRID SEARCH - THRESHOLD OTIMO"
display "============================================================"

* Estrategia: testar cada valor candidato c no grid e estimar duas
* regressoes lineares separadas (regime baixo: lag1 <= c, regime alto: lag1 > c).
* O threshold otimo minimiza a soma dos RSS (Residual Sum of Squares) dos
* dois regimes. Isso equivale ao estimador de minimos quadrados concentrados.

* Inicializar variaveis para rastrear o melhor threshold
local best_rss = 1e20
local best_c = 0
local best_rss1 = .
local best_rss2 = .
local best_n1 = 0
local best_n2 = 0

* Definir grid: de -2 a 2 com passo de 0.1 (cobre faixa tipica do PIB)
* O trim implicito e garantido pelo capture: se um regime tiver <2 obs,
* a regressao falha e o candidato e ignorado.
forvalues c = -2(0.1)2 {
    capture {
        * Regime 1 (baixo): observacoes onde lag1 <= threshold candidato
        quietly reg y lag1 if lag1 <= `c' & !missing(lag1)
        scalar rss1 = e(rss)
        local n1 = e(N)

        * Regime 2 (alto): observacoes onde lag1 > threshold candidato
        quietly reg y lag1 if lag1 > `c' & !missing(lag1)
        scalar rss2 = e(rss)
        local n2 = e(N)

        * RSS total = soma dos RSS de ambos os regimes
        scalar rss_total = rss1 + rss2

        * Atualizar melhor threshold se RSS total for menor
        if rss_total < `best_rss' {
            local best_rss = rss_total
            local best_c = `c'
            local best_rss1 = rss1
            local best_rss2 = rss2
            local best_n1 = `n1'
            local best_n2 = `n2'
        }
    }
}

display _newline
display "--- Resultado do Grid Search ---"
display "Threshold otimo: `best_c'"
display "RSS Regime 1 (lag1 <= `best_c'): `best_rss1'"
display "RSS Regime 2 (lag1 >  `best_c'): `best_rss2'"
display "RSS Total:                        `best_rss'"
display "N obs Regime 1: `best_n1'"
display "N obs Regime 2: `best_n2'"

*==============================================================================
* PARTE 3: Estimar regressoes por regime no threshold otimo
*==============================================================================

display _newline(2)
display "============================================================"
display "  ESTIMACAO POR REGIME - THRESHOLD = `best_c'"
display "============================================================"

*----------------------------------------------------------------------
* 3.1 Regime 1: Abaixo do threshold (lag1 <= c)
*----------------------------------------------------------------------

display _newline
display "--- Regime 1: lag1 <= `best_c' ---"

reg y lag1 if lag1 <= `best_c' & !missing(lag1)
estimates store regime1

* Extrair parametros do Regime 1
* intercepto (constante) e coeficiente AR (phi)
scalar intercept_r1 = _b[_cons]
scalar phi_r1 = _b[lag1]
scalar rss_r1 = e(rss)
scalar rmse_r1 = e(rmse)
scalar r2_r1 = e(r2)
scalar nobs_r1 = e(N)

display _newline
display "Intercepto (Regime 1): " intercept_r1
display "Phi (Regime 1):        " phi_r1
display "RSS (Regime 1):        " rss_r1
display "RMSE (Regime 1):       " rmse_r1
display "R2 (Regime 1):         " r2_r1
display "N obs (Regime 1):      " nobs_r1

*----------------------------------------------------------------------
* 3.2 Regime 2: Acima do threshold (lag1 > c)
*----------------------------------------------------------------------

display _newline
display "--- Regime 2: lag1 > `best_c' ---"

reg y lag1 if lag1 > `best_c' & !missing(lag1)
estimates store regime2

* Extrair parametros do Regime 2
scalar intercept_r2 = _b[_cons]
scalar phi_r2 = _b[lag1]
scalar rss_r2 = e(rss)
scalar rmse_r2 = e(rmse)
scalar r2_r2 = e(r2)
scalar nobs_r2 = e(N)

display _newline
display "Intercepto (Regime 2): " intercept_r2
display "Phi (Regime 2):        " phi_r2
display "RSS (Regime 2):        " rss_r2
display "RMSE (Regime 2):       " rmse_r2
display "R2 (Regime 2):         " r2_r2
display "N obs (Regime 2):      " nobs_r2

*----------------------------------------------------------------------
* 3.3 Modelo linear (sem threshold) para comparacao
*----------------------------------------------------------------------

display _newline
display "--- Modelo Linear (sem threshold) ---"

reg y lag1 if !missing(lag1)
estimates store linear

scalar intercept_lin = _b[_cons]
scalar phi_lin = _b[lag1]
scalar rss_lin = e(rss)
scalar rmse_lin = e(rmse)
scalar r2_lin = e(r2)
scalar nobs_lin = e(N)
scalar ll_lin = e(ll)

display _newline
display "Intercepto (Linear): " intercept_lin
display "Phi (Linear):        " phi_lin
display "RSS (Linear):        " rss_lin
display "RMSE (Linear):       " rmse_lin
display "R2 (Linear):         " r2_lin

*----------------------------------------------------------------------
* 3.4 Comparacao de modelos: RSS e F-test informal
*----------------------------------------------------------------------

display _newline(2)
display "============================================================"
display "  COMPARACAO: LINEAR vs SETAR"
display "============================================================"

* RSS do SETAR = soma dos RSS dos dois regimes
scalar rss_setar = rss_r1 + rss_r2

* Graus de liberdade
* Linear: N - 2 (intercepto + phi)
* SETAR: N - 4 (2 interceptos + 2 phis)
* Restricoes testadas: 2 (igualdade de intercepto e phi entre regimes)
scalar df_linear = nobs_lin - 2
scalar df_setar = nobs_lin - 4
scalar df_diff = 2

* F-statistic (nota: nao e o teste de Hansen exato, mas uma aproximacao)
* F = [(RSS_restrito - RSS_irrestrito) / q] / [RSS_irrestrito / (N - k)]
scalar f_stat = ((rss_lin - rss_setar) / df_diff) / (rss_setar / df_setar)

display "RSS Linear:       " rss_lin
display "RSS SETAR:         " rss_setar
display "Reducao RSS:       " rss_lin - rss_setar
display "F-statistic:       " f_stat
display "df numerador:      " df_diff
display "df denominador:    " df_setar

* Calcular AIC e BIC manualmente para o SETAR
* k_setar = 4 parametros (2 interceptos + 2 phis) + 1 threshold + 2 variancias = 5
* Usamos aproximacao: AIC = N*ln(RSS/N) + 2*k
scalar k_setar = 5
scalar k_linear = 2
scalar aic_setar = nobs_lin * ln(rss_setar / nobs_lin) + 2 * k_setar
scalar bic_setar = nobs_lin * ln(rss_setar / nobs_lin) + k_setar * ln(nobs_lin)
scalar aic_linear = nobs_lin * ln(rss_lin / nobs_lin) + 2 * k_linear
scalar bic_linear = nobs_lin * ln(rss_lin / nobs_lin) + k_linear * ln(nobs_lin)

display _newline
display "--- Criterios de Informacao ---"
display "AIC Linear: " aic_linear
display "BIC Linear: " bic_linear
display "AIC SETAR:  " aic_setar
display "BIC SETAR:  " bic_setar

*==============================================================================
* PARTE 4: Teste de nao-linearidade (Tsay-like)
*==============================================================================

display _newline(2)
display "============================================================"
display "  TESTE DE NAO-LINEARIDADE"
display "============================================================"

* Regressao auxiliar com termos quadraticos e cubicos do lag
* Se os termos nao-lineares forem significativos, ha evidencia de
* nao-linearidade na relacao entre y e lag1.
* H0: modelo linear e adequado (coeficientes quadratico e cubico = 0)
* H1: existe nao-linearidade

gen lag1_sq = lag1^2
gen lag1_cu = lag1^3

display _newline
display "--- Regressao Auxiliar: y = b0 + b1*lag1 + b2*lag1^2 + b3*lag1^3 ---"
reg y lag1 lag1_sq lag1_cu if !missing(lag1)

* Teste F conjunto para os termos nao-lineares
display _newline
display "--- Teste F: H0: coeficientes de lag1^2 e lag1^3 = 0 ---"
test lag1_sq lag1_cu

* Salvar resultados do teste
scalar f_nonlin = r(F)
scalar p_nonlin = r(p)
scalar df_nonlin = r(df)

display _newline
display "F-statistic (nao-linearidade): " f_nonlin
display "p-valor:                        " p_nonlin
display "Graus de liberdade:             " df_nonlin

* Interpretacao
if p_nonlin < 0.05 {
    display "Resultado: Rejeita H0 a 5% -> Evidencia de nao-linearidade"
}
else {
    display "Resultado: Nao rejeita H0 a 5% -> Sem evidencia de nao-linearidade"
}

*==============================================================================
* PARTE 5: Exportar resultados para CSV
*==============================================================================

display _newline(2)
display "============================================================"
display "  EXPORTANDO RESULTADOS"
display "============================================================"

*----------------------------------------------------------------------
* 5.1 Exportar parametros dos regimes
*----------------------------------------------------------------------

preserve
clear
set obs 3

gen str20 model = ""
gen double intercept = .
gen double phi = .
gen double rss = .
gen double rmse = .
gen double r2 = .
gen double nobs = .
gen double aic = .
gen double bic = .

* Modelo linear (benchmark)
replace model     = "Linear" in 1
replace intercept = intercept_lin in 1
replace phi       = phi_lin in 1
replace rss       = rss_lin in 1
replace rmse      = rmse_lin in 1
replace r2        = r2_lin in 1
replace nobs      = nobs_lin in 1
replace aic       = aic_linear in 1
replace bic       = bic_linear in 1

* SETAR Regime 1
replace model     = "SETAR_Regime1" in 2
replace intercept = intercept_r1 in 2
replace phi       = phi_r1 in 2
replace rss       = rss_r1 in 2
replace rmse      = rmse_r1 in 2
replace r2        = r2_r1 in 2
replace nobs      = nobs_r1 in 2
replace aic       = . in 2
replace bic       = . in 2

* SETAR Regime 2
replace model     = "SETAR_Regime2" in 3
replace intercept = intercept_r2 in 3
replace phi       = phi_r2 in 3
replace rss       = rss_r2 in 3
replace rmse      = rmse_r2 in 3
replace r2        = r2_r2 in 3
replace nobs      = nobs_r2 in 3
replace aic       = . in 3
replace bic       = . in 3

list, clean noobs

export delimited "`output_dir'/stata_validation_threshold_params.csv", replace
display "Parametros exportados para: `output_dir'/stata_validation_threshold_params.csv"

restore

*----------------------------------------------------------------------
* 5.2 Exportar resumo do modelo SETAR
*----------------------------------------------------------------------

preserve
clear
set obs 1

gen double threshold = `best_c'
gen double rss_regime1 = `best_rss1'
gen double rss_regime2 = `best_rss2'
gen double rss_setar = `best_rss'
gen double rss_linear = rss_lin
gen double f_stat_linear_vs_setar = f_stat
gen double intercept_regime1 = intercept_r1
gen double phi_regime1 = phi_r1
gen double intercept_regime2 = intercept_r2
gen double phi_regime2 = phi_r2
gen double nobs_regime1 = `best_n1'
gen double nobs_regime2 = `best_n2'
gen double aic_setar_val = aic_setar
gen double bic_setar_val = bic_setar
gen double aic_linear_val = aic_linear
gen double bic_linear_val = bic_linear

list, clean noobs

export delimited "`output_dir'/stata_validation_threshold_summary.csv", replace
display "Resumo SETAR exportado para: `output_dir'/stata_validation_threshold_summary.csv"

restore

*----------------------------------------------------------------------
* 5.3 Exportar resultados do teste de nao-linearidade
*----------------------------------------------------------------------

preserve
clear
set obs 1

gen str30 test_name = "Tsay_nonlinearity"
gen double f_statistic = f_nonlin
gen double p_value = p_nonlin
gen double df_test = df_nonlin
gen str10 reject_5pct = ""
replace reject_5pct = "Yes" if f_nonlin > 0 & p_nonlin < 0.05
replace reject_5pct = "No"  if f_nonlin > 0 & p_nonlin >= 0.05

list, clean noobs

export delimited "`output_dir'/stata_validation_threshold_nonlinearity.csv", replace
display "Teste de nao-linearidade exportado para: `output_dir'/stata_validation_threshold_nonlinearity.csv"

restore

*==============================================================================
* RESUMO FINAL
*==============================================================================

display _newline(2)
display "============================================================"
display "  RESUMO DA VALIDACAO THRESHOLD (SETAR)"
display "============================================================"
display _newline
display "Threshold otimo (grid search): `best_c'"
display _newline
display "--- Regime 1 (lag1 <= `best_c') ---"
display "  Intercepto: " intercept_r1
display "  Phi:        " phi_r1
display "  N obs:      " nobs_r1
display "  RSS:        " rss_r1
display _newline
display "--- Regime 2 (lag1 > `best_c') ---"
display "  Intercepto: " intercept_r2
display "  Phi:        " phi_r2
display "  N obs:      " nobs_r2
display "  RSS:        " rss_r2
display _newline
display "RSS Total (SETAR): " rss_setar
display "RSS (Linear):      " rss_lin
display "F-stat (Lin vs SETAR): " f_stat
display _newline
display "Teste nao-linearidade: F = " f_nonlin " (p = " p_nonlin ")"
display _newline
display "============================================================"
display "  VALIDACAO CONCLUIDA"
display "============================================================"
display "Arquivos gerados em `output_dir'/:"
display "  - stata_validation_threshold_params.csv"
display "  - stata_validation_threshold_summary.csv"
display "  - stata_validation_threshold_nonlinearity.csv"
display "============================================================"

* Fim do script
exit
