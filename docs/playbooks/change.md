# Fazer uma mudança

Use a parte pertinente; uma correção pequena não precisa de plano, ADR ou arquivo de tarefa.

## Delimitar

Defina o comportamento final e a evidência que demonstrará sucesso. Veja o estado do Git; localize o contrato e os consumidores atingidos. Consulte [projeto](../context/project.md), [mapa](../context/map.md) ou [comandos](../context/commands.md) somente se faltar essa informação.

| Tipo de trabalho | Evidência inicial | Validação principal |
| --- | --- | --- |
| Bug | Reprodução ou diagnóstico observável | Caso deixa de falhar e comportamento vizinho continua válido |
| Funcionalidade | Critério de aceitação concreto | Fluxo novo produz o resultado esperado |
| Refatoração | Contrato e consumidores existentes | Mesmo comportamento nos pontos atingidos |
| Documentação | Fato incorreto, lacuna ou caminho inválido | Fonte conferida, links íntegros, instrução executável |
| Revisão | Diff e contrato afetado | Achado reproduzível com consequência |

## Executar

Faça a mudança completa de menor alcance. Preserve trabalho existente e não reformate áreas alheias. Consulte ou crie uma decisão apenas para uma escolha estrutural com alternativas e consequências duráveis; use [o modelo](../templates/decision.md).

Se o trabalho precisar de outra sessão ou ferramenta, salve [um registro de tarefa](../templates/task.md). Não dependa da memória da conversa como único lugar de uma decisão necessária.

## Verificar e concluir

Use os comandos reais da stack. Escolha testes pelo comportamento atingido; para uma edição textual, a checagem documental e a conferência da fonte bastam. Se alterar o validador, seus testes devem cobrir o caso que motivou a alteração.

Revise o diff para omissões, regressões e documentação desatualizada. Registre o comando e resultado; diferencie verificação passada, falha e não executada. Não repita a mesma suíte sem mudança ou evidência nova que justifique.

Conclua com o resultado, a validação e qualquer pendência material. Arquive o registro de tarefa se existir; não anuncie publicação ou execução que não ocorreu.
