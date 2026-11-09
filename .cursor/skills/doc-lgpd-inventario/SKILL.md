---
name: doc-lgpd-inventario
description: >-
  Cria e atualiza o inventario de dados pessoais (LGPD) com finalidade, base
  legal, retencao e acesso por campo. Use em inventario LGPD, classificar dados
  pessoais, dado sensivel, mapear dados pessoais, base legal.
argument-hint: "Tabela ou modulo a inventariar (vazio = todos)."
---

# Skill: doc-lgpd-inventario

Grava em `docs/09_dados_e_tabelas/lgpd/inventario.md` (classificacao `pessoal`).

## Fluxo

1. Varrer o esquema atras de campos pessoais: nome, CPF, e-mail, telefone,
   endereco, data de nascimento, saude, localizacao, biometria.
2. Uma linha por **ponto de exposicao** (campo em cada tabela), mesmo que o
   dado se repita em varias tabelas.
3. Preencher: dado, sensivel (sim ou nao), finalidade, base legal, retencao,
   papeis com acesso.
4. Finalidade, base legal e retencao sem fonte documentada ficam `A DEFINIR`,
   com a pergunta ao encarregado (DPO) ou ao gestor. Nao decidir sozinho.
5. Marcar tambem logs, caches e copias (exposicoes indiretas).
6. Rodar `doc-lint`.

## Regras

- Nenhum dado pessoal real no inventario (so nomes de campos e tabelas).
- Orientacao tecnica, nao parecer juridico (ver G12).
