*==============================================================================
* Validation Script: GARCH Diagnostics in Stata
*
* Purpose: Validate archbox diagnostic tools against Stata's built-in
*          post-estimation diagnostics (ARCH-LM, Ljung-Box, residual analysis)
*
* Usage: stata -b do validation_diagnostics.do
*
* Reference: Engle (1982) - ARCH-LM test; Ljung & Box (1978) - portmanteau test
*==============================================================================

clear all
set more off
capture log close
log using "../outputs/validation_diagnostics.log", replace

display "=============================================="
display " GARCH Diagnostics Validation - Stata"
display " Date: $S_DATE $S_TIME"
display "=============================================="

*------------------------------------------------------------------------------
* 1. Import data and estimate GARCH(1,1)
*------------------------------------------------------------------------------

import delimited "../data/sp500_returns.csv", clear
gen t = _n
tsset t

summarize returns
display "Observations: " r(N)
display "Mean return:  " r(mean)
display "Std dev:      " r(sd)

* Estimate GARCH(1,1) with normal distribution
display _newline "=============================================="
display " Estimating GARCH(1,1) - Normal Distribution"
display "=============================================="
arch returns, arch(1) garch(1) distribution(normal)

* Store estimates
estimates store garch11

*------------------------------------------------------------------------------
* 2. ARCH-LM test for residual ARCH effects
*------------------------------------------------------------------------------

display _newline "=============================================="
display " ARCH-LM Test (Engle, 1982)"
display "=============================================="

* ARCH-LM test with lags 1, 5, 10
estat archlm, lags(1 5 10)

* Save results from the returned matrix
matrix archlm_results = r(archlm)

* Extract chi2 statistics and p-values
scalar chi2_archlm_1  = archlm_results[1, 1]
scalar df_archlm_1    = archlm_results[1, 2]
scalar p_archlm_1     = archlm_results[1, 3]

scalar chi2_archlm_5  = archlm_results[2, 1]
scalar df_archlm_5    = archlm_results[2, 2]
scalar p_archlm_5     = archlm_results[2, 3]

scalar chi2_archlm_10 = archlm_results[3, 1]
scalar df_archlm_10   = archlm_results[3, 2]
scalar p_archlm_10    = archlm_results[3, 3]

display _newline "ARCH-LM Summary:"
display "  Lag  1: chi2 = " chi2_archlm_1  " | p = " p_archlm_1
display "  Lag  5: chi2 = " chi2_archlm_5  " | p = " p_archlm_5
display "  Lag 10: chi2 = " chi2_archlm_10 " | p = " p_archlm_10

*------------------------------------------------------------------------------
* 3. Standardized residuals and Ljung-Box tests
*------------------------------------------------------------------------------

display _newline "=============================================="
display " Standardized Residuals and Ljung-Box Tests"
display "=============================================="

* Obtain residuals and conditional variance
predict double resid_garch, residuals
predict double sigma2_hat, variance

* Compute standardized residuals
gen double std_resid = resid_garch / sqrt(sigma2_hat)

* Compute squared standardized residuals
gen double std_resid_sq = std_resid^2

* Summary statistics of standardized residuals
summarize std_resid, detail
scalar mean_stdresid = r(mean)
scalar sd_stdresid   = r(sd)
scalar skew_stdresid = r(skewness)
scalar kurt_stdresid = r(kurtosis)

display _newline "Standardized Residuals Summary:"
display "  Mean:     " mean_stdresid
display "  Std Dev:  " sd_stdresid
display "  Skewness: " skew_stdresid
display "  Kurtosis: " kurt_stdresid

* Ljung-Box test on standardized residuals (lags 10 and 20)
display _newline "--- Ljung-Box: Standardized Residuals ---"
wntestq std_resid, lags(10)
scalar lb_resid_10     = r(stat)
scalar p_lb_resid_10   = r(p)

wntestq std_resid, lags(20)
scalar lb_resid_20     = r(stat)
scalar p_lb_resid_20   = r(p)

display "  Lags 10: Q = " lb_resid_10 " | p = " p_lb_resid_10
display "  Lags 20: Q = " lb_resid_20 " | p = " p_lb_resid_20

* Ljung-Box test on squared standardized residuals (lags 10 and 20)
display _newline "--- Ljung-Box: Squared Standardized Residuals ---"
wntestq std_resid_sq, lags(10)
scalar lb_sq_10     = r(stat)
scalar p_lb_sq_10   = r(p)

wntestq std_resid_sq, lags(20)
scalar lb_sq_20     = r(stat)
scalar p_lb_sq_20   = r(p)

display "  Lags 10: Q = " lb_sq_10 " | p = " p_lb_sq_10
display "  Lags 20: Q = " lb_sq_20 " | p = " p_lb_sq_20

*------------------------------------------------------------------------------
* 4. QQ-plot and histogram of standardized residuals
*------------------------------------------------------------------------------

display _newline "=============================================="
display " Graphical Diagnostics"
display "=============================================="

* QQ-plot of standardized residuals
qnorm std_resid, title("QQ-Plot: Standardized Residuals (GARCH)") ///
    note("Validation: archbox vs Stata") ///
    scheme(s2color)
graph export "../outputs/stata_qqplot.png", replace width(800)
display "  QQ-plot saved: ../outputs/stata_qqplot.png"

* Histogram with normal overlay
histogram std_resid, normal ///
    title("Histogram: Standardized Residuals (GARCH)") ///
    note("Validation: archbox vs Stata") ///
    scheme(s2color)
graph export "../outputs/stata_histogram.png", replace width(800)
display "  Histogram saved: ../outputs/stata_histogram.png"

*------------------------------------------------------------------------------
* 5. Correlogram
*------------------------------------------------------------------------------

display _newline "=============================================="
display " Correlograms"
display "=============================================="

display _newline "--- Correlogram: Standardized Residuals ---"
corrgram std_resid, lags(40)

display _newline "--- Correlogram: Squared Standardized Residuals ---"
corrgram std_resid_sq, lags(40)

*------------------------------------------------------------------------------
* 6. EGARCH and GJR-GARCH estimation + diagnostics
*------------------------------------------------------------------------------

display _newline "=============================================="
display " EGARCH(1,1) Estimation and Diagnostics"
display "=============================================="

* Drop previous predictions
drop resid_garch sigma2_hat std_resid std_resid_sq

* Estimate EGARCH(1,1)
arch returns, earch(1) egarch(1) distribution(normal)
estimates store egarch11

* ARCH-LM test for EGARCH
estat archlm, lags(1 5 10)
matrix archlm_egarch = r(archlm)

scalar chi2_egarch_1  = archlm_egarch[1, 1]
scalar p_egarch_1     = archlm_egarch[1, 3]
scalar chi2_egarch_5  = archlm_egarch[2, 1]
scalar p_egarch_5     = archlm_egarch[2, 3]
scalar chi2_egarch_10 = archlm_egarch[3, 1]
scalar p_egarch_10    = archlm_egarch[3, 3]

display "EGARCH ARCH-LM:"
display "  Lag  1: chi2 = " chi2_egarch_1  " | p = " p_egarch_1
display "  Lag  5: chi2 = " chi2_egarch_5  " | p = " p_egarch_5
display "  Lag 10: chi2 = " chi2_egarch_10 " | p = " p_egarch_10

* Residuals for EGARCH
predict double resid_egarch, residuals
predict double sigma2_egarch, variance
gen double std_resid_egarch = resid_egarch / sqrt(sigma2_egarch)
gen double std_resid_sq_egarch = std_resid_egarch^2

wntestq std_resid_egarch, lags(10)
scalar p_lb_egarch_resid = r(p)
wntestq std_resid_sq_egarch, lags(10)
scalar p_lb_egarch_sq = r(p)

display "EGARCH Ljung-Box:"
display "  Residuals (10): p = " p_lb_egarch_resid
display "  Squared   (10): p = " p_lb_egarch_sq

display _newline "=============================================="
display " GJR-GARCH(1,1) Estimation and Diagnostics"
display "=============================================="

* Clean up
drop resid_egarch sigma2_egarch std_resid_egarch std_resid_sq_egarch

* Estimate GJR-GARCH (threshold ARCH)
arch returns, arch(1) garch(1) tarch(1) distribution(normal)
estimates store gjr11

* ARCH-LM test for GJR
estat archlm, lags(1 5 10)
matrix archlm_gjr = r(archlm)

scalar chi2_gjr_1  = archlm_gjr[1, 1]
scalar p_gjr_1     = archlm_gjr[1, 3]
scalar chi2_gjr_5  = archlm_gjr[2, 1]
scalar p_gjr_5     = archlm_gjr[2, 3]
scalar chi2_gjr_10 = archlm_gjr[3, 1]
scalar p_gjr_10    = archlm_gjr[3, 3]

display "GJR-GARCH ARCH-LM:"
display "  Lag  1: chi2 = " chi2_gjr_1  " | p = " p_gjr_1
display "  Lag  5: chi2 = " chi2_gjr_5  " | p = " p_gjr_5
display "  Lag 10: chi2 = " chi2_gjr_10 " | p = " p_gjr_10

* Residuals for GJR
predict double resid_gjr, residuals
predict double sigma2_gjr, variance
gen double std_resid_gjr = resid_gjr / sqrt(sigma2_gjr)
gen double std_resid_sq_gjr = std_resid_gjr^2

wntestq std_resid_gjr, lags(10)
scalar p_lb_gjr_resid = r(p)
wntestq std_resid_sq_gjr, lags(10)
scalar p_lb_gjr_sq = r(p)

display "GJR-GARCH Ljung-Box:"
display "  Residuals (10): p = " p_lb_gjr_resid
display "  Squared   (10): p = " p_lb_gjr_sq

*------------------------------------------------------------------------------
* 7. Export results to CSV
*------------------------------------------------------------------------------

display _newline "=============================================="
display " Exporting Results to CSV"
display "=============================================="

* --- Export ARCH-LM results ---
capture file close fh
file open fh using "../outputs/stata_archlm_results.csv", write replace

file write fh "model,lag,chi2,df,p_value" _newline

* GARCH(1,1)
file write fh "GARCH(1,1),1," (chi2_archlm_1) "," (df_archlm_1) "," (p_archlm_1) _newline
file write fh "GARCH(1,1),5," (chi2_archlm_5) "," (df_archlm_5) "," (p_archlm_5) _newline
file write fh "GARCH(1,1),10," (chi2_archlm_10) "," (df_archlm_10) "," (p_archlm_10) _newline

* EGARCH(1,1)
file write fh "EGARCH(1,1),1," (chi2_egarch_1) ",1," (p_egarch_1) _newline
file write fh "EGARCH(1,1),5," (chi2_egarch_5) ",5," (p_egarch_5) _newline
file write fh "EGARCH(1,1),10," (chi2_egarch_10) ",10," (p_egarch_10) _newline

* GJR-GARCH(1,1)
file write fh "GJR-GARCH(1,1),1," (chi2_gjr_1) ",1," (p_gjr_1) _newline
file write fh "GJR-GARCH(1,1),5," (chi2_gjr_5) ",5," (p_gjr_5) _newline
file write fh "GJR-GARCH(1,1),10," (chi2_gjr_10) ",10," (p_gjr_10) _newline

file close fh
display "  ARCH-LM results saved: ../outputs/stata_archlm_results.csv"

* --- Export Ljung-Box results ---
capture file close fh
file open fh using "../outputs/stata_ljungbox_results.csv", write replace

file write fh "model,test,lags,statistic,p_value" _newline

* GARCH(1,1)
file write fh "GARCH(1,1),LB_residuals,10," (lb_resid_10) "," (p_lb_resid_10) _newline
file write fh "GARCH(1,1),LB_residuals,20," (lb_resid_20) "," (p_lb_resid_20) _newline
file write fh "GARCH(1,1),LB_squared,10," (lb_sq_10) "," (p_lb_sq_10) _newline
file write fh "GARCH(1,1),LB_squared,20," (lb_sq_20) "," (p_lb_sq_20) _newline

* EGARCH(1,1)
file write fh "EGARCH(1,1),LB_residuals,10,.,(" (p_lb_egarch_resid) ")" _newline
file write fh "EGARCH(1,1),LB_squared,10,.,(" (p_lb_egarch_sq) ")" _newline

* GJR-GARCH(1,1)
file write fh "GJR-GARCH(1,1),LB_residuals,10,.,(" (p_lb_gjr_resid) ")" _newline
file write fh "GJR-GARCH(1,1),LB_squared,10,.,(" (p_lb_gjr_sq) ")" _newline

file close fh
display "  Ljung-Box results saved: ../outputs/stata_ljungbox_results.csv"

* --- Export residual statistics ---
capture file close fh
file open fh using "../outputs/stata_residual_stats.csv", write replace

file write fh "statistic,value" _newline
file write fh "mean," (mean_stdresid) _newline
file write fh "std_dev," (sd_stdresid) _newline
file write fh "skewness," (skew_stdresid) _newline
file write fh "kurtosis," (kurt_stdresid) _newline

file close fh
display "  Residual stats saved: ../outputs/stata_residual_stats.csv"

* --- Export combined summary ---
capture file close fh
file open fh using "../outputs/stata_diagnostics_summary.csv", write replace

file write fh "model,archlm_p1,archlm_p5,archlm_p10,lb_resid_p,lb_sq_p" _newline
file write fh "GARCH(1,1)," (p_archlm_1) "," (p_archlm_5) "," (p_archlm_10) "," (p_lb_resid_10) "," (p_lb_sq_10) _newline
file write fh "EGARCH(1,1)," (p_egarch_1) "," (p_egarch_5) "," (p_egarch_10) "," (p_lb_egarch_resid) "," (p_lb_egarch_sq) _newline
file write fh "GJR-GARCH(1,1)," (p_gjr_1) "," (p_gjr_5) "," (p_gjr_10) "," (p_lb_gjr_resid) "," (p_lb_gjr_sq) _newline

file close fh
display "  Summary saved: ../outputs/stata_diagnostics_summary.csv"

*------------------------------------------------------------------------------
* Final summary
*------------------------------------------------------------------------------

display _newline "=============================================="
display " Validation Complete"
display "=============================================="
display "Models estimated: GARCH(1,1), EGARCH(1,1), GJR-GARCH(1,1)"
display "Tests performed:  ARCH-LM, Ljung-Box, Correlogram"
display "Graphics saved:   QQ-plot, Histogram"
display "Results exported: 4 CSV files in ../outputs/"
display "=============================================="

log close
exit
