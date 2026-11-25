# Perfil de reconhecimento: Fullstack (UI + API + Banco)

Use este perfil quando o produto precisa de interface web, regras de servidor e persistência no mesmo repositório desde a POC (SaaS inicial, portal interno, CRUD com fluxo de negócio).

## 1. Exemplo de primeiro prompt rico

> "Quero construir uma POC fullstack de gestão de reservas de salas com login simples por e-mail/senha, calendário semanal, criação/cancelamento de reserva sem conflito de horário e histórico. Prefiro monólito simples (Next.js + SQLite/Postgres ou FastAPI + React + SQLite) rodando com 1 comando local, migrações versionadas e testes de conflito de reserva em CI."

## 2. Perguntas de corte para a POC

1. **Modelo de código:** monólito fullstack em uma linguagem (ex.: Next.js/Remix/Django/Rails) ou separação leve `backend/` + `frontend/` no mesmo repo?
2. **Persistência na POC:** SQLite local (zero infra na POC) ou PostgreSQL (via Docker Compose) já necessário por recursos específicos (PostGIS, JSONB, concorrência)?
3. **Autenticação e papéis:** usuário único/sem login na POC, sessão simples com cookies ou multi-tenant com RBAC?
4. **Deploy alvo:** servidor único/Docker, PaaS gerenciado ou apenas demonstração local por enquanto?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Fullstack TypeScript | Next.js / SvelteKit / Remix + Prisma ou Drizzle + SQLite/Postgres | Microserviços, mensageria distribuída, GraphQL federation |
| Backend Python + UI leve | FastAPI + SQLite/SQLAlchemy (ou Django + HTMX/Templates) + Vite React se precisar de SPA rica | Kubernetes, Terraform multi-conta, Redis sem gargalo medido |
| Protótipo CRUD/admin ultrarrápido | Django (admin + templates/HTMX) ou Rails + SQLite | API + SPA separados quando server-rendered resolve em metade do código |

## 4. Arquitetura mínima e fronteiras

Mantenha 1 repositório, 1 processo principal (ou 2 bem delimitados) e 1 fonte de verdade para o schema:

```text
src/ (ou backend/ + frontend/)
  db/            # Schema, migrações versionadas e seed mínimo reproduzível
  domain/        # Regras de negócio puras (ex.: detecção de conflito, cálculos, permissões)
  api/           # Rotas/handlers finos com validação de entrada e códigos HTTP consistentes
  ui/            # Páginas e componentes consumindo contratos tipados da API
tests/
  unit/          # Regras de domínio sem rede
  integration/   # Fluxos HTTP + banco de teste isolado (SQLite em memória/tmp)
```

**Contrato obrigatório:** validação de entrada e regras de negócio ficam no servidor (`domain/` + `api/`), nunca apenas no cliente.

## 5. Armadilhas clássicas na POC

- **Começar com microserviços ou 4 containers obrigatórios:** o tempo inteiro vai para Docker/CORS/rede em vez de validar o fluxo de valor.
- **Migrações ad-hoc sem seed reproduzível:** impossível recriar o ambiente em sessão nova ou na CI.
- **Confiança cega na validação de frontend:** formulários validados só no browser deixam o banco corrompível via API.
- **Misturar segredos e configurações de ambiente:** sem `.env.example` e validação de config no boot, falhas aparecem tarde e com erro críptico.
- **Falta de isolamento entre testes:** testes compartilham o mesmo arquivo de banco e passam/falham dependendo da ordem.

## 6. Estratégia real de verificação e CI

- **Testes de domínio + integração HTTP/DB em CI:** subir migrações em banco limpo de teste, executar o fluxo principal (criar → consultar → atualizar → erro de validação/conflito) e validar status codes e persistência.
- **Build + typecheck + lint:** validar frontend e backend em comando único encadeado (`&&`).
- **Smoke test E2E no Antigravity:** subir servidor local em daemon de teste e usar `/browser` para exercitar o fluxo principal de ponta a ponta (UI → API → banco → reload confirmando persistência).

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- 1 comando documentado prepara banco/seed e sobe a aplicação localmente.
- O fluxo vertical completo (UI → API → banco → persistência após recarregar) funciona e tem testes automatizados cobrindo as regras críticas.
- `.env.example` e `docs/context/commands.md` permitem reprodução limpa em sessão nova.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova arquivos bibliográficos se não for projeto acadêmico.
- Mantenha `.env`, bancos locais (`*.db`, `*.sqlite`), `node_modules/`, `.venv/` e artefatos de build fora do Git e do contexto (`.gitignore` e `.geminiignore`).
