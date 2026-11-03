# Trabalho retomável

Esta pasta guarda apenas registros que precisam sobreviver à sessão ou à troca de ferramenta. Não existe tarefa ativa criada pelo template.

Use [o modelo](../templates/task.md) para criar `id-curto.md`. Mantenha objetivo, base Git, diff relevante, evidência e próximo passo. Para encontrar um registro, busque seu identificador ou o estado:

```sh
rg -n 'Estado:|Objetivo|Próximo passo' docs/tasks
```

Ao retomar, confirme o estado atual do repositório. Ao concluir, marque o resultado e mova para `docs/tasks/archive/` se precisar conservar o histórico. Não leia o arquivo inteiro de tarefas nem o histórico arquivado como rotina de início.

Uma decisão durável pertence a `docs/decisions/`; o registro da tarefa apenas aponta para ela. Não transforme esta pasta em cópia de todas as conversas.
