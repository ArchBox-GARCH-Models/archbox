###############################################################################
# full_comparison.R
# Validacao cruzada completa: archbox vs rugarch/rmgarch
#
# Este script executa o pipeline completo de modelagem de volatilidade:
#   1. Estimacao de 6 modelos GARCH univariados
#   2. Tabela comparativa (AIC, BIC, log-likelihood)
#   3. Diagnosticos: sign bias e teste de Nyblom
#   4. Rolling VaR backtest com ugarchroll
#   5. Teste de Kupiec para VaR 95% e 99%
#   6. DCC multivariado em 4 series FX
#   7. VaR do portfolio com pesos iguais
#   8. Exportacao de todos os resultados em CSV
#
# Uso: Rscript full_comparison.R
# Executar a partir do diretorio R/ do projeto
###############################################################################

# --- Carregamento de pacotes ---
# rugarch: modelos GARCH univariados, VaR, backtesting
# rmgarch: modelos DCC/CCC multivariados
# readr: leitura e escrita de CSVs
# dplyr: manipulacao de dados
library(rugarch)
library(rmgarch)
library(readr)
library(dplyr)

cat("=============================================================\n")
cat("  Validacao Completa: rugarch + rmgarch\n")
cat("  Comparacao ponto-a-ponto com archbox\n")
cat("=============================================================\n\n")

# --- Criar diretorio de saida se nao existir ---
output_dir <- "../outputs"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

###############################################################################
# SECAO 1: MODELOS GARCH UNIVARIADOS
# Estimamos 6 especificacoes diferentes usando retornos do S&P 500
###############################################################################

cat(">>> Secao 1: Estimando 6 modelos GARCH univariados...\n")

# Leitura dos retornos do S&P 500
returns_df <- read_csv("../data/sp500_returns.csv", show_col_types = FALSE)
returns <- returns_df$returns

cat(sprintf("    Numero de observacoes: %d\n", length(returns)))
cat(sprintf("    Media dos retornos: %.6f\n", mean(returns)))
cat(sprintf("    Desvio padrao: %.6f\n", sd(returns)))

# Definicao dos 6 modelos a serem estimados
# sGARCH:    GARCH padrao (Bollerslev, 1986)
# eGARCH:    GARCH exponencial (Nelson, 1991)
# gjrGARCH:  GJR-GARCH com efeito de alavancagem (Glosten et al., 1993)
# apARCH:    Asymmetric Power ARCH (Ding et al., 1993)
# iGARCH:    Integrated GARCH (Engle & Bollerslev, 1986)
# csGARCH:   Component GARCH com componente de longo prazo (Engle & Lee, 1999)
models <- c("sGARCH", "eGARCH", "gjrGARCH", "apARCH", "iGARCH", "csGARCH")

# Lista para armazenar todos os resultados
results <- list()
fit_objects <- list()

for (m in models) {
  cat(sprintf("    Estimando modelo: %s...\n", m))

  # Especificacao do modelo:
  # - Ordem GARCH(1,1)
  # - Media com constante (sem ARMA)
  # - Distribuicao t de Student (caudas pesadas)
  spec <- ugarchspec(
    variance.model = list(model = m, garchOrder = c(1, 1)),
    mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
    distribution.model = "std"
  )

  # Estimacao usando solver hibrido (mais robusto)
  fit <- tryCatch(
    ugarchfit(spec, returns, solver = "hybrid"),
    error = function(e) {
      cat(sprintf("    AVISO: Erro ao estimar %s: %s\n", m, e$message))
      return(NULL)
    }
  )

  if (!is.null(fit)) {
    # Armazenar objeto fit para uso posterior
    fit_objects[[m]] <- fit

    # Extrair coeficientes estimados
    coefs <- coef(fit)

    # Calcular log-verossimilhanca e criterios de informacao
    ll <- likelihood(fit)
    ic <- infocriteria(fit)

    # Executar teste de sign bias (Engle & Ng, 1993)
    # Verifica se choques positivos e negativos tem efeitos diferentes na volatilidade
    sb <- signbias(fit)

    # Executar teste de estabilidade de Nyblom (1989)
    # Verifica se os parametros sao estaveis ao longo do tempo
    ny <- nyblom(fit)

    results[[m]] <- list(
      coef = coefs,
      ll = ll,
      aic = ic[1],
      bic = ic[2],
      signbias = sb,
      nyblom = ny
    )

    cat(sprintf("    %s: LogLik=%.2f, AIC=%.6f, BIC=%.6f\n", m, ll, ic[1], ic[2]))
  }
}

cat(sprintf("    Modelos estimados com sucesso: %d/%d\n\n",
            length(results), length(models)))

###############################################################################
# SECAO 2: TABELA COMPARATIVA DE MODELOS
# Resumo com log-likelihood, AIC e BIC para selecao de modelo
###############################################################################

cat(">>> Secao 2: Construindo tabela comparativa...\n")

# Montar dataframe de comparacao
estimated_models <- names(results)
comparison <- data.frame(
  model = estimated_models,
  loglik = sapply(results, function(x) x$ll),
  aic = sapply(results, function(x) x$aic),
  bic = sapply(results, function(x) x$bic),
  stringsAsFactors = FALSE
)
rownames(comparison) <- NULL

# Exibir tabela no console
cat("    Tabela Comparativa de Modelos:\n")
print(comparison)

# Salvar tabela comparativa em CSV
write_csv(comparison, file.path(output_dir, "r_full_univariate_comparison.csv"))
cat("    Salvo: r_full_univariate_comparison.csv\n\n")

###############################################################################
# SECAO 3: DIAGNOSTICOS - SIGN BIAS E NYBLOM
# Exportar resultados dos testes de diagnostico para cada modelo
###############################################################################

cat(">>> Secao 3: Exportando diagnosticos (sign bias e Nyblom)...\n")

# --- Sign Bias Test ---
# O teste verifica tres efeitos:
#   1. Sign Bias: efeito geral de choques negativos vs positivos
#   2. Negative Size Bias: magnitude dos choques negativos
#   3. Positive Size Bias: magnitude dos choques positivos
#   4. Joint Effect: teste conjunto dos tres efeitos

signbias_rows <- list()
for (m in estimated_models) {
  sb <- results[[m]]$signbias
  # signbias retorna uma matriz com t-stat e p-value
  sb_df <- data.frame(
    model = m,
    test = rownames(sb),
    t_statistic = sb[, 1],
    p_value = sb[, 2],
    stringsAsFactors = FALSE
  )
  rownames(sb_df) <- NULL
  signbias_rows[[m]] <- sb_df
}
signbias_all <- bind_rows(signbias_rows)
write_csv(signbias_all, file.path(output_dir, "r_full_signbias.csv"))
cat("    Salvo: r_full_signbias.csv\n")

# --- Nyblom Stability Test ---
# Testa a hipotese nula de estabilidade dos parametros
# Valores acima do valor critico indicam instabilidade

nyblom_rows <- list()
for (m in estimated_models) {
  ny <- results[[m]]$nyblom
  # Extrair estatisticas individuais dos parametros
  ind_stats <- ny$IndividualStat
  ny_df <- data.frame(
    model = m,
    parameter = rownames(ind_stats),
    statistic = ind_stats[, 1],
    stringsAsFactors = FALSE
  )
  rownames(ny_df) <- NULL
  # Adicionar estatistica conjunta como linha extra
  joint_row <- data.frame(
    model = m,
    parameter = "Joint",
    statistic = ny$JointStat,
    stringsAsFactors = FALSE
  )
  ny_df <- bind_rows(ny_df, joint_row)
  nyblom_rows[[m]] <- ny_df
}
nyblom_all <- bind_rows(nyblom_rows)
write_csv(nyblom_all, file.path(output_dir, "r_full_nyblom.csv"))
cat("    Salvo: r_full_nyblom.csv\n\n")

###############################################################################
# SECAO 4: COEFICIENTES DETALHADOS
# Exportar todos os parametros estimados de cada modelo
###############################################################################

cat(">>> Secao 4: Exportando coeficientes detalhados...\n")

coef_rows <- list()
for (m in estimated_models) {
  coefs <- results[[m]]$coef
  coef_df <- data.frame(
    model = m,
    parameter = names(coefs),
    value = as.numeric(coefs),
    stringsAsFactors = FALSE
  )
  coef_rows[[m]] <- coef_df
}
coef_all <- bind_rows(coef_rows)
write_csv(coef_all, file.path(output_dir, "r_full_coefficients.csv"))
cat("    Salvo: r_full_coefficients.csv\n\n")

###############################################################################
# SECAO 5: ROLLING VAR BACKTEST
# Backtest com janela movel usando o melhor modelo (por AIC)
# - Janela de previsao: 500 observacoes
# - Reestimacao a cada 50 observacoes
###############################################################################

cat(">>> Secao 5: Rolling VaR backtest...\n")

# Selecionar o melhor modelo pelo AIC (menor valor)
best_model <- comparison$model[which.min(comparison$aic)]
cat(sprintf("    Melhor modelo por AIC: %s\n", best_model))

# Especificacao do melhor modelo para backtest
spec_best <- ugarchspec(
  variance.model = list(model = best_model, garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "std"
)

# Executar rolling forecast
# n.ahead=1: previsao 1 passo a frente
# forecast.length=500: ultimas 500 observacoes como janela de teste
# refit.every=50: reestimar o modelo a cada 50 observacoes
cat("    Executando ugarchroll (pode demorar alguns minutos)...\n")
roll <- ugarchroll(
  spec_best,
  returns,
  n.ahead = 1,
  forecast.length = 500,
  refit.every = 50,
  refit.window = "moving",
  solver = "hybrid",
  calculate.VaR = TRUE,
  VaR.alpha = c(0.01, 0.05)
)

cat("    Rolling forecast concluido.\n")

# Extrair VaR das previsoes rolling
# ugarchroll com calculate.VaR=TRUE disponibiliza VaR diretamente
roll_report <- as.data.frame(roll)

# Salvar resultados do rolling forecast
write_csv(roll_report, file.path(output_dir, "r_full_rolling_forecast.csv"))
cat("    Salvo: r_full_rolling_forecast.csv\n")

###############################################################################
# SECAO 6: TESTE DE KUPIEC (VaR 95% e 99%)
# Teste incondicional de cobertura do VaR
# H0: a frequencia de violacoes e consistente com o nivel de confianca
###############################################################################

cat(">>> Secao 6: Teste de Kupiec para VaR...\n")

# Extrair retornos realizados e VaR da janela de backtest
actual_returns <- roll_report$Realized
var_95 <- roll_report$`alpha(5%)`
var_99 <- roll_report$`alpha(1%)`

# Teste de Kupiec para VaR 95% (alpha = 0.05)
kupiec_95 <- VaRTest(
  alpha = 0.05,
  actual = actual_returns,
  VaR = var_95,
  conf.level = 0.95
)

# Teste de Kupiec para VaR 99% (alpha = 0.01)
kupiec_99 <- VaRTest(
  alpha = 0.01,
  actual = actual_returns,
  VaR = var_99,
  conf.level = 0.95
)

# Montar tabela de resultados do Kupiec
kupiec_results <- data.frame(
  confidence = c("95%", "99%"),
  alpha = c(0.05, 0.01),
  expected_exceedances = c(
    kupiec_95$expected.exceed,
    kupiec_99$expected.exceed
  ),
  actual_exceedances = c(
    kupiec_95$actual.exceed,
    kupiec_99$actual.exceed
  ),
  uc_statistic = c(
    kupiec_95$uc.LRstat,
    kupiec_99$uc.LRstat
  ),
  uc_pvalue = c(
    kupiec_95$uc.LRp,
    kupiec_99$uc.LRp
  ),
  cc_statistic = c(
    kupiec_95$cc.LRstat,
    kupiec_99$cc.LRstat
  ),
  cc_pvalue = c(
    kupiec_95$cc.LRp,
    kupiec_99$cc.LRp
  ),
  stringsAsFactors = FALSE
)

cat("    Resultados do teste de Kupiec:\n")
print(kupiec_results)

write_csv(kupiec_results, file.path(output_dir, "r_full_kupiec.csv"))
cat("    Salvo: r_full_kupiec.csv\n\n")

###############################################################################
# SECAO 7: DCC MULTIVARIADO
# Estimacao do modelo DCC(1,1) em 4 series de retornos FX
# Pacote rmgarch com distribuicao t multivariada
###############################################################################

cat(">>> Secao 7: Estimando DCC multivariado em series FX...\n")

# Leitura dos retornos FX (4 pares: EURUSD, GBPUSD, JPYUSD, CHFUSD)
fx_df <- read_csv("../data/fx_majors.csv", show_col_types = FALSE)
fx_returns <- as.matrix(fx_df[, -1])  # Remover coluna de data

cat(sprintf("    Series FX: %d observacoes x %d ativos\n",
            nrow(fx_returns), ncol(fx_returns)))
cat(sprintf("    Ativos: %s\n", paste(colnames(fx_returns), collapse = ", ")))

# Especificacao univariada para cada serie
# Cada serie e modelada como GARCH(1,1) com distribuicao t de Student
uspec <- multispec(replicate(
  ncol(fx_returns),
  ugarchspec(
    variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
    mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
    distribution.model = "std"
  )
))

# Especificacao DCC(1,1) com distribuicao t multivariada
dcc_spec <- dccspec(
  uspec,
  dccOrder = c(1, 1),
  distribution = "mvt"
)

# Estimacao do modelo DCC
cat("    Estimando DCC(1,1)...\n")
dcc_fit <- dccfit(dcc_spec, fx_returns)
cat("    DCC estimado com sucesso.\n")

# Extrair e salvar parametros DCC (a e b da equacao de correlacao)
dcc_params <- coef(dcc_fit, type = "dcc")
dcc_params_df <- data.frame(
  param = names(dcc_params),
  value = as.numeric(dcc_params),
  stringsAsFactors = FALSE
)
write_csv(dcc_params_df, file.path(output_dir, "r_full_dcc_params.csv"))
cat("    Salvo: r_full_dcc_params.csv\n")

# Extrair e salvar todos os coeficientes (univariados + DCC)
all_dcc_coefs <- coef(dcc_fit)
# all_dcc_coefs retorna um vetor nomeado com todos os parametros
all_dcc_df <- data.frame(
  param = names(all_dcc_coefs),
  value = as.numeric(all_dcc_coefs),
  stringsAsFactors = FALSE
)
write_csv(all_dcc_df, file.path(output_dir, "r_full_dcc_all_coefs.csv"))
cat("    Salvo: r_full_dcc_all_coefs.csv\n")

# Extrair correlacoes condicionais medias
# rcor retorna um array 3D (N x N x T)
R_array <- rcor(dcc_fit)
n_assets <- dim(R_array)[1]
n_time <- dim(R_array)[3]

# Calcular correlacao media ao longo do tempo para cada par
pairs <- list()
for (i in 1:(n_assets - 1)) {
  for (j in (i + 1):n_assets) {
    pair_name <- paste0(colnames(fx_returns)[i], "_", colnames(fx_returns)[j])
    pairs[[pair_name]] <- R_array[i, j, ]
  }
}
corr_df <- as.data.frame(pairs)
corr_df$t <- 1:n_time
write_csv(corr_df, file.path(output_dir, "r_full_dcc_correlations.csv"))
cat("    Salvo: r_full_dcc_correlations.csv\n\n")

###############################################################################
# SECAO 8: VAR DO PORTFOLIO COM PESOS IGUAIS
# Calculo do VaR do portfolio usando as matrizes de covariancia do DCC
###############################################################################

cat(">>> Secao 8: Calculando VaR do portfolio...\n")

# Pesos iguais para os 4 ativos
w <- rep(1 / ncol(fx_returns), ncol(fx_returns))
cat(sprintf("    Pesos do portfolio: %s\n",
            paste(sprintf("%.4f", w), collapse = ", ")))

# Extrair matrizes de covariancia condicional (array 3D: N x N x T)
H <- rcov(dcc_fit)

# Calcular variancia e VaR do portfolio para cada periodo
n_periods <- dim(H)[3]
port_vol <- numeric(n_periods)
port_var_95 <- numeric(n_periods)
port_var_99 <- numeric(n_periods)

for (t in 1:n_periods) {
  # Variancia do portfolio: w' * H_t * w
  port_variance <- as.numeric(t(w) %*% H[, , t] %*% w)
  port_vol[t] <- sqrt(port_variance)

  # VaR parametrico (distribuicao normal)
  # VaR_95 = sigma_p * z_0.05 (negativo, pois z_0.05 < 0)
  port_var_95[t] <- port_vol[t] * qnorm(0.05)
  port_var_99[t] <- port_vol[t] * qnorm(0.01)
}

# Montar dataframe com resultados do portfolio
portfolio_df <- data.frame(
  t = 1:n_periods,
  portfolio_vol = port_vol,
  var_95 = port_var_95,
  var_99 = port_var_99
)

# Estatisticas resumo
cat(sprintf("    Volatilidade media do portfolio: %.6f\n", mean(port_vol)))
cat(sprintf("    VaR 95%% medio: %.6f\n", mean(port_var_95)))
cat(sprintf("    VaR 99%% medio: %.6f\n", mean(port_var_99)))

write_csv(portfolio_df, file.path(output_dir, "r_full_portfolio_var.csv"))
cat("    Salvo: r_full_portfolio_var.csv\n\n")

###############################################################################
# SECAO 9: VOLATILIDADE CONDICIONAL DOS MODELOS UNIVARIADOS
# Exportar series de volatilidade para comparacao com archbox
###############################################################################

cat(">>> Secao 9: Exportando volatilidades condicionais...\n")

# Extrair e salvar a volatilidade condicional de cada modelo univariado
for (m in estimated_models) {
  fit <- fit_objects[[m]]
  if (!is.null(fit)) {
    sigma_t <- as.numeric(sigma(fit))
    vol_df <- data.frame(
      t = 1:length(sigma_t),
      sigma = sigma_t
    )
    filename <- sprintf("r_full_vol_%s.csv", tolower(m))
    write_csv(vol_df, file.path(output_dir, filename))
    cat(sprintf("    Salvo: %s\n", filename))
  }
}

cat("\n")

###############################################################################
# RESUMO FINAL
###############################################################################

cat("=============================================================\n")
cat("  Validacao completa finalizada!\n")
cat("=============================================================\n")
cat("\n  Arquivos gerados em ../outputs/:\n")
cat("    - r_full_univariate_comparison.csv  (comparacao 6 modelos)\n")
cat("    - r_full_signbias.csv               (teste sign bias)\n")
cat("    - r_full_nyblom.csv                 (teste Nyblom)\n")
cat("    - r_full_coefficients.csv           (coeficientes detalhados)\n")
cat("    - r_full_rolling_forecast.csv       (rolling VaR backtest)\n")
cat("    - r_full_kupiec.csv                 (teste de Kupiec)\n")
cat("    - r_full_dcc_params.csv             (parametros DCC)\n")
cat("    - r_full_dcc_all_coefs.csv          (todos coeficientes DCC)\n")
cat("    - r_full_dcc_correlations.csv       (correlacoes condicionais)\n")
cat("    - r_full_portfolio_var.csv           (VaR do portfolio)\n")
cat("    - r_full_vol_*.csv                  (volatilidades condicionais)\n")
cat("\n  Estes CSVs podem ser comparados ponto-a-ponto com os outputs\n")
cat("  gerados pela archbox no notebook Python.\n")
cat("=============================================================\n")
