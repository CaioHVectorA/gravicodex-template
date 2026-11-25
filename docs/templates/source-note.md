# Modelo de ficha de leitura (`docs/references/notes/<chave>.md`)

Crie esta ficha sob demanda apenas para obras centrais do trabalho (fundamentação principal, baseline experimental ou norma decisiva). Metadados completos pertencem exclusivamente a `docs/references/references.bib`.

```markdown
# @chave — Título curto da obra

- **Chave BibTeX:** `@chave`
- **Tipo de fonte:** Primária revisada por pares / Normativa/técnica oficial / Secundária/síntese / Cinza/preliminar
- **Status de leitura:** metadados / parcial / conferida / descartada
- **Acesso verificado em:** AAAA-MM-DD (arquivo local, DOI ou URL oficial)
- **Seções do projeto onde entra:** Introdução, Trabalhos Relacionados, Metodologia

## Problema e contribuição central

Em 2–4 frases, qual pergunta o trabalho responde e qual evidência principal apresenta.

## Metodologia, cenário e métricas verificadas

- **Cenário / dataset / hardware:** preencher somente com dados lidos na obra.
- **Métricas reportadas:** valor exato + unidade + página/tabela (ex.: latência p95 = 18 ms, Tabela 3, p. 7).
- **Limitações declaradas pelos autores:** o que o estudo não cobre ou assume.

## Citações diretas verificadas

- `"Trecho literal exato"` (`@chave`, p. XX).

## Relação com este projeto

- **O que adotamos ou comparamos:** conexão concreta com nossa hipótese ou implementação.
- **O que difere:** escopo, restrições ou variáveis distintas do nosso experimento.
- **Pendências:** listar itens `[A CONFERIR: @chave]` se a leitura ainda for parcial.
```
