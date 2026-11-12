#!/usr/bin/env bash
# gerar_dados_prisma.sh - gera ER/dicionario base a partir do schema.prisma.
# Uso: scripts/docs/gerar_dados_prisma.sh [caminho/do/schema.prisma]
# Este script NAO edita o schema: se faltar o gerador, mostra o bloco para voce colar.
set -euo pipefail

SCHEMA="${1:-prisma/schema.prisma}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [[ ! -f "$SCHEMA" ]]; then
  echo "ERRO: schema nao encontrado: $SCHEMA" >&2
  exit 1
fi
if ! command -v npx >/dev/null 2>&1; then
  echo "ERRO: npx (Node.js) nao encontrado." >&2
  exit 1
fi

if ! grep -q 'prisma-markdown' "$SCHEMA"; then
  SCHEMA_ABS="$(cd "$(dirname "$SCHEMA")" && pwd)/$(basename "$SCHEMA")"
  DEST="$ROOT/docs/09_dados_e_tabelas/er/ER.md"
  REL="$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1], os.path.dirname(sys.argv[2])))' "$DEST" "$SCHEMA_ABS")"
  cat <<EOF
O schema ainda nao tem o gerador de documentacao. Faca uma vez:

  npm install -D prisma-markdown

E adicione ao schema.prisma (output relativo a este arquivo: $SCHEMA_ABS):

  generator markdown {
    provider = "prisma-markdown"
    output   = "$REL"
    title    = "ER e dicionario"
  }

O script nao edita o schema. Confira as opcoes na documentacao da versao instalada. Depois rode este script de novo.
EOF
  exit 2
fi

npx prisma generate --schema "$SCHEMA"
echo "Concluido. Revise docs/09_dados_e_tabelas/er/ e complete os dic_*.md (skill doc-dados-schema)."
