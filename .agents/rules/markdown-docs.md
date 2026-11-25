---
trigger: glob
globs: "*.md, docs/**/*.md"
description: "Convenções verificáveis de Markdown, fonte única e diagramas Mermaid ao editar documentação."
---

# Regras de Markdown e documentação

Aplicável ao criar ou editar arquivos `.md` na raiz ou em `docs/`. Referência completa: [guia de Markdown](../../docs/guides/markdown.md).

## Integridade verificável

- Use um propósito por arquivo, título H1 único e subtítulos sem formatação inline ou duplicações (âncoras duplicadas falham na checagem).
- Escreva links internos como inline literais relativos (`[rótulo](caminho.md#secao)`). Use `<caminho com espacos.md>` se houver espaço; nunca linke caminhos fictícios de modelos (use crases).
- Feche toda cerca de código (` ``` ` ou ` ~~~ `) com o mesmo marcador e comprimento igual ou superior.
- Respeite os orçamentos em bytes UTF-8: `AGENTS.md` ≤ 3 KiB, `docs/INDEX.md` ≤ 4 KiB, `docs/starters/*.md` ≤ 16 KiB (temporários), demais permanentes ≤ 8 KiB.

## Fonte única e Mermaid

- Comandos ficam em [comandos](../../docs/context/commands.md), estado em [projeto](../../docs/context/project.md), fronteiras no [mapa](../../docs/context/map.md), motivos em `docs/decisions/` e retomada em `docs/tasks/`. Linke em vez de copiar.
- Use `mermaid` apenas para relações ou fluxos que precisem de visão estrutural; acompanhe com prosa curta que explique as setas e confira cada nó contra caminhos reais.
- Frontmatter YAML só deve existir onde uma ferramenta o consome (`.agents/rules/`, `.agents/skills/`, `.agents/agents/`).
