# F1.S1.P4 — Matriz de mapeamento skills/agentes (14/10/2026)

> Plano: [`unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md`](../unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md)
> Destino canonico: `.cursor/skills/<nome>/SKILL.md` e `.cursor/agents/<nome>.md`.

Convencao: **Manter** = entra como esta · **Fundir** = conteudo mesclado em
um so arquivo · **Renomear** = nome final PT-BR · **Descartar** = nao entra
(fica historico) · **Produto** = nao entra no template generico; fica no
consumidor.

## Skills — origem: API-VScode-GLPI (kit GLPI)

| Skill | Destino | Nome final | Observacao |
|-------|---------|-----------|------------|
| `acompanhar-chamado` | Manter | `acompanhar-chamado` | GLPI follow-up |
| `atualizar` | Fundir | `atualizar` | Fundir com `sincronize` (P2) |
| `atualizar-kit` | Manter | `atualizar-kit` | Aponta para toolkit-agentes-skills |
| `backup` | Fundir | `backup` | Fundir com `backup-projeto` (P2) |
| `commit` | Manter | `commit` | Substitui `commit-skill` dos consumidores |
| `documentar` | Fundir | `documentar` | Fundir com `documentar-sessao` (P2) |
| `documente-o-plano` | Manter | `documente-o-plano` | S/P + timestamps GLPI |
| `encerrar-sessao` | Fundir | `encerrar-sessao` | Fundir versao template + kit (P2) |
| `exporte` | Manter | `exporte` | Push |
| `glpi-backlog-export` | Manter | `glpi-backlog-export` | |
| `glpi-commit-harvest` | Manter | `glpi-commit-harvest` | Binario ausente (F2.S2.P4) |
| `glpi-document-attach` | Manter | `glpi-document-attach` | |
| `glpi-followup` | Manter (alias) | `glpi-followup` | Alias DEPRECATED de `acompanhar-chamado` |
| `glpi-migrate-codes` | Manter | `glpi-migrate-codes` | Binario ausente (F2.S2.P4) |
| `glpi-node-upsert` | Manter | `glpi-node-upsert` | Binario ausente (F2.S2.P4) |
| `glpi-phase-ensure` | Manter | `glpi-phase-ensure` | Binario ausente (F2.S2.P4) |
| `glpi-progress-rollup` | Manter | `glpi-progress-rollup` | Binario ausente (F2.S2.P4) |
| `glpi-project-create` | Manter (alias) | `glpi-project-create` | Alias DEPRECATED de `glpi-project-upsert` |
| `glpi-retro-scan` | Manter | `glpi-retro-scan` | |
| `glpi-task-upsert` | Manter (alias) | `glpi-task-upsert` | Alias DEPRECATED de `glpi-node-upsert` |
| `glpi-tree-validate` | Manter | `glpi-tree-validate` | Binario existe |
| `glpi_seed_phases` | Manter (alias) | `glpi_seed_phases` | Alias DEPRECATED de `glpi-phase-ensure` |
| `importe` | Manter | `importe` | Pull |
| `inserir-pendencia` | Manter | `inserir-pendencia` | |
| `oncoto-oncovo` | Manter | `oncoto-oncovo` | |
| `planeje-a-semana` | Manter | `planeje-a-semana` | |

## Skills — origem: consumidores (nao estao no kit GLPI)

| Skill | Destino | Nome final | Origem escolhida |
|-------|---------|-----------|------------------|
| `sincronize` | Manter | `sincronize` | `~/.cursor/skills/sincronize` (versao mais completa, 2853 bytes) |

## Skills — origem: template (hexagonal/operacional)

| Skill | Destino | Nome final | Observacao |
|-------|---------|-----------|------------|
| `backup-projeto` | Fundir | `backup` | Conteudo mesclado em `backup` |
| `documentar-sessao` | Fundir | `documentar` | Conteudo mesclado em `documentar` |
| `encerrar-sessao` | Fundir | `encerrar-sessao` | Mesclar com versao do kit |
| `fluxo-orquestrado-hexagonal` | Manter | `fluxo-orquestrado-hexagonal` | Dominio hexagonal |
| `guardrails-hexagonal` | Manter | `guardrails-hexagonal` | |
| `checar-contratos-portas` | Manter | `checar-contratos-portas` | |
| `revisar-casos-de-uso` | Manter | `revisar-casos-de-uso` | |
| `operacao-planilha-segura` | Manter | `operacao-planilha-segura` | |
| `gate-release-hexagonal` | Manter | `gate-release-hexagonal` | |
| `config/` | Manter | `config/` | `endpoints_operacionais.json` |

## Skills — especificas de produto (nao entram no template)

| Skill | Projeto | Acao |
|-------|---------|------|
| `build-backend` / `build-web` / `build-mobile` | Bot_Pan, samu, Barra | Produto |
| `deploy-backend` / `deploy-web` / `deploy-mobile` | Bot_Pan, samu | Produto |
| `empacotar-apk` | Bot_Pan, samu | Produto |
| `implemente` | samu-operacional | Produto (dispatcher local) |
| `registrar-tentativa` | Bot_Pan | Produto |
| `revisar-docs` | Bot_Pan | Produto |
| `ricardizar` | Bot_Pan | Produto; corrigir `Skill.md`→`SKILL.md` |
| `commit-skill` | mev_v3, Barra | Descartar (substituida por `commit`) |
| `USABILIDADE_MEV.md` | mev_v3 | Produto (fora de skills/) |
| `CATALOGO_IMPORTACAO.md` | Barra | Produto (fora de skills/) |

## Agentes

| Agente | Origem | Destino | Nome final `.cursor/agents/` |
|--------|--------|---------|------------------------------|
| `glpi-orchestrator` | kit GLPI | Reescrever | `glpi-orquestrador.md` |
| `glpi-auditor` | kit GLPI | Reescrever | `glpi-auditor.md` |
| `glpi-migrator` | kit GLPI | Reescrever | `glpi-migrador.md` |
| `glpi-scribe` | kit GLPI | Reescrever | `glpi-escriba.md` |
| `orquestrador-hexagonal` | template | Reescrever | `orquestrador-hexagonal.md` |
| `revisor-arquitetura-hexagonal` | template | Reescrever | `revisor-arquitetura-hexagonal.md` |
| `analista-incidentes-integracao` | template | Reescrever | `analista-incidentes-integracao.md` |
| `operador-entrega-controlada` | template | Reescrever | `operador-entrega-controlada.md` |
| `integrador-chatbot-pet` | mev_v3 | Produto | fica no mev_v3 |

Agentes `.agent.md` (Copilot) em `.github/agents/`: **descontinuados**
(nao entram no template novo; permanecem nos consumidores ate o upgrade F4).

## Resumo

- Entram no template: **25 (kit) + 1 (sincronize) + 9 (hexagonal) + config = 36 skills**
- Agentes no template: **8** (4 GLPI + 4 hexagonais), reescritos em `.cursor/agents/*.md`
- Aliases DEPRECATED mantidos: `glpi-followup`, `glpi-project-create`, `glpi-task-upsert`, `glpi_seed_phases`
