---
name: doc-adr
description: >-
  Registra uma decisao de arquitetura (ADR) com contexto, decisao, alternativas
  e consequencias. Use em registrar a decisao, criar ADR, documentar escolha
  tecnica, por que escolhemos.
argument-hint: "Decisao em uma frase (ex: usar PostgreSQL como banco principal)."
---

# Skill: doc-adr

Grava `docs/02_arquitetura/adr/adr_<NNN>_<slug>.md` com o modelo `MOD_adr`.

## Fluxo

1. Extrair da conversa: contexto, decisao, alternativas consideradas.
   Se houver uma so alternativa, perguntar quais foram descartadas.
2. Numerar em sequencia (`ADR-001`, `ADR-002`...). Nunca reutilizar numero.
3. Preencher `Contexto`, `Decisao`, `Alternativas consideradas`, `Consequencias`.
4. Se a decisao substitui outra, marcar a antiga como `obsoleto` e citar a nova.
5. Atualizar o indice em `docs/02_arquitetura/adr/README.md`.
6. Rodar `doc-lint`.

## Regras

- Um ADR por decisao. Decisao em voz ativa.
- Decisao que envolve dado pessoal em escala cita o G12 (avaliar RIPD).
- Nunca editar um ADR aprovado: criar outro que o substitua.
