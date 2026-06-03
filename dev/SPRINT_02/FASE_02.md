# Fase 02 — Cap 04: Notebooks GARCH Avancados

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 5 notebooks do capitulo 04 cobrindo modelos GARCH especializados.

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/04_garch_avancados/`

### 01_igarch.ipynb
- IGARCH no bitcoin: `from archbox.models import IGARCH`
- Persistencia unitaria (alpha + beta = 1), variancia incondicional infinita
- Comparar com EWMA (lambda=0.94): `from archbox.risk import EWMA`
- Plot: IGARCH vs EWMA — volatilidade condicional

### 02_figarch.ipynb
- FIGARCH no sp500: `from archbox.models import FIGARCH`
- Memoria longa em volatilidade: parametro d (fracionario)
- Efeito de `truncation_lag` (default 1000)
- Interpretar: decaimento hiperbolico vs exponencial

### 03_garch_m.ipynb
- GARCH-M com sp500: `from archbox.models import GARCHM`
- 3 opcoes de risk_premium: 'variance', 'volatility', 'log_variance'
- Lambda (premio de risco): positivo? significativo?
- Implicacao: retornos maiores quando volatilidade e alta

### 04_component_garch.ipynb
- ComponentGARCH no sp500: `from archbox.models import ComponentGARCH`
- `result.variance_decomposition()` — separar q_t (permanente) e h_t (transitorio)
- Plot: componente permanente vs transitorio ao longo do tempo
- Interpretar: choques de curto vs longo prazo

### 05_har_rv.ipynb
- HAR-RV com realized_vol dataset: `from archbox.models import HARRV`
- Dados: `load_dataset('realized_vol')` — daily, weekly, monthly RV
- Ajustar: `model = HARRV(rv_data)` e `result = model.fit()`
- `result.summary()` — coeficientes beta_d, beta_w, beta_m
- `result.forecast()` — previsao multi-passos
- Interpretar: heterogeneidade de horizontes (Corsi, 2009)

---

## Criterios de Aceite

- [ ] Arquivo `01_igarch.ipynb` criado com comparacao IGARCH vs EWMA
- [ ] Arquivo `02_figarch.ipynb` criado com parametro d e memoria longa
- [ ] Arquivo `03_garch_m.ipynb` criado com 3 opcoes de risk_premium
- [ ] Arquivo `04_component_garch.ipynb` criado com variance_decomposition
- [ ] Arquivo `05_har_rv.ipynb` criado com realized_vol dataset
- [ ] Todos os notebooks com texto em portugues

---

**End of Specification**
