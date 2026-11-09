---
name: doc-gate-fase
description: >-
  Confere o criterio de saida da fase (F1 a F5) e emite o relatorio de fase
  com o que esta pronto, o que falta e os riscos. Use em posso encerrar a
  fase, criterio de saida, relatorio da fase, gate da fase.
argument-hint: "Fase a conferir (ex: F2)."
---

# Skill: doc-gate-fase

Confere o checklist de saida do guia da fase (G04 a G08) contra as evidencias.

## Fluxo

1. Ler o checklist da fase no guia correspondente.
2. Para cada item, buscar evidencia: documento aprovado, plano com `[x]`,
   commit, ata, resultado de teste.
3. Rodar `doc-lint` e, se houver GLPI, sugerir `glpi-tree-validate`.
4. Classificar cada item como **atendido**, **parcial** ou **nao atendido**,
   citando o arquivo ou commit que prova.
5. Gravar `docs/05_progresso/geral/rel_<fase>_<slug>.md` com o resultado e
   os riscos residuais.
6. Concluir: **pode encerrar**, **pode encerrar com pendencias** ou **nao pode**.

## Regras

- Sem evidencia, o item nao esta atendido.
- Nao encerra a fase nem altera o plano. Quem fecha F, S e P e o `glpi-escriba`.

