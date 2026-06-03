# archbox — Plano de Execucao dos Exemplos Demonstrativos

**Status**: PENDENTE
**Data**: 2026-03-24
**Objetivo**: Criar 127 arquivos de demonstracao (notebooks, scripts R, scripts Stata) cobrindo toda a API do archbox.
**Target**: `/home/guhaase/projetos/archbox/examples/capitulos/`
**Spec completa**: `/home/guhaase/projetos/archbox/dev/demo-plan.md`

---

## Organizacao em Sprints

| Sprint | Tema | Capitulos | Fases | Arquivos |
|--------|------|-----------|-------|----------|
| 01 | Fundamentos (Intro + GARCH + Assimetricos) | 01, 02, 03 | 6 | 30 |
| 02 | Avancados + Distribuicoes + Diagnosticos | 04, 05, 06 | 6 | 24 |
| 03 | Previsao + Risco | 07, 08 | 5 | 16 |
| 04 | Multivariados + Portfolio | 09, 10, 13 | 6 | 18 |
| 05 | Regime-Switching + Threshold/STAR | 11, 12 | 6 | 23 |
| 06 | Experimentos + Visualizacao + Relatorios + Validacao | 14, 15, 16, 17 | 6 | 29 |
| **Total** | | **17 capitulos** | **35 fases** | **127+13 arquivos** |

---

## Ordem de Execucao

Para cada sprint:

1. Ler `00_OVERVIEW.md` (este documento)
2. Entrar no diretorio do sprint: `cd SPRINT_NN/`
3. Executar `chmod +x prompt.sh && ./prompt.sh`
4. Acompanhar: `tail -f LOG/latest.log`

Sprints sao independentes entre si — podem ser executados em qualquer ordem.
Dentro de cada sprint, as fases sao sequenciais.

---

## Pre-requisitos

- Python 3.11+ com archbox instalado (`pip install -e ".[dev]"`)
- Claude CLI instalado (`npm install -g @anthropic-ai/claude-code`)
- Jupyter instalado para validar notebooks (`pip install jupyter`)

---

## Criterio de Sucesso

Todos os 127 arquivos criados em `examples/capitulos/` com:
- Notebooks (.ipynb) executaveis sem erros
- Scripts R (.R) com sintaxe valida
- Scripts Stata (.do) com sintaxe valida
- Cada arquivo com explicacoes em portugues

---

**End of Document**
