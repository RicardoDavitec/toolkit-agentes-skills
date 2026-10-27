---
name: encerrar-sessao
description: >-
  Encerra a sessao do dia: cria SESSAO_AAAA-MM-DD em docs/05_progresso/geral,
  conduz commit/push, anexo GLPI opcional e backup opcional. Use em encerrar
  sessao, finalizar o dia, resumo do dia, fechar o dia.
argument-hint: "Foco da sessao (ex: build mobile, docs geral) ou vazio para resumo automatico."
---

# Skill: encerrar-sessao

Fecha a sessao do dia com registro objetivo em `docs/05_progresso/geral/`.

## Modo eficiente (obrigatorio)

- Coletar apenas comandos minimos (`git log` do dia e resumo de diff quando necessario).
- Gerar resumo curto e factual, sem repetir logs inteiros.
- Perguntas: commit, push, **anexo GLPI** (opcional), backup.

## Fluxo minimo obrigatorio

1. Coletar contexto:
   - `git log --oneline --since="00:00" --format="%h %s"`
   - Verificar alteracoes pendentes no git (`git status -sb`).
2. Nomear arquivo: `SESSAO_AAAA-MM-DD_<DESCRICAO_CURTA>.md` em `docs/05_progresso/geral/`.
3. Criar documento com: Sumario Executivo, Commits da sessao, Problemas, Decisoes, Proximas acoes.
   Em cada P fechado no dia, o plano correspondente leva `inicio_real` e `fim_real` preenchidos. Campo real vazio fica vazio.
4. Atualizar `docs/05_progresso/geral/README.md` (ou `LEIA-ME.md` se existir).
5. Versionar: `git add docs/`, sugerir `docs(geral): registra sessao AAAA-MM-DD`, confirmar, commitar.
6. Perguntar sobre push (skill `exporte`; com remote `github`, skill `sincronize`).
7. **Anexar ao GLPI (opcional):** perguntar se deve enviar o `SESSAO_*` como Document no Ticket.
   - Dry-run: `./tools/glpi/bin/glpi-document-attach --file=docs/05_progresso/geral/SESSAO_....md --ticket`
   - Apply: mesmo comando com `--apply` (somente com confirmacao).
   - Opcional: acompanhamento via skill `acompanhar-chamado` apontando o arquivo/sha.
8. Perguntar sobre backup; se sim, carregar skill `backup` e executar.
9. Verificacao (nao altera o plano): `python .github/skills/convencao-codigos-glpi/scripts/checar_prefixo.py`. Exit 1 indica prefixo `C#.R#` fora do cabecalho.

## Script de apoio (opcional)

- Checklist de encerramento:
  `python .cursor/skills/encerrar-sessao/scripts/checklist_encerramento.py --repo .`
- Endpoints centralizados: `.cursor/skills/config/endpoints_operacionais.json`
  (chaves `backup.destino_padrao`, `sessao.historico_relativo_repo`).

## Regras essenciais

- Nao inventar atividades.
- Se nao houver commit no dia, registrar contexto real da conversa.
- Nunca usar `--force`.
- Nao anexar segredos (`.env`, tokens).

## Criterio de conclusao

- Sessao encerrada com rastreabilidade tecnica e operacional.

## Referencias

- Skill `documentar`
- Skill `acompanhar-chamado` (alias legado: `glpi-followup`)
- Skill `backup`
- Wrapper: `tools/glpi/bin/glpi-document-attach`
- Dicas: [DICAS_USO.md](DICAS_USO.md)
