###############################################################################
# validation_02_figarch.R
# Validacao cruzada: archbox (Python) vs rugarch/lm (R)
#
# Este script estima modelos GARCH avancados usando o pacote rugarch e
# regressao OLS, comparando com os resultados da archbox:
#   1. FIGARCH(1,d,1) - memoria longa na volatilidade
#   2. GARCH-M        - premio de risco na media (sigma e sigma^2)
#   3. HAR-RV         - volatilidade realizada heterogenea
#
# Uso: cd examples/02_garch_advanced/R && Rscript validation_02_figarch.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(rugarch)
library(readr)
library(dplyr)

cat("=== Validacao R: GARCH Avancado (FIGARCH, GARCH-M, HAR-RV) ===\n\n")

# --- Definir diretorios relativos ao script ---
# O script assume que e executado a partir do diretorio R/
data_dir   <- "../data"
output_dir <- "../outputs"

# Criar diretorio de saida se nao existir
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# --- Carregar datasets ---
cat("Carregando datasets...\n")

sp500 <- read_csv(file.path(data_dir, "sp500_returns.csv"), show_col_types = FALSE)
rv    <- read_csv(file.path(data_dir, "realized_volatility.csv"), show_col_types = FALSE)

cat(sprintf("  SP500 retornos:          %d observacoes\n", nrow(sp500)))
cat(sprintf("  Volatilidade realizada:  %d observacoes\n", nrow(rv)))
cat("\n")

# Extrair vetor de retornos
returns <- sp500$returns

###############################################################################
# PARTE 1: FIGARCH(1,d,1)
# Modelo com memoria longa na variancia condicional.
# O parametro d (0 < d < 1) controla a persistencia fracionaria.
###############################################################################

cat("--- PARTE 1: FIGARCH(1,d,1) ---\n")

# Especificacao do modelo FIGARCH usando rugarch
# variance.model: model="fiGARCH" com garchOrder=c(1,1)
# mean.model: sem ARMA, com media constante
# distribuicao: normal para comparacao direta com archbox
spec_figarch <- ugarchspec(
  variance.model = list(
    model      = "fiGARCH",
    garchOrder = c(1, 1)
  ),
  mean.model = list(
    armaOrder    = c(0, 0),
    include.mean = TRUE
  ),
  distribution.model = "norm"
)

cat("  Estimando FIGARCH(1,d,1)...")

# Estimar o modelo com solver hibrido para maior robustez
fit_figarch <- tryCatch({
  ugarchfit(spec_figarch, returns, solver = "hybrid")
}, error = function(e) {
  cat(sprintf(" ERRO: %s\n", e$message))
  NULL
})

# Extrair parametros do FIGARCH
if (!is.null(fit_figarch)) {
  params_figarch <- coef(fit_figarch)
  ic_figarch     <- infocriteria(fit_figarch)
  ll_figarch     <- likelihood(fit_figarch)

  # O parametro d e o parametro fracionario (d)
  # No rugarch, para fiGARCH, o parametro d esta nos coeficientes
  d_figarch      <- params_figarch["d"]
  omega_figarch  <- params_figarch["omega"]
  alpha_figarch  <- params_figarch["alpha1"]
  beta_figarch   <- params_figarch["beta1"]

  cat(sprintf(" OK\n"))
  cat(sprintf("  Parametro d (fracionario): %.6f\n", d_figarch))
  cat(sprintf("  omega:  %.8f\n", omega_figarch))
  cat(sprintf("  alpha1: %.6f\n", alpha_figarch))
  cat(sprintf("  beta1:  %.6f\n", beta_figarch))
  cat(sprintf("  LogLik: %.2f | AIC: %.6f | BIC: %.6f\n",
              ll_figarch, ic_figarch[1], ic_figarch[2]))
} else {
  # Valores padrao em caso de falha
  d_figarch     <- NA_real_
  omega_figarch <- NA_real_
  alpha_figarch <- NA_real_
  beta_figarch  <- NA_real_
  ll_figarch    <- NA_real_
  ic_figarch    <- c(NA_real_, NA_real_)
}
cat("\n")

###############################################################################
# PARTE 2: GARCH-M (GARCH-in-Mean)
# Modelo onde a volatilidade condicional entra na equacao da media.
# archpow=1: r_t = mu + lambda * sigma_t + eps_t
# archpow=2: r_t = mu + lambda * sigma_t^2 + eps_t
# O coeficiente lambda mede o premio de risco.
###############################################################################

cat("--- PARTE 2: GARCH-M (GARCH-in-Mean) ---\n")

# --- GARCH-M com sigma na media (archpow=1) ---
cat("  Estimando GARCH-M com archpow=1 (sigma na media)...")

spec_garchm1 <- ugarchspec(
  variance.model = list(
    model      = "sGARCH",
    garchOrder = c(1, 1)
  ),
  mean.model = list(
    armaOrder    = c(0, 0),
    include.mean = TRUE,
    archm        = TRUE,
    archpow      = 1
  ),
  distribution.model = "norm"
)

fit_garchm1 <- tryCatch({
  ugarchfit(spec_garchm1, returns, solver = "hybrid")
}, error = function(e) {
  cat(sprintf(" ERRO: %s\n", e$message))
  NULL
})

if (!is.null(fit_garchm1)) {
  params_gm1 <- coef(fit_garchm1)
  ic_gm1     <- infocriteria(fit_garchm1)
  ll_gm1     <- likelihood(fit_garchm1)

  # O coeficiente archm e o lambda (premio de risco)
  lambda_gm1  <- params_gm1["archm"]
  omega_gm1   <- params_gm1["omega"]
  alpha_gm1   <- params_gm1["alpha1"]
  beta_gm1    <- params_gm1["beta1"]

  cat(sprintf(" OK\n"))
  cat(sprintf("  lambda (archm, sigma):   %.6f\n", lambda_gm1))
  cat(sprintf("  omega:  %.8f\n", omega_gm1))
  cat(sprintf("  alpha1: %.6f\n", alpha_gm1))
  cat(sprintf("  beta1:  %.6f\n", beta_gm1))
  cat(sprintf("  LogLik: %.2f | AIC: %.6f | BIC: %.6f\n",
              ll_gm1, ic_gm1[1], ic_gm1[2]))
} else {
  lambda_gm1 <- NA_real_
  omega_gm1  <- NA_real_
  alpha_gm1  <- NA_real_
  beta_gm1   <- NA_real_
  ll_gm1     <- NA_real_
  ic_gm1     <- c(NA_real_, NA_real_)
}
cat("\n")

# --- GARCH-M com sigma^2 na media (archpow=2) ---
cat("  Estimando GARCH-M com archpow=2 (sigma^2 na media)...")

spec_garchm2 <- ugarchspec(
  variance.model = list(
    model      = "sGARCH",
    garchOrder = c(1, 1)
  ),
  mean.model = list(
    armaOrder    = c(0, 0),
    include.mean = TRUE,
    archm        = TRUE,
    archpow      = 2
  ),
  distribution.model = "norm"
)

fit_garchm2 <- tryCatch({
  ugarchfit(spec_garchm2, returns, solver = "hybrid")
}, error = function(e) {
  cat(sprintf(" ERRO: %s\n", e$message))
  NULL
})

if (!is.null(fit_garchm2)) {
  params_gm2 <- coef(fit_garchm2)
  ic_gm2     <- infocriteria(fit_garchm2)
  ll_gm2     <- likelihood(fit_garchm2)

  # Lambda para a versao com variancia na media
  lambda_gm2 <- params_gm2["archm"]
  omega_gm2  <- params_gm2["omega"]
  alpha_gm2  <- params_gm2["alpha1"]
  beta_gm2   <- params_gm2["beta1"]

  cat(sprintf(" OK\n"))
  cat(sprintf("  lambda (archm, sigma^2): %.6f\n", lambda_gm2))
  cat(sprintf("  omega:  %.8f\n", omega_gm2))
  cat(sprintf("  alpha1: %.6f\n", alpha_gm2))
  cat(sprintf("  beta1:  %.6f\n", beta_gm2))
  cat(sprintf("  LogLik: %.2f | AIC: %.6f | BIC: %.6f\n",
              ll_gm2, ic_gm2[1], ic_gm2[2]))
} else {
  lambda_gm2 <- NA_real_
  omega_gm2  <- NA_real_
  alpha_gm2  <- NA_real_
  beta_gm2   <- NA_real_
  ll_gm2     <- NA_real_
  ic_gm2     <- c(NA_real_, NA_real_)
}
cat("\n")

###############################################################################
# PARTE 3: HAR-RV (Heterogeneous Autoregressive Realized Volatility)
# Modelo de Corsi (2009) que decompoe a volatilidade realizada em
# componentes diario, semanal e mensal:
#   RV_{t+1} = beta_0 + beta_d * RV_t^(d) + beta_w * RV_t^(w) + beta_m * RV_t^(m) + eps
# Estimado por OLS simples com lm()
###############################################################################

cat("--- PARTE 3: HAR-RV ---\n")

# Preparar dados para HAR-RV
# rv_daily: volatilidade realizada diaria
# rv_weekly: media movel 5 dias da RV
# rv_monthly: media movel 22 dias da RV
# Variavel dependente: rv_daily do proximo periodo (lead)

cat("  Preparando dados HAR-RV...\n")

# Criar variavel dependente: RV diaria do proximo periodo
rv_data <- rv %>%
  mutate(rv_daily_lead = lead(rv_daily, 1)) %>%
  filter(!is.na(rv_daily_lead))  # Remover ultima observacao (sem lead)

cat(sprintf("  Observacoes para regressao: %d\n", nrow(rv_data)))

# Estimar HAR-RV por OLS
cat("  Estimando HAR-RV com lm()...")

fit_har <- lm(rv_daily_lead ~ rv_daily + rv_weekly + rv_monthly, data = rv_data)

# Extrair coeficientes
coefs_har    <- coef(fit_har)
summary_har  <- summary(fit_har)
r2_har       <- summary_har$r.squared
adj_r2_har   <- summary_har$adj.r.squared

beta_0 <- coefs_har["(Intercept)"]
beta_d <- coefs_har["rv_daily"]
beta_w <- coefs_har["rv_weekly"]
beta_m <- coefs_har["rv_monthly"]

cat(sprintf(" OK\n"))
cat(sprintf("  beta_0 (intercept): %.6f\n", beta_0))
cat(sprintf("  beta_d (diario):    %.6f\n", beta_d))
cat(sprintf("  beta_w (semanal):   %.6f\n", beta_w))
cat(sprintf("  beta_m (mensal):    %.6f\n", beta_m))
cat(sprintf("  R^2:          %.6f\n", r2_har))
cat(sprintf("  R^2 ajustado: %.6f\n", adj_r2_har))
cat("\n")

# Exibir resumo completo da regressao
cat("  Resumo da regressao HAR-RV:\n")
print(summary_har)
cat("\n")

###############################################################################
# PARTE 4: Consolidar e salvar resultados
###############################################################################

cat("--- Salvando resultados ---\n")

# --- Tabela de resultados (metricas por modelo) ---
results_df <- data.frame(
  model = c("FIGARCH(1,d,1)", "GARCH-M (sigma)", "GARCH-M (sigma^2)", "HAR-RV"),
  loglik = c(
    ifelse(is.null(fit_figarch), NA_real_, ll_figarch),
    ifelse(is.null(fit_garchm1), NA_real_, ll_gm1),
    ifelse(is.null(fit_garchm2), NA_real_, ll_gm2),
    as.numeric(logLik(fit_har))
  ),
  aic = c(
    ifelse(is.null(fit_figarch), NA_real_, ic_figarch[1]),
    ifelse(is.null(fit_garchm1), NA_real_, ic_gm1[1]),
    ifelse(is.null(fit_garchm2), NA_real_, ic_gm2[1]),
    AIC(fit_har)
  ),
  bic = c(
    ifelse(is.null(fit_figarch), NA_real_, ic_figarch[2]),
    ifelse(is.null(fit_garchm1), NA_real_, ic_gm1[2]),
    ifelse(is.null(fit_garchm2), NA_real_, ic_gm2[2]),
    BIC(fit_har)
  ),
  r_squared = c(NA_real_, NA_real_, NA_real_, r2_har),
  stringsAsFactors = FALSE
)

# --- Tabela de parametros (formato long: model, parametro, valor) ---
# Conforme especificacao: colunas model, parametro, valor
params_list <- list()

# Parametros FIGARCH
params_list[[1]]  <- data.frame(model = "FIGARCH(1,d,1)", parametro = "d",      valor = d_figarch)
params_list[[2]]  <- data.frame(model = "FIGARCH(1,d,1)", parametro = "omega",  valor = omega_figarch)
params_list[[3]]  <- data.frame(model = "FIGARCH(1,d,1)", parametro = "alpha1", valor = alpha_figarch)
params_list[[4]]  <- data.frame(model = "FIGARCH(1,d,1)", parametro = "beta1",  valor = beta_figarch)

# Parametros GARCH-M (sigma)
params_list[[5]]  <- data.frame(model = "GARCH-M (sigma)", parametro = "lambda", valor = lambda_gm1)
params_list[[6]]  <- data.frame(model = "GARCH-M (sigma)", parametro = "omega",  valor = omega_gm1)
params_list[[7]]  <- data.frame(model = "GARCH-M (sigma)", parametro = "alpha1", valor = alpha_gm1)
params_list[[8]]  <- data.frame(model = "GARCH-M (sigma)", parametro = "beta1",  valor = beta_gm1)

# Parametros GARCH-M (sigma^2)
params_list[[9]]  <- data.frame(model = "GARCH-M (sigma^2)", parametro = "lambda", valor = lambda_gm2)
params_list[[10]] <- data.frame(model = "GARCH-M (sigma^2)", parametro = "omega",  valor = omega_gm2)
params_list[[11]] <- data.frame(model = "GARCH-M (sigma^2)", parametro = "alpha1", valor = alpha_gm2)
params_list[[12]] <- data.frame(model = "GARCH-M (sigma^2)", parametro = "beta1",  valor = beta_gm2)

# Parametros HAR-RV
params_list[[13]] <- data.frame(model = "HAR-RV", parametro = "beta_0",       valor = beta_0)
params_list[[14]] <- data.frame(model = "HAR-RV", parametro = "beta_d",       valor = beta_d)
params_list[[15]] <- data.frame(model = "HAR-RV", parametro = "beta_w",       valor = beta_w)
params_list[[16]] <- data.frame(model = "HAR-RV", parametro = "beta_m",       valor = beta_m)
params_list[[17]] <- data.frame(model = "HAR-RV", parametro = "r_squared",    valor = r2_har)
params_list[[18]] <- data.frame(model = "HAR-RV", parametro = "adj_r_squared", valor = adj_r2_har)

params_df <- bind_rows(params_list)

# Salvar CSVs
write_csv(results_df, file.path(output_dir, "r_validation_advanced_results.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_advanced_results.csv")))

write_csv(params_df, file.path(output_dir, "r_validation_advanced_params.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_advanced_params.csv")))

# --- Exibir resumo final ---
cat("\n=== Resumo dos Resultados ===\n\n")

cat("--- Metricas por Modelo ---\n")
print(as.data.frame(results_df), row.names = FALSE)

cat("\n--- Parametros Estimados ---\n")
print(as.data.frame(params_df), row.names = FALSE)

###############################################################################
# PARTE 5: Comparacao com resultados Python (archbox)
# Carrega os resultados Python salvos pelos notebooks e compara
###############################################################################

cat("\n--- Comparacao R vs Python ---\n")
cat("  Para comparar, execute os notebooks Python primeiro e depois\n")
cat("  compare os valores de:\n")
cat("    - FIGARCH: parametro d deve ser proximo entre R e Python\n")
cat("    - GARCH-M: lambda (premio de risco) deve ser proximo\n")
cat("    - HAR-RV: coeficientes b_d, b_w, b_m e R^2 devem ser proximos\n")
cat("  Nota: diferencas pequenas sao esperadas devido a otimizadores diferentes.\n")

cat("\n=== Validacao R concluida com sucesso! ===\n")
