---
name: backup-projeto
description: 'Executa backup operacional do projeto com validacao de git, add/commit/push opcional, geracao de .tar.gz e arquivo .tar.gz.SHA256 com destino padrao por SO.'
argument-hint: 'Destino do backup e nivel desejado'
user-invocable: true
---

# Backup Projeto

## Quando usar
- Antes de mudanca de alto impacto.
- Ao final de entrega relevante.

## Procedimento
1. Verificar status do git e sincronizacao com remoto.
2. Se necessario, adicionar, commitar e enviar.
3. Definir estrategia por ambiente:
   - Todos os ambientes: tar.gz
   - Gerar arquivo de integridade: tar.gz.SHA256
4. Criar pasta por projeto no destino configurado.
5. Gerar nome do arquivo com commit e timestamp.

## Script de apoio
- [Gerar backup por ambiente](./scripts/backup_projeto.py)

Exemplo:
- `python .github/skills/backup-projeto/scripts/backup_projeto.py`
- `python .github/skills/backup-projeto/scripts/backup_projeto.py --destino E:\\VSCode-bkp`

## Endpoint operacional
- Arquivo central: `/.github/skills/config/endpoints_operacionais.json`
- Chaves: `backup.destino_padrao`, `backup.fallback_por_so`, `backup.fallback_relativo_repo`, `backup.formato_nome_arquivo`

## Variaveis de ambiente (precedencia)
- `BACKUP_DESTINO_WINDOWS`, `BACKUP_DESTINO_LINUX`, `BACKUP_DESTINO_DARWIN`
- `BACKUP_DESTINO_FALLBACK_WINDOWS`, `BACKUP_DESTINO_FALLBACK_LINUX`, `BACKUP_DESTINO_FALLBACK_DARWIN`
- Precedencia: `--destino` > variavel de ambiente > config central > fallback relativo no repositorio

## Criterio de Conclusao
- Backup gerado e validado no destino esperado.
