---
name: doc-lint
description: >-
  Valida a documentacao do projeto: front matter, nomes, secoes obrigatorias,
  catalogo do kit e prefixos de codigo. Use em validar a documentacao, rodar o
  lint, antes de commitar docs, conferir os documentos.
argument-hint: "Opcional: --estrito (exige front matter em todos os documentos)."
---

# Skill: doc-lint

Executa, nesta ordem, e resume os resultados:

~~~bash
python3 scripts/docs/lint_docs.py
python3 scripts/lint_template.py
~~~

## Fluxo

1. Rodar os comandos. Se algum arquivo nao existir, avisar e seguir.
2. Agrupar os achados por arquivo.
3. Propor a correcao de cada erro. Aplicar apenas dentro de `docs/`.
4. Reexecutar ate zerar os erros.

## Regras

- Nao alterar planos, anexos nem `SESSAO_*` para satisfazer o lint.
- O aviso "prefixo C#.R# fora do cabecalho" pede para corrigir o texto: C e R
  so aparecem no cabecalho do plano.
- Avisos nao bloqueiam, mas devem ser listados.
