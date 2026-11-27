# Sessao 2026-11-27 — Codigos de elemento

## Sumario executivo

F1, F2 e F3 ficaram concluidas. F4.S1 ficou concluida com o relatorio de replicacao do kit. F4 permanece aberta: a homologacao com usuarios-chave e a publicacao da versao nao comecaram. O remoto `main` esta em `ac93cbb`.

## Commits da sessao

F1 a F3 e F4.S1, de `6dfcb81` a `ac93cbb`. O ultimo e `ac93cbb` docs(F4.S1.P6): registra o relatorio da replicacao do kit.

## Problemas

- Dois trechos locais em `scripts/bootstrap-into.sh` e `scripts/upgrade-into.sh` continuam fora do commit. Eles excluem manuais de produto na copia e nao entram neste encerramento.

## Decisoes

- D16 permanece resolvida: so `upgrade-into.sh`; no Windows, Git Bash ou WSL.
- A publicacao `v1.1.0` continua parada ate a homologacao e a autorizacao.

## Proximas acoes

- Homologacao com usuarios-chave.
- F5 so depois dessa homologacao e de autorizacao explicita.
