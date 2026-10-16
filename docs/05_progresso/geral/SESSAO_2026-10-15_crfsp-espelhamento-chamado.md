# Sessao 2026-10-15 — Plano C/R/F/S/P e espelhamento no chamado ITIL

> **Chamado ITIL (C):** 15817 (producao)
> **Projeto/Requisicao (R):** 12 - "GEP - Botao de Panico - 0. [PAI]"
> **Piloto:** Bot_Pan | **Data:** 15/10/2026

## Sumario executivo

Investigado o chamado 15817 (Botao do Panico) em producao, so leitura.
Criado o plano vigente `espelhamento_chamado_itil_crfsp-15_10_26-13_45.md`,
que acrescenta os niveis C (chamado ITIL) e R (projeto/requisicao) acima de
F/S/P e espelha pacotes em andamento e futuros como tarefas do chamado. O
plano de unificacao, aceito em 14/10, foi para `legados/` com os anexos.

## Commits da sessao

- `d717bcf` (14/10, enviado hoje) — F5.S1, tag `v1.0.0`
- Commit deste registro — plano C/R/F/S/P, anexo de decisoes e mudanca para legados
- `API-VScode-GLPI` `101518b` (14/10, enviado hoje) — README aponta para o template

## Evidencia do GLPI (producao, so GET)

- Ticket 15817 ligado ao Project 12 por `Itil_Project` 74.
- Project 12 sem `ProjectTask`; 12 tarefas de teste no chamado, sem code.
- `TaskTemplate`, `TaskCategory` e `ITILCategory`: 403 para o perfil Technician.

## Problemas

- O perfil da API nao le modelos nem categorias de tarefa. Os ids vao no
  catalogo, informados a mao.
- O catalogo do `glpi-tree-validate` tem duas regras V23. A renumeracao
  entrou no plano (F2.S1.P3).

## Decisoes

- Code longo `C<n>.R<n>.F<n>.S<n>.P<n>`, com ids GLPI por ambiente no
  `.glpi/project.yaml`; a forma curta segue valida.
- Espelho so de pacotes em andamento e futuros, sentido plano → chamado,
  sem exclusao automatica. As 12 tarefas de teste ficam fora.
- Catalogo de modelos e categorias em YAML editavel, com fases elegiveis
  (GEP 1–4 F1, GEP 5 F2, GEP 6 F3, GEP 7 F5).
- Homologacao primeiro, com chamado novo no `suporte-homolog`.

## Proximas acoes

- F1.S2.P2: responder as pendencias do anexo (fases dos modelos
  genericos, padrao de F1, GEP 7 em F4, C/R do toolkit, ids GLPI).
- F1.S2.P1: requisitos RF11–RF13 e RNF6.
