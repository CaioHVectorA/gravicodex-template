# Eficiência de contexto e turnos

Objetivo: minimizar turnos e contexto irrelevante sem omitir contratos, repetir investigações ou aceitar regressões.

## Recuperar em paralelo por necessidade

1. Extraia da tarefa: resultado esperado, restrições e evidência de conclusão.
2. Aproveite o snapshot de abertura (`SessionStart`) e fatos já confirmados na sessão.
3. Se faltar informação, abra a rota exata no [índice](../INDEX.md) (ou mencione `@arquivo` diretamente).
4. **Localize antes → leia em paralelo no mesmo turno:** use `find_by_name`, `grep_search` ou `rg` para achar arquivos/linhas e dispare leituras independentes juntas no mesmo turno.
5. Em arquivos longos, leia fatias de 150–200 linhas centradas no símbolo; leia o arquivo inteiro se tiver ≤ 300 linhas.
6. **Higiene de comandos:** prefira ferramentas de leitura/busca em vez de pipelines shell elaborados; para verificações pesadas (lint, testes, build), agrupe comandos independentes em uma execução (`&&`) e resuma falhas com comando, código de saída e trecho diagnóstico.
7. Para varreduras amplas de documentação, delegue ao subagente somente leitura [doc-auditor](../../.agents/agents/doc-auditor.md). Entre marcos longos, use `/compact`; transforme correções recorrentes em regra/skill com `/learn`.

Evite despejar lockfiles, dependências, artefatos gerados, binários ou logs completos no chat (mantenha [.geminiignore](../../.geminiignore) atualizado).

## Densidade sem linguagem cifrada

- Escreva regras concretas: condição → ação → evidência.
- Deixe uma única fonte para cada fato e aponte para ela.
- Registre o motivo de escolhas duráveis em `docs/decisions/`; não replique explicações nas entradas.
- Use tabelas para comparar e Mermaid para relações; prefira prosa curta para sequências simples.
- Não use siglas inventadas ou formatos artificiais por suposta economia de tokens, nem esconda instruções em comentários HTML/`<details>` (continuam no arquivo).

## Orçamento local em bytes

O validador protege limites em UTF-8:

| Escopo | Limite | Papel |
| --- | --- | --- |
| `AGENTS.md` | 3 KiB (3.072 B) | Entrada sempre carregada |
| `docs/INDEX.md` | 4 KiB (4.096 B) | Mapa opcional de rotas |
| Demais Markdown permanentes | 8 KiB (8.192 B) | Guias, contexto, playbooks, ADRs, modelos |
| `docs/starters/*.md` | 16 KiB (16.384 B) | Perfis ricos temporários (deletados na faxina) |
| `.agents/rules/*.md` | 24.000 B | Teto oficial de truncamento do Antigravity |
| Snapshot `SessionStart` | 1.500 B | Injeção única de cold-start via `session_snapshot.py` |

Bytes e palavras são indicadores de manutenção, não contagem de tokens. Limites documentais nunca autorizam cortar uma investigação técnica necessária.

## Medir antes de afirmar ganho

Compare tarefas equivalentes com mesmo modelo, versão e configuração. Use [bench_transcript.py](../../scripts/bench_transcript.py) offline sobre arquivos `transcript.jsonl` do Antigravity:

```sh
python3 scripts/bench_transcript.py --before baseline.jsonl --after otimizado.jsonl
```

O script sumariza turnos, chamadas de ferramenta, distribuição por ferramenta e tokens (entrada, saída, cache e total) quando presentes no log — marcando explicitamente **não medidos** quando ausentes. Registre também duração, retrabalho e aceitação final do resultado. Não anuncie economia percentual sem experimento reproduzível.

## Retomar sem repetir

Quando uma tarefa cruzar sessões, use `/session-handoff` ([modelo](../templates/task.md)) preservando objetivo, SHA/branch, diff relevante, evidências reais e próximo passo. Confirme `git status --short` antes de confiar no registro.
