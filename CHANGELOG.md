# Changelog

## v1.0.0 — 2026-10-14

Template unico de inicializacao. O `API-VScode-GLPI` (`pmf-dev-kit`) deixa de
ser a fonte; o historico dele permanece no repositorio de origem.

### Adicionado

- Catalogo canonico em `.cursor/skills` e `.cursor/agents`.
- `.github/skills` como symlink para `../.cursor/skills`.
- CLI GLPI em `tools/glpi/`, presets `generic` e `api-vscode-glpi`, sem segredos.
- `scripts/bootstrap-into.sh` e `scripts/upgrade-into.sh`, com backup e
  preservacao da camada do produto. O wrapper do produto aponta para este template.
- Arvore `docs/` de `00_visao_geral` a `11_ia`, com `07_doc_academica/livros`.
- Lint de catalogo, CI e `glpi-tree-validate` no exemplo.
- `glpi-temporal-fill`: datas e duracoes da ProjectTask. Aplicado ao projeto 72
  em `suporte.franca.sp.gov.br`.

### Descontinuado

- Agentes `.agent.md` (Copilot), sem conversao automatica.
- `API-VScode-GLPI` como fonte de bootstrap e upgrade. O README de la aponta
  para este repositorio. Nenhum arquivo de la foi apagado.

## v0.1.0 — 2026-04-03

Baseline inicial do toolkit (tag `v0.1.0`, commit `f54ade4`).
