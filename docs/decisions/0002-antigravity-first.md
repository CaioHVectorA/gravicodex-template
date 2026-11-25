# 0002 — Evolução Antigravity-first com customizações nativas e starters descartáveis

## Estado

Aceita em 2026-11-25 para a base GraviCodex. Complementa e atualiza [0001 — Contexto sob demanda](0001-context-on-demand.md) para o foco atual em Google Antigravity, mantendo Codex em *stand-by*.

## Problema e restrições

A base inicial priorizava o menor denominador comum entre Codex e Antigravity, abrindo mão de recursos nativos do Antigravity (rules com `glob`/`model_decision`, skills sob demanda convertidas em `/comando`, hook `SessionStart`, subagente somente leitura e `.geminiignore`). Além disso, iniciar uma POC do zero exigia repetir entrevistas de arquitetura e ainda não havia trilha estruturada para bibliografia acadêmica anti-alucinação.

Restrições mantidas: zero dependências externas obrigatórias (Python 3.11+ stdlib + Markdown), `AGENTS.md` ≤ 3 KiB, validação determinística em CI e proibição de anunciar ganhos de tokens sem medição real.

## Decisão

1. **Identidade e foco:** manter o nome `GraviCodex` para preservar links e histórico, declarando foco operacional em **Google Antigravity** (App/Desktop 2.0, CLI `agy` e IDE) e Codex em *stand-by* via `AGENTS.md`.
2. **Customizações nativas enxutas em `.agents/`:**
   - 3 rules modulares (`markdown-docs`, `academic-references`, `verification`) usando progressive disclosure (`glob` e `model_decision`), sem usar `.agents/workflows/` (descontinuado).
   - 3 skills de alto impacto (`bootstrap-poc`, `audit-docs`, `session-handoff`), evitando inchar a lista de metadados carregada a cada turno.
   - 1 hook `SessionStart` em [.agents/hooks.json](../../.agents/hooks.json) rodando [session_snapshot.py](../../scripts/session_snapshot.py) (habilitado por padrão, *fail-open* silencioso, ≤ 1,5 KB, desligável em 1 linha). Nenhum hook bloqueante em `PreToolUse`/`PreInvocation`.
   - 1 subagente somente leitura ([doc-auditor](../../.agents/agents/doc-auditor.md)) em `model: flash` com ferramentas oficiais verificadas.
3. **Onboarding descartável (`docs/starters/`):** 10 perfis ricos (teto temporário de 16 KiB) combinados a uma fase obrigatória de faxina que remove `docs/starters/`, `docs/playbooks/bootstrap.md` e `.agents/skills/bootstrap-poc/` após o reconhecimento.
4. **Esquema bibliográfico acadêmico:** guia em 3 camadas ([references.md](../guides/references.md)) + modelos copiáveis + regra glob, mantidos apenas em projetos acadêmicos.
5. **Validação e medição offline:** estender [check_docs.py](../../scripts/check_docs.py) para validar frontmatter/hooks do Antigravity e adicionar [bench_transcript.py](../../scripts/bench_transcript.py) para medir `transcript.jsonl` localmente sem prometer economia não comprovada.

## Alternativas e consequências

| Alternativa | Consequência |
| --- | --- |
| Manter apenas Markdown genérico sem `.agents/` | Portável, mas desperdiça progressive disclosure nativo, cold-start e subagente isolado |
| Adicionar hooks `PreToolUse` para bloquear comandos/leituras | Aumenta latência em cada ferramenta e risco de falsos positivos em projetos variados |
| Instalar plugins externos (ex.: MCP) dentro do template | Quebra a premissa zero-dependência; melhor documentá-los como opcionais em [antigravity.md](../guides/antigravity.md) |
| Adotar arquitetura nativa stdlib + faxina obrigatória | Eleva a utilidade no primeiro prompt e protege contra descarte silencioso, com custo pequeno de validação em Python stdlib |

## Verificar ou reconsiderar

Validar continuamente via `scripts/check_docs.py`, suíte `unittest` e smoke test do hook `SessionStart`. Reconsiderar se uma atualização do Antigravity alterar o contrato de `.agents/hooks.json`, frontmatter de rules/skills/subagents, ou se medições reais via `bench_transcript.py` indicarem que o snapshot inicial não compensa seu tamanho em contexto.
