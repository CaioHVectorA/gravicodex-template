# Perfil de reconhecimento: Projetos Acadêmicos e Pesquisa Reprodutível

Use este perfil para TCC, monografia, dissertação, tese, artigo científico, revisão sistemática ou benchmark experimental com bibliografia formal. Combine com um segundo perfil técnico (`iot.md`, `ai-data.md`, `cli-lib.md`, etc.) quando o trabalho incluir protótipo ou experimentos computacionais.

## 1. Exemplo de primeiro prompt rico

> "Quero estruturar meu TCC em Engenharia sobre detecção de anomalias em séries temporais de sensores industriais com norma ABNT (NBR 6023/10520) em Quarto/LaTeX. Preciso da base bibliográfica em 3 camadas (`references.bib`, matriz temática e fichas sob demanda), pipeline reproduzível em Python para gerar tabelas e gráficos a partir de dados sintéticos/públicos com seed fixa, e validação automatizada de citações e resultados sem nenhuma referência inventada."

## 2. Perguntas de corte para a POC

1. **Tipo de documento e norma:** TCC, dissertação, tese, artigo ou relatório? Qual norma de citação (**ABNT NBR 6023/10520**, **IEEE** ou **APA 7**) e formato de saída (LaTeX/BibLaTeX, Quarto, Pandoc/Markdown)?
2. **Pergunta de pesquisa e hipótese:** qual problema central, métrica de avaliação e baseline de comparação?
3. **Natureza da evidência:** revisão bibliográfica, experimento computacional/benchmark, estudo de caso ou protótipo de hardware/software?
4. **Fontes e dados já disponíveis:** o usuário já possui PDFs/`.bib`/datasets locais ou começará catalogando metadados reais com `[A CONFERIR: @chave]`?

## 3. Opções de stack enxuta para POC

| Cenário | Stack enxuta recomendada | Evitar cedo na POC |
| --- | --- | --- |
| Manuscrito + código + gráficos integrados | Quarto (`quarto render`) ou Pandoc (`--citeproc` + CSL ABNT/IEEE/APA) | Editar manualmente referências no Word ou copiar números de gráficos na mão |
| Modelo institucional LaTeX (abnTeX2 / IEEEtran) | LaTeX + `biblatex` (`biber`) com `Makefile` ou `latexmk` | Pacotes LaTeX exóticos que quebram compilação em outra máquina |
| Experimentos e gráficos reprodutíveis | Python 3.11+ (`venv`/lock leve, scripts com `--seed`, saída CSV/JSON + SVG/PNG) | Notebooks executados fora de ordem sem script reprodutível |
| Gestão de bibliografia | `docs/references/references.bib` + `README.md` + `notes/<chave>.md` ([guia](../guides/references.md)) | Colar dezenas de resumos gigantes num único arquivo |

## 4. Arquitetura mínima e fronteiras

Separe claramente **bibliografia**, **experimentos/dados** e **manuscrito**:

```text
docs/
  references/
    references.bib  # Fonte única de metadados BibTeX (verificada)
    README.md       # Matriz Seção/Tema -> @chave -> Tipo -> Status -> Ficha
    notes/          # Fichas individuais apenas para obras centrais
experiments/        # Scripts parametrizados com seed fixa e logs reproduzíveis
data/
  processed/        # Amostras pequenas versionáveis (dados brutos pesados no .gitignore/.geminiignore)
manuscript/         # Capítulos/seções em .tex, .qmd ou .md + estilo CSL/classe
results/            # Tabelas e figuras geradas por script (reproduzíveis)
```

**Contrato obrigatório:** siga integralmente [o guia de referências](../guides/references.md) e mantenha [`.agents/rules/academic-references.md`](../../.agents/rules/academic-references.md) ativa. Separe sempre literatura citada, dado empírico reproduzido e hipótese autoral.

## 5. Armadilhas clássicas na POC

- **Alucinação bibliográfica:** inventar DOI, páginas, autores ou conclusões de memória destrói a credibilidade do trabalho. Use `[A CONFERIR: @chave]` sempre que não leu o texto-fonte.
- **Números hardcoded no texto:** alterar um experimento e esquecer de atualizar tabelas/parágrafos cria contradição interna.
- **Experimentos não determinísticos:** esquecer de fixar seeds (`random`, `numpy`, splits) impede reproduzir a própria tabela na defesa.
- **Misturar fonte primária com blog/preprint sem sinalizar:** sempre classifique tipo de fonte e status de leitura na matriz.
- **Commitar PDFs pesados e datasets brutos de GB:** incha o repositório Git e polui o contexto do agente.

## 6. Estratégia real de verificação e CI

- **Integridade bibliográfica:** script/checagem garantindo que toda `@chave` citada no manuscrito existe em `docs/references/references.bib`, que o `.bib` parseia sem erros e que não restam marcadores `[A CONFERIR:` em versões de entrega (`rg -n 'A CONFERIR' docs/ manuscript/`).
- **Reprodutibilidade experimental:** comando em CI que roda um experimento reduzido (*smoke benchmark* com dataset mínimo e seed fixa) verificando que métricas e figuras são geradas sem erro.
- **Compilação do manuscrito:** quando houver LaTeX/Quarto/Pandoc no ambiente, registrar o comando exato de build em `docs/context/commands.md` e validar a geração sem citações indefinidas (`??`).

## 7. Critério de pronto e limpeza específica

**POC pronta quando:**
- `docs/references/references.bib` e `docs/references/README.md` estão inicializados a partir de [bibliography-index.md](../templates/bibliography-index.md) e [source-note.md](../templates/source-note.md) com fontes reais (ou pendências marcadas).
- O esqueleto do manuscrito compila e resolve citações reais sem chaves quebradas.
- Se houver experimento, 1 execução mínima reprodutível gera saída verificada por script.

**Limpeza pós-reconhecimento:**
- Execute a [Fase 4 do bootstrap](../playbooks/bootstrap.md#fase-4-faxina-pós-reconhecimento) deletando `docs/starters/`, `docs/playbooks/bootstrap.md` e `.agents/skills/bootstrap-poc/`.
- **MANTENHA** os ativos acadêmicos: `docs/guides/references.md`, `.agents/rules/academic-references.md`, `docs/templates/bibliography-index.md` e `docs/templates/source-note.md`.
- Adicione PDFs de referência (`papers/*.pdf`), dados brutos (`data/raw/`) e auxiliares de compilação LaTeX (`*.aux`, `*.bbl`, `*.blg`, `*.log`, `*.out`, `*.toc`) em `.gitignore` e `.geminiignore`.
