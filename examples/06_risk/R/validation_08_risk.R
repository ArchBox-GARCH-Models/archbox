###############################################################################
# validation_08_risk.R
# Validacao cruzada: archbox (Python) vs rugarch (R) - Expected Shortfall & EWMA
#
# Este script calcula Expected Shortfall (ES), executa ESTest,
# e implementa EWMA (RiskMetrics, lambda=0.94) para comparacao.
#
# Resultados sao salvos em CSV para comparacao com a archbox.
#
# Uso: Rscript validation_08_risk.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(rugarch)
library(readr)
library(dplyr)

cat("=== Validacao R: Expected Shortfall e EWMA ===\n\n")

# --- Definir diretorios ---
data_dir <- "../data"
output_dir <- "../outputs"

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# --- Carregar dados ---
cat("Carregando sp500_returns.csv...\n")
sp500 <- read_csv(file.path(data_dir, "sp500_returns.csv"), show_col_types = FALSE)
returns <- sp500$returns
n <- length(returns)
cat(sprintf("  SP500: %d observacoes\n\n", n))

###############################################################################
# Etapa 1: Rolling backtest com GARCH(1,1)-tStudent para ES
###############################################################################

cat("--- Etapa 1: Rolling backtest GARCH(1,1)-tStudent ---\n")

forecast_length <- 500
refit_every <- 50

spec_t <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "std"
)

cat(sprintf("  forecast.length=%d, refit.every=%d\n", forecast_length, refit_every))
cat("  Executando ugarchroll (t-Student)...\n")

roll_t <- ugarchroll(
  spec_t, returns,
  n.ahead = 1,
  forecast.length = forecast_length,
  refit.every = refit_every,
  refit.window = "moving",
  solver = "hybrid",
  calculate.VaR = TRUE,
  VaR.alpha = c(0.01, 0.05)
)

cat("  Rolling backtest concluido.\n\n")

# Extrair dados do rolling
roll_t_df <- as.data.frame(roll_t)
actual_returns <- tail(returns, forecast_length)

# VaR series
var05_t <- roll_t_df[, "VaR[0.05]"]
var01_t <- roll_t_df[, "VaR[0.01]"]

###############################################################################
# Etapa 2: Calcular Expected Shortfall
###############################################################################

cat("--- Etapa 2: Expected Shortfall ---\n")

# Extrair mu e sigma do rolling forecast
mu_roll <- roll_t_df$Mu
sigma_roll <- roll_t_df$Sigma

# Obter shape (graus de liberdade) do ultimo fit
# Reestimar para obter shape
fit_t <- ugarchfit(spec_t, returns, solver = "hybrid")
shape_param <- coef(fit_t)["shape"]

cat(sprintf("  Shape (graus de liberdade t-Student): %.4f\n", shape_param))

# Calcular ES analitico para distribuicao t-Student
# ES = mu + sigma * ES_standardized
# Para t-Student: ES_std = -(dt(qt(alpha, nu), nu) / alpha) * ((nu + qt(alpha,nu)^2) / (nu - 1))
calc_es_t <- function(alpha, mu, sigma, nu) {
  q_alpha <- qt(alpha, df = nu)
  d_alpha <- dt(q_alpha, df = nu)
  es_std <- -(d_alpha / alpha) * ((nu + q_alpha^2) / (nu - 1))
  return(mu + sigma * es_std)
}

es05_t <- calc_es_t(0.05, mu_roll, sigma_roll, shape_param)
es01_t <- calc_es_t(0.01, mu_roll, sigma_roll, shape_param)

cat(sprintf("  ES(5%%) media:  %.6f\n", mean(es05_t)))
cat(sprintf("  ES(1%%) media:  %.6f\n", mean(es01_t)))

# Contar violacoes de ES (retornos abaixo do ES)
cat(sprintf("  ES(5%%) violacoes: %d / %d\n",
            sum(actual_returns < es05_t), forecast_length))
cat(sprintf("  ES(1%%) violacoes: %d / %d\n\n",
            sum(actual_returns < es01_t), forecast_length))

###############################################################################
# Etapa 3: Teste de Expected Shortfall (ESTest)
###############################################################################

cat("--- Etapa 3: Teste de ES (ESTest) ---\n")

# ESTest para alpha=0.05
tryCatch({
  es_test_05 <- ESTest(
    alpha = 0.05,
    actual = actual_returns,
    ES = es05_t,
    VaR = var05_t,
    conf.level = 0.95
  )
  cat(sprintf("  ESTest(5%%): stat=%.4f, p-value=%.4f, boot.p=%.4f\n",
              es_test_05$expected.exceed,
              es_test_05$p.value,
              es_test_05$boot.p.value))
  es05_pval <- es_test_05$p.value
  es05_boot_pval <- es_test_05$boot.p.value
}, error = function(e) {
  cat(sprintf("  ESTest(5%%): ERRO - %s\n", e$message))
  es05_pval <<- NA_real_
  es05_boot_pval <<- NA_real_
})

# ESTest para alpha=0.01
tryCatch({
  es_test_01 <- ESTest(
    alpha = 0.01,
    actual = actual_returns,
    ES = es01_t,
    VaR = var01_t,
    conf.level = 0.95
  )
  cat(sprintf("  ESTest(1%%): stat=%.4f, p-value=%.4f, boot.p=%.4f\n\n",
              es_test_01$expected.exceed,
              es_test_01$p.value,
              es_test_01$boot.p.value))
  es01_pval <- es_test_01$p.value
  es01_boot_pval <- es_test_01$boot.p.value
}, error = function(e) {
  cat(sprintf("  ESTest(1%%): ERRO - %s\n\n", e$message))
  es01_pval <<- NA_real_
  es01_boot_pval <<- NA_real_
})

###############################################################################
# Etapa 4: EWMA (RiskMetrics, lambda=0.94)
###############################################################################

cat("--- Etapa 4: EWMA (lambda=0.94) ---\n")

lambda <- 0.94

# Implementar EWMA manualmente
ewma_var <- numeric(n)
ewma_var[1] <- var(returns)  # Inicializar com variancia amostral

for (i in 2:n) {
  ewma_var[i] <- lambda * ewma_var[i - 1] + (1 - lambda) * returns[i - 1]^2
}

ewma_sigma <- sqrt(ewma_var)

# VaR EWMA (assumindo distribuicao normal)
ewma_var95 <- qnorm(0.05) * ewma_sigma
ewma_var99 <- qnorm(0.01) * ewma_sigma

# ES EWMA (normal): ES = -sigma * dnorm(qnorm(alpha)) / alpha
ewma_es95 <- -ewma_sigma * dnorm(qnorm(0.05)) / 0.05
ewma_es99 <- -ewma_sigma * dnorm(qnorm(0.01)) / 0.01

# Avaliar no periodo de backtest (ultimos 500 obs)
ewma_var95_bt <- tail(ewma_var95, forecast_length)
ewma_var99_bt <- tail(ewma_var99, forecast_length)
ewma_es95_bt <- tail(ewma_es95, forecast_length)
ewma_es99_bt <- tail(ewma_es99, forecast_length)

n_viol_ewma_95 <- sum(actual_returns < ewma_var95_bt)
n_viol_ewma_99 <- sum(actual_returns < ewma_var99_bt)

cat(sprintf("  Lambda = %.2f\n", lambda))
cat(sprintf("  EWMA sigma media: %.6f\n", mean(tail(ewma_sigma, forecast_length))))
cat(sprintf("  EWMA VaR(5%%) violacoes: %d / %d (%.2f%%)\n",
            n_viol_ewma_95, forecast_length,
            100 * n_viol_ewma_95 / forecast_length))
cat(sprintf("  EWMA VaR(1%%) violacoes: %d / %d (%.2f%%)\n\n",
            n_viol_ewma_99, forecast_length,
            100 * n_viol_ewma_99 / forecast_length))

# Teste de Kupiec para EWMA
test_ewma_05 <- VaRTest(0.05, actual_returns, ewma_var95_bt, conf.level = 0.95)
test_ewma_01 <- VaRTest(0.01, actual_returns, ewma_var99_bt, conf.level = 0.95)

cat(sprintf("  EWMA VaR(5%%): Kupiec p=%.4f, CC p=%.4f\n",
            test_ewma_05$uc.LRp, test_ewma_05$cc.LRp))
cat(sprintf("  EWMA VaR(1%%): Kupiec p=%.4f, CC p=%.4f\n\n",
            test_ewma_01$uc.LRp, test_ewma_01$cc.LRp))

###############################################################################
# Etapa 5: Salvar todos os resultados em CSV
###############################################################################

cat("--- Etapa 5: Salvar resultados ---\n")

# Resultados consolidados de risco
risk_results <- data.frame(
  model = c(
    "GARCH-tStudent", "GARCH-tStudent",
    "EWMA-Normal", "EWMA-Normal"
  ),
  alpha = c(0.05, 0.01, 0.05, 0.01),
  forecast_length = forecast_length,
  n_violations = c(
    sum(actual_returns < var05_t),
    sum(actual_returns < var01_t),
    n_viol_ewma_95,
    n_viol_ewma_99
  ),
  p_kupiec = c(
    VaRTest(0.05, actual_returns, var05_t)$uc.LRp,
    VaRTest(0.01, actual_returns, var01_t)$uc.LRp,
    test_ewma_05$uc.LRp,
    test_ewma_01$uc.LRp
  ),
  p_christoffersen = c(
    VaRTest(0.05, actual_returns, var05_t)$cc.LRp,
    VaRTest(0.01, actual_returns, var01_t)$cc.LRp,
    test_ewma_05$cc.LRp,
    test_ewma_01$cc.LRp
  ),
  stringsAsFactors = FALSE
)

write_csv(risk_results, file.path(output_dir, "r_validation_risk_results.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_risk_results.csv")))

# ES resultados
es_results <- data.frame(
  model = c("GARCH-tStudent", "GARCH-tStudent", "EWMA-Normal", "EWMA-Normal"),
  alpha = c(0.05, 0.01, 0.05, 0.01),
  es_mean = c(
    mean(es05_t), mean(es01_t),
    mean(ewma_es95_bt), mean(ewma_es99_bt)
  ),
  es_test_pvalue = c(
    ifelse(exists("es05_pval"), es05_pval, NA_real_),
    ifelse(exists("es01_pval"), es01_pval, NA_real_),
    NA_real_,  # ESTest nao aplicavel a EWMA-Normal diretamente
    NA_real_
  ),
  stringsAsFactors = FALSE
)

write_csv(es_results, file.path(output_dir, "r_validation_es_results.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_es_results.csv")))

# EWMA series (volatilidade, VaR, ES) para comparacao detalhada
ewma_detail <- data.frame(
  date = tail(sp500$date, forecast_length),
  returns = actual_returns,
  ewma_sigma = tail(ewma_sigma, forecast_length),
  ewma_var95 = ewma_var95_bt,
  ewma_var99 = ewma_var99_bt,
  ewma_es95 = ewma_es95_bt,
  ewma_es99 = ewma_es99_bt
)

write_csv(ewma_detail, file.path(output_dir, "r_validation_ewma_detail.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_ewma_detail.csv")))

# --- Exibir resumo final ---
cat("\n=== Resumo: Resultados de Risco ===\n\n")
cat("--- VaR Backtest ---\n")
print(as.data.frame(risk_results), row.names = FALSE)

cat("\n--- Expected Shortfall ---\n")
print(as.data.frame(es_results), row.names = FALSE)

cat("\n=== Validacao R (ES & EWMA) concluida com sucesso! ===\n")
