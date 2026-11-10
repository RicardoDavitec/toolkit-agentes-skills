#!/usr/bin/env bash
# procedimento_documentar.sh — Procedimento B (G15): atalhos de documentação no produto.
# Uso (na raiz do produto, ou com --root=):
#   ./scripts/docs/procedimento_documentar.sh --ajuda
#   ./scripts/docs/procedimento_documentar.sh lint
#   ./scripts/docs/procedimento_documentar.sh novo <tipo> --titulo "..."
#   ./scripts/docs/procedimento_documentar.sh onde
set -euo pipefail

ROOT=""
CMD=""

usage() {
  cat <<'EOF'
Procedimento B — Documentar (guia G15)

Comandos:
  lint                         Roda scripts/docs/lint_docs.py
  novo <tipo> --titulo "..."   Delega a novo_doc.py (tipos do G03)
  onde                         Mostra pastas-chave do padrao 12

Skills Cursor equivalentes:
  documente-o-plano  → plano em docs/05_progresso/planos_ativos/
  documentar         → atualiza docs existentes
  doc-novo / doc-adr → cria documento de apoio
  doc-lint           → lint
  commit             → fecha P com plano no mesmo commit
EOF
  exit "${1:-0}"
}

ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help|--ajuda) usage 0 ;;
    --root=*) ROOT="${1#*=}"; shift ;;
    lint|novo|onde) CMD="$1"; shift; ARGS=("$@"); break ;;
    *) echo "Comando desconhecido: $1" >&2; usage 2 ;;
  esac
done

if [[ -z "$ROOT" ]]; then
  # script em <produto>/scripts/docs/ ou <kit>/scripts/docs/
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
ROOT="$(cd "$ROOT" && pwd)"
DOCS_SCRIPTS="$ROOT/scripts/docs"

[[ -n "$CMD" ]] || usage 2

case "$CMD" in
  lint)
    exec python3 "$DOCS_SCRIPTS/lint_docs.py" "${ARGS[@]}"
    ;;
  novo)
    exec python3 "$DOCS_SCRIPTS/novo_doc.py" "${ARGS[@]}"
    ;;
  onde)
    cat <<EOF
Raiz: $ROOT
Padrao:     docs/12_padrao_documentacao/
Modelos:    docs/12_padrao_documentacao/02_modelos/
Planos:     docs/05_progresso/planos_ativos/
Visao:      docs/00_visao_geral/
Requisitos: docs/01_requisitos/
Arquitetura:docs/02_arquitetura/ (+ adr/)
Operacao:   docs/04_operacao/
LGPD:       docs/09_dados_e_tabelas/lgpd/
EOF
    ;;
esac
