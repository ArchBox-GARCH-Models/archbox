###############################################################################
# validation_07_var.R
# Validacao cruzada: archbox (Python) vs rugarch (R) - Value at Risk
#
# Este script calcula VaR usando modelos GARCH(1,1) com distribuicao normal
# e t-Student, realiza rolling backtest com ugarchroll, e executa testes
# de Kupiec e Christoffersen para validacao.
#
# Resultados sao salvos em CSV para comparacao com a archbox.
#
# Uso: Rscript validation_07_var.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(rugarch)
library(readr)
library(dplyr)

cat("=== Validacao R: Value at Risk (VaR) ===\n\n")

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
# Etapa 1: Estimar GARCH(1,1) com dist normal e t-Student (amostra completa)
###############################################################################

cat("--- Etapa 1: Estimacao GARCH(1,1) (amostra completa) ---\n")

# Especificacao Normal
spec_norm <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "norm"
)

# Especificacao t-Student
spec_t <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "std"
)

# Estimar modelos
fit_norm <- ugarchfit(spec_norm, returns, solver = "hybrid")
fit_t <- ugarchfit(spec_t, returns, solver = "hybrid")

cat("  GARCH(1,1)-Normal:\n")
cat(sprintf("    omega=%.6e, alpha1=%.6f, beta1=%.6f\n",
            coef(fit_norm)["omega"], coef(fit_norm)["alpha1"], coef(fit_norm)["beta1"]))
cat(sprintf("    loglik=%.2f\n", likelihood(fit_norm)))

cat("  GARCH(1,1)-tStudent:\n")
cat(sprintf("    omega=%.6e, alpha1=%.6f, beta1=%.6f, shape=%.4f\n",
            coef(fit_t)["omega"], coef(fit_t)["alpha1"], coef(fit_t)["beta1"],
            coef(fit_t)["shape"]))
cat(sprintf("    loglik=%.2f\n\n", likelihood(fit_t)))

###############################################################################
# Etapa 2: Calcular VaR estatico (95% e 99%) para ambas distribuicoes
###############################################################################

cat("--- Etapa 2: VaR estatico (amostra completa) ---\n")

sigma_norm <- as.numeric(sigma(fit_norm))
sigma_t <- as.numeric(sigma(fit_t))
mu_norm <- coef(fit_norm)["mu"]
mu_t <- coef(fit_t)["mu"]
shape_t <- coef(fit_t)["shape"]

# VaR com distribuicao Normal
var95_norm <- mu_norm + sigma_norm * qnorm(0.05)
var99_norm <- mu_norm + sigma_norm * qnorm(0.01)

# VaR com distribuicao t-Student (usando qdist do rugarch)
var95_t <- mu_t + sigma_t * qdist("std", 0.05, shape = shape_t)
var99_t <- mu_t + sigma_t * qdist("std", 0.01, shape = shape_t)

# Contar violacoes na amostra completa
cat(sprintf("  Normal  VaR(95%%): violacoes = %d / %d (%.2f%%)\n",
            sum(returns < var95_norm), n, 100 * sum(returns < var95_norm) / n))
cat(sprintf("  Normal  VaR(99%%): violacoes = %d / %d (%.2f%%)\n",
            sum(returns < var99_norm), n, 100 * sum(returns < var99_norm) / n))
cat(sprintf("  Student VaR(95%%): violacoes = %d / %d (%.2f%%)\n",
            sum(returns < var95_t), n, 100 * sum(returns < var95_t) / n))
cat(sprintf("  Student VaR(99%%): violacoes = %d / %d (%.2f%%)\n\n",
            sum(returns < var99_t), n, 100 * sum(returns < var99_t) / n))

###############################################################################
# Etapa 3: Rolling backtest com ugarchroll
###############################################################################

cat("--- Etapa 3: Rolling backtest (forecast.length=500) ---\n")

forecast_length <- 500
refit_every <- 50

cat(sprintf("  forecast.length=%d, refit.every=%d\n", forecast_length, refit_every))

cat("  Executando ugarchroll (Normal)...\n")
roll_norm <- ugarchroll(
  spec_norm, returns,
  n.ahead = 1,
  forecast.length = forecast_length,
  refit.every = refit_every,
  refit.window = "moving",
  solver = "hybrid",
  calculate.VaR = TRUE,
  VaR.alpha = c(0.01, 0.05)
)

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

###############################################################################
# Etapa 4: Extrair VaR do rolling forecast
###############################################################################

cat("--- Etapa 4: Extrair VaR series do rolling ---\n")

# Extrair dados do rolling forecast
roll_norm_df <- as.data.frame(roll_norm)
roll_t_df <- as.data.frame(roll_t)

# Retornos realizados no periodo de backtest
actual_returns <- tail(returns, forecast_length)

# VaR series (alpha=0.05 e alpha=0.01)
var05_norm_roll <- roll_norm_df[, "VaR[0.05]"]
var01_norm_roll <- roll_norm_df[, "VaR[0.01]"]
var05_t_roll <- roll_t_df[, "VaR[0.05]"]
var01_t_roll <- roll_t_df[, "VaR[0.01]"]

cat(sprintf("  Normal  VaR(5%%):  %d violacoes em %d obs (%.2f%%)\n",
            sum(actual_returns < var05_norm_roll), forecast_length,
            100 * sum(actual_returns < var05_norm_roll) / forecast_length))
cat(sprintf("  Normal  VaR(1%%):  %d violacoes em %d obs (%.2f%%)\n",
            sum(actual_returns < var01_norm_roll), forecast_length,
            100 * sum(actual_returns < var01_norm_roll) / forecast_length))
cat(sprintf("  Student VaR(5%%):  %d violacoes em %d obs (%.2f%%)\n",
            sum(actual_returns < var05_t_roll), forecast_length,
            100 * sum(actual_returns < var05_t_roll) / forecast_length))
cat(sprintf("  Student VaR(1%%):  %d violacoes em %d obs (%.2f%%)\n\n",
            sum(actual_returns < var01_t_roll), forecast_length,
            100 * sum(actual_returns < var01_t_roll) / forecast_length))

###############################################################################
# Etapa 5: Testes de Kupiec e Christoffersen
###############################################################################

cat("--- Etapa 5: Testes de Kupiec e Christoffersen ---\n")

# Teste VaR 5% - Normal
test_norm_05 <- VaRTest(0.05, actual_returns, var05_norm_roll, conf.level = 0.95)
cat(sprintf("  Normal VaR(5%%):  Kupiec p=%.4f, CC p=%.4f\n",
            test_norm_05$uc.LRp, test_norm_05$cc.LRp))

# Teste VaR 1% - Normal
test_norm_01 <- VaRTest(0.01, actual_returns, var01_norm_roll, conf.level = 0.95)
cat(sprintf("  Normal VaR(1%%):  Kupiec p=%.4f, CC p=%.4f\n",
            test_norm_01$uc.LRp, test_norm_01$cc.LRp))

# Teste VaR 5% - t-Student
test_t_05 <- VaRTest(0.05, actual_returns, var05_t_roll, conf.level = 0.95)
cat(sprintf("  Student VaR(5%%): Kupiec p=%.4f, CC p=%.4f\n",
            test_t_05$uc.LRp, test_t_05$cc.LRp))

# Teste VaR 1% - t-Student
test_t_01 <- VaRTest(0.01, actual_returns, var01_t_roll, conf.level = 0.95)
cat(sprintf("  Student VaR(1%%): Kupiec p=%.4f, CC p=%.4f\n\n",
            test_t_01$uc.LRp, test_t_01$cc.LRp))

###############################################################################
# Etapa 6: Salvar resultados em CSV
###############################################################################

cat("--- Etapa 6: Salvar resultados ---\n")

# Consolidar resultados dos testes VaR
var_results <- data.frame(
  model = c("GARCH-Normal", "GARCH-Normal", "GARCH-tStudent", "GARCH-tStudent"),
  alpha = c(0.05, 0.01, 0.05, 0.01),
  forecast_length = forecast_length,
  n_violations = c(
    sum(actual_returns < var05_norm_roll),
    sum(actual_returns < var01_norm_roll),
    sum(actual_returns < var05_t_roll),
    sum(actual_returns < var01_t_roll)
  ),
  expected_violations = c(
    round(forecast_length * 0.05),
    round(forecast_length * 0.01),
    round(forecast_length * 0.05),
    round(forecast_length * 0.01)
  ),
  violation_rate = c(
    sum(actual_returns < var05_norm_roll) / forecast_length,
    sum(actual_returns < var01_norm_roll) / forecast_length,
    sum(actual_returns < var05_t_roll) / forecast_length,
    sum(actual_returns < var01_t_roll) / forecast_length
  ),
  p_kupiec = c(
    test_norm_05$uc.LRp,
    test_norm_01$uc.LRp,
    test_t_05$uc.LRp,
    test_t_01$uc.LRp
  ),
  p_christoffersen = c(
    test_norm_05$cc.LRp,
    test_norm_01$cc.LRp,
    test_t_05$cc.LRp,
    test_t_01$cc.LRp
  ),
  stringsAsFactors = FALSE
)

write_csv(var_results, file.path(output_dir, "r_validation_var_results.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_var_results.csv")))

# Salvar parametros estimados
params_df <- data.frame(
  model = c("GARCH-Normal", "GARCH-tStudent"),
  mu = c(coef(fit_norm)["mu"], coef(fit_t)["mu"]),
  omega = c(coef(fit_norm)["omega"], coef(fit_t)["omega"]),
  alpha1 = c(coef(fit_norm)["alpha1"], coef(fit_t)["alpha1"]),
  beta1 = c(coef(fit_norm)["beta1"], coef(fit_t)["beta1"]),
  shape = c(NA_real_, coef(fit_t)["shape"]),
  loglik = c(likelihood(fit_norm), likelihood(fit_t)),
  stringsAsFactors = FALSE
)

write_csv(params_df, file.path(output_dir, "r_validation_var_params.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_var_params.csv")))

# --- Exibir resumo final ---
cat("\n=== Resumo dos Resultados VaR ===\n\n")
print(as.data.frame(var_results), row.names = FALSE)

cat("\n=== Validacao R (VaR) concluida com sucesso! ===\n")
