---
id: DIC-atendimentos
tipo: dicionario_dados
titulo: Dicionário de dados – atendimentos
status: rascunho
versao: 0.1.0
data: 2026-11-09
autor: Exemplo
classificacao: restrito
---

# Dicionário de dados – atendimentos

## Finalidade
Registro central de cada chamada atendida (tabela fictícia de exemplo).

## Colunas
| Coluna | Tipo | Nulo? | Padrão | Descrição | Dado pessoal? | Valores permitidos ou exemplo |
|---|---|---|---|---|---|---|
| `id` | uuid | Não | gerado | Identificador | Não | – |
| `protocolo` | texto | Não | – | Protocolo único | Não | `250101-0001` |
| `telefone` | texto | Sim | – | Telefone de origem | Sim | – |
| `status` | texto | Não | `ABERTO` | Situação | Não | `ABERTO`, `EM_ANALISE`, `ENCERRADO` |

## Relacionamentos
| Relação | Cardinalidade | Regra de exclusão |
|---|---|---|
| atendimentos → registros_clinicos | 1 para N | Cascata |

## Índices e restrições
`protocolo` único; índice em `status`.

## Regras de negócio relacionadas
RN-001

## Dívida técnica
`status` é texto livre; avaliar migrar para enum.
