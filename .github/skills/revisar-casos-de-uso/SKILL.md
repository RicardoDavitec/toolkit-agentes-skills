---
name: revisar-casos-de-uso
description: 'Revisa fluxo de casos de uso na camada de aplicacao. Use em envio em lote, preflight, mudanca de regra de negocio e falhas de orquestracao.'
argument-hint: 'Caso de uso alvo e objetivo da revisao'
user-invocable: true
---

# Revisar Casos de Uso

## Quando usar
- Ajustes em servicos de aplicacao.
- Incidentes de fluxo com multiplas dependencias.
- Preparacao de release.

## Procedimento
1. Mapeie entrada, regras de negocio e saida.
2. Verifique ordem de chamadas externas.
3. Verifique idempotencia e repeticao segura.
4. Verifique tratamento de erro e estado parcial.
5. Proponha correcao minima e validacao.

## Criterio de Conclusao
- Fluxo com previsibilidade, erro tratado e impacto conhecido.
