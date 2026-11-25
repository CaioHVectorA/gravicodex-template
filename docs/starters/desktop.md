# Perfil de reconhecimento: Aplicações Desktop

Use este perfil para softwares locais com interface gráfica em Windows, Linux ou macOS (ferramentas técnicas, editores locais, painéis offline, utilitários com acesso a sistema de arquivos ou periféricos).

## 1. Exemplo de primeiro prompt rico

> "Quero criar uma POC de aplicativo desktop em Python + PySide6 (ou Tauri se fizer mais sentido) para importar planilhas CSV de laboratório, validar colunas obrigatórias, plotar um gráfico comparativo e exportar um relatório PDF/CSV local. Precisa rodar offline no Windows e Linux, sem travar a interface durante arquivos de 50 MB, com toda a lógica de validação testada em headless na CI."

## 2. Perguntas de corte para a POC

1. **Sistemas operacionais alvo:** Windows apenas, Linux, macOS ou multiplataforma desde a POC?
2. **Distribuição e peso aceitável:** script/venv local para uso interno, binário leve (Tauri/Go/Rust) ou empacotamento completo (PyInstaller/Electron)?
3. **Acesso a sistema local:** precisa de arquivos grandes, banco SQLite local, porta serial/USB, tray icon ou atalhos globais?
4. **Carga de trabalho:** há operações lentas (I/O pesado, OCR, processamento de mídia) que exigem worker thread/processo separado da UI?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Ecossistema Python / dados / engenharia | Python 3.11+ + PySide6 (Qt) ou CustomTkinter/Tkinter + `sqlite3` | Auto-updater assinado, instaladores MSI/DMG notarizados na POC |
| UI web moderna + binário leve | Tauri (Rust backend + frontend enxuto) | Electron com dezenas de dependências nativas sem necessidade |
| App web já existente precisando de desktop | Electron enxuto com `contextIsolation: true` | Expor `nodeIntegration: true` no renderer |
| Ferramenta interna ultrarrápida | TUI (`textual` em Python ou `bubbletea` em Go) se GUI não for obrigatória | Construir GUI completa quando uma TUI resolve melhor |

## 4. Arquitetura mínima e fronteiras

Isole a UI (janelas, widgets, eventos) do núcleo da aplicação para permitir testes sem servidor gráfico:

```text
app/
  core/          # Casos de uso, validação, leitura/escrita, SQLite (0 imports de GUI)
  workers/       # Execução assíncrona / threads / fila de progresso e cancelamento
  ui/            # Janelas, views, dialogs e bindings finos para core/
  main.*         # Bootstrap da aplicação e injeção de dependências
tests/           # Testes headless completos de core/ e workers/
```

**Contrato obrigatório:** `app/core/` nunca importa toolkit gráfico (`PySide6`, `tkinter`, `electron`). Toda operação > 100 ms roda fora da thread principal da UI emitindo progresso/erro estruturado.

## 5. Armadilhas clássicas na POC

- **Bloquear a thread da UI:** ler arquivos grandes ou rodar subprocessos na thread principal congela a janela e dá sensação de crash.
- **Caminhos hardcoded de sistema operacional:** concatenar barras `\`/`/` em vez de usar `pathlib.Path` ou diretórios padrão de usuário (`platformdirs` / `dirs`).
- **Salvar configuração/banco dentro da pasta do executável:** falha em instalações com permissão somente leitura.
- **Misturar estado de tela com persistência:** perder dados ao fechar a janela inesperadamente por falta de gravação atômica ou SQLite em modo WAL.
- **Testabilidade zero em CI Linux headless:** importar GUI no topo dos módulos impede rodar testes unitários no GitHub Actions.

## 6. Estratégia real de verificação e CI

- **CI headless (obrigatória):** rodar suíte unitária e de integração em `app/core/` e `app/workers/` com arquivos de fixture reais (incluindo arquivos corrompidos/vazios) e validar ausência de imports de GUI no núcleo.
- **Smoke test de UI (quando suportado):** no Linux CI, usar `QT_QPA_PLATFORM=offscreen` (Qt) ou `xvfb-run` para instanciar a janela principal sem erro de boot.
- **Checklist manual por SO:** registrar em `docs/context/commands.md` os passos de smoke test visual no SO alvo (abrir arquivo, cancelar operação longa, fechar e reabrir preservando estado).

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- O usuário executa o fluxo principal na interface local sem congelamento e com feedback claro de progresso/erro.
- Toda a lógica de negócio passa em CI headless com comandos registrados em `docs/context/commands.md`.
- Há instrução clara de como rodar localmente (e, se aplicável, empacotar um build de teste).

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova arquivos bibliográficos se não for projeto acadêmico.
- Adicione artefatos de empacotamento (`dist/`, `build/`, `*.spec`, `target/`, `release/`) em `.gitignore` e `.geminiignore`.
