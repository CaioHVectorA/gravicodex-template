# Perfil de reconhecimento: Automação, ETL Leve e Integrações

Use este perfil para scripts agendados, pipelines de coleta/transformação, bots operacionais, sincronização entre APIs/planilhas/bancos ou automações de tarefas repetitivas.

## 1. Exemplo de primeiro prompt rico

> "Quero construir uma POC de automação em Python que consulta diariamente uma API de notas fiscais, normaliza os registros, evita duplicatas usando um banco SQLite de checkpoints e gera um resumo CSV + alerta webhook em caso de erro. Precisa ter modo `--dry-run`, retries com backoff e testes rodando totalmente offline com respostas HTTP gravadas."

## 2. Perguntas de corte para a POC

1. **Gatilho e frequência:** execução sob demanda (CLI), agendada (cron / GitHub Actions / systemd timer) ou orientada a evento/webhook?
2. **Idempotência e estado:** o que acontece se a automação rodar duas vezes no mesmo dia? Precisa de checkpoint local (SQLite/JSON) ou chave de idempotência no destino?
3. **Efeitos colaterais externos:** escreve em banco, envia e-mails/mensagens, modifica arquivos ou faz cobranças? (Define a obrigatoriedade de `--dry-run` e limites de taxa.)
4. **Autenticação e segredos:** API key, OAuth2, service account ou cookies? Onde os segredos viverão em execução?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Integração HTTP / planilhas / arquivos | Python 3.11+ (`httpx` ou `urllib`, `sqlite3`, `csv`/`json`, `argparse`) | Airflow, Prefect, Dagster ou Celery antes de haver múltiplas DAGs reais |
| Automação de navegador (sem API oficial) | Playwright com seletores resilientes e rate limit explícito | Selenium legado frágil ou contorno de CAPTCHA/anti-bot |
| Automação leve de CLI/shell/DevOps | Python stdlib ou Go (binário único) | Bash > 150 linhas com parsing frágil de JSON/texto |
| Agendamento na POC | `cron`, `systemd timer` ou GitHub Actions `schedule` | Orquestrador distribuído com banco próprio |

## 4. Arquitetura mínima e fronteiras

Separe **extração (I/O externo)**, **transformação (pura)** e **carga/efeito colateral (idempotente)**:

```text
src/
  connectors/    # Clientes HTTP/API/arquivos com timeout, retry e interface mockável
  transform/     # Parsing, normalização, deduplicação e validação de schema (100% puro)
  state/         # Checkpoint/cursor de execução (SQLite ou JSON atômico)
  runner.py      # Orquestração com --dry-run, resumo final estruturado e códigos de saída
tests/
  fixtures/      # Payloads reais anonimizados para testes offline
```

**Contrato obrigatório:** toda execução imprime resumo objetivo (`lidos`, `processados`, `ignorados`, `falhas`, `dry_run=true/false`) e retorna código de saída `0` apenas em sucesso ou erro explicitamente tolerado.

## 5. Armadilhas clássicas na POC

- **Execução não idempotente:** reexecutar após falha parcial duplica registros, mensagens ou cobranças.
- **Chamadas sem `timeout` nem `retry` limitado:** uma API lenta trava o job indefinidamente ou entra em loop infinito de retentativas.
- **Vazar segredos em logs ou código:** imprimir headers `Authorization` ou commitar `.env` em vez de `.env.example`.
- **Falha silenciosa:** capturar `except Exception: pass` e retornar exit code `0` mascara quebras de schema na fonte.
- **Acoplar testes a APIs reais:** CI falha por rate limit, rede ou mudança de dados externos.

## 6. Estratégia real de verificação e CI

- **Testes offline em CI (obrigatório):** validar `transform/` com fixtures válidos, bordas (campos nulos, formatos de data, encoding) e payloads malformados; testar `runner.py` com conectores fake verificando idempotência (rodar 2x produz o mesmo estado final) e `--dry-run` (zero escritas externas).
- **Smoke test controlado:** documentar em `docs/context/commands.md` o comando seguro de execução em modo `--dry-run` contra ambiente real/homologação.

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- O pipeline executa ponta a ponta em `--dry-run` e em modo real controlado, com idempotência verificada e `.env.example` documentando todas as variáveis necessárias.
- Testes automatizados offline cobrem transformação, erro de API e reexecução sem duplicatas.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova arquivos bibliográficos se não for projeto acadêmico.
- Garanta `.env`, checkpoints locais (`*.sqlite`, `state/`), logs e dumps brutos em `.gitignore` e `.geminiignore`.
