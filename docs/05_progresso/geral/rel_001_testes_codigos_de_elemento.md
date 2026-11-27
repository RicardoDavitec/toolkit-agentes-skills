---
id: REL-001
tipo: relatorio
titulo: Testes internos dos códigos de elemento
codigo: F3.S2.P5
status: em_revisao
versao: 0.1.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Testes internos dos códigos de elemento

## Resumo
Os scripts de código passaram no Linux e no Windows. O chamado fictício `[ppain1] ajuste do painel inicial` foi tratado em dry-run local. Não houve escrita no GLPI: este repositório não tem `project.yaml` de projeto, e a cadeia do orquestrador não foi chamada.

## Resultado
| Item do critério de saída | Situação | Evidência |
|---|---|---|
| Formato inválido é bloqueado | passou | TST-001-F, `formato invalido: painel` |
| Código duplicado é bloqueado | passou | TST-001-D, `codigo duplicado: ppain1` |
| Caminho inexistente é bloqueado | passou | TST-001-C, `caminho inexistente: ausente.html` |
| Linux, 16 testes unitários | passou | 27/11/2026, 0,006 s, segunda rodada |
| Windows, 16 testes unitários | passou | PowerShell, Python 3.14.4, 0,026 s, segunda rodada |
| Preservação de registro, escala e histórico | passou | `scripts/manutencao/testes/test_preservar.sh` |
| Localização do arquivo em menos de 1 minuto | passou no ensaio | 0,000097 s numa pasta com um arquivo, `painel.html` |
| Escrita no GLPI | não executada | dry-run local; sem `project.yaml` |

## Riscos residuais
- A medição de tempo usou uma pasta com um único arquivo, não uma árvore de produto.
- O lint de documentos ainda avisa o hífen em `padrao-identificacao.md`.
- A fase seguinte não foi iniciada.
