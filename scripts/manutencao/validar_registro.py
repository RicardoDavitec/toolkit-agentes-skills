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


def erros_caminho(itens: list[dict], raiz: Path) -> list[str]:
    erros: list[str] = []
    for item in itens:
        if item.get("aposentado") is True:
            continue
        caminho = item.get("caminho", "")
        if not isinstance(caminho, str) or caminho == "":
            continue
        destino = Path(caminho)
        if destino.is_absolute() or ".." in destino.parts or not (raiz / destino).is_file():
            erros.append(f"caminho inexistente: {caminho}")
    return erros


def validar(itens: list[dict], raiz: Path | None = None) -> list[str]:
    base = raiz if raiz is not None else Path(".")
    return erros_regex(itens) + erros_duplicidade(itens) + erros_caminho(itens, base)


def ler_itens(texto: str) -> tuple[list[dict] | None, list[str]]:
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        return None, ["formato do registro: JSON invalido"]
    if not isinstance(dados, dict) or not isinstance(dados.get("itens"), list):
        return None, ["formato do registro: falta a lista itens"]
    erros: list[str] = []
    itens: list[dict] = []
    for indice, item in enumerate(dados["itens"], 1):
        if not isinstance(item, dict):
            erros.append(f"formato do registro: item {indice} nao e objeto")
            continue
        if not isinstance(item.get("codigo"), str) or item.get("codigo") == "":
            erros.append(f"formato do registro: item {indice} sem codigo")
        if not isinstance(item.get("caminho"), str) or item.get("caminho") == "":
            erros.append(f"formato do registro: item {indice} sem caminho")
        if "aposentado" in item and not isinstance(item["aposentado"], bool):
            erros.append(
                f"formato do registro: item {indice} aposentado deve ser booleano"
            )
        if "descricao" in item and not isinstance(item["descricao"], str):
            erros.append(f"formato do registro: item {indice} descricao deve ser texto")
        itens.append(item)
    if erros:
        return None, erros
    return itens, []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida registro-codigos.json.")
    parser.add_argument("registro", help="Caminho do registro JSON")
    parser.add_argument("--raiz", default=".", help="Raiz dos caminhos do registro")
    args = parser.parse_args(argv)
    caminho = Path(args.registro)
    if not caminho.is_file():
        print("formato do registro: arquivo inexistente", file=sys.stderr)
        return 1
    itens, erros = ler_itens(caminho.read_text(encoding="utf-8"))
    if itens is not None:
        erros.extend(validar(itens, Path(args.raiz)))
    for erro in erros:
        print(erro, file=sys.stderr)
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
