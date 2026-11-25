---
name: session-handoff
description: "Cria, atualiza ou arquiva um registro curto de retomada em docs/tasks/ usando docs/templates/task.md sem transcrever a conversa."
---

# Skill: Registro curto de retomada

Use esta skill ao pausar uma tarefa multi-sessão, preparar troca de agente ou concluir um trabalho que já possuía registro em [tarefas](../../../docs/tasks/README.md). Não crie registro para ajustes triviais já finalizados.

## Fluxo

1. **Verifique o estado real antes de escrever:**

```sh
git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD && git status --short
```

2. **Escolha a operação:**
   - **Criar:** copie a estrutura de [docs/templates/task.md](../../../docs/templates/task.md) para `docs/tasks/<id-curto>.md`.
   - **Atualizar:** abra apenas o registro ativo pertinente, sincronize SHA/diff/evidências e substitua o próximo passo.
   - **Arquivar:** ao concluir, marque `Estado: concluída`, registre a verificação final e mova para `docs/tasks/archive/<id-curto>.md` se precisar guardar histórico.
3. **Regras de concisão:**
   - Inclua apenas objetivo, critério de pronto, estado Git confirmado, decisões aplicáveis, tabela de evidências reais e próximo passo concreto.
   - Nunca transcreva chat, raciocínio interno, segredos ou logs extensos.
   - Se a sessão continuar após um marco grande, sugira `/compact`.
4. **Valide os links:** rode `python3 scripts/check_docs.py && git diff --check`.
