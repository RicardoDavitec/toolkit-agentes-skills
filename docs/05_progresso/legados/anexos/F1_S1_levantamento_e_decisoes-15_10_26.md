# F1.S1 — Levantamento e decisoes (15/10/2026)

> **Chamado ITIL (C):** 15817 (producao)
> **Projeto/Requisicao (R):** 12 - "GEP - Botao de Panico - 0. [PAI]"
> **Piloto:** Bot_Pan | **Data:** 15/10/2026

> Plano (legado): [`espelhamento_chamado_itil_crfsp-15_10_26-13_45.md`](../espelhamento_chamado_itil_crfsp-15_10_26-13_45.md)
> Arquivado em 27/10/2026 com o plano. Chamado ITIL do template em producao: 16531.

## 1. Evidencia lida no GLPI de producao (15/10, 11:42–11:55)

Leitura por API REST (`suporte.franca.sp.gov.br`, perfil `Technician`), so GET.

| Objeto | Achado |
|--------|--------|
| Ticket 15817 | "Botão do Pânico - Implementação.", tipo 2 (requisicao), status 3, categoria ITIL 155, `actiontime` 167400 s |
| `Itil_Project` 74 | liga Ticket 15817 ao Project 12 |
| Project 12 | "GEP - Botão de Pânico - 0. [PAI]", code `GEP_BP2026`, plano 15/01–20/02/2026, **0 ProjectTask**, 0 subprojetos |
| TicketTask do 15817 | 12 tarefas manuais de teste (ids 2413–2458), sem code F/S/P, categoria e modelo 0, tecnico `ricardodavid`, grupo 3 `Desenvolvimento` |
| `ProjectTask_Ticket` | vazio |
| `TaskTemplate`, `TaskCategory`, `ITILCategory` | **403** para o perfil Technician |

As 12 tarefas de teste ficam fora do espelho: o script ignora tarefa sem
marcador de code. O usuario as substitui por tarefas reais.

## 2. Campos da tarefa de chamado (tela → API)

| Tela | `TicketTask` | Origem no plano |
|------|--------------|-----------------|
| Criacao / criador | `date_creation` / `users_id` | GLPI (so leitura) |
| Ultima atualizacao / editor | `date_mod` / `users_id_editor` | GLPI (deteccao de conflito) |
| Descricao | `content` | titulo + criterio do P + marcador de code |
| Arquivos | `Document` + `Document_Item` (itemtype `TicketTask`) | atributo `anexo` do P |
| Modelo | `tasktemplates_id` | atributo `modelo` do P ou padrao da fase |
| Data | `date` | data do espelhamento |
| Categoria | `taskcategories_id` | atributo `categoria` do P ou padrao do R |
| Status Informacao / A fazer / Feito | `state` 0 / 1 / 2 | marcador do P |
| Privado | `is_private` | `mirror.private` (padrao 0) |
| Base de conhecimento | campo do formulario — nome na API a confirmar (F2.S3.P3) | padrao falso |
| Duracao `##h##` | `actiontime` (s) | `hours` do P (padrao 2 h) |
| Usuario / Grupo | `users_id_tech` / `groups_id_tech` | `mirror.user` / `mirror.group_id` |
| Data inicial / Periodo | `begin` / `end` | `plan_start` / `plan_end` do P |

| Botao | API | Uso pelo script |
|-------|-----|-----------------|
| Salvar | `POST` / `PUT /TicketTask` | upsert idempotente |
| Desfazer planejamento | `PUT` com `begin`/`end` vazios (aceite pela API a confirmar) | P que perdeu a janela |
| Excluir permanentemente | `DELETE /TicketTask/{id}?force_purge=1` | **nunca** automatico |

## 3. Decisoes propostas

- **D1 — Hierarquia C/R/F/S/P.** C = chamado ITIL de origem (`Ticket`).
  R = projeto/requisicao (`Project`, ligado ao C por `Itil_Project`).
  F/S/P seguem como hoje. Um C pode ter varios R.
- **D2 — REVOGADA em 16/10/2026.** O code longo `C1.R1.F2.S1.P1` deixa de
  valer em itens, titulos, comentarios `glpi: code=` e nomes de arquivo.
  Os ids GLPI continuam em `.glpi/project.yaml`, por ambiente
  (o chamado de homologacao tem outro id):

  ```yaml
  chamados:
    C1: { prod: 15817, homolog: null }
  requisicoes:
    R1: { chamado: C1, prod: 12, homolog: 12 }
  ```

- **D-novo:** C e R somente no cabecalho. Codes e itens usam F#.S#.P#.
  Vinculo com C e R no GLPI por IDs (tickets_id, projects_id, Itil_Project).
  A TicketTask leva o code curto no texto visivel. Sem parse de titulo.
- **D3 — Origem obrigatoria.** Todo R precisa de um C. Regra nova no
  validate e pergunta obrigatoria no `bootstrap-into.sh`.
- **D4 — Escopo do espelho.** So P em andamento (`[~]`, `[t]`) ou futuros
  (`[ ]` com `plan_start` >= agora). Concluidos e o historico ficam de fora.
  Um P ja espelhado que fecha (`[x]`/`[A]`) vira "Feito".
- **D5 — Sentido unico.** Plano → TicketTask. Se a tarefa foi editada no GLPI
  depois do ultimo espelho (`users_id_editor` diferente do usuario da API ou
  `date_mod` maior que o registrado), o script nao sobrescreve e relata.
- **D6 — REVOGADA em 16/10/2026.** O prefixo longo `[C1.R1.F2.S1.P3]` nao e
  mais usado no `content` nem no comentario. A identidade da TicketTask e o
  code curto `F2.S1.P3` no texto visivel, mais o indice `.glpi/index.json`.
- **D7 — Sem exclusao.** P removido do plano vira "Informacao" (0) com
  `[cancelado]`. Excluir permanentemente fica so na tela.
- **D8 — Homologacao primeiro.** Chamado novo em `suporte-homolog`, ligado
  ao projeto do Bot_Pan na homologacao. Producao (15817) so depois do aceite.
- **D9 — Catalogo editavel.** Um arquivo YAML com modelos, categorias e
  status. YAML aceita comentario e e facil de estender; o kit ja depende de
  PyYAML (`glpi-weekly-sheet.py`). O loader tambem aceita `.json` com o
  mesmo schema. O preset traz o catalogo; o produto sobrescreve em
  `.glpi/catalogos/tarefa_chamado.yaml`.
- **D10 — Elegibilidade por fase.** O validate recusa modelo fora das fases
  listadas. GEP 7 vai em F5 (na PMF, "Producao"); `fases` e editavel.

## 4. Rascunho do catalogo (implementar em F2.S2)

```yaml
schema: 1
modelos_tarefa:
  - { chave: limpeza,           nome: "Limpeza",                                         fases: ["*"], glpi_id: { prod: null, homolog: null } }
  - { chave: teste_componentes, nome: "Teste de Componentes",                            fases: ["*"], glpi_id: { prod: null, homolog: null } }
  - { chave: backup,            nome: "Backup",                                          fases: ["*"], glpi_id: { prod: null, homolog: null } }
  - { chave: formatar,          nome: "Formatar",                                        fases: ["*"], glpi_id: { prod: null, homolog: null } }
  - { chave: gep1, nome: "GEP 1. Descoberta do problema (Product discovery)", fases: [F1], glpi_id: { prod: null, homolog: null } }
  - { chave: gep2, nome: "GEP 2. Elicitação de Requisitos",                  fases: [F1], glpi_id: { prod: null, homolog: null } }
  - { chave: gep3, nome: "GEP 3. Análise de Requisitos",                     fases: [F1], glpi_id: { prod: null, homolog: null } }
  - { chave: gep4, nome: "GEP 4. Projeto da Solução",                        fases: [F1], glpi_id: { prod: null, homolog: null } }
  - { chave: gep5, nome: "GEP 5. Implementação das funcionalidades",         fases: [F2], padrao_da_fase: true, glpi_id: { prod: null, homolog: null } }
  - { chave: gep6, nome: "GEP 6. Validação e Testes",                        fases: [F3], padrao_da_fase: true, glpi_id: { prod: null, homolog: null } }
  - { chave: gep7, nome: "GEP 7. Disponibilização",                          fases: [F5], padrao_da_fase: true, glpi_id: { prod: null, homolog: null } }

categorias_tarefa:
  - { chave: adequacao_legal,         nome: "Adequação Legal" }
  - { chave: corretiva,               nome: "Corretiva" }
  - { chave: debito_tecnico,          nome: "Débito técnico" }
  - { chave: desenvolvimento_proprio, nome: "Desenvolvimento próprio" }
  - { chave: evolutiva,               nome: "Evolutiva" }
  - { chave: manutencao_equipamento,  nome: "Manutenção de equipamento" }
  - { chave: suporte_operacao,        nome: "Suporte/Operação" }

status_tarefa: { informacao: 0, a_fazer: 1, feito: 2 }
```

Os `glpi_id` ficam nulos ate alguem com leitura de `TaskTemplate` e
`TaskCategory` os informar (o perfil da API recebe 403). Com id nulo, o
script grava sem modelo/categoria e avisa.

## 5. A confirmar com o usuario (F1.S2.P2)

- Fases dos modelos genericos (Limpeza, Teste de Componentes, Backup,
  Formatar): o rascunho deixa todos em todas as fases (`"*"`).
- Modelo padrao de F1 quando o P nao declarar `modelo` (GEP 1 a 4 sao
  todos de F1).
- GEP 7 tambem em F4 (disponibilizacao em homologacao)?
- C e R deste repositorio (`toolkit-agentes-skills`): chamado e projeto GLPI
  ainda nao definidos.
- Ids de `TaskTemplate` e `TaskCategory` em producao e em homologacao.

## 6. Achado lateral

O catalogo do `glpi-tree-validate` tem duas regras **V23** (datas/duracoes e
horas por sessao). A de datas/duracoes passa a V31 em F2.S1.P3. As
regras novas deste plano usam V32 em diante.
