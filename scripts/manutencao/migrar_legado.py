#!/usr/bin/env python3
"""Mescla um mapa ou uma varredura no registro, sem gravar escala nem histórico."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import validar_registro
import varrer_codigos


def itens_da_varredura(raiz: Path) -> list[dict]:
    itens: list[dict] = []
    base = raiz.resolve()
    for codigo, caminho, _linha in varrer_codigos.varrer(raiz):
        try:
            relativo = caminho.resolve().relative_to(base).as_posix()
        except ValueError:
            continue
        itens.append(
            {
                "codigo": codigo,
                "caminho": relativo,
                "descricao": "",
                "aposentado": False,
            }
        )
    return itens


def carregar_destino(caminho: Path) -> tuple[list[dict], list[str]]:
    if not caminho.exists():
        return [], []
    return validar_registro.ler_itens(caminho.read_text(encoding="utf-8"))


def mesclar(destino: list[dict], entrada: list[dict], raiz: Path) -> tuple[list[dict], list[str]]:
    resultado = list(destino)
    conhecidos = {item.get("codigo") for item in destino}
    relatorio: list[str] = []
    for item in entrada:
        codigo = item.get("codigo", "")
        if codigo in conhecidos:
            relatorio.append(f"mantido: {codigo}")
            continue
        erros = validar_registro.validar([item], raiz)
        if erros:
            relatorio.append(f"recusado: {erros[0]}")
            continue
        resultado.append(item)
        conhecidos.add(codigo)
        relatorio.append(f"novo: {codigo}")
    return resultado, relatorio


def destino_proibido(caminho: Path) -> bool:
    return caminho.name == "escala.json" or "historico" in caminho.parts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mescla legado no registro de códigos.")
    parser.add_argument("--origem", help="JSON no formato do registro")
    parser.add_argument("--destino", required=True, help="registro-codigos.json do produto")
    parser.add_argument("--raiz", default=".", help="Raiz dos caminhos")
    parser.add_argument("--apply", action="store_true", help="Grava o destino. Sem isto, só relata.")
    args = parser.parse_args(argv)

    destino = Path(args.destino)
    if destino_proibido(destino):
        print("recusado: este comando nao grava escala nem historico", file=sys.stderr)
        return 1

    raiz = Path(args.raiz)
    if not raiz.is_dir():
        print(f"pasta inexistente: {raiz}", file=sys.stderr)
        return 2

    entrada: list[dict] = []
    if args.origem:
        origem = Path(args.origem)
        if not origem.is_file():
            print("formato do registro: arquivo inexistente", file=sys.stderr)
            return 1
        itens, erros = validar_registro.ler_itens(origem.read_text(encoding="utf-8"))
        if itens is None:
            for erro in erros:
                print(erro, file=sys.stderr)
            return 1
        entrada.extend(itens)
    else:
        entrada.extend(itens_da_varredura(raiz))

    atual, erros_destino = carregar_destino(destino)
    if atual is None:
        for erro in erros_destino:
            print(erro, file=sys.stderr)
        return 1

    mesclado, relatorio = mesclar(atual, entrada, raiz)
    for linha in relatorio:
        print(linha)
    if not args.apply:
        print("dry-run: nada foi gravado")
        return 0

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps({"itens": mesclado}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
