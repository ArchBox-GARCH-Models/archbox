###############################################################################
# validation_diagnostics.R
# Validacao cruzada: archbox (Python) vs rugarch (R) - Diagnosticos
#
# Este script estima modelos GARCH(1,1), EGARCH(1,1) e GJR-GARCH(1,1) com
# rugarch e executa testes de diagnostico:
#   - Sign bias test (Engle-Ng, 1993)
#   - Nyblom stability test
#   - News impact curve
#   - Criterios de informacao (AIC, BIC)
#
# Resultados sao salvos em CSV para comparacao com a archbox.
#
# Uso: Rscript validation_diagnostics.R
###############################################################################

# --- Carregar pacotes necessarios ---
library(rugarch)
library(readr)

cat("=== Validacao R: Diagnosticos de Modelos GARCH ===\n\n")

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
# Etapa 1: Estimacao dos modelos GARCH(1,1), EGARCH(1,1) e GJR-GARCH(1,1)
###############################################################################

cat("--- Etapa 1: Estimacao dos modelos ---\n")

# GARCH(1,1) com distribuicao normal
spec_garch <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "norm"
)
fit_garch <- ugarchfit(spec_garch, returns)
cat("  GARCH(1,1) estimado com sucesso\n")

# EGARCH(1,1) com distribuicao normal
spec_egarch <- ugarchspec(
  variance.model = list(model = "eGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "norm"
)
fit_egarch <- ugarchfit(spec_egarch, returns)
cat("  EGARCH(1,1) estimado com sucesso\n")

# GJR-GARCH(1,1) com distribuicao normal
spec_gjr <- ugarchspec(
  variance.model = list(model = "gjrGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "norm"
)
fit_gjr <- ugarchfit(spec_gjr, returns)
cat("  GJR-GARCH(1,1) estimado com sucesso\n\n")

###############################################################################
# Etapa 2: Sign Bias Test (Engle-Ng, 1993)
#
# O teste de sign bias verifica se choques positivos e negativos tem impacto
# assimetrico na volatilidade, o que modelos simetricos como GARCH nao capturam.
# Componentes:
#   - Sign Bias: verifica se o sinal do choque importa
#   - Negative Size Bias: verifica se a magnitude de choques negativos importa
#   - Positive Size Bias: verifica se a magnitude de choques positivos importa
#   - Joint Effect: teste conjunto dos 3 efeitos acima
###############################################################################

cat("--- Etapa 2: Sign Bias Test ---\n")

# Executar sign bias test para os 3 modelos
sb_garch <- signbias(fit_garch)
cat("  Sign bias - GARCH: concluido\n")

sb_egarch <- signbias(fit_egarch)
cat("  Sign bias - EGARCH: concluido\n")

sb_gjr <- signbias(fit_gjr)
cat("  Sign bias - GJR: concluido\n")

# Combinar resultados dos 3 modelos em um unico data.frame
# signbias() retorna data.frame com colunas: t-value, prob
# e linhas: Sign Bias, Negative Size Bias, Positive Size Bias, Joint Effect
sb_results <- rbind(
  cbind(model = "GARCH", test = rownames(sb_garch), sb_garch),
  cbind(model = "EGARCH", test = rownames(sb_egarch), sb_egarch),
  cbind(model = "GJR", test = rownames(sb_gjr), sb_gjr)
)
rownames(sb_results) <- NULL

# Salvar resultados do sign bias
write_csv(sb_results, file.path(output_dir, "r_signbias_results.csv"))
cat("  Resultados salvos em r_signbias_results.csv\n")

# Exibir resumo
cat("\n  Sign Bias Test - Resumo:\n")
for (m in c("GARCH", "EGARCH", "GJR")) {
  subset_m <- sb_results[sb_results$model == m, ]
  cat(sprintf("    %s:\n", m))
  for (i in 1:nrow(subset_m)) {
    sig <- ifelse(subset_m$prob[i] < 0.05, " *", "")
    cat(sprintf("      %-22s t=%.4f  p=%.4f%s\n",
                subset_m$test[i], subset_m$`t-value`[i], subset_m$prob[i], sig))
  }
}
cat("\n")

###############################################################################
# Etapa 3: Nyblom Stability Test
#
# O teste de Nyblom avalia se os parametros do modelo sao estaveis ao longo
# do tempo. Estatisticas individuais testam cada parametro separadamente,
# enquanto a estatistica conjunta (joint) testa estabilidade de todos juntos.
# Valores criticos de Hansen (1990) sao usados para inferencia.
###############################################################################

cat("--- Etapa 3: Nyblom Stability Test ---\n")

# Executar teste de Nyblom para o modelo GARCH(1,1)
nyb_garch <- nyblom(fit_garch)

# Construir data.frame com estatisticas individuais
nyb_results <- data.frame(
  parameter = names(nyb_garch$IndividualStat),
  statistic = as.numeric(nyb_garch$IndividualStat),
  critical_10 = nyb_garch$IndividualCritical[1],
  critical_5 = nyb_garch$IndividualCritical[2]
)

# Adicionar estatistica conjunta (joint)
nyb_results <- rbind(nyb_results, data.frame(
  parameter = "Joint",
  statistic = as.numeric(nyb_garch$JointStat),
  critical_10 = nyb_garch$JointCritical[1],
  critical_5 = nyb_garch$JointCritical[2]
))

# Salvar resultados do Nyblom
write_csv(nyb_results, file.path(output_dir, "r_nyblom_results.csv"))
cat("  Resultados salvos em r_nyblom_results.csv\n")

# Exibir resumo
cat("\n  Nyblom Stability Test - GARCH(1,1):\n")
for (i in 1:nrow(nyb_results)) {
  sig <- ifelse(nyb_results$statistic[i] > nyb_results$critical_5[i], " **",
                ifelse(nyb_results$statistic[i] > nyb_results$critical_10[i], " *", ""))
  cat(sprintf("    %-12s stat=%.4f  cv10%%=%.4f  cv5%%=%.4f%s\n",
              nyb_results$parameter[i], nyb_results$statistic[i],
              nyb_results$critical_10[i], nyb_results$critical_5[i], sig))
}
cat("\n")

###############################################################################
# Etapa 4: News Impact Curve (NIC)
#
# A NIC mostra como choques (eps) de diferentes magnitudes e sinais afetam
# a variancia condicional. Modelos assimetricos (EGARCH, GJR) produzem
# curvas assimetricas, enquanto GARCH produz curva simetrica.
# newsimpact() retorna: $zx (valores de eps) e $zy (variancia resultante)
###############################################################################

cat("--- Etapa 4: News Impact Curve ---\n")

# Extrair dados da NIC para os 3 modelos
nic_garch <- newsimpact(fit_garch)
nic_egarch <- newsimpact(fit_egarch)
nic_gjr <- newsimpact(fit_gjr)

# Combinar em um data.frame: eps e sigma2 para cada modelo
nic_data <- data.frame(
  eps = nic_garch$zx,
  garch = nic_garch$zy,
  egarch = nic_egarch$zy,
  gjr = nic_gjr$zy
)

# Salvar dados da NIC
write_csv(nic_data, file.path(output_dir, "r_nic_data.csv"))
cat("  Dados da NIC salvos em r_nic_data.csv\n")
cat(sprintf("  NIC: %d pontos por modelo\n\n", nrow(nic_data)))

###############################################################################
# Etapa 5: Criterios de Informacao (AIC, BIC)
#
# infocriteria() retorna vetor com 4 criterios:
#   [1] AIC (Akaike), [2] BIC (Bayes/Schwarz),
#   [3] Shibata, [4] Hannan-Quinn
# AIC e BIC sao os mais utilizados para selecao de modelos.
# Menores valores indicam melhor ajuste relativo.
###############################################################################

cat("--- Etapa 5: Criterios de Informacao ---\n")

# Extrair AIC e BIC para os 3 modelos
ic <- data.frame(
  model = c("GARCH", "EGARCH", "GJR"),
  aic = c(infocriteria(fit_garch)[1], infocriteria(fit_egarch)[1], infocriteria(fit_gjr)[1]),
  bic = c(infocriteria(fit_garch)[2], infocriteria(fit_egarch)[2], infocriteria(fit_gjr)[2]),
  shibata = c(infocriteria(fit_garch)[3], infocriteria(fit_egarch)[3], infocriteria(fit_gjr)[3]),
  hannan_quinn = c(infocriteria(fit_garch)[4], infocriteria(fit_egarch)[4], infocriteria(fit_gjr)[4])
)

# Salvar criterios de informacao
write_csv(ic, file.path(output_dir, "r_infocriteria_results.csv"))
cat("  Resultados salvos em r_infocriteria_results.csv\n")

# Exibir resumo
cat("\n  Criterios de Informacao:\n")
cat(sprintf("    %-8s  AIC=%.6f  BIC=%.6f\n", ic$model[1], ic$aic[1], ic$bic[1]))
cat(sprintf("    %-8s  AIC=%.6f  BIC=%.6f\n", ic$model[2], ic$aic[2], ic$bic[2]))
cat(sprintf("    %-8s  AIC=%.6f  BIC=%.6f\n", ic$model[3], ic$aic[3], ic$bic[3]))

# Identificar melhor modelo por AIC e BIC
best_aic <- ic$model[which.min(ic$aic)]
best_bic <- ic$model[which.min(ic$bic)]
cat(sprintf("\n  Melhor modelo por AIC: %s\n", best_aic))
cat(sprintf("  Melhor modelo por BIC: %s\n\n", best_bic))

###############################################################################
# Resumo final
###############################################################################

cat("=== Validacao concluida ===\n")
cat("Arquivos gerados em ../outputs/:\n")
cat("  - r_signbias_results.csv      (sign bias test - 3 modelos)\n")
cat("  - r_nyblom_results.csv        (Nyblom stability test - GARCH)\n")
cat("  - r_nic_data.csv              (news impact curve - 3 modelos)\n")
cat("  - r_infocriteria_results.csv  (AIC, BIC - 3 modelos)\n")
