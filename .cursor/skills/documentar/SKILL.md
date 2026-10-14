---
name: documentar
description: >-
  Atualiza planos, decisoes, riscos e progresso em docs/ e registra resumo de
  sessao/handoff. Para criar plano novo F/S/P com timestamps, use
  documente-o-plano. Ao fechar Sn/Pm com codigo, use tambem a skill commit
  (gate de plano). Use em documentar, registrar decisao, resumo de sessao.
argument-hint: "Escopo da sessao e resultado principal."
---

# Skill: documentar

Atualizar documentos existentes e registrar o andamento tecnico:

- `docs/05_progresso/geral/PLANO_IMPLEMENTACAO.md` (checklists)
- Planos em `docs/05_progresso/planos_ativos/*-DD_MM_AA-hh_mm.md`
- Arquitetura / requisitos conforme pastas `docs/02_arquitetura/`, `docs/01_requisitos/`

**Criar plano novo:** skill `documente-o-plano` (nome com timestamp, hierarquia
F/S/P, comentarios `<!-- glpi: ... -->`).

**Fechar item S/P com codigo:** skill `commit` — atualizar planos **antes** do
`git commit` (mesmo commit da entrega).

## Documentar sessao / handoff

Quando o pedido for registrar a sessao (fim de bloco relevante ou handoff):

1. Registrar o que foi feito e por que foi feito.
2. Registrar tentativas, erros e correcoes.
3. Registrar pendencias e tarefas delegadas para depois.
4. Atualizar checklist e status de progresso.
5. Registrar riscos e observacoes tecnicas.

Script de apoio (bloco padrao de resumo):

```bash
python .cursor/skills/documentar/scripts/gerar_resumo_sessao.py
python .cursor/skills/documentar/scripts/gerar_resumo_sessao.py --saida docs/05_progresso/historico/sessao_2026-04-03.md
```

## Endpoint operacional

- Arquivo central: `.cursor/skills/config/endpoints_operacionais.json`
- Chaves: `sessao.historico_relativo_repo`, `sessao.formato_nome_arquivo`,
  `sessao.titulo_padrao`
- Variaveis: `SESSAO_HISTORICO_RELATIVO_REPO`, `SESSAO_FORMATO_NOME_ARQUIVO`,
  `SESSAO_TITULO_PADRAO`
- Precedencia: `--saida/--titulo` > variavel de ambiente > config central

## Criterio de conclusao

- Estado da sessao rastreavel por outra pessoa sem contexto previo.
