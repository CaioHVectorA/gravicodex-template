---
trigger: glob
globs: "docs/references/**, **/*.bib"
description: "Regras anti-alucinação bibliográfica para projetos acadêmicos e arquivos BibTeX."
---

# Regras de referências acadêmicas

Aplicável ao editar bibliografia, fichas de leitura ou citações em `docs/references/` e arquivos `.bib`. Guia completo: [guia de referências](../../docs/guides/references.md).

## Proibições absolutas (anti-alucinação)

- **Nunca invente de memória** DOI, ISBN, ISSN, número de página, volume, ano, nome de autor, URL ou métrica experimental.
- Quando um metadado ou trecho não estiver verificado no texto-fonte disponível, marque explicitamente `[A CONFERIR: @chave]` em vez de preencher por suposição.
- Toda citação direta exige página ou seção exata confirmada no documento original.

## Camadas e rastreabilidade

- `docs/references/references.bib` é a fonte única de metadados BibTeX.
- `docs/references/README.md` mantém a matriz `Seção/Tema → @chave → Tipo → Status → Ficha`.
- `docs/references/notes/<chave>.md` é criado sob demanda apenas para obras centrais.
- Separe explicitamente no texto: (1) literatura citada, (2) dado empírico reproduzido no projeto e (3) hipótese ou proposta autoral.
- Em projetos não acadêmicos, remova esta regra durante a faxina pós-reconhecimento do bootstrap.
