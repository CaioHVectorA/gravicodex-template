# Google Antigravity nesta base

Documentação oficial consultada em **2026-11-25** ([fontes consultadas](../research/sources.md)). Esta base é **Antigravity-first** (App/Desktop 2.0, CLI `agy` e Antigravity IDE); o suporte a Codex permanece em *stand-by* via `AGENTS.md`.

## Hierarquia nativa de customização

| Camada | Caminho | Quando carrega | Papel nesta base |
| --- | --- | --- | --- |
| Entrada raiz | [AGENTS.md](../../AGENTS.md) | Sempre ativa (`always_on`) | Acordo curto (≤ 3 KiB), gatilho `/bootstrap-poc` e hábitos de eficiência |
| Rules modulares | `.agents/rules/*.md` | `glob`, `model_decision`, `always_on` ou `manual` | Regras de Markdown, referências acadêmicas e verificação |
| Skills sob demanda | `.agents/skills/<nome>/SKILL.md` | Nome + descrição visíveis; corpo carregado sob demanda ou via `/<nome>` | 3 procedimentos enxutos: `/bootstrap-poc`, `/audit-docs`, `/session-handoff` |
| Lifecycle hook | [.agents/hooks.json](../../.agents/hooks.json) | `SessionStart` (1x na abertura da sessão) | Snapshot de cold-start via [session_snapshot.py](../../scripts/session_snapshot.py) (≤ 1,5 KB, *fail-open*) |
| Subagente leve | [.agents/agents/doc-auditor.md](../../.agents/agents/doc-auditor.md) | Delegado via `invoke_subagent` | Auditoria somente leitura em `model: flash` sem poluir contexto principal |
| Filtro FinOps | [.geminiignore](../../.geminiignore) | Exclui ruído em buscas/indexação quando suportado pela superfície | Ignora `.venv/`, `node_modules/`, `dist/`, lockfiles extensos e binários pesados |

### Cuidados verificados na documentação oficial

- **Descarte silencioso de rules:** arquivos em `.agents/rules/*.md` sem frontmatter YAML ou com `trigger` inválido (ex.: `camelCase`) são ignorados sem erro. Cada arquivo tem teto oficial de **24.000 bytes**; todas as rules `always_on` + globais dividem orçamento de 20.000 tokens.
- **Legado removido:** `.agents/workflows/` foi descontinuado (migração oficial para `.agents/skills/`).
- **Subagentes customizados:** nomes incorretos ou não mapeados em `tools` podem travar a execução do subagente. Use apenas nomes oficiais verificados (`view_file`, `list_dir`, `find_by_name`, `grep_search`).
- **Hooks sem atrito por passo:** este template usa apenas `SessionStart` (habilitado por padrão; desligável com `"enabled": false` em `.agents/hooks.json`). Não adiciona hooks bloqueantes em `PreToolUse`/`PreInvocation` que somam latência em toda ferramenta.
- **`.geminiignore`:** reduz ruído em varreduras, mas não substitui regras de permissão/sandbox (`deny` list) para segredos ou arquivos sensíveis; o respeito ao arquivo pode variar entre versões da CLI e do App.

## Comandos nativos e atalhos no dia a dia

| Recurso | Quando usar | Efeito prático |
| --- | --- | --- |
| `@arquivo` / `@pasta` | Quando você já sabe o alvo | Envia caminho canônico sem gastar turno de busca |
| `/plan` | Mudança multi-arquivo ou com risco | Separa exploração e plano revisável antes de editar |
| `/grill-me` | Requisitos ambíguos na POC ou arquitetura | Entrevista curta para fechar decisões antes do código |
| `/compact` | Entre marcos longos da mesma sessão | Resume histórico para reduzir degradação do contexto |
| `/learn` | Após corrigir um padrão recorrente | Converte a lição em regra ou skill reutilizável |
| `/swarm` | Tarefa ampla divisível em trilhas independentes | Coordena workers paralelos + verificador no mesmo quadro |
| `/browser` | Validação visual de UI, console e rede | Abre subagente de navegador para testar fluxos web reais |
| `/hooks` e `/agents` | Diagnóstico na CLI `agy` | Lista hooks carregados e monitora subagentes ativos |

## Plugins complementares opcionais

Este template permanece **100% stdlib/Markdown**, sem exigir plugins externos. Em projetos maiores que justificarem extensões locais, avalie combinar externamente:

- **`INK-Q/agy-fast`** (MCP local): útil em repositórios médios/grandes com muitas buscas, outlines e edições em lote.
- **`Domush/antigravity-plugin-context-mode`**: útil quando builds, testes ou comandos geram logs massivos que inflam o histórico do App.
- **Monitores de uso e cache** (e `/usage` ou `/context` na CLI `agy`): úteis para acompanhar consumo real antes e depois de ajustes.

Trate percentuais de economia divulgados por plugins de terceiros como hipóteses a reproduzir no seu repositório com [bench_transcript.py](../../scripts/bench_transcript.py) e [o protocolo de medição](efficiency.md#medir-antes-de-afirmar-ganho). Revise código e permissões antes de instalar qualquer plugin externo.

## Nota sobre Codex (stand-by)

Codex continua reconhecendo `AGENTS.md` na raiz caso você retome uma tarefa nele. As extensões nativas em `.agents/` (rules com frontmatter, skills, `hooks.json` e subagente) são específicas do Google Antigravity e não são executadas pelo Codex; por isso, contratos duráveis do produto continuam acessíveis pelo [índice comum](../INDEX.md).
