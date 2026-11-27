#!/usr/bin/env python3
"""Fluxo do título fictício até o código."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import varrer_codigos  # noqa: E402

TITULO_FICTICIO = "[ppain1] ajuste do painel inicial"
CODIGO_NO_TITULO = re.compile(r"^\[([pqjmec][a-z]{2,4}[0-9]{1,2})\] .+$")


def codigo_do_titulo(titulo: str) -> str | None:
    encontrado = CODIGO_NO_TITULO.fullmatch(titulo)
    if encontrado is None:
        return None
    return encontrado.group(1)


def localizar(raiz: Path, codigo: str) -> Path | None:
    for achado, caminho, _linha in varrer_codigos.varrer(raiz):
        if achado == codigo:
            return caminho
    return None


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

    def test_localiza_o_arquivo_pelo_codigo(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            arquivo = raiz / "painel.html"
            arquivo.write_text('<div data-maint-id="ppain1"></div>\n', encoding="utf-8")
            codigo = codigo_do_titulo(TITULO_FICTICIO)
            self.assertIsNotNone(codigo)
            encontrado = localizar(raiz, codigo or "")
            self.assertEqual(encontrado, arquivo)


if __name__ == "__main__":
    unittest.main()
