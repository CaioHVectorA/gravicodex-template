# Perfil de reconhecimento: Mobile (Android / iOS)

Use este perfil para aplicativos móveis nativos ou multiplataforma (Flutter, React Native/Expo, Kotlin/Swift), especialmente quando envolvem navegação mobile, câmera/GPS/BLE, notificações ou operação offline-first.

## 1. Exemplo de primeiro prompt rico

> "Quero construir uma POC de app mobile em Flutter (ou React Native com Expo) para registro de vistorias em campo com formulário offline-first salvo em SQLite local, foto anexada e sincronização manual para uma API REST (mockada na POC). Preciso das regras de validação e fila de sincronização 100% isoladas de widgets para rodar testes automatizados em CI Linux sem emulador Android/iOS."

## 2. Perguntas de corte para a POC

1. **Plataformas alvo na POC:** Android apenas, iOS apenas ou ambos (cross-platform)? Há macOS/Xcode disponível se iOS for obrigatório agora?
2. **Recursos nativos reais:** precisa de câmera, GPS, Bluetooth/BLE, push notifications ou leitura NFC já na POC, ou começa com UI + estado local?
3. **Conectividade:** sempre online consumindo API ou precisa operar offline com fila de sincronização e resolução de conflito?
4. **Backend na POC:** consome API já existente, usa mock local na POC ou combina com [backend-api.md](backend-api.md)?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Cross-platform com ecossistema JS/TS | React Native + Expo (Managed workflow) + TypeScript + SQLite/AsyncStorage | Eject precoce (`prebuild` customizado complexo) sem necessidade de módulo nativo |
| Cross-platform UI consistente / alta fluidez | Flutter + Dart + testes de domínio/widget (`flutter test`) | Arquiteturas BLoC/Clean com 8 camadas para 3 telas |
| Nativo Android | Kotlin + Jetpack Compose + Room/DataStore | Módulos multi-feature complexos antes do primeiro fluxo |
| Nativo iOS | Swift + SwiftUI + SwiftData/SQLite | Dependências externas pesadas onde frameworks nativos bastam |

## 4. Arquitetura mínima e fronteiras

Desacople **domínio e sincronização (testáveis em host Linux)** de **telas e pontes de hardware/SO**:

```text
src/ (ou lib/)
  domain/        # Modelos, validação, fila offline e regras puras (0 dependência de plataforma)
  data/          # Repositório local (SQLite/storage) + cliente HTTP/mock atrás de interface
  platform/      # Adaptadores finos para câmera, GPS, permissões e sensores (mockáveis)
  screens/       # Telas e navegação fina consumindo estado/casos de uso
tests/           # Testes unitários de domain/ + testes de componentes/widgets sem emulador
```

**Contrato obrigatório:** toda permissão de sistema (câmera, localização, Bluetooth) tem tratamento explícito para os 3 estados (`concedida`, `negada`, `negada permanentemente`).

## 5. Armadilhas clássicas na POC

- **Acoplar regra de negócio a ciclos de vida de tela ou módulos nativos:** impede rodar testes rápidos na CI sem subir emulador lento.
- **Ignorar estado offline e rede instável:** timeouts longos, falta de retry/fila local e perda de preenchimento quando o app vai para background.
- **Assumir que simulador equivale a aparelho físico:** câmera, BLE, GPS real, bateria e permissões precisam de teste explícito em dispositivo real (registrado como limitação se não executado).
- **Configurar pipelines de loja (Play Store/App Store/Fastlane) antes do fluxo principal:** desperdiça tempo na POC.
- **Segredos de API embutidos no bundle do app:** qualquer chave no cliente mobile pode ser extraída do APK/IPA; deixe isso explícito na arquitetura.

## 6. Estratégia real de verificação e CI

- **CI headless (obrigatória):** lint, checagem de tipos/análise estática (`tsc --noEmit` / `dart analyze`) e testes unitários/widget de `domain/`, `data/` (fila offline + mock de API) e telas críticas sem depender de emulador pesado.
- **Build de sanidade:** validar compilação/bundle de debug quando o runner suportar; se iOS exigir macOS não disponível na CI, documentar explicitamente a limitação.
- **Checklist em dispositivo/emulador:** registrar em `docs/context/commands.md` o comando local (`npx expo start` / `flutter run`) e o roteiro de validação manual (modo avião → criar registro → reconectar → sincronizar).

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- O fluxo principal executa em emulador ou aparelho (ou web preview equivalente quando aplicável), com estados de erro, carregamento e permissões tratados.
- Toda a lógica de domínio e persistência/sincronização passa em testes automatizados em CI com comandos registrados em `docs/context/commands.md`.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) e remova arquivos bibliográficos se não for projeto acadêmico.
- Garanta artefatos móveis pesados (`android/.gradle/`, `ios/Pods/`, `build/`, `.dart_tool/`, `.expo/`, `*.apk`, `*.ipa`) em `.gitignore` e `.geminiignore`.
