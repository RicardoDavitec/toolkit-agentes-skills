#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 nao encontrado. Instale Python 3 e tente de novo." >&2
  exit 127
fi

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
