---
name: manutencao-migrar-legado
description: >-
  Mapeia elementos de um projeto antigo para o registro de códigos, sem
  sobrescrever registro, escala ou histórico. Use em migrar legado, importar
  códigos antigos, preservar dados na atualização.
---

# Skill: manutencao-migrar-legado

## Fluxo

1. Leia a estrutura antiga e proponha o mapeamento para `registro-codigos.json`.
2. Use `python3 scripts/manutencao/migrar_legado.py` quando o arquivo existir. Se não existir, pare e não invente o mapeamento no registro.
3. Não sobrescreva registro, escala nem histórico já gravados.
4. Mostre o diff e espere confirmação antes de gravar.

## Fronteira

A preservação no `bootstrap-into.sh` e no `upgrade-into.sh` não entra nesta skill enquanto a decisão do equivalente Windows estiver aberta.
