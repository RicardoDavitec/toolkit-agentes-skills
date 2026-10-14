---
name: checar-contratos-portas
description: 'Valida contratos entre portas e adaptadores. Use ao reestruturar adapter, mudar assinatura/payload, trocar sender (fake/twilio) ou ajustar tratamento de erro.'
argument-hint: 'Porta alvo e adaptadores envolvidos'
user-invocable: true
---

# Checar Contratos de Portas

## Quando usar
- Mudanca em interfaces de portas.
- Inclusao de novo adaptador.
- Falhas apos refatoracao de integracao.

## Procedimento
1. Liste metodos da porta e assinaturas esperadas.
2. Compare implementacoes nos adaptadores.
3. Verifique compatibilidade de retorno e excecoes.
4. Verifique chamada da camada de aplicacao.
5. Registre incompatibilidades e impacto.

## Criterio de Conclusao
- Todos os adaptadores aderentes a porta sem quebra funcional.
