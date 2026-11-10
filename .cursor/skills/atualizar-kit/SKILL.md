---
name: atualizar-kit
description: "Verifica atualizacoes no toolkit-agentes-skills e sincroniza tools/skills/docs no repositorio produto que chamou. Use quando o usuario pedir atualizar kit, sync kit, upgrade kit ou sincronizar o template."
argument-hint: "Opcional: --profile=pmf-core|full-skeleton|glpi-only · --check-only · caminho do kit"
---

# Skill: atualizar-kit

Sincroniza o **produto atual** (repo que chamou) com novidades do **toolkit-agentes-skills** sem apagar `.glpi/project.yaml` / state.

## Gatilhos

- "atualizar kit", "sync kit", "upgrade kit", "sincronizar toolkit-agentes-skills"

## Fluxo obrigatorio

1. **Resolver dirs**
   - `TARGET` = raiz do repositorio produto (`git rev-parse --show-toplevel` ou cwd do produto).
   - `KIT` = clone do toolkit-agentes-skills (ver resolucao abaixo).
2. **Checar branches (kit + destino) antes de qualquer escrita**
   ```bash
   python3 "$KIT/scripts/atualizar_kit.py" --target="$TARGET" --check-only
   # ou:
   "$KIT/scripts/procedimento_atualizar_template.sh" --target="$TARGET" --check-only
   ```
   O script faz `git fetch` em `origin` (e `github`/`gitness` se existirem) no **kit** e no **destino**.
   - Se o **destino** estiver atras do remoto → **bloquear** apply. Orientar skill `sincronize` / `git pull --ff-only`.
   - Se o **kit** estiver atras de `origin` → **bloquear** apply (ou `--pull-kit` se working tree do kit limpa).
   - Working tree suja: avisar, nao bloquear so por isso.
3. **Se houver commits novos no remoto do kit** (ou working tree do kit mais nova que a ultima sync):
   - Mostrar resumo (`git log` curto do kit).
   - Confirmar com o usuario antes de gravar no produto (exceto se `--yes`).
4. **Aplicar sync** (so depois do gate de branch)
   ```bash
   "$KIT/scripts/atualizar-kit" --target="$TARGET" --profile=full-skeleton --yes
   ```
   Perfil default sugerido: o mesmo ja usado no produto (`full-skeleton` se existir `docs/00_visao_geral`; senao `pmf-core`).
5. **Relatorio**
   - Branch/HEAD do kit e do destino, perfil, arquivos novos/alterados (`git status -sb` no TARGET).
   - Nao commitar automaticamente; sugerir skill `exporte` / `commit` se o usuario quiser.

## Resolucao do caminho do kit

Ordem:

1. Flag `--kit=/caminho/toolkit-agentes-skills`
2. Env `TOOLKIT_KIT`, `TOOLKIT_ROOT`, `PMF_DEV_KIT` ou `PMF_KIT_ROOT`
3. `.glpi/kit.yaml` no produto com `path:`
4. O proprio script, se estiver rodando de dentro do kit
5. Irmao `../toolkit-agentes-skills` e `$HOME/projetos/toolkit-agentes-skills`
6. Fallback legado: `../pmf-dev-kit` e `$HOME/projetos/pmf-dev-kit`

Se nao achar: **parar** e pedir o caminho.

## Regras essenciais

- **Sempre** verificar se as branches do destino (e do kit) estao atualizadas vs remotos **antes** da transferencia.
- Preservar sempre `.glpi/project.yaml`, `workspace.yaml` e `state-project-*.json`.
- Preferir `git fetch` + comparar; so `git pull` no kit com `--pull-kit` e working tree limpa.
- Nunca `--force` git / reset hard no produto.
- Nao sobrescrever skills especificos do produto (ex.: `build-*`) — o bootstrap/upgrade so atualiza skills do kit.
- Se TARGET == KIT: informar que ja esta no fonte; nada a sincronizar para si mesmo.
- Escape de emergencia: `--allow-behind` (documentar no relatorio; nao sugerir por padrao).

## Wrappers no produto (apos bootstrap)

Se o produto tiver `scripts/atualizar-kit` vendorizado, preferir:

```bash
./scripts/atualizar-kit --check-only
./scripts/atualizar-kit --profile=full-skeleton --yes
```

## Referencias

- `scripts/atualizar_kit.py` · `scripts/atualizar-kit`
- `scripts/procedimento_atualizar_template.sh` · G15
- `scripts/upgrade-into.sh` · `scripts/bootstrap-into.sh`
- Skill `sincronize` para equalizar local e remotos do produto
