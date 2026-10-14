#!/usr/bin/env python3
"""lint_template.py — lint do catalogo .cursor do toolkit-agentes-skills.

Verifica:
- skills: frontmatter YAML valido, name == pasta, description com tracos PT-BR
- agentes: frontmatter YAML valido com description
- sem marcadores de conflito git em arquivos versionados
- sem segredos reais (tokens/keys com cara de producao)

Uso: python3 scripts/lint_template.py [raiz]
Saida: exit 0 ok; exit 1 com lista de erros.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

PT = re.compile(r"\b(de|da|do|para|com|skill|plano|quando|use|em)\b", re.I)
CONFLITO = re.compile(r"^(<{7}|={7}|>{7})( |$)", re.M)
SEGREDOS = (
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"glpat-[0-9A-Za-z_-]{15,}"),
    re.compile(r"(?i)(api_?key|secret|passwd)\s*[:=]\s*['\"]?[A-Za-z0-9_/.+-]{20,}"),
)
# arquivos onde tokens de EXEMPLO sao esperados (doc oficial, .example)
SEGREDO_OK = ("docs/06_glpi/", ".example")


def tracked_files(root: Path) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    return [root / f for f in out if (root / f).is_file()]


def lint_skills(root: Path, erros: list[str]) -> None:
    for p in sorted((root / ".cursor" / "skills").glob("*/SKILL.md")):
        t = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        if not m:
            erros.append(f"{p}: sem frontmatter")
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except Exception as e:  # noqa: BLE001
            erros.append(f"{p}: YAML invalido: {e}")
            continue
        if not isinstance(fm, dict) or "name" not in fm or "description" not in fm:
            erros.append(f"{p}: falta name/description")
            continue
        if fm["name"] != p.parent.name:
            erros.append(f"{p}: name={fm['name']!r} != pasta {p.parent.name!r}")
        if not PT.search(str(fm["description"])):
            erros.append(f"{p}: description sem tracos PT-BR")


def lint_agents(root: Path, erros: list[str]) -> None:
    for p in sorted((root / ".cursor" / "agents").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        fm = yaml.safe_load(m.group(1)) if m else None
        if not isinstance(fm, dict) or "description" not in fm:
            erros.append(f"{p}: falta description")


def lint_conflitos_segredos(root: Path, erros: list[str]) -> None:
    for f in tracked_files(root):
        rel = str(f.relative_to(root))
        if rel.endswith((".png", ".jpg", ".pdf", ".zip", ".ico")):
            continue
        texto = f.read_text(encoding="utf-8", errors="ignore")
        if CONFLITO.search(texto):
            erros.append(f"{rel}: marcador de conflito git")
        if any(ok in rel for ok in SEGREDO_OK):
            continue
        for pat in SEGREDOS:
            if pat.search(texto):
                erros.append(f"{rel}: possivel segredo real ({pat.pattern[:30]}...)")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    erros: list[str] = []
    lint_skills(root, erros)
    lint_agents(root, erros)
    lint_conflitos_segredos(root, erros)
    if erros:
        print(f"LINT FALHOU — {len(erros)} erro(s):")
        for e in erros:
            print(f"  - {e}")
        return 1
    print("lint ok: skills, agentes, conflitos e segredos verificados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
