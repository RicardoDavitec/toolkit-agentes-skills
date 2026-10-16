# toolkit-agentes-skills

**Versao:** [`v1.0.0`](CHANGELOG.md) (14/10/2026). Fonte unica de inicializacao.
O `API-VScode-GLPI` permanece como historico.

Kit reutilizavel de **agentes e skills para Cursor**, com integracao **GLPI**
via API REST (qualquer instancia) e fluxo de documentacao **F/S/P**
(Fase / Sessao-Sprint / Tarefa ancorada em commit). Unifica o antigo
`pmf-dev-kit` (API-VScode-GLPI) e o template hexagonal.

## Conteudo

- `.cursor/skills/`: **catalogo canonico** de skills — operacao git,
  sessao, backup, GLPI e fluxo hexagonal. Convenção de códigos:
  `convencao-codigos-glpi` (C e R só no cabeçalho; itens em `F#.S#.P#`).
- `.cursor/agents/`: **catalogo canonico** de agentes (8) — 4 GLPI
  (`glpi-orquestrador`, `glpi-auditor`, `glpi-migrador`, `glpi-escriba`) +
  4 hexagonais.
- `.github/skills`: **symlink** para `../.cursor/skills` (compatibilidade;
  nunca editar por aqui).
- `tools/glpi/`: CLI GLPI (`bin/glpi-*`) vendorizado nos consumidores.
- `.glpi/`: configuracao por produto — **sem segredos** no template
  (`*.example`, `presets/`, `templates/`, `model.defaults.yaml`).
- `scripts/`: `bootstrap-into.sh`, `upgrade-into.sh`, `install-glpi.sh`,
  `install_glpi.py`, `atualizar-kit` (+`.py`).
- `docs/06_glpi/`: manual da integracao GLPI.
- `docs/guia_agentes_skills_ptbr.md`: guia de uso em Portugues-BR.

## Precedencia (fonte unica)

1. **Canonico**: `.cursor/skills/<nome>/SKILL.md` e `.cursor/agents/<nome>.md`.
2. `.github/skills` e apenas um link — edicoes sempre em `.cursor/`.
3. Agentes `.agent.md` (Copilot) foram **descontinuados** neste kit.

## Setup rapido

### Projeto novo (bootstrap)

```bash
./scripts/bootstrap-into.sh --target=/caminho/do/projeto
```

### Projeto existente (upgrade)

```bash
./scripts/upgrade-into.sh --target=. --apply
```

Os scripts copiam `.cursor/skills` e `.cursor/agents`, criam o symlink
`.github/skills -> ../.cursor/skills` e preservam a camada do produto
(skills proprias, `.glpi/project.yaml`, `workspace.yaml`, estados).

## Arvore padrao de docs

- `docs/00_visao_geral` · `01_requisitos` · `02_arquitetura` ·
  `03_implementacao` · `04_operacao`
- `docs/05_progresso/{planos_ativos,geral,legados,pendencias,historico}`
- `docs/06_glpi`

## Modelo F/S/P

```text
Projeto -> F (fase) -> S (sessao/sprint/semana) -> P (tarefa ~2h, ancorada em commit)
F1 Planejamento · F2 Implementacao · F3 Testes Internos · F4 Homologacao · F5 Aprovacao
Estados (papeis, nao IDs): todo -> doing -> testing -> done -> closed
Marcadores: [ ] [~] [t] [x] [A]
```

## Segredos

Nunca no template: tokens, `.env`, `instance.yaml`, `project.yaml`,
`maps/states.json`. O `.gitignore` ja cobre; o lint de catalogo bloqueia.

## Observacoes

- Funciona em qualquer projeto (hexagonal ou nao); as skills operacionais
  valem para todos, os agentes/skills hexagonais sao opcionais.
- Identificadores sem acento (compatibilidade de tooling); textos e gatilhos
  em Portugues-BR.
- Symlink `.github/skills`: no Windows nativo exige Modo de Desenvolvedor +
  `core.symlinks=true`; em WSL/Linux/macOS funciona nativamente.
