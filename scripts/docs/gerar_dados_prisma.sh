#!/usr/bin/env bash
# gerar_dados_prisma.sh - gera ER/dicionario base a partir do schema.prisma.
# Uso: scripts/docs/gerar_dados_prisma.sh [caminho/do/schema.prisma]
# Este script NAO edita o schema: se faltar o gerador, mostra o bloco para voce colar.
set -euo pipefail

SCHEMA="${1:-prisma/schema.prisma}"

if [[ ! -f "$SCHEMA" ]]; then
  echo "ERRO: schema nao encontrado: $SCHEMA" >&2
  exit 1
fi
if ! command -v npx >/dev/null 2>&1; then
  echo "ERRO: npx (Node.js) nao encontrado." >&2
  exit 1
fi

if ! grep -q 'prisma-markdown' "$SCHEMA"; then
  cat <<'MSG'
O schema ainda nao tem o gerador de documentacao. Faca uma vez:

  npm install -D prisma-markdown

E adicione ao schema.prisma (ajuste o caminho relativo ao arquivo do schema):

  generator markdown {
    provider = "prisma-markdown"
    output   = "../docs/09_dados_e_tabelas/er/ER.md"
    title    = "ER e dicionario"
  }

Confira as opcoes na documentacao da versao instalada. Depois rode este script de novo.
MSG
  exit 2
fi

npx prisma generate --schema "$SCHEMA"
echo "Concluido. Revise docs/09_dados_e_tabelas/er/ e complete os dic_*.md (skill doc-dados-schema)."
