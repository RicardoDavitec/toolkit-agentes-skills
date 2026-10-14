# Sessao 2026-10-14 — Unificacao do kit, GLPI e arvore docs

## Sumario executivo

Fechados F2.S4, F3 e quase todo o F4 do plano de unificacao. O catalogo
canonico ficou em `.cursor/`. O upgrade foi aplicado nos consumidores.
As 67 tarefas do projeto GLPI 72 (producao, `suporte.franca.sp.gov.br`)
receberam datas e duracoes. A arvore `docs/` passou a ter 12 pastas,
de `00_visao_geral` a `11_ia`.

## Commits da sessao

- `ca801f1` F2.S4 — scripts `.cursor`, `AGENTS.md` modelo
- `2e870bf` / `2b917f3` F3.S1 — lint, CI, tree-validate
- `57ff1bb` F3.S2 — bootstrap/upgrade em repos descartaveis
- `4b39fb8` F4.S2 — upgrade dos consumidores e wrapper do produto
- `bf71aa2` datas e duracoes obrigatorias na ProjectTask; projeto 72 preenchido
- `9473d30` arvore canonica de 12 pastas
- `333720c` `07_doc_academica/livros` vazia no template

Consumidores (locais ate o push desta sessao): Bot_Pan `3c49e66`,
samu-operacional `cc3c20e`, mev_v3 `0be11b2` (livros em
`07_doc_academica/livros`), Barra_Factory `b4bc0c1`.

## Problemas

- `upgrade-into.sh` abortava no primeiro incremento com `set -e` e o backup
  nao cobria `.cursor/`. Corrigido antes do piloto.
- O wrapper copiado fazia o produto apontar para si mesmo. Passou a delegar
  ao template.
- Homologacao (`suporte-homolog`) so foi lida (chamado 5621). A gravacao das
  duracoes foi em producao.

## Decisoes

- Canonico continua `.cursor/`; `.github/skills` e symlink.
- Duracao e esforco (pacote 2 h, fase sem filhos 8 h, fase com filhos = soma).
  Data e a janela. Data real so com evidencia.
- Pastas de docs usam `NN_nome` com underscore. Hifen foi mesclado.
- `10_livros` do mev_v3 virou `docs/07_doc_academica/livros`.
- chatbot-docs segue fora: repositorio ausente.

## Proximas acoes

- F4.S1.P3: follow-up GLPI, se houver titulo e chamado confirmados.
- Enviar a tag `v1.0.0` e o README do `API-VScode-GLPI` se ainda estiverem so no local.

## Continuacao (15:03)

F5.S1 aceito: `CHANGELOG.md`, tag `v1.0.0` e termo
`anexos/F5_S1_termo_aceite-14_10_26.md`. O README do `API-VScode-GLPI`
aponta para este template; o manual de la foi mantido.
