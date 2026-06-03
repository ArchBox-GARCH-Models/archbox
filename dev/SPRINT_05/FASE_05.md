# Fase 05 — Cap 12: Notebooks Restantes Threshold/STAR

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 4 notebooks restantes do capitulo 12.

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/12_threshold_star/`

### 05_lstar.ipynb
- `from archbox.threshold import LSTAR`
- Transicao logistica suave: G(s) = 1/(1 + exp(-gamma*(s-c)))
- `model = LSTAR(data, order=1, delay=1, refine=True)`
- Interpretar gamma: velocidade de transicao (alto = quase TAR, baixo = suave)
- Plot: funcao de transicao + dados

### 06_estar.ipynb
- `from archbox.threshold import ESTAR`
- Transicao exponencial: G(s) = 1 - exp(-gamma*(s-c)^2)
- Simetrica em torno do threshold c
- Diferenca fundamental com LSTAR: regime intermediario vs extremos
- Plot: funcao de transicao exponencial

### 07_funcoes_transicao.ipynb
- `from archbox.threshold.transition import logistic_transition, exponential_transition`
- Visualizar funcoes para diferentes valores de gamma e c
- `plot_transition_function()` — comparar logistica vs exponencial
- `plot_phase_diagram()` — diagrama de fase para SETAR
- Funcao didatica: entender intuitivamente cada tipo de transicao

### 08_comparacao.ipynb
- Ajustar TAR, SETAR, LSTAR, ESTAR nos mesmos dados
- Tabela: AIC, BIC, RSS, parametros
- Thresholds estimados: comparar c entre modelos
- Plot: previsoes de cada modelo sobrepostas
- Conclusao: como selecionar o modelo nao-linear adequado

---

## Criterios de Aceite

- [ ] Arquivo `05_lstar.ipynb` criado com LSTAR e interpretacao de gamma
- [ ] Arquivo `06_estar.ipynb` criado com ESTAR e transicao simetrica
- [ ] Arquivo `07_funcoes_transicao.ipynb` criado com visualizacao interativa
- [ ] Arquivo `08_comparacao.ipynb` criado com 4 modelos comparados

---

**End of Specification**
