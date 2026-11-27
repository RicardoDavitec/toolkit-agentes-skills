#!/usr/bin/env python3
"""Testes de varrer_codigos.py."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import varrer_codigos  # noqa: E402


class TesteVarrer(unittest.TestCase):
    def test_le_aspas_duplas_e_simples(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "painel.html").write_text(
                '<div data-maint-id="ppain1"></div>\n', encoding="utf-8"
            )
            (raiz / "quadro.html").write_text(
                "<div data-maint-id='qkart1'></div>\n", encoding="utf-8"
            )
            achados = varrer_codigos.varrer(raiz)
            codigos = sorted(item[0] for item in achados)
            self.assertEqual(codigos, ["ppain1", "qkart1"])

    def test_pasta_inexistente(self) -> None:
        self.assertEqual(varrer_codigos.main(["/pasta/que/nao/existe"]), 2)


if __name__ == "__main__":
    unittest.main()
