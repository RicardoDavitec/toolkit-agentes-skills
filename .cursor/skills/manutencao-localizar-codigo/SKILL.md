---
name: manutencao-localizar-codigo
description: >-
  Localiza o arquivo de um elemento a partir do código ou da descrição.
  Use em localizar código, achar arquivo do elemento, abrir o código de manutenção.
---

# Skill: manutencao-localizar-codigo

## Fluxo

1. Se houver registro, leia o `caminho` do código.
2. Se o código estiver só na interface, rode `scripts/manutencao/manutencao.sh varrer .` e filtre a saída.
3. Entregue o caminho e a linha. Não altere arquivo nem registro.

## Fronteira

Esta skill não abre chamado e não escreve no GLPI.
