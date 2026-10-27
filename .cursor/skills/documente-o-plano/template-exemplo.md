# Plano: Exemplo Offline Sync

> Criado: 24/07/2026 09:40 · Modulo: `geral` · Arquivo: `offline_sync-24_07_26-09_40.md`
> Requisitos: `docs/01_requisitos/README.md` (substituir pelos RNs reais do produto)

## Objetivo

Entregar sincronizacao offline testavel no modulo operacional, sem violar requisitos de negocio ja documentados.

## Requisitos de negocio (vinculo)

- Conferir `docs/01_requisitos/` antes de iniciar S1.
- Se a pasta so tiver esqueleto: **ACAO** — documentar RNs de sync/fila/auditoria antes do codigo.
- Exemplo de vinculo: RN-fila-offline → nenhum evento perde ordem FIFO.

## Organograma (resumo)

| Code | Titulo | Status | Plan ini | Plan fim | Real ini | Real fim |
|------|--------|--------|----------|----------|----------|---------|
| F2.S1 | Spike + contrato de fila | [ ] | 2026-07-24 09:00 | 2026-07-24 18:00 | | |
| F2.S1.P1 | Mapear eventos offline | [ ] | 2026-07-24 09:00 | 2026-07-24 12:00 | | |
| F2.S1.P2 | Prototipo fila local | [ ] | 2026-07-24 13:00 | 2026-07-24 18:00 | | |

## Fases e tarefas

### F2.S1 — Spike + contrato de fila

- [ ] **F2.S1** Spike + contrato de fila
  Definir contrato de eventos offline, criterios de replay e limites de lote.
  Aceite: documento de contrato revisado + spike rodando em dev.
  Detalhe: [`anexos/F2_S1_contrato_fila-24_07_26.md`](./anexos/F2_S1_contrato_fila-24_07_26.md)
  - inicio: 2026-07-24 09:00
  - fim: 2026-07-24 18:00
  - inicio_real:
  - fim_real:

  - [ ] **F2.S1.P1** Mapear eventos offline
    Criterio: lista de event-types com payload minimo e ordem FIFO.
    - inicio: 2026-07-24 09:00
    - fim: 2026-07-24 12:00
    - inicio_real:
    - fim_real:

  - [ ] **F2.S1.P2** Prototipo fila local
    Criterio: enqueue/dequeue em memoria ou SQLite com teste manual.
    - inicio: 2026-07-24 13:00
    - fim: 2026-07-24 18:00
    - inicio_real:
    - fim_real:
