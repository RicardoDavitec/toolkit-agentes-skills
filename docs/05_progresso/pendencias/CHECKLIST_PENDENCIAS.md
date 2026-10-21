# Checklist de pendências atemporais

> **Convenções e instruções:** [`README.md`](README.md)  
> **Padrão de checklist:** skill `documente-o-plano` · **Alimentação:** skill `inserir-pendencia`

## Índice

| ID | Status | Módulo | Inserido em | Corrigido em | Título |
|----|--------|--------|-------------|--------------|--------|
| PEND-20261021-001 | [x] | glpi+docs | 2026-10-21 10:05 | 2026-10-21 13:10 | Retro-scan gera arvore fora de C-R-F-S-P |
| PEND-20261021-002 | [x] | glpi+docs | 2026-10-21 10:14 | 2026-10-21 13:10 | Nome do projeto raiz ainda nao usa o molde completo GEP |
| PEND-20261021-003 | [x] | glpi+docs | 2026-10-21 11:19 | 2026-10-21 13:10 | Gerador ainda nao grava as quatro datas e duracoes |

## Pendências

- [x] **PEND-20261021-001** Retro-scan gera arvore fora de C-R-F-S-P
  Módulo: `glpi+docs`
  Inserido em: `2026-10-21 10:05`
  Corrigido em: `2026-10-21 13:10`
  Contexto: O `glpi-retro-scan` deste template ainda descreve S como fase e P como pacote. Não emite Chamado ITIL (C) nem Projeto vinculado (R). Os códigos saem de títulos antigos de markdown (`M.DOCS`, `8.2.A`, `R1`, `F0`) em vez de `F#` / `F#.S#` / `F#.S#.P#`. A convenção `convencao-codigos-glpi` já manda C e R só no cabeçalho, por id, e o corpo em Fase → Sessão → Tarefa. O achado veio do teste de homologação do Bot_Pan (scan `2026-10-21_0951_botpan_pack`, 458 candidatos). A correção nasce neste repositório. O produto só recebe a cópia pelo upgrade do kit, depois que o teste de homologação terminar. O filtro paliativo do Bot_Pan não substitui este item.
  Critério: `glpi-retro-scan` e `glpi-retro-apply` emitem árvore C (Ticket, só id) → R (Project ligado por Itil_Project, só id) → F1–F5 fixas → sessões `F#.S#` → tarefas `F#.S#.P#`; o validador recusa outro formato; o relatório deixa de tratar S como fase e P como pacote; o R legado de markdown (`## R1`) não vira projeto.
  Evidência: relatório do Bot_Pan `docs/06_glpi/retro-scans/2026-10-21_0951_botpan_pack.md` (cabeçalho “S = fase · P = pacote”). Espelho no produto: `PEND-20261021-001`.
  Refs: `tools/glpi/lib/retro_scan.py`; `tools/glpi/lib/retro_apply.py`; `.cursor/skills/glpi-retro-scan/SKILL.md`; `.cursor/skills/convencao-codigos-glpi/SKILL.md`.
  <!-- glpi: plan_start="2026-10-21 10:05" plan_end="2026-10-31 18:00" real_end="2026-10-21 13:10" -->

- [x] **PEND-20261021-002** Nome do projeto raiz ainda nao usa o molde completo GEP
  Módulo: `glpi+docs`
  Inserido em: `2026-10-21 10:14`
  Corrigido em: `2026-10-21 13:10`
  Contexto: O preset declara `naming.root` = `GEP - {produto} - 0. [PAI]`, mas a criação de Project não substituía esse molde. O teste do Bot_Pan criou o projeto 83 como "Botão do Pânico". `glpi project create` sem projeto pai agora coloca o prefixo `GEP - ` se ele faltar. Fase, sessão e tarefa não recebem o prefixo. Falta um helper único que aplique o molde inteiro, inclusive o sufixo ` - 0. [PAI]`, e que os agentes chamem esse helper.
  Critério: criar Project raiz no preset PMF grava o nome pelo molde `naming.root`, sem prefixo duplicado; subprojeto de fase não recebe `GEP - `; skill, CLI e agentes GLPI usam o mesmo helper.
  Evidência: achado no Bot_Pan, projeto homolog 83. Espelho no produto: `PEND-20261021-002`.
  Refs: `tools/glpi/glpi`; `.glpi/presets/api-vscode-glpi/model.overlay.yaml`; `.cursor/skills/convencao-codigos-glpi/SKILL.md`; `.cursor/agents/glpi-orquestrador.md`.
  <!-- glpi: plan_start="2026-10-21 10:14" plan_end="2026-10-31 18:00" real_end="2026-10-21 13:10" -->

- [x] **PEND-20261021-003** Gerador ainda nao grava as quatro datas e duracoes
  Módulo: `glpi+docs`
  Inserido em: `2026-10-21 11:19`
  Corrigido em: `2026-10-21 13:10`
  Contexto: F, S e P precisam de `plan_start_date`, `plan_end_date`, `planned_duration` e `effective_duration`. No realizado, a origem é o plano ou o `git log`. No planejado, as duas datas são obrigatórias e a duração efetiva é 0. Skills, agentes, `retro_apply` (envia as duas durações) e `temporal_fill` (usa o intervalo real até 8 h) já declaram a regra. `retro_scan.py` ainda não garante as duas datas a partir do git em todo nó.
  Critério: o gerador preenche os quatro campos em todo F, S e P; o realizado não usa data inventada; o planejado não sai sem início e fim planejados.
  Evidência: teste do Bot_Pan no projeto homolog 83. Espelho no produto: `PEND-20261021-003`.
  Refs: `tools/glpi/lib/retro_scan.py`; `tools/glpi/lib/retro_apply.py`; `.cursor/skills/glpi-retro-scan/SKILL.md`.
  <!-- glpi: plan_start="2026-10-21 11:19" plan_end="2026-10-31 18:00" real_end="2026-10-21 13:10" -->

## Histórico (concluídas)

_Nenhuma ainda._
