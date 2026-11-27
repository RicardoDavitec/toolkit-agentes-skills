#!/usr/bin/env python3
"""Valida o registro de códigos de elemento."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CODIGO_RE = re.compile(r"^[pqjmec][a-z]{2,4}[0-9]{1,2}$")


def erros_regex(itens: list[dict]) -> list[str]:
    erros: list[str] = []
    for item in itens:
        codigo = item.get("codigo", "")
        if not isinstance(codigo, str) or CODIGO_RE.fullmatch(codigo) is None:
            erros.append(f"formato invalido: {codigo}")
    return erros


def erros_duplicidade(itens: list[dict]) -> list[str]:
    erros: list[str] = []
    vistos: dict[str, int] = {}
    for indice, item in enumerate(itens, 1):
        codigo = item.get("codigo", "")
        if not isinstance(codigo, str) or codigo == "":
            continue
        if codigo in vistos:
            erros.append(f"codigo duplicado: {codigo}")
        else:
            vistos[codigo] = indice
    return erros


def validar(itens: list[dict], raiz: Path | None = None) -> list[str]:
    del raiz
    return erros_regex(itens) + erros_duplicidade(itens)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida registro-codigos.json.")
    parser.add_argument("registro", help="Caminho do registro JSON")
    parser.add_argument("--raiz", default=".", help="Raiz dos caminhos do registro")
    args = parser.parse_args(argv)
    dados = json.loads(Path(args.registro).read_text(encoding="utf-8"))
    erros = validar(dados["itens"], Path(args.raiz))
    for erro in erros:
        print(erro, file=sys.stderr)
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
