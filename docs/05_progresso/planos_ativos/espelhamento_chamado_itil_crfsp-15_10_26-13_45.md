# Plano: Chamado ITIL de origem e espelhamento de pacotes em tarefas do chamado (C/R/F/S/P)

> Criado: 15/10/2026 13:45 · Fase principal: `F1` · Produto: `toolkit-agentes-skills`
> Arquivo: `espelhamento_chamado_itil_crfsp-15_10_26-13_45.md`
> Substitui: `unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md` (aceito em 14/10, movido para legados neste ciclo)
> Estado: **planejado**
> Piloto: Bot_Pan — C1 = chamado 15817 (producao), R1 = projeto 12 "GEP - Botão de Pânico - 0. [PAI]"

## Objetivo

Acrescentar dois niveis acima de F/S/P no kit — **C** (chamado ITIL de
origem) e **R** (projeto/requisicao) — e espelhar os pacotes P em andamento
e futuros como **tarefas do chamado ITIL pai** (`TicketTask`), com modelo,
categoria, duracao e janela planejada. Gravacao primeiro em homologacao.

## Motivacao (evidencia)

Todo projeto nasce de um chamado ITIL. No GLPI de producao, o chamado 15817
ja esta ligado ao projeto 12 (`Itil_Project` 74), mas o planejamento futuro
nao aparece no chamado: o projeto 12 tem zero `ProjectTask`, e as 12 tarefas
do chamado foram criadas a mao, para teste. O kit hoje so escreve
acompanhamento (`ITILFollowup`) no chamado e `ProjectTask` no projeto.
Detalhe: `anexos/F1_S1_levantamento_e_decisoes-15_10_26.md`.

## Requisitos de negocio (vinculo)

- Todo projeto/requisicao (R) tem um chamado ITIL de origem (C). Um C pode ter varios R.
- Espelhar so pacotes em andamento e futuros. As 12 tarefas de teste do 15817 ficam fora.
- Cada tarefa espelhada leva id GLPI, janela planejada (inicio e fim) e duracao estimada.
- Modelos de tarefa (Limpeza, Teste de Componentes, Backup, Formatar, GEP 1..7)
  e categorias em arquivo editavel, com elegibilidade por fase:
  GEP 1–4 → F1, GEP 5 → F2, GEP 6 → F3, GEP 7 → F5 (Producao/Aprovacao).
- Homologacao (`suporte-homolog`) antes de producao; o chamado de homologacao
  precisa ser criado.
- Nenhum segredo nos planos, no catalogo ou nos logs.

## Hierarquia C/R/F/S/P

```text
C  Chamado ITIL (Ticket)            C1           origem; recebe as TicketTask espelhadas
R  Projeto/Requisicao (Project)     C1.R1        ligado ao C por Itil_Project
F  Fase (subprojeto ou ProjectTask) C1.R1.F2     F1..F5 fixas
S  Sessao/sprint/semana             C1.R1.F2.S1
P  Tarefa ~2 h, ancorada em commit  C1.R1.F2.S1.P1  → espelhada como TicketTask no C
```

C e R sao ordinais locais; os ids GLPI ficam no `.glpi/project.yaml`, por
ambiente. A forma curta `F2.S1.P1` continua valida quando ha um so C e um so R.

## Janela de execucao

15/10/2026 a 30/10/2026. 28/10 (Dia do Servidor Publico) fica fora da agenda.
Pacote = 2 h (estimativa padrao do kit).

## Organograma (resumo)

| Code | Titulo | Janela | Esforco | Status |
|------|--------|--------|---------|--------|
| C1.R1.F1.S1 | Levantamento e decisoes | 15/10 | 8 h | [~] |
| C1.R1.F1.S2 | Requisitos e aceite das decisoes | 16/10 | 4 h | [ ] |
| C1.R1.F2.S1 | Niveis C e R no modelo e no validate | 19/10 | 8 h | [ ] |
| C1.R1.F2.S2 | Catalogo de modelos e categorias | 20/10 | 6 h | [ ] |
| C1.R1.F2.S3 | CLI do chamado ITIL | 21/10 | 6 h | [ ] |
| C1.R1.F2.S4 | Script de espelhamento | 22/10 | 8 h | [ ] |
| C1.R1.F2.S5 | Skills, agentes e docs | 23/10 | 8 h | [ ] |
| C1.R1.F3.S1 | Testes internos | 26/10 | 6 h | [ ] |
| C1.R1.F4.S1 | Homologacao no suporte-homolog | 27/10 | 8 h | [ ] |
| C1.R1.F4.S2 | Producao no chamado 15817 | 29/10 | 4 h | [ ] |
| C1.R1.F5.S1 | Versao e aceite | 30/10 | 4 h | [ ] |

## Fases e tarefas

### F1 — Planejamento

- [~] **C1.R1.F1** Planejamento do C/R/F/S/P e do espelhamento
  Aceite: decisoes D1–D10 aprovadas e requisitos atualizados.
  <!-- glpi: code="C1.R1.F1" plan_start="2026-10-15T11:30:00-03:00" plan_end="2026-10-16T12:00:00-03:00" real_start="2026-10-15T11:42:00-03:00" -->

  - [~] **C1.R1.F1.S1** Levantamento e decisoes (15/10)
    Leitura do chamado 15817 e do projeto 12; mapa dos campos da tarefa de
    chamado; decisoes D1–D10; rascunho do catalogo.
    Detalhe: `anexos/F1_S1_levantamento_e_decisoes-15_10_26.md`.
    <!-- glpi: code="C1.R1.F1.S1" plan_start="2026-10-15T11:30:00-03:00" plan_end="2026-10-15T19:30:00-03:00" real_start="2026-10-15T11:42:00-03:00" -->

    - [x] **C1.R1.F1.S1.P1** Investigar o chamado 15817 e o projeto 12 (15/10)
      Leitura por API em producao, so GET: vinculo `Itil_Project` 74,
      projeto 12 sem `ProjectTask`, 12 tarefas de teste, 403 em
      `TaskTemplate`/`TaskCategory`.
      <!-- glpi: code="C1.R1.F1.S1.P1" plan_start="2026-10-15T11:30:00-03:00" plan_end="2026-10-15T13:30:00-03:00" real_start="2026-10-15T11:42:00-03:00" real_end="2026-10-15T11:55:00-03:00" -->

    - [~] **C1.R1.F1.S1.P2** Esquema de codes C/R/F/S/P
      Criterio: D1–D3 (niveis, code longo, ids por ambiente, forma curta
      compativel, origem obrigatoria).
      <!-- glpi: code="C1.R1.F1.S1.P2" plan_start="2026-10-15T13:30:00-03:00" plan_end="2026-10-15T15:30:00-03:00" real_start="2026-10-15T13:45:00-03:00" -->

    - [~] **C1.R1.F1.S1.P3** Catalogo de modelos e categorias
      Criterio: D9–D10 e rascunho do arquivo (11 modelos, 7 categorias,
      3 status, fases elegiveis).
      <!-- glpi: code="C1.R1.F1.S1.P3" plan_start="2026-10-15T15:30:00-03:00" plan_end="2026-10-15T17:30:00-03:00" real_start="2026-10-15T13:45:00-03:00" -->

    - [~] **C1.R1.F1.S1.P4** Regras do espelho
      Criterio: D4–D8 (escopo, sentido unico, identidade, sem exclusao,
      homologacao primeiro) e mapa campo a campo.
      <!-- glpi: code="C1.R1.F1.S1.P4" plan_start="2026-10-15T17:30:00-03:00" plan_end="2026-10-15T19:30:00-03:00" real_start="2026-10-15T13:45:00-03:00" -->

  - [ ] **C1.R1.F1.S2** Requisitos e aceite das decisoes (16/10)
    <!-- glpi: code="C1.R1.F1.S2" plan_start="2026-10-16T08:00:00-03:00" plan_end="2026-10-16T12:00:00-03:00" -->

    - [ ] **C1.R1.F1.S2.P1** Atualizar `docs/01_requisitos`
      Criterio: RF11 (C de origem obrigatorio), RF12 (espelho P → TicketTask),
      RF13 (catalogo editavel com elegibilidade por fase), RNF6 (homologacao
      antes de producao) e riscos.
      <!-- glpi: code="C1.R1.F1.S2.P1" plan_start="2026-10-16T08:00:00-03:00" plan_end="2026-10-16T10:00:00-03:00" -->

    - [ ] **C1.R1.F1.S2.P2** Aceite das decisoes pendentes
      Criterio: respostas da secao 5 do anexo (fases dos modelos genericos,
      padrao de F1, GEP 7 em F4, C/R do toolkit, ids de modelo e categoria).
      <!-- glpi: code="C1.R1.F1.S2.P2" plan_start="2026-10-16T10:00:00-03:00" plan_end="2026-10-16T12:00:00-03:00" -->

### F2 — Implementacao

- [ ] **C1.R1.F2** Implementacao no template
  Aceite: kit entende C/R, le o catalogo e espelha P em TicketTask em simulacao.
  <!-- glpi: code="C1.R1.F2" plan_start="2026-10-19T08:00:00-03:00" plan_end="2026-10-23T17:00:00-03:00" -->

  - [ ] **C1.R1.F2.S1** Niveis C e R no modelo e no validate (19/10)
    <!-- glpi: code="C1.R1.F2.S1" plan_start="2026-10-19T08:00:00-03:00" plan_end="2026-10-19T17:00:00-03:00" -->

    - [ ] **C1.R1.F2.S1.P1** `codes.pattern` e `topology` em `model.defaults.yaml`
      Criterio: aceita `C<n>.R<n>.F..` e a forma curta; `max_depth` 5 com C e R
      fora dos objetos `ProjectTask`.
      <!-- glpi: code="C1.R1.F2.S1.P1" plan_start="2026-10-19T08:00:00-03:00" plan_end="2026-10-19T10:00:00-03:00" -->

    - [ ] **C1.R1.F2.S1.P2** `chamados` e `requisicoes` no `project.yaml`
      Criterio: `.glpi/project.yaml.example` e `project.homolog.yaml.example`
      com ids por ambiente; loader comum em Python e no bash.
      <!-- glpi: code="C1.R1.F2.S1.P2" plan_start="2026-10-19T10:00:00-03:00" plan_end="2026-10-19T12:00:00-03:00" -->

    - [ ] **C1.R1.F2.S1.P3** Regras do validate
      Criterio: V23 duplicada desfeita (datas/duracoes → V31); V32 R sem C;
      V33 P em andamento/futuro sem TicketTask (remoto); V34 modelo fora da
      fase; V35 TicketTask divergente do plano. `tree-example.json` com C/R.
      <!-- glpi: code="C1.R1.F2.S1.P3" plan_start="2026-10-19T13:00:00-03:00" plan_end="2026-10-19T15:00:00-03:00" -->

    - [ ] **C1.R1.F2.S1.P4** `retro_scan` e `retro_apply` com code longo
      Criterio: leem `C1.R1.F2.S1.P1` e a forma curta sem regressao.
      <!-- glpi: code="C1.R1.F2.S1.P4" plan_start="2026-10-19T15:00:00-03:00" plan_end="2026-10-19T17:00:00-03:00" -->

  - [ ] **C1.R1.F2.S2** Catalogo de modelos e categorias (20/10)
    <!-- glpi: code="C1.R1.F2.S2" plan_start="2026-10-20T08:00:00-03:00" plan_end="2026-10-20T14:00:00-03:00" -->

    - [ ] **C1.R1.F2.S2.P1** Arquivo do catalogo
      Criterio: `.glpi/presets/api-vscode-glpi/catalogos/tarefa_chamado.yaml`
      (PMF) e `.glpi/presets/generic/catalogos/tarefa_chamado.yaml.example`;
      sobrescrita do produto em `.glpi/catalogos/`.
      <!-- glpi: code="C1.R1.F2.S2.P1" plan_start="2026-10-20T08:00:00-03:00" plan_end="2026-10-20T10:00:00-03:00" -->

    - [ ] **C1.R1.F2.S2.P2** Loader e elegibilidade por fase
      Criterio: `tools/glpi/lib/catalogo.py` le YAML ou JSON, valida chaves
      unicas e fases, devolve o modelo padrao da fase.
      <!-- glpi: code="C1.R1.F2.S2.P2" plan_start="2026-10-20T10:00:00-03:00" plan_end="2026-10-20T12:00:00-03:00" -->

    - [ ] **C1.R1.F2.S2.P3** Ids GLPI dos modelos e categorias
      Criterio: `glpi catalog discover` tenta a API e, com 403, gera a
      planilha de preenchimento manual; ids nulos geram aviso.
      <!-- glpi: code="C1.R1.F2.S2.P3" plan_start="2026-10-20T12:00:00-03:00" plan_end="2026-10-20T14:00:00-03:00" -->

  - [ ] **C1.R1.F2.S3** CLI do chamado ITIL (21/10)
    <!-- glpi: code="C1.R1.F2.S3" plan_start="2026-10-21T08:00:00-03:00" plan_end="2026-10-21T14:00:00-03:00" -->

    - [ ] **C1.R1.F2.S3.P1** `glpi ticket create` e `glpi itil-link`
      Criterio: cria Ticket (simulacao por padrao) e o vinculo `Itil_Project`
      com um Project.
      <!-- glpi: code="C1.R1.F2.S3.P1" plan_start="2026-10-21T08:00:00-03:00" plan_end="2026-10-21T10:00:00-03:00" -->

    - [ ] **C1.R1.F2.S3.P2** `glpi itil-origin`
      Criterio: dado um Project, lista os chamados de origem; dado um Ticket,
      lista os projetos.
      <!-- glpi: code="C1.R1.F2.S3.P2" plan_start="2026-10-21T10:00:00-03:00" plan_end="2026-10-21T12:00:00-03:00" -->

    - [ ] **C1.R1.F2.S3.P3** `tools/glpi/lib/ticket_task.py`
      Criterio: list/get/create/update de TicketTask; anexo por
      `Document_Item`; nome do campo "adicionar a base de conhecimento"
      confirmado na API.
      <!-- glpi: code="C1.R1.F2.S3.P3" plan_start="2026-10-21T12:00:00-03:00" plan_end="2026-10-21T14:00:00-03:00" -->

  - [ ] **C1.R1.F2.S4** Script de espelhamento (22/10)
    `tools/glpi/bin/glpi-ticket-mirror` sobre `lib/ticket_mirror.py`.
    <!-- glpi: code="C1.R1.F2.S4" plan_start="2026-10-22T08:00:00-03:00" plan_end="2026-10-22T17:00:00-03:00" -->

    - [ ] **C1.R1.F2.S4.P1** Selecao e mapeamento
      Criterio: so P `[~]`/`[t]` ou `[ ]` com `plan_start` futuro; campos
      conforme o anexo (modelo, categoria, duracao, janela, usuario, grupo).
      <!-- glpi: code="C1.R1.F2.S4.P1" plan_start="2026-10-22T08:00:00-03:00" plan_end="2026-10-22T10:00:00-03:00" -->

    - [ ] **C1.R1.F2.S4.P2** Upsert idempotente com deteccao de conflito
      Criterio: prefixo `[code]` + `.glpi/index.json`; segunda execucao sem
      mudanca nao grava nada; edicao humana no GLPI nao e sobrescrita.
      <!-- glpi: code="C1.R1.F2.S4.P2" plan_start="2026-10-22T10:00:00-03:00" plan_end="2026-10-22T12:00:00-03:00" -->

    - [ ] **C1.R1.F2.S4.P3** Desfazer planejamento e cancelamento
      Criterio: P sem janela limpa `begin`/`end`; P removido vira
      "Informacao" com `[cancelado]`; nenhum `force_purge`.
      <!-- glpi: code="C1.R1.F2.S4.P3" plan_start="2026-10-22T13:00:00-03:00" plan_end="2026-10-22T15:00:00-03:00" -->

    - [ ] **C1.R1.F2.S4.P4** Relatorio antes/depois
      Criterio: tabela por P (acao, campos, conflito); `--env`, `--apply`,
      `--only=<code>`; exit != 0 se o validate falhar.
      <!-- glpi: code="C1.R1.F2.S4.P4" plan_start="2026-10-22T15:00:00-03:00" plan_end="2026-10-22T17:00:00-03:00" -->

  - [ ] **C1.R1.F2.S5** Skills, agentes e docs (23/10)
    <!-- glpi: code="C1.R1.F2.S5" plan_start="2026-10-23T08:00:00-03:00" plan_end="2026-10-23T17:00:00-03:00" -->

    - [ ] **C1.R1.F2.S5.P1** Skill `espelhar-chamado`
      Criterio: simulacao, tabela, confirmacao, gravacao, acompanhamento
      opcional; alias `glpi-ticket-mirror`.
      <!-- glpi: code="C1.R1.F2.S5.P1" plan_start="2026-10-23T08:00:00-03:00" plan_end="2026-10-23T10:00:00-03:00" -->

    - [ ] **C1.R1.F2.S5.P2** Skills existentes com C/R
      Criterio: `documente-o-plano`, `commit`, `oncoto-oncovo`,
      `glpi-tree-validate`, `glpi-retro-scan`, `glpi-node-upsert`,
      `glpi-migrate-codes` (F/S/P → C/R/F/S/P, so para frente),
      `acompanhar-chamado` (usa o C do plano).
      <!-- glpi: code="C1.R1.F2.S5.P2" plan_start="2026-10-23T10:00:00-03:00" plan_end="2026-10-23T12:00:00-03:00" -->

    - [ ] **C1.R1.F2.S5.P3** Agentes e bootstrap
      Criterio: `glpi-escriba`, `glpi-orquestrador`, `glpi-auditor` e
      `glpi-migrador` com C/R; `bootstrap-into.sh` pede o chamado de origem.
      <!-- glpi: code="C1.R1.F2.S5.P3" plan_start="2026-10-23T13:00:00-03:00" plan_end="2026-10-23T15:00:00-03:00" -->

    - [ ] **C1.R1.F2.S5.P4** Docs GLPI e lint
      Criterio: `docs/06_glpi/HIERARQUIA_S_P_GLPI.md` com C/R e o espelho;
      `planos_ativos/README.md` com o code longo; lint verde.
      <!-- glpi: code="C1.R1.F2.S5.P4" plan_start="2026-10-23T15:00:00-03:00" plan_end="2026-10-23T17:00:00-03:00" -->

### F3 — Testes Internos

- [ ] **C1.R1.F3** Testes internos
  <!-- glpi: code="C1.R1.F3" plan_start="2026-10-26T08:00:00-03:00" plan_end="2026-10-26T15:00:00-03:00" -->

  - [ ] **C1.R1.F3.S1** Testes offline e simulacao (26/10)
    <!-- glpi: code="C1.R1.F3.S1" plan_start="2026-10-26T08:00:00-03:00" plan_end="2026-10-26T15:00:00-03:00" -->

    - [ ] **C1.R1.F3.S1.P1** Testes com fixtures JSON
      Criterio: selecao, mapeamento, elegibilidade, conflito e idempotencia
      sem rede.
      <!-- glpi: code="C1.R1.F3.S1.P1" plan_start="2026-10-26T08:00:00-03:00" plan_end="2026-10-26T10:00:00-03:00" -->

    - [ ] **C1.R1.F3.S1.P2** CI
      Criterio: `glpi-tree-validate --strict` no exemplo C/R e lint no workflow.
      <!-- glpi: code="C1.R1.F3.S1.P2" plan_start="2026-10-26T10:00:00-03:00" plan_end="2026-10-26T12:00:00-03:00" -->

    - [ ] **C1.R1.F3.S1.P3** Simulacao contra homologacao
      Criterio: `glpi-ticket-mirror --env=homolog` sem `--apply`, so leitura.
      <!-- glpi: code="C1.R1.F3.S1.P3" plan_start="2026-10-26T13:00:00-03:00" plan_end="2026-10-26T15:00:00-03:00" -->

### F4 — Homologacao

- [ ] **C1.R1.F4** Homologacao
  Aceite: tarefas espelhadas conferidas na tela do chamado de homologacao e
  depois no 15817.
  <!-- glpi: code="C1.R1.F4" plan_start="2026-10-27T08:00:00-03:00" plan_end="2026-10-29T12:00:00-03:00" -->

  - [ ] **C1.R1.F4.S1** Homologacao no suporte-homolog (27/10)
    <!-- glpi: code="C1.R1.F4.S1" plan_start="2026-10-27T08:00:00-03:00" plan_end="2026-10-27T17:00:00-03:00" -->

    - [ ] **C1.R1.F4.S1.P1** Chamado ITIL de homologacao
      Criterio: Ticket criado em `suporte-homolog` espelhando o 15817 e
      ligado ao projeto do Bot_Pan na homologacao; id gravado em
      `chamados.C1.homolog` do Bot_Pan.
      <!-- glpi: code="C1.R1.F4.S1.P1" plan_start="2026-10-27T08:00:00-03:00" plan_end="2026-10-27T10:00:00-03:00" -->

    - [ ] **C1.R1.F4.S1.P2** Plano real do Bot_Pan em C/R/F/S/P
      Criterio: pacotes futuros com janela, horas e modelo; validate exit 0.
      <!-- glpi: code="C1.R1.F4.S1.P2" plan_start="2026-10-27T10:00:00-03:00" plan_end="2026-10-27T12:00:00-03:00" -->

    - [ ] **C1.R1.F4.S1.P3** Espelhar em homologacao
      Criterio: `--apply` em homologacao; conferencia de modelo, categoria,
      duracao, janela e status na tela; segunda execucao sem alteracao.
      <!-- glpi: code="C1.R1.F4.S1.P3" plan_start="2026-10-27T13:00:00-03:00" plan_end="2026-10-27T15:00:00-03:00" -->

    - [ ] **C1.R1.F4.S1.P4** Acompanhamento no chamado de homologacao
      Criterio: follow-up com titulo confirmado pelo usuario (herda o
      F4.S1.P3 do plano de unificacao).
      <!-- glpi: code="C1.R1.F4.S1.P4" plan_start="2026-10-27T15:00:00-03:00" plan_end="2026-10-27T17:00:00-03:00" -->

  - [ ] **C1.R1.F4.S2** Producao no chamado 15817 (29/10)
    <!-- glpi: code="C1.R1.F4.S2" plan_start="2026-10-29T08:00:00-03:00" plan_end="2026-10-29T12:00:00-03:00" -->

    - [ ] **C1.R1.F4.S2.P1** Espelhar no 15817
      Criterio: so apos o aceite de homologacao; as 12 tarefas de teste nao
      sao tocadas.
      <!-- glpi: code="C1.R1.F4.S2.P1" plan_start="2026-10-29T08:00:00-03:00" plan_end="2026-10-29T10:00:00-03:00" -->

    - [ ] **C1.R1.F4.S2.P2** Conferencia em producao
      Criterio: validate remoto exit 0; tarefas visiveis no planejamento do
      chamado.
      <!-- glpi: code="C1.R1.F4.S2.P2" plan_start="2026-10-29T10:00:00-03:00" plan_end="2026-10-29T12:00:00-03:00" -->

### F5 — Aprovacao

- [ ] **C1.R1.F5** Aprovacao
  <!-- glpi: code="C1.R1.F5" plan_start="2026-10-30T08:00:00-03:00" plan_end="2026-10-30T12:00:00-03:00" -->

  - [ ] **C1.R1.F5.S1** Versao e aceite (30/10)
    <!-- glpi: code="C1.R1.F5.S1" plan_start="2026-10-30T08:00:00-03:00" plan_end="2026-10-30T12:00:00-03:00" -->

    - [ ] **C1.R1.F5.S1.P1** Versao `v1.1.0` e `CHANGELOG.md`
      <!-- glpi: code="C1.R1.F5.S1.P1" plan_start="2026-10-30T08:00:00-03:00" plan_end="2026-10-30T10:00:00-03:00" -->

    - [ ] **C1.R1.F5.S1.P2** Termo de aceite
      Criterio: `[x]` → `[A]` com `accept_ref`.
      <!-- glpi: code="C1.R1.F5.S1.P2" plan_start="2026-10-30T10:00:00-03:00" plan_end="2026-10-30T12:00:00-03:00" -->

## Riscos

| Risco | Mitigacao |
|-------|-----------|
| Perfil da API sem leitura de modelo/categoria (403) | ids no catalogo, preenchidos a mao; aviso com id nulo |
| Editor do GLPI remover o comentario `glpi-meta` | prefixo visivel `[code]` + indice local |
| Sobrescrever edicao feita na tela | sentido unico com deteccao por `users_id_editor`/`date_mod` |
| Fuso nas datas (`begin` 02:00 nas tarefas de teste) | converter para America/Sao_Paulo e conferir na tela em homologacao |
| Code longo quebrar planos antigos | forma curta aceita com C1.R1 implicito |
| Exclusao acidental | nenhum `force_purge`; cancelamento vira "Informacao" |

## Pendencias

- [ ] C e R deste repositorio (`toolkit-agentes-skills`): chamado e projeto GLPI a definir.
- [ ] Ids de `TaskTemplate` e `TaskCategory` em producao e homologacao.
- [ ] Datas e duracoes dos projetos GLPI sem evidencia neste workspace (herdado do plano de unificacao).
- [ ] Implementar os 5 binarios GLPI so em spec (herdado do plano de unificacao).

## Proximos comandos sugeridos

```bash
./tools/glpi/bin/glpi-retro-scan      # depois de C1.R1.F2.S1.P4
./tools/glpi/bin/glpi-tree-validate --from=<scan.json> --strict
```
