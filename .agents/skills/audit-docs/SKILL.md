---
name: audit-docs
description: "Executa auditoria de Markdown, orçamentos em bytes e customizações Antigravity tratando scripts/check_docs.py como caixa-preta."
---

# Skill: Auditoria de documentação e customizações

Use esta skill para validar links locais, âncoras, cercas de código, limites em bytes e a integridade das customizações nativas do Antigravity (`.agents/rules/`, `.agents/skills/`, `.agents/agents/`, `.agents/hooks.json`).

## Protocolo (script como caixa-preta)

1. Descubra a interface sem ler o código-fonte inteiro do script:

```sh
python3 scripts/check_docs.py --help
```

2. Execute a auditoria e verifique higiene do diff em um único comando:

```sh
python3 scripts/check_docs.py && git diff --check
```

3. Se a tarefa envolver muitos arquivos ou revisão documental ampla sem alterações imediatas, delegue a varredura de leitura ao subagente `doc-auditor` (`.agents/agents/doc-auditor.md`) para preservar o contexto principal.

## Formato de saída

- **Status:** passou / falhou (com código de saída).
- **Orçamentos:** destaque apenas arquivos próximos (> 85%) ou acima do teto (`AGENTS.md` 3 KiB, `docs/INDEX.md` 4 KiB, `docs/starters/` 16 KiB, `.agents/rules/` 24.000 B, demais 8 KiB).
- **Violações:** liste caminho, linha e causa exata para correção direta.
- **Limitações:** lembre que o validador não testa URLs externas, sintaxe Mermaid nem medição de tokens.
