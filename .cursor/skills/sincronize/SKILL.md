---
name: sincronize
description: >-
  Equaliza git local e remotos do repositorio em foco. Se existir remote
  `github` e/ou `gitness`, local = origin = cada espelho no mesmo SHA.
  Senao, local = origin.
  Use em sincronize, sincronizar repositorios, equalizar Gitness e GitHub,
  atualizar git, deixar local e remoto iguais.
argument-hint: "Vazio — equaliza o branch ativo."
---

# Skill: sincronize

Equaliza o **git root em foco** (pedido no plural: repetir em cada root do workspace).

Pedido de sincronizar **ja autoriza** commit da entrega local (exceto secrets/lixo) + pull + push. Nao parar no meio sugerindo so `exporte`/`importe`.

Alias: `atualizar` segue este arquivo.

## 1. Detectar espelhos

```bash
git rev-parse --show-toplevel
git branch --show-current
git remote -v
```

| Remotes | Gate de sucesso |
|---------|-----------------|
| `origin` + `github` | `HEAD == origin/$BR == github/$BR` |
| `origin` + `gitness` | `HEAD == origin/$BR == gitness/$BR` |
| `origin` + `github` + `gitness` | os tres SHAs iguais |
| so `origin` | `HEAD == origin/$BR` |

Nao inventar remote `github` nem `gitness`. Se `.github/skills/REMOTOS_ESPELHO.md` existir, respeitar a ordem origin, depois github, depois gitness. `origin` e o mestre; `github` e `gitness` sao espelhos quando existirem.

Branch: o **atual**. Nao assumir `teste-sigs-samu-operacional` se o checkout for outro.

**Fora de escopo:** atualizar checkout no servidor `172.21.31.167` so porque houve push.

## 2. Diagnostico

```bash
BR=$(git branch --show-current)
git fetch origin
git remote get-url github >/dev/null 2>&1 && git fetch github
git remote get-url gitness >/dev/null 2>&1 && git fetch gitness
git status -sb
git log --oneline origin/$BR..HEAD
git log --oneline HEAD..origin/$BR
git diff --stat
# se houver github:
git log --oneline github/$BR..HEAD
git log --oneline HEAD..github/$BR
git log --oneline origin/$BR..github/$BR
git log --oneline github/$BR..origin/$BR
# se houver gitness:
git log --oneline gitness/$BR..HEAD
git log --oneline HEAD..gitness/$BR
git log --oneline origin/$BR..gitness/$BR
git log --oneline gitness/$BR..origin/$BR
```

## 3. Commit se dirty (entrega)

Skill `commit`. Incluir `.md` de plano da entrega. Nunca `.env`, credenciais, `.auth/`, `node_modules`, `*.tar.gz`, APK. Sem entrega: nao commit vazio. Relatar lixo restante.

## 4. Integrar remotos → local

- Merge `origin/$BR` (`--no-edit`; ff se possivel).
- Se existir `github` e SHA diferente: merge `github/$BR` tambem.
- Se existir `gitness` e SHA diferente: merge `gitness/$BR` tambem.
- Atalho um remote, so atras: `git pull --ff-only origin "$BR"`.
- Conflito: listar arquivos, **parar**, nao auto-resolver.

## 5. Push

```bash
git push origin "$BR"
git remote get-url github >/dev/null 2>&1 && git push github "$BR"
git remote get-url gitness >/dev/null 2>&1 && git push gitness "$BR"
```

**origin primeiro** (mestre), depois `github` e `gitness` se existirem. Todos os que existirem. Nunca `--force` / `--force-with-lease`. Um falhou → sync incompleto.

## 6. Verificar

Fetch de novo. SHA do gate identicos. Se nao, repetir 4–5 **uma** vez; ainda diferente: tabela ahead/behind e parar.

## Relatorio

Branch, SHA (local e cada remote), push OK por remote, lixo nao commitado.

## Proibido

`--force`, `reset --hard`, `rebase -i`, descartar working tree, commitar secrets.

## Delegacao

`commit` para mensagem. `exporte`/`importe` sao pecas unidirecionais — nao substituem este skill quando o pedido e equalizar.
