# Plano: Unificacao do template toolkit-agentes-skills com API-VScode-GLPI (canonico .cursor)

> Criado: 13/10/2026 14:37 · Fase principal: `F1` · Produto: `toolkit-agentes-skills`
> Arquivo: `unificacao_template_kit_glpi_cursor_canonico-13_10_26-14_37.md`
> Substitui: `unificacao_template_kit_glpi-12_10_26-10_40.md` (movido para legados neste ciclo)
> Estado: **planejado**

## Objetivo

Tornar o `toolkit-agentes-skills` o **unico template de inicializacao** de
repositorios de projeto, incorporando o conteudo do `API-VScode-GLPI`
(`pmf-dev-kit` no Gitness: CLI GLPI, configuracao `.glpi/`, skills e agentes
GLPI, scripts de bootstrap/upgrade). Resultado esperado:

- skills e agentes no padrao **F/S/P versao longa**;
- **uma fonte unica**: skills em `.cursor/skills/<nome>/SKILL.md`, agentes em
  `.cursor/agents/<nome>.md`;
- `.github/skills` existe apenas como **link de compatibilidade** apontando
  para `.cursor/skills` (nao e o canonico); agentes `.github/agents/*.agent.md`
  (Copilot) sao **descontinuados**, pois o Copilot deixa de ser alvo deste kit;
- nomes, descricoes, palavras-chave de acionamento, tags e rotulos de chamados
  GLPI **em portugues do Brasil** (identificadores sem acento);
- projetos consumidores atualizados a partir do template, sem perda de
  historico nem de customizacoes locais.

## Motivacao (evidencia)

No Bot_Pan, o commit `dcc7a47` (06/10/2026, merge de `api-vscode-glpi/main`)
deixou 13 skills com duas versoes coladas (S/P curta + F/S/P longa), 5 delas
com cabecalho YAML invalido, e 7 arquivos com marcadores de conflito. Alem
disso, `.github/skills` e `.cursor/skills` divergiram (37 x 27 no Bot_Pan,
33 x 23 no samu-operacional). O Cursor **le** `.cursor/skills` e
`.cursor/agents`; nesta estacao o catalogo pessoal fica em `~/.cursor/skills`.
Com a saida do Copilot do fluxo, o default passa a ser o que o Cursor consome.
Detalhe do levantamento de 13/10: `anexos/F1_S1_inventario-13_10_26.md`.

## Requisitos de negocio (vinculo)

- Fases canonicas fixas: F1 Planejamento · F2 Implementacao ·
  F3 Testes Internos · F4 Homologacao · F5 Aprovacao.
- F = fase · S = sessao/sprint/semana · P = tarefa (~2h, ancorada em commit).
- O template deve servir a qualquer instancia GLPI com API REST (preset
  `generic`); a PMF Franca e o exemplo (preset `api-vscode-glpi`).
- Nenhum segredo (token, `.env`, keystore) entra no template.
- Nenhum historico legado e apagado (do template, do `pmf-dev-kit` ou dos
  consumidores).

## Janela de execucao

Sem data definida. Os atributos `plan_start`/`plan_end` ficam **omitidos** ate
o agendamento; antes de rodar `glpi-retro-scan` / `glpi-tree-validate`,
preencher as janelas (filho contido no pai) — ver pendencias.

## Organograma (resumo)

| Code | Titulo | Status |
|------|--------|--------|
| F1.S1 | Inventario e diagnostico (13/10) | [x] |
| F1.S2 | Decisoes de arquitetura (canonico .cursor) | [ ] |
| F2.S1 | Importacao do API-VScode-GLPI com historico | [ ] |
| F2.S2 | Unificacao de skills em .cursor/skills (F/S/P longa) | [ ] |
| F2.S3 | Traducao PT-BR (skills, agentes, GLPI) | [ ] |
| F2.S4 | Kit de inicializacao de projetos (.cursor) | [ ] |
| F3.S1 | Validadores automaticos do catalogo | [ ] |
| F3.S2 | Bootstrap e upgrade em repositorios descartaveis | [ ] |
| F4.S1 | Piloto no Bot_Pan | [ ] |
| F4.S2 | Demais projetos consumidores | [ ] |
| F5.S1 | Aceite, versao e descontinuacao da fonte antiga | [ ] |

## Fases e tarefas

### F1 — Planejamento

- [ ] **F1** Planejamento da unificacao
  Aceite: inventario completo, matriz de mapeamento aprovada e decisoes de
  arquitetura registradas antes de qualquer alteracao de codigo.
  <!-- glpi: code="F1" -->

  - [x] **F1.S1** Inventario e diagnostico (13/10)
    Levantamento executado nesta sessao em `/home/wsl/projetos` (template,
    API-VScode-GLPI, Bot_Pan, samu-operacional, mev_v3, `~/.cursor/skills`).
    Resumo: `anexos/F1_S1_inventario-13_10_26.md`.
    <!-- glpi: code="F1.S1" -->

    - [x] **F1.S1.P1** Clonar/localizar `API-VScode-GLPI` e inventariar
      Criterio: presente em `/home/wsl/projetos/API-VScode-GLPI`
      (`f83ff4f`), 25 skills, 4 agentes, `tools/glpi/`, `.glpi/`, scripts.
      <!-- glpi: code="F1.S1.P1" -->

    - [x] **F1.S1.P2** Inventariar o template atual
      Criterio: 9 skills + `config` + 4 agentes `.agent.md` (formato Copilot).
      <!-- glpi: code="F1.S1.P2" -->

    - [x] **F1.S1.P3** Inventariar consumidores e divergencias
      Criterio: Bot_Pan 37/27 com YAML duplicado e conflitos; samu-operacional
      33/23 com `description` duplicada; mev_v3 = so zip + pasta extraida;
      Barra_Factory e chatbot-docs nao estao nesta maquina.
      <!-- glpi: code="F1.S1.P3" -->

    - [x] **F1.S1.P4** Matriz de mapeamento skills/agentes
      Criterio: cada item com destino (manter/fundir/renomear/descartar),
      nome final PT-BR e versao de origem escolhida. Incluir `sincronize`.
      Detalhe: `anexos/F1_S1_P4_matriz_mapeamento-14_10_26.md` (36 skills +
      8 agentes entram no template).
      <!-- glpi: code="F1.S1.P4" -->

  - [ ] **F1.S2** Decisoes de arquitetura do template
    Fechar as escolhas estruturais antes da implementacao. Detalhe:
    `anexos/F1_S2_decisoes-13_10_26.md`.
    <!-- glpi: code="F1.S2" -->

    - [x] **F1.S2.P1** Fonte unica e espelho (decidido em 13/10)
      Criterio: canonico em `.cursor/skills/<nome>/SKILL.md` e
      `.cursor/agents/<nome>.md`. `.github/skills` = **link simbolico**
      apontando para `../.cursor/skills` (compatibilidade de scripts e de
      documentacao que citam `.github/skills/...`). Agentes `.agent.md`
      (Copilot) **descontinuados** — sem link e sem conversao automatica,
      pois o schema de agente e diferente. No Windows nativo, o link so
      funciona com Modo de Desenvolvedor + `core.symlinks=true`; no WSL,
      funciona nativo.
      <!-- glpi: code="F1.S2.P1" -->

    - [ ] **F1.S2.P2** Arvore de documentacao unificada
      Criterio: decidir entre `05_progresso` + `06_progresso/historico`
      (template) e `05_progresso/{planos_ativos,geral,legados,pendencias}` +
      `06_glpi` (kit GLPI). Proposta: adotar a arvore do kit GLPI.
      <!-- glpi: code="F1.S2.P2" -->

    - [ ] **F1.S2.P3** Estrategia de importacao com historico
      Criterio: metodo escolhido (subtree ou merge de historicos nao
      relacionados em branch) e regra de resolucao manual de conflitos.
      Proibido `-X union` ou "aceitar ambos" sem edicao (causa dos defeitos
      do Bot_Pan).
      <!-- glpi: code="F1.S2.P3" -->

    - [ ] **F1.S2.P4** Glossario PT-BR
      Criterio: nomes de skills/agentes, palavras-chave de acionamento, tags,
      categorias e titulos de chamados GLPI, nomes de estados. Chaves de
      protocolo GLPI (`todo`, `doing`, `testing`, `done`, `closed`) **nao**
      sao traduzidas; so os rotulos humanos. Renomear skill quebra comandos
      ja usados: manter alias depreciado.
      <!-- glpi: code="F1.S2.P4" -->

    - [ ] **F1.S2.P5** Atualizar `docs/01_requisitos`
      Criterio: requisitos do template registrados (hoje so ha esqueleto).
      <!-- glpi: code="F1.S2.P5" -->

### F2 — Implementacao

- [ ] **F2** Implementacao da unificacao no template
  Aceite: template unico com catalogo F/S/P longo em `.cursor/`, PT-BR, sem
  duplicacao.
  <!-- glpi: code="F2" -->

  - [ ] **F2.S1** Importacao do API-VScode-GLPI com historico
    Trazer o conteudo para o template em branch propria, preservando
    historico e resolvendo conflitos **arquivo a arquivo**.
    <!-- glpi: code="F2.S1" -->

    - [ ] **F2.S1.P1** Branch de integracao e importacao
      Criterio: branch `integracao/api-vscode-glpi` com o historico importado.
      <!-- glpi: code="F2.S1.P1" -->

    - [ ] **F2.S1.P2** Resolucao manual de conflitos
      Criterio: zero marcadores de conflito; nenhum arquivo com duas versoes
      concatenadas. Antes do commit de merge, rodar `rg -n` com padrao de
      marcadores e lint de YAML das skills sem erro.
      <!-- glpi: code="F2.S1.P2" -->

    - [ ] **F2.S1.P3** CLI e configuracao GLPI sem segredos
      Criterio: `tools/glpi/`, `.glpi/*.example`, presets `generic` e
      `api-vscode-glpi`; arquivos reais (`instance.yaml`, `project.yaml`,
      `maps/states.json`) fora do template; `.gitignore` cobrindo segredos.
      <!-- glpi: code="F2.S1.P3" -->

  - [ ] **F2.S2** Unificacao de skills em `.cursor/skills` (F/S/P longa)
    Reescrever o catalogo conforme a matriz do F1.S1.P4.
    <!-- glpi: code="F2.S2" -->

    - [ ] **F2.S2.P1** Skills na versao longa F/S/P
      Criterio: um unico cabecalho YAML valido por `SKILL.md`; `name` igual ao
      nome da pasta; arquivo sempre `SKILL.md` (nunca `Skill.md`).
      <!-- glpi: code="F2.S2.P1" -->

    - [ ] **F2.S2.P2** Fundir skills sobrepostas
      Criterio: pares resolvidos sem perder funcionalidade. Pares principais:
      `encerrar-sessao` (template x kit), `documentar-sessao` x `documentar`,
      `backup-projeto` x `backup`, `atualizar` x `sincronize`/`exporte`/`importe`.
      <!-- glpi: code="F2.S2.P2" -->

    - [ ] **F2.S2.P3** Importar skill `sincronize` dos consumidores
      Criterio: skill `sincronize` presente em Bot_Pan, samu-operacional e
      `~/.cursor/skills` mas ausente no `API-VScode-GLPI`; integrar ao
      catalogo canonico do template.
      <!-- glpi: code="F2.S2.P3" -->

    - [ ] **F2.S2.P4** Binarios GLPI faltantes
      Criterio: existem os binarios citados pelas skills F/S/P
      (`glpi-commit-harvest`, `glpi-progress-rollup`, `glpi-node-upsert`,
      `glpi-phase-ensure`, `glpi-migrate-codes`) ou as skills deixam de
      cita-los. `glpi-tree-validate` ja existe em `tools/glpi/bin/`.
      <!-- glpi: code="F2.S2.P4" -->

    - [ ] **F2.S2.P5** Agentes em `.cursor/agents/*.md`
      Criterio: agentes GLPI (`orchestrator`, `auditor`, `migrator`, `scribe`)
      e agentes hexagonais do template reescritos em formato Cursor
      (`.cursor/agents/<nome>.md`), a partir de fonte unica. Sem conversao
      automatica de `.agent.md` — reescrita manual.
      <!-- glpi: code="F2.S2.P5" -->

    - [ ] **F2.S2.P6** Espelho `.github/skills` conforme F1.S2.P1
      Criterio: `.github/skills` e um symlink apontando para `../.cursor/skills`;
      scripts e documentacao que referenciam `.github/skills/...` continuam
      funcionando.
      <!-- glpi: code="F2.S2.P6" -->

  - [ ] **F2.S3** Traducao PT-BR
    Aplicar o glossario do F1.S2.P4.
    <!-- glpi: code="F2.S3" -->

    - [ ] **F2.S3.P1** Skills e agentes
      Criterio: nomes, descricoes e gatilhos em PT-BR; identificadores sem
      acentos (compatibilidade de tooling).
      <!-- glpi: code="F2.S3.P1" -->

    - [ ] **F2.S3.P2** Artefatos GLPI
      Criterio: titulos de chamados, tags, categorias e mapeamento de estados
      em PT-BR nos templates `.glpi/`. Chaves de protocolo (`todo`, `doing`,
      `testing`, `done`, `closed`) nao traduzidas.
      <!-- glpi: code="F2.S3.P2" -->

    - [ ] **F2.S3.P3** Documentacao e guias
      Criterio: `README.md`, `docs/guia_agentes_skills_ptbr.md` e manuais GLPI
      unificados; referencias a `.cursor/skills` como canonico.
      <!-- glpi: code="F2.S3.P3" -->

  - [ ] **F2.S4** Kit de inicializacao de projetos (.cursor)
    Fluxo unico para criar e atualizar projetos a partir do template.
    <!-- glpi: code="F2.S4" -->

    - [ ] **F2.S4.P1** Scripts de bootstrap e upgrade
      Criterio: `bootstrap-into.sh` e `upgrade-into.sh` (ou equivalentes)
      copiando para `.cursor/skills` e `.cursor/agents`, criando o symlink
      `.github/skills -> ../.cursor/skills`, com dry-run, backup e camada do
      produto preservada. Skill `atualizar-kit` passa a apontar para
      `toolkit-agentes-skills` como fonte.
      <!-- glpi: code="F2.S4.P1" -->

    - [ ] **F2.S4.P2** Esqueleto de docs e planos
      Criterio: arvore decidida no F1.S2.P2, `planos_ativos/README.md`,
      template de plano exemplo F/S/P.
      <!-- glpi: code="F2.S4.P2" -->

    - [ ] **F2.S4.P3** `AGENTS.md` modelo
      Criterio: modelo generico com padrao de commit, regras de resposta e
      ponteiros para o catalogo em `.cursor/`.
      <!-- glpi: code="F2.S4.P3" -->

### F3 — Testes internos

- [ ] **F3** Testes internos do template
  Aceite: validadores verdes e bootstrap/upgrade testados fora de projetos reais.
  <!-- glpi: code="F3" -->

  - [ ] **F3.S1** Validadores automaticos do catalogo
    <!-- glpi: code="F3.S1" -->

    - [ ] **F3.S1.P1** Lint de skills e agentes
      Criterio: falha se houver YAML invalido, chave duplicada, `name` diferente
      da pasta, arquivo fora do nome `SKILL.md`, marcador de conflito ou
      segredo. Aplicar em `.cursor/skills` e `.cursor/agents`.
      <!-- glpi: code="F3.S1.P1" -->

    - [ ] **F3.S1.P2** Validacao GLPI do plano exemplo
      Criterio: `glpi-tree-validate` com exit 0 no plano exemplo.
      <!-- glpi: code="F3.S1.P2" -->

    - [ ] **F3.S1.P3** CI no GitHub
      Criterio: workflow rodando os validadores em cada push/PR.
      <!-- glpi: code="F3.S1.P3" -->

  - [ ] **F3.S2** Bootstrap e upgrade em repositorios descartaveis
    <!-- glpi: code="F3.S2" -->

    - [ ] **F3.S2.P1** Projeto novo vazio
      Criterio: bootstrap completo; Cursor lista as skills e os agentes a
      partir de `.cursor/`.
      <!-- glpi: code="F3.S2.P1" -->

    - [ ] **F3.S2.P2** Clone de projeto existente
      Criterio: upgrade preserva arquivos do produto; nenhum arquivo concatenado.
      <!-- glpi: code="F3.S2.P2" -->

### F4 — Homologacao

- [ ] **F4** Homologacao nos projetos consumidores
  Aceite: piloto aprovado e consumidores atualizados.
  <!-- glpi: code="F4" -->

  - [ ] **F4.S1** Piloto no Bot_Pan
    <!-- glpi: code="F4.S1" -->

    - [ ] **F4.S1.P1** Sanear o Bot_Pan antes do upgrade
      Criterio: 13 skills concatenadas, 7 arquivos com marcadores de conflito,
      `ricardizar/Skill.md` e remote `origin` corrigidos.
      <!-- glpi: code="F4.S1.P1" -->

    - [ ] **F4.S1.P2** Upgrade a partir do template
      Criterio: catalogo unico em `.cursor/`; `.github/skills` deixa de ser
      copia e vira symlink. Skills de produto (`build-*`, `deploy-*`,
      `registrar-tentativa`, `revisar-docs`) preservadas.
      <!-- glpi: code="F4.S1.P2" -->

    - [ ] **F4.S1.P3** Uso real
      Criterio: `commit`, `encerrar-sessao`, `documente-o-plano` e
      `acompanhar-chamado` exercitados contra GLPI de homologacao.
      <!-- glpi: code="F4.S1.P3" -->

  - [ ] **F4.S2** Demais projetos consumidores
    <!-- glpi: code="F4.S2" -->

    - [ ] **F4.S2.P1** Ordem e riscos por projeto
      <!-- glpi: code="F4.S2.P1" -->

    - [ ] **F4.S2.P2** Aplicar upgrade
      Criterio: samu-operacional (preservando `implemente` e
      `.glpi/project.yaml`), mev_v3 (quando houver clone de verdade),
      Barra_Factory e chatbot-docs (quando presentes) atualizados ou com
      justificativa de exclusao.
      <!-- glpi: code="F4.S2.P2" -->

### F5 — Aprovacao

- [ ] **F5** Aprovacao
  <!-- glpi: code="F5" -->

  - [ ] **F5.S1** Aceite, versao e descontinuacao da fonte antiga
    <!-- glpi: code="F5.S1" -->

    - [ ] **F5.S1.P1** Versao `v1.0.0` e `CHANGELOG.md`
      <!-- glpi: code="F5.S1.P1" -->

    - [ ] **F5.S1.P2** Descontinuar `API-VScode-GLPI` como fonte
      Criterio: README do `API-VScode-GLPI` aponta para o template; nada apagado.
      <!-- glpi: code="F5.S1.P2" -->

    - [ ] **F5.S1.P3** Termo de aceite
      Criterio: `[x]` → `[A]` com `accept_ref`.
      <!-- glpi: code="F5.S1.P3" -->

## Pendencias

- [ ] Definir janelas `plan_start`/`plan_end` de F, S e P antes de integrar ao GLPI.
- [ ] Decidir se `docs/06_progresso/` do template e mantido ou absorvido.
- [ ] Preencher `docs/01_requisitos` do template (F1.S2.P5).
- [ ] Escrever anexos `F1_S1_inventario-13_10_26.md` e `F1_S2_decisoes-13_10_26.md`.
- [ ] Mover plano antigo `unificacao_template_kit_glpi-12_10_26-10_40.md` para
  `docs/05_progresso/legados/` (neste ciclo ou quando este plano for aprovado).


