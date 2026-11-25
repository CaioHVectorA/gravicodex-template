# Fundamentação e limites

Documentação oficial consultada em **2026-11-25**. As descrições abaixo separam estritamente o que foi verificado nas fontes oficiais, o que inspirou decisões locais e o que **não** foi demonstrado neste repositório.

## Fontes oficiais consultadas

| Fonte | Informação conferida | Aplicação nesta base |
| --- | --- | --- |
| [Google Antigravity — Rules](https://antigravity.google/docs/rules/) | `AGENTS.md` sem frontmatter (`always_on`); `.agents/rules/*.md` com frontmatter YAML (`always_on`, `model_decision`, `glob`, `manual`), descarte silencioso se inválido, teto de 24.000 bytes por arquivo e orçamento agregado de 20.000 tokens | Entrada enxuta + 3 rules em `.agents/rules/` + validação estática em `scripts/check_docs.py` |
| [Google Antigravity — Agent Skills](https://antigravity.google/docs/skills/) | `.agents/skills/<nome>/SKILL.md` com `description` obrigatória, conversão automática em `/<nome>`, scripts como caixa-preta via `--help`, progressive disclosure | 3 skills focadas (`/bootstrap-poc`, `/audit-docs`, `/session-handoff`) + validação de frontmatter |
| [Google Antigravity — Workflows to Skills](https://antigravity.google/docs/migration/workflows-to-skills/) | Descontinuação de `.agents/workflows/` e migração para `.agents/skills/` | Zero uso de `.agents/workflows/`; validador alerta se pasta legado existir |
| [Google Antigravity — Hooks](https://antigravity.google/docs/hooks/) | `.agents/hooks.json`, campo `enabled`, 6 eventos (`SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`), contrato JSON stdin/stdout (`injectSteps` com `systemMessage`) | Hook `SessionStart` zero-dependência (`session_snapshot.py`) sem hooks bloqueantes por passo |
| [Google Antigravity — Custom Subagents](https://antigravity.google/docs/subagents/) | `.agents/agents/<nome>.md` (`name`, `description`, `tools`, `subagent`, `mainAgent`, `model`), risco de travamento com nomes de ferramentas inválidos | Subagente somente leitura `doc-auditor` (`model: flash`, 4 ferramentas oficiais verificadas) |
| [Google Antigravity — CLI Best Practices](https://antigravity.google/docs/cli/best-practices/) | Loops de verificação local, explorar → planejar → executar, `@arquivo`, `/compact`, subagentes paralelos | Hábitos em `AGENTS.md` e guia [antigravity.md](../guides/antigravity.md) |
| [OpenAI — AGENTS.md](https://developers.openai.com/codex/guides/agents-md) *(stand-by)* | Descoberta de `AGENTS.md` e limite padrão de 32 KiB | Preservado apenas como nota de *stand-by* na raiz |
| [GitHub — Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) | Diagramas Mermaid em cercas de código | Grafos textuais versionáveis no repositório |

## Referências conceituais da comunidade

Nenhuma linha de código de terceiros foi copiada; este template permanece 100% Python stdlib + Markdown. Padrões conceituais observados na comunidade:

- `INK-Q/agy-fast` e `oil-oil/agy-fast-io`: inspiração conceitual para snapshot único de cold-start, leituras paralelas no mesmo turno e agrupamento de comandos de verificação.
- `Domush/antigravity-plugin-context-mode`: referência para evitar despejo de logs extensos no chat e documentada como plugin externo opcional em [antigravity.md](../guides/antigravity.md).
- `rizalkr/agy-setup`, `vudovn/ag-kit`, `affaan-m/ECC`: referências de organização de kits, regras modulares e higiene de contexto.

## O que não foi demonstrado neste repositório

- **Sem benchmark de economia:** não há medição neste template provando redução percentual de tokens, custo ou latência; números divulgados por plugins externos não são tratados como garantias.
- **Execução interativa do App/CLI:** o contrato de `.agents/hooks.json`, rules, skills e subagente foi validado contra a documentação oficial e por testes unitários/CLI dos scripts Python, sem execução interativa dentro do binário Desktop/CLI do Antigravity neste ambiente.
- **`.geminiignore`:** o respeito ao arquivo depende da superfície e versão do agente; não substitui políticas de sandbox/permissão (`deny` list).
- **Bytes ≠ tokens:** limites em bytes são guardrails de manutenção; para medições reais de sessão, use [bench_transcript.py](../../scripts/bench_transcript.py) conforme [eficiência](../guides/efficiency.md#medir-antes-de-afirmar-ganho).
