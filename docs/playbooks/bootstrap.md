# Adaptar a base para um produto ou POC (Bootstrap)

Procedimento em 4 fases alinhado à skill [`/bootstrap-poc`](../../.agents/skills/bootstrap-poc/SKILL.md). Use apenas ao transformar este template em um projeto real; não é necessário para manter o próprio template.

## Fase 1: Reconhecimento

1. Leia o primeiro prompt do usuário e identifique o domínio principal do projeto.
2. Abra [o catálogo de perfis](../starters/README.md) e escolha **1 perfil principal** (ou no máximo **2 perfis combinados**, por exemplo `academic` + `iot`, `ai-data` + `backend-api` ou `web` + `backend-api`).
3. Abra somente o(s) perfil(is) escolhido(s) em `docs/starters/`. Nunca leia os 10 perfis por rotina.

## Fase 2: Entrevista de corte e escopo verificável

1. Aproveite todo contexto já fornecido no prompt do usuário.
2. Usando as perguntas de corte do perfil, pergunte **somente** pelas decisões ausentes que realmente mudam stack, fronteiras arquiteturais ou critério de pronto (use `/grill-me` se houver múltiplas incertezas de produto).
3. Feche o menor recorte verificável da POC (1 fluxo ponta a ponta observável, dependências mínimas, estratégia real de teste/simulação e o que fica explicitamente fora desta entrega).

## Fase 3: Atualização da base e menor fluxo funcional

1. Substitua o estado de template nos documentos centrais:
   - [projeto](../context/project.md): problema, usuário, escopo, restrições e estado real (removendo os marcadores de template para que [session_snapshot.py](../../scripts/session_snapshot.py) passe a reportar `PRODUTO`).
   - [mapa](../context/map.md): apenas módulos, pastas e contratos que realmente existem.
   - [comandos](../context/commands.md): comandos de instalação, execução, lint, build e teste comprovados na stack escolhida.
   - [AGENTS.md](../../AGENTS.md) e [README.md](../../README.md): identidade, entrada curta (≤ 3 KiB) e instruções reais do produto.
   - [CI](../../.github/workflows/docs.yml): adicionar ou criar workflow com build/testes reais do produto mantendo a checagem documental.
2. Se o projeto for acadêmico (ou híbrido com `academic`), crie `docs/references/README.md` e `docs/references/references.bib` a partir de [bibliography-index.md](../templates/bibliography-index.md) e mantenha [references.md](../guides/references.md) e `.agents/rules/academic-references.md`.
3. Implemente o menor fluxo funcional da POC e valide-o com evidência executável (incluindo mocks/simuladores quando faltar hardware ou serviço externo).

## Fase 4: Faxina pós-reconhecimento

Todo o material descartável de onboarding deve sair do repositório do produto assim que a POC estiver estruturada, reduzindo ruído e manutenção.

| Ação | Caminhos | Condição |
| --- | --- | --- |
| **Sempre deletar** | `docs/starters/`, `docs/playbooks/bootstrap.md`, `.agents/skills/bootstrap-poc/` | Obrigatório ao concluir o bootstrap |
| **Manter só se acadêmico** | `docs/guides/references.md`, `.agents/rules/academic-references.md`, `docs/templates/bibliography-index.md`, `docs/templates/source-note.md` | Deletar em projetos sem bibliografia formal |
| **Substituir ou deletar** | `docs/research/sources.md`, `docs/decisions/0001-context-on-demand.md`, `docs/decisions/0002-antigravity-first.md` | Substituir por pesquisa/ADRs do produto ou remover se irrelevantes |
| **Preservar e adaptar** | `AGENTS.md`, `docs/INDEX.md`, `docs/context/*`, `docs/guides/{antigravity,efficiency,markdown}.md`, `docs/playbooks/change.md`, `docs/tasks/`, `docs/templates/{task,decision,component}.md`, `.agents/{hooks.json,rules/{markdown-docs,verification}.md,skills/{audit-docs,session-handoff}/,agents/doc-auditor.md}`, `.geminiignore`, `scripts/*`, `tests/*` | Manter operacionais para o produto |

### Fechamento obrigatório da faxina

1. Pode [docs/INDEX.md](../INDEX.md) e [README.md](../../README.md) removendo qualquer link para arquivos deletados.
2. Execute a validação completa para garantir **zero links quebrados** e customizações íntegras:

```sh
python3 scripts/check_docs.py && python3 -m unittest discover -s tests -v && git diff --check
```

3. Pronto quando uma sessão nova do Antigravity recebe o snapshot com `Modo: PRODUTO`, localiza o código e valida o fluxo principal sem transcrição prévia.
