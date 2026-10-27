---
name: convencao-codigos-glpi
description: >-
  Convenção de códigos C/R/F/S/P. C e R só no cabeçalho; itens usam F#.S#.P#.
  Use ao escrever plano, anexo, sessão, comentário glpi: code= ou tarefa de chamado.
---

# Skill: convencao-codigos-glpi

Fonte única da convenção de códigos do kit. O espelho `glpi ticket-mirror`
grava no chamado pai só a tarefa em andamento ou futura, com o código curto.

## Regra normativa

- C = Chamado ITIL (Information Technology Infrastructure Library)
- R = Projeto/Requisição
- F = Fase, S = Sessão, P = Tarefa

1. C e R aparecem uma única vez, no cabeçalho do plano e dos demais documentos que pertençam a um chamado e a um projeto. Não inventar ids.
2. Títulos, itens de fase/sessão/tarefa, comentários `glpi: code=`, nomes de arquivos de anexos e prosa usam apenas o código relativo: `F#`, `F#.S#`, `F#.S#.P#`.
3. Formatos obrigatórios:
   - Sessão (tabela): `F1.S1 | Levantamento e decisoes | 15/10 | 8 h | [~] |`
   - Tarefa: `[ ] **F2.S1.P1** titulo da tarefa`
4. No GLPI, C e R são ligados por IDs (`tickets_id`, `projects_id`, vínculo `Itil_Project`), nunca por prefixo no texto.
5. A TicketTask recebe o code curto no texto visível. C e R vão somente via `tickets_id` e `Itil_Project`. É proibido fazer parse do título para extrair C ou R.
6. O "R" legado do `retro_scan` (`## R1`, `**R1**`, `P7.1`) não é o R de Projeto. Não reinterpretar. Não alargar o `CODE_RE` de `tree_validate.py` para cinco níveis: `F#.S#.P#` já cabe (no máximo dois pontos).

## Onde cada nível aparece

| Nível | Significado | Onde aparece | Onde não aparece |
|-------|-------------|--------------|------------------|
| C | Chamado ITIL | Cabeçalho, uma vez, com o id do Ticket | Título, item, `glpi: code=`, nome de arquivo |
| R | Projeto/Requisição | Cabeçalho, uma vez, com o id do Project | Título, item, `glpi: code=`, nome de arquivo |
| F | Fase | Seção, tabela, `code="F1"` | — |
| S | Sessão | `F1.S1` na tabela e no item | — |
| P | Tarefa | `F2.S1.P1` no item e no texto da TicketTask | — |

No GLPI, C e R existem como ids (`tickets_id`, `projects_id`, `Itil_Project`), não como texto do código.

## Nome do projeto raiz (R)

No preset PMF (`api-vscode-glpi`), o Project raiz leva o prefixo `GEP - ` na frente do nome do produto. O molde em `naming.root` é `GEP - {produto} - 0. [PAI]`. Subprojeto de fase não recebe esse prefixo. `glpi project create` sem `--parent-project` aplica `GEP - ` quando o nome ainda não começa assim.

## Estado e data de criação

Na criação de Project (raiz ou fase), gravar Estado e Data de criação. Sem `--state`, o estado é `gep1` (GEP 1. Produto Backlog). Sem `--date`, o campo `date` recebe o instante da criação (`YYYY-MM-DD HH:MM:SS`). Na ficha, "Data de criação" é `date`. "Última atualização" é `date_mod` e não ocupa o lugar de `date`.

Na criação de sessão ou tarefa (`ProjectTask`), gravar o mesmo Estado (`gep1` se não vier outro). A Data de criação da tarefa é `date_creation`. A ficha da tarefa não tem o campo `date` do projeto. Atualização de tarefa já existente não recoloca `gep1` nem reescreve `date_creation`.

## Cabeçalho único

Só em documento que pertença a um chamado e a um projeto já conhecidos. Modelo do piloto Bot_Pan:

```
> **Chamado ITIL (C):** 15817 (producao)
> **Projeto/Requisicao (R):** 12 - "GEP - Botao de Panico - 0. [PAI]"
> **Piloto:** Bot_Pan | **Data:** DD/MM/AAAA
```

Documento sem chamado definido não ganha essas linhas.

## Exemplos corretos

- Tabela: `F1.S1 | Levantamento e decisoes | 15/10 | 8 h | [~] |`
- Tarefa: `- [ ] **F2.S1.P1** codes.pattern e topology em model.defaults.yaml`
- Comentário: `<!-- glpi: code="F2.S1.P1" -->`
- Anexo: `docs/05_progresso/legados/anexos/F1_S1_levantamento_e_decisoes-15_10_26.md`

## Regex de validação

- Sessão: `^F\d+\.S\d+$`
- Tarefa: `^F\d+\.S\d+\.P\d+$`
- Proibido em itens, títulos e comentários: `\bC\d+\.R\d+`

## Exemplos INCORRETOS

Estes formatos não são usados. O validador ignora este bloco.

- Item: `- [ ] **C1.R1.F2.S1.P1** titulo`
- Tabela: `| C1.R1.F1.S1 | Levantamento |`
- Comentário: `<!-- glpi: code="C1.R1.F1.S1.P1" -->`
- Arquivo: `C1_R1_F1_S1_levantamento.md`

## Verificação

```bash
python .github/skills/convencao-codigos-glpi/scripts/checar_prefixo.py
```

Varre `docs/` e `.github/`, exceto `docs/05_progresso/legados/`. Exit 1 se achar o prefixo longo fora do cabeçalho, deste bloco INCORRETO, ou das decisões D2/D6 revogadas e D-novo do anexo.

## Aviso de parser

`retro_scan.py` trata `## R1` e `**R1**` como seção legada de plano antigo. Isso não é o R de Projeto. `tree_validate.py` (`CODE_RE`) aceita no máximo dois pontos (`F1.S1.P1`). Não alargar esse padrão para `C.R.F.S.P`.
