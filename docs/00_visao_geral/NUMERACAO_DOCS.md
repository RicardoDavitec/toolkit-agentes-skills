# Numeração docs — decisão de remapeamento

## Problema
Árvore de produto (figura): `00_visao_geral`, `01_requisitos`, …  
Kit anterior no samu-operacional: `docs/00-GLPI`  
→ conflito de identidade numérica no `00`.

## Decisão
| Antes (samu) | Kit fonte (`pmf-dev-kit`) |
|--------------|---------------------------|
| `docs/00-GLPI` | `docs/06_glpi` |
| (gap na figura entre 05 e 07) | ocupado por GLPI |
| `docs/05-gestao-projeto` | `docs/05_progresso` |
| `docs/01-arquitetura` | `docs/02_arquitetura` |
| `docs/03-compilacao` | `docs/03_implementacao/compilacao` |

Convenção de nome: `NN_snake_case` (underscores, sem acentos no path).

## Árvore canônica (12 pastas)

`00_visao_geral` `01_requisitos` `02_arquitetura` `03_implementacao`
`04_operacao` `05_progresso` `06_glpi` `07_doc_academica` `08_imagens`
`09_dados_e_tabelas` `10_setup` `11_ia`

O índice usa underscore (`00_visao_geral`). Hífen (`00-visao_geral`) e
variação de maiúsculas não são canônicos: o conteúdo migra para a pasta
com underscore e a pasta antiga sai.

| Pasta antiga | Destino |
|--------------|---------|
| `00-visao_geral` | `00_visao_geral` |
| `01-requisitos`, `01_requisito` | `01_requisitos` |
| `02-arquitetura` | `02_arquitetura` |
| `03-compilacao` | `03_implementacao/compilacao` |
| `07-guias-rapidos` | `04_operacao/guias_rapidos` |
| `08-imagens` | `08_imagens` |
| `09-dados_e_tabelas` | `09_dados_e_tabelas` |
| `10-setup` | `10_setup` |
| `ia` | `11_ia` |
| `06_progresso/` | `05_progresso/historico` |
