# Fase 04 — Cap 15: Notebooks Visualizacao Restantes

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 5 notebooks restantes do capitulo 15 (Visualizacao).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/15_visualizacao/`

### 06_distribuicao.ipynb
- `from archbox.visualization import plot_distribution_fit`
- Histograma dos residuos padronizados + densidade da distribuicao ajustada
- Normal vs Student-t vs Skewed-t sobrepostas

### 07_risco_plot.ipynb
- `from archbox.visualization import plot_var_backtest, plot_traffic_light, plot_var_comparison`
- `plot_var_backtest()` — retornos com VaR e violacoes destacadas
- `plot_traffic_light()` — resultado Basel III visual
- `plot_var_comparison()` — multiplos metodos de VaR no mesmo grafico

### 08_transicao_plot.ipynb
- `from archbox.visualization import plot_transition_function, plot_phase_diagram`
- Funcao de transicao logistica e exponencial
- Diagrama de fase para SETAR: y_t vs y_{t-d}

### 09_temas.ipynb
- `from archbox.visualization import get_theme`
- Demonstrar todos os temas: 'professional', 'seaborn', 'minimal'
- Mesmo grafico renderizado com cada tema
- Como customizar: `matplotlib.rcParams.update(get_theme('professional'))`

### 10_exportacao.ipynb
- `from archbox.visualization import export_png, export_pdf, export_svg`
- Gerar figura e exportar em 3 formatos
- DPI para publicacao (300 dpi)
- Tamanhos para paper vs slides vs poster

---

## Criterios de Aceite

- [ ] Arquivo `06_distribuicao.ipynb` criado com plot_distribution_fit
- [ ] Arquivo `07_risco_plot.ipynb` criado com 3 tipos de plot de risco
- [ ] Arquivo `08_transicao_plot.ipynb` criado com transition e phase plots
- [ ] Arquivo `09_temas.ipynb` criado com todos os temas demonstrados
- [ ] Arquivo `10_exportacao.ipynb` criado com export em PNG, PDF, SVG

---

**End of Specification**
