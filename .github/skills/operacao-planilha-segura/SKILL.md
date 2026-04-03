---
name: operacao-planilha-segura
description: 'Executa operacoes em planilhas com seguranca operacional. Use para escrita em lote, persistir qrcode, atualizar status, dry-run e validacao pos-escrita.'
argument-hint: 'Aba alvo, tipo de operacao e volume'
user-invocable: true
---

# Operacao Planilha Segura

## Quando usar
- Atualizacao em lote.
- Persistencia de QR codes.
- Mudanca de status de convidados.

## Procedimento
1. Rodar dry-run e registrar impacto previsto.
2. Validar cabecalho e estrutura da aba.
3. Confirmar estrategia de backup antes de escrita real.
4. Executar escrita com log estruturado.
5. Validar integridade pos-escrita.

## Criterio de Conclusao
- Escrita concluida sem perda estrutural, com log e validacao final.
