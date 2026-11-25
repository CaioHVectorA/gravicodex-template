# Modelo de índice bibliográfico e `references.bib`

Copie as duas seções abaixo ao iniciar um projeto acadêmico: crie `docs/references/README.md` (matriz temática) e `docs/references/references.bib` (fonte única de metadados). Consulte [o guia de referências](../guides/references.md) para regras anti-alucinação e normas ABNT/IEEE/APA 7.

## Esqueleto de `docs/references/README.md`

```markdown
# Referências do projeto

Fonte única de metadados: `docs/references/references.bib`.
Fichas aprofundadas ficam em `docs/references/notes/<chave>.md` (criadas apenas para obras centrais).

## Matriz temática

| Seção / Tema | Chave | Tipo de fonte | Status | Ficha |
| --- | --- | --- | --- | --- |
| Fundamentação teórica | `@silva2024exemplo` | Primária revisada por pares | conferida | `notes/silva2024exemplo.md` |
| Arquitetura / protocolo | `@ieee2023padrao` | Normativa/técnica oficial | parcial | — |
| Benchmark / ferramenta | `@ferramenta2025` | Normativa/técnica oficial | metadados | — |

## Pendências abertas

- Conferir páginas exatas de `[A CONFERIR: @ieee2023padrao]` antes da revisão final.
```

## Esqueleto comentado de `docs/references/references.bib`

Substitua as entradas ilustrativas por obras realmente verificadas. Nunca mantenha exemplos fictícios no projeto final.

```bibtex
% Convenção de chave: primeiroautorANOpalavrachave (minúsculas, sem acento)
% Proteja siglas com chaves {ABNT}, {MQTT}, {LLM} para preservar maiúsculas.

@article{silva2024exemplo,
  author  = {Silva, Maria Clara and Souza, João Pedro},
  title   = {Título completo do artigo com sigla {IoT}},
  journal = {Nome Completo do Periódico},
  year    = {2024},
  volume  = {12},
  number  = {3},
  pages   = {45--62},
  doi     = {10.0000/substituir-por-doi-verificado},
  note    = {Status: metadados — substituir antes de citar}
}

@inproceedings{pereira2025conferencia,
  author    = {Pereira, Lucas},
  title     = {Título do trabalho publicado em anais},
  booktitle = {Proceedings of the International Conference on Example Systems},
  year      = {2025},
  month     = {oct},
  pages     = {101--110},
  publisher = {IEEE},
  address   = {São Paulo},
  doi       = {10.0000/substituir-por-doi-verificado}
}

@book{autor2022livro,
  author    = {Autor, Ana Beatriz},
  title     = {Título do livro},
  subtitle  = {Subtítulo opcional para {ABNT}},
  edition   = {2},
  publisher = {Nome da Editora},
  address   = {Campinas},
  year      = {2022},
  isbn      = {978-0-00-000000-0}
}

@techreport{org2023norma,
  author      = {{Associação Brasileira de Normas Técnicas}},
  title       = {{NBR 6023}: Informação e documentação — Referências — Elaboração},
  institution = {ABNT},
  address     = {Rio de Janeiro},
  year        = {2018},
  number      = {NBR 6023}
}

@software{ferramenta2025,
  author  = {Mantenedor, Nome},
  title   = {Nome do Software ou Biblioteca},
  version = {1.0.0},
  year    = {2025},
  url     = {https://example.invalid/repo},
  urldate = {2026-11-25}
}
```
