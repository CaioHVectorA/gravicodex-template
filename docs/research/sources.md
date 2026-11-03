# Fundamentação e limites

Páginas oficiais consultadas em **2026-11-03**. As descrições abaixo resumem o que foi conferido; escolhas locais não são apresentadas como garantias dos fornecedores.

| Fonte | Informação conferida | Aplicação nesta base |
| --- | --- | --- |
| [OpenAI — Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md) | Descoberta de instruções, precedência de override e limite padrão de 32 KiB | Entrada raiz e cuidado com escopo; veja [agentes](../guides/agents.md) |
| [OpenAI — Best practices](https://developers.openai.com/codex/learn/best-practices) | Contexto pertinente, critérios de conclusão, instruções curtas e referências para guias específicos | Rotas por tarefa e validação explícita |
| [Google Antigravity — Rules](https://antigravity.google/docs/rules) | `AGENTS.md`, regras cumulativas, escopo de descoberta, frontmatter e gatilhos | Entrada compartilhada; sem configuração duplicada obrigatória |
| [GitHub — Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) | Diagramas Mermaid em blocos de código cercados | Grafos em texto versionáveis e renderizáveis no GitHub |

## O que não foi demonstrado

- Não há benchmark neste template provando redução de tokens, custo ou tempo.
- Bytes e palavras não equivalem à tokenização de nenhum modelo específico.
- Links Markdown não garantem que o agente abrirá o destino.
- Diagramas e títulos organizam recuperação, mas não criam memória automática.
- A compatibilidade foi baseada na documentação consultada, sem execução interativa dos dois produtos neste ambiente.

## Revisar uma afirmação

Reabra a fonte quando mudar a integração ou a versão do agente. Atualize a orientação afetada e esta data somente após nova consulta. Para testar o efeito sobre consumo, siga [o protocolo de medição](../guides/efficiency.md#medir-antes-de-afirmar-ganho).
