# Perfil de reconhecimento: Web Frontend

Use este perfil para aplicações web focadas em interface, visualização, ferramentas interativas no navegador, SPA/SSR leve ou protótipos consumindo APIs existentes. Se precisar criar API + banco junto, use [fullstack.md](fullstack.md) ou combine com [backend-api.md](backend-api.md).

## 1. Exemplo de primeiro prompt rico

> "Quero uma POC de painel web em React + Vite + TypeScript para acompanhar pedidos em tempo real a partir de uma API REST já existente (ou mockada em JSON local por enquanto). Precisa de listagem filtrável, detalhe em drawer lateral, estado vazio/erro bem tratado e responsividade desktop/mobile. Quero lint, typecheck e testes de fluxo principal rodando em CI."

## 2. Perguntas de corte para a POC

1. **Natureza da entrega:** ferramenta interativa SPA client-side, site estático/SEO (SSR/SSG) ou página única sem bundler?
2. **Fonte de dados na POC:** API real já acessível, fixture JSON/MSW local ou persistência apenas em `localStorage`/IndexedDB?
3. **Autenticação e permissões:** aberta na POC ou exige fluxo de login/sessão desde o dia 1?
4. **Alvo de visualização:** desktop-first, mobile-first ou ambos? Há requisitos fortes de acessibilidade ou design system pré-existente?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Ferramenta/widget simples | HTML + CSS + ES Modules (ou Vite vanilla TS) | Framework SSR pesado, monorepo, micro-frontends |
| SPA interativa moderna | Vite + React/Preact/Vue/Svelte + TypeScript + Tailwind ou CSS Modules | Redux/MobX complexo, GraphQL client pesado, Storybook antes de haver componentes estáveis |
| Conteúdo + SEO / SSR leve | Astro ou Next.js App Router enxuto | CMS headless pago + pipelines multi-ambiente na POC |
| Dados mockados na POC | Repositório/cliente tipado trocável + fixtures JSON (ou MSW) | BFF separado só para servir mock |

## 4. Arquitetura mínima e fronteiras

```text
src/
  api/           # Cliente HTTP + tipos de entrada/saída + adaptação de erro (e mock trocável)
  domain/        # Regras puras de formatação, filtro, cálculo e validação (sem DOM)
  components/    # Componentes reutilizáveis sem acoplamento direto a rotas
  features/      # Fluxos da POC (estado local + composição de componentes)
  styles/        # Tokens CSS (cores, tipografia, espaçamento)
tests/           # Testes unitários de domain/ + testes de fluxo de UI
```

**Contrato obrigatório:** concentre a fronteira com API/mock em `src/api/` com tipos explícitos para que trocar mock por backend real não espalhe alterações por componentes.

## 5. Armadilhas clássicas na POC

- **Lógica de negócio dentro de componentes visuais:** torna testes frágeis e obriga montar DOM para validar regras simples.
- **Esquecer estados de carregamento, vazio e erro:** a POC funciona com dados perfeitos e quebra em tela branca quando a API falha.
- **Dependências prematuras de UI/estado:** instalar 10 bibliotecas antes de ter 1 fluxo funcionando trava build e aumenta superfície de erro.
- **CSS ad-hoc inconsistente:** falta de variáveis CSS para cores/espaçamentos torna qualquer ajuste visual trabalhoso.
- **Ignorar bundle/build de produção:** código funciona no dev server (`vite dev`) mas falha em `tsc --noEmit` ou `vite build`.

## 6. Estratégia real de verificação e CI

- **Checagem estática obrigatória:** `typecheck` (ex.: `tsc --noEmit`), lint e build de produção (`npm run build`) em CI.
- **Testes automatizados:** testes unitários em `src/domain/` (Vitest/Node test runner) e ao menos 1 teste de componente/fluxo crítico (Testing Library ou Playwright headless quando justificar).
- **Verificação visual no Antigravity:** usar `/browser` (subagente de navegador) para validar renderização, responsividade, erros de console e chamadas de rede no fluxo principal; registrar limitações se rodou apenas com mock.

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- O fluxo principal de usuário funciona ponta a ponta no navegador, com estados de loading, vazio e erro tratados e zero erros de console.
- Build de produção, checagem de tipos e testes passam em um único comando documentado em `docs/context/commands.md`.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova os arquivos bibliográficos se não for projeto acadêmico.
- Garanta `node_modules/`, `dist/`, `.next/`, `coverage/` e lockfiles extensos coerentes em `.gitignore` / `.geminiignore`.
