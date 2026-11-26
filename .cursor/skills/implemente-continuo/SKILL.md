---
name: implemente-continuo
description: >-
  Executa o plano vigente sem pausa entre tarefas P: checklist e commit ao
  fim de cada P, e o proximo P no mesmo turno. Pausa so em circunstancia
  especial no fim de cada S e no fim de cada F. No fim do plano, sugere
  implementar as pendencias registradas nesse ciclo. Use quando o usuario
  pedir implemente o plano no modelo continuo, implemente continuamente,
  modo continuo, ou esta skill pelo nome.
argument-hint: "Codigo inicial opcional (ex: F1.S1.P7). Vazio = primeiro P aberto do plano vigente."
---

# Skill: Implemente o plano no modelo contínuo

Executa o plano vigente em `docs/05_progresso/planos_ativos/` (índice `README.md`), no formato da skill `documente-o-plano`. Não substitui `implemente`.

## O que é contínuo

Implementar continuadamente significa **sem pausa entre as tarefas P**. Checklist, commit e a linha de andamento acontecem, e o próximo P aberto começa em seguida, no mesmo turno. A resposta ao usuário não encerra o trabalho.

Enquanto esta skill estiver ativa, ela prevalece sobre a ordem de resposta que pede "resultado, estado do plano e próximo item". É proibido terminar o turno com "próximo item", "posso seguir", "a fase continua aberta" ou um relatório que espera o usuário, se ainda houver P aberto e nenhuma pausa permitida.

Pausa só em **circunstância especial**, e só nestes marcos:

- fim de uma S
- fim de uma F

Fora desses marcos, a próxima ação depois do commit do P é o P seguinte.

## Diretivas (verbatim)

Crie a SKILL  "Implemente o plano no modelo contínuo" Seguindo o procedimento a seguir:
1. Implemente continuamente  o planejamentocom com retorno de andamento mínimo.
1.1. Continuamente significa sem pausa entre tarefas P. A pausa só ocorre em circunstância especial no fim de cada S e no fim de cada F.
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
4. Ao final de cada fase "F", quando todas as S da fase estiverem fechadas: preencher o checklist da fase, conferir o critério de saída, consolidar o percentual, commit e push.
4.1. Pausa no fim da F só em circunstância especial: o gate não permite encerrar, o aceite de homologação ou de produção depende da pessoa, ou ainda falta deploy no servidor ou APK/AAB que dependa da pessoa.
4.2. Sem essa circunstância, abrir a próxima F no mesmo turno.

## Leitura operacional

- **P** = tarefa `F#.S#.P#`. **S** = a sessão pai (`F#.S#`). **F** = a fase pai (`F#`). Um extra com critério de aceite conta como P.
- Andamento mínimo: uma linha por P (`código [x]` ou `código bloqueado: motivo`), uma linha no fechamento da S e uma linha no fechamento da F. A linha não é o fim do turno. Sem relato de ferramenta, sem perguntar o próximo P.
- Não pular P. Não abrir a próxima S antes de fechar a atual. Não abrir a próxima F antes de fechar a atual.
- Secrets, `.env` e keystore nunca no commit.

## Loop de cada P

1. Marcar `[~]` com `real_start` (agora). Implementar só o critério daquele P.
2. Falha dentro do critério: corrigir no mesmo P.
3. Necessidade fora do critério: skill `inserir-pendencia`, salvo pré-requisito para continuar. Pré-requisito: corrigir na hora ou inserir um P novo no plano vigente, na posição que destrava o restante com menos retrabalho. Registrar a escolha na linha de andamento.
4. Ao final da implementação do P: preencher e atualizar os checklists dos planos ativos em implementação (`docs/05_progresso/planos_ativos/`, índice `README.md`, e o anexo da S quando o P o alterar). Marcar o P `[x]`, `%` 100 e `fim_real` / `real_end`. A S pai fica `[~]` até o último P. A F pai fica `[~]` até a última S. Esse delta do plano entra no commit do P.
5. Skill `commit`: um commit por P, mensagem cita o código. Sem push no meio da S.
6. No mesmo turno, começar o próximo P aberto da S. Se a S acabou, ir ao fechamento da S. Não responder ao usuário só com o status deste P.

## Fechamento de cada S

Quando todos os P da S estiverem `[x]`:

1. Decidir o teste (3.1), nesta ordem, e executar só o que a S exige:
   - S só de documentação: sem build e sem reinício.
   - Checagem local sem serviço: `tsc`/build da app alterada, ou dry-run em background (3.1.1). Não subir container nesta estação.
   - Teste que depende da pessoa (aparelho, login, aceite): propor o roteiro interativo (3.1.2) e seguir os outros P que não dependam dele. Não marcar a S `[x]` enquanto o aceite exigido pelo critério estiver pendente.
   - Build e reinício de containers (3.1.3): skill `commit` + skill `sincronize` (push). Entregar o comando de pull, build e up **no servidor**. Quem executa é o usuário (skill `deploy-backend`). Proibido `docker compose up` nesta estação.
   - APK (3.1.4): skill `build-mobile` no WSL e `adb install` no PowerShell do Windows. Não instalar pelo WSL.
   - AAB (3.1.4): procedimentos de nova versão na Play Store do projeto, com `versionName` e `versionCode` nas normas do repositório (não inventar versão).
2. Documentar testes e correções (skill `documentar`; falha de build/deploy: `registrar-tentativa`).
3. Marcar a S `[x]` com `real_end` quando o teste cabível estiver feito. Preencher o checklist da S nos planos ativos.
4. Skill `encerrar-sessao` sem as perguntas de commit, push, anexo GLPI e backup: o commit e o push desta skill já estão mandados. Gravar o `SESSAO_*` e seguir.
5. Skill `commit` da sessão e das correções. Skill `sincronize` (3.3).
6. Pausa só se houver circunstância especial (lista abaixo). Sem ela, no mesmo turno, abrir a próxima S da mesma F. Se esta era a última S da F, ir ao fechamento da F.

### Circunstância especial no fim da S

Parar somente nestes casos. Nomear o código da S e o motivo, numa linha:

- O critério de aceite exige a pessoa (3.1.2) e não há outro P independente para seguir.
- A S só pode ser marcada `[x]` depois do build e reinício no servidor (3.1.3): comandos já entregues, à espera da saída.
- APK ou AAB depende da pessoa no aparelho ou na Play Store (3.1.4), e o que dava para fazer nesta estação já foi feito.
- Bloqueio: segredo ausente, decisão que o plano não cobre, ou ferramenta indisponível.

S só de documentação, ou S cujo `tsc`/dry-run passou, **não** é pausa. Fechar e continuar.

## Fechamento de cada F

Quando todas as S da F estiverem `[x]` (diretiva 4):

1. Preencher o checklist da F nos planos ativos em implementação: marcador, `%` e `fim_real`. O `%` da F sai das S (esforço), não de conta manual solta. Se existir `tools/glpi/bin/glpi-progress-rollup`, rodar a skill `glpi-progress-rollup`. Se o binário não existir, calcular no plano e registrar isso na linha de andamento.
2. Gate da fase, skill `doc-gate-fase`, contra o DoD do guia daquela F (G04 a G08; resumo em G01 §8). Gravar o relatório em `docs/05_progresso/geral/`.
3. Tratar o resultado do gate:
   - **Pode encerrar:** marcar a F `[x]`, `%` 100, `fim_real`.
   - **Pode encerrar com pendências** que não bloqueiam a próxima F: skill `inserir-pendencia` para o que ainda não estiver na lista, marcar a F `[x]` e seguir.
   - **Não pode**, ou pendência que bloqueia a próxima F: esta é circunstância especial. Listar o que falta e parar. Não abrir a próxima F.
4. Skill `commit` do fechamento da F. Skill `sincronize`.
5. Outras circunstâncias especiais neste marco (além do gate):
   - F4: homologação com o usuário final ou ata ainda por fazer.
   - F5: `accept_ref` ou acompanhamento que exige a pessoa.
   - Deploy no servidor ou APK/AAB da fase ainda não entregue, se a última S não tiver pausado por isso. Vale o mesmo procedimento 3.1.3 ou 3.1.4, uma vez por fase.
6. Sem circunstância especial, no mesmo turno, abrir a primeira S aberta da próxima F.
7. Se não houver próxima F, ir ao fim do plano.

## Fim do plano

Depois da última F (3.4), com a última S já fechada:

1. Resumo da implementação em `docs/05_progresso/geral/`.
2. Skill `encerrar-sessao`.
3. Skill `commit`. Skill `sincronize`.
4. Pendências deste ciclo (3.5): ler `docs/05_progresso/pendencias/CHECKLIST_PENDENCIAS.md` e listar só os itens ainda abertos (`[ ]` ou `[~]`) inseridos durante esta implementação (skill `inserir-pendencia`). Sugerir implementá-los em seguida, na ordem do checklist, com o id `PEND-…` e uma linha do que cada um pede. Se não houver item aberto deste ciclo, dizer isso. Não começar essa implementação: a sugestão encerra o plano; a execução só começa com o aceite.

## Relação com outras skills

| Skill | Quando |
|-------|--------|
| `implemente` | O mesmo plano, com parada e relato entre tarefas |
| `commit` | Fim de cada P (checklist dos planos ativos já atualizado), fim de cada S, fim de cada F, fim do plano |
| `encerrar-sessao` | Fim de cada S e fim do plano, sem perguntar commit/push no meio do contínuo |
| `inserir-pendencia` | Correção que não é pré-requisito; no fim da F, pendência que não bloqueia; no fim do plano, sugerir implementar as abertas deste ciclo |
| `doc-gate-fase` | Critério de saída ao fechar cada F |
| `glpi-progress-rollup` | Percentual da F a partir das S, quando o binário existir |
| `documentar` / `registrar-tentativa` | Testes e falhas do fechamento da S |
| `build-mobile` / `empacotar-apk` | APK no fechamento da S ou da F |
| `deploy-backend` | Pull, build e up no servidor, depois do push |
| `sincronize` | Push no fim da S, no fim da F, no 3.1.3 e no fim do plano |
