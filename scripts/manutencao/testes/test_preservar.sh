#!/usr/bin/env bash
# Copia descartavel: bootstrap e upgrade nao alteram registro, escala nem historico.
set -euo pipefail

raiz="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
alvo="$(mktemp -d)"
trap 'rm -rf "$alvo"' EXIT

mkdir -p "$alvo/.glpi/manutencao/historico" "$alvo/docs/05_progresso/historico"
printf 'REGISTRO-ORIGINAL\n' > "$alvo/.glpi/manutencao/registro-codigos.json"
printf 'ESCALA-ORIGINAL\n' > "$alvo/.glpi/manutencao/escala.json"
printf 'HIST-ORIGINAL\n' > "$alvo/.glpi/manutencao/historico/nota.txt"
printf 'HIST-DOCS-ORIGINAL\n' > "$alvo/docs/05_progresso/historico/README.md"

bash "$raiz/scripts/bootstrap-into.sh" "$alvo" --profile=pmf-core --key=exemplo >/dev/null
bash "$raiz/scripts/upgrade-into.sh" --target="$alvo" --apply --yes --no-backup --no-validate >/dev/null

cmp -s <(printf 'REGISTRO-ORIGINAL\n') "$alvo/.glpi/manutencao/registro-codigos.json"
cmp -s <(printf 'ESCALA-ORIGINAL\n') "$alvo/.glpi/manutencao/escala.json"
cmp -s <(printf 'HIST-ORIGINAL\n') "$alvo/.glpi/manutencao/historico/nota.txt"
cmp -s <(printf 'HIST-DOCS-ORIGINAL\n') "$alvo/docs/05_progresso/historico/README.md"
echo "preservado"
