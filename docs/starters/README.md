# Catálogo de perfis de reconhecimento (`docs/starters/`)

Pasta temporária usada **apenas** na Fase 1 do [bootstrap](../playbooks/bootstrap.md) via `/bootstrap-poc`. **Toda esta pasta deve ser deletada na Fase 4 (faxina pós-reconhecimento)** assim que a POC estiver configurada.

## Regra de seleção

- Abra **apenas 1 perfil principal** compatível com o pedido do usuário.
- Se o projeto cruzar dois domínios (por exemplo, TCC com telemetria embarcada ou agente IA exposto via API), combine **no máximo 2 perfis** (ex.: `academic` + `iot`, `ai-data` + `backend-api`).
- Nunca leia todos os perfis por rotina.

## Matriz de escolha rápida

| Perfil | Quando escolher | Combinações comuns |
| --- | --- | --- |
| [iot.md](iot.md) | Firmware (ESP32/STM32/RP2040), sensores, MQTT/BLE/Serial, edge gateway | `iot` + `academic`, `iot` + `backend-api` |
| [web.md](web.md) | Frontend SPA/SSR, landing interativa, dashboard ou ferramenta browser-first | `web` + `backend-api` |
| [desktop.md](desktop.md) | App local Windows/Linux/macOS (Tauri, Electron, PySide6/Qt, Tkinter) | `desktop` + `automation` |
| [automation.md](automation.md) | Bots, pipelines agendados, ETL leve, scraping ético, integrações entre APIs | `automation` + `ai-data` |
| [fullstack.md](fullstack.md) | Produto web completo com UI + API + banco de dados no mesmo repositório | `fullstack` + `ai-data` |
| [academic.md](academic.md) | TCC, dissertação, tese, artigo científico, benchmark reprodutível com bibliografia | `academic` + `iot`, `academic` + `ai-data` |
| [backend-api.md](backend-api.md) | API REST/GraphQL/gRPC, webhooks, workers assíncronos e persistência | `backend-api` + `web`, `backend-api` + `mobile` |
| [cli-lib.md](cli-lib.md) | Ferramenta de linha de comando, SDK ou biblioteca reutilizável distribuível | `cli-lib` + `automation` |
| [ai-data.md](ai-data.md) | RAG, agentes LLM, pipelines de dados, notebooks reprodutíveis, avaliação de modelos | `ai-data` + `backend-api`, `ai-data` + `academic` |
| [mobile.md](mobile.md) | App Android/iOS (Flutter, React Native/Expo, Kotlin/Swift) com ou sem offline-first | `mobile` + `backend-api` |

## O que cada perfil entrega

1. Exemplo de primeiro prompt rico para o usuário calibrar o escopo.
2. Perguntas de corte objetivas que realmente mudam stack ou arquitetura.
3. Opções de stack enxuta para POC e lista explícita do que evitar cedo.
4. Arquitetura mínima, fronteiras de pastas e contratos.
5. Armadilhas clássicas do domínio na fase de prova de conceito.
6. Estratégia real de verificação e CI (incluindo simulação/mock quando faltar hardware ou serviço externo).
7. Critério de pronto da POC e checklist de faxina específica.
