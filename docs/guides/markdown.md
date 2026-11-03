# Markdown para recuperação

## Estrutura

- Um propósito por documento, título H1 único e subtítulos descritivos. Abra com o que o leitor precisa decidir ou fazer.
- Use links relativos explícitos, tabelas curtas e cercas com linguagem. O perfil verificável usa links inline literais: `[rótulo](arquivo.md#secao)`.
- Para caminhos com espaços, use `<caminho com espaços.md>`. Prefira novos caminhos sem espaços; não use links de referência, HTML ou imagens para navegação obrigatória.
- Âncoras verificadas são derivadas de títulos simples: minúsculas, remoção de pontuação e espaços convertidos em hífens; acentos são preservados. Evite títulos duplicados, formatação inline em títulos e IDs HTML.
- Não crie links navegáveis para caminhos fictícios de modelos. Apresente esses caminhos entre crases e substitua ao instanciar o modelo.
- Frontmatter só quando uma ferramenta o consumir. Metadados decorativos aumentam o custo de manutenção.

O validador cobre esse subconjunto, não a especificação completa de Markdown. Texto em cercas e código inline não é interpretado como link navegável. Links externos precisam de conferência separada.

## Fonte única

Comandos pertencem a [comandos](../context/commands.md), estado a [projeto](../context/project.md), relações ao [mapa](../context/map.md), motivos a decisões e progresso a tarefas. Linke esses arquivos em vez de repetir seus conteúdos. Um resumo derivado deve indicar sua origem e ser revisado junto dela.

## Grafos úteis

Use `mermaid` em cerca para relações de dependência, fluxo de dados ou estados. Mantenha diagramas focados em uma pergunta, com nomes identificáveis e setas explicadas. Texto descritivo junto ao grafo deve permitir compreender a relação mesmo sem renderizador.

O grafo não é uma base de conhecimento executável. Confira cada nó contra caminhos existentes ou marque-o como conceitual; confira cada relação contra implementação ou contrato. Para um mapa textual do repositório, veja [o exemplo real](../context/map.md).

Renderize diagramas alterados antes de depender de sua apresentação. A checagem local só verifica cercas e referências escritas como links Markdown, não a sintaxe interna do Mermaid.

## Evolução

Atualize o documento dono do fato quando o comportamento mudar. Adicione uma rota no índice se o novo conhecimento precisar ser encontrado por tarefa. Remova orientações obsoletas, mas preserve decisões históricas com estado substituído e ligação para sua sucessora.

O uso de `<details>`, comentários ou imagens pode melhorar apresentação, mas não reduz por si só o texto que um agente recebe.
