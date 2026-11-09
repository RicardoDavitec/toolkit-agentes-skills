---
name: commit
description: >-
  Commits padronizados (gitmoji + timestamp PT-BR) com atualizacao obrigatoria
  de planos F/S/P. Use ao commitar, fechar item F/S/P ou apos testes de entrega.
argument-hint: "Opcional: code F/S/P afetado (ex: F2.S4.P5) e resumo curto."
---

# Skill: commit (pmf-dev-kit / produto)

Formato da mensagem:

~~~text
<gitmoji> <tipo>(<escopo>): <descricao-sem-acentos>_DD-MM-AA_hh-mm
~~~

- `tipo`: `feat`, `fix`, `docs`, `refactor`, `test`, `deploy`
- Escopos tipicos: `backend`, `web`, `mobile`, `docs`, `infra`, `db`
  (o produto pode estender em `AGENTS.md`)
- Sem rodape `Refs:` / `Req:` — rastreio pelo code `F#.S#.P#` na descricao
- Timestamp: fuso `America/Sao_Paulo`

Checklist operacional complementar:
`.cursor/skills/commit/FLUXO_COMMIT_CHECKLIST.md`
(em divergencia, **esta skill** prevalece).

Referencias: `AGENTS.md` do produto ·
`docs/05_progresso/planos_ativos/README.md` ·
`docs/06_glpi/HIERARQUIA_F_S_P_GLPI.md`

---

## Gate obrigatorio — planos antes do commit

**Nao commitar codigo de entrega sem atualizar o(s) plano(s)** quando a mudanca
implementa, avanca ou conclui um item `F<n>`, `F<n>.S<n>` ou `F<n>.S<n>.P<n>`.

Regra formal:

~~~text
commit permitido  <=>  (delta_codigo vazio)  OU  (delta_plano nao vazio)  OU  (excecao documentada)
~~~

- `delta_codigo`: arquivos de codigo no stage (`git diff --cached --name-only`)
- `delta_plano`: plano vigente e/ou anexos no **mesmo** commit
- `excecao documentada`: ver secao Excecoes (mensagem ou status)

Em palavras: quem muda codigo precisa mudar o plano no mesmo commit, salvo
excecao registrada. Se a mensagem cita um code, o plano deve mostrar o mesmo
status.

### Quando atualizar

| Situacao | Acao no plano |
|----------|---------------|
| Implementou um **P** | `[ ]`→`[~]`, `%`, `inicio_real` |
| Testou um **P** internamente | `[~]`→`[t]`, `%` 80..99 |
| Concluiu um **P** | `[t]`→`[x]`, `%`=100, `fim_real` |
| Concluiu todos os P de um **S** | fechar o S pai (`[x]`, `%`, `fim_real`) |
| Concluiu todos os S de um **F** | fechar a fase; rodar `glpi-progress-rollup` |
| Aceite formal (F5) | `[x]`→`[A]` + `accept_ref` apontando ao termo |
| Entrega so de docs/plano | commit `docs` sem mudar status de codigo |
| Hotfix sem item no plano | nota em "Concluido nesta sessao" **ou** abrir P; nao deixar orfao |

### Onde atualizar

1. **Plano vigente** (fluxo principal):
   `docs/05_progresso/planos_ativos/<nome>-DD_MM_AA-hh_mm.md`
2. **Anexo da sessao** (detalhe):
   `docs/05_progresso/planos_ativos/anexos/F<n>_S<n>_<slug>-DD_MM_AA.md`
3. **Campos visiveis** (o vazio fica vazio; nao copiar planejado para real):
   ~~~text
   - inicio: ...
   - fim: ...
   - inicio_real: ...
   - fim_real: ...
   ~~~
   Comentario legado (opcional):
   ~~~html
   <!-- glpi: code="F2.S4.P5" plan_start="..." plan_end="..." real_start="..." real_end="..." -->
   ~~~
   Se os quatro campos visiveis existirem, **eles prevalecem** sobre o comentario.

| Marcador | Papel | `%` | `inicio_real` | `fim_real` |
|----------|-------|-----|---------------|------------|
| `[ ]` | todo | 0 | vazio | vazio |
| `[~]` | doing | >0 e <80 | **obrigatorio** | vazio |
| `[t]` | testing | 80..99 | **obrigatorio** | vazio |
| `[x]` | done | 100 | **obrigatorio** | **obrigatorio** |
| `[A]` | closed | 100 | **obrigatorio** | **obrigatorio** + `accept_ref` |

Nunca inventar `inicio_real` / `fim_real`. Sem evidencia, o campo fica vazio.

4. **Sessao** (opcional no mesmo commit): bloco
   "Concluido nesta sessao (DD/MM)" ou skill `encerrar-sessao`.

### Ordem de trabalho do agente

1. Identificar `F<n>.S<n>.P<n>` afetados (argumento, diff, ou `oncoto-oncovo`).
2. **Se o code nao tiver fase** (`S4` em vez de `F2.S4`): plano em v1 →
   sugerir `glpi-migrate-codes --dry-run` antes de prosseguir.
3. Atualizar checklists + `%` do S pai (coerente com o rollup ponderado).
4. Atualizar documentos de apoio afetados (dicionario, ADR, inventario LGPD, runbook).
5. Incluir os `.md` de plano no **mesmo** `git add` do codigo.
6. So entao `git commit` no padrao.
7. Push apenas se o usuario pediu (`exporte`). **Nunca** `--force` em `main`/`master`.
8. Sugerir (nao executar sem pedido):
   ~~~bash
   ./tools/glpi/bin/glpi-commit-harvest --since-last-sync
   ./tools/glpi/bin/glpi-tree-validate --remote --project-code=<CODE>
   ./tools/glpi/bin/glpi-progress-rollup --apply
   ~~~

### Excecoes (documentar no status ou na mensagem)

- Commit **apenas** de formatacao/typo sem impacto de fase.
- Lockfile / arquivos gerados sem mudanca funcional
  (plano so se o P for de deps/infra).
- **Sem plano vigente** em `planos_ativos/` (template/kit): nao inventar plano;
  registrar na mensagem (`excecao gate: sem plano vigente`).
- Secrets / `.env`: **nunca** commitar. Planos nao contem senha, token ou vetor
  sensivel (`safety.deny_content_regex`).

---

## Checklist pre-commit (agente)

- [ ] Code afetado com fase (`F<n>.S<n>.P<n>`) **ou** excecao documentada
- [ ] Planos F/S/P atualizados **ou** justificativa de excecao
- [ ] `inicio_real` / `fim_real` / `%` coerentes com o marcador (nunca inventados)
- [ ] Documentos de apoio afetados atualizados
- [ ] Build/teste da app alterada (quando houver codigo)
- [ ] Sem secrets no stage (`git diff --cached | grep -iE 'token|password'`)
- [ ] Mensagem no padrao gitmoji + tipo + escopo + timestamp PT-BR, **sem acentos**
- [ ] Arquivos da entrega commitados juntos (codigo + planos)

---

## Relacao com outras skills

| Skill | Papel |
|-------|-------|
| `documentar` | updates pontuais de docs; **commit** exige o gate de plano |
| `documente-o-plano` | criar/atualizar plano F/S/P |
| `oncoto-oncovo` | descobrir fase/sessao/tarefa ativa antes de marcar |
| `exporte` | commit (com este gate) + push |
| `encerrar-sessao` | `SESSAO_*` do dia (complementa o checklist) |
| `acompanhar-chamado` | follow-up opcional no Ticket (`[F#.S#.P#] resumo + sha`) |
| `glpi-commit-harvest` | commits → P no GLPI (substitui o espelho manual) |
| `glpi-node-upsert` | ajuste cirurgico de um no (antes: `glpi-task-upsert`) |
| `glpi-progress-rollup` | consolidar `%` e estado para cima apos o commit |
| `glpi-tree-validate` | conferir coerencia antes de qualquer `--apply` |
| `inserir-pendencia` | pendencias atemporais (nao substitui fechar P) |

---

## Exemplos

~~~text
✨ feat(web): shell operacional 4 paineis_05-10-26_13-58
📝 docs(docs): marca F2.S4.P5 em teste apos regressao_05-10-26_14-16
🐛 fix(backend): corrige upsert de cache_05-10-26_15-00
♻️ refactor(infra): skills glpi para modelo f-s-p_05-10-26_11-05
✅ test(backend): cobertura da fila offline F3.S1.P2_05-10-26_16-20
🚀 deploy(infra): homologacao F4.S1 em suporte-homolog_05-10-26_17-00
✨ feat(docs): padrao 12 no template_09-11-26_13-58

excecao gate: sem plano vigente
~~~

Se a mensagem cita um code, o plano correspondente **deve** refletir o mesmo
status no mesmo commit.
