---
name: guardrails-hexagonal
description: 'Valida limites da arquitetura hexagonal. Use em refatoracao, revisao de adapter, mudanca de porta, pre-merge e pre-release para evitar acoplamento indevido.'
argument-hint: 'Escopo da revisao e arquivos principais'
user-invocable: true
---

# Guardrails Hexagonal

## Quando usar
- Antes de PR importante.
- Antes de release.
- Apos refatoracao estrutural.

## Procedimento
1. Verifique imports proibidos entre camadas.
2. Confirme que regras de negocio estao no dominio.
3. Confirme que portas nao dependem de infraestrutura.
4. Confirme que adaptadores implementam portas sem vazar detalhes.
5. Gere relatorio de desvios e risco.

## Criterio de Conclusao
- Nenhum acoplamento critico entre dominio e infraestrutura.
