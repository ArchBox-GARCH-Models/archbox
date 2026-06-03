###############################################################################
# compare_results.R
# Comparacao automatizada: archbox (Python) vs rugarch (R)
#
# Este script le os CSVs gerados pelo Python (archbox) e pelo R (rugarch)
# e calcula as diferencas percentuais nos parametros e metricas.
#
# Espera encontrar os seguintes arquivos no diretorio outputs/:
#   - r_validation_garch_results.csv  (gerado por validation_01_garch.R)
#   - r_validation_garch_params.csv   (gerado por validation_01_garch.R)
#   - python_garch_results.csv        (gerado pelo notebook Python)
#   - python_garch_params.csv         (gerado pelo notebook Python)
#
# Uso: Rscript compare_results.R
###############################################################################

# --- Carregar pacotes ---
library(readr)
library(dplyr)

cat("=== Comparacao Python (archbox) vs R (rugarch) ===\n\n")

# --- Definir diretorio de saida ---
output_dir <- "../outputs"

# --- Funcao para calcular diferenca percentual ---
# Calcula a diferenca percentual entre dois valores
# Usa o valor R como referencia (denominador)
pct_diff <- function(python_val, r_val) {
  ifelse(
    is.na(python_val) | is.na(r_val) | r_val == 0,
    NA_real_,
    ((python_val - r_val) / abs(r_val)) * 100
  )
}

# --- Carregar resultados do R ---
cat("Carregando resultados do R...\n")

r_results_file <- file.path(output_dir, "r_validation_garch_results.csv")
r_params_file  <- file.path(output_dir, "r_validation_garch_params.csv")

if (!file.exists(r_results_file)) {
  stop("Arquivo nao encontrado: ", r_results_file,
       "\nExecute primeiro: Rscript validation_01_garch.R")
}

r_results <- read_csv(r_results_file, show_col_types = FALSE)
r_params  <- read_csv(r_params_file, show_col_types = FALSE)

cat(sprintf("  R: %d linhas de resultados, %d linhas de parametros\n",
            nrow(r_results), nrow(r_params)))

# --- Carregar resultados do Python ---
cat("Carregando resultados do Python...\n")

py_results_file <- file.path(output_dir, "python_garch_results.csv")
py_params_file  <- file.path(output_dir, "python_garch_params.csv")

if (!file.exists(py_results_file)) {
  cat(sprintf("  AVISO: Arquivo nao encontrado: %s\n", py_results_file))
  cat("  Os resultados do Python ainda nao foram gerados.\n")
  cat("  Execute o notebook Python primeiro e salve os resultados em CSV.\n")
  cat("  Formato esperado para python_garch_results.csv:\n")
  cat("    dataset, model, loglik, aic, bic\n")
  cat("  Formato esperado para python_garch_params.csv:\n")
  cat("    dataset, model, mu, omega, alpha1, beta1, gamma1\n\n")

  # Mostrar apenas os resultados do R como referencia
  cat("--- Resultados R (referencia) ---\n")
  print(as.data.frame(r_results), row.names = FALSE)
  cat("\n--- Parametros R (referencia) ---\n")
  print(as.data.frame(r_params), row.names = FALSE)

  cat("\n=== Comparacao nao realizada (faltam resultados Python) ===\n")
  quit(status = 0)
}

py_results <- read_csv(py_results_file, show_col_types = FALSE)
py_params  <- read_csv(py_params_file, show_col_types = FALSE)

cat(sprintf("  Python: %d linhas de resultados, %d linhas de parametros\n",
            nrow(py_results), nrow(py_params)))

# --- Comparar metricas (loglik, AIC, BIC) ---
cat("\n--- Comparacao de Metricas ---\n\n")

# Juntar resultados por dataset e modelo
comp_results <- r_results %>%
  inner_join(py_results, by = c("dataset", "model"), suffix = c("_r", "_py")) %>%
  mutate(
    pct_diff_loglik = pct_diff(loglik_py, loglik_r),
    pct_diff_aic    = pct_diff(aic_py, aic_r),
    pct_diff_bic    = pct_diff(bic_py, bic_r)
  )

# Exibir comparacao de metricas
for (ds in unique(comp_results$dataset)) {
  cat(sprintf("Dataset: %s\n", ds))

  ds_comp <- comp_results %>% filter(dataset == ds)

  for (i in seq_len(nrow(ds_comp))) {
    row <- ds_comp[i, ]
    cat(sprintf("  %-8s | LogLik: R=%.2f  Py=%.2f  (diff=%.4f%%)\n",
                row$model, row$loglik_r, row$loglik_py, row$pct_diff_loglik))
    cat(sprintf("           | AIC:    R=%.6f  Py=%.6f  (diff=%.4f%%)\n",
                row$aic_r, row$aic_py, row$pct_diff_aic))
    cat(sprintf("           | BIC:    R=%.6f  Py=%.6f  (diff=%.4f%%)\n",
                row$bic_r, row$bic_py, row$pct_diff_bic))
  }
  cat("\n")
}

# --- Comparar parametros ---
cat("--- Comparacao de Parametros ---\n\n")

# Juntar parametros por dataset e modelo
comp_params <- r_params %>%
  inner_join(py_params, by = c("dataset", "model"), suffix = c("_r", "_py")) %>%
  mutate(
    pct_diff_omega  = pct_diff(omega_py, omega_r),
    pct_diff_alpha1 = pct_diff(alpha1_py, alpha1_r),
    pct_diff_beta1  = pct_diff(beta1_py, beta1_r),
    pct_diff_gamma1 = pct_diff(gamma1_py, gamma1_r)
  )

# Exibir comparacao de parametros
for (ds in unique(comp_params$dataset)) {
  cat(sprintf("Dataset: %s\n", ds))

  ds_comp <- comp_params %>% filter(dataset == ds)

  for (i in seq_len(nrow(ds_comp))) {
    row <- ds_comp[i, ]
    cat(sprintf("  %-8s | omega:  R=%.8f  Py=%.8f  (diff=%.4f%%)\n",
                row$model,
                ifelse(is.na(row$omega_r), 0, row$omega_r),
                ifelse(is.na(row$omega_py), 0, row$omega_py),
                ifelse(is.na(row$pct_diff_omega), NA, row$pct_diff_omega)))
    cat(sprintf("           | alpha1: R=%.8f  Py=%.8f  (diff=%.4f%%)\n",
                ifelse(is.na(row$alpha1_r), 0, row$alpha1_r),
                ifelse(is.na(row$alpha1_py), 0, row$alpha1_py),
                ifelse(is.na(row$pct_diff_alpha1), NA, row$pct_diff_alpha1)))
    cat(sprintf("           | beta1:  R=%.8f  Py=%.8f  (diff=%.4f%%)\n",
                ifelse(is.na(row$beta1_r), 0, row$beta1_r),
                ifelse(is.na(row$beta1_py), 0, row$beta1_py),
                ifelse(is.na(row$pct_diff_beta1), NA, row$pct_diff_beta1)))
    if (!is.na(row$gamma1_r) || !is.na(row$gamma1_py)) {
      cat(sprintf("           | gamma1: R=%.8f  Py=%.8f  (diff=%.4f%%)\n",
                  ifelse(is.na(row$gamma1_r), 0, row$gamma1_r),
                  ifelse(is.na(row$gamma1_py), 0, row$gamma1_py),
                  ifelse(is.na(row$pct_diff_gamma1), NA, row$pct_diff_gamma1)))
    }
  }
  cat("\n")
}

# --- Salvar comparacao em CSV ---
cat("Salvando comparacoes...\n")

# Salvar comparacao de metricas
write_csv(comp_results, file.path(output_dir, "comparison_garch_results.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "comparison_garch_results.csv")))

# Salvar comparacao de parametros
write_csv(comp_params, file.path(output_dir, "comparison_garch_params.csv"))
cat(sprintf("  Salvo: %s\n", file.path(output_dir, "comparison_garch_params.csv")))

# --- Resumo final ---
cat("\n=== Resumo da Comparacao ===\n")

# Calcular estatisticas das diferencas percentuais
cat(sprintf("\nDiferenca percentual media (absoluta) nos parametros:\n"))
cat(sprintf("  omega:  %.4f%%\n", mean(abs(comp_params$pct_diff_omega), na.rm = TRUE)))
cat(sprintf("  alpha1: %.4f%%\n", mean(abs(comp_params$pct_diff_alpha1), na.rm = TRUE)))
cat(sprintf("  beta1:  %.4f%%\n", mean(abs(comp_params$pct_diff_beta1), na.rm = TRUE)))
cat(sprintf("  gamma1: %.4f%%\n", mean(abs(comp_params$pct_diff_gamma1), na.rm = TRUE)))

cat(sprintf("\nDiferenca percentual media (absoluta) nas metricas:\n"))
cat(sprintf("  loglik: %.4f%%\n", mean(abs(comp_results$pct_diff_loglik), na.rm = TRUE)))
cat(sprintf("  AIC:    %.4f%%\n", mean(abs(comp_results$pct_diff_aic), na.rm = TRUE)))
cat(sprintf("  BIC:    %.4f%%\n", mean(abs(comp_results$pct_diff_bic), na.rm = TRUE)))

# Verificar se diferencas estao dentro de limites aceitaveis (< 1%)
max_diff <- max(
  abs(comp_params$pct_diff_omega),
  abs(comp_params$pct_diff_alpha1),
  abs(comp_params$pct_diff_beta1),
  abs(comp_params$pct_diff_gamma1),
  na.rm = TRUE
)

if (max_diff < 1.0) {
  cat("\n>>> RESULTADO: Diferencas dentro do limite aceitavel (< 1%) <<<\n")
} else if (max_diff < 5.0) {
  cat(sprintf("\n>>> RESULTADO: Algumas diferencas moderadas (max=%.2f%%) <<<\n", max_diff))
  cat("    Diferente metodos de otimizacao podem causar pequenas variacoes.\n")
} else {
  cat(sprintf("\n>>> ATENCAO: Diferencas significativas encontradas (max=%.2f%%) <<<\n", max_diff))
  cat("    Verifique as configuracoes dos modelos e dados de entrada.\n")
}

cat("\n=== Comparacao concluida! ===\n")
