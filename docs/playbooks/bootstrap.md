# Adaptar a um produto

Use este procedimento ao iniciar um produto com a base; ele não é pré-requisito para editar o template.

1. Defina problema, usuário e primeiro resultado verificável. Aproveite o contexto já fornecido; pergunte somente pelas decisões ausentes que mudem o produto.
2. Atualize [projeto](../context/project.md): escopo, restrições e estado real. Mantenha incógnitas explícitas.
3. Escolha stack e estrutura a partir dessas necessidades. Não instale dependências apenas para preencher o template. Registre uma decisão se houver alternativas estruturais relevantes.
4. Crie o menor fluxo funcional. Substitua o [mapa](../context/map.md) por componentes e caminhos que existam; adicione [contratos](../templates/component.md) apenas nas fronteiras que precisem deles.
5. Execute instalação, build e testes aplicáveis; registre comandos comprovados em [comandos](../context/commands.md). Ajuste CI às verificações do produto e mantenha a checagem documental.
6. Revise [AGENTS.md](../../AGENTS.md) para o projeto real. Mantenha a entrada curta; procedimentos específicos ficam nas rotas sob demanda.
7. Remova exemplos sem utilidade, renomeie o README e ajuste o índice. Não preserve texto do template como se fosse uma decisão do produto.

Pronto quando uma pessoa ou agente, em sessão nova, consegue localizar a entrada, executar o fluxo principal e validar uma mudança sem receber uma transcrição de contexto.
