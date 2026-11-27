---
name: manutencao-identificar-elemento
description: >-
  Atribui um código estável a um elemento visível e grava data-maint-id.
  Use em identificar elemento, atribuir código de manutenção, marcar painel,
  quadro, janela, modal, formulário ou componente.
---

# Skill: manutencao-identificar-elemento

## Fluxo

1. Classifique o elemento: `p` painel, `q` quadro, `j` janela, `m` modal, `e` formulário, `c` componente. Skill, agente e script deste kit também usam `c`.
2. Monte o código na forma `^[pqjmec][a-z]{2,4}[0-9]{1,2}$`.
3. Confira no registro se o código já existe, inclusive entre aposentados. Se existir, escolha outro.
4. Grave `data-maint-id` no elemento e proponha a entrada no registro. Não grave o registro sem confirmação.

## Fronteira

Esta skill não substitui `convencao-codigos-glpi`. O código do elemento não é um código `F#.S#.P#`.
