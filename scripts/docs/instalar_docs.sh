#!/usr/bin/env bash
# instalar_docs.sh - instala o padrao de documentacao em um projeto.
# Uso: scripts/docs/instalar_docs.sh [diretorio-do-projeto]   (padrao: .)
# Nao sobrescreve arquivos existentes.
set -euo pipefail

ORIGEM="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ALVO="$(cd "${1:-.}" && pwd)"

copiar() {  # copiar <relativo>
  local rel="$1"
  [[ -e "$ORIGEM/$rel" ]] || { echo "aviso: ausente na origem: $rel"; return 0; }
  [[ "$ORIGEM" == "$ALVO" ]] && return 0
  mkdir -p "$(dirname "$ALVO/$rel")"
  cp -n "$ORIGEM/$rel" "$ALVO/$rel" && echo "ok: $rel" || true
}

for f in \
  .vscode/extensions.json .vscode/settings.json .cursor/rules/documentacao.mdc \
  .cursor/agents/doc-arquiteto.md .cursor/agents/doc-dados-lgpd.md .cursor/agents/doc-revisor.md \
  scripts/docs/lint_docs.py scripts/docs/novo_doc.py scripts/docs/gerar_rastreabilidade.py \
  scripts/docs/gerar_dados_prisma.sh scripts/docs/instalar_docs.sh \
  scripts/docs/procedimento_documentar.sh scripts/procedimento_atualizar_template.sh; do
  copiar "$f"
done

for s in doc-novo doc-adr doc-dados-schema doc-lgpd-inventario doc-rastreabilidade doc-gate-fase doc-lint; do
  copiar ".cursor/skills/$s/SKILL.md"
done

# Padrao 12: guias, modelos e exemplos (nao sobrescreve existentes)
if [[ -d "$ORIGEM/docs/12_padrao_documentacao" ]]; then
  while IFS= read -r -d '' f; do
    rel="${f#"$ORIGEM"/}"
    copiar "$rel"
  done < <(find "$ORIGEM/docs/12_padrao_documentacao" -type f -print0)
fi
copiar "docs/README.md"

for d in 00_visao_geral 01_requisitos 02_arquitetura/adr 03_implementacao/testes \
         03_implementacao/homologacao 04_operacao 09_dados_e_tabelas/er \
         09_dados_e_tabelas/dicionario 09_dados_e_tabelas/enums 09_dados_e_tabelas/lgpd \
         09_dados_e_tabelas/linhagem; do
  mkdir -p "$ALVO/docs/$d"
  [[ -e "$ALVO/docs/$d/.gitkeep" ]] || : > "$ALVO/docs/$d/.gitkeep"
done

chmod +x "$ALVO"/scripts/docs/*.sh 2>/dev/null || true
echo "Pronto. Proximo passo: python3 scripts/docs/lint_docs.py"
