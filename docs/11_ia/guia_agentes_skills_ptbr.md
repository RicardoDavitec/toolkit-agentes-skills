---
id: GUI-agentes-skills
tipo: guia
titulo: Guia de uso de agentes e skills (PT-BR)
status: em_revisao
versao: 1.1.0
data: 2026-11-09
autor: Ricardo
classificacao: publico
---

# Guia de uso de agentes e skills (PT-BR)

> Atualizado em 09/11/2026. Canônico: `.cursor/` (unificação com o kit GLPI).

Este guia descreve como usar os agentes e skills do **toolkit-agentes-skills**: fluxo de desenvolvimento com Cursor, integração GLPI (modelo F/S/P), documentação padronizada e operação segura com rastreabilidade.

Para **como escrever a documentação** (nomes, front matter, fases, commits), veja o padrão em `docs/12_padrao_documentacao/` (guias G01 a G14). O G14 trata do catálogo de agentes e skills de documentação; este guia trata do uso geral.

## Fonte única (onde editar)

| O que | Canônico | Atalho |
|-------|----------|--------|
| Skills | `.cursor/skills/<nome>/SKILL.md` | `.github/skills` (symlink) |
| Agentes | `.cursor/agents/<nome>.md` | — |
| Regras do Cursor | `.cursor/rules/*.mdc` | — |

Nunca edite pelo atalho `.github/skills`. Agentes `.agent.md` (Copilot) foram descontinuados.

## Endpoints operacionais (configuração central)

- Arquivo: `.cursor/skills/config/endpoints_operacionais.json`
- Objetivo: destinos padrão e políticas consumidas por skills e agentes.
- Blocos previstos: `backup` (destino por SO, fallback, formato de nome), `sessao` (pasta de histórico, formato, título) e `seguranca` (roots permitidos).
- Pasta do registro diário: `docs/05_progresso/geral` (chave `sessao.historico_relativo_repo`).

> Conferir o JSON do projeto: os valores de backup abaixo são os do padrão anterior e podem estar vazios na sua cópia.

Padrão de backup:

- Windows: `E:/VSCode-bkp`
- Linux/WSL: `/mnt/e/VSCode-bkp`
- Darwin: `/Volumes/VSCode-bkp`
- Estrutura: `<destino>/<nome-do-projeto>/<commit>_<DD-MM-YY_hh-mm>.tar.gz`
- Integridade: `<arquivo>.tar.gz.SHA256`

## Catálogo

### Agentes GLPI (`.cursor/agents/`)

| Agente | Quando acionar | Escreve no GLPI? |
|--------|----------------|------------------|
| `glpi-orquestrador` | sincronizar repo <-> GLPI (cadeia completa) | sim, com confirmação |
| `glpi-auditor` | auditar / CI / status real | **nunca** |
| `glpi-migrador` | migrar v1 (S/P) -> v2 (F/S/P), uso único | sim, confirmação dupla |
| `glpi-escriba` | planos, commits, sessões, pendências | só em `docs/` |

### Agentes de documentação (`.cursor/agents/`)

Todos escrevem **somente em `docs/`**. Não alteram planos (isso é do `glpi-escriba`).

| Agente | Fase | Quando acionar |
|--------|------|----------------|
| `doc-arquiteto` | F1 | requisitos, regras de negócio, arquitetura, ADR |
| `doc-dados-lgpd` | todas | banco de dados, ER, dicionário, inventário LGPD |
| `doc-revisor` | F3 e F4 | plano de testes, ata de homologação, rastreabilidade, gate de fase |

### Agentes hexagonais (`.cursor/agents/`)

- `orquestrador-hexagonal` — agente principal do fluxo hexagonal
- `revisor-arquitetura-hexagonal` — boundaries, portas, adaptadores (leitura)
- `analista-incidentes-integracao` — Twilio, Selenium, Sheets, envios
- `operador-entrega-controlada` — implementação com mudança mínima

### Skills operacionais (`.cursor/skills/`)

| Grupo | Skills |
|-------|--------|
| Git/remoto | `commit`, `exporte` (push), `importe` (pull), `atualizar` (sincronizar 1 remote), `sincronize` (equalizar origin e espelhos `github`/`gitness`, se existirem) |
| Sessão/planos | `documentar`, `documente-o-plano`, `encerrar-sessao`, `oncoto-oncovo`, `planeje-a-semana`, `inserir-pendencia` |
| Documentação (padrão 12) | `doc-novo`, `doc-adr`, `doc-dados-schema`, `doc-lgpd-inventario`, `doc-rastreabilidade`, `doc-gate-fase`, `doc-lint` |
| Backup/kit | `backup`, `atualizar-kit` |
| GLPI | `convencao-codigos-glpi`, `acompanhar-chamado`, `glpi-document-attach`, `glpi-retro-scan`, `glpi-tree-validate`, `glpi-backlog-export`, `glpi-commit-harvest`*, `glpi-progress-rollup`*, `glpi-node-upsert`*, `glpi-phase-ensure`*, `glpi-migrate-codes`* |
| Aliases DEPRECATED | `glpi-followup` (=acompanhar-chamado), `glpi-project-create`, `glpi-task-upsert` (=glpi-node-upsert), `glpi_seed_phases` (=glpi-phase-ensure) |
| Hexagonal | `fluxo-orquestrado-hexagonal`, `guardrails-hexagonal`, `checar-contratos-portas`, `revisar-casos-de-uso`, `operacao-planilha-segura`, `gate-release-hexagonal` |

\* especificação de CLI futuro — a SKILL.md traz nota de status com o equivalente manual executável hoje.

## Como pensar o fluxo

1. Um agente principal orquestra.
2. Skills definem procedimentos reutilizáveis.
3. Subagentes executam partes especializadas quando necessário.

## Fluxos recomendados

### Fluxo GLPI: sincronizar repositório -> GLPI

1. Invoque `glpi-orquestrador`.
2. Ele roda a cadeia em dry-run: harvest -> validate (porteiro) -> phase-ensure -> upsert -> rollup -> followup.
3. Revise a tabela de diff e digite APLICAR para efetivar.

### Fluxo 1: Implementação segura (hexagonal)

1. Invoque `orquestrador-hexagonal` com objetivo claro.
2. Aplique `revisar-casos-de-uso`.
3. Se houver risco de arquitetura, aplique `guardrails-hexagonal`.
4. Implemente com `operador-entrega-controlada`.
5. Finalize com `documentar`.

### Fluxo 2: Incidente de integração

1. Invoque `analista-incidentes-integracao`.
2. Aplique `checar-contratos-portas`.
3. Se envolver planilha, aplique `operacao-planilha-segura`.
4. Gere recomendação de mitigação e correção definitiva.
5. Finalize com `documentar`.

### Fluxo 3: Pré-release

1. Invoque `orquestrador-hexagonal`.
2. Aplique `gate-release-hexagonal`.
3. Resolva pendências apontadas.
4. Encerre com `encerrar-sessao`.
5. Opcional: `backup`.

### Fluxo 4: Documentação por fase

1. **F1:** `doc-arquiteto` para requisitos, arquitetura e ADRs; depois `documente-o-plano` (via `glpi-escriba`) para os planos F/S/P.
2. **F2:** a cada tarefa P, `commit` com o gate de plano. Se o esquema do banco mudou, `doc-dados-lgpd`.
3. **F3:** `doc-revisor` com `doc-rastreabilidade` para a matriz e o plano de testes.
4. **F4:** `doc-revisor` para o roteiro e a ata de homologação.
5. **F5:** runbooks (`doc-novo`, tipo `operacao`) e `doc-gate-fase`.
6. Ao fim de cada sessão: `doc-lint`, `encerrar-sessao` e sincronização com o GLPI.

## Padrão de prompts

Use prompts com 4 blocos: **Objetivo** · **Escopo** · **Restrições** · **Critério de pronto**.

## Convenções de nomeação (PT-BR sem acento nos identificadores)

- Agentes: substantivo + contexto (ex.: `operador-entrega-controlada`).
- Skills: verbo no infinitivo + objeto (ex.: `checar-contratos-portas`).
- Identificadores sem acento; `name` do YAML igual ao nome da pasta.

## Execução rápida de scripts de apoio

```bash
# Lint do catálogo do kit e da documentação
python3 scripts/lint_template.py
python3 scripts/docs/lint_docs.py

# Matriz de rastreabilidade
python3 scripts/docs/gerar_rastreabilidade.py

# Novo documento a partir de modelo
python3 scripts/docs/novo_doc.py adr --titulo "Titulo da decisao" --autor Nome

# Checklist de encerramento
python .cursor/skills/encerrar-sessao/scripts/checklist_encerramento.py --repo .

# Backup por ambiente
python .cursor/skills/backup/scripts/backup_projeto.py

# Conferir se existem (não verificados):
#   .cursor/skills/fluxo-orquestrado-hexagonal/scripts/gerar_checklist_fluxo.py
#   .cursor/skills/documentar/scripts/gerar_resumo_sessao.py
```

## Variáveis de ambiente

- Backup: `BACKUP_DESTINO_<SO>`, `BACKUP_DESTINO_FALLBACK_<SO>`, `BACKUP_ROOT`, `BACKUP_EXCLUDE`, `BACKUP_FORMAT`
- Sessão: `SESSAO_HISTORICO_RELATIVO_REPO`, `SESSAO_FORMATO_NOME_ARQUIVO`, `SESSAO_TITULO_PADRAO`
- Precedência: argumento CLI > variável de ambiente > config central > fallback

Os scripts carregam automaticamente variáveis do `.env` da raiz do repositório (quando `python-dotenv` estiver disponível).
