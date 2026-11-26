---
name: implemente-continuo
description: >-
  Executa o plano vigente em sequencia, com retorno de andamento minimo,
  commit ao fim de cada tarefa P, com o checklist dos planos ativos
  preenchido e atualizado, sessao e teste ao fim de cada S, e push
  no fechamento. No fim do plano, sugere implementar as pendencias
  registradas nesse ciclo. Use quando o usuario pedir implemente o plano no
  modelo continuo, implemente continuamente, modo continuo, ou esta skill pelo nome.
argument-hint: "Codigo inicial opcional (ex: F1.S1.P7). Vazio = primeiro P aberto do plano vigente."
---

# Skill: Implemente o plano no modelo contínuo

Executa o plano vigente em `docs/05_progresso/planos_ativos/` (índice `README.md`), no formato da skill `documente-o-plano`. Não substitui `implemente`: esta skill não para entre tarefas para relatar, e o push segue o fechamento da S e o fim do plano.

## Diretivas (verbatim)

Crie a SKILL  "Implemente o plano no modelo contínuo" Seguindo o procedimento a seguir:
1. Implemente continuamente  o planejamentocom com retorno de andamento mínimo.
2. Commit a o final de cada tarefa "P";
2.1. Ao final da implementação de cada "P", preencher e atualizar os checklists dos planos ativos em implementação.
3. Encerre a sessão e commita ao final de cada Sessão "S"
3.1. Verifique a necessidade de teste ao final de cada "S", considerando a necessidade ou não de build e reinicalização de ambientes.
3.1.1. Se possivel teste em dryrun, em background;
3.1.2. Se necessário sugira processo de teste interativo comigo.
3.1.3. Se necessitar Build e reinicialização de containers: Fazer commit e push e orientar pull , build e up a partir do servidor.
3.1.4. Se necessitar de build de APK ou ABB. Executar build na máquina local e instalação conforme skill de build de APK, através de adb no powershell do windows local, ou, no caso de AAB, seguindo procedimentos para nova versão no google play store. Manter versionamento registrado conforme normas do projeto.
3.2. Se surgirem necessidades de alterações, correções e criação de novos códigos, incerir como item na lista vigente de pendências, execeto se a alteração seja necessária como pré requisito para continuar a implementação. Nesse caso consirede alteração imediata ou inserção de novo item no plano de ação vigente, estratégicamente colocado para maximizar a eficiência da implementação.
3.3. documente os trestes e correções, commit e push.
3.4. Ao final da implementação geral, depois do último "S" , apresente e documente resumo da implementação encerre a sessão, commit e push.
3.5. Ao final, depois do resumo, sessão, commit e push, sugerir a implementação das pendências registradas ao longo do processo na lista vigente de pendências. Não iniciá-las antes do aceite.

## Leitura operacional

- **P** = tarefa `F#.S#.P#`. **S** = a fase pai (`F#.S#`). Um extra com critério de aceite conta como P.
- Andamento mínimo: uma linha por P (`código [x]` ou `código bloqueado: motivo`) e uma linha no fechamento da S. Sem relato de ferramenta, sem perguntar o próximo P.
- Não pular P. Não abrir a próxima S antes de fechar a atual (teste cabível + sessão + push).
- Secrets, `.env` e keystore nunca no commit.

## Loop de cada P

1. Marcar `[~]` com `real_start` (agora). Implementar só o critério daquele P.
2. Falha dentro do critério: corrigir no mesmo P.
3. Necessidade fora do critério: skill `inserir-pendencia`, salvo pré-requisito para continuar. Pré-requisito: corrigir na hora ou inserir um P novo no plano vigente, na posição que destrava o restante com menos retrabalho. Registrar a escolha na linha de andamento.
4. Ao final da implementação do P: preencher e atualizar os checklists dos planos ativos em implementação (`docs/05_progresso/planos_ativos/`, índice `README.md`, e o anexo da S quando o P o alterar). Marcar o P `[x]`, `%` 100 e `fim_real` / `real_end`. A S pai fica `[~]` até o último P. Esse delta do plano entra no commit do P.
5. Skill `commit`: um commit por P, mensagem cita o código. Sem push no meio da S.

## Fechamento de cada S

Quando todos os P da S estiverem `[x]`:

1. Decidir o teste (3.1), nesta ordem, e executar só o que a S exige:
   - S só de documentação: sem build e sem reinício.
   - Checagem local sem serviço: `tsc`/build da app alterada, ou dry-run em background (3.1.1). Não subir container nesta estação.
   - Teste que depende da pessoa (aparelho, login, aceite): propor o roteiro interativo (3.1.2) e seguir para os outros P que não dependam dele. Não marcar a S `[x]` enquanto o aceite exigido pelo critério estiver pendente.
   - Build e reinício de containers (3.1.3): skill `commit` + skill `sincronize` (push). Entregar o comando de pull, build e up **no servidor**. Quem executa é o usuário (skill `deploy-backend`). Proibido `docker compose up` nesta estação.
   - APK (3.1.4): skill `build-mobile` no WSL e `adb install` no PowerShell do Windows. Não instalar pelo WSL.
   - AAB (3.1.4): procedimentos de nova versão na Play Store do projeto, com `versionName` e `versionCode` nas normas do repositório (não inventar versão).
2. Documentar testes e correções (skill `documentar`; falha de build/deploy: `registrar-tentativa`).
3. Marcar a S `[x]` com `real_end`.
4. Skill `encerrar-sessao`.
5. Skill `commit` da sessão e das correções. Skill `sincronize` (3.3).

## Fim do plano

Depois da última S (3.4):

1. Resumo da implementação em `docs/05_progresso/geral/`.
2. Skill `encerrar-sessao`.
3. Skill `commit`. Skill `sincronize`.
4. Pendências deste ciclo (3.5): ler `docs/05_progresso/pendencias/CHECKLIST_PENDENCIAS.md` e listar só os itens ainda abertos (`[ ]` ou `[~]`) inseridos durante esta implementação (skill `inserir-pendencia`). Sugerir implementá-los em seguida, na ordem do checklist, com o id `PEND-…` e uma linha do que cada um pede. Se não houver item aberto deste ciclo, dizer isso. Não começar essa implementação: a sugestão encerra o plano; a execução só começa com o aceite.

## Relação com outras skills

| Skill | Quando |
|-------|--------|
| `implemente` | O mesmo plano, com parada e relato entre tarefas |
| `commit` | Fim de cada P (checklist dos planos ativos já atualizado), fim de cada S, fim do plano |
| `encerrar-sessao` | Fim de cada S e fim do plano |
| `inserir-pendencia` | Correção que não é pré-requisito; no fim do plano, sugerir implementar as abertas deste ciclo |
| `documentar` / `registrar-tentativa` | Testes e falhas do fechamento da S |
| `build-mobile` / `empacotar-apk` | APK no fechamento da S |
| `deploy-backend` | Pull, build e up no servidor, depois do push |
| `sincronize` | Push no fim da S, no 3.1.3 e no fim do plano |
