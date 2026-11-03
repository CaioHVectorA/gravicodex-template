# Eficiência de contexto

Objetivo: minimizar o contexto necessário para entregar uma mudança correta. Menos texto não compensa omitir um contrato, repetir uma investigação ou aceitar uma regressão.

## Recuperar por necessidade

1. Extraia da tarefa: resultado esperado, restrição e evidência de conclusão.
2. Reutilize caminhos e fatos já confirmados na sessão.
3. Se faltar uma informação, escolha uma rota no [índice](../INDEX.md).
4. Liste nomes no diretório provável; depois procure o símbolo ou contrato. Exemplos:

```sh
rg --files docs/context
rg -n --fixed-strings 'check_docs' scripts tests
```

5. Leia o trecho pertinente e contexto suficiente para entender suas dependências. Amplie a busca se houver consumidores desconhecidos ou resultados contraditórios.
6. Pare a exploração quando conseguir explicar a alteração e como verificá-la. Retome a investigação se a execução trouxer evidência nova.

Evite despejar arquivos gerados, dependências, lockfiles, logs completos e diretórios inteiros no chat. Um resumo de erro deve preservar comando, código de saída e trecho diagnóstico. Saída limitada pode esconder resultados: refine a consulta em vez de presumir que a primeira página é completa.

## Densidade sem linguagem cifrada

- Escreva regras concretas: condição → ação → evidência, quando essa forma ajudar.
- Deixe uma única fonte para cada fato e aponte para ela.
- Registre o motivo de escolhas duráveis em decisões; não replique explicações em todas as entradas.
- Use tabelas para comparar e grafos para relações; prefira prosa curta para uma sequência simples.
- Não use siglas inventadas, XML, JSON ou grafos apenas por suposta economia de tokens. A tokenização depende do modelo e do conteúdo.
- Não esconda orientações em comentários HTML ou `<details>` esperando economizar contexto: o texto continua no arquivo.

## Orçamento local

O validador limita **AGENTS.md a 3 KiB**, **INDEX.md a 4 KiB** e cada outro Markdown a **8 KiB**. São escolhas de manutenção deste template, não limites universais dos agentes. Divida por necessidade de recuperação; criar dezenas de arquivos minúsculos também custa navegação.

O orçamento é em bytes UTF-8. Palavras também são mostradas como indicador grosseiro; nenhuma das duas medidas equivale a tokens. O índice só é lido quando necessário. Limites documentais não autorizam cortar uma investigação necessária.

## Medir antes de afirmar ganho

Compare tarefas equivalentes, usando o mesmo modelo e configuração. Registre a versão/commit, tokens de entrada e saída informados pela ferramenta, tokens em cache quando disponíveis, duração, chamadas de ferramenta, correções e aceitação do resultado. Sem medidor, marque tokens como **não medidos**.

Inclua leituras de ferramenta e retrabalho, não apenas o primeiro prompt. Separe custo faturado de tamanho do contexto; cache e preços podem mudar a relação. As fontes oficiais fundamentam a organização; a redução neste repositório ainda depende de experimento.

## Retomar sem repetir

Se uma tarefa atravessar sessões ou agentes, preserve objetivo, decisões já tomadas, arquivos, evidência e próximo passo usando [o modelo](../templates/task.md). Confirme o estado do Git e o diff antes de confiar no registro. Não arquive raciocínio interno, conversa completa ou tentativas sem valor para a continuação.
