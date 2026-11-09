---
name: doc-dados-schema
description: >-
  Regenera o ER, o dicionario de dados e o catalogo de enums a partir do
  esquema do banco (Prisma ou equivalente) e aponta campos sem descricao.
  Use em atualizar o dicionario, gerar o ER, mudou o schema, nova migracao,
  documentar o banco.
argument-hint: "Caminho do esquema (padrao: prisma/schema.prisma)."
---

# Skill: doc-dados-schema

Mantem `docs/09_dados_e_tabelas/` coerente com o esquema.

## Fluxo

1. Localizar o esquema. Ler, sem editar.
2. Rodar `scripts/docs/gerar_dados_prisma.sh` quando existir. Sem o script,
   avisar e montar o ER em Mermaid manualmente, por modulo.
3. Para cada tabela nova ou alterada: criar ou atualizar
   `dicionario/dic_<tabela>.md` com o modelo `MOD_dicionario_dados`.
4. Atualizar `enums/` com cada valor e seu significado operacional.
5. Listar em "divida tecnica": relacoes sem `@relation`, campos de texto que
   funcionam como enum, campos JSON sem exemplo, indices suspeitos.
6. Calcular a cobertura: modelos e campos com descricao dividido pelo total.
7. Entregar no chat os comentarios `///` sugeridos para o esquema.
8. Rodar `doc-lint`.

## Regras

- Nunca editar o esquema (fica fora de `docs/`).
- ER legivel: ate cerca de 25 entidades por diagrama; dividir por modulo.
- Conferir contagens (modelos, enums) com um comando, nao de memoria.
