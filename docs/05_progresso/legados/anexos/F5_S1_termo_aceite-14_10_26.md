# Termo de aceite — F5.S1 (14/10/2026)

> Plano: [`unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md`](../unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md)
> Versao: `v1.0.0` · Produto: `toolkit-agentes-skills`
> Branch: `integracao/api-vscode-glpi`

O `toolkit-agentes-skills` passa a ser a fonte unica de inicializacao de
repositorios. O `API-VScode-GLPI` permanece como historico.

## Evidencia

| Criterio | Resultado |
|----------|-----------|
| RF1–RF2 catalogo em `.cursor/` | skills e agentes no formato Cursor |
| RF3 symlink | `.github/skills` → `../.cursor/skills` |
| RF4–RF5 CLI e config sem segredo | `tools/glpi/`, presets `generic` e `api-vscode-glpi`; `instance.yaml`, `project.yaml` e `maps/states.json` no `.gitignore` (commit `3b82344`) |
| RF6 bootstrap e upgrade | F3.S2 em repositorio descartavel; F4 nos consumidores |
| RF7 fonte do wrapper | `atualizar-kit` do produto delega a este template |
| RF8–RF10 PT-BR, docs e aliases | gatilhos em portugues; 12 pastas em `docs/`; aliases DEPRECATED mantidos |
| RNF2 lint | `scripts/lint_template.py` exit 0 em 14/10/2026 15:03 |
| RNF3 historico | subtree `f83ff4f`; nada apagado no `API-VScode-GLPI` |
| RNF5 Copilot | `.agent.md` sem manutencao neste kit |
| Versao | `CHANGELOG.md` e tag `v1.0.0` |
| Fonte antiga | README do `API-VScode-GLPI` aponta para este repositorio |

## Fora deste aceite

- F4.S1.P3: follow-up GLPI nao enviado. O chamado 5621 em homologacao nao e deste upgrade.
- chatbot-docs: repositorio inexistente; exclusao registrada no F4.S2.
- Cinco binarios GLPI seguem so como spec (`glpi-commit-harvest`, `glpi-progress-rollup`, `glpi-node-upsert`, `glpi-phase-ensure`, `glpi-migrate-codes`).
- Duracoes no GLPI de producao: somente o projeto 72.

## Aceite

F5 e F5.S1 ficam `[A]`. `accept_ref` deste termo:
`docs/05_progresso/legados/anexos/F5_S1_termo_aceite-14_10_26.md`.
