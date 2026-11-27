---
id: GUI-016
tipo: guia
titulo: Padrão de identificação de elemento
codigo: F1.S2.P1
status: rascunho
versao: 0.1.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Padrão de identificação de elemento

## Forma
O código casa com `^[pqjmec][a-z]{2,4}[0-9]{1,2}$`.

1. Uma letra de tipo, minúscula, dentre `p`, `q`, `j`, `m`, `e` e `c`.
2. De duas a quatro letras minúsculas.
3. Um ou dois dígitos.

## Tipos
| Letra | Tipo |
|---|---|
| `p` | painel |
| `q` | quadro |
| `j` | janela |
| `m` | modal |
| `e` | formulário |
| `c` | componente |

## Exemplos
| Código | Leitura |
|---|---|
| `ppain1` | painel |
| `qkart1` | quadro |
| `jmain1` | janela |
| `mavis1` | modal |
| `eform1` | formulário |
| `ccomp1` | componente |

Não casam com a forma: `pain1` (sem letra de tipo), `eformul1` (cinco letras no meio), `PPain1` (maiúsculas).

## Exibição
O código fica no canto inferior esquerdo do elemento. O checkbox "Exibir código de identificação para manutenção nos elementos do sistema." controla a exibição.
