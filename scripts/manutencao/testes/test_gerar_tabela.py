#!/usr/bin/env python3
"""Testes de gerar_tabela.py."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gerar_tabela  # noqa: E402


class TesteGerar(unittest.TestCase):
    def test_gera_link_para_o_arquivo(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            registro = raiz / "registro-codigos.json"
            registro.write_text(
                json.dumps(
                    {
                        "itens": [
                            {
                                "codigo": "ppain1",
                                "caminho": "painel.html",
                                "descricao": "Painel inicial",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            saida = raiz / "tabela-mapeamento.md"
            self.assertEqual(
                gerar_tabela.main([str(registro), "--saida", str(saida)]), 0
            )
            texto = saida.read_text(encoding="utf-8")
            self.assertIn("`ppain1`", texto)
            self.assertIn("[painel.html](painel.html)", texto)


if __name__ == "__main__":
    unittest.main()
