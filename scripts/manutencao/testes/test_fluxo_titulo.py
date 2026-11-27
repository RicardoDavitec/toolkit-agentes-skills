#!/usr/bin/env python3
"""Fluxo do título fictício até o código."""
from __future__ import annotations

import re
import unittest

TITULO_FICTICIO = "[ppain1] ajuste do painel inicial"
CODIGO_NO_TITULO = re.compile(r"^\[([pqjmec][a-z]{2,4}[0-9]{1,2})\] .+$")


def codigo_do_titulo(titulo: str) -> str | None:
    encontrado = CODIGO_NO_TITULO.fullmatch(titulo)
    if encontrado is None:
        return None
    return encontrado.group(1)


def preparar_chamado(titulo: str) -> dict[str, str]:
    """Dry-run local. Não chama a rede nem grava chamado."""
    return {
        "modo": "dry-run",
        "titulo": titulo,
        "codigo": codigo_do_titulo(titulo) or "",
        "glpi": "sem escrita",
    }


class TesteTitulo(unittest.TestCase):
    def test_chamado_ficticio_traz_o_codigo(self) -> None:
        self.assertEqual(codigo_do_titulo(TITULO_FICTICIO), "ppain1")

    def test_dry_run_nao_grava_chamado(self) -> None:
        preparado = preparar_chamado(TITULO_FICTICIO)
        self.assertEqual(preparado["modo"], "dry-run")
        self.assertEqual(preparado["glpi"], "sem escrita")
        self.assertEqual(preparado["codigo"], "ppain1")


if __name__ == "__main__":
    unittest.main()
