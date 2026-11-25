# Catálogo de perfis de reconhecimento

Pasta temporária usada **apenas** nas Fases 1 e 2 do [bootstrap](../playbooks/bootstrap.md) via `/bootstrap-poc` (entrevista estilo `/grill-me`). **Toda esta pasta deve ser deletada na Fase 4 (faxina pós-reconhecimento)** assim que a POC estiver configurada.

## Regra de seleção e uso com grill-me

- Abra **apenas 1 perfil principal** compatível com o pedido do usuário (ou **no máximo 2** em projetos híbridos, como `academic` + `iot` ou `ai-data` + `backend-api`).
- Nunca leia todos os perfis por rotina e **nunca despeje todas as perguntas de corte de uma vez**: use-as como banco de decisões para conduzir uma entrevista estilo `/grill-me` (1 decisão por vez, com opção `(Recomendada)` e trade-off curto) que alimenta diretamente os Markdowns sob medida do projeto (`AGENTS.md`, `project.md`, `map.md`, `commands.md`, `.agents/rules/`).

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

## O que cada perfil fornece à entrevista

1. Exemplo de primeiro prompt rico para calibrar escopo rapidamente.
2. Perguntas de corte objetivas para a entrevista `/grill-me` (apenas decisões que alteram arquitetura, stack ou Markdowns).
3. Opções de stack enxuta para fundamentar a recomendação em cada pergunta (e o que evitar cedo).
4. Arquitetura mínima, fronteiras de pastas e contratos para gerar `docs/context/map.md`.
5. Armadilhas clássicas do domínio para virar guardrails concretos em `AGENTS.md` e `.agents/rules/`.
6. Estratégia real de verificação e CI (incluindo simulação/mock) para gerar `docs/context/commands.md`.
7. Critério de pronto da POC e checklist de faxina específica.
