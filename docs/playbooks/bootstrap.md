# Adaptar a base para um produto ou POC (Bootstrap via grill-me)

Procedimento em 4 fases alinhado à skill [`/bootstrap-poc`](../../.agents/skills/bootstrap-poc/SKILL.md) e ao estilo de entrevista socrática do comando nativo `/grill-me`. Use ao transformar este template em um projeto real; não é necessário para manter o próprio template.

## Como o usuário aciona

O usuário não precisa redigir uma especificação gigante no primeiro prompt. Basta abrir o repositório no Antigravity e enviar uma ideia curta com um destes formatos:

- `/grill-me /bootstrap-poc Quero criar <ideia resumida do projeto>` *(recomendado para alinhar requisitos e esculpir os Markdowns antes de codar)*
- `/plan /grill-me Quero criar <ideia resumida do projeto>` *(entrevista + plano revisável antes de editar arquivos)*
- Ou um prompt direto descrevendo a POC: enquanto `docs/context/project.md` estiver em `TEMPLATE`, o agente ativa `/bootstrap-poc` automaticamente.

## Fase 1: Reconhecimento silencioso

1. Leia o primeiro prompt do usuário e identifique o domínio principal (e se há segundo domínio).
2. Abra [o catálogo de perfis](../starters/README.md) e escolha **1 perfil principal** (ou no máximo **2 perfis combinados**, ex.: `academic` + `iot`, `ai-data` + `backend-api`).
3. Abra somente o(s) perfil(is) escolhido(s) em `docs/starters/` para carregar as perguntas de corte, armadilhas e opções de stack. Nunca leia os 10 perfis por rotina.

## Fase 2: Entrevista estilo grill-me orientada aos Markdowns

Em vez de despejar uma lista longa de perguntas ou gerar Markdowns genéricos cheios de placeholders, conduza uma **entrevista ramificada, uma decisão por vez**:

1. **Não pergunte o óbvio:** aproveite tudo o que o usuário já informou no prompt ou que pode ser inferido do perfil.
2. **Uma pergunta de corte por vez com recomendação:** para cada decisão aberta que muda arquitetura, stack, contrato ou verificação, apresente opções curtas marcando a opção **`(Recomendada)`** e o motivo objetivo (usando `ask_question` quando disponível ou pergunta direta no chat).
3. **Ramificação viva:** cada resposta fecha ou abre a pergunta seguinte, cobrindo os 4 eixos que alimentam os Markdowns finais do projeto:

| Eixo da entrevista | O que decide | Markdowns esculpidos na Fase 3 |
| --- | --- | --- |
| 1. Problema e recorte da POC | Usuário, fluxo ponta a ponta, critério de pronto e o que fica fora | `docs/context/project.md`, `README.md` |
| 2. Stack, fronteiras e contratos | Linguagem/framework enxuto, pastas reais, interfaces e trade-offs | `docs/context/map.md`, ADR inicial em `docs/decisions/` (se houver alternativa relevante) |
| 3. Verificação e CI | Testes reais, lint/build, mocks/simuladores quando faltar hardware ou API | `docs/context/commands.md`, `.github/workflows/`, `.agents/rules/verification.md` |
| 4. Invariantes e regras do domínio | Armadilhas a bloquear, convenções por extensão, dados sensíveis ou bibliografia | `AGENTS.md` (≤ 3 KiB), rules sob medida em `.agents/rules/`, `.geminiignore`, `docs/references/` (se acadêmico) |

4. **Síntese de entendimento compartilhado (checkpoint obrigatório):** quando não restarem decisões abertas, apresente um resumo curto (`Decisões fechadas → Markdowns que serão criados/adaptados/deletados`) e aguarde confirmação antes de editar o repositório.
5. **Atalho sem entrevista:** se o usuário pedir explicitamente *"pule perguntas e use os padrões recomendados"*, siga direto para a Fase 3 deixando todas as premissas explícitas em `docs/context/project.md`.

## Fase 3: Esculpir os Markdowns sob medida e menor fluxo funcional

1. **Reescreva a base documental com precisão de produto** (zero texto residual de template, fonte única por fato, respeitando os limites em bytes):
   - [projeto](../context/project.md): problema, usuário, escopo, restrições, premissas e estado real (removendo os marcadores de template para que [session_snapshot.py](../../scripts/session_snapshot.py) passe a reportar `PRODUTO`).
   - [mapa](../context/map.md): tabela e diagrama Mermaid apenas com módulos, pastas e contratos que realmente existem.
   - [comandos](../context/commands.md): comandos de instalação, execução, lint, build e teste comprovados na stack escolhida.
   - [AGENTS.md](../../AGENTS.md) e [README.md](../../README.md): identidade, regras curtas da stack (≤ 3 KiB) e instruções reais do produto.
   - `.agents/rules/`: adicione 1 regra `glob` específica da stack/domínio somente se houver invariante recorrente concreto (ex.: migrações SQL, HAL embarcado, schema de API); mantenha `.agents/rules/academic-references.md` apenas se o projeto for acadêmico.
   - [.geminiignore](../../.geminiignore) e [CI](../../.github/workflows/docs.yml): ajuste exclusões FinOps e adicione build/testes reais do produto mantendo `check_docs.py`.
2. Se o projeto for acadêmico (ou híbrido com `academic`), crie `docs/references/README.md` e `docs/references/references.bib` a partir de [bibliography-index.md](../templates/bibliography-index.md).
3. Implemente o menor fluxo funcional verificável da POC (ou encerre na documentação/arquitetura se o usuário pediu apenas os Markdowns primeiro) e valide com comandos reais.

## Fase 4: Faxina pós-reconhecimento

Todo o material descartável de onboarding deve sair do repositório do produto assim que a base estiver estruturada, reduzindo ruído e manutenção.

| Ação | Caminhos | Condição |
| --- | --- | --- |
| **Sempre deletar** | `docs/starters/`, `docs/playbooks/bootstrap.md`, `.agents/skills/bootstrap-poc/` | Obrigatório ao concluir o bootstrap |
| **Manter só se acadêmico** | `docs/guides/references.md`, `.agents/rules/academic-references.md`, `docs/templates/bibliography-index.md`, `docs/templates/source-note.md` | Deletar em projetos sem bibliografia formal |
| **Substituir ou deletar** | `docs/research/sources.md`, `docs/decisions/0001-context-on-demand.md`, `docs/decisions/0002-antigravity-first.md` | Substituir por pesquisa/ADRs do produto ou remover se irrelevantes |
| **Preservar e adaptar** | `AGENTS.md`, `docs/INDEX.md`, `docs/context/*`, `docs/guides/{antigravity,efficiency,markdown}.md`, `docs/playbooks/change.md`, `docs/tasks/`, `docs/templates/{task,decision,component}.md`, `.agents/{hooks.json,rules/{markdown-docs,verification}.md,skills/{audit-docs,session-handoff}/,agents/doc-auditor.md}`, `.geminiignore`, `scripts/*`, `tests/*` | Manter operacionais para o produto |

### Fechamento obrigatório da faxina

1. Pode [docs/INDEX.md](../INDEX.md) e [README.md](../../README.md) removendo qualquer link para arquivos deletados e incluindo eventuais novos contratos/ADRs do produto.
2. Execute a validação completa para garantir **zero links quebrados** e customizações íntegras:

```sh
python3 scripts/check_docs.py && python3 -m unittest discover -s tests -v && git diff --check
```

3. Pronto quando uma sessão nova do Antigravity recebe o snapshot com `Modo: PRODUTO`, lê Markdowns sob medida sem lixo de template e valida o fluxo principal sem transcrição prévia.
