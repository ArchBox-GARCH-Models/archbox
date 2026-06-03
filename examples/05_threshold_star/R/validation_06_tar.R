###############################################################################
# validation_06_tar.R
# Validacao cruzada: archbox (Python) vs tsDyn (R) - Modelos TAR/SETAR e STAR
#
# Este script estima modelos SETAR e LSTAR nos mesmos dados de PIB
# usados pela archbox, usando o pacote tsDyn como referencia.
# Os resultados sao salvos em CSV para comparacao automatizada.
#
# Modelos estimados:
#   SETAR(1): Self-Exciting TAR com 1 threshold e 1 lag
#   LSTAR(1): Logistic Smooth Transition AR com 1 lag
#
# Testes realizados:
#   setarTest: teste de linearidade contra alternativa threshold
#   linearity.test: teste LM de linearidade contra alternativa STAR
#
# Pacotes necessarios: tsDyn, readr
#
# Uso: cd examples/05_threshold_star/R && Rscript validation_06_tar.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(tsDyn)
library(readr)

cat("=== Validacao R: TAR/SETAR e LSTAR com tsDyn ===\n\n")

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
cat(sprintf("  Media do crescimento: %.4f\n", mean(gdp$y)))
cat(sprintf("  Desvio padrao: %.4f\n", sd(gdp$y)))
cat("\n")

# Extrair serie como vetor numerico
y <- gdp$y

###############################################################################
# ETAPA 2: Estimar modelo SETAR com 1 threshold
###############################################################################

cat("--- Etapa 2: Estimando modelo SETAR(1) ---\n")

# setar: estima Self-Exciting TAR com m lags e nthresh thresholds
# m = 1: um lag autorregressivo
# thDelay = 0: variavel threshold e y_{t-1} (primeiro lag)
# nthresh = 1: um unico threshold dividindo a serie em 2 regimes
setar_fit <- setar(y, m = 1, thDelay = 0, nthresh = 1)

cat("  Resumo do modelo SETAR:\n")
print(summary(setar_fit))
cat("\n")

# Extrair valor do threshold estimado
th <- getTh(setar_fit)
cat(sprintf("  Threshold estimado (c): %.6f\n", th))

# Extrair coeficientes por regime
# Regime baixo (y_{t-1} <= c): intercepto e coeficiente do lag
coefs_all <- coef(setar_fit)
cat("  Coeficientes completos:\n")
print(coefs_all)
cat("\n")

# Separar coeficientes por regime
# tsDyn nomeia: const.L, phiL.1 (regime baixo), const.H, phiH.1 (regime alto)
coefs_low  <- coefs_all[grep("L", names(coefs_all))]
coefs_high <- coefs_all[grep("H", names(coefs_all))]

cat("  Coeficientes Regime Baixo (y_{t-1} <= c):\n")
cat(sprintf("    Intercepto: %.6f\n", coefs_low[1]))
cat(sprintf("    phi_1:      %.6f\n", coefs_low[2]))

cat("  Coeficientes Regime Alto (y_{t-1} > c):\n")
cat(sprintf("    Intercepto: %.6f\n", coefs_high[1]))
cat(sprintf("    phi_1:      %.6f\n", coefs_high[2]))
cat("\n")

# Criterios de informacao do SETAR
aic_setar <- AIC(setar_fit)
bic_setar <- BIC(setar_fit)
cat(sprintf("  AIC (SETAR): %.4f\n", aic_setar))
cat(sprintf("  BIC (SETAR): %.4f\n", bic_setar))
cat("\n")

###############################################################################
# ETAPA 3: Estimar modelo LSTAR
###############################################################################

cat("--- Etapa 3: Estimando modelo LSTAR ---\n")

# lstar: estima Logistic Smooth Transition AR
# m = 1: um lag autorregressivo
# thDelay = 0: variavel de transicao e y_{t-1}
# A funcao de transicao logistica e: G(y_{t-1}; gamma, c) = 1 / (1 + exp(-gamma * (y_{t-1} - c)))
lstar_fit <- tryCatch({
  lstar(y, m = 1, thDelay = 0)
}, error = function(e) {
  cat(sprintf("  AVISO: lstar falhou com m=1, thDelay=0: %s\n", e$message))
  cat("  Tentando com starting.control ajustado...\n")
  tryCatch({
    lstar(y, m = 1, thDelay = 0,
          starting.control = list(gammaInt = c(1, 20), nTh = 100))
  }, error = function(e2) {
    cat(sprintf("  ERRO: lstar falhou novamente: %s\n", e2$message))
    NULL
  })
})

if (!is.null(lstar_fit)) {
  cat("  Resumo do modelo LSTAR:\n")
  print(summary(lstar_fit))
  cat("\n")

  # Extrair parametros da funcao de transicao
  lstar_coefs <- coef(lstar_fit)
  cat("  Coeficientes completos do LSTAR:\n")
  print(lstar_coefs)
  cat("\n")

  # Extrair gamma (velocidade de transicao) e c (threshold)
  gamma_val <- lstar_coefs["gamma"]
  c_val     <- lstar_coefs["th"]

  cat(sprintf("  Gamma (velocidade de transicao): %.6f\n", gamma_val))
  cat(sprintf("  Threshold (c): %.6f\n", c_val))

  # Coeficientes dos regimes extremos do LSTAR
  # phi1._ sao os coeficientes do regime "linear" (G=0)
  # phi2._ sao os coeficientes adicionais quando G=1
  cat("  Coeficientes do regime linear (G=0):\n")
  phi1_names <- grep("^phi1", names(lstar_coefs), value = TRUE)
  for (nm in phi1_names) {
    cat(sprintf("    %s: %.6f\n", nm, lstar_coefs[nm]))
  }

  cat("  Coeficientes adicionais no regime nao-linear (G=1):\n")
  phi2_names <- grep("^phi2", names(lstar_coefs), value = TRUE)
  for (nm in phi2_names) {
    cat(sprintf("    %s: %.6f\n", nm, lstar_coefs[nm]))
  }
  cat("\n")

  # Criterios de informacao do LSTAR
  aic_lstar <- AIC(lstar_fit)
  bic_lstar <- BIC(lstar_fit)
  cat(sprintf("  AIC (LSTAR): %.4f\n", aic_lstar))
  cat(sprintf("  BIC (LSTAR): %.4f\n", bic_lstar))
  cat("\n")
} else {
  cat("  AVISO: Modelo LSTAR nao pode ser estimado. Resultados parciais.\n")
  gamma_val <- NA
  c_val     <- NA
  aic_lstar <- NA
  bic_lstar <- NA
  cat("\n")
}

###############################################################################
# ETAPA 4: Teste de linearidade - setarTest (threshold)
###############################################################################

cat("--- Etapa 4: Teste de linearidade - setarTest ---\n")

# setarTest: testa H0 (linearidade) contra H1 (SETAR com 1 threshold)
# test = "1vs": testa 1 regime vs 2 regimes
# nboot = 1000: numero de replicacoes bootstrap para p-valor
cat("  Executando setarTest (pode demorar devido ao bootstrap)...\n")

setar_test <- tryCatch({
  setarTest(y, m = 1, nthresh = 1, test = "1vs", nboot = 1000)
}, error = function(e) {
  cat(sprintf("  ERRO no setarTest: %s\n", e$message))
  NULL
})

if (!is.null(setar_test)) {
  cat("  Resultado do teste de threshold (setarTest):\n")
  print(setar_test)
  cat("\n")

  # Extrair estatistica de teste e p-valor
  # O objeto retornado por setarTest contem $SSR_1vs (ou similar)
  setar_test_stat <- setar_test$statistic
  setar_test_pval <- setar_test$p.value

  cat(sprintf("  Estatistica de teste: %.4f\n", setar_test_stat))
  cat(sprintf("  P-valor (bootstrap): %.4f\n", setar_test_pval))

  if (setar_test_pval < 0.05) {
    cat("  -> Rejeita H0 de linearidade ao nivel de 5%% (evidencia de threshold)\n")
  } else {
    cat("  -> Nao rejeita H0 de linearidade ao nivel de 5%%\n")
  }
} else {
  setar_test_stat <- NA
  setar_test_pval <- NA
}
cat("\n")

###############################################################################
# ETAPA 5: Teste de linearidade - linearity.test (LM-STAR)
###############################################################################

cat("--- Etapa 5: Teste LM de linearidade contra STAR ---\n")

# linearity.test: testa H0 (linearidade) contra H1 (LSTAR)
# Baseado no teste LM de Luukkonen, Saikkonen e Terasvirta (1988)
star_test <- tryCatch({
  linearity.test(y, type = "LSTAR", m = 1)
}, error = function(e) {
  cat(sprintf("  ERRO no linearity.test: %s\n", e$message))
  # Tentativa alternativa usando a funcao star com teste embutido
  tryCatch({
    linearity.test(ts(y), type = "LSTAR", m = 1)
  }, error = function(e2) {
    cat(sprintf("  ERRO na segunda tentativa: %s\n", e2$message))
    NULL
  })
})

if (!is.null(star_test)) {
  cat("  Resultado do teste LM-STAR (linearity.test):\n")
  print(star_test)
  cat("\n")

  # Extrair estatistica F e p-valor
  star_test_stat <- star_test$statistic
  star_test_pval <- star_test$p.value

  cat(sprintf("  Estatistica de teste (F): %.4f\n", star_test_stat))
  cat(sprintf("  P-valor: %.4f\n", star_test_pval))

  if (star_test_pval < 0.05) {
    cat("  -> Rejeita H0 de linearidade ao nivel de 5%% (evidencia de nao-linearidade STAR)\n")
  } else {
    cat("  -> Nao rejeita H0 de linearidade ao nivel de 5%%\n")
  }
} else {
  star_test_stat <- NA
  star_test_pval <- NA
}
cat("\n")

###############################################################################
# ETAPA 6: Salvar resultados consolidados em CSV
###############################################################################

cat("--- Etapa 6: Salvando resultados consolidados ---\n")

# Tabela principal com modelos e parametros
results <- data.frame(
  model       = c("SETAR", "LSTAR"),
  threshold_c = c(th, ifelse(is.na(c_val), NA, c_val)),
  gamma       = c(NA, ifelse(is.na(gamma_val), NA, gamma_val)),
  aic         = c(aic_setar, ifelse(is.na(aic_lstar), NA, aic_lstar)),
  bic         = c(bic_setar, ifelse(is.na(bic_lstar), NA, bic_lstar)),
  stringsAsFactors = FALSE
)

results_file <- file.path(output_dir, "r_validation_tar_results.csv")
write_csv(results, results_file)
cat(sprintf("  Resultados dos modelos salvos em: %s\n", results_file))

# Tabela de coeficientes por regime do SETAR
setar_coefs_df <- data.frame(
  regime      = c("baixo", "baixo", "alto", "alto"),
  parametro   = c("intercepto", "phi_1", "intercepto", "phi_1"),
  valor       = c(coefs_low[1], coefs_low[2], coefs_high[1], coefs_high[2]),
  stringsAsFactors = FALSE
)

coefs_file <- file.path(output_dir, "r_validation_tar_coefs.csv")
write_csv(setar_coefs_df, coefs_file)
cat(sprintf("  Coeficientes por regime salvos em: %s\n", coefs_file))

# Tabela de testes de linearidade
tests <- data.frame(
  teste      = c("setarTest", "linearity.test_LSTAR"),
  estatistica = c(ifelse(is.na(setar_test_stat), NA, setar_test_stat),
                  ifelse(is.na(star_test_stat), NA, star_test_stat)),
  p_valor    = c(ifelse(is.na(setar_test_pval), NA, setar_test_pval),
                 ifelse(is.na(star_test_pval), NA, star_test_pval)),
  stringsAsFactors = FALSE
)

tests_file <- file.path(output_dir, "r_validation_tar_tests.csv")
write_csv(tests, tests_file)
cat(sprintf("  Resultados dos testes salvos em: %s\n", tests_file))
cat("\n")

###############################################################################
# ETAPA 7: Resumo para comparacao com archbox
###############################################################################

cat("=== Resumo para comparacao com archbox ===\n\n")

cat("  Modelo SETAR:\n")
cat(sprintf("    Threshold (c): %.6f\n", th))
cat(sprintf("    Regime Baixo: intercepto=%.6f, phi_1=%.6f\n",
            coefs_low[1], coefs_low[2]))
cat(sprintf("    Regime Alto:  intercepto=%.6f, phi_1=%.6f\n",
            coefs_high[1], coefs_high[2]))
cat(sprintf("    AIC=%.4f, BIC=%.4f\n", aic_setar, bic_setar))
cat("\n")

if (!is.null(lstar_fit)) {
  cat("  Modelo LSTAR:\n")
  cat(sprintf("    Gamma (velocidade): %.6f\n", gamma_val))
  cat(sprintf("    Threshold (c): %.6f\n", c_val))
  cat(sprintf("    AIC=%.4f, BIC=%.4f\n", aic_lstar, bic_lstar))
  cat("\n")
}

cat("  Testes de linearidade:\n")
if (!is.na(setar_test_pval)) {
  cat(sprintf("    setarTest p-valor: %.4f\n", setar_test_pval))
}
if (!is.na(star_test_pval)) {
  cat(sprintf("    linearity.test (LSTAR) p-valor: %.4f\n", star_test_pval))
}
cat("\n")

# Nota sobre comparacao
cat("  NOTA: Os resultados da archbox devem ser comparados considerando que:\n")
cat("    - Pequenas diferencas nos parametros sao esperadas devido a\n")
cat("      diferentes algoritmos de otimizacao\n")
cat("    - O threshold estimado pode diferir ligeiramente pela discretizacao\n")
cat("      do grid de busca no SETAR\n")
cat("    - O gamma do LSTAR depende da escala e pode diferir se a\n")
cat("      parametrizacao for diferente\n")
cat("    - Os criterios AIC/BIC podem usar convencoes diferentes\n")
cat("      (e.g., log-verossimilhanca concentrada vs completa)\n")
cat("\n")

cat("=== Validacao TAR/SETAR e LSTAR concluida com sucesso! ===\n")
