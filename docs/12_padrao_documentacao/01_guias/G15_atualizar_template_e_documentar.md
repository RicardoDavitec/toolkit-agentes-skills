---
id: GUI-015
tipo: guia
titulo: Atualizar o template e documentar no projeto
status: rascunho
versao: 0.1.0
data: 2026-11-10
autor: Ricardo
classificacao: publico
---

# G15 – Atualizar o template e documentar no projeto

Dois procedimentos recorrentes em qualquer produto baseado neste kit. Skills: `atualizar-kit`, `documente-o-plano`, `documentar`, `doc-novo`, `doc-lint`, `commit`.

## Procedimento A — Atualizar o template (kit → produto)

### Quando

Há commits novos em `toolkit-agentes-skills`, ou o produto ainda não tem `docs/12_padrao_documentacao/`, skills `doc-*` ou scripts em `scripts/docs/`.

### Passos

1. No produto, confira o caminho do kit em `.glpi/kit.yaml` (`path:`).
2. Dry-run / check:
   ```bash
   ./scripts/atualizar-kit --check-only
   # equivalente a partir do clone do kit:
   python3 /caminho/toolkit-agentes-skills/scripts/atualizar_kit.py \
     --target=/caminho/produto --check-only
   ```
3. Aplicar (perfil `full-skeleton` se já existir `docs/00_visao_geral`):
   ```bash
   ./scripts/atualizar-kit --profile=full-skeleton --yes
   ```
   Por baixo: `upgrade-into.sh --target=... --apply --yes` e, no fim, `scripts/docs/instalar_docs.sh` (`cp -n`, não sobrescreve docs do produto).
4. Atalho só do padrão 12 (sem sync GLPI completo):
   ```bash
   bash /caminho/toolkit-agentes-skills/scripts/docs/instalar_docs.sh /caminho/produto
   # ou, no kit:
   ./scripts/procedimento_atualizar_template.sh --target=/caminho/produto --docs-only
   ```
5. Revisar `git status` no produto. Não commit automático. Commit com a skill `commit` (sem `.keys/`, `.env`, credenciais).
6. Lint: `python3 scripts/docs/lint_docs.py` (0 erros).

### Regras

- `upgrade-into.sh` **não** aceita `--profile` (isso é do `bootstrap-into.sh`). O wrapper `atualizar_kit.py` já traduz para `--target/--apply/--yes`.
- Preserva `.glpi/project.yaml`, `workspace.yaml` e state do produto.
- Skills exclusivas do produto (ex.: `build-*`) não são apagadas (sync granular).

### Script

`scripts/procedimento_atualizar_template.sh` — ver § Scripts.

## Procedimento B — Documentar

### Quando

Abrir plano novo, atualizar progresso, ou criar documento técnico (visão, requisito, ADR, etc.) no padrão 12.

### Passos

| Situação | Skill / comando |
|---|---|
| Plano novo F/S/P | `documente-o-plano` → `docs/05_progresso/planos_ativos/` |
| Atualizar plano/docs existentes | `documentar` |
| Criar doc de apoio | `doc-novo` ou `python3 scripts/docs/novo_doc.py <tipo> --titulo "..."` |
| ADR pontual | `doc-adr` |
| Lint | `doc-lint` ou `python3 scripts/docs/lint_docs.py` |
| Fechar P com código | skill `commit` (plano no mesmo commit) |

Ordem sugerida na F1 (G04): visão → requisitos/RN/glossário → arquitetura → ADRs → dados/LGPD → planos → GLPI (G10).

### Script

```bash
./scripts/docs/procedimento_documentar.sh --ajuda
./scripts/docs/procedimento_documentar.sh lint
./scripts/docs/procedimento_documentar.sh novo requisito --titulo "..."
```

## Scripts

| Script | Papel |
|---|---|
| `scripts/procedimento_atualizar_template.sh` | Check/apply do kit ou só `instalar_docs` |
| `scripts/atualizar-kit` / `atualizar_kit.py` | Sync oficial kit → produto |
| `scripts/upgrade-into.sh` | Camadas K/P/S do GLPI + chama `instalar_docs` |
| `scripts/docs/instalar_docs.sh` | Copia padrão 12, skills `doc-*`, `.vscode` (`cp -n`) |
| `scripts/docs/procedimento_documentar.sh` | Atalhos lint / novo_doc / inventário do fluxo |
| `scripts/docs/novo_doc.py` | Cria arquivo a partir de `02_modelos/` |
| `scripts/docs/lint_docs.py` | Valida front matter e pastas |

## Ver também

- G14 — Cursor, agentes e skills `doc-*`
- G09 — commits e rastreabilidade
- G10 — sincronização GLPI
- `docs/06_glpi/GUIA_USO_INTEGRACAO_VSCODE_GLPI.md` — caminho 2 (projeto em andamento)
