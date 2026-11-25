---
name: bootstrap-poc
description: "Orquestra o primeiro prompt de POC ou novo projeto no estilo /grill-me a partir de docs/starters/, esculpe os Markdowns sob medida e executa a faxina pós-reconhecimento."
---

# Skill: Bootstrap de POC guiado por grill-me

Use esta skill quando o repositório ainda estiver no estado `TEMPLATE` (confirmado em [projeto](../../../docs/context/project.md)) e o usuário pedir para criar uma POC, protótipo ou novo projeto — inclusive quando invocado junto a `/grill-me` ou `/plan /grill-me`. Siga o [playbook completo](../../../docs/playbooks/bootstrap.md).

## Protocolo de entrevista (estilo grill-me)

O objetivo da entrevista não é preencher um formulário genérico, mas **extrair decisões reais para gerar os melhores Markdowns sob medida do projeto** antes de escrever código:

1. **Reconhecimento silencioso (Fase 1):** leia o prompt inicial, consulte [o catálogo de perfis](../../../docs/starters/README.md) e abra **apenas 1 perfil principal** (ou no máximo 2 se cruzar domínios, ex.: `academic` + `iot`). Nunca pergunte o que já está respondido no prompt ou no repositório.
2. **Entrevista ramificada, 1 decisão por vez (Fase 2):**
   - Faça **uma pergunta decisiva por vez** (ou use `ask_question` com opções objetivas), sempre destacando uma opção **`(Recomendada)`** baseada no perfil escolhido e explicando brevemente o trade-off.
   - Use cada resposta para podar ou aprofundar o próximo ramo da árvore de decisão, cobrindo apenas lacunas reais em 4 eixos:
     1. **Problema, usuário, critério de pronto e fora de escopo** → define `docs/context/project.md` e `README.md`.
     2. **Stack enxuta, fronteiras de módulos e contratos** → define `docs/context/map.md` e eventual ADR inicial.
     3. **Verificação real, CI e mocks/simuladores** → define `docs/context/commands.md`, CI e `.agents/rules/verification.md`.
     4. **Invariantes do domínio, riscos e regras sob medida** → define `AGENTS.md`, novas rules em `.agents/rules/` (se houver invariante recorrente), `.geminiignore` e `docs/references/` (se acadêmico).
   - **Checkpoint de entendimento compartilhado:** ao zerar as decisões abertas, apresente um resumo curto mapeando `Decisão fechada → Markdown que será gerado/adaptado/removido` e peça confirmação antes de editar arquivos.
   - **Atalho de escape:** se o usuário pedir explicitamente para pular perguntas e usar padrões recomendados, aplique as recomendações e registre as premissas assumidas em `docs/context/project.md`.
3. **Esculpir Markdowns sob medida + menor fluxo funcional (Fase 3):**
   - Gere documentação específica do projeto (zero texto genérico de template, respeitando fonte única e orçamentos em bytes) e implemente o menor fluxo verificável (ou entregue apenas a arquitetura/Markdowns se o usuário pediu somente especificação inicial).
   - Se for projeto acadêmico, crie `docs/references/` usando [os modelos bibliográficos](../../../docs/templates/bibliography-index.md).
4. **Faxina pós-reconhecimento (Fase 4):** aplique a matriz de remoção do [playbook de bootstrap](../../../docs/playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento), incluindo a auto-remoção desta skill (`.agents/skills/bootstrap-poc/`), `docs/starters/` e `docs/playbooks/bootstrap.md`.
5. **Fechamento obrigatório:** pode `docs/INDEX.md` para remover rotas deletadas e rode:

```sh
python3 scripts/check_docs.py && python3 -m unittest discover -s tests -v && git diff --check
```
