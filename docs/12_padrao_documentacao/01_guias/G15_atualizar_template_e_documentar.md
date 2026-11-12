---
id: GUI-015
tipo: guia
titulo: Atualizar o template e documentar no projeto
status: rascunho
versao: 0.4.0
data: 2026-11-12
autor: Ricardo
classificacao: publico
---

# G15 – Atualizar o template e documentar no projeto

Três procedimentos recorrentes em qualquer produto baseado neste kit. Skills: `atualizar-kit`, `documente-o-plano`, `documentar`, `doc-novo`, `doc-dados-schema`, `doc-lgpd-inventario`, `doc-lint`, `commit`, `sincronize`.

## Procedimento A — Atualizar o template (kit → produto)

### Quando

Há commits novos em `toolkit-agentes-skills`, ou o produto ainda não tem `docs/12_padrao_documentacao/`, skills `doc-*` ou scripts em `scripts/docs/`.

### Pré-requisito: branches atualizadas

Antes de copiar arquivos, `atualizar_kit.py` faz `git fetch` no **kit** e no **destino** (`origin`; também `github`/`gitness` se existirem) e **recusa** o apply se alguma branch estiver atrasada.

| Situação | Ação |
|---|---|
| Destino atrasado do remoto | Skill `sincronize` ou `git pull --ff-only` no produto; depois repetir |
| Kit atrasado de `origin` | `git pull --ff-only` no kit, ou `--pull-kit` (working tree limpa) |
| Destino só à frente do remoto | OK aplicar; depois `commit` + `sincronize`/push |
| Working tree suja | Aviso; upgrade segue — separe commits (kit vs WIP) |
| Emergência | `--allow-behind` (não use no fluxo normal) |

### Passos

1. No produto, confira o caminho do kit em `.glpi/kit.yaml` (`path:`).
2. Dry-run / check (mostra behind/ahead de kit e destino):
   ```bash
   ./scripts/atualizar-kit --check-only
   # equivalente a partir do clone do kit:
   python3 /caminho/toolkit-agentes-skills/scripts/atualizar_kit.py \
     --target=/caminho/produto --check-only
   ```
3. Se o check acusar destino/kit atrasados: equalize primeiro (skill `sincronize`).
4. Aplicar (perfil `full-skeleton` se já existir `docs/00_visao_geral`):
   ```bash
   ./scripts/atualizar-kit --profile=full-skeleton --yes
   ```
   Por baixo: `upgrade-into.sh --target=... --apply --yes` e, no fim, `scripts/docs/instalar_docs.sh` (`cp -n`, não sobrescreve docs do produto).
5. Atalho só do padrão 12 (sem sync GLPI completo):
   ```bash
   bash /caminho/toolkit-agentes-skills/scripts/docs/instalar_docs.sh /caminho/produto
   # ou, no kit:
   ./scripts/procedimento_atualizar_template.sh --target=/caminho/produto --docs-only
   ```
6. Revisar `git status` no produto. Não commit automático. Commit com a skill `commit` (sem `.keys/`, `.env`, credenciais).
7. Equalizar remotos do produto com skill `sincronize` (origin; e github/gitness se existirem).
8. Lint no produto, os dois (skill `doc-lint`). `lint_docs.py` valida `docs/`. `lint_template.py` valida o catálogo `.cursor` e o padrão de segredo na raiz do alvo. Os dois com 0 erros:
   ```bash
   python3 scripts/docs/lint_docs.py
   python3 scripts/lint_template.py
   ```
   O `upgrade` copia `scripts/lint_template.py`. Se o arquivo ainda não estiver no produto, rode o do kit apontando a raiz: `python3 /caminho/toolkit-agentes-skills/scripts/lint_template.py /caminho/produto`.
9. Se o produto tiver `schema.prisma`, a arquitetura de dados segue o Procedimento C (o `cp` do template não gera o extrato).

### Regras

- `upgrade-into.sh` **não** aceita `--profile` (isso é do `bootstrap-into.sh`). O wrapper `atualizar_kit.py` já traduz para `--target/--apply/--yes`.
- Preserva `.glpi/project.yaml`, `workspace.yaml` e state do produto.
- Skills exclusivas do produto (ex.: `build-*`) não são apagadas (sync granular).

### Script

`scripts/procedimento_atualizar_template.sh` — ver § Scripts.

## Procedimento B — Documentar

### Quando

Abrir plano novo, atualizar progresso, ou criar documento técnico no padrão 12.

O B diz **qual** documento abrir e **qual** comando usar. O texto de cada fase continua no guia: F1 no G04, dados no G11–G13, testes no G06, homologação no G07, runbook no G08.

### O que produzir

Um arquivo por item, via `doc-novo`. O que a fonte (chamado, legado, pendência, código) não sustenta fica `A DEFINIR`. Placeholder, pasta vazia e legado sem prefixo contam como ausência.

| Documento | Guia | Situação no alvo | Ação |
|---|---|---|---|
| `vis_*` | G04 | `00_visao_geral/` só com placeholder, ou texto sem prefixo `vis_` | Visão com o objetivo do chamado |
| C4 nível 1 | G13 | A visão não tem o contexto; o Mermaid está só noutro doc (ex.: ARQ-001) | `flowchart` de contexto dentro da `vis_*` |
| `req_*` | G04 | Catálogo ausente; o requisito vive em legado (ex.: `REGRAS_de_negocio_SAMU.md`, dezenas de itens) | Um `req_` por requisito que a fonte sustenta |
| `rn_*` | G04 | A regra está numa pendência e ainda sem arquivo (ex.: RN-044 camuflagem, `PEND-20261104-001`) | `rn_` com enunciado e fonte na pendência ou no legado. A pendência continua no checklist |
| `adr_*` | G04, G09 | `docs/02_arquitetura/adr/` vazia | Um ADR por decisão que mude custo, segurança ou prazo |
| `tst_*` | G06 | `03_implementacao/testes/` sem documento numerado | Plano de testes; cada caso cita um REQ ou RN |
| `hml_*` | G07 | `03_implementacao/homologacao/` sem documento numerado | Roteiro de homologação ligado aos REQ |
| `ops_*` | G08 | Arquivos em `04_operacao/` sem prefixo `ops_` nem front matter | Um `ops_` canônico por runbook vigente. O arquivo antigo permanece até o conteúdo passar |

Esboço de `tst_*` e `hml_*` já entra na F1 (G04, passo 8). O plano executado é da F3; a ata com o usuário é da F4.

### Passos

| Situação | Skill / comando |
|---|---|
| Plano novo F/S/P | `documente-o-plano` → `docs/05_progresso/planos_ativos/` |
| Atualizar plano/docs existentes | `documentar` |
| Criar doc de apoio | `doc-novo` ou `python3 scripts/docs/novo_doc.py <tipo> --titulo "..."` |
| ADR pontual | `doc-adr` |
| Há `schema.prisma` | Procedimento C — `./scripts/docs/procedimento_documentar.sh dados` |
| Lint | `doc-lint` — `lint_docs.py` e `lint_template.py` (`procedimento_documentar.sh lint`) |
| Fechar P com código | skill `commit` (plano no mesmo commit) |

Ordem sugerida na F1 (G04): visão → requisitos/RN/glossário → arquitetura → ADRs → dados/LGPD → planos → GLPI (G10).

### Script

```bash
./scripts/docs/procedimento_documentar.sh --ajuda
./scripts/docs/procedimento_documentar.sh lint
./scripts/docs/procedimento_documentar.sh novo requisito --titulo "..."
./scripts/docs/procedimento_documentar.sh dados
```

## Procedimento C — Arquitetura de dados (extrato Prisma e correlatos)

### Quando

Entra somente se o projeto alvo tiver ao menos um `schema.prisma` fora de `node_modules`. Sem esse arquivo, o procedimento é omitido.

Rode depois do Procedimento A (o padrão 12 já está no produto) e junto do Procedimento B, na ordem da F1: dados e LGPD vêm depois da arquitetura e dos ADRs (G04, G11, G12).

### O que documentar

| Peça | Destino | Origem |
|---|---|---|
| Extrato ER | `docs/09_dados_e_tabelas/er/` | `schema.prisma` via `prisma-markdown` |
| Dicionário | `docs/09_dados_e_tabelas/dicionario/dic_<tabela>.md` | Extrato + curadoria (`MOD_dicionario_dados`) |
| Enums | `docs/09_dados_e_tabelas/enums/` | `enum` do schema, com o significado operacional |
| LGPD | `docs/09_dados_e_tabelas/lgpd/` | Candidato no schema (`/// @pii`, `/// @sens`); curadoria e base legal no G12 |
| Linhagem | `docs/09_dados_e_tabelas/linhagem/` | Integrações que leem ou gravam essas tabelas |

As pastas `prisma/migrations/` ao lado do schema são fonte para conferir o extrato. O SQL da migração permanece no Prisma.

### Passos

1. Localizar os schemas e gerar o extrato:
   ```bash
   ./scripts/docs/procedimento_documentar.sh dados
   # um schema só:
   ./scripts/docs/gerar_dados_prisma.sh apps/backend/prisma/schema.prisma
   ```
2. Sem `schema.prisma`: o comando informa a omissão e termina com sucesso.
3. Exit 2: o schema ainda não declara `generator` com `prisma-markdown`. O script mostra o bloco com `output` **relativo ao arquivo do schema**, apontando para `docs/09_dados_e_tabelas/er/ER.md`. Em monorepo (`apps/backend/prisma/schema.prisma`) esse relativo sobe até a raiz do produto. A pessoa instala `prisma-markdown` e cola o bloco uma vez; o fluxo automático deixa o schema intacto. Repetir o passo 1 em seguida.
4. Com o generate concluído: revisar `er/ER.md`. Acima de cerca de 25 entidades, dividir o diagrama por módulo (G11).
5. Criar ou atualizar `dic_<tabela>.md` só das tabelas novas ou alteradas. Descrição, nulabilidade e dado pessoal saem do schema. Campo sem `///` fica `A DEFINIR`.
6. Correlatos, só com evidência no schema, na migração ou em documento já existente:
   - `enums/`: cada valor e o que significa na operação.
   - `lgpd/`: inventário curado (`doc-lgpd-inventario`, G12). Nome de campo e `/// @pii` só marcam candidato. Finalidade, base legal, retenção e acesso entram quando houver fonte (documento, chamado ou encarregado). Sem fonte, a célula fica `A definir`. O RIPD formal (G12 §5) é ADR quando o critério bater; este passo não redige o RIPD.
   - `linhagem/`: origem e destino quando houver integração nomeada (API, fila, outro banco).
7. Dívida técnica no dicionário: relação sem `@relation`, `String` que funciona como enum, JSON sem exemplo.
8. Lint de novo, os dois do passo 8 do Procedimento A (0 erros).

### Regras

- `schema.prisma`, migrations e seed ficam fora de `docs/`. Este procedimento não os edita.
- O `output` do gerador é relativo à pasta do schema, não à raiz do repositório.
- Sem segredo e sem dado pessoal real nos exemplos do dicionário e do inventário.
- Contar modelos e enums com um comando sobre o schema. A cobertura $$C_{doc}$$ está no G11.

### Script

`scripts/docs/gerar_dados_prisma.sh` gera o extrato. `procedimento_documentar.sh dados` acha os `schema.prisma` do alvo e chama esse script. A curadoria dos correlatos é a skill `doc-dados-schema`.

## Scripts

| Script | Papel |
|---|---|
| `scripts/procedimento_atualizar_template.sh` | Check/apply do kit ou só `instalar_docs` |
| `scripts/atualizar-kit` / `atualizar_kit.py` | Sync oficial kit → produto |
| `scripts/upgrade-into.sh` | Camadas K/P/S do GLPI + chama `instalar_docs` |
| `scripts/docs/instalar_docs.sh` | Copia padrão 12, skills `doc-*`, `.vscode` (`cp -n`) |
| `scripts/docs/procedimento_documentar.sh` | Atalhos lint / novo_doc / dados / inventário do fluxo |
| `scripts/docs/novo_doc.py` | Cria arquivo a partir de `02_modelos/` |
| `scripts/docs/gerar_dados_prisma.sh` | Extrato ER a partir de `schema.prisma`, se o gerador já estiver no schema |
| `scripts/docs/lint_docs.py` | Valida front matter e pastas |
| `scripts/lint_template.py` | Catálogo `.cursor` e padrão de segredo (Procedimento A) |

## Ver também

- G04 — fase F1 (visão, requisitos, ADR, esboço de teste e homologação)
- G06 — testes (`tst_*`)
- G07 — homologação (`hml_*`)
- G08 — runbooks (`ops_*`)
- G11 — dados, ER e dicionário
- G12 — LGPD e classificação
- G13 — diagramas, inclusive C4 nível 1
- G14 — Cursor, agentes e skills `doc-*`
- G09 — commits e rastreabilidade
- G10 — sincronização GLPI
- `docs/06_glpi/GUIA_USO_INTEGRACAO_VSCODE_GLPI.md` — caminho 2 (projeto em andamento)
