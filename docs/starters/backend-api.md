# Perfil de reconhecimento: Backend e APIs

Use este perfil para serviços HTTP/REST, webhooks, GraphQL/gRPC, workers assíncronos ou backends headless que serão consumidos por web, mobile, integrações externas ou CLIs.

## 1. Exemplo de primeiro prompt rico

> "Quero construir uma POC de API REST em FastAPI + SQLite (com SQLAlchemy/migrações prontas para migrar para Postgres depois) para gestão de chamados técnicos: cadastro, atribuição, transição de status com regras de máquina de estados e webhook de saída. Preciso de validação estrita de payload, `/healthz`, OpenAPI consistente e testes de integração HTTP rodando em CI sem containers externos."

## 2. Perguntas de corte para a POC

1. **Estilo de interface e clientes:** REST JSON (OpenAPI), GraphQL ou gRPC? Quem consome a API (browser com CORS, app mobile, webhook servidor-servidor)?
2. **Persistência e consistência:** SQLite na POC ou PostgreSQL obrigatório desde o início? Há transações críticas ou filas assíncronas?
3. **Autenticação e autorização:** API key simples, JWT/OAuth2, HMAC de webhook ou aberta localmente na POC?
4. **Restrições operacionais:** alvo de runtime (Python, Go, Node/TypeScript, Rust), requisitos de latência/concorrência ou integração externa obrigatória?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Backend Python rápido e tipado | FastAPI + Pydantic v2 + SQLite/SQLAlchemy (ou `sqlite3`) + `pytest` | Microserviços, Kafka, service mesh, API Gateway separado |
| Backend Go enxuto e performático | `net/http` (Go 1.22+ router) ou `chi` + `database/sql` (SQLite/Postgres) | Frameworks pesados com geração mágica excessiva |
| Backend TypeScript | Fastify ou Hono + Zod + Drizzle/Prisma + SQLite/Postgres | NestJS com dezenas de camadas abstratas para 3 endpoints |
| Jobs assíncronos na POC | Tabela de jobs no banco ou worker simples no mesmo repo | Broker distribuído (RabbitMQ/Kafka) sem carga comprovada |

## 4. Arquitetura mínima e fronteiras

Mantenha rotas finas e regras de domínio testáveis sem subir servidor HTTP:

```text
src/
  api/           # Rotas/handlers HTTP, parsing de request, mapeamento de erro (RFC 7807 / JSON)
  schemas/       # Contratos de entrada/saída (Pydantic/Zod/structs)
  domain/        # Regras de negócio, máquinas de estado, políticas (sem HTTP nem SQL direto)
  storage/       # Repositórios, conexão, migrações e queries parametrizadas
  config.py      # Leitura e validação de env vars no boot (falha rápida se faltar config)
tests/
  unit/          # Regras de domain/
  integration/   # Requests reais contra app de teste + banco temporário isolado
```

**Contrato obrigatório:** toda resposta de erro segue formato único e previsível (status HTTP correto + código de erro + mensagem segura sem stack trace em produção).

## 5. Armadilhas clássicas na POC

- **Regra de negócio espalhada nos handlers HTTP:** impede reaproveitamento em workers/CLI e dificulta testar bordas.
- **SQL montado por concatenação de string:** abre SQL injection mesmo em POCs internas; use sempre queries parametrizadas.
- **Falta de idempotência em POST/webhooks:** reenvios de rede duplicam entidades ou cobranças.
- **Endpoints sem paginação nem limites de payload:** um `GET /items` sem `limit` derruba memória assim que a base cresce.
- **Configuração implícita e segredos no código:** falta de `.env.example` e de validação de variáveis no startup.

## 6. Estratégia real de verificação e CI

- **Testes de contrato e integração HTTP (CI obrigatória):** testar cada endpoint crítico com banco temporário limpo cobrindo caminho feliz, payload inválido (`400`/`422`), recurso ausente (`404`), conflito/transição inválida (`409`) e autenticação (`401`/`403` quando aplicável).
- **Integrações externas mockadas:** clientes HTTP externos recebem interface injetável ou servidor fake local nos testes; nunca depender de rede externa na CI.
- **Smoke test de boot:** verificar `/healthz` e exportação de schema OpenAPI válido quando aplicável.

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- Os endpoints centrais atendem ao contrato de entrada/saída com erros padronizados e persistência real testada em isolamento.
- 1 comando sobe a API localmente e 1 comando executa lint + testes unitários + testes de integração em CI.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova arquivos bibliográficos se não for projeto acadêmico.
- Garanta `.env`, bancos locais (`*.sqlite`, `*.db`), caches e dependências em `.gitignore` e `.geminiignore`.
