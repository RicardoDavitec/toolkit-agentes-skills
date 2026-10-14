---
name: backup
description: >-
  Backup COMPLETO do repositorio em foco (inclui .git; exclui segredos).
  Gera .tar.gz + .tar.gz.SHA256 com destino padrao por SO e validacao de
  integridade. Use em backup, copia de seguranca, backup completo. Nao use
  para documentar, auditar docs ou encerrar sessao.
argument-hint: "Opcional: commit/push antes do backup; destino custom."
---

# Skill: backup

Objetivo: gerar backup completo com versionamento opcional e verificacao de
integridade, com destino padrao por sistema operacional.

## Fluxo padrao (baixo custo de tokens)

1. Confirmar repositorio git e detectar remoto (`git remote -v`).
2. Se houver alteracoes, perguntar **uma unica vez** sobre git add/commit/push.
3. Executar o script de apoio:
   - `python .cursor/skills/backup/scripts/backup_projeto.py`
   - `python .cursor/skills/backup/scripts/backup_projeto.py --destino /mnt/e/VSCode-bkp`
4. Reportar apenas resultado final: arquivo gerado + checksum + destino.

## Politica de compactacao

- Linux/WSL/macOS: `tar.gz` por padrao (mais rapido). Opcional `tar.xz`
  (`BACKUP_FORMAT=tar.xz`).
- Windows: `zip` por padrao.
- Integridade: sempre gerar `<arquivo>.SHA256` ao lado do backup.

## Destino por SO (precedencia)

1. Argumento `--destino`
2. Variavel de ambiente (`BACKUP_DESTINO_WINDOWS` / `BACKUP_DESTINO_LINUX` /
   `BACKUP_DESTINO_DARWIN`, e `*_FALLBACK_*`)
3. `.cursor/skills/config/endpoints_operacionais.json` (`backup.*`)
4. Fallback relativo no repositorio

Padrao da config central:

- Windows: `E:/VSCode-bkp`
- Linux/WSL: `/mnt/e/VSCode-bkp`
- Darwin: `/Volumes/VSCode-bkp`

Estrutura: `<destino>/<nome-do-projeto>/<commit>_<DD-MM-YY_hh-mm>.tar.gz`.

## Variaveis suportadas

- `BACKUP_DESTINO_<SO>` e `BACKUP_DESTINO_FALLBACK_<SO>`: destinos por SO.
- `BACKUP_ROOT`: override generico da raiz do backup.
- `BACKUP_EXCLUDE`: lista separada por virgula de paths a excluir.
- `BACKUP_FORMAT`: `auto`|`tar.gz`|`tar.xz`|`zip`.

## Boas praticas para eficiencia

- Evitar varreduras desnecessarias: nao ler docs extensos durante o backup.
- Responder com resumo curto (sem logs longos) apos execucao.
- Excluir artefatos volumosos (`node_modules`, `build`, `coverage`) quando
  nao forem necessarios para restauracao.
- **Nunca** incluir `.env`, tokens ou keystores.

## Fallback de compactadores

- Linux/WSL/macOS: se faltar `tar`/`xz`/`zip`, sugerir instalacao pelo
  gerenciador detectado (apt, dnf, yum, pacman, zypper, brew).
- Windows: se faltar `Compress-Archive`, tentar `7z`; se ausente, sugerir
  `winget install 7zip.7zip`.

## Criterio de conclusao

- Backup gerado e validado (SHA256 confere) no destino esperado.

## Referencias

- Script: [scripts/backup_projeto.py](scripts/backup_projeto.py)
- Dicas: [DICAS_USO.md](DICAS_USO.md)
- Endpoints: `.cursor/skills/config/endpoints_operacionais.json`
