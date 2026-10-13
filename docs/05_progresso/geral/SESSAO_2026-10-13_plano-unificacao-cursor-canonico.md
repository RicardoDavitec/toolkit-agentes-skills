# Sessao 2026-10-13 — Plano de unificacao com canonico .cursor

## Sumario

Revisao da estrategia de unificacao do `toolkit-agentes-skills` com o
`API-VScode-GLPI` (`pmf-dev-kit`). Decisao central: **canonico em `.cursor/`**,
nao mais em `.github/`, porque o Copilot deixa de ser alvo do fluxo.

## Decisoes

- **F1.S2.P1 decidido**: canonico em `.cursor/skills/<nome>/SKILL.md` e
  `.cursor/agents/<nome>.md`. `.github/skills` vira symlink de compatibilidade
  apontando para `../.cursor/skills`. Agentes `.agent.md` (Copilot) sao
  descontinuados.
- Plano antigo (`unificacao_template_kit_glpi-12_10_26-10_40.md`) movido para
  `docs/05_progresso/legados/`.
- Novo plano vigente criado: `unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md`
  (360 linhas, modelo longo F/S/P).
- Inventario de 13/10 incorporado ao plano: `sincronize` entra como skill a
  importar dos consumidores; `glpi-tree-validate` ja existe; mev_v3 = zip;
  Barra_Factory e chatbot-docs ausentes nesta maquina.

## Commits

- (pendente) `docs(plano): unificacao template kit glpi cursor canonico`

## Proximas acoes

- Escrever anexos `F1_S1_inventario-13_10_26.md` e `F1_S2_decisoes-13_10_26.md`.
- Definir janelas `plan_start`/`plan_end` antes de integrar ao GLPI.
- Executar F1.S1.P4 (matriz de mapeamento skills/agentes).
