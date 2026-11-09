#!/usr/bin/env python3
"""novo_doc.py - cria documento de apoio a partir de um modelo.

Exemplo:
    python3 scripts/docs/novo_doc.py adr --titulo "Usar PostgreSQL" --autor Ricardo
    python3 scripts/docs/novo_doc.py dicionario_dados --titulo "Dicionario - atendimentos" --slug atendimentos

Planos, anexos, SESSAO_* e pendencias NAO sao criados aqui (use as skills do kit).
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs"
MODELOS = DOCS / "12_padrao_documentacao" / "02_modelos"

# tipo: (prefixo, pasta, classificacao padrao, arquivo numerado?)
TIPOS = {
    "visao": ("VIS", "00_visao_geral", "interno", True),
    "requisito": ("REQ", "01_requisitos", "interno", True),
    "regra_negocio": ("RN", "01_requisitos", "interno", True),
    "glossario": ("GLO", "01_requisitos", "publico", True),
    "arquitetura": ("ARQ", "02_arquitetura", "interno", True),
    "adr": ("ADR", "02_arquitetura/adr", "interno", True),
    "teste": ("TST", "03_implementacao/testes", "interno", True),
    "homologacao": ("HML", "03_implementacao/homologacao", "interno", True),
    "operacao": ("OPS", "04_operacao", "restrito", True),
    "dicionario_dados": ("DIC", "09_dados_e_tabelas/dicionario", "restrito", False),
    "inventario_lgpd": ("LGP", "09_dados_e_tabelas/lgpd", "pessoal", False),
    "relatorio": ("REL", "05_progresso/geral", "interno", True),
}


def slugify(texto: str) -> str:
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def proximo_numero(prefixo: str) -> int:
    maior = 0
    padrao = re.compile(rf"^id:\s*{prefixo}-(\d+)\s*$", re.M)
    for arq in DOCS.rglob("*.md"):
        if "02_modelos" in arq.as_posix() or "03_exemplos" in arq.as_posix():
            continue
        for m in padrao.finditer(arq.read_text(encoding="utf-8", errors="ignore")):
            maior = max(maior, int(m.group(1)))
    return maior + 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("tipo", choices=sorted(TIPOS))
    ap.add_argument("--titulo", required=True)
    ap.add_argument("--autor", default="")
    ap.add_argument("--slug", help="slug do arquivo (padrao: derivado do titulo)")
    ap.add_argument("--chamado", help="numero do chamado C (so cabecalho)")
    ap.add_argument("--requisicao", help="numero da requisicao R (so cabecalho)")
    ap.add_argument("--codigo", help="code relativo F#[.S#[.P#]]")
    a = ap.parse_args()

    prefixo, pasta, classif, numerado = TIPOS[a.tipo]
    modelo = MODELOS / f"MOD_{a.tipo}.md"
    if not modelo.exists():
        print(f"ERRO: modelo ausente: {modelo.relative_to(RAIZ)}", file=sys.stderr)
        return 1

    slug = a.slug or slugify(a.titulo)
    if numerado:
        n = proximo_numero(prefixo)
        doc_id, nome = f"{prefixo}-{n:03d}", f"{prefixo.lower()}_{n:03d}_{slug}.md"
    else:
        doc_id, nome = f"{prefixo}-{slug}", f"{prefixo.lower()}_{slug}.md"

    titulo = a.titulo.replace('"', "'")
    linhas = ["---", f"id: {doc_id}", f"tipo: {a.tipo}", f'titulo: "{titulo}"']
    if a.chamado:
        linhas.append(f'chamado: "{a.chamado}"')
    if a.requisicao:
        linhas.append(f'requisicao: "{a.requisicao}"')
    if a.codigo:
        linhas.append(f"codigo: {a.codigo}")
    linhas += [
        "status: rascunho", "versao: 0.1.0", f"data: {date.today().isoformat()}",
        f"autor: {a.autor or 'A DEFINIR'}", f"classificacao: {classif}", "---", "",
    ]
    corpo = modelo.read_text(encoding="utf-8").replace("{{titulo}}", a.titulo)

    destino = DOCS / pasta / nome
    if destino.exists():
        print(f"ERRO: ja existe: {destino.relative_to(RAIZ)}", file=sys.stderr)
        return 1
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas) + corpo, encoding="utf-8")
    print(f"Criado: {destino.relative_to(RAIZ)}  ({doc_id})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
