#!/usr/bin/env bash
# procedimento_atualizar_template.sh — Procedimento A (G15): atualizar kit/template no produto.
# Uso:
#   ./scripts/procedimento_atualizar_template.sh --target=/caminho/produto [--check-only]
#   ./scripts/procedimento_atualizar_template.sh --target=/caminho/produto --yes
#   ./scripts/procedimento_atualizar_template.sh --target=/caminho/produto --docs-only
#   ./scripts/procedimento_atualizar_template.sh --target=... --yes --pull-kit
#   ./scripts/procedimento_atualizar_template.sh --target=... --yes --allow-behind
# Sempre verifica se kit e destino estao atualizados vs remotos antes do apply (G15).
set -euo pipefail

KIT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET=""
CHECK_ONLY=0
YES=0
DOCS_ONLY=0
PULL_KIT=0
ALLOW_BEHIND=0
PROFILE="full-skeleton"

usage() {
  sed -n '2,9p' "$0" | sed 's/^# //'
  exit "${1:-0}"
}

for arg in "$@"; do
  case "$arg" in
    -h|--help) usage 0 ;;
    --target=*) TARGET="${arg#*=}" ;;
    --check-only) CHECK_ONLY=1 ;;
    --yes|-y) YES=1 ;;
    --docs-only) DOCS_ONLY=1 ;;
    --pull-kit) PULL_KIT=1 ;;
    --allow-behind) ALLOW_BEHIND=1 ;;
    --profile=*) PROFILE="${arg#*=}" ;;
    *) echo "Parametro desconhecido: $arg" >&2; usage 2 ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "ERRO: informe --target=/caminho/produto" >&2
  usage 2
fi
TARGET="$(cd "$TARGET" && pwd)"

if [[ "$DOCS_ONLY" == "1" ]]; then
  echo "==> instalar_docs.sh → $TARGET"
  bash "$KIT_ROOT/scripts/docs/instalar_docs.sh" "$TARGET"
  exit 0
fi

ARGS=(--kit="$KIT_ROOT" --target="$TARGET" --profile="$PROFILE")
if [[ "$CHECK_ONLY" == "1" ]]; then
  ARGS+=(--check-only)
elif [[ "$YES" == "1" ]]; then
  ARGS+=(--yes)
else
  echo "Informe --check-only ou --yes (apply). Veja G15." >&2
  exit 2
fi
[[ "$PULL_KIT" == "1" ]] && ARGS+=(--pull-kit)
[[ "$ALLOW_BEHIND" == "1" ]] && ARGS+=(--allow-behind)

exec python3 "$KIT_ROOT/scripts/atualizar_kit.py" "${ARGS[@]}"
