#!/usr/bin/env python3
"""Árvore C/R/F/S/P e nome do projeto raiz.

C (chamado) e R (projeto) ficam só no cabeçalho, por id.
F1–F5 são fases. Sessão é F#.S#. Tarefa é F#.S#.P#.
O R de um título markdown antigo (R1) não vira projeto.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

FSP_RE = re.compile(r"^F\d+(?:\.S\d+(?:\.P\d+)?)?$", re.I)
LEGACY_R_RE = re.compile(r"^R\d+(?:\.\d+)*$", re.I)
LEGACY_S_RE = re.compile(r"^S\d+$", re.I)
LEGACY_P_RE = re.compile(r"^(S\d+)\.P\d+$", re.I)
SESSION_RE = re.compile(r"^(F\d+)\.S\d+$", re.I)
TASK_RE = re.compile(r"^(F\d+\.S\d+)\.P\d+$", re.I)
PHASES = (
    ("F1", "F1. Planejamento"),
    ("F2", "F2. Implementação"),
    ("F3", "F3. Testes Internos"),
    ("F4", "F4. Homologação"),
    ("F5", "F5. Aprovação"),
)
PHASE_CODES = {code for code, _title in PHASES}
PHASE_TITLES = dict(PHASES)
ROOT_PREFIX = "GEP - "
ROOT_SUFFIX = " - 0. [PAI]"
EFFORT_SECONDS = 2 * 3600
DAY_SECONDS = 8 * 3600
REALIZED = {"done", "archived", "partial"}


def format_root_name(name: str) -> str:
    """Molde naming.root: GEP - {produto} - 0. [PAI]. Sem prefixo duplicado."""
    text = (name or "").strip()
    while text.startswith(ROOT_PREFIX):
        text = text[len(ROOT_PREFIX) :].strip()
    if text.endswith(ROOT_SUFFIX):
        text = text[: -len(ROOT_SUFFIX)].strip()
    if not text:
        return (name or "").strip()
    return f"{ROOT_PREFIX}{text}{ROOT_SUFFIX}"


def load_glpi_ids(repo_root: Path) -> dict[str, str]:
    """Lê project_id e ticket_id. Em homolog, o bloco homolog: vence."""
    path = repo_root / ".glpi" / "project.yaml"
    top: dict[str, str] = {}
    homolog: dict[str, str] = {}
    section = ""
    if path.is_file():
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if re.match(r"^homolog:\s*$", raw):
                section = "homolog"
                continue
            if re.match(r"^[A-Za-z]", raw):
                section = ""
            match = re.match(r"^(\s*)(project_id|ticket_id):\s*(.*?)\s*$", raw)
            if not match:
                continue
            indent, key, value = match.groups()
            value = value.strip().strip("\"'")
            if not value:
                continue
            if section == "homolog" and indent:
                homolog[key] = value
            elif not indent:
                top[key] = value
    env = (os.environ.get("GLPI_ENV") or "prod").strip().lower()
    use_homolog = env in ("homolog", "hml", "homo", "homologacao", "homologação")
    chosen = homolog if use_homolog and homolog else top
    return {
        "project_id": chosen.get("project_id") or top.get("project_id") or "",
        "ticket_id": chosen.get("ticket_id") or top.get("ticket_id") or "",
    }


def classify(code: str | None) -> tuple[str, str | None]:
    if not code:
        return "other", None
    text = str(code).strip().upper()
    if re.fullmatch(r"F\d+", text):
        return ("F", None) if text in PHASE_CODES else ("other", None)
    match = SESSION_RE.fullmatch(text)
    if match and match.group(1).upper() in PHASE_CODES:
        return "S", match.group(1).upper()
    match = TASK_RE.fullmatch(text)
    if match:
        parent = match.group(1).upper()
        phase = parent.split(".", 1)[0]
        if phase in PHASE_CODES:
            return "P", parent
    if LEGACY_R_RE.fullmatch(text):
        return "legacy-r", None
    if LEGACY_S_RE.fullmatch(text):
        return "legacy-s", None
    match = LEGACY_P_RE.fullmatch(text)
    if match:
        return "legacy-p", match.group(1).upper()
    return "other", None


def _parse_dt(value) -> datetime | None:
    if not value:
        return None
    text = str(value).strip().replace("T", " ")[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _fmt(value: datetime) -> str:
    return value.replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")


def _git_bounds(repo: Path, token: str, cache: dict) -> tuple[datetime, datetime] | None:
    if not token or token in cache:
        return cache.get(token)
    if not (repo / ".git").exists():
        cache[token] = None
        return None
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo), "log", "-S", token, "--pretty=%cI", "--", "docs"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        out = ""
    stamps = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            stamps.append(datetime.fromisoformat(line).replace(tzinfo=None))
        except ValueError:
            continue
    found = (min(stamps), max(stamps)) if stamps else None
    cache[token] = found
    return found


class _Slots:
    def __init__(self) -> None:
        start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        if start.hour >= 18:
            start = start + timedelta(days=1)
        self.cursor = start

    def take(self) -> tuple[datetime, datetime]:
        while True:
            while self.cursor.weekday() >= 5:
                self.cursor = (self.cursor + timedelta(days=1)).replace(hour=9, minute=0, second=0)
            if self.cursor.hour >= 18 or self.cursor.hour < 9:
                self.cursor = (self.cursor + timedelta(days=1)).replace(hour=9, minute=0, second=0)
                continue
            if self.cursor.hour == 12:
                self.cursor = self.cursor.replace(hour=14)
            end = self.cursor + timedelta(hours=2)
            if end.hour > 18 or (end.hour == 18 and end.minute):
                self.cursor = (self.cursor + timedelta(days=1)).replace(hour=9, minute=0, second=0)
                continue
            start = self.cursor
            self.cursor = end
            return start, end


def _fill_dates(cands: list[dict], repo_root: Path) -> None:
    cache: dict = {}
    slots = _Slots()
    for cand in cands:
        if cand.get("level") not in ("F", "S", "P"):
            continue
        status = str(cand.get("status_local") or cand.get("status") or "").lower()
        realized = status in REALIZED or int(cand.get("percent_done") or 0) > 0
        plan_start = _parse_dt(cand.get("plan_start"))
        plan_end = _parse_dt(cand.get("plan_end"))
        real_start = _parse_dt(cand.get("real_start"))
        real_end = _parse_dt(cand.get("real_end"))
        if realized and (real_start is None or real_end is None):
            bounds = _git_bounds(repo_root, str(cand.get("code") or ""), cache)
            if bounds:
                real_start, real_end = bounds
                cand["temporal_source"] = cand.get("temporal_source") or "git"
        if realized and plan_start is None:
            plan_start = real_start
        if realized and plan_end is None:
            plan_end = real_end
        if realized and plan_start and plan_end and plan_end <= plan_start:
            plan_end = plan_start + timedelta(hours=2)
        if not realized and (plan_start is None or plan_end is None or plan_end <= plan_start):
            plan_start, plan_end = slots.take()
            cand["temporal_source"] = "stipulated"
            real_start = None
            real_end = None
        if plan_start:
            cand["plan_start"] = _fmt(plan_start)
        if plan_end:
            cand["plan_end"] = _fmt(plan_end)
        if realized and real_start and real_end:
            cand["real_start"] = _fmt(real_start)
            cand["real_end"] = _fmt(real_end)
        planned = EFFORT_SECONDS
        if plan_start and plan_end and plan_end > plan_start:
            planned = int((plan_end - plan_start).total_seconds())
        effective = 0
        if realized and real_start and real_end and real_end >= real_start:
            effective = int((real_end - real_start).total_seconds())
        cand["planned_duration"] = planned
        cand["effective_duration"] = effective


def _rollup_windows(cands: list[dict]) -> None:
    by_parent: dict[str, list[dict]] = {}
    for cand in cands:
        parent = str(cand.get("parent_code") or "").upper()
        if parent:
            by_parent.setdefault(parent, []).append(cand)
    for level in ("S", "F"):
        for cand in cands:
            if cand.get("level") != level:
                continue
            kids = by_parent.get(str(cand.get("code") or "").upper()) or []
            starts = [d for d in (_parse_dt(k.get("plan_start")) for k in kids) if d]
            ends = [d for d in (_parse_dt(k.get("plan_end")) for k in kids) if d]
            if not starts or not ends:
                continue
            cand["plan_start"] = _fmt(min(starts))
            cand["plan_end"] = _fmt(max(ends))
            reals = [d for d in (_parse_dt(k.get("real_start")) for k in kids) if d]
            reale = [d for d in (_parse_dt(k.get("real_end")) for k in kids) if d]
            if reals and reale:
                real_start, real_end = min(reals), max(reale)
                cand["real_start"] = _fmt(real_start)
                cand["real_end"] = _fmt(real_end)
                cand["effective_duration"] = int((real_end - real_start).total_seconds())
            else:
                cand["effective_duration"] = 0
            start = _parse_dt(cand["plan_start"])
            end = _parse_dt(cand["plan_end"])
            if start and end and end > start:
                cand["planned_duration"] = int((end - start).total_seconds())


def ensure_fsp(cands: list[dict], repo_root: Path) -> tuple[list[dict], list[dict]]:
    """Garante F1–F5, tira o R legado da lista de apply e preenche datas."""
    kept: list[dict] = []
    legacy: list[dict] = []
    for cand in cands:
        level, parent = classify(cand.get("code"))
        if level == "legacy-r":
            cand["level"] = "legacy-r"
            cand["kind"] = "skip"
            cand["action_hint"] = "SKIP"
            cand["rationale"] = "Titulo R de markdown antigo nao e o projeto GLPI."
            legacy.append(cand)
            continue
        if level == "F":
            cand["kind"] = "phase"
            cand["level"] = "F"
            cand["parent_code"] = None
            cand["title"] = PHASE_TITLES[str(cand.get("code") or "").upper()]
            kept.append(cand)
            continue
        if level in ("S", "P"):
            cand["kind"] = "item"
            cand["level"] = level
            cand["parent_code"] = parent
            kept.append(cand)
            continue
        cand["kind"] = "skip"
        cand["action"] = "SKIP"
        cand["action_hint"] = "SKIP"
        cand["confidence"] = 0
        cand["rationale"] = "Fora de F1-F5, F#.S# e F#.S#.P#. Nao entra na arvore."
        legacy.append(cand)

    have = {str(c.get("code") or "").upper() for c in kept}
    for cand in list(kept):
        if cand.get("level") != "P":
            continue
        parent = str(cand.get("parent_code") or "").upper()
        if not parent or parent in have:
            continue
        phase = parent.split(".", 1)[0]
        kept.append(
            {
                "kind": "item",
                "level": "S",
                "code": parent,
                "parent_code": phase,
                "title": parent,
                "status_local": "pending",
                "percent_done": 0,
                "confidence": 1,
                "phase": phase,
            }
        )
        have.add(parent)

    have = {str(c.get("code") or "").upper() for c in kept}
    for code, title in PHASES:
        if code in have:
            continue
        kept.append(
            {
                "kind": "phase",
                "level": "F",
                "code": code,
                "parent_code": None,
                "title": title,
                "status_local": "pending",
                "percent_done": 0,
                "state": "gep1",
                "confidence": 1,
                "phase_source": "lifecycle",
                "sources": [],
            }
        )
    _fill_dates(kept, repo_root)
    _rollup_windows(kept)
    return kept, legacy


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--format-root-name":
        print(format_root_name(sys.argv[2]))
        return 0
    print("uso: crfsp.py --format-root-name NOME", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
