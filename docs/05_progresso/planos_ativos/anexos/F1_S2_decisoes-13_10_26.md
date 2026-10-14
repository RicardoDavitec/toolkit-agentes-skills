# F1.S2 — Decisoes de arquitetura do template (13-14/10/2026)

> Plano: [`unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md`](../unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md)

## F1.S2.P1 — Fonte unica e espelho (decidido 13/10)

- **Canonico**: `.cursor/skills/<nome>/SKILL.md` e `.cursor/agents/<nome>.md`.
- **`.github/skills`**: symlink para `../.cursor/skills` (compatibilidade de
  scripts/docs que citam `.github/skills/...`). Nao e copia; nao e canonico.
- **Agentes `.agent.md` (Copilot)**: descontinuados. Sem link, sem conversao
  automatica — os schemas diferem (`tools`/`agents`/`user-invocable` vs
  frontmatter Cursor). Reescrita manual no F2.S2.P5.
- Windows nativo: link exige Modo de Desenvolvedor + `core.symlinks=true`.
  WSL/Linux/macOS: nativo.

## F1.S2.P2 — Arvore de documentacao unificada (decidido 14/10)

Adotar a **arvore do kit GLPI**:

```text
docs/
  00_visao_geral/  01_requisitos/  02_arquitetura/
  03_implementacao/  04_operacao/
  05_progresso/
    planos_ativos/ (+ anexos/)
    geral/           # SESSAO_* do dia
    legados/         # planos encerrados/substituídos
    pendencias/      # CHECKLIST_PENDENCIAS
    historico/       # (absorvido do 06_progresso/historico)
  06_glpi/           # manuais e hierarquia F/S/P (vem do kit)
```

- `docs/06_progresso/` do template e **absorvido**: `historico/` ja movido
  para `05_progresso/historico/` (14/10).
- `endpoints_operacionais.json` e skill `documentar` apontam para
  `05_progresso/geral` (sessoes) e `05_progresso/historico`.

## F1.S2.P3 — Estrategia de importacao com historico (decidido 14/10)

Metodo: **`git subtree add --prefix=_import/kit-glpi`** em branch
`integracao/api-vscode-glpi`, seguido de movimentacao **arquivo a arquivo**
(`git mv`) para os destinos canonicos, e remocao do prefixo ao final.

Justificativa: os destinos canonicos (`.cursor/skills`, `.cursor/agents`,
`tools/glpi`, `.glpi`, `docs/06_glpi`) **nao existem** no template — logo
nao ha conflito de merge. As fusoes de conteudo (`backup`, `documentar`,
`encerrar-sessao`, `atualizar`+`sincronize`) sao editoriais, feitas a mao,
arquivo a arquivo, antes de qualquer commit da versao unificada.

Regras obrigatorias:

- Proibido `-X union` ou "aceitar ambos" (causa dos defeitos do Bot_Pan).
- Gate pre-commit: `rg -n '^(<{7}|={7}|>{7})'` sem resultado e lint YAML das
  skills sem erro.

## F1.S2.P4 — Glossario PT-BR (decidido 14/10)

| Item | Decisao |
|------|---------|
| Identificadores de skills | **Manter os atuais** — ja sao PT-BR na maioria (`acompanhar-chamado`, `documente-o-plano`, `exporte`, `importe`); `glpi-*` e prefixo de programa (como a CLI). Renomear quebraria scripts e habitos |
| Identificadores de agentes GLPI | Traduzir: `glpi-orchestrator`→`glpi-orquestrador`, `glpi-migrator`→`glpi-migrador`, `glpi-scribe`→`glpi-escriba`, `glpi-auditor`→`glpi-auditor` |
| `description` e gatilhos | PT-BR, sem acento nos identificadores; "Use em ..." obrigatorio |
| Aliases DEPRECATED | Manter (`glpi-followup`, `glpi-project-create`, `glpi-task-upsert`, `glpi_seed_phases`) |
| Chaves de protocolo GLPI | **Nao traduzir**: `todo`, `doing`, `testing`, `done`, `closed` (papeis semanticos usados pelo CLI) |
| Rotulos humanos de estado | PT-BR: `NOVO`, `EM ATENDIMENTO`, `PENDENTE`, `SOLUCIONADO`, `FECHADO` (ja em `.glpi/agenda.yaml`) |
| Titulos de chamados GLPI | Padrao `Modulo-Fase-Pacote-acao` em PT-BR |
| Fases F1..F5 | `Planejamento`, `Implementacao`, `Testes Internos`, `Homologacao`, `Aprovacao` |

## F1.S2.P5 — Requisitos do template

Ver `docs/01_requisitos/README.md` (preenchido em 14/10).
