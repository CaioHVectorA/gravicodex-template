# Comandos verificados

Execute na raiz. Requer Python 3.11+; usa somente a biblioteca padrão. `rg` é uma conveniência para busca, não uma dependência da validação.

| Intenção | Comando | Quando |
| --- | --- | --- |
| Conferir documentação | `python3 scripts/check_docs.py` | Mudanças em Markdown, caminhos ou limites |
| Testar o validador | `python3 -m unittest discover -s tests -v` | Mudanças no script ou nos testes |
| Conferir espaços e conflitos no diff | `git diff --check` | Antes de concluir alterações |
| Ver alterações locais | `git status --short` | Antes de editar e antes de concluir |
| Listar documentos | `rg --files -g '*.md' -g '!node_modules' -g '!vendor'` | Quando faltar um caminho |

## O que a checagem cobre

[check_docs.py](../../scripts/check_docs.py) valida links locais inline literais, inclusive âncoras de títulos simples, cercas de código e limites de bytes. Imprime bytes e palavras de cada Markdown. O perfil aceito está em [convenções](../guides/markdown.md).

Não consulta URLs externas, não renderiza Mermaid, não testa descoberta dos agentes e não mede tokens. Confira visualmente diagramas alterados no preview do GitHub ou em um renderizador Mermaid compatível.

A [CI](../../.github/workflows/docs.yml) executa a checagem e os testes. Não existe comando de build, servidor ou teste de aplicação enquanto não houver produto. Ao adicionar uma stack, registre os comandos realmente executados e o diretório de execução nesta página.
