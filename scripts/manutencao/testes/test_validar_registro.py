#!/usr/bin/env python3
"""Testes de validar_registro.py."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validar_registro  # noqa: E402


def gravar(pasta: Path, itens: list[dict]) -> Path:
    caminho = pasta / "registro-codigos.json"
    caminho.write_text(json.dumps({"itens": itens}), encoding="utf-8")
    return caminho


class TesteValidar(unittest.TestCase):
    def test_aceita_codigo_e_arquivo_existente(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "painel.html").write_text("ok", encoding="utf-8")
            registro = gravar(
                raiz, [{"codigo": "ppain1", "caminho": "painel.html"}]
            )
            self.assertEqual(
                validar_registro.main([str(registro), "--raiz", str(raiz)]), 0
            )

    def test_bloqueia_formato_invalido(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "painel.html").write_text("ok", encoding="utf-8")
            registro = gravar(raiz, [{"codigo": "painel", "caminho": "painel.html"}])
            self.assertEqual(
                validar_registro.main([str(registro), "--raiz", str(raiz)]), 1
            )

    def test_bloqueia_duplicado(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "painel.html").write_text("ok", encoding="utf-8")
            registro = gravar(
                raiz,
                [
                    {"codigo": "ppain1", "caminho": "painel.html"},
                    {"codigo": "ppain1", "caminho": "painel.html", "aposentado": True},
                ],
            )
            self.assertEqual(
                validar_registro.main([str(registro), "--raiz", str(raiz)]), 1
            )

    def test_bloqueia_caminho_inexistente(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            registro = gravar(raiz, [{"codigo": "ppain1", "caminho": "ausente.html"}])
            self.assertEqual(
                validar_registro.main([str(registro), "--raiz", str(raiz)]), 1
            )

    def test_aposentado_pode_ficar_sem_arquivo(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            registro = gravar(
                raiz,
                [
                    {
                        "codigo": "ppain1",
                        "caminho": "ausente.html",
                        "aposentado": True,
                    }
                ],
            )
            self.assertEqual(
                validar_registro.main([str(registro), "--raiz", str(raiz)]), 0
            )

    def test_json_invalido(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            registro = Path(pasta) / "registro-codigos.json"
            registro.write_text("{", encoding="utf-8")
            self.assertEqual(validar_registro.main([str(registro)]), 1)


if __name__ == "__main__":
    unittest.main()
