#!/usr/bin/env Rscript
# Regenerate tests/validation/fixtures/mswm_msar24.json with the R package MSwM.
#
# Usage (from the repository root):
#   Rscript tests/validation/fixtures/generate_mswm_msar24.R
#   Rscript tests/validation/fixtures/generate_mswm_msar24.R <repo-root>
#
# Data
# ----
# archbox/datasets/data/macro/us_gdp_quarterly.csv, column `growth`
# (the series returned by archbox.datasets.load_dataset("us_gdp")).
#
# Models
# ------
# Both are MS(2)-AR(4) fitted on the 303 observations that remain after
# conditioning on the first p = 4 lags (`embed`), exactly like archbox:
#
#  1. common AR coefficients, switching intercept and switching variance
#     sw = c(TRUE, FALSE, FALSE, FALSE, FALSE, TRUE)
#     == MarkovSwitchingAR(y, k_regimes=2, order=4, switching_ar=False)
#  2. everything switching
#     sw = c(TRUE, TRUE, TRUE, TRUE, TRUE, TRUE)
#     == MarkovSwitchingAR(y, k_regimes=2, order=4, switching_ar=True)
#
# archbox writes the model in mean-deviation form
#     y_t = mu_s + sum_l phi_l(s) (y_{t-l} - mu_s) + eps_t,  eps_t ~ N(0, sigma_s^2)
# which is the intercept-switching AR estimated by MSwM with
#     c_s = mu_s * (1 - sum_l phi_l(s))    <=>    mu_s = c_s / (1 - sum_l phi_l(s)).
#
# Sign convention
# ---------------
# MSwM stores the NEGATIVE log-likelihood in `@Fit@logLikel` (it reports
# +373.92 where the log-likelihood is -373.92; this was verified by
# evaluating the archbox Hamilton-filter log-likelihood at the MSwM
# parameter estimates).  The JSON stores the log-likelihood itself.
suppressMessages(library(MSwM))
suppressMessages(library(jsonlite))

args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args) >= 1) args[1] else "."
csv <- file.path(root, "archbox", "datasets", "data", "macro", "us_gdp_quarterly.csv")
out <- file.path(root, "tests", "validation", "fixtures", "mswm_msar24.json")

d <- read.csv(csv)
y <- as.numeric(d$growth)
y <- y[!is.na(y)]
p <- 4

lagmat <- embed(y, p + 1)
df <- data.frame(
  y = lagmat[, 1],
  y1 = lagmat[, 2],
  y2 = lagmat[, 3],
  y3 = lagmat[, 4],
  y4 = lagmat[, 5]
)

fit_model <- function(sw, seed = 1234) {
  set.seed(seed)
  mod <- lm(y ~ y1 + y2 + y3 + y4, data = df)
  msmFit(mod, k = 2, sw = sw, p = 0,
         control = list(parallel = FALSE, maxiter = 2000, tol = 1e-10))
}

# Regimes are labelled by increasing implied mean, so that the fixture does
# not depend on the (arbitrary) EM labelling.
summarise <- function(fit) {
  cf <- as.matrix(fit@Coef)
  intercepts <- as.numeric(cf[, 1])
  phis <- cf[, 2:(p + 1), drop = FALSE]
  mus <- intercepts / (1 - rowSums(phis))
  sigmas <- as.numeric(fit@std)
  pdiag <- diag(fit@transMat)
  ord <- order(mus)
  list(
    loglikelihood = -as.numeric(fit@Fit@logLikel),
    mu = mus[ord],
    intercept = intercepts[ord],
    sigma = sigmas[ord],
    phi = phis[ord, , drop = FALSE],
    pdiag = pdiag[ord]
  )
}

common <- summarise(fit_model(c(TRUE, FALSE, FALSE, FALSE, FALSE, TRUE)))
switching <- summarise(fit_model(rep(TRUE, 6)))

cat("common AR   loglike:", common$loglikelihood, "\n")
cat("switching AR loglike:", switching$loglikelihood, "\n")

common_params <- list(
  mu_0 = common$mu[1], mu_1 = common$mu[2],
  intercept_0 = common$intercept[1], intercept_1 = common$intercept[2],
  sigma_0 = common$sigma[1], sigma_1 = common$sigma[2],
  phi_1 = common$phi[1, 1], phi_2 = common$phi[1, 2],
  phi_3 = common$phi[1, 3], phi_4 = common$phi[1, 4],
  p_00 = common$pdiag[1], p_11 = common$pdiag[2]
)

switching_params <- list(
  mu_0 = switching$mu[1], mu_1 = switching$mu[2],
  intercept_0 = switching$intercept[1], intercept_1 = switching$intercept[2],
  sigma_0 = switching$sigma[1], sigma_1 = switching$sigma[2],
  p_00 = switching$pdiag[1], p_11 = switching$pdiag[2]
)
for (s in 1:2) {
  for (l in 1:p) {
    switching_params[[sprintf("phi_%d_%d", l, s - 1)]] <- switching$phi[s, l]
  }
}

fixture <- list(
  description = paste(
    "MS(2)-AR(4) on the archbox us_gdp dataset (quarterly growth),",
    "fitted with R MSwM::msmFit"
  ),
  r_package = "MSwM",
  r_version = as.character(packageVersion("MSwM")),
  r_script = "tests/validation/fixtures/generate_mswm_msar24.R",
  command = "Rscript tests/validation/fixtures/generate_mswm_msar24.R",
  dataset = "us_gdp (archbox/datasets/data/macro/us_gdp_quarterly.csv, column growth)",
  model = "MS(2)-AR(4), switching intercept and variance, common AR coefficients",
  conditioning = paste(
    "the first p=4 observations are conditioned on (nobs_effective =",
    paste0(nrow(df), ");"),
    "MSwM conditions the same way"
  ),
  nobs_effective = nrow(df),
  regime_order = "regimes sorted by increasing implied mean (regime 0 = low mean)",
  loglikelihood_sign = "MSwM@Fit@logLikel holds the negative log-likelihood; it is negated here",
  parameters = common_params,
  loglikelihood = common$loglikelihood,
  tolerance = list(params_pct = 0.05, params_abs = 0.10, loglike_abs = 1.5),
  switching_ar_model = list(
    model = "MS(2)-AR(4), all coefficients switching (sw = rep(TRUE, 6))",
    parameters = switching_params,
    loglikelihood = switching$loglikelihood,
    tolerance = list(params_pct = 0.05, params_abs = 0.05, loglike_abs = 1.0)
  ),
  note = paste(
    "For the common-AR model MSwM's M-step regresses the pooled regimes on the",
    "shared coefficients with weights P(S_t=s|Y_T) only, ignoring the 1/sigma_s^2",
    "factor, so it is not the maximiser of the expected complete-data",
    "log-likelihood: archbox's GLS M-step attains a strictly higher likelihood",
    "(-372.88 vs -373.92) and the point estimates differ accordingly. Replacing",
    "archbox's weights by MSwM's reproduces the MSwM numbers to ~1% (see",
    "tests/validation/test_vs_mswm.py::test_msar24_reproduces_mswm_with_mswm_mstep).",
    "For the all-switching model both M-steps coincide and the estimates agree."
  )
)

writeLines(toJSON(fixture, auto_unbox = TRUE, pretty = TRUE, digits = 10), out)
cat("wrote", out, "\n")
