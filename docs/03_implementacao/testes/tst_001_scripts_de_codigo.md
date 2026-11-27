---
id: TST-001
tipo: teste
titulo: Scripts de código de elemento
codigo: F3.S1
status: em_revisao
versao: 0.4.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Scripts de código de elemento

## Escopo
Scripts em `scripts/manutencao/` no Linux (WSL) e no Windows (PowerShell, Python 3.14.4).

## Estratégia
Teste unitário com `unittest` e teste de preservação em cópia descartável. Os resultados do Linux e do Windows, inclusive formato, duplicidade e caminho, ficam nesta ficha.

## Casos de teste
| ID | Requisito | Passos | Resultado esperado | Resultado obtido | Estado |
|---|---|---|---|---|---|
| TST-001-L | RN-001, RN-003, RN-006 | `python3 -m unittest discover -s scripts/manutencao/testes` e `bash scripts/manutencao/testes/test_preservar.sh` | 16 testes unitários ok; preservação confirma o marcador | 16 ok em 0,006 s; preservação ok | passou |
| TST-001-W | RN-001, RN-003 | No PowerShell, `python -m unittest discover -s scripts/manutencao/testes` | 16 testes unitários ok | 16 ok em 0,034 s, Python 3.14.4 | passou |
| TST-001-F | RN-001 | Caso `test_bloqueia_formato_invalido` | código fora da forma é recusado | mensagem `formato invalido: painel`, saída 1 | passou |
| TST-001-D | RN-001 | Caso `test_bloqueia_duplicado` | código repetido é recusado | mensagem `codigo duplicado: ppain1`, saída 1 | passou |
| TST-001-C | RN-003 | Caso `test_bloqueia_caminho_inexistente` | caminho ausente é recusado | mensagem `caminho inexistente: ausente.html`, saída 1 | passou |

## Critérios de saída
- [x] Linux (WSL) executado em 27/11/2026
- [x] Windows (PowerShell) executado em 27/11/2026
- [ ] Falhas corrigidas, ou nenhuma falha na rodada
- [ ] Nova rodada registrada
