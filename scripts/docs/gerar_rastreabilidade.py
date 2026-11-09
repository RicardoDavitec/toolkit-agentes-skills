#!/usr/bin/env python3
"""gerar_rastreabilidade.py - matriz requisito -> tarefa -> commit -> teste -> homologacao.

Uso: python3 scripts/docs/gerar_rastreabilidade.py
Saida: docs/01_requisitos/rastreabilidade.md

Fontes:
  - REQ-/RN- citados nos itens de planos_ativos/ e legados/ (bloco de cada **F#.S#.P#**)
  - codes F#.S#.P# na mensagem dos commits (git log)
  - REQ-/RN- citados em docs/03_implementacao/testes e /homologacao
Nao inventa vinculos: sem evidencia, a celula fica vazia.
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs"
SAIDA = DOCS / "01_requisitos" / "rastreabilidade.md"

RE_ITEM = re.compile(r"\*\*(F[1-5]\.S\d+\.P\d+)\*\*")
RE_SESSAO = re.compile(r"\*\*(F[1-5]\.S\d+)\*\*")
RE_CODE = re.compile(r"\bF[1-5]\.S\d+\.P\d+\b")
RE_REQ = re.compile(r"\b(?:REQ|RN)-\d+\b")
RE_CHAVE = re.compile(r"^([a-z_]+):\s*(.*)$")


def front_matter(texto: str) -> dict[str, str]:
    if not texto.startswith("---\n"):
        return {}
    fim = texto.find("\n---", 4)
    if fim == -1:
        return {}
    d = {}
    for linha in texto[4:fim].splitlines():
        m = RE_CHAVE.match(linha)
        if m:
            d[m.group(1)] = m.group(2).strip().strip('"')
    return d


def requisitos() -> list[str]:
    ids = []
    for arq in sorted((DOCS / "01_requisitos").glob("*.md")):
        fm = front_matter(arq.read_text(encoding="utf-8"))
        if fm.get("tipo") in ("requisito", "regra_negocio") and fm.get("status") != "obsoleto":
            ids.append(fm["id"])
    return ids


def tarefas_por_requisito() -> dict[str, set[str]]:
    mapa: dict[str, set[str]] = defaultdict(set)
    for pasta in ("planos_ativos", "legados"):
        base = DOCS / "05_progresso" / pasta
        for arq in base.rglob("*.md") if base.exists() else []:
            atual = None
            for linha in arq.read_text(encoding="utf-8").splitlines():
                if linha.startswith("#") or (RE_SESSAO.search(linha) and not RE_ITEM.search(linha)):
                    atual = None
                m = RE_ITEM.search(linha)
                if m:
                    atual = m.group(1)
                if atual:
                    for r in RE_REQ.findall(linha):
                        mapa[r].add(atual)
    return mapa


def commits_por_code() -> dict[str, list[str]]:
    mapa: dict[str, list[str]] = defaultdict(list)
    try:
        saida = subprocess.run(["git", "log", "--format=%h%x09%s"], cwd=RAIZ,
                               capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        print("AVISO: git log indisponivel; coluna de commits ficara vazia.", file=sys.stderr)
        return mapa
    for linha in saida.splitlines():
        sha, _, assunto = linha.partition("\t")
        for code in set(RE_CODE.findall(assunto)):
            mapa[code].append(sha)
    return mapa


def citados_em(subpasta: str) -> dict[str, set[str]]:
    mapa: dict[str, set[str]] = defaultdict(set)
    base = DOCS / "03_implementacao" / subpasta
    for arq in base.rglob("*.md") if base.exists() else []:
        texto = arq.read_text(encoding="utf-8")
        doc_id = front_matter(texto).get("id", arq.stem)
        for r in set(RE_REQ.findall(texto)):
            mapa[r].add(doc_id)
    return mapa


def main() -> int:
    reqs = requisitos()
    tarefas = tarefas_por_requisito()
    commits = commits_por_code()
    testes = citados_em("testes")
    homolog = citados_em("homologacao")

    linhas, lacunas, cobertos = [], [], 0
    for r in reqs:
        ts = sorted(tarefas.get(r, []))
        cs = sorted({c for t in ts for c in commits.get(t, [])})
        te = sorted(testes.get(r, []))
        hm = sorted(homolog.get(r, []))
        linhas.append(f"| {r} | {', '.join(ts)} | {', '.join(f'`{c}`' for c in cs)} | "
                      f"{', '.join(te)} | {', '.join(hm)} |")
        if ts and cs and te:
            cobertos += 1
        else:
            faltam = [n for n, v in (("tarefa", ts), ("commit", cs), ("teste", te)) if not v]
            lacunas.append(f"- {r}: sem {', '.join(faltam)}")

    total = len(reqs)
    cobertura = (cobertos / total * 100) if total else 0.0
    hoje = date.today().isoformat()
    doc = [
        "---", "id: REL-RASTREABILIDADE", "tipo: relatorio",
        'titulo: "Matriz de rastreabilidade (gerada)"', "status: rascunho",
        "versao: 0.1.0", f"data: {hoje}", "autor: gerar_rastreabilidade.py",
        "classificacao: interno", "---", "",
        "# Matriz de rastreabilidade", "",
        "Arquivo **gerado**. Nao edite; rode `python3 scripts/docs/gerar_rastreabilidade.py`.", "",
        "## Resumo", "",
        f"- Requisitos e regras considerados: {total}",
        f"- Com tarefa, commit e teste: {cobertos}",
        f"- Cobertura de rastreabilidade: {cobertura:.1f}%", "",
        "## Resultado", "",
        "| Requisito | Tarefas | Commits | Testes | Homologacao |",
        "|---|---|---|---|---|", *linhas, "",
        "## Riscos residuais", "", *(lacunas or ["- Nenhuma lacuna encontrada."]), "",
    ]
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text("\n".join(doc), encoding="utf-8")
    print(f"Gerado: {SAIDA.relative_to(RAIZ)} | cobertura {cobertura:.1f}% ({cobertos}/{total})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
