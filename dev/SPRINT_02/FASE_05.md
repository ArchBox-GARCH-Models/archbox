# Fase 05 — Cap 06: Notebooks Diagnosticos

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 8 notebooks do capitulo 06 cobrindo todos os testes diagnosticos da biblioteca.

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/06_diagnosticos/`

### 01_arch_lm.ipynb
- `from archbox.diagnostics import arch_lm_test`
- Testar ANTES do ajuste (residuos do modelo de media): detectar ARCH effects
- Testar DEPOIS do ajuste (residuos padronizados): verificar se GARCH capturou
- Interpretar: p-valor < 0.05 = rejeita H0 de "sem efeitos ARCH"

### 02_ljung_box.ipynb
- `from archbox.diagnostics import ljung_box_squared`
- Aplicar nos residuos padronizados ao quadrado (z^2_t)
- Testar com lags=5, 10, 20
- Interpretar: autocorrelacao residual = modelo inadequado

### 03_sign_bias.ipynb
- `from archbox.diagnostics import sign_bias_test`
- Sign bias, negative sign bias, positive sign bias, joint test
- Interpretar: rejeicao sugere modelo assimetrico (EGARCH, GJR)
- Fluxo: GARCH falha → sign bias → tentar GJR

### 04_nyblom.ipynb
- `from archbox.diagnostics import nyblom_test`
- Estabilidade dos parametros: H0 = parametros constantes
- Estatistica conjunta e individual
- Interpretar: instabilidade sugere regime-switching

### 05_diagnostico_completo.ipynb
- `from archbox.diagnostics import full_diagnostics`
- `report = full_diagnostics(result, lags=[5, 10])`
- `report.summary(significance=0.05)` — tabela PASS/FAIL
- `plot_diagnostics(result)` — ACF, PACF, QQ-plot
- Fluxo de decisao: qual teste falha → qual modelo tentar

### 06_engle_sheppard.ipynb
- `from archbox.diagnostics import engle_sheppard_test`
- Aplicar nos residuos de modelos multivariados
- Testar estrutura de correlacao

### 07_hong_spillover.ipynb
- `from archbox.diagnostics import hong_spillover_test`
- Testar spillovers de volatilidade entre pares de series
- Aplicar com fx_majors (USD/EUR vs USD/GBP)

### 08_workflow_diagnostico.ipynb
- Workflow completo iterativo:
  1. Ajustar GARCH(1,1) no sp500
  2. Rodar full_diagnostics → sign bias falha
  3. Ajustar GJR-GARCH(1,1)
  4. Rodar full_diagnostics → todos passam
  5. Comparar AIC final
- Demonstrar o ciclo: modelo → diagnostico → reajuste

---

## Criterios de Aceite

- [ ] Arquivo `01_arch_lm.ipynb` criado com teste antes/depois do ajuste
- [ ] Arquivo `02_ljung_box.ipynb` criado com multiplos lags
- [ ] Arquivo `03_sign_bias.ipynb` criado com 4 componentes do teste
- [ ] Arquivo `04_nyblom.ipynb` criado com estatisticas conjunta e individual
- [ ] Arquivo `05_diagnostico_completo.ipynb` criado com full_diagnostics e plot
- [ ] Arquivo `06_engle_sheppard.ipynb` criado para residuos multivariados
- [ ] Arquivo `07_hong_spillover.ipynb` criado com teste de spillover
- [ ] Arquivo `08_workflow_diagnostico.ipynb` criado com ciclo iterativo completo

---

**End of Specification**
