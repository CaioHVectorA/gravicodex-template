# Perfil de reconhecimento: CLI e Bibliotecas Reutilizáveis

Use este perfil para ferramentas de linha de comando (CLIs), SDKs, pacotes Python/Node/Go/Rust ou bibliotecas internas com foco em API pública estável, previsibilidade e baixo atrito de instalação.

## 1. Exemplo de primeiro prompt rico

> "Quero construir uma POC de CLI + biblioteca Python (zero dependências externas ou apenas stdlib) que valida arquivos CSV contra um schema JSON declarativo, imprime relatório legível para humanos ou `--json` para pipelines CI e devolve exit codes semânticos (`0` ok, `1` violação de dados, `2` erro de uso). Quero testes unitários e testes de subprocesso da CLI rodando em CI."

## 2. Perguntas de corte para a POC

1. **Forma principal de consumo:** CLI interativa/scriptável, biblioteca importável por código ou ambos (núcleo de lib + camada fina de CLI)?
2. **Linguagem e distribuição alvo:** Python (`pyproject.toml`), Node/TypeScript (`package.json`), Go (binário único) ou Rust (`Cargo.toml`)?
3. **Ergonomia de saída e composição:** precisa funcionar em pipes (`stdin`/`stdout`), saída `--json` estruturada e códigos de saída semânticos?
4. **Política de dependências:** zero dependências externas (stdlib) ou biblioteca específica de parsing/TUI?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| CLI/Lib Python enxuta | Python 3.11+ + `pyproject.toml` + `argparse` (ou `click`/`typer` se muitos subcomandos) + `unittest`/`pytest` | Plugins dinâmicos complexos, publicação automatizada no PyPI antes de estabilizar API |
| Binário único sem runtime | Go (`flag`/`cobra`) ou Rust (`clap`) | Cross-compilation de 10 alvos e Homebrew tap antes de validar o comando principal |
| CLI/Lib TypeScript | Node 22 + TypeScript + `node:util` (`parseArgs`) + `node:test` ou Vitest | Bundlers complexos com múltiplos formatos CJS/UMD/ESM sem necessidade |

## 4. Arquitetura mínima e fronteiras

Mantenha a lógica desacoplada de `sys.argv`, `stdin`/`stdout` e `sys.exit`:

```text
src/<pacote>/
  __init__.py    # Superfície pública mínima e explícita (__all__)
  core.py        # Funções/classes puras e tipadas (sem print nem exit)
  errors.py      # Hierarquia curta de exceções de domínio
  cli.py         # Parsing de argumentos, I/O (stdin/stdout/stderr) e mapeamento para exit codes
tests/
  test_core.py   # Testes diretos da API pública e casos de borda
  test_cli.py    # Testes de integração da CLI (stdout, stderr, --help, --json, exit codes)
```

**Contrato obrigatório:**
- Dados/resultado vão para `stdout`; diagnósticos, avisos e erros vão para `stderr`.
- `--help` claro e exemplos reais funcionais; modo `--json` quando a CLI for consumida por scripts ou agentes.

## 5. Armadilhas clássicas na POC

- **Misturar `print()` e `sys.exit()` na lógica principal:** torna a biblioteca inutilizável por outros módulos e dificulta testes.
- **Imprimir logs ou banners no `stdout`:** quebra pipelines Unix (`cmd | jq`) e parsers JSON.
- **Códigos de saída inconsistentes:** retornar `0` em falha parcial ou `1` para erro de sintaxe confunde automações e CI.
- **API pública inchada na v0:** exportar helpers internos cria dívida de compatibilidade desde o primeiro consumidor.
- **Tratar mal encoding, caminhos com espaço ou `stdin` vazio:** falhas clássicas em ambiente real de usuário.

## 6. Estratégia real de verificação e CI

- **Testes de unidade na API pública:** validar entradas válidas, bordas (vazio, Unicode, caminhos relativos/espaços) e exceções tipadas.
- **Testes de CLI ponta a ponta:** invocar a CLI via função `main(argv)` e ao menos 1 teste de subprocesso verificando `--help`, `--json`, separação `stdout`/`stderr` e códigos de saída.
- **Teste de empacotamento/instalação:** em CI, instalar em modo editável ou buildar o pacote/binário para confirmar que o entrypoint declarado realmente existe e executa.

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- O comando principal (`--help` + caso principal + caso de erro) funciona via entrypoint instalado e respeita a separação `stdout`/`stderr` e exit codes.
- A API pública mínima está documentada no `README.md` com exemplos executáveis e 100% testada em CI.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova arquivos bibliográficos se não for projeto acadêmico.
- Mantenha artefatos de build/empacotamento (`dist/`, `build/`, `*.egg-info/`, `target/`, `node_modules/`) em `.gitignore` e `.geminiignore`.
