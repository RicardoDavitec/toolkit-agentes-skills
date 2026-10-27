---
name: oncoto-oncovo
description: >-
  Situacao do plano do repositorio em foco (onde estou / onde vou / proximo
  passo), com as tarefas ativas do chamado ITIL desse projeto. Use no inicio
  de sessao, apos milestone ou antes de deploy.
---

# Skill: oncoto-oncovo

Quatro blocos, nesta ordem. So leitura: nao cria tarefa, nao fecha chamado e nao grava no GLPI.

## 1. Onde estou

- Fase atual do plano vigente: `docs/05_progresso/planos_ativos/` (indice `README.md`). Arquivo em `legados/`.
- Branch e sync (`git status -sb`; se houver `github`, mencionar os dois).
- Ambiente (local / intranet / URL do `AGENTS.md` ou `FLUXO_BRANCHES_AMBIENTES.md` **deste** repo).
- Ultimo checkpoint validado.
- Chamado ITIL do projeto, no bloco 3.

## 2. Onde vou

- Proximo item `[ ]` ou `[~]` do vigente.
- Sugestao de continuidade: dentre as tarefas ativas do chamado, a de `begin` mais proximo cujo codigo ainda esta `[ ]` ou `[~]` no plano. Esse e o proximo passo, se o plano nao apontar outro item mais urgente.
- Se o proximo do plano nao tem tarefa no chamado, dizer isso. Nao criar a tarefa nesta skill.
- Se a tarefa ativa mais proxima ja esta `[x]` no plano, tratar como residuo do espelho e nao reabrir o item.
- Dependencias bloqueantes.

## 3. Estado do checklist

Tabela: item | status | criterio. Marcar so com evidencia (codigo + teste).

### Chamado ITIL

Tabela das tarefas ativas: id | estado | inicio | fim | texto.

- Ativa = `state` diferente de 2 (feita).
- Ordenar por `begin`.
- Sem tarefa ativa: escrever "chamado sem tarefa a fazer".
- Nomear o chamado e o ambiente lidos (topo do yaml ou bloco `homolog`).

## 4. Acao imediata

Um proximo passo, o da sugestao de continuidade. Maximo 2 extras alinhados ao plano.

## Fontes

1. `docs/05_progresso/planos_ativos/README.md` + arquivos listados
2. `docs/05_progresso/geral/FLUXO_BRANCHES_AMBIENTES.md` se existir
3. `git log -5 --oneline` e `git status -sb`
4. Tarefas ativas do chamado do projeto em foco

Nao copiar URL/porta do outro produto (SAMU 3700 vs Bot_Pan). Ler `AGENTS.md` do git root.

## Leitura do chamado

O ticket sai de `.glpi/project.yaml` do git root:

- `GLPI_ENV=homolog` usa `homolog.ticket_id`
- sem essa variavel, usa o `ticket_id` do topo

Nao rodar `glpi auth`: o comando imprime o token da sessao.

```bash
./tools/glpi/glpi ticket tasks
./tools/glpi/glpi --env=homolog ticket tasks
```

O comando so consulta. Estado 1 e a fazer. Estado 2 (feita) nao entra na lista.
