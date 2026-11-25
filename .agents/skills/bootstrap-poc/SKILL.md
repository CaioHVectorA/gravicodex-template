---
name: bootstrap-poc
description: "Orquestra o primeiro prompt de POC ou novo projeto a partir de docs/starters/, configura o repositório e executa a faxina pós-reconhecimento."
---

# Skill: Bootstrap de POC e faxina pós-reconhecimento

Use esta skill quando o repositório ainda estiver no estado `TEMPLATE` (confirmado em [projeto](../../../docs/context/project.md)) e o usuário pedir para criar uma POC, protótipo ou novo projeto. Siga o [playbook completo](../../../docs/playbooks/bootstrap.md).

## Árvore de decisão

1. **Reconhecimento (Fase 1):** consulte [o catálogo de perfis](../../../docs/starters/README.md) e abra **apenas 1 perfil principal** (ou no máximo 2 se o projeto combinar domínios, como `academic` + `iot` ou `ai-data` + `backend-api`). Nunca leia todos os perfis por rotina.
2. **Corte de escopo (Fase 2):** faça apenas as perguntas de corte do perfil que realmente alteram arquitetura, stack ou critério de pronto — aproveite tudo o que o usuário já informou. Se faltar decisão crítica, use perguntas diretas ou `/grill-me`.
3. **Construção enxuta (Fase 3):**
   - Reescreva `docs/context/project.md`, `docs/context/map.md`, `docs/context/commands.md`, `README.md` e ajuste `AGENTS.md` e `.github/workflows/` para o produto real.
   - Se o projeto for acadêmico, crie `docs/references/` usando [os modelos bibliográficos](../../../docs/templates/bibliography-index.md).
   - Implemente o menor fluxo funcional verificável e valide com comandos reais.
4. **Faxina pós-reconhecimento (Fase 4):** aplique a matriz de remoção do [playbook de bootstrap](../../../docs/playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento), incluindo a auto-remoção desta própria skill (`.agents/skills/bootstrap-poc/`), `docs/starters/` e `docs/playbooks/bootstrap.md`.
5. **Fechamento obrigatório:** pode `docs/INDEX.md` para remover rotas deletadas e rode:

```sh
python3 scripts/check_docs.py && python3 -m unittest discover -s tests -v && git diff --check
```
