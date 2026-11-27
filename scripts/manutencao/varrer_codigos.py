#!/usr/bin/env python3
"""Lista os valores de data-maint-id em arquivos de texto."""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ATTR = re.compile(r"""data-maint-id\s*=\s*(['"])(.*?)\1""", re.IGNORECASE)
IGNORAR_DIR = {".git", "node_modules", ".venv", "venv", "__pycache__"}


def varrer(raiz: Path) -> list[tuple[str, Path, int]]:
    """Devolve (codigo, caminho, linha) na ordem de leitura."""
    achados: list[tuple[str, Path, int]] = []
    for dirpath, dirnames, filenames in os.walk(raiz, followlinks=False):
        base = Path(dirpath)
        dirnames[:] = [
            nome
            for nome in dirnames
            if nome not in IGNORAR_DIR and not (base / nome).is_symlink()
        ]
        for nome in filenames:
            caminho = base / nome
            if caminho.is_symlink():
                continue
            try:
                texto = caminho.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for numero, linha in enumerate(texto.splitlines(), 1):
                for encontrado in ATTR.finditer(linha):
                    achados.append((encontrado.group(2), caminho, numero))
    return achados


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Varre data-maint-id.")
    parser.add_argument("raiz", nargs="?", default=".", help="Pasta a varrer")
    args = parser.parse_args(argv)
    raiz = Path(args.raiz)
    if not raiz.is_dir():
        print(f"pasta inexistente: {raiz}", file=sys.stderr)
        return 2
    for codigo, caminho, linha in varrer(raiz):
        print(f"{codigo}\t{caminho}:{linha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
