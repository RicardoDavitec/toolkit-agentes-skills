# Fluxo de commit e validação

Checklist de entrega no modelo **F/S/P**. Complementa a skill `commit` (`.cursor/skills/commit/SKILL.md`), que é a fonte canônica das regras. Em caso de divergência, vale a skill.

Hierarquia: `docs/06_glpi/HIERARQUIA_F_S_P_GLPI.md`.

Onde:
- F (Fase): `F1` a `F5` (planejamento, implementação, testes internos, homologação, aprovação).
- S (Sessão, semana ou sprint): janela de tempo dentro de uma fase, por exemplo `F2.S4`.
- P (Pacote de tarefa, cerca de 2 h): item ancorado em commit, por exemplo `F2.S4.P5`.
- C (Chamado) e R (Requisição, que é um projeto): aparecem só no cabeçalho do plano, nunca no code do item.

## 1. Gate de plano (regra central)

```text
commit permitido  <=>  (delta_codigo vazio)  OU  (delta_plano nao vazio)  OU  (excecao documentada)
```

Onde:
- `delta_codigo`: arquivos de código incluídos no commit (`git diff --cached --name-only`).
- `delta_plano`: arquivos de plano incluídos no mesmo commit (plano vigente e anexos).
- `excecao documentada`: uma das exceções da seção 5 (tipografia/lockfile, sem plano vigente, etc.), registrada na mensagem ou no status.
- `<=>`: "se e somente se".

Em palavras: quem muda código precisa mudar o plano **no mesmo commit**, salvo exceção documentada. Se a mensagem cita um code, o plano deve mostrar o mesmo status.

## 2. Checklist antes de commitar

- [ ] Identifiquei o code afetado, com fase (`F2.S4.P5`). Em dúvida, usar a skill `oncoto-oncovo`
- [ ] Se o plano ainda usa code sem fase (`S4`), rodar antes: `./tools/glpi/bin/glpi-migrate-codes --dry-run`
- [ ] Rodei build e testes da aplicação alterada
- [ ] **Atualizei o plano** (obrigatório se a entrega avança ou conclui um `F<n>`, `F<n>.S<n>` ou `F<n>.S<n>.P<n>`):
  - plano vigente em `docs/05_progresso/planos_ativos/<nome>-DD_MM_AA-hh_mm.md`
  - anexo da sessão em `docs/05_progresso/planos_ativos/anexos/F<n>_S<n>_<slug>-DD_MM_AA.md`
  - marcador, `%`, `inicio_real` e `fim_real` coerentes (tabela da seção 3)
  - `%` do S pai coerente com o rollup ponderado
- [ ] Documentos de apoio afetados foram atualizados (dicionário de dados, ADR, inventário LGPD, runbook)
- [ ] Os arquivos de plano estão no **mesmo** `git add` do código
- [ ] Nenhum segredo no stage: `git diff --cached | grep -iE 'token|password'`
- [ ] Mensagem no padrão da seção 4

## 3. Marcadores, percentual e datas reais

| Marcador | Papel | `%` | `inicio_real` | `fim_real` |
|---|---|---|---|---|
| `[ ]` | todo (a fazer) | 0 | vazio | vazio |
| `[~]` | doing (em andamento) | maior que 0 e menor que 80 | **obrigatório** | vazio |
| `[t]` | testing (em teste) | 80 a 99 | **obrigatório** | vazio |
| `[x]` | done (concluído) | 100 | **obrigatório** | **obrigatório** |
| `[A]` | closed (aceite formal) | 100 | **obrigatório** | **obrigatório**, com `accept_ref` |

Onde:
- `%` (percentual de conclusão): para `[t]` e `[x]` vem da skill `commit`. A faixa de `[~]` é a leitura coerente com elas.
- `inicio_real` e `fim_real`: datas realizadas, vindas do commit ou da sessão. **Nunca inventar.** Sem evidência, o campo fica vazio.
- `accept_ref` (referência do aceite): termo, ata ou parecer que comprova o aceite.

### Quando atualizar

| Situação | Ação no plano |
|---|---|
| Implementou um P | `[ ]` para `[~]`, `%`, `inicio_real` |
| Testou um P internamente | `[~]` para `[t]`, `%` entre 80 e 99 |
| Concluiu um P | `[t]` para `[x]`, `%` igual a 100, `fim_real` |
| Concluiu todos os P de um S | Fechar o S pai (`[x]`, `%`, `fim_real`) |
| Concluiu todos os S de uma F | Fechar a fase e rodar `glpi-progress-rollup` |
| Aceite formal (F5) | `[x]` para `[A]` com `accept_ref` |
| Entrega só de documentação ou plano | Commit `docs`, sem mudar o status de código |
| Hotfix sem item no plano | Nota em "Concluído nesta sessão" **ou** abrir um P. Não deixar órfão |

### Formato dos quatro campos visíveis

O vazio fica vazio. Não copie o planejado para o real.

```text
- [~] **F2.S4.P5** titulo da tarefa
  - inicio: 2026-11-09 14:00
  - fim: 2026-11-09 16:00
  - inicio_real: 2026-11-09 14:10
  - fim_real:
```

O comentário `<!-- glpi: code="F2.S4.P5" plan_start="..." plan_end="..." real_start="..." real_end="..." -->` continua válido em plano antigo. Se os quatro campos visíveis existirem, eles prevalecem.

## 4. Mensagem de commit

```text
<gitmoji> <tipo>(<escopo>): <descricao-sem-acentos>_DD-MM-AA_hh-mm
```

Onde:
- `gitmoji`: emoji que indica a natureza da mudança.
- `tipo`: `feat`, `fix`, `docs`, `refactor`, `test`, `deploy`.
- `escopo`: `backend`, `web`, `mobile`, `docs`, `infra`, `db` (o produto pode estender no `AGENTS.md`).
- `descricao-sem-acentos`: texto curto, **sem acentos**. Cite o code `F#.S#.P#` quando o commit mexe em um item do plano.
- `DD-MM-AA_hh-mm`: dia, mês, ano de dois dígitos, hora e minuto.

Exemplos:

```text
✨ feat(web): shell operacional 4 paineis_05-10-26_13-58
📝 docs(docs): marca F2.S4.P5 em teste apos regressao_05-10-26_14-16
🐛 fix(backend): corrige upsert de cache_05-10-26_15-00
✅ test(backend): cobertura da fila offline F3.S1.P2_05-10-26_16-20
🚀 deploy(infra): homologacao F4.S1 em suporte-homolog_05-10-26_17-00
```

Não há rodapé `Refs:` nem `Req:`. A rastreabilidade vem do code na descrição.

## 5. Exceções (registrar no status ou na mensagem)

- Commit **só** de formatação ou erro de digitação, sem impacto de fase.
- Arquivo de dependências travadas (lockfile) ou arquivo gerado, sem mudança funcional. O plano só entra se o P for de dependências ou infraestrutura.
- **Sem plano vigente** em `planos_ativos/` (template/kit): não inventar plano; registrar na mensagem (`excecao gate: sem plano vigente`).
- Segredos e `.env`: **nunca** commitar. Planos não contêm senha, token ou dado sensível.


## 6. Depois do commit

- [ ] Push **somente se o usuário pediu** (skill `exporte`). Nunca usar `--force`
- [ ] Promoção entre ambientes (teste, homologação, `main`): seguir a regra do `AGENTS.md` do produto
- [ ] Sugerir, sem executar sem pedido:

```bash
./tools/glpi/bin/glpi-commit-harvest --since-last-sync
./tools/glpi/bin/glpi-tree-validate --remote --project-code=<CODE>
./tools/glpi/bin/glpi-progress-rollup --apply
```

- [ ] Follow-up (acompanhamento) no chamado, **opcional**: skill `acompanhar-chamado`, com texto no formato `[F2.S4.P5] resumo da entrega + sha do commit + próximo passo`
- [ ] ProjectTask do GLPI atualizada: o `glpi-commit-harvest` fecha os P a partir dos commits. Para ajuste pontual de um nó, usar a skill `glpi-node-upsert`

Os dois ciclos são diferentes:
- O **follow-up** fecha a auditoria local com o suporte institucional (chamado do projeto).
- A **ProjectTask** fecha o plano local (F/S/P) com a gestão de entrega no Project.

## 7. Fim de sessão

1. Plano e anexo atualizados (seção 2).
2. Pendências registradas (skill `inserir-pendencia`).
3. Skill `encerrar-sessao`: cria `SESSAO_AAAA-MM-DD_<DESCRICAO>.md` em `docs/05_progresso/geral/` e pergunta sobre commit, push, anexo ao GLPI e backup.
4. Plano encerrado ou substituído vai para `legados/` com `git mv`, **no mesmo ciclo**, junto com os anexos.

## 8. Comandos rápidos

```bash
# Ajuste aos scripts do produto
npm run build:backend   # se existir
npm run build:web       # se existir
curl http://localhost:3700/health   # se houver API local

# Conferir o que entra no commit (gate de plano)
git diff --cached --name-only

# Validar a documentação antes de commitar docs
python3 scripts/docs/lint_docs.py
python3 scripts/lint_template.py
```

## 9. Skills relacionadas

| Skill | Papel |
|---|---|
| `commit` | Regras de mensagem e gate de plano (fonte canônica) |
| `documente-o-plano` | Criar e atualizar o plano F/S/P |
| `oncoto-oncovo` | Descobrir fase, sessão e tarefa ativa antes de marcar |
| `exporte` | Commit com o gate, mais push |
| `encerrar-sessao` | Registro `SESSAO_*` do dia |
| `inserir-pendencia` | Pendências atemporais (não substitui fechar P) |
| `glpi-commit-harvest` | Commits viram P no GLPI |
| `glpi-progress-rollup` | Consolida `%` e estado para cima |
| `glpi-tree-validate` | Confere a coerência antes de qualquer `--apply` |
| `glpi-node-upsert` | Ajuste cirúrgico de um nó (antes: `glpi-task-upsert`) |
| `acompanhar-chamado` | Follow-up no chamado (alias legado: `glpi-followup`) |
