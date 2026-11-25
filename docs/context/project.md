# Projeto

## Estado atual

GraviCodex é um template **Antigravity-first** para engenharia assistida pelo **Google Antigravity** (App/Desktop 2.0, CLI `agy` e IDE), mantendo Codex em *stand-by* via `AGENTS.md`. O acervo combina documentação sob demanda em Markdown, customizações nativas em `.agents/` (rules, skills, hook `SessionStart`, subagente `doc-auditor`), perfis descartáveis de POC (`docs/starters/`), scripts em Python 3.11+ stdlib e CI; ainda não há aplicação de produto.

## Objetivo

Fornecer entrada curta, snapshot de cold-start *fail-open*, regras/skills nativas com progressive disclosure, pipeline de primeiro prompt para POCs e esquema acadêmico opcional que reduzam atrito de inicialização e manutenção sem exigir dependências externas.

## Contrato desta base

- Público: pessoas e agentes no Google Antigravity trabalhando no mesmo repositório.
- Idioma da documentação: português; caminhos e identificadores técnicos podem usar inglês.
- Restrições: zero dependências externas obrigatórias, `AGENTS.md` ≤ 3 KiB, informação com proprietário claro, nenhuma afirmação de economia sem medição real.
- Pronto quando: uma tarefa localiza contexto sob demanda, executa a mudança e apresenta evidência verificável; em projetos novos, `/bootstrap-poc` adapta a base e conclui a faxina sem links quebrados.
- Fora de escopo: prometer redução fixa de tokens/latência, instalar plugins terceiros por padrão ou impor stack de aplicação antes do bootstrap.

## Ao criar um produto

Acione `/bootstrap-poc` ([playbook](../playbooks/bootstrap.md)) e substitua este perfil por: problema, usuário, resultado observável, escopo, restrições e estado real. Remova esta seção e os marcadores de template para que [session_snapshot.py](../../scripts/session_snapshot.py) passe a identificar o repositório como `PRODUTO`. Atualize [comandos](commands.md) e [mapa](map.md) com caminhos existentes.

Detalhes voláteis de tarefas pertencem a [registros de trabalho](../tasks/README.md), não a este perfil.
