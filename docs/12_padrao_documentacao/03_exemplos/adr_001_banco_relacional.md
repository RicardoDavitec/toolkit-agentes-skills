---
id: ADR-001
tipo: adr
titulo: Usar banco relacional como base principal
codigo: F1.S1.P2
status: aprovado
versao: 1.0.0
data: 2026-11-09
autor: Exemplo
classificacao: interno
---

# Usar banco relacional como base principal

## Contexto
O sistema precisa de integridade referencial entre atendimentos, equipes e registros clínicos, com consultas por período.

## Decisão
Adotar PostgreSQL como banco principal, acessado por um ORM com migrações versionadas.

## Alternativas consideradas
| Alternativa | Vantagens | Desvantagens |
|---|---|---|
| PostgreSQL | Integridade, JSON nativo, maturidade | Exige administração |
| Banco de documentos | Esquema flexível | Integridade fica na aplicação |

## Consequências
O esquema passa a ser documentado em `09_dados_e_tabelas`. Mudanças de esquema exigem atualizar o dicionário (guia G11).
