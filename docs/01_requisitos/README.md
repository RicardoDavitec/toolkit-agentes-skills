# 01 Requisitos — toolkit-agentes-skills

> Preenchido em 14/10/2026 (F1.S2.P5 do plano de unificacao).

## Visao

Template **unico** de inicializacao de repositorios de projeto, com agentes e
skills para **Cursor**, integracao **GLPI** via API REST (qualquer instancia)
e fluxo de documentacao **F/S/P** (Fase / Sessao-Sprint / Tarefa ancorada em
commit). Substitui o `pmf-dev-kit` (API-VScode-GLPI) como fonte.

## Requisitos funcionais

| # | Requisito |
|---|-----------|
| RF1 | Catalogo canonico de skills em `.cursor/skills/<nome>/SKILL.md`, uma por pasta, cabecalho YAML unico e valido, `name` igual ao nome da pasta |
| RF2 | Catalogo canonico de agentes em `.cursor/agents/<nome>.md` (formato Cursor) |
| RF3 | `.github/skills` como symlink para `../.cursor/skills` (compatibilidade; nunca copia) |
| RF4 | CLI GLPI em `tools/glpi/` vendorizado nos consumidores; presets `generic` e `api-vscode-glpi` |
| RF5 | Config `.glpi/` sem segredos no template (`*.example`; `instance.yaml`, `project.yaml`, `maps/states.json` so no consumidor) |
| RF6 | Scripts `bootstrap-into.sh` (projeto novo) e `upgrade-into.sh` (projeto existente) com dry-run, backup e preservacao da camada de produto |
| RF7 | Skill `atualizar-kit` apontando para `toolkit-agentes-skills` como fonte |
| RF8 | Documentacao do template em PT-BR; gatilhos de skill com "Use em ..." |
| RF9 | Arvore de docs: `05_progresso/{planos_ativos,geral,legados,pendencias,historico}` + `06_glpi` |
| RF10 | Aliases DEPRECATED mantidos para skills renomeadas/fundidas |

## Requisitos nao funcionais

| # | Requisito |
|---|-----------|
| RNF1 | Identificadores sem acento (compatibilidade de tooling) |
| RNF2 | Nenhum segredo versionado (token, `.env`, keystore) — lint bloqueia |
| RNF3 | Historico dos repositorios de origem preservado (subtree); nada apagado |
| RNF4 | Funciona em WSL/Linux/macOS; Windows nativo exige Modo Desenvolvedor para o symlink |
| RNF5 | Copilot fora do alvo: `.agent.md` descontinuado, sem manutencao |

## Criterios de aceite (macro)

- Lint de skills/agentes verde (YAML valido, sem chave duplicada, sem
  marcador de conflito, sem segredo, `SKILL.md` com nome exato).
- `glpi-tree-validate` exit 0 no plano exemplo.
- Bootstrap em projeto vazio: Cursor lista skills e agentes.
- Upgrade em consumidor: preserva skills de produto e `.glpi/` real.

## Riscos de requisito

| Risco | Mitigacao |
|-------|-----------|
| Repetir o erro do Bot_Pan (versoes concatenadas) | Proibido merge `union`; gate `rg` de marcadores + lint YAML |
| Symlink quebrar no Windows nativo | Documentar requisito; scripts detectam e avisam |
| Divergencia com `~/.cursor/skills` pessoal | Documentar precedencia: projeto vence pessoal |
| Binarios GLPI citados e ausentes | F2.S2.P4: criar ou remover a citacao |
