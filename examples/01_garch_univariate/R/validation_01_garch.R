###############################################################################
# validation_01_garch.R
# Validacao cruzada: archbox (Python) vs rugarch (R)
#
# Este script estima 6 modelos GARCH univariados usando o pacote rugarch
# nos mesmos datasets usados pelos notebooks Python da archbox.
# Os resultados sao salvos em CSV para comparacao automatizada.
#
# Modelos estimados:
#   1. GARCH(1,1)   - sGARCH
#   2. EGARCH(1,1)  - eGARCH
#   3. GJR-GARCH(1,1) - gjrGARCH
#   4. APARCH(1,1)  - apARCH
#   5. IGARCH(1,1)  - iGARCH
#   6. Component-GARCH - csGARCH
#
# Uso: Rscript validation_01_garch.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(rugarch)
library(readr)
library(dplyr)

cat("=== Validacao R: GARCH Univariado ===\n\n")

# --- Definir diretorio de dados relativo ao script ---
# O script assume que e executado a partir do diretorio R/
data_dir <- "../data"
output_dir <- "../outputs"

# Criar diretorio de saida se nao existir
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# --- Carregar os 3 datasets ---
cat("Carregando datasets...\n")

sp500 <- read_csv(file.path(data_dir, "sp500_returns.csv"), show_col_types = FALSE)
ibov  <- read_csv(file.path(data_dir, "ibovespa_returns.csv"), show_col_types = FALSE)
btc   <- read_csv(file.path(data_dir, "bitcoin_returns.csv"), show_col_types = FALSE)

cat(sprintf("  SP500:    %d observacoes\n", nrow(sp500)))
cat(sprintf("  Ibovespa: %d observacoes\n", nrow(ibov)))
cat(sprintf("  Bitcoin:  %d observacoes\n", nrow(btc)))
cat("\n")

# --- Funcao generica de estimacao ---
# Estima um modelo GARCH usando rugarch e retorna parametros e metricas
estimate_model <- function(returns, model_type, garch_order = c(1, 1)) {
  # Definir especificacao do modelo
  spec <- ugarchspec(
    variance.model = list(model = model_type, garchOrder = garch_order),
    mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
    distribution.model = "norm"
  )

  # Estimar o modelo com solver hibrido para maior robustez
  fit <- ugarchfit(spec, returns, solver = "hybrid")

  # Extrair parametros estimados
  params <- coef(fit)

  # Extrair criterios de informacao (AIC, BIC, Shibata, Hannan-Quinn)
  ic <- infocriteria(fit)

  # Extrair log-verossimilhanca
  ll <- likelihood(fit)

  # Extrair volatilidade condicional (sigma)
  vol <- as.numeric(sigma(fit))

  list(
    fit    = fit,
    params = params,
    loglik = ll,
    aic    = ic[1],
    bic    = ic[2],
    sigma  = vol
  )
}

# --- Funcao para extrair parametros padronizados ---
# Extrai omega, alpha1, beta1, gamma1 de forma uniforme entre modelos
extract_params <- function(params, model_name) {
  # Inicializar com NA
  omega  <- NA_real_
  alpha1 <- NA_real_
  beta1  <- NA_real_
  gamma1 <- NA_real_
  mu     <- NA_real_

  # Extrair mu (media) - presente em todos os modelos
  if ("mu" %in% names(params)) mu <- params["mu"]

  # Extrair parametros conforme o tipo de modelo
  if (model_name %in% c("GARCH", "IGARCH")) {
    # sGARCH e iGARCH: omega, alpha1, beta1
    if ("omega"  %in% names(params)) omega  <- params["omega"]
    if ("alpha1" %in% names(params)) alpha1 <- params["alpha1"]
    if ("beta1"  %in% names(params)) beta1  <- params["beta1"]

  } else if (model_name == "EGARCH") {
    # eGARCH: omega, alpha1, beta1, gamma1
    if ("omega"  %in% names(params)) omega  <- params["omega"]
    if ("alpha1" %in% names(params)) alpha1 <- params["alpha1"]
    if ("beta1"  %in% names(params)) beta1  <- params["beta1"]
    if ("gamma1" %in% names(params)) gamma1 <- params["gamma1"]

  } else if (model_name == "GJR") {
    # gjrGARCH: omega, alpha1, beta1, gamma1 (leverage)
    if ("omega"  %in% names(params)) omega  <- params["omega"]
    if ("alpha1" %in% names(params)) alpha1 <- params["alpha1"]
    if ("beta1"  %in% names(params)) beta1  <- params["beta1"]
    if ("gamma1" %in% names(params)) gamma1 <- params["gamma1"]

  } else if (model_name == "APARCH") {
    # apARCH: omega, alpha1, beta1, gamma1, delta
    if ("omega"  %in% names(params)) omega  <- params["omega"]
    if ("alpha1" %in% names(params)) alpha1 <- params["alpha1"]
    if ("beta1"  %in% names(params)) beta1  <- params["beta1"]
    if ("gamma1" %in% names(params)) gamma1 <- params["gamma1"]

  } else if (model_name == "CGARCH") {
    # csGARCH (Component GARCH): parametros especificos
    # Permanente: omega, beta1 (rho em csGARCH = beta1)
    # Transitorio: alpha1, beta1 (phi em csGARCH)
    if ("omega"  %in% names(params)) omega  <- params["omega"]
    if ("alpha1" %in% names(params)) alpha1 <- params["alpha1"]
    if ("beta1"  %in% names(params)) beta1  <- params["beta1"]
    if ("eta11"  %in% names(params)) gamma1 <- params["eta11"]
  }

  data.frame(
    mu     = mu,
    omega  = omega,
    alpha1 = alpha1,
    beta1  = beta1,
    gamma1 = gamma1,
    stringsAsFactors = FALSE
  )
}

# --- Funcao para estimar todos os modelos em um dataset ---
estimate_all_models <- function(returns, dataset_name) {
  cat(sprintf("--- Estimando modelos para %s ---\n", dataset_name))

  # Definicao dos modelos: nome amigavel -> tipo rugarch
  models <- list(
    list(name = "GARCH",  type = "sGARCH"),
    list(name = "EGARCH", type = "eGARCH"),
    list(name = "GJR",    type = "gjrGARCH"),
    list(name = "APARCH", type = "apARCH"),
    list(name = "IGARCH", type = "iGARCH"),
    list(name = "CGARCH", type = "csGARCH")
  )

  # Listas para armazenar resultados
  results_list <- list()
  params_list  <- list()

  for (m in models) {
    cat(sprintf("  Estimando %s...", m$name))

    tryCatch({
      # Estimar modelo
      res <- estimate_model(returns, m$type)

      # Armazenar metricas
      results_list[[m$name]] <- data.frame(
        dataset = dataset_name,
        model   = m$name,
        loglik  = res$loglik,
        aic     = res$aic,
        bic     = res$bic,
        stringsAsFactors = FALSE
      )

      # Extrair e armazenar parametros padronizados
      p <- extract_params(res$params, m$name)
      p$dataset <- dataset_name
      p$model   <- m$name
      params_list[[m$name]] <- p

      cat(sprintf(" OK (loglik=%.2f, AIC=%.6f)\n", res$loglik, res$aic))

    }, error = function(e) {
      # Caso o modelo falhe na convergencia, registrar com NA
      cat(sprintf(" ERRO: %s\n", e$message))

      results_list[[m$name]] <<- data.frame(
        dataset = dataset_name,
        model   = m$name,
        loglik  = NA_real_,
        aic     = NA_real_,
        bic     = NA_real_,
        stringsAsFactors = FALSE
      )

      params_list[[m$name]] <<- data.frame(
        dataset = dataset_name,
        model   = m$name,
        mu      = NA_real_,
        omega   = NA_real_,
        alpha1  = NA_real_,
        beta1   = NA_real_,
        gamma1  = NA_real_,
        stringsAsFactors = FALSE
      )
    })
  }

  cat("\n")

  list(
    results = bind_rows(results_list),
    params  = bind_rows(params_list)
  )
}

# --- Estimar modelos nos 3 datasets ---

# SP500
sp500_res <- estimate_all_models(sp500$returns, "sp500")

# Ibovespa
ibov_res <- estimate_all_models(ibov$returns, "ibovespa")

# Bitcoin
btc_res <- estimate_all_models(btc$returns, "bitcoin")

# --- Consolidar resultados ---
cat("Consolidando resultados...\n")

# Juntar resultados de todos os datasets
all_results <- bind_rows(
  sp500_res$results,
  ibov_res$results,
  btc_res$results
)

all_params <- bind_rows(
  sp500_res$params,
  ibov_res$params,
  btc_res$params
)

# Reordenar colunas dos parametros
all_params <- all_params %>%
  select(dataset, model, mu, omega, alpha1, beta1, gamma1)

# --- Salvar resultados em CSV ---
cat("Salvando resultados...\n")

# Resultados (loglik, AIC, BIC) por dataset
write_csv(all_results, file.path(output_dir, "r_validation_garch_results.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_garch_results.csv")))

# Parametros estimados por dataset
write_csv(all_params, file.path(output_dir, "r_validation_garch_params.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "r_validation_garch_params.csv")))

# --- Exibir resumo ---
cat("\n=== Resumo dos Resultados ===\n\n")

cat("--- Metricas (loglik, AIC, BIC) ---\n")
print(as.data.frame(all_results), row.names = FALSE)

cat("\n--- Parametros Estimados ---\n")
print(as.data.frame(all_params), row.names = FALSE)

cat("\n=== Validacao R concluida com sucesso! ===\n")
