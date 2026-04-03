---
name: documentar-sessao
description: 'Documenta andamento tecnico e decisoes da sessao. Use para atualizar todo list, checklist, riscos, tentativas-erros-correcoes e pendencias futuras na hierarquia de docs.'
argument-hint: 'Escopo da sessao e resultado principal'
user-invocable: true
---

# Documentar Sessao

## Quando usar
- Ao final de bloco relevante de trabalho.
- Antes de handoff para outra pessoa ou outro agente.

## Procedimento
1. Registrar o que foi feito e por que foi feito.
2. Registrar tentativas, erros e correcoes.
3. Registrar pendencias e tarefas delegadas para depois.
4. Atualizar checklist e status de progresso.
5. Registrar riscos e observacoes tecnicas.

## Script de apoio
- [Gerar bloco padrao de resumo](./scripts/gerar_resumo_sessao.py)

Exemplo:
- `python .github/skills/documentar-sessao/scripts/gerar_resumo_sessao.py`
- `python .github/skills/documentar-sessao/scripts/gerar_resumo_sessao.py --saida docs/06_progresso/historico/sessao_2026-04-03.md`

## Endpoint operacional
- Arquivo central: `/.github/skills/config/endpoints_operacionais.json`
- Chaves: `sessao.historico_relativo_repo`, `sessao.formato_nome_arquivo`, `sessao.titulo_padrao`

## Variaveis de ambiente (precedencia)
- `SESSAO_HISTORICO_RELATIVO_REPO`
- `SESSAO_FORMATO_NOME_ARQUIVO`
- `SESSAO_TITULO_PADRAO`
- Precedencia: `--saida/--titulo` > variavel de ambiente > config central

## Criterio de Conclusao
- Estado da sessao rastreavel por outra pessoa sem contexto previo.
