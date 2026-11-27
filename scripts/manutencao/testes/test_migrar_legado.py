#!/usr/bin/env python3
"""Testes de migrar_legado.py."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import migrar_legado  # noqa: E402


class TesteMigrar(unittest.TestCase):
    def test_dry_run_nao_grava(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "painel.html").write_text("ok", encoding="utf-8")
            origem = raiz / "mapa.json"
            origem.write_text(
                json.dumps({"itens": [{"codigo": "ppain1", "caminho": "painel.html"}]}),
                encoding="utf-8",
            )
            destino = raiz / "registro-codigos.json"
            codigo = migrar_legado.main(
                ["--origem", str(origem), "--destino", str(destino), "--raiz", str(raiz)]
            )
            self.assertEqual(codigo, 0)
            self.assertFalse(destino.exists())

    def test_apply_mantem_codigo_existente(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "painel.html").write_text("ok", encoding="utf-8")
            (raiz / "outro.html").write_text("ok", encoding="utf-8")
            destino = raiz / "registro-codigos.json"
            destino.write_text(
                json.dumps(
                    {"itens": [{"codigo": "ppain1", "caminho": "painel.html", "descricao": "orig"}]}
                ),
                encoding="utf-8",
            )
            origem = raiz / "mapa.json"
            origem.write_text(
                json.dumps(
                    {
                        "itens": [
                            {"codigo": "ppain1", "caminho": "outro.html"},
                            {"codigo": "qkart1", "caminho": "outro.html"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                migrar_legado.main(
                    [
                        "--origem",
                        str(origem),
                        "--destino",
                        str(destino),
                        "--raiz",
                        str(raiz),
                        "--apply",
                    ]
                ),
                0,
            )
            itens = json.loads(destino.read_text(encoding="utf-8"))["itens"]
            por_codigo = {item["codigo"]: item for item in itens}
            self.assertEqual(por_codigo["ppain1"]["caminho"], "painel.html")
            self.assertEqual(por_codigo["qkart1"]["caminho"], "outro.html")

    def test_nao_grava_escala_nem_historico(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            self.assertEqual(
                migrar_legado.main(
                    ["--destino", str(raiz / "escala.json"), "--raiz", str(raiz)]
                ),
                1,
            )
            self.assertEqual(
                migrar_legado.main(
                    [
                        "--destino",
                        str(raiz / "historico" / "nota.json"),
                        "--raiz",
                        str(raiz),
                    ]
                ),
                1,
            )


if __name__ == "__main__":
    unittest.main()
