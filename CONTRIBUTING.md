# Contribuir

Localize a rota no [índice](docs/INDEX.md). Mantenha cada fato em um lugar e use links nas demais páginas. Uma orientação nova deve resolver uma dúvida ou falha recorrente; texto genérico também custa contexto.

Para alterar Markdown, use [as convenções](docs/guides/markdown.md). Para mudar o comportamento do template, siga [o procedimento de mudança](docs/playbooks/change.md).

Antes de enviar:

```sh
python3 scripts/check_docs.py
git diff --check
```

Se mudar o validador, execute os testes descritos em [comandos](docs/context/commands.md). Descreva o problema resolvido e a validação realizada; só registre decisão arquitetural se houver uma escolha durável com alternativas relevantes.
