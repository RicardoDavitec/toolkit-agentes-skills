---
name: encerrar-sessao
description: 'Fecha a sessao de trabalho com checklist completo. Use para consolidar progresso, documentar, sincronizar git/github e oferecer backup opcional.'
argument-hint: 'Resumo da sessao e decisao de publicacao'
user-invocable: true
---

# Encerrar Sessao

## Quando usar
- Ao terminar uma sessao de desenvolvimento.
- Antes de trocar de contexto ou encerrar o dia.

## Procedimento
1. Verificar estado tecnico da sessao.
2. Acionar documentar-sessao.
3. Verificar alteracoes pendentes no git.
4. Commitar e enviar quando aplicavel.
5. Perguntar se deseja acionar backup-projeto.

## Script de apoio
- [Rodar checklist de encerramento](./scripts/checklist_encerramento.py)

Exemplo:
- `python .github/skills/encerrar-sessao/scripts/checklist_encerramento.py --repo .`

## Endpoint operacional
- Arquivo central: `/.github/skills/config/endpoints_operacionais.json`
- Chaves usadas no checklist: `backup.destino_padrao`, `backup.fallback_relativo_repo`, `sessao.historico_relativo_repo`

## Criterio de Conclusao
- Sessao encerrada com rastreabilidade tecnica e operacional.
