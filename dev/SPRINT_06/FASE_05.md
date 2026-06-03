# Fase 05 — Cap 16: Notebooks Relatorios Automatizados

**Status**: PENDENTE
**Dependencias**: FASE_01
**Bloqueia**: Nenhuma

---

## Objetivo

Criar os 5 notebooks do capitulo 16 (Relatorios Automatizados).

---

## Descricao Tecnica

**Diretorio**: `/home/guhaase/projetos/archbox/examples/capitulos/16_relatorios/`

### 01_relatorio_html.ipynb
- `from archbox.report import ReportManager`
- `rm = ReportManager()`
- `html = rm.generate(result, report_type='garch', fmt='html', theme='professional')`
- Salvar em arquivo e visualizar inline com `IPython.display.HTML`

### 02_relatorio_latex.ipynb
- `latex = rm.generate(result, report_type='garch', fmt='latex')`
- Saida LaTeX para papers academicos
- Mostrar o codigo LaTeX gerado
- Discutir: como incluir em documento .tex

### 03_relatorio_markdown.ipynb
- `md = rm.generate(result, report_type='garch', fmt='markdown')`
- Integracao com documentacao (mkdocs, etc.)
- Mostrar output Markdown renderizado

### 04_tipos_relatorio.ipynb
- Todos os 4 tipos de relatorio:
  - `report_type='garch'` — modelo univariado
  - `report_type='multivariate'` — modelo multivariado
  - `report_type='regime'` — regime-switching
  - `report_type='risk'` — analise de risco
- Cada um com seus dados e resultado correspondente

### 05_customizacao.ipynb
- Opcoes de customizacao:
  - `theme='professional'` vs outros temas
  - `title='Relatorio Customizado'`
  - `output_path='relatorio.html'` — salvar direto em arquivo
- CSS manager para temas HTML
- Template manager para templates customizados

---

## Criterios de Aceite

- [ ] Arquivo `01_relatorio_html.ipynb` criado com relatorio HTML interativo
- [ ] Arquivo `02_relatorio_latex.ipynb` criado com saida LaTeX
- [ ] Arquivo `03_relatorio_markdown.ipynb` criado com saida Markdown
- [ ] Arquivo `04_tipos_relatorio.ipynb` criado com os 4 tipos
- [ ] Arquivo `05_customizacao.ipynb` criado com opcoes de customizacao

---

**End of Specification**
