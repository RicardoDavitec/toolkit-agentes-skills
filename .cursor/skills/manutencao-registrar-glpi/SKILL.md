---
name: manutencao-registrar-glpi
description: >-
  Prepara o chamado de manutenção com o código no título e para na confirmação.
  Use em abrir chamado de manutenção, registrar código no GLPI, título do chamado.
---

# Skill: manutencao-registrar-glpi

## Fluxo

1. O título é `[código] descrição curta`. O assunto do e-mail é esse título.
2. A categoria leva o nome do tipo (`Painel`, `Quadro`, `Janela`, `Modal`, `Formulário`, `Componente`). O id fica no catálogo da instância.
3. Rode a cadeia do `glpi-orquestrador` em dry-run e mostre o diff.
4. Só aplique depois da confirmação explícita. Sem essa frase, não há escrita no GLPI.

## Fronteira

Não invente número de chamado. Não copie plano interno para o repositório público.
