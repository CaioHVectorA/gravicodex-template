# 0001 — Contexto sob demanda com entrada compartilhada

## Estado

Aceita em 2026-11-03 para a base GraviCodex. A economia quantitativa ainda não foi medida.

## Problema

Instruções longas repetidas em cada sessão e documentação sem rota de descoberta aumentam o material a recuperar. Separar regras por ferramenta também cria risco de divergência entre Codex e Antigravity.

## Decisão

Manter `AGENTS.md` curto na raiz como acordo comum; usar um índice orientado à tarefa e documentos especializados acessados quando necessários. Guardar estado de trabalho separado das regras duráveis. Usar links e Mermaid para navegação e relações, sem presumir importação ou execução do conteúdo.

As [fontes oficiais](../research/sources.md) documentam suporte a `AGENTS.md` nos dois produtos e recomendam instruções práticas no Codex. Os limites em bytes e a organização desta base são escolhas locais, descritas em [eficiência](../guides/efficiency.md).

## Alternativas e consequências

| Alternativa | Consequência |
| --- | --- |
| Manual único sempre carregado | Menos navegação, mas inclui detalhes irrelevantes em tarefas pequenas |
| Regras completas duplicadas por agente | Permite customização imediata, mas exige sincronizar o mesmo contrato |
| Muitos arquivos com fragmentos mínimos | Reduz cada leitura, mas aumenta chamadas e dificulta seguir o raciocínio |
| Entrada curta e rotas por necessidade | Exige um índice mantido e recuperação explícita; favorece compartilhar o contrato |

Risco assumido: o agente pode não abrir um documento necessário. Mitigação: rotas por intenção, critérios observáveis de conclusão e validação dos links. O índice não substitui investigação dos consumidores reais.

## Reconsiderar

Revisar se uma mudança de versão eliminar a entrada comum, se as buscas frequentemente falharem ou se medições mostrarem que navegação e retrabalho superam o benefício. Comparar tarefas equivalentes com correção e tokens medidos, não apenas tamanho de arquivos.
