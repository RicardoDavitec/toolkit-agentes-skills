#!/usr/bin/env python3
"""Gera tabela-mapeamento.md a partir do registro de códigos."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import validar_registro


def gerar(itens: list[dict]) -> str:
    linhas = [
        "# Tabela de mapeamento",
        "",
        "| Código | Caminho | Descrição | Aposentado |",
        "|---|---|---|---|",
    ]
    for item in itens:
        codigo = str(item["codigo"]).replace("|", "/")
        caminho = str(item["caminho"]).replace("|", "/")
        descricao = str(item.get("descricao") or "").replace("|", "/")
        aposentado = "sim" if item.get("aposentado") else "nao"
        linhas.append(
            f"| `{codigo}` | [{caminho}]({caminho}) | {descricao} | {aposentado} |"
        )
    linhas.append("")
    return "\n".join(linhas)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gera a tabela de mapeamento.")
    parser.add_argument("registro", help="Caminho do registro JSON")
    parser.add_argument(
        "--saida", default="tabela-mapeamento.md", help="Markdown de saída"
    )
    args = parser.parse_args(argv)
    caminho = Path(args.registro)
    if not caminho.is_file():
        print("formato do registro: arquivo inexistente", file=sys.stderr)
        return 1
    itens, erros = validar_registro.ler_itens(caminho.read_text(encoding="utf-8"))
    if itens is None:
        for erro in erros:
            print(erro, file=sys.stderr)
        return 1
    Path(args.saida).write_text(gerar(itens), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
