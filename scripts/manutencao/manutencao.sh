#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cmd="${1:-}"
if [[ $# -gt 0 ]]; then
  shift
fi

case "$cmd" in
  varrer)
    python3 "$DIR/varrer_codigos.py" "$@"
    ;;
  validar)
    python3 "$DIR/validar_registro.py" "$@"
    ;;
  tabela)
    python3 "$DIR/gerar_tabela.py" "$@"
    ;;
  *)
    echo "Uso: manutencao.sh varrer|validar|tabela [argumentos]" >&2
    exit 2
    ;;
esac
