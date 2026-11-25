# GraviCodex Template

Base de engenharia **Antigravity-first** em Markdown + Python stdlib, focada no **Google Antigravity** (App/Desktop 2.0, CLI `agy` e Antigravity IDE), mantendo o **Codex em *stand-by*** via `AGENTS.md`. A proposta combina contexto sob demanda, customizações nativas enxutas em `.agents/` e onboarding descartável para POCs, com zero dependências externas obrigatórias.

## Começar

1. Use este repositório como base de um novo projeto ou POC.
2. Abra a raiz no Google Antigravity. O arquivo [AGENTS.md](AGENTS.md) define o acordo de trabalho e o hook `SessionStart` em [.agents/hooks.json](.agents/hooks.json) injeta um snapshot compacto inicial (desligável em 1 linha com `"enabled": false`).
3. No primeiro prompt de criação/POC, o agente aciona `/bootstrap-poc` ([playbook](docs/playbooks/bootstrap.md) + [catálogo de perfis](docs/starters/README.md)) e, ao final, executa a faxina removendo o material de template.
4. Valide localmente com Python 3.11+:

```sh
python3 scripts/check_docs.py && python3 -m unittest discover -s tests -v && git diff --check
```

Não há stack de aplicação, plugin externo ou pacote de IA obrigatório. Os comandos acima validam esta base documental e suas customizações nativas; não substituem testes do produto que vier a ser criado.

## Arquitetura de contexto no Antigravity

```mermaid
flowchart LR
    H["SessionStart hook (<=1,5 KB)"] --> A["AGENTS.md (<=3 KiB)"]
    A --> R[".agents/rules (glob / model_decision)"]
    A --> S[".agents/skills (/bootstrap-poc, /audit-docs, /session-handoff)"]
    A --> I["docs/INDEX.md: localizar o que falta"]
    I --> D["Contexto, guias, perfis ou referências"]
    A --> SA[".agents/agents/doc-auditor (flash, read-only)"]
```

Links Markdown comuns apontam caminhos sem importar seu conteúdo automaticamente. O carregamento seletivo combina recursos nativos do Antigravity (`.agents/`) com navegação explícita pelo índice.

## O que vem pronto

| Recurso | Utilidade |
| --- | --- |
| [Índice de rotas](docs/INDEX.md) | Escolher o documento certo pela informação que falta |
| [Guia do Antigravity](docs/guides/antigravity.md) | Hierarquia nativa (`.agents/`), comandos `/`, plugins opcionais e nota de Codex em stand-by |
| [Perfis de POC descartáveis](docs/starters/README.md) | 10 perfis ricos de reconhecimento removidos na faxina do bootstrap |
| [Referências acadêmicas](docs/guides/references.md) | Bibliografia em 3 camadas anti-alucinação (ABNT, IEEE, APA 7) |
| [Mapa de dependências](docs/context/map.md) | Fronteiras reais da base e análise de impacto |
| [Guia de eficiência](docs/guides/efficiency.md) | Busca paralela, higiene de comandos e medição via `bench_transcript.py` |
| [Fontes e limites](docs/research/sources.md) | Separação entre documentação oficial, referências e escolhas locais |

## Limites da proposta

Bytes e palavras são indicadores locais de manutenção, não contagem de tokens. O validador protege links, limites e contratos `.agents/`; para medir impacto real em sessões do Antigravity, compare logs equivalentes com [bench_transcript.py](scripts/bench_transcript.py) antes de afirmar ganhos.

Para contribuir, veja [CONTRIBUTING.md](CONTRIBUTING.md).
