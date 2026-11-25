# Esquema de fontes e referências bibliográficas

Guia sob demanda para projetos acadêmicos (TCC, dissertação, tese, artigo científico ou relatório técnico). Em projetos não acadêmicos, remova este arquivo e [a regra de referências](../../.agents/rules/academic-references.md) na fase de faxina do bootstrap.

## Arquitetura em 3 camadas sob demanda

Carregar dezenas de resumos na mesma página desperdiça contexto. Separe metadados, rastreamento e leitura aprofundada:

| Camada | Caminho no produto | Papel | Quando abrir |
| --- | --- | --- | --- |
| 1. Metadados | `docs/references/references.bib` | Fonte única BibTeX para compilação e citação | Ao inserir, corrigir ou citar uma obra |
| 2. Matriz temática | `docs/references/README.md` | Mapa `Seção/Tema → @chave → Tipo → Status → Ficha` | Ao planejar ou revisar uma seção do texto |
| 3. Fichas seletivas | `docs/references/notes/<chave>.md` | Resumo técnico, método, métricas e citações exatas | Apenas para obras centrais do trabalho |

Modelos copiáveis: [índice e BibTeX](../../docs/templates/bibliography-index.md) e [ficha de obra](../../docs/templates/source-note.md).

## Hierarquia de fontes e status de leitura

Classifique cada entrada na matriz por **tipo de fonte** e **status de verificação**:

| Tipo de fonte | Peso argumentativo | Uso típico |
| --- | --- | --- |
| `Primária revisada por pares` | Mais alto | Artigos em periódicos e anais revisados, teses defendidas |
| `Normativa/técnica oficial` | Alto para especificações | Normas ABNT/ISO/IEEE, RFCs, datasheets, manuais oficiais |
| `Secundária/síntese` | Apoio contextual | Livros-texto, revisões sistemáticas, surveys (rastreie a primária quando citar dado crítico) |
| `Cinza/preliminar` | Restrito e sinalizado | Preprints (arXiv), relatórios internos, posts técnicos; nunca apresente como revisado por pares |

| Status | Significado | Pode sustentar afirmação central? |
| --- | --- | --- |
| `metadados` | Referência catalogada, texto ainda não lido | Não; apenas mapeamento inicial |
| `parcial` | Resumo/seções lidas, método ou tabelas pendentes | Apenas para escopo geral, com ressalva |
| `conferida` | Texto-fonte verificado contra a afirmação e página/seção | Sim |
| `descartada` | Mantida no histórico apenas para evitar retrabalho | Não |

## Regras anti-alucinação

1. **Zero invenção de memória:** nunca preencha DOI, ISBN, ISSN, volume, número, páginas, ano, autores ou resultado numérico sem conferir na fonte ou no arquivo `.bib` verificado.
2. **Marcador explícito de pendência:** quando faltar confirmação de metadado, página ou argumento, escreva `[A CONFERIR: @chave]` no rascunho. Remova o marcador somente após checagem real.
3. **Citação direta com localização exata:** toda transcrição literal exige página (`p. 42`) ou seção/tabela verificada no original.
4. **Separação epistemológica obrigatória:** deixe inequívoco no texto o que é:
   - **Literatura citada:** atribuída a `@chave` com escopo fiel ao autor;
   - **Dado empírico reproduzido:** obtido por experimento, script ou dataset versionado no repositório;
   - **Hipótese ou proposta autoral:** inferência, arquitetura ou síntese produzida pelo trabalho atual.

## Campos críticos no `.bib` por norma

Use um único `references.bib` em UTF-8 e delegue a formatação a **BibLaTeX** (`biblatex-abnt`, `ieee`, `apa`), **Pandoc** (`--citeproc` + arquivo CSL) ou **Quarto** (`bibliography:` + `csl:`).

| Campo BibTeX / BibLaTeX | ABNT (NBR 6023 / 10520) | IEEE | APA 7 |
| --- | --- | --- | --- |
| `author` / `editor` | Sobrenome e nome completos (evite truncar inicial) | Iniciais + sobrenome gerados pelo estilo | Sobrenome + iniciais; manter ordem exata |
| `title` / `subtitle` | Título e subtítulo separados; proteger siglas com `{Sigla}` | Proteger siglas e nomes próprios com `{...}` | *Sentence case* + proteger siglas com `{...}` |
| `year` / `date` | Obrigatório (`YYYY` ou `YYYY-MM-DD`) | Obrigatório (`year` + `month` em conferências) | Obrigatório (`YYYY`) |
| `journal` / `booktitle` | Nome completo do periódico ou evento | Nome/abreviação padrão do periódico/evento | Nome completo em *title case* |
| `volume`, `number`, `pages` | Obrigatórios em artigos; `pages` com intervalo real | Obrigatórios quando publicados | `volume` e `pages` obrigatórios; `number` se disponível |
| `publisher` e `address` (`location`) | **Críticos na ABNT** (cidade + editora) | Recomendados em livros/relatórios | `publisher` obrigatório; cidade dispensada na APA 7 |
| `doi` / `url` e `urldate` | `doi` preferencial; `url` + `urldate` (acesso em) para fontes online | `doi` preferencial em artigos/conferências | `doi` em formato `10.xxxx/...` sempre que existir |
| `version` (para `@software`) | Versão/commit e data de acesso | Versão/release e repositório | Versão e tipo (`[Computer software]`) |

## Fluxo mínimo de validação

- Confirme se toda `@chave` citada no manuscrito existe em `docs/references/references.bib`.
- Procure pendências abertas antes de entregar rascunhos finais: `rg -n 'A CONFERIR' docs/`.
- Mantenha a regra [`.agents/rules/academic-references.md`](../../.agents/rules/academic-references.md) ativa enquanto o projeto tiver bibliografia.
