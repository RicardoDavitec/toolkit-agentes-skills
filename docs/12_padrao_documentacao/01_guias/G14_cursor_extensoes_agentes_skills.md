---
id: GUI-014
tipo: guia
titulo: Cursor, extensões, agentes e skills
status: rascunho
versao: 0.3.0
data: 2026-11-10
autor: Ricardo
classificacao: publico
---
# G14 – Cursor, extensões, agentes e skills

## 1. Extensões recomendadas

Arquivo `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "yzhang.markdown-all-in-one",
    "davidanson.vscode-markdownlint",
    "bierner.markdown-mermaid",
    "prisma.prisma",
    "redhat.vscode-yaml",
    "streetsidesoftware.code-spell-checker",
    "streetsidesoftware.code-spell-checker-portuguese-brazilian",
    "gruntfuggly.todo-tree",
    "eamodio.gitlens",
    "ms-python.python",
    "editorconfig.editorconfig"
  ]
}
```

Opcionais: `jebbs.plantuml` (exige Java e Graphviz) e `hediet.vscode-drawio`.

O Cursor usa o registro **Open VSX**. Algumas extensões podem faltar ou estar em versão antiga; confira ao instalar.

## 2. Configurações (`.vscode/settings.json`)

```json
{
  "files.encoding": "utf8",
  "files.eol": "\n",
  "[markdown]": { "editor.wordWrap": "on" },
  "cSpell.language": "en,pt-BR"
}
```

## 3. Onde fica cada coisa

| Item | Local | Quem escreve |
|---|---|---|
| Documentos | `docs/` | Humanos e agentes de documentação |
| Agentes | `.cursor/agents/*.md` | Mantenedor do kit |
| Skills | `.cursor/skills/<nome>/SKILL.md` | Mantenedor do kit |
| Configuração das skills | `.cursor/skills/config/endpoints_operacionais.json` | Mantenedor do kit |
| Regras do Cursor | `.cursor/rules/*.mdc` | Mantenedor do kit |
| Scripts de documentação | `scripts/docs/` | Mantenedor do kit |
| Modelos de documento | `docs/12_padrao_documentacao/02_modelos/` | Mantenedor do kit |
| Pipeline de CI | `.github/workflows/ci.yml` | Mantenedor do kit |

Agentes de documentação gravam **somente em** `docs/`, como o `glpi-escriba`.

## 4. Regras que os lints cobram

### 4.1 `scripts/lint_template.py` (catálogo do kit)

**Skill** (`.cursor/skills/<nome>/SKILL.md`):

- Front matter YAML válido, com `name` e `description`.
- `name` **igual** ao nome da pasta.
- `description` com traços de português (palavras como "de", "para", "com", "plano", "use", "quando", "em").

**Agente** (`.cursor/agents/<nome>.md`): front matter YAML válido com `description`.

**Geral:** nenhum marcador de conflito git e nenhum segredo com aparência real.

Duas armadilhas:

- Uma linha com exatamente `=======` conta como conflito git. Em Markdown, use `#` para títulos e nunca sublinhado com `=`.
- Texto como `api_key: <20 ou mais caracteres>` é bloqueado fora de `docs/06_glpi/` e de arquivos `.example`. Em documentos, escreva `<TOKEN>`.

### 4.2 `scripts/docs/lint_docs.py` (documentos de apoio)

Valida front matter, tipo, prefixo do id, status, classificação, formato do `codigo`, seções obrigatórias por tipo e nomes de pasta. Ignora planos, anexos, `SESSAO_*`, pendências, `legados/`, `06_glpi/` e `02_modelos/`. Detalhes no G03 §5.

## 5. Padrão de descrição

Descrição boa diz **o que faz** e **quando acionar**, com frases que o usuário diria:

```yaml
description: >-
  Cria ADR (registro de decisao de arquitetura) a partir de uma decisao
  discutida. Use em registre a decisao, criar ADR, documentar escolha tecnica.
```

## 6. Catálogo de documentação

### 6.1 Agentes

| Agente | Fase | Escreve em | Papel |
|---|---|---|---|
| `doc-arquiteto` | F1 | `00_visao_geral`, `01_requisitos`, `02_arquitetura` | Requisitos, arquitetura, ADRs |
| `doc-dados-lgpd` | Todas | `09_dados_e_tabelas` | Dicionário, ER, inventário LGPD |
| `doc-revisor` | F3, F4 | `03_implementacao`, `05_progresso/geral` | Lint, rastreabilidade, testes, ata, relatório de fase |
| `glpi-escriba` | Todas | `docs/05_progresso/` | Planos, commit, sessão, pendência (já existia) |

### 6.2 Skills

| Skill | Papel |
|---|---|
| `doc-novo` | Cria documento a partir do modelo |
| `doc-adr` | Registra uma decisão de arquitetura |
| `doc-dados-schema` | Regenera ER, dicionário e enums |
| `doc-lgpd-inventario` | Cria e atualiza o inventário de dados pessoais |
| `doc-rastreabilidade` | Gera a matriz requisito, tarefa, commit, teste |
| `doc-gate-fase` | Confere o critério de saída e emite o relatório de fase |
| `doc-lint` | Roda os lints e resume os achados |
| `atualizar-kit` | Sincroniza o kit no produto (procedimento A, G15) |
| `documente-o-plano` / `documentar` | Plano F/S/P e atualização de docs (procedimento B, G15) |

### 6.3 Quem usa o quê (regra `.cursor/rules/documentacao.mdc`)

| Fase ou tarefa | Agente |
|---|---|
| F1: requisitos, arquitetura, ADR | `doc-arquiteto` |
| Qualquer fase: banco, ER, LGPD | `doc-dados-lgpd` |
| F3 e F4: testes, homologação, revisão, gate | `doc-revisor` |
| Plano, commit, sessão, pendência | `glpi-escriba` |

Os agentes e skills que já existiam (`glpi-escriba`, `documente-o-plano`, `commit`, `encerrar-sessao`, `inserir-pendencia`) **não** são duplicados. Os novos os chamam.

> O agente `glpi-orquestrador` coordena a cadeia de sincronização com o GLPI (harvest, validate, phase-ensure, upsert, rollup e followup, em dry-run, com confirmação `APLICAR`). Ele **não** distribui trabalho entre os agentes `doc-`*. Guia geral de uso: `docs/11_ia/guia_agentes_skills_ptbr.md`.

## 7. Instalação e integração

1. `scripts/docs/instalar_docs.sh [diretório]` copia para o projeto `.vscode/`, a regra do Cursor, os agentes, as skills, os scripts de documentação e o padrão `docs/12_padrao_documentacao/` (guias, modelos, exemplos), e cria as pastas vazias de `docs/`. Nunca sobrescreve arquivo existente (`cp -n`).
2. `bootstrap-into.sh` chama `instalar_docs.sh` ao final (todos os perfis). No perfil `full-skeleton`, também faz `rsync` de `docs/12_padrao_documentacao/` junto com `00`–`11`.
3. `upgrade-into.sh` chama `instalar_docs.sh` ao final: em dry-run só anuncia; com `--apply` executa (respeita `cp -n` e `GLPI_DRY_RUN=1`).
4. O `.github/workflows/ci.yml` já roda `lint_template.py` e `lint_docs.py`. O job de documentação só executa se `scripts/docs/lint_docs.py` existir.
5. Antes de publicar uma nova versão do template: `python3 scripts/lint_template.py` e `python3 scripts/docs/lint_docs.py`.

## 8. Rotina do desenvolvedor no Cursor

1. Abrir o plano da fase e escolher a P.
2. Pedir ao agente da tabela 6.3, citando o código `F#.S#.P#`.
3. Revisar o diff, principalmente o que foi escrito em `docs/`.
4. Rodar a skill `doc-lint`.
5. Commitar com a skill `commit` (G09), no mesmo `git add` do plano.
6. Encerrar a sessão com `encerrar-sessao` e sincronizar com o GLPI (G10).
