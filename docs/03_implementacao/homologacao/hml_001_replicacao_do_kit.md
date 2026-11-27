---
id: HML-001
tipo: homologacao
titulo: Replicação do kit na cópia de teste
codigo: F4.S1
status: em_revisao
versao: 0.4.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Replicação do kit na cópia de teste

## Participantes
| Nome | Papel | Presença |
|---|---|---|
| Ricardo | execução da replicação | presente |

## Cenários
| ID | Cenário | Requisito | Resultado |
|---|---|---|---|
| HML-001-C | Cópia de teste sem remote | RN-007 | A cópia já estava no caminho aprovado e não tinha remote. Não houve novo clone. |
| HML-001-F | Quatro CSVs trocados por 8 linhas fictícias | RN-007 | Conteúdo real não foi lido nem copiado. Cada arquivo ficou com cabeçalho e sete linhas de teste. |
| HML-001-E | Estado antes do bootstrap | RN-006 | Registro, escala e histórico ausentes. Nenhum arquivo com esses nomes. Os quatro CSVs fictícios tinham o mesmo sha256. |
| HML-001-B | Bootstrap com perfil pmf-core | RN-006 | Concluído. Registro e escala continuaram ausentes. A pasta de histórico foi criada vazia. O sha256 dos CSVs não mudou. Nenhum número de chamado foi gravado. |

## Achados
| ID | Descrição | Gravidade | Tratamento |
|---|---|---|---|
| HML-001-A1 | Novo clone apagaria a cópia já existente | alta | Clone não refeito; remote já estava ausente |

## Decisão
**Resultado:** em andamento

**Referência do aceite (`accept_ref`):** sessão F4.S1, 27/11/2026
