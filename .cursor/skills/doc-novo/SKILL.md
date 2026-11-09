---
name: doc-novo
description: >-
  Cria documento de apoio (requisito, regra de negocio, glossario, arquitetura,
  teste, homologacao, runbook) a partir do modelo do padrao. Nao cria planos.
  Use em criar requisito, nova regra de negocio, criar runbook, plano de
  testes, ata de homologacao, novo documento.
argument-hint: "Tipo e titulo (ex: requisito, 'Cadastro de usuario')."
---

# Skill: doc-novo

Cria um documento a partir de `docs/12_padrao_documentacao/02_modelos/MOD_<tipo>.md`.

## Fluxo

1. Confirmar o tipo (guia G03) e o titulo. Planos: use `documente-o-plano`.
   Sessao do dia: `encerrar-sessao`. Pendencia: `inserir-pendencia`.
2. Localizar o modelo. Se nao existir, avisar e parar.
3. Definir pasta e nome pelo G03 (snake_case, sem acento, `<prefixo>_<NNN>_<slug>.md`).
   Calcular o proximo `NNN` olhando os arquivos existentes.
4. Preencher o front matter (`id`, `tipo`, `titulo`, `status: rascunho`,
   `versao: 0.1.0`, `data`, `autor`, `classificacao`).
5. Preencher as secoes com o que a conversa e os documentos sustentam.
   O que faltar fica como `A DEFINIR` com uma pergunta. Nada de invencao.
6. Rodar `doc-lint`.

## Regras

- C e R so no cabecalho, nunca no id nem no nome do arquivo.
- Sem segredo e sem dado pessoal real.
- Escreve apenas em `docs/`.
