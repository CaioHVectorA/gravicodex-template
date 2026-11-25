# Comandos verificados

Execute na raiz. Requer Python 3.11+; usa somente a biblioteca padrão. `rg` é conveniência para busca, não dependência da validação. Todos os scripts aceitam `--help`.

| Intenção | Comando | Quando |
| --- | --- | --- |
| Conferir Markdown e `.agents/` | `python3 scripts/check_docs.py` | Mudanças em Markdown, links, limites ou `.agents/` |
| Rodar suíte completa de testes | `python3 -m unittest discover -s tests -v` | Mudanças em scripts, hooks ou testes |
| Testar hook `SessionStart` | `printf '{"workspacePaths":["."]}\n' \| python3 scripts/session_snapshot.py` | Mudanças no snapshot ou detecção `TEMPLATE`/`PRODUTO` |
| Resumir/comparar transcript local | `python3 scripts/bench_transcript.py --help` | Medir turnos, ferramentas e tokens em `transcript.jsonl` |
| Conferir espaços e conflitos | `git diff --check` | Antes de concluir alterações |
| Ver alterações locais | `git status --short` | Antes de editar e antes de concluir |

## O que a checagem cobre

[check_docs.py](../../scripts/check_docs.py) valida:

- Markdown: links locais inline literais, âncoras de títulos simples, cercas de código fechadas e limites em bytes (`AGENTS.md` ≤ 3 KiB, `docs/INDEX.md` ≤ 4 KiB, `docs/starters/*.md` ≤ 16 KiB, `.agents/rules/*.md` ≤ 24.000 bytes, demais permanentes ≤ 8 KiB).
- Customizações Antigravity: frontmatter YAML obrigatório em `.agents/rules/*.md` (`trigger`, `description`/`globs`), `.agents/skills/*/SKILL.md` (`description`) e `.agents/agents/*.md` (`name`, `description`), esquema/eventos de `.agents/hooks.json` e bloqueio ao legado `.agents/workflows/`.

Não consulta URLs externas, não renderiza Mermaid, não valida execução interativa do app/CLI do Antigravity e não mede tokens. Confira diagramas alterados no preview do GitHub.

A [CI](../../.github/workflows/docs.yml) executa `check_docs.py`, `unittest`, smoke test do `session_snapshot.py` e `git diff --check`. Ao criar um produto, registre aqui os comandos reais de build, lint e testes da stack escolhida.
