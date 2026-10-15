# F1.S1 — Inventario e diagnostico (13/10/2026, atualizado 14/10)

> Plano: [`unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md`](../unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md)
> Levantamento: 13/10/2026; clones de mev_v3 e Barra_Factory em 14/10/2026.

## Fontes

| Repositorio | Papel | Situacao local |
|-------------|-------|----------------|
| `toolkit-agentes-skills` (GitHub) | Template de destino | `/home/wsl/projetos/toolkit-agentes-skills` |
| `API-VScode-GLPI` = `pmf-dev-kit` | Origem CLI GLPI, skills, agentes | `/home/wsl/projetos/API-VScode-GLPI` (`f83ff4f`) |
| `Bot_Pan` | Consumidor piloto | 37 skills `.github` x 27 `.cursor`; conflitos |
| `samu-operacional` | Consumidor com CLI GLPI | 33 x 23; `implemente` local |
| `mev_v3` | Consumidor | Clonado 14/10 (`a891c34`); 37 skills `.github`, 0 `.cursor`, 5 agentes (inclui `integrador-chatbot-pet`) |
| `Barra_Factory` | Consumidor | Clonado 14/10; 24 skills `.github`, 0 `.cursor`, 4 agentes hexagonais |
| `chatbot-docs` | Consumidor citado no plano de 12/10 | **Nao encontrado** no GitHub (`RicardoDavitec`) nem no Gitness. Justificativa de exclusao. |

## Template atual (toolkit-agentes-skills)

| Tipo | Itens |
|------|-------|
| Agentes (`.github/agents/*.agent.md`, Copilot) | `orquestrador-hexagonal`, `revisor-arquitetura-hexagonal`, `analista-incidentes-integracao`, `operador-entrega-controlada` |
| Skills (`.github/skills/`) | `backup-projeto`, `documentar-sessao`, `encerrar-sessao`, `fluxo-orquestrado-hexagonal`, `guardrails-hexagonal`, `checar-contratos-portas`, `revisar-casos-de-uso`, `operacao-planilha-segura`, `gate-release-hexagonal` + `config/` |
| Ausente | `.cursor/`, `AGENTS.md`, CLI GLPI |

## Kit GLPI (API-VScode-GLPI)

| Tipo | Itens |
|------|-------|
| Skills (25 em `.github/skills/`) | `acompanhar-chamado`, `atualizar`, `atualizar-kit`, `backup`, `commit`, `documentar`, `documente-o-plano`, `encerrar-sessao`, `exporte`, `glpi-*` (13: backlog-export, commit-harvest, document-attach, followup, migrate-codes, node-upsert, phase-ensure, progress-rollup, project-create, retro-scan, task-upsert, tree-validate, seed_phases), `importe`, `inserir-pendencia`, `oncoto-oncovo`, `planeje-a-semana` |
| Agentes (`.github/agents/<nome>/AGENT.md`) | `glpi-orchestrator`, `glpi-auditor`, `glpi-migrator`, `glpi-scribe` |
| CLI (`tools/glpi/bin/`) | `glpi-document-attach`, `glpi-followup`, `glpi-project-create`, `glpi-retro-apply`, `glpi-retro-scan`, `glpi-seed-phases`, `glpi-task-upsert`, `glpi-tree-validate`, `glpi-weekly-sheet.py` |
| Config (`.glpi/`) | `model.defaults.yaml`, `presets/{generic,api-vscode-glpi}`, `templates/`, `maps/` |
| Scripts | `bootstrap-into.sh`, `upgrade-into.sh`, `install-glpi.sh`, `install_glpi.py`, `atualizar-kit` |

Binarios citados por skills mas **ausentes** no CLI: `glpi-commit-harvest`,
`glpi-progress-rollup`, `glpi-node-upsert`, `glpi-phase-ensure`,
`glpi-migrate-codes`. `glpi-tree-validate` existe.

## Skill ausente no kit: `sincronize`

Presente em Bot_Pan, samu-operacional e `~/.cursor/skills`, **ausente** no
API-VScode-GLPI. Deve entrar no catalogo canonico (F2.S2.P3).

## Defeitos nos consumidores (14/10)

| Projeto | Defeitos |
|---------|----------|
| Bot_Pan | YAML com 2x `description` em `documentar`, `encerrar-sessao`, `exporte`, `importe`, `oncoto-oncovo`; conflitos em `README.md`, `docs/README.md`, `.gitignore`, `FLUXO_COMMIT_CHECKLIST.md`; `ricardizar/Skill.md` (nome fora do padrao); remote `origin` com `.` final |
| samu-operacional | `glpi-retro-scan` com `<<<<<<<`; `description` duplicada em `acompanhar-chamado`, `documentar`, `encerrar-sessao`, `exporte`, `importe`, `oncoto-oncovo` |
| mev_v3 | Sem `.cursor/`; tem `commit-skill` (variante de `commit`), `USABILIDADE_MEV.md` em skills; agente extra `integrador-chatbot-pet` |
| Barra_Factory | Sem `.cursor/`; `commit-skill` idem; `CATALOGO_IMPORTACAO.md` em skills |

## Sobreposicoes template x kit GLPI

| Template | Kit GLPI | Acao |
|----------|----------|------|
| `encerrar-sessao` | `encerrar-sessao` | Fundir |
| `documentar-sessao` | `documentar` | Fundir |
| `backup-projeto` | `backup` | Fundir |
| agentes hexagonais (4) | agentes `glpi-*` (4) | Manter ambos, reescritos em `.cursor/agents/*.md` |
