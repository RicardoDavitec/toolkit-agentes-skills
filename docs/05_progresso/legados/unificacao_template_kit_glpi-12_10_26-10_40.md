# Plano: Unificacao do template toolkit-agents-skills com API-VSCode-GLPI

> Criado: 12/10/2026 10:40 · Fase principal: `F1` · Produto: `toolkit-agents-skills`
> Arquivo: `unificacao_template_kit_glpi-12_10_26-10_40.md`
> Requisitos: `docs/01_requisitos/README.md` (ainda vazio — ver pendencias)
> Estado: **planejado, nao executar ainda** (decisao do responsavel em 12/10/2026)

## Objetivo

Tornar o `toolkit-agents-skills` o **unico template de inicializacao** de
repositorios de projeto, incorporando o conteudo do `API-VSCode-GLPI`
(`pmf-dev-kit` no Gitness: CLI GLPI, configuracao `.glpi/`, skills e agentes
GLPI, scripts de bootstrap/upgrade). Resultado esperado:

- skills e agentes no padrao **F/S/P versao longa**;
- **uma fonte unica** de skills e agentes, sem copias divergentes entre
  `.github/` e `.cursor/`;
- nomes, descricoes, palavras-chave de acionamento, tags e rotulos de chamados
  GLPI **em portugues do Brasil**;
- projetos consumidores atualizados a partir do template, sem perda de
  historico nem de customizacoes locais.

## Motivacao (evidencia)

No Bot_Pan, o commit `dcc7a47` (06/10/2026, merge de `api-vscode-glpi/main`)
deixou 13 skills com duas versoes coladas (S/P curta + F/S/P longa), 5 delas
com cabecalho YAML invalido, e 7 arquivos com marcadores de conflito. Alem
disso, `.github/skills` e `.cursor/skills` divergiram. Detalhe em
[`anexos/F1_S1_diagnostico-12_10_26.md`](./anexos/F1_S1_diagnostico-12_10_26.md).

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
| F1.S1 | Inventario e diagnostico | [ ] |
| F1.S2 | Decisoes de arquitetura do template | [ ] |
| F2.S1 | Importacao do API-VSCode-GLPI com historico | [ ] |
| F2.S2 | Unificacao de skills e agentes (F/S/P longa) | [ ] |
| F2.S3 | Traducao PT-BR (skills, agentes, GLPI) | [ ] |
| F2.S4 | Kit de inicializacao de projetos | [ ] |
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

  - [ ] **F1.S1** Inventario e diagnostico
    Levantar o que existe no template, no `API-VSCode-GLPI` e nos consumidores,
    e classificar cada skill/agente (manter, fundir, renomear, descartar).
    Detalhe: [`anexos/F1_S1_diagnostico-12_10_26.md`](./anexos/F1_S1_diagnostico-12_10_26.md)
    <!-- glpi: code="F1.S1" -->

    - [ ] **F1.S1.P1** Clonar `API-VSCode-GLPI` (`pmf-dev-kit`) e inventariar
      Criterio: lista de skills, agentes, binarios `tools/glpi/bin/`, arquivos
      `.glpi/`, scripts e docs, com versao/commit de referencia.
      <!-- glpi: code="F1.S1.P1" -->

    - [ ] **F1.S1.P2** Inventariar o template atual
      Criterio: 9 skills + 4 agentes Copilot classificados por dominio
      (operacional, hexagonal, documentacao, backup).
      <!-- glpi: code="F1.S1.P2" -->

    - [ ] **F1.S1.P3** Inventariar consumidores e divergencias
      Criterio: tabela por projeto (Bot_Pan, Barra_Factory, chatbot-docs,
      mev_v3, samu_operacional) com skills locais, customizacoes e defeitos.
      <!-- glpi: code="F1.S1.P3" -->

    - [ ] **F1.S1.P4** Matriz de mapeamento skills/agentes
      Criterio: cada item com destino (manter/fundir/renomear/descartar),
      nome final PT-BR e versao de origem escolhida.
      <!-- glpi: code="F1.S1.P4" -->

  - [ ] **F1.S2** Decisoes de arquitetura do template
    Fechar as escolhas estruturais antes da implementacao.
    Detalhe: [`anexos/F1_S2_decisoes_arquitetura-12_10_26.md`](./anexos/F1_S2_decisoes_arquitetura-12_10_26.md)
    <!-- glpi: code="F1.S2" -->

    - [ ] **F1.S2.P1** Fonte unica e espelho Cursor/Copilot
      Criterio: decisao registrada (canonico em `.github/`, espelho em
      `.cursor/` por link simbolico ou script) incluindo comportamento em
      Windows sem WSL.
      <!-- glpi: code="F1.S2.P1" -->

    - [ ] **F1.S2.P2** Arvore de documentacao unificada
      Criterio: decidir entre `05_progresso` + `06_progresso/historico`
      (template) e `05_progresso/{planos_ativos,geral,legados,pendencias}` +
      `06_glpi` (kit GLPI).
      <!-- glpi: code="F1.S2.P2" -->

    - [ ] **F1.S2.P3** Estrategia de importacao com historico
      Criterio: metodo escolhido (subtree ou merge de historicos nao
      relacionados em branch) e regra de resolucao manual de conflitos.
      <!-- glpi: code="F1.S2.P3" -->

    - [ ] **F1.S2.P4** Glossario PT-BR
      Criterio: nomes de skills/agentes, palavras-chave de acionamento, tags,
      categorias e titulos de chamados GLPI, nomes de estados.
      <!-- glpi: code="F1.S2.P4" -->

    - [ ] **F1.S2.P5** Atualizar `docs/01_requisitos`
      Criterio: requisitos do template registrados (hoje so ha esqueleto).
      <!-- glpi: code="F1.S2.P5" -->

### F2 — Implementacao

- [ ] **F2** Implementacao da unificacao no template
  Aceite: template unico com catalogo F/S/P longo, PT-BR, sem duplicacao.
  <!-- glpi: code="F2" -->

  - [ ] **F2.S1** Importacao do API-VSCode-GLPI com historico
    Trazer o conteudo do `pmf-dev-kit` para o template em branch propria,
    preservando historico e resolvendo conflitos **arquivo a arquivo**.
    <!-- glpi: code="F2.S1" -->

    - [ ] **F2.S1.P1** Branch de integracao e importacao
      Criterio: branch `integracao/api-vscode-glpi` com o historico importado.
      <!-- glpi: code="F2.S1.P1" -->

    - [ ] **F2.S1.P2** Resolucao manual de conflitos
      Criterio: zero marcadores `<<<<<<<`/`>>>>>>>`; nenhum arquivo com duas
      versoes concatenadas (licao do `dcc7a47`). Proibido merge `union`.
      <!-- glpi: code="F2.S1.P2" -->

    - [ ] **F2.S1.P3** CLI e configuracao GLPI sem segredos
      Criterio: `tools/glpi/`, `.glpi/*.example`, presets `generic` e
      `api-vscode-glpi`; arquivos reais (`instance.yaml`, `project.yaml`,
      `maps/states.json`) fora do template; `.gitignore` cobrindo segredos.
      <!-- glpi: code="F2.S1.P3" -->

  - [ ] **F2.S2** Unificacao de skills e agentes (F/S/P longa)
    Reescrever o catalogo conforme a matriz do F1.S1.P4.
    <!-- glpi: code="F2.S2" -->

    - [ ] **F2.S2.P1** Skills na versao longa F/S/P
      Criterio: um unico cabecalho YAML valido por `SKILL.md`; `name` igual ao
      nome da pasta; arquivo sempre `SKILL.md`.
      <!-- glpi: code="F2.S2.P1" -->

    - [ ] **F2.S2.P2** Fundir skills sobrepostas
      Criterio: pares resolvidos (`encerrar-sessao` x2, `documentar-sessao` x
      `documentar`, `backup-projeto` x `backup`) sem perder funcionalidade.
      <!-- glpi: code="F2.S2.P2" -->

    - [ ] **F2.S2.P3** Binarios GLPI faltantes
      Criterio: existem os binarios citados pelas skills F/S/P
      (`glpi-tree-validate`, `glpi-commit-harvest`, `glpi-progress-rollup`,
      `glpi-node-upsert`, `glpi-phase-ensure`, `glpi-migrate-codes`) ou as
      skills deixam de cita-los.
      <!-- glpi: code="F2.S2.P3" -->

    - [ ] **F2.S2.P4** Agentes Copilot e Cursor
      Criterio: agentes GLPI (`orchestrator`, `auditor`, `migrator`, `scribe`)
      e agentes do template disponiveis nos dois formatos a partir de uma
      fonte unica (gerador ou wrapper fino).
      <!-- glpi: code="F2.S2.P4" -->

    - [ ] **F2.S2.P5** Espelho `.cursor/` conforme F1.S2.P1
      Criterio: Cursor e Copilot enxergam o mesmo catalogo sem copia manual.
      <!-- glpi: code="F2.S2.P5" -->

  - [ ] **F2.S3** Traducao PT-BR
    Aplicar o glossario do F1.S2.P4.
    <!-- glpi: code="F2.S3" -->

    - [ ] **F2.S3.P1** Skills e agentes
      Criterio: nomes, descricoes e gatilhos em PT-BR; identificadores sem
      acentos (compatibilidade de tooling).
      <!-- glpi: code="F2.S3.P1" -->

    - [ ] **F2.S3.P2** Artefatos GLPI
      Criterio: titulos de chamados, tags, categorias e mapeamento de estados
      em PT-BR nos templates `.glpi/`.
      <!-- glpi: code="F2.S3.P2" -->

    - [ ] **F2.S3.P3** Documentacao e guias
      Criterio: `README.md`, `docs/guia_agentes_skills_ptbr.md` e manuais GLPI
      unificados.
      <!-- glpi: code="F2.S3.P3" -->

  - [ ] **F2.S4** Kit de inicializacao de projetos
    Fluxo unico para criar e atualizar projetos a partir do template.
    <!-- glpi: code="F2.S4" -->

    - [ ] **F2.S4.P1** Scripts de bootstrap e upgrade
      Criterio: `bootstrap-into.sh` e `upgrade-into.sh` (ou equivalentes)
      apontando para o template, com dry-run, backup e camada do produto
      preservada.
      <!-- glpi: code="F2.S4.P1" -->

    - [ ] **F2.S4.P2** Esqueleto de docs e planos
      Criterio: arvore decidida no F1.S2.P2, `planos_ativos/README.md`,
      template de plano exemplo F/S/P.
      <!-- glpi: code="F2.S4.P2" -->

    - [ ] **F2.S4.P3** `AGENTS.md` modelo
      Criterio: modelo generico com padrao de commit, regras de resposta e
      ponteiros para o catalogo.
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
      segredo.
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
      Criterio: bootstrap completo; Cursor e VS Code Copilot listam as skills e
      os agentes.
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
      Criterio: catalogo unico; `.cursor/skills` deixa de ser copia.
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
      Criterio: Barra_Factory, chatbot-docs, mev_v3 e samu_operacional
      atualizados ou com justificativa de exclusao.
      <!-- glpi: code="F4.S2.P2" -->

### F5 — Aprovacao

- [ ] **F5** Aprovacao
  <!-- glpi: code="F5" -->

  - [ ] **F5.S1** Aceite, versao e descontinuacao da fonte antiga
    <!-- glpi: code="F5.S1" -->

    - [ ] **F5.S1.P1** Versao `v1.0.0` e `CHANGELOG.md`
      <!-- glpi: code="F5.S1.P1" -->

    - [ ] **F5.S1.P2** Descontinuar `pmf-dev-kit` como fonte
      Criterio: README do `pmf-dev-kit` aponta para o template; nada apagado.
      <!-- glpi: code="F5.S1.P2" -->

    - [ ] **F5.S1.P3** Termo de aceite
      Criterio: `[x]` → `[A]` com `accept_ref`.
      <!-- glpi: code="F5.S1.P3" -->

## Pendencias

- [ ] Definir janelas `plan_start`/`plan_end` de F, S e P antes de integrar ao GLPI.
- [ ] Obter acesso ao `API-VSCode-GLPI` (Gitness) a partir desta maquina.
- [ ] Decidir se `docs/06_progresso/` do template e mantido ou absorvido.
- [ ] Preencher `docs/01_requisitos` do template (F1.S2.P5).
