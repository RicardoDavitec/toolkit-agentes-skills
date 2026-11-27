---
id: TST-001
tipo: teste
titulo: Scripts de código de elemento
codigo: F3.S1
status: em_revisao
versao: 0.1.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Scripts de código de elemento

## Escopo
Scripts em `scripts/manutencao/` no Linux (WSL).

## Estratégia
Teste unitário com `unittest` e teste de preservação em cópia descartável.

## Casos de teste
| ID | Requisito | Passos | Resultado esperado | Resultado obtido | Estado |
|---|---|---|---|---|---|
| TST-001-L | RN-001, RN-003, RN-006 | `python3 -m unittest discover -s scripts/manutencao/testes` e `bash scripts/manutencao/testes/test_preservar.sh` | 16 testes unitários ok; preservação confirma o marcador | 16 ok em 0,006 s; preservação ok | passou |

## Critérios de saída
- [x] Linux (WSL) executado em 27/11/2026
- [ ] Windows (PowerShell) executado
- [ ] Falhas corrigidas, ou nenhuma falha na rodada
- [ ] Nova rodada registrada
