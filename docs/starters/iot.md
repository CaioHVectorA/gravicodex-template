# Perfil de reconhecimento: IoT e Sistemas Embarcados

Use este perfil para projetos com microcontroladores (ESP32, RP2040, STM32), sensores/atuadores, comunicação serial/BLE/MQTT/LoRa ou gateways Linux embarcados (Raspberry Pi).

## 1. Exemplo de primeiro prompt rico

> "Quero construir uma POC de monitoramento de temperatura e vibração em motores usando ESP32 + sensor DHT22/MPU6050 publicando via MQTT a cada 5s para um coletor local em Python + SQLite. Não tenho a placa conectada nesta máquina agora, então quero a lógica de leitura/enquadramento separada do HAL de hardware, um simulador de telemetria MQTT local e testes unitários do parser e da máquina de estados rodando em CI."

## 2. Perguntas de corte para a POC

Pergunte apenas o que não veio no prompt e muda o código:

1. **Alvo de hardware real:** qual MCU/placa (ESP32, RP2040, STM32, Linux embarcado) e há placa física disponível para flash agora ou a POC começa em simulação/host?
2. **Protocolo e topologia:** comunicação direta Serial/USB, Wi-Fi (MQTT/HTTP), BLE ou LoRaWAN? Precisa operar offline com buffer local?
3. **Orçamento de energia e tempo real:** alimentado por tomada ou bateria (*deep sleep*)? Há restrição rígida de latência/taxa de amostragem (Hz)?
4. **Destino dos dados:** basta log local/CSV/SQLite + CLI na POC ou exige dashboard web/broker remoto?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Firmware C/C++ com testes no host | PlatformIO (`native` + target board) ou ESP-IDF + Unity/doctest | RTOS customizado complexo, OTA com assinatura criptográfica completa |
| Protótipo rápido em MCU | MicroPython/CircuitPython + módulos puros testáveis em CPython | Frameworks proprietários pesados ou nuvens IoT gerenciadas antes de validar payload |
| Gateway / coletor local | Python 3.11+ (`paho-mqtt` ou `pyserial` + `sqlite3` stdlib) ou Go | Kafka, Kubernetes, InfluxDB clusterizado, microserviços |
| Simulação sem placa física | Simulador em Python/C++ gerando frames sintéticos + broker Mosquitto local ou fake em memória | Gêmeo digital 3D ou hardware-in-the-loop complexo |

## 4. Arquitetura mínima e fronteiras

Separe estritamente **lógica pura (testável no host)** de **drivers/HAL (dependentes da placa)**:

```text
firmware/
  core/          # Parser de payload, máquina de estados, filtros, CRC (0 dependências de hardware)
  hal/           # Interfaces finas (read_sensor, publish, sleep) + implementação da placa
  main.*         # Wiring de boot e loop principal
gateway/         # (Opcional) Ingestão MQTT/Serial -> validação de schema -> SQLite/CSV
sim/             # Emulador de dispositivo/sensor para testar ponta a ponta sem bancada
tests/           # Testes nativos de core/ + testes de contrato do protocolo
```

**Contrato obrigatório:** defina um único schema de mensagem (JSON versionado ou struct binária com tamanho, endianness e CRC explícitos) em `docs/context/map.md` ou arquivo dedicado de protocolo.

## 5. Armadilhas clássicas na POC

- **Acoplar regra de negócio a `Arduino.h` / SDK da placa:** impede rodar testes unitários em CI sem hardware.
- **Ignorar desconexão e reconexão:** Wi-Fi/MQTT cai; sem backoff exponencial e watchdog, o nó trava silenciosamente após horas.
- **Payload sem timestamp, `device_id` nem `schema_version`:** quebra o coletor na primeira evolução de campo.
- **Unidades implícitas e calibração mágica:** misturar °C/m°C ou raw ADC sem documentar fator de conversão.
- **Segredos hardcoded no firmware:** credenciais Wi-Fi/MQTT commitadas em `config.h` em vez de `secrets.example.h` ignorado no `.gitignore`.

## 6. Estratégia real de verificação e CI

- **Camada `core/` (CI obrigatória):** compilar e testar no host (ex.: `pio test -e native`, `pytest` ou `ctest`) cobrindo parsers, bordas de sensor (NaN, desconexão, saturação), CRC e transições de estado.
- **Integração sem placa:** subir simulador `sim/` enviando payloads válidos e corrompidos contra o coletor/parser e verificar persistência e contagem de descartes.
- **Bancada física (quando houver placa):** registrar checklist manual reproduzível em `docs/context/commands.md` (porta serial, baud rate, comando de flash, critério visual/log esperado) e separar claramente o que rodou em CI do que foi validado em bancada.

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- A lógica `core/` passa 100% em testes automatizados no host.
- O fluxo ponta a ponta (simulado ou em placa real) recebe, valida e persiste telemetria com recuperação básica de falha.
- `docs/context/commands.md` documenta comandos reais de build/teste/simulação e pinagem/protocolo mínimos.

**Limpeza pós-reconhecimento:**
- Execute a matriz da [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) (deletar `docs/starters/`, `docs/playbooks/bootstrap.md`, `.agents/skills/bootstrap-poc/`).
- Se não for TCC/artigo, remova também os arquivos bibliográficos (`docs/guides/references.md`, `.agents/rules/academic-references.md`, modelos em `docs/templates/`).
- Adicione artefatos de build embarcado (`.pio/`, `build/`, `*.elf`, `*.bin`) em `.gitignore` e `.geminiignore`.
