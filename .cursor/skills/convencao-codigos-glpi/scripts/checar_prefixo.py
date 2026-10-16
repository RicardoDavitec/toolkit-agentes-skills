#!/usr/bin/env python3
"""Procura prefixo longo C#.R# fora do cabecalho e dos blocos autorizados.

Nao altera tree_validate, retro_scan nem model.defaults.
Exit 0 se nao houver violacao; exit 1 se houver.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

FORBIDDEN = re.compile(r"\bC\d+\.R\d+")
CODE_ATTR = re.compile(r'code="C' + r'\d+')
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")

ROOTS = ("docs", ".github")
SKIP_DIR = Path("docs/05_progresso/legados")


def allowed(line: str, in_incorrect: bool) -> bool:
    stripped = line.lstrip()
    if in_incorrect:
        return True
    if stripped.startswith(">") and (
        "Chamado ITIL" in line or "Projeto/Requisicao" in line or "Projeto/Requisição" in line
    ):
        return True
    if "REVOGADA" in line or "D-novo" in line:
        return True
    return False


def scan_file(path: Path, root: Path) -> list[str]:
    rel = path.relative_to(root).as_posix()
    if rel.startswith(SKIP_DIR.as_posix()):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    if "\0" in text:
        return []
    out: list[str] = []
    in_incorrect = False
    incorrect_level = 0
    for n, line in enumerate(text.splitlines(), 1):
        heading = HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            if in_incorrect and level <= incorrect_level:
                in_incorrect = False
            if "INCORRETO" in title.upper():
                in_incorrect = True
                incorrect_level = level
        if allowed(line, in_incorrect):
            continue
        snippet = line.strip()
        if FORBIDDEN.search(line) or CODE_ATTR.search(line):
            out.append(f"{rel}:{n}:{snippet}")
    return out


def main() -> int:
    root = Path(__file__).resolve().parents[4]
    hits: list[str] = []
    for name in ROOTS:
        base = root / name
        if not base.exists():
            continue
        seen: set[str] = set()
        for dirpath, dirnames, filenames in os.walk(base, followlinks=True):
            real = os.path.realpath(dirpath)
            if real in seen:
                dirnames.clear()
                continue
            seen.add(real)
            if SKIP_DIR.as_posix() in Path(dirpath).relative_to(root).as_posix():
                dirnames.clear()
                continue
            for name in filenames:
                path = Path(dirpath) / name
                if path.is_file():
                    hits.extend(scan_file(path, root))
    if hits:
        print("\n".join(hits))
        return 1
    print("ok: nenhum prefixo C#.R# indevido")
    return 0


if __name__ == "__main__":
    sys.exit(main())
