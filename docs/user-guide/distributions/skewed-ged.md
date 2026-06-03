---
title: "Skewed GED"
description: "Distribuicao Skewed Generalized Error Distribution para modelos GARCH -- combina flexibilidade de forma com assimetria."
---

# Skewed GED

!!! info "Quick Reference"
    **Parametros extras:** $\nu$ (parametro de forma, $\nu > 0$), $\lambda$ (assimetria, $\lambda \in (-1, 1)$)
    **R equivalent:** `rugarch::ugarchspec(distribution.model = "sged")`
    **Status no ArchBox:** Ainda nao implementada -- documentada como referencia teorica

!!! warning "Disponibilidade"
    A Skewed GED **nao esta implementada** na versao atual do ArchBox. Esta pagina documenta a teoria e a formulacao para referencia. Para modelar caudas pesadas com assimetria, use a [Skewed Student-t](skewed-t.md), que e a alternativa disponivel.

## Overview

A **Skewed Generalized Error Distribution** (Skewed GED ou SGED) estende a [GED](ged.md) com um parametro de assimetria $\lambda$, combinando **flexibilidade no formato das caudas** (via $\nu$) com **assimetria** (via $\lambda$). Foi proposta por Theodossiou (1998) e oferece a distribuicao condicional mais flexivel da familia exponencial simetrica.

A ideia central e permitir que as duas metades da distribuicao tenham escalas diferentes, controladas por $\lambda$, enquanto o formato geral das caudas e controlado por $\nu$.

**Quando usar:**

- Quando se deseja maxima flexibilidade distribucional
- Quando a Skewed-t e a GED sao rejeitadas pelos diagnosticos
- Para comparacao em exercicios de selecao de distribuicao

**Limitacoes:**

- Dois parametros extras ($\nu, \lambda$) -- mais dificil de estimar
- Requer amostras grandes ($T > 1000$) para estimacao confiavel
- Pode ser sobre-parametrizada para muitas aplicacoes praticas

## Formulacao Matematica

### PDF (Theodossiou, 1998)

A densidade da SGED padronizada:

$$f(z; \nu, \lambda) = \frac{\nu}{\lambda_s \cdot 2^{1+1/\nu} \cdot \Gamma(1/\nu)} \cdot \begin{cases} \exp\left(-\frac{1}{2}\left|\frac{z + \delta}{\lambda_s(1-\lambda)}\right|^\nu\right) & \text{se } z < -\delta \\[8pt] \exp\left(-\frac{1}{2}\left|\frac{z + \delta}{\lambda_s(1+\lambda)}\right|^\nu\right) & \text{se } z \geq -\delta \end{cases}$$

onde as constantes de padronizacao sao:

$$\lambda_s = \sqrt{2^{-2/\nu} \cdot \frac{\Gamma(1/\nu)}{\Gamma(3/\nu)}}$$

$$\delta = \frac{2\lambda \cdot \lambda_s \cdot \Gamma(2/\nu)}{\Gamma(1/\nu)}$$

### Relacao entre Parametros e Momentos

| Propriedade | Dependencia |
|:------------|:------------|
| Media | $E[z] = 0$ (garantido pela padronizacao) |
| Variancia | $\text{Var}(z) = 1$ (garantido por $\lambda_s$ e $\delta$) |
| Assimetria | Controlada por $\lambda$ |
| Curtose | Controlada por $\nu$ (e ligeiramente por $\lambda$) |

### Casos Especiais

| Condicao | Distribuicao resultante |
|:---------|:-----------------------|
| $\lambda = 0$ | [GED](ged.md) |
| $\nu = 2$ | Skewed Normal |
| $\lambda = 0$, $\nu = 2$ | [Normal](normal.md) |
| $\lambda = 0$, $\nu = 1$ | Laplace |

## Parametros

| Parametro | Descricao | Restricao |
|:----------|:----------|:----------|
| $\nu$ | Parametro de forma | $\nu > 0$ |
| $\lambda$ | Assimetria | $\lambda \in (-1, 1)$ |

## Exemplo Conceitual

Embora a SGED nao esteja implementada no ArchBox, o workflow de uso seria analogo as outras distribuicoes:

```python
# Exemplo conceitual -- nao disponivel na versao atual
# from archbox.distributions import SkewedGED
# from archbox import GARCH
# from archbox.datasets import load_dataset
#
# sp500 = load_dataset('sp500')
#
# # GARCH(1,1) com Skewed GED
# model = GARCH(sp500['returns'], p=1, q=1, dist=SkewedGED())
# results = model.fit()
# print(results.summary())
```

### Alternativa Disponivel: Skewed Student-t

Para modelar caudas pesadas com assimetria, use a Skewed Student-t:

```python
from archbox import GARCH
from archbox.distributions import SkewedT
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# Skewed Student-t captura caudas pesadas + assimetria
model = GARCH(sp500['returns'], p=1, q=1, dist=SkewedT())
results = model.fit()
print(results.summary())
```

### Comparacao Teorica: SGED vs. Skewed-t

| Aspecto | Skewed-t (Hansen) | Skewed GED |
|:--------|:-------------------|:-----------|
| Caudas | Potencia ($\|z\|^{-(\nu+1)}$) | Exponencial estendida ($e^{-\|z\|^\nu}$) |
| Assimetria | Via $\lambda$ | Via $\lambda$ |
| Parametros extras | 2 ($\nu, \lambda$) | 2 ($\nu, \lambda$) |
| Casos especiais | Student-t, Normal | GED, Laplace, Normal |
| Peso das caudas extremas | Mais pesadas | Menos pesadas |
| Preferencia empirica | Mais comum em financas | Menos comum |

!!! tip "Na pratica"
    A Skewed Student-t e geralmente preferida em financas porque as caudas de potencia (power-law tails) aproximam melhor a distribuicao empirica de retornos extremos. A SGED pode ser preferida em contextos onde as caudas sao pesadas mas nao tao extremas quanto as da Student-t.

## Implementacao em Outras Ferramentas

=== "R (rugarch)"

    ```r
    # A SGED esta disponivel no rugarch
    spec <- ugarchspec(
      variance.model = list(model = "sGARCH"),
      distribution.model = "sged"
    )
    fit <- ugarchfit(spec, data = returns)
    ```

=== "Python (arch)"

    ```python
    # O pacote arch nao implementa SGED diretamente
    # Use SkewStudent como alternativa
    from arch import arch_model

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='SkewStudent')
    res = am.fit()
    ```

## References

- Theodossiou, P. (1998). Financial Data and the Skewed Generalized T Distribution. *Management Science*, 44(12), 1650--1661.
- Nelson, D. B. (1991). Conditional Heteroskedasticity in Asset Returns: A New Approach. *Econometrica*, 59(2), 347--370.
- Bali, T. G., & Theodossiou, P. (2007). A Conditional-SGT-VaR Approach with Alternative GARCH Models. *Annals of Operations Research*, 151(1), 241--267.

## See Also

- [GED](ged.md) -- Caso especial simetrico ($\lambda = 0$)
- [Skewed Student-t](skewed-t.md) -- Alternativa disponivel para caudas pesadas + assimetria
- [Normal](normal.md) -- Caso especial com $\nu = 2$, $\lambda = 0$
- [Guia de Selecao](choosing.md) -- Workflow de comparacao de distribuicoes
