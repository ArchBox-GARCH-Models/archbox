###############################################################################
# validation_05_ms.R
# Validacao cruzada: archbox (Python) vs MSwM (R) - Modelos Markov-Switching
#
# Este script estima um modelo MS(2) com medias e variancias por regime
# usando o pacote MSwM nos mesmos dados de PIB usados pela archbox.
# Os resultados sao salvos em CSV para comparacao automatizada.
#
# Modelo estimado:
#   MS(2)-Mean: 2 regimes com intercepto e variancia que mudam entre regimes
#
# Pacotes necessarios: MSwM, readr
#
# Uso: cd examples/04_regime_switching/R && Rscript validation_05_ms.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(MSwM)
library(readr)

cat("=== Validacao R: Markov-Switching MS(2) com MSwM ===\n\n")

# --- Definir diretorios relativos ao script ---
data_dir   <- "../data"
output_dir <- "../outputs"

# Criar diretorio de saida se nao existir
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

###############################################################################
# ETAPA 1: Carregar dados de PIB trimestral
###############################################################################

cat("--- Etapa 1: Carregando dados ---\n")

gdp <- read_csv(file.path(data_dir, "us_gdp_growth.csv"), show_col_types = FALSE)

cat(sprintf("  Dimensoes: %d observacoes\n", nrow(gdp)))
cat(sprintf("  Periodo: %s a %s\n", min(gdp$date), max(gdp$date)))
cat(sprintf("  Media do crescimento: %.4f\n", mean(gdp$gdp_growth)))
cat(sprintf("  Desvio padrao: %.4f\n", sd(gdp$gdp_growth)))
cat("\n")

# Converter para serie temporal trimestral
y <- ts(gdp$gdp_growth, frequency = 4, start = c(1962, 1))

###############################################################################
# ETAPA 2: Estimar modelo linear base com lm()
###############################################################################

cat("--- Etapa 2: Estimando modelo linear base ---\n")

# Modelo de media (intercepto apenas - sem regressores)
lm_model <- lm(gdp_growth ~ 1, data = gdp)

cat("  Resumo do modelo linear base:\n")
cat(sprintf("    Intercepto (media global): %.6f\n", coef(lm_model)[1]))
cat(sprintf("    Desvio padrao residuos:    %.6f\n", summary(lm_model)$sigma))
cat("\n")

###############################################################################
# ETAPA 3: Estimar MS(2) com msmFit
###############################################################################

cat("--- Etapa 3: Estimando MS(2) com msmFit ---\n")

# sw = c(TRUE, TRUE) => intercepto e variancia mudam entre regimes
# k = 2 => dois regimes (expansao e recessao)
# p = 0 => sem termos autorregressivos (modelo MS-Mean)
# control = list(parallel = FALSE) para garantir reprodutibilidade
ms_fit <- tryCatch({
  msmFit(lm_model, k = 2, sw = c(TRUE, TRUE), control = list(parallel = FALSE))
}, error = function(e) {
  cat(sprintf("  ERRO na estimacao MS(2): %s\n", e$message))
  cat("  Tentando com parametros alternativos...\n")
  # Tentativa alternativa com sw incluindo regressores
  tryCatch({
    msmFit(lm_model, k = 2, sw = c(TRUE, TRUE), p = 0,
           control = list(parallel = FALSE))
  }, error = function(e2) {
    cat(sprintf("  ERRO na segunda tentativa: %s\n", e2$message))
    NULL
  })
})

if (is.null(ms_fit)) {
  cat("ERRO: Nao foi possivel estimar o modelo MS(2). Abortando.\n")
  quit(status = 1)
}

cat("  Modelo MS(2) estimado com sucesso!\n\n")

# Exibir resumo completo
cat("--- Resumo do modelo MS(2) ---\n")
summary(ms_fit)
cat("\n")

###############################################################################
# ETAPA 4: Extrair parametros por regime
###############################################################################

cat("--- Etapa 4: Extraindo parametros por regime ---\n")

# Coeficientes por regime (intercepto = media de cada regime)
coefs <- coef(ms_fit)
cat("  Coeficientes por regime:\n")
print(coefs)
cat("\n")

# Media (intercepto) de cada regime
mu_regime1 <- coefs[1, 1]
mu_regime2 <- coefs[2, 1]

cat(sprintf("  mu (Regime 1): %.6f\n", mu_regime1))
cat(sprintf("  mu (Regime 2): %.6f\n", mu_regime2))

# Desvio padrao de cada regime
sigma_regime1 <- ms_fit@std[1]
sigma_regime2 <- ms_fit@std[2]

cat(sprintf("  sigma (Regime 1): %.6f\n", sigma_regime1))
cat(sprintf("  sigma (Regime 2): %.6f\n", sigma_regime2))
cat("\n")

# Identificar regimes: regime de baixa volatilidade (expansao) vs alta (recessao)
if (sigma_regime1 < sigma_regime2) {
  cat("  Regime 1 -> Baixa volatilidade (expansao)\n")
  cat("  Regime 2 -> Alta volatilidade (recessao)\n")
} else {
  cat("  Regime 1 -> Alta volatilidade (recessao)\n")
  cat("  Regime 2 -> Baixa volatilidade (expansao)\n")
}
cat("\n")

###############################################################################
# ETAPA 5: Extrair e salvar matriz de transicao
###############################################################################

cat("--- Etapa 5: Extraindo matriz de transicao ---\n")

trans_mat <- ms_fit@transMat

cat("  Matriz de transicao:\n")
cat(sprintf("    P(1->1) = %.6f    P(1->2) = %.6f\n", trans_mat[1, 1], trans_mat[1, 2]))
cat(sprintf("    P(2->1) = %.6f    P(2->2) = %.6f\n", trans_mat[2, 1], trans_mat[2, 2]))
cat("\n")

# Probabilidade de permanencia em cada regime
p11 <- trans_mat[1, 1]
p22 <- trans_mat[2, 2]

cat(sprintf("  Probabilidade de permanencia no Regime 1: %.6f\n", p11))
cat(sprintf("  Probabilidade de permanencia no Regime 2: %.6f\n", p22))
cat("\n")

###############################################################################
# ETAPA 6: Calcular duracao esperada de cada regime
###############################################################################

cat("--- Etapa 6: Duracao esperada de cada regime ---\n")

# Duracao esperada = 1 / (1 - p_ii), onde p_ii e a probabilidade de permanencia
dur_regime1 <- 1 / (1 - p11)
dur_regime2 <- 1 / (1 - p22)

cat(sprintf("  Duracao esperada Regime 1: %.2f trimestres (%.1f anos)\n",
            dur_regime1, dur_regime1 / 4))
cat(sprintf("  Duracao esperada Regime 2: %.2f trimestres (%.1f anos)\n",
            dur_regime2, dur_regime2 / 4))
cat("\n")

###############################################################################
# ETAPA 7: Extrair e salvar probabilidades suavizadas
###############################################################################

cat("--- Etapa 7: Extraindo probabilidades suavizadas ---\n")

smooth_probs <- ms_fit@Fit@smoProb

cat(sprintf("  Dimensoes das probabilidades suavizadas: %d x %d\n",
            nrow(smooth_probs), ncol(smooth_probs)))

# Criar data.frame com probabilidades suavizadas
# A matriz tem T linhas e k colunas (probabilidade de cada regime em cada t)
probs_df <- data.frame(
  date = gdp$date,
  prob_regime1 = smooth_probs[, 1],
  prob_regime2 = smooth_probs[, 2]
)

# Salvar probabilidades suavizadas em CSV
probs_file <- file.path(output_dir, "r_validation_ms_probs.csv")
write_csv(probs_df, probs_file)
cat(sprintf("  Probabilidades suavizadas salvas em: %s\n", probs_file))

# Estatisticas resumo das probabilidades
cat(sprintf("  Prob media Regime 1: %.4f\n", mean(probs_df$prob_regime1)))
cat(sprintf("  Prob media Regime 2: %.4f\n", mean(probs_df$prob_regime2)))

# Fracao do tempo em cada regime (baseado na classificacao mais provavel)
regime_class <- ifelse(smooth_probs[, 1] > 0.5, 1, 2)
cat(sprintf("  Fracao em Regime 1: %.1f%%\n", 100 * mean(regime_class == 1)))
cat(sprintf("  Fracao em Regime 2: %.1f%%\n", 100 * mean(regime_class == 2)))
cat("\n")

###############################################################################
# ETAPA 8: Salvar resultados consolidados
###############################################################################

cat("--- Etapa 8: Salvando resultados consolidados ---\n")

# Tabela de parametros por regime
results <- data.frame(
  regime           = c(1, 2),
  mu               = c(mu_regime1, mu_regime2),
  sigma            = c(sigma_regime1, sigma_regime2),
  p_stay           = c(p11, p22),
  expected_duration = c(dur_regime1, dur_regime2),
  stringsAsFactors = FALSE
)

results_file <- file.path(output_dir, "r_validation_ms_results.csv")
write_csv(results, results_file)
cat(sprintf("  Parametros por regime salvos em: %s\n", results_file))

# Salvar matriz de transicao
trans_df <- data.frame(
  from_regime = c(1, 1, 2, 2),
  to_regime   = c(1, 2, 1, 2),
  probability = c(trans_mat[1, 1], trans_mat[1, 2],
                  trans_mat[2, 1], trans_mat[2, 2])
)
trans_file <- file.path(output_dir, "r_validation_ms_transition.csv")
write_csv(trans_df, trans_file)
cat(sprintf("  Matriz de transicao salva em: %s\n", trans_file))

cat("\n")

###############################################################################
# ETAPA 9: Exibir resumo para comparacao com archbox
###############################################################################

cat("=== Resumo para comparacao com archbox ===\n\n")

cat("  Parametros por regime:\n")
cat(sprintf("    Regime 1: mu=%.6f, sigma=%.6f\n", mu_regime1, sigma_regime1))
cat(sprintf("    Regime 2: mu=%.6f, sigma=%.6f\n", mu_regime2, sigma_regime2))
cat("\n")

cat("  Matriz de transicao:\n")
cat(sprintf("    | %.6f  %.6f |\n", trans_mat[1, 1], trans_mat[1, 2]))
cat(sprintf("    | %.6f  %.6f |\n", trans_mat[2, 1], trans_mat[2, 2]))
cat("\n")

cat("  Duracao esperada:\n")
cat(sprintf("    Regime 1: %.2f trimestres\n", dur_regime1))
cat(sprintf("    Regime 2: %.2f trimestres\n", dur_regime2))
cat("\n")

# Nota sobre comparacao
cat("  NOTA: Os resultados da archbox devem ser comparados considerando que:\n")
cat("    - A rotulacao dos regimes pode ser invertida (regime 1 <-> regime 2)\n")
cat("    - Pequenas diferencas nos parametros sao esperadas devido a\n")
cat("      diferentes algoritmos de otimizacao (EM vs quasi-Newton)\n")
cat("    - O criterio de convergencia pode afetar os resultados finais\n")
cat("    - A variancia (sigma^2) da archbox corresponde a sigma^2 do MSwM\n")
cat("\n")

cat("=== Validacao MS(2) concluida com sucesso! ===\n")
