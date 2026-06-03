# Fase 05 — Cap 02 Scripts R/Stata + Cap 03 Notebooks Assimetricos

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os scripts R e Stata do capitulo 02 e os 5 notebooks do capitulo 03 (GARCH Assimetricos).

---

## Descricao Tecnica

### Cap 02 — Scripts R e Stata

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/02_garch_classico/`

#### 01_garch_basico.R
- rugarch: `ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1,1)))` com sp500, bitcoin, usdbrl
- `ugarchfit(spec, data)` para cada serie
- Comparar `coef(fit)`, `persistence(fit)`, `infocriteria(fit)`

#### 02_ordens_pq.R
- Ajustar GARCH(1,1), (1,2), (2,1), (2,2) com rugarch
- `infocriteria(fit)` para cada ordem
- Tabela comparativa

#### 01_garch_basico.do
- Stata: `arch returns, arch(1) garch(1)` para sp500
- `estat ic` para criterios de informacao

#### 02_ordens_pq.do
- Stata: ajustar varias ordens e comparar com `estat ic`

### Cap 03 — Notebooks Assimetricos

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/03_garch_assimetricos/`

#### 01_egarch.ipynb
- EGARCH(1,1) no sp500: `from archbox.models import EGARCH`
- Interpretar parametro gamma (assimetria): choques negativos vs positivos
- Comparar com GARCH(1,1) simetrico: AIC, loglike
- Plot de volatilidade condicional: EGARCH vs GARCH
- Vantagem: log(sigma2) garante positividade

#### 02_gjr_garch.ipynb
- GJR-GARCH(1,1) no sp500: `from archbox.models import GJRGARCH`
- Indicadora I(epsilon < 0): efeito de choques negativos
- Interpretar gamma: quanto mais a volatilidade sobe com choques negativos
- Comparar: resposta a choque de +1% vs -1%

#### 03_aparch.ipynb
- APARCH(1,1) no sp500: `from archbox.models import APARCH`
- Parametro de potencia delta: generaliza GARCH (delta=2), AVGARCH (delta=1)
- Assimetria gamma: similar ao GJR mas com potencia flexivel
- Interpretar delta estimado

#### 04_comparacao_assimetricos.ipynb
- Ajustar GARCH, EGARCH, GJR, APARCH no sp500
- Tabela comparativa: loglike, AIC, BIC, parametros de assimetria
- News impact curves lado a lado: `from archbox.utils import news_impact_curve, compare_news_impact`
- Plot: `plot_news_impact_comparison()` — 4 modelos no mesmo grafico
- Conclusao: qual modelo captura melhor o efeito alavancagem?

#### 05_news_impact.ipynb
- Foco na news impact curve (NIC)
- Teoria: sigma2(t) como funcao de epsilon(t-1)
- Calcular NIC para cada modelo: `news_impact_curve(model, result)`
- Plot individual e comparativo
- Interpretacao visual: curva simetrica (GARCH) vs assimetrica (EGARCH, GJR, APARCH)
- Funcionalidades: `news_impact_curve()`, `compare_news_impact()`, `plot_news_impact()`, `plot_news_impact_comparison()`

---

## Instrucoes

1. Scripts R e Stata no diretorio do cap 02
2. Notebooks no diretorio do cap 03
3. Texto em portugues, codigo em ingles
4. Imports corretos para cada modelo assimetrico

---

## Criterios de Aceite

- [ ] Arquivo `02_garch_classico/01_garch_basico.R` criado
- [ ] Arquivo `02_garch_classico/02_ordens_pq.R` criado
- [ ] Arquivo `02_garch_classico/01_garch_basico.do` criado
- [ ] Arquivo `02_garch_classico/02_ordens_pq.do` criado
- [ ] Arquivo `03_garch_assimetricos/01_egarch.ipynb` criado
- [ ] Arquivo `03_garch_assimetricos/02_gjr_garch.ipynb` criado
- [ ] Arquivo `03_garch_assimetricos/03_aparch.ipynb` criado
- [ ] Arquivo `03_garch_assimetricos/04_comparacao_assimetricos.ipynb` criado
- [ ] Arquivo `03_garch_assimetricos/05_news_impact.ipynb` criado

---

**End of Specification**
