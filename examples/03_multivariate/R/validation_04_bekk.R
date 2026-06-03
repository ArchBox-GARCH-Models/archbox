###############################################################################
# validation_04_bekk.R
# Validacao cruzada: archbox (Python) vs mgarchBEKK (R) - Modelo BEKK
#
# Este script estima o modelo BEKK(1,1) bivariado usando o pacote mgarchBEKK
# em um subset de 2 series do dataset de cambio.
# Os resultados sao salvos em CSV para comparacao automatizada.
#
# Modelo estimado:
#   BEKK(1,1) bivariado com matrizes C, A, B
#   H_t = C'C + A' * e_{t-1} * e_{t-1}' * A + B' * H_{t-1} * B
#
# Pacotes necessarios: mgarchBEKK, readr, dplyr
#
# Uso: cd examples/03_multivariate/R && Rscript validation_04_bekk.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(mgarchBEKK)
library(readr)
library(dplyr)

cat("=== Validacao R: BEKK Multivariado ===\n\n")

# --- Definir diretorios relativos ao script ---
data_dir   <- "../data"
output_dir <- "../outputs"

# Criar diretorio de saida se nao existir
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# --- Carregar dataset de cambio ---
cat("Carregando fx_majors.csv...\n")
fx <- read_csv(file.path(data_dir, "fx_majors.csv"), show_col_types = FALSE)

cat(sprintf("  Dimensoes totais: %d observacoes x %d colunas\n", nrow(fx), ncol(fx)))
cat(sprintf("  Series disponiveis: %s\n", paste(names(fx)[-1], collapse = ", ")))

# --- Selecionar subset de 2 series para BEKK ---
# BEKK bivariado: usar EUR/USD e GBP/USD (as duas primeiras series)
series_names <- names(fx)[-1]
selected <- series_names[1:2]
cat(sprintf("\n  Series selecionadas para BEKK: %s, %s\n", selected[1], selected[2]))

returns <- as.matrix(fx[, selected])
n <- nrow(returns)
k <- ncol(returns)

cat(sprintf("  Observacoes: %d\n", n))
cat(sprintf("  Dimensao: %d series\n\n", k))

###############################################################################
# ESTIMACAO BEKK(1,1)
###############################################################################

cat("--- Estimando BEKK(1,1) ---\n")
cat("  Modelo: H_t = C'C + A' * eps_{t-1} * eps_{t-1}' * A + B' * H_{t-1} * B\n")
cat("  Ordem: BEKK(1,1)\n\n")

# Estimar BEKK(1,1)
cat("  Estimando modelo (pode levar alguns minutos)...\n")
bekk_fit <- tryCatch({
  BEKK(returns, order = c(1, 1), params = NULL, fixed = NULL, method = "BFGS")
}, error = function(e) {
  cat(sprintf("  ERRO na estimacao BEKK: %s\n", e$message))
  # Tentar com metodo alternativo
  cat("  Tentando com metodo Nelder-Mead...\n")
  tryCatch({
    BEKK(returns, order = c(1, 1), params = NULL, fixed = NULL, method = "Nelder-Mead")
  }, error = function(e2) {
    cat(sprintf("  ERRO tambem com Nelder-Mead: %s\n", e2$message))
    NULL
  })
})

if (!is.null(bekk_fit)) {
  cat("  Estimacao BEKK concluida!\n\n")

  # --- Extrair parametros estimados ---
  est_params <- bekk_fit$est.params

  # Extrair matrizes C, A, B do resultado
  # A estrutura do mgarchBEKK retorna as matrizes em est.params
  # Para BEKK(1,1) bivariado:
  #   C: matriz triangular inferior 2x2 (3 parametros)
  #   A: matriz 2x2 (4 parametros)
  #   B: matriz 2x2 (4 parametros)

  # Extrair matriz C (triangular inferior, intercepto)
  C_mat <- matrix(0, k, k)
  if (!is.null(bekk_fit$C)) {
    C_mat <- bekk_fit$C
  } else if (is.list(est_params)) {
    # Tentar extrair de est.params
    C_mat <- est_params$C
  }

  # Extrair matriz A (ARCH)
  A_mat <- matrix(0, k, k)
  if (!is.null(bekk_fit$A)) {
    A_mat <- bekk_fit$A
  } else if (is.list(est_params)) {
    A_mat <- est_params$A
  }

  # Extrair matriz B (GARCH)
  B_mat <- matrix(0, k, k)
  if (!is.null(bekk_fit$B)) {
    B_mat <- bekk_fit$B
  } else if (is.list(est_params)) {
    B_mat <- est_params$B
  }

  # Exibir matrizes estimadas
  cat("  Matriz C (intercepto, triangular inferior):\n")
  print(round(C_mat, 6))
  cat("\n")

  cat("  Matriz A (ARCH):\n")
  print(round(A_mat, 6))
  cat("\n")

  cat("  Matriz B (GARCH):\n")
  print(round(B_mat, 6))
  cat("\n")

  # --- Extrair log-likelihood e AIC ---
  bekk_ll <- NA_real_
  bekk_aic <- NA_real_

  if (!is.null(bekk_fit$lik)) {
    bekk_ll <- bekk_fit$lik
    cat(sprintf("  Log-Likelihood: %.4f\n", bekk_ll))
  }

  if (!is.null(bekk_fit$aic)) {
    bekk_aic <- bekk_fit$aic
    cat(sprintf("  AIC: %.6f\n", bekk_aic))
  }

  # Calcular numero de parametros
  # BEKK(1,1) bivariado: C tem k*(k+1)/2=3, A tem k^2=4, B tem k^2=4 => total 11
  n_params <- k * (k + 1) / 2 + 2 * k^2
  cat(sprintf("  Numero de parametros: %.0f\n", n_params))

  # Se AIC nao esta disponivel, calcular manualmente
  if (is.na(bekk_aic) && !is.na(bekk_ll)) {
    bekk_aic <- -2 * bekk_ll + 2 * n_params
    cat(sprintf("  AIC (calculado): %.6f\n", bekk_aic))
  }

  # Calcular BIC
  bekk_bic <- NA_real_
  if (!is.na(bekk_ll)) {
    bekk_bic <- -2 * bekk_ll + log(n) * n_params
    cat(sprintf("  BIC (calculado): %.6f\n", bekk_bic))
  }

  cat("\n")

  ###########################################################################
  # SALVAR RESULTADOS
  ###########################################################################

  cat("--- Salvando resultados ---\n")

  # Salvar parametros das matrizes em formato longo
  params_df <- data.frame(
    matrix = character(),
    row    = integer(),
    col    = integer(),
    value  = numeric(),
    stringsAsFactors = FALSE
  )

  # Adicionar elementos da matriz C
  for (i in 1:k) {
    for (j in 1:k) {
      params_df <- rbind(params_df, data.frame(
        matrix = "C", row = i, col = j, value = C_mat[i, j],
        stringsAsFactors = FALSE
      ))
    }
  }

  # Adicionar elementos da matriz A
  for (i in 1:k) {
    for (j in 1:k) {
      params_df <- rbind(params_df, data.frame(
        matrix = "A", row = i, col = j, value = A_mat[i, j],
        stringsAsFactors = FALSE
      ))
    }
  }

  # Adicionar elementos da matriz B
  for (i in 1:k) {
    for (j in 1:k) {
      params_df <- rbind(params_df, data.frame(
        matrix = "B", row = i, col = j, value = B_mat[i, j],
        stringsAsFactors = FALSE
      ))
    }
  }

  # Salvar resultados consolidados com metricas
  results <- data.frame(
    model     = "BEKK(1,1)",
    series1   = selected[1],
    series2   = selected[2],
    n_obs     = n,
    n_params  = n_params,
    loglik    = bekk_ll,
    aic       = bekk_aic,
    bic       = bekk_bic,
    C_11      = C_mat[1, 1],
    C_21      = C_mat[2, 1],
    C_22      = C_mat[2, 2],
    A_11      = A_mat[1, 1],
    A_12      = A_mat[1, 2],
    A_21      = A_mat[2, 1],
    A_22      = A_mat[2, 2],
    B_11      = B_mat[1, 1],
    B_12      = B_mat[1, 2],
    B_21      = B_mat[2, 1],
    B_22      = B_mat[2, 2],
    stringsAsFactors = FALSE
  )

  # Salvar em CSV
  results_file <- file.path(output_dir, "r_validation_bekk_results.csv")
  write_csv(results, results_file)
  cat(sprintf("  Salvo: %s\n", results_file))

  # Salvar parametros detalhados das matrizes
  params_file <- file.path(output_dir, "r_validation_bekk_params.csv")
  write_csv(params_df, params_file)
  cat(sprintf("  Salvo: %s\n", params_file))

  # --- Exibir resumo final ---
  cat("\n--- Resumo BEKK(1,1) ---\n")
  cat(sprintf("  Series: %s, %s\n", selected[1], selected[2]))
  cat(sprintf("  Observacoes: %d\n", n))
  cat(sprintf("  Log-Likelihood: %.4f\n", bekk_ll))
  if (!is.na(bekk_aic)) cat(sprintf("  AIC: %.6f\n", bekk_aic))
  if (!is.na(bekk_bic)) cat(sprintf("  BIC: %.6f\n", bekk_bic))

} else {
  cat("\n  AVISO: Nao foi possivel estimar o modelo BEKK.\n")
  cat("  Verifique se o pacote mgarchBEKK esta instalado.\n")
  cat("  Instalacao: install.packages('mgarchBEKK')\n")

  # Salvar resultado vazio para registro
  results <- data.frame(
    model    = "BEKK(1,1)",
    series1  = selected[1],
    series2  = selected[2],
    n_obs    = n,
    n_params = NA_real_,
    loglik   = NA_real_,
    aic      = NA_real_,
    bic      = NA_real_,
    stringsAsFactors = FALSE
  )

  results_file <- file.path(output_dir, "r_validation_bekk_results.csv")
  write_csv(results, results_file)
  cat(sprintf("  Resultado vazio salvo: %s\n", results_file))
}

cat("\n=== Validacao BEKK concluida! ===\n")
