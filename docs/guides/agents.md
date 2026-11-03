# Codex e Antigravity

Comportamento consultado em 2026-11-03; detalhes e versões podem mudar. [Fontes oficiais](../research/sources.md).

## Entrada compartilhada

Os dois produtos documentam suporte a `AGENTS.md`. Por isso esta base usa um único arquivo na raiz e links Markdown comuns para documentos opcionais. Não exige `GEMINI.md`, regras duplicadas ou configuração global.

Abra a raiz do repositório como workspace/diretório de trabalho para a entrada comum. Na primeira execução, peça ao agente para informar quais instruções encontrou e o comando de validação aplicável. Isso é uma verificação prática de instalação; a checagem local de Markdown não a realiza.

## Diferenças que importam

| Aspecto | Codex | Antigravity |
| --- | --- | --- |
| Descoberta de projeto | Da raiz até o diretório de trabalho | Workspace/diretório de início e ancestrais até a raiz |
| Entrada | `AGENTS.override.md` precede `AGENTS.md` no mesmo diretório | Documenta `AGENTS.md` ou `GEMINI.md`; mantenha só uma entrada compartilhada |
| Regras abaixo da pasta aberta | Não presuma descoberta ao editar; confira instruções no caminho | Não carrega automaticamente regras de subpastas abaixo do workspace |
| Limite documentado | `project_doc_max_bytes`: 32 KiB por padrão para a cadeia de projeto | Ativação e orçamento dependem do tipo de regra; confira a versão |

Antes de editar uma subpasta com instruções próprias, leia explicitamente seus arquivos aplicáveis. Uma política importante não deve depender de um comportamento de descoberta que apenas um dos agentes oferece.

## Extensões opcionais

Só adicione regras especializadas quando houver domínio e repetição que justifiquem sua manutenção. No Antigravity atual, `.agents/rules/*.md` exige frontmatter com `trigger` válido. Exemplo ilustrativo, não instalado nesta base:

```yaml
---
trigger: model_decision
description: "Consultar ao alterar o contrato de persistência do projeto."
---
```

`model_decision` expõe descrição e caminho para seleção sob demanda; `always_on` injeta o corpo. Não replique o acordo raiz dentro dessas regras. Codex não passa a reconhecer tais gatilhos só porque os arquivos existem: mantenha o guia canônico acessível pelo índice comum.

No Antigravity, a sintaxe especial `@[rótulo](caminho)` inclui conteúdo na regra; um link Markdown comum não faz isso. Evite inclusões do acervo completo na entrada: elas eliminam a recuperação seletiva.

## Troca de ferramenta

Use o mesmo registro de tarefa, confirme arquivos alterados e repita somente verificações invalidadas por mudanças ou ambiente. Estado da conversa e resultados de comandos não são automaticamente compartilhados entre produtos.
