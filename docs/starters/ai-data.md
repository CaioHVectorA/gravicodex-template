# Perfil de reconhecimento: IA, Agentes LLM e Pipelines de Dados

Use este perfil para aplicações de IA aplicada (RAG, extração estruturada, agentes com ferramentas, avaliação de prompts/modelos) ou pipelines analíticos/ML reprodutíveis. Combine com [backend-api.md](backend-api.md) para exposição HTTP ou [academic.md](academic.md) para pesquisa com bibliografia.

## 1. Exemplo de primeiro prompt rico

> "Quero construir uma POC em Python de RAG local sobre manuais técnicos em Markdown/PDF: chunking determinístico, busca híbrida leve (BM25/SQLite FTS5 + embeddings opcionais) e geração de resposta citando exatamente o arquivo e seção de origem. Quero um conjunto de avaliação offline de 20 perguntas com gabarito e testes em CI usando um cliente LLM mockado para não gastar API nem depender de rede."

## 2. Perguntas de corte para a POC

1. **Tipo de problema:** extração estruturada, busca/RAG sobre corpus próprio, agente com chamadas de ferramenta ou pipeline tabular/ML clássico?
2. **Modelo e orçamento de inferência:** API externa (Gemini/OpenAI/Anthropic), modelo local ou abordagem híbrida? Qual o limite de custo/latência na POC?
3. **Critério objetivo de qualidade:** quais 10–30 casos reais (*eval set*) definem se a POC acerta ou falha (precisão de extração, citação fiel, recall@k, F1)?
4. **Privacidade e dados:** os dados podem sair da máquina para API externa ou exigem anonimização/execução 100% local?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| RAG / busca sobre documentos | Python 3.11+ + SQLite FTS5 (BM25) + embeddings em SQLite/NumPy + SDK oficial do provedor | Bancos vetoriais clusterizados (Pinecone/Weaviate/Milvus) e frameworks com 5 camadas de abstração antes de provar recall |
| Extração / agentes com ferramentas | SDK oficial do modelo + schema tipado (Pydantic/JSON Schema) + loop explícito de ferramentas | Orquestradores pesados que escondem prompts, tokens e erros reais |
| Dados / ML clássico | Python + `polars`/`pandas` ou `duckdb` + `scikit-learn` + scripts com `--seed` | Spark/Databricks/Kubeflow para dados que cabem em RAM |
| Avaliação (evals) | JSONL versionado com entradas + critérios determinísticos + script de score em Python | Julgamento puramente subjetivo ("parece bom no chat") |

## 4. Arquitetura mínima e fronteiras

Isole **ingestão/dados**, **interface do modelo (substituível por mock)** e **avaliação reproduzível**:

```text
src/
  ingest/        # Leitura, limpeza, chunking determinístico e metadados de origem
  retrieval/     # Índice e ranking (BM25/vetorial) devolvendo trechos + fonte exata
  llm/           # Adaptador fino de modelo (protocolo/interface + implementação real + fake/mock)
  pipeline.py    # Orquestração, prompts versionados em arquivos/constantes e validação de saída
evals/
  dataset.jsonl  # Casos de teste curados (entrada, fontes esperadas, critérios objetivos)
  run_eval.py    # Executor offline/online que mede acerto, latência e tokens (ou marca não medidos)
tests/           # Testes determinísticos sem rede usando llm fake
```

**Contrato obrigatório:** toda resposta baseada em documentos carrega rastreabilidade da fonte (arquivo/chunk); saídas estruturadas passam por validação de schema antes de seguir adiante.

## 5. Armadilhas clássicas na POC

- **Desenvolver sem `evals/` desde o dia 1:** mexer em prompt ou chunking sem bateria de avaliação vira regressão invisível ("melhorou 1 caso, quebrou 5").
- **Acoplar tudo a um framework opaco:** dificulta inspecionar exatamente qual prompt, contexto e custo de tokens foram enviados ao modelo.
- **Testes de CI chamando API paga:** gera custo imprevisível, flakiness por rede/rate limit e quebra sem chave secreta.
- **Confundir demonstração bonita com fidelidade:** o modelo responde fluentemente mesmo quando o retrieval trouxe o trecho errado (alucinação).
- **Versionar datasets brutos, checkpoints ou pesos no Git:** explode tamanho do repositório e do contexto do agente.

## 6. Estratégia real de verificação e CI

- **CI determinística e gratuita (obrigatória):** testes unitários de ingestão/chunking/retrieval (recall em fixtures pequenos), validação de schema de saída e fluxo ponta a ponta usando adaptador `FakeLLM`.
- **Avaliação controlada (sob demanda):** rodar `evals/run_eval.py` contra modelo real em amostras fixas, registrando versão de prompt, modelo, taxa de acerto, falhas de schema e tokens informados pela API (sem inventar métricas ausentes).

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- O pipeline executa ponta a ponta com rastreabilidade de fonte/schema e tem interface de modelo mockável testada em CI.
- Existe um conjunto mínimo de `evals/` reproduzível documentado em `docs/context/commands.md` com baseline registrado.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova arquivos bibliográficos se não for projeto acadêmico.
- Garanta `.env`, chaves de API, dados brutos (`data/raw/`), índices gerados e pesos (`*.bin`, `*.pt`, `*.onnx`, `*.parquet`, `*.sqlite`) em `.gitignore` e `.geminiignore`.
