---
name: doc-rastreabilidade
description: >-
  Gera a matriz de rastreabilidade requisito, tarefa, commit, teste e
  homologacao e calcula a cobertura. Use em matriz de rastreabilidade,
  cobertura dos requisitos, requisito sem teste, fechar a F3.
argument-hint: "Opcional: fase ou intervalo de datas."
---

# Skill: doc-rastreabilidade

Grava `docs/01_requisitos/rastreabilidade.md`.

## Fluxo

1. Rodar `scripts/docs/gerar_rastreabilidade.py` quando existir. Sem o script,
   avisar e montar a matriz manualmente.
2. Fontes: `REQ-` e `RN-` citados nos planos e anexos, codes `F#.S#.P#` na
   mensagem dos commits (`git log`), casos de teste e atas.
3. Destacar: requisito sem tarefa, tarefa sem commit, requisito sem teste.
4. Informar a cobertura $$C_{rast} = R_{cob} / R_{tot} \times 100$$.

Onde:
- $$C_{rast}$$ (Cobertura de Rastreabilidade): percentual de requisitos com tarefa, commit e teste.
- $$R_{cob}$$ (Requisitos cobertos): requisitos com os tres vinculos.
- $$R_{tot}$$ (Requisitos totais): requisitos aprovados do projeto.

## Regras

- Nao inventar vinculos. Sem evidencia, a celula fica vazia.
- Nao altera planos. Lacunas viram sugestao de P para o `glpi-escriba`.
