# F1.S1 — Inventario e diagnostico (levantamento inicial)

> Plano: [`unificacao_template_kit_glpi-12_10_26-10_40.md`](../unificacao_template_kit_glpi-12_10_26-10_40.md)
> Levantamento: 12/10/2026, a partir dos clones locais em `~/ws/`.
> Este anexo e o ponto de partida do F1.S1; os P ainda precisam ser executados.

## Fontes

| Repositorio | Papel | Situacao local |
|-------------|-------|----------------|
| `toolkit-agents-skills` (GitHub) | Template de destino | Clonado em `~/ws/toolkit-agents-skills` (2 commits) |
| `API-VSCode-GLPI` = `pmf-dev-kit` (Gitness PMF) | Origem do CLI GLPI, skills e agentes GLPI | **Nao clonado**; conteudo visivel so via Bot_Pan |
| `Bot_Pan` | Consumidor que ja recebeu o kit GLPI | `~/ws/bot_pan` |

## Template atual (toolkit-agents-skills)

Foco: VS Code + Copilot Chat, fluxo hexagonal, backup e sessao.

| Tipo | Itens |
|------|-------|
| Agentes (`.github/agents/*.agent.md`, formato Copilot) | `orquestrador-hexagonal`, `revisor-arquitetura-hexagonal`, `analista-incidentes-integracao`, `operador-entrega-controlada` |
| Skills (`.github/skills/`) | `backup-projeto`, `documentar-sessao`, `encerrar-sessao`, `fluxo-orquestrado-hexagonal`, `guardrails-hexagonal`, `checar-contratos-portas`, `revisar-casos-de-uso`, `operacao-planilha-segura`, `gate-release-hexagonal` |
| Config | `.github/skills/config/endpoints_operacionais.json`, `.env.endpoints.example` |
| Docs | `docs/00_visao_geral` .. `docs/05_progresso`, `docs/06_progresso/historico`, `docs/guia_agentes_skills_ptbr.md` |
| Ausente | `.cursor/`, `AGENTS.md`, planos F/S/P, CLI GLPI |

## Kit GLPI (como aparece no Bot_Pan)

| Tipo | Itens |
|------|-------|
| Skills (37 em `.github/skills/`) | `acompanhar-chamado`, `atualizar`, `atualizar-kit`, `backup`, `build-*`, `commit`, `deploy-*`, `documentar`, `documente-o-plano`, `empacotar-apk`, `encerrar-sessao`, `exporte`, `glpi-*` (13), `implemente`, `importe`, `inserir-pendencia`, `oncoto-oncovo`, `planeje-a-semana`, `registrar-tentativa`, `revisar-docs`, `sincronize` |
| Agentes (`.github/agents/<nome>/AGENT.md`) | `glpi-orchestrator`, `glpi-auditor`, `glpi-migrator`, `glpi-scribe` |
| CLI (`tools/glpi/bin/`) | `glpi-document-attach`, `glpi-followup`, `glpi-project-create`, `glpi-retro-apply`, `glpi-retro-scan`, `glpi-seed-phases`, `glpi-task-upsert`, `glpi-weekly-sheet.py` |
| Config (`.glpi/`) | `model.defaults.yaml`, `presets/{generic,api-vscode-glpi}`, `templates/*-phases.*`, `*.example`, `maps/` |
| Scripts | `bootstrap-into.sh`, `upgrade-into.sh`, `install-glpi.sh`, `atualizar-kit` |
| Docs | `docs/06_glpi/` (manuais, hierarquia, integracao) |

Skills especificas de produto (nao vao para o template generico):
`build-*`, `deploy-*`, `empacotar-apk`.

## Defeitos encontrados no Bot_Pan

1. **Skills concatenadas** (commit `dcc7a47`, merge de `api-vscode-glpi/main`):
   13 skills com a versao curta S/P seguida da versao longa F/S/P —
   `atualizar`, `backup`, `commit`, `documentar`, `documente-o-plano`,
   `encerrar-sessao`, `exporte`, `glpi-followup`, `glpi-project-create`,
   `glpi-retro-scan`, `glpi-task-upsert`, `importe`, `oncoto-oncovo`.
   Cabecalho YAML invalido (duas chaves `description`) em `documentar`,
   `encerrar-sessao`, `exporte`, `importe`, `oncoto-oncovo`.
2. **Marcadores de conflito** nao resolvidos em 7 arquivos: `.gitignore`,
   `scripts/atualizar-kit`, `LICENSE`, `README.md`, `docs/README.md`,
   `docs/05_progresso/geral/README.md`,
   `docs/05_progresso/geral/FLUXO_COMMIT_CHECKLIST.md`.
3. **Catalogo duplicado e divergente**: `.github/skills` (37) x
   `.cursor/skills` (27). 13 iguais, 13 diferentes, 11 so em `.github`,
   1 so em `.cursor` (`ricardizar`).
4. `.cursor/skills/ricardizar/Skill.md` — nome fora do padrao `SKILL.md`.
5. Skills F/S/P citam binarios ainda inexistentes: `glpi-tree-validate`,
   `glpi-commit-harvest`, `glpi-progress-rollup`, `glpi-node-upsert`,
   `glpi-phase-ensure`, `glpi-migrate-codes`.
6. Documentos citados e ausentes: `docs/06_glpi/HIERARQUIA_F_S_P_GLPI.md`
   (existe so `HIERARQUIA_S_P_GLPI.md`).
7. Remote `origin` do Bot_Pan com ponto final
   (`git@github.com:RicardoDavitec/Bot_Pan.git.`).

## Outros consumidores (contagem em 12/10/2026)

| Projeto | `.github/skills` | `.cursor/skills` | `tools/glpi` |
|---------|------------------|------------------|--------------|
| Barra_Factory | 24 | 0 | nao |
| chatbot-docs | 24 | 0 | nao |
| mev_v3 | 34 | 0 | nao |
| samu_operacional | 7 | 0 | sim |

## Sobreposicoes template x kit GLPI (entrada para F1.S1.P4)

| Template | Kit GLPI | Acao proposta |
|----------|----------|---------------|
| `encerrar-sessao` | `encerrar-sessao` | Fundir (manter anexo GLPI + checklist do template) |
| `documentar-sessao` | `documentar` / `encerrar-sessao` | Avaliar fusao |
| `backup-projeto` | `backup` | Fundir (endpoints por SO do template) |
| agentes hexagonais | agentes `glpi-*` | Manter ambos; hexagonais como opcionais |
