---
name: manutencao-auditar-codigos
description: >-
  Audita códigos de elemento em somente leitura. Compara a varredura com o
  registro e aponta divergência. Use em auditar códigos, conferir registro,
  achar código duplicado ou caminho inexistente.
---

# Skill: manutencao-auditar-codigos

## Fluxo

1. Rode `scripts/manutencao/manutencao.sh varrer .`.
2. Rode `scripts/manutencao/manutencao.sh validar <registro> --raiz .`.
3. Relacione código na interface sem registro, código no registro sem `data-maint-id` e erros do validador.
4. Entregue o relatório. Não altere arquivo, registro, Git nem GLPI.

## Proibições

- Qualquer `--apply`.
- Qualquer `git add`, `commit` ou `push`.
