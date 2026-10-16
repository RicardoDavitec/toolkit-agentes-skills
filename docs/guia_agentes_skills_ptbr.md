# Guia de Uso de Agentes e Skills (PT-BR)

> Atualizado em 14/10/2026 — canonico `.cursor/` (unificacao com o kit GLPI).

Este guia descreve como usar os agentes e skills do **toolkit-agentes-skills**:
fluxo de desenvolvimento com Cursor, integracao GLPI (modelo F/S/P) e
operacao segura com rastreabilidade.

## Fonte unica (onde editar)

| O que | Canonico | Atalho |
|-------|----------|--------|
| Skills | `.cursor/skills/<nome>/SKILL.md` | `.github/skills` (symlink) |
| Agentes | `.cursor/agents/<nome>.md` | — |

Nunca edite pelo atalho `.github/skills`. Agentes `.agent.md` (Copilot) foram
descontinuados.

## Endpoints operacionais (configuracao central)

- Arquivo: `.cursor/skills/config/endpoints_operacionais.json`
- Objetivo: destinos padrao e politicas consumidas por skills e agentes.
- Blocos: `backup` (destino por SO, fallback, formato de nome), `sessao`
  (pasta de historico, formato, titulo), `seguranca` (roots permitidos).

Padrao atual de backup:

- Windows: `E:/VSCode-bkp`
- Linux/WSL: `/mnt/e/VSCode-bkp`
- Darwin: `/Volumes/VSCode-bkp`
- Estrutura: `<destino>/<nome-do-projeto>/<commit>_<DD-MM-YY_hh-mm>.tar.gz`
- Integridade: `<arquivo>.tar.gz.SHA256`

## Catalogo

### Agentes GLPI (`.cursor/agents/`)

| Agente | Quando acionar | Escreve no GLPI? |
|--------|----------------|------------------|
| `glpi-orquestrador` | sincronizar repo <-> GLPI (cadeia completa) | sim, com confirmacao |
| `glpi-auditor` | auditar / CI / status real | **nunca** |
| `glpi-migrador` | migrar v1 (S/P) -> v2 (F/S/P), uso unico | sim, confirmacao dupla |
| `glpi-escriba` | planos, commits, sessoes | so em `docs/` |

### Agentes hexagonais (`.cursor/agents/`)

- `orquestrador-hexagonal` — agente principal do fluxo hexagonal
- `revisor-arquitetura-hexagonal` — boundaries, portas, adaptadores (leitura)
- `analista-incidentes-integracao` — Twilio, Selenium, Sheets, envios
- `operador-entrega-controlada` — implementacao com mudanca minima

### Skills operacionais (`.cursor/skills/`)

| Grupo | Skills |
|-------|--------|
| Git/remoto | `commit`, `exporte` (push), `importe` (pull), `atualizar` (sincronizar 1 remote), `sincronize` (equalizar origin+github) |
| Sessao/docs | `documentar`, `documente-o-plano`, `encerrar-sessao`, `oncoto-oncovo`, `planeje-a-semana`, `inserir-pendencia` |
| Backup/kit | `backup`, `atualizar-kit` |
| GLPI | `convencao-codigos-glpi`, `acompanhar-chamado`, `glpi-document-attach`, `glpi-retro-scan`, `glpi-tree-validate`, `glpi-backlog-export`, `glpi-commit-harvest`*, `glpi-progress-rollup`*, `glpi-node-upsert`*, `glpi-phase-ensure`*, `glpi-migrate-codes`* |
| Aliases DEPRECATED | `glpi-followup` (=acompanhar-chamado), `glpi-project-create`, `glpi-task-upsert` (=glpi-node-upsert), `glpi_seed_phases` (=glpi-phase-ensure) |
| Hexagonal | `fluxo-orquestrado-hexagonal`, `guardrails-hexagonal`, `checar-contratos-portas`, `revisar-casos-de-uso`, `operacao-planilha-segura`, `gate-release-hexagonal` |

\* especificacao de CLI futuro — a SKILL.md traz nota de status com o
equivalente manual executavel hoje.

## Como pensar o fluxo

1. Um agente principal orquestra.
2. Skills definem procedimentos reutilizaveis.
3. Subagentes executam partes especializadas quando necessario.

## Fluxos recomendados

### Fluxo GLPI: sincronizar repositorio -> GLPI

1. Invoque `glpi-orquestrador`.
2. Ele roda a cadeia em dry-run: harvest -> validate (porteiro) ->
   phase-ensure -> upsert -> rollup -> followup.
3. Revise a tabela de diff e digite APLICAR para efetivar.

### Fluxo 1: Implementacao segura (hexagonal)

1. Invoque `orquestrador-hexagonal` com objetivo claro.
2. Aplique `revisar-casos-de-uso`.
3. Se houver risco de arquitetura, aplique `guardrails-hexagonal`.
4. Implemente com `operador-entrega-controlada`.
5. Finalize com `documentar`.

### Fluxo 2: Incidente de integracao

1. Invoque `analista-incidentes-integracao`.
2. Aplique `checar-contratos-portas`.
3. Se envolver planilha, aplique `operacao-planilha-segura`.
4. Gere recomendacao de mitigacao e correcao definitiva.
5. Finalize com `documentar`.

### Fluxo 3: Pre-release

1. Invoque `orquestrador-hexagonal`.
2. Aplique `gate-release-hexagonal`.
3. Resolva pendencias apontadas.
4. Encerre com `encerrar-sessao`.
5. Opcional: `backup`.

## Padrao de prompts

Use prompts com 4 blocos: **Objetivo** · **Escopo** · **Restricoes** ·
**Criterio de pronto**.

## Convencoes de nomeacao (PT-BR sem acento)

- Agentes: substantivo + contexto (ex.: `operador-entrega-controlada`).
- Skills: verbo no infinitivo + objeto (ex.: `checar-contratos-portas`).
- Identificadores sem acento; `name` do YAML igual ao nome da pasta.

## Execucao rapida de scripts de apoio

```bash
# Checklist de fluxo hexagonal
python .cursor/skills/fluxo-orquestrado-hexagonal/scripts/gerar_checklist_fluxo.py

# Resumo de sessao
python .cursor/skills/documentar/scripts/gerar_resumo_sessao.py

# Checklist de encerramento
python .cursor/skills/encerrar-sessao/scripts/checklist_encerramento.py --repo .

# Backup por ambiente
python .cursor/skills/backup/scripts/backup_projeto.py
```

## Variaveis de ambiente

- Backup: `BACKUP_DESTINO_<SO>`, `BACKUP_DESTINO_FALLBACK_<SO>`, `BACKUP_ROOT`,
  `BACKUP_EXCLUDE`, `BACKUP_FORMAT`
- Sessao: `SESSAO_HISTORICO_RELATIVO_REPO`, `SESSAO_FORMATO_NOME_ARQUIVO`,
  `SESSAO_TITULO_PADRAO`
- Precedencia: argumento CLI > variavel de ambiente > config central > fallback

Os scripts carregam automaticamente variaveis do `.env` da raiz do repositorio
(quando `python-dotenv` estiver disponivel).
