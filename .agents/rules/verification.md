---
trigger: model_decision
description: "Aplicar ao validar mudanças, escolher comandos de teste por tipo de alteração ou revisar diffs antes de concluir uma tarefa."
---

# Critérios de verificação e revisão de diff

Use este checklist antes de encerrar qualquer mudança de código, script, configuração ou documentação. Procedimento completo: [mudança](../../docs/playbooks/change.md).

## Validação por tipo de mudança

| Tipo | Evidência mínima obrigatória |
| --- | --- |
| Documentação / Markdown | `python3 scripts/check_docs.py` + `git diff --check` |
| Scripts / Validador / Hooks | `python3 scripts/check_docs.py && python3 -m unittest discover -s tests -v && git diff --check` |
| Funcionalidade ou bug de produto | Testes do fluxo atingido + comandos registrados em [comandos](../../docs/context/commands.md) |
| Customizações `.agents/` | Validação pelo `check_docs.py` + teste isolado de script/hook quando aplicável |

## Higiene de verificação e honestidade

- Agrupe checagens independentes com `&&` quando fizer sentido para reduzir turnos; preserve comando, código de saída e trecho diagnóstico se algo falhar.
- Inspecione `git status --short` e `git diff --stat` antes de responder para detectar arquivos esquecidos, regressões ou documentação fora de sincronia.
- Diferencie explicitamente: (a) comportamento verificado por execução/teste, (b) comportamento apenas documentado pela ferramenta e (c) limitações não testadas no ambiente atual.
- Nunca afirme economia percentual de tokens ou latência sem medição registrada via [protocolo de eficiência](../../docs/guides/efficiency.md#medir-antes-de-afirmar-ganho).
