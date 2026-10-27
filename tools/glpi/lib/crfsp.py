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
    drop = _rename_day(repo)
    stamps = [s for s in stamps if drop is None or s.date().isoformat() != drop]
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


_RENAME_SHA = "96fa03f"
_F_CODE_RE = re.compile(r"(?<![\w.])(F\d+(?:\.S\d+(?:\.P\d+)?)?)(?![\w.])")
_LEGACY_CODE_RE = re.compile(
    r"(?<![\w.])((?:RF|CO|SL|[SRIHE])\d+(?:\.[Pp]\d+[a-z]?)?)(?![\w.])"
)
_ESTIMATE_MINUTES = int(os.environ.get("GLPI_RETRO_ESTIMATE_MINUTES", "60"))
_EXPLICIT_SOURCES = ("checklist-tempo", "checklist-comment")


def _rename_cutoff(repo: Path) -> str | None:
    """Commit de rename dos códigos, só se existir neste repositório."""
    sha = (os.environ.get("GLPI_RENAME_SHA") or _RENAME_SHA).strip()
    if not sha:
        return None
    proc = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", sha + "^{commit}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return sha if proc.returncode == 0 else None


def _rename_day(repo: Path) -> str | None:
    sha = _rename_cutoff(repo)
    if not sha:
        return None
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo), "log", "-1", "--pretty=%cI", sha],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return datetime.fromisoformat(out).date().isoformat()
    except (subprocess.CalledProcessError, ValueError):
        return None


def _norm_title(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())[:48]


def _legacy_map(repo: Path) -> dict[str, str]:
    """Código F atual → código que o git e as sessões ainda citam."""
    cutoff = _rename_cutoff(repo)
    if not cutoff:
        return {}
    files = subprocess.check_output(
        ["git", "-C", str(repo), "diff", "--name-only", f"{cutoff}^", "HEAD", "--", "docs/05_progresso/planos_ativos"],
        text=True,
        stderr=subprocess.DEVNULL,
    ).split()
    bold = re.compile(r"\*\*([A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*)\*\*\s*(.*)$")
    out: dict[str, str] = {}

    def extract(rev: str, path: str) -> list[tuple[str, str]]:
        try:
            text = subprocess.check_output(
                ["git", "-C", str(repo), "show", f"{rev}:{path}"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            return []
        rows = []
        for line in text.splitlines():
            match = bold.search(line)
            if not match:
                continue
            if line.lstrip()[:1] in "-*|":
                rows.append((match.group(1), _norm_title(match.group(2))))
        return rows

    for path in files:
        if not path.endswith(".md"):
            continue
        old = extract(f"{cutoff}^", path)
        new = extract("HEAD", path)
        used: set[int] = set()
        for code, title in old:
            if not title:
                continue
            for index, (code2, title2) in enumerate(new):
                if index in used or title != title2:
                    continue
                used.add(index)
                if code != code2 and FSP_RE.fullmatch(code2):
                    out[code2.upper()] = code
                break
    return out


def _plan_windows(repo: Path) -> dict[str, tuple[datetime, datetime]]:
    windows: dict[str, tuple[datetime, datetime]] = {}
    root = repo / "docs/05_progresso/planos_ativos"
    if not root.is_dir():
        return windows
    for path in root.glob("*.md"):
        headers: list[str] | None = None
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.startswith("|"):
                headers = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            low = [c.lower() for c in cells]
            if "plan ini" in low and ("code" in low or "id" in low or "código" in low or "codigo" in low):
                headers = low
                continue
            if not headers or len(cells) < len(headers):
                continue
            if set(low) & {"code", "id", "titulo", "título", "plan ini"}:
                continue
            got = {headers[i]: cells[i] for i in range(min(len(headers), len(cells)))}
            code = (got.get("code") or got.get("id") or got.get("código") or got.get("codigo") or "").upper()
            if not FSP_RE.fullmatch(code):
                continue
            start = _parse_dt(got.get("plan ini"))
            end = _parse_dt(got.get("plan fim"))
            if start and end and end > start:
                windows[code] = (start, end)
    return windows


def _close_commits(repo: Path) -> dict[str, tuple[str, datetime]]:
    """Primeiro commit que marcou o código legado como feito. Ignora o rename, se houver."""
    cutoff = _rename_cutoff(repo)
    cmd = [
        "git", "-C", str(repo), "log", "--reverse", "-p",
        "--pretty=format:%H%x00%cI",
    ]
    if cutoff:
        cmd.append(cutoff + "^")
    cmd.extend(["--", "docs/05_progresso/planos_ativos"])
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        text=True,
        stderr=subprocess.DEVNULL,
    )
    closed: dict[tuple[str, str], tuple[str, datetime]] = {}
    sha = ""
    path = ""
    when: datetime | None = None
    assert proc.stdout is not None
    for raw in proc.stdout:
        line = raw.rstrip("\n")
        if line.startswith("diff --git "):
            path = line.split(" b/", 1)[-1].strip()
            continue
        if "\x00" in line and not line.startswith(("+", "-", " ", "@", "d", "i")):
            sha, iso = line.split("\x00", 1)
            if cutoff and sha.startswith(cutoff):
                sha = ""
                when = None
                continue
            try:
                when = datetime.fromisoformat(iso.strip()).replace(tzinfo=None)
            except ValueError:
                when = None
            continue
        if not sha or when is None or not path or not line.startswith("+") or line.startswith("+++"):
            continue
        body = line[1:]
        if not re.search(r"\[x\]", body, re.I):
            continue
        found: list[str] = []
        bold = re.search(r"\*\*([A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*)\*\*", body)
        if bold and re.search(r"\[x\]", body[: bold.start()], re.I):
            found.append(bold.group(1))
        elif body.lstrip().startswith("|"):
            cells = [re.sub(r"[*`]", "", c).strip() for c in body.strip().strip("|").split("|")]
            token = cells[0] if cells else ""
            if re.fullmatch(r"[A-Za-z][A-Za-z0-9.]*(?:\.[A-Za-z0-9]+)*", token):
                if any(re.search(r"\[x\]", c, re.I) for c in cells):
                    found.append(token)
        for code in found:
            key = (path, code.upper())
            if key not in closed:
                closed[key] = (sha, when)
    proc.wait()
    return closed


def _commit_times(repo: Path) -> list[datetime]:
    cmd = ["git", "-C", str(repo), "log", "--pretty=%cI"]
    cutoff = _rename_cutoff(repo)
    if cutoff:
        cmd.append(cutoff + "^")
    out = subprocess.check_output(
        cmd,
        text=True,
        stderr=subprocess.DEVNULL,
    )
    times = []
    for line in out.splitlines():
        try:
            times.append(datetime.fromisoformat(line.strip()).replace(tzinfo=None))
        except ValueError:
            continue
    times.sort()
    return times


def _session_index(repo: Path) -> dict[str, list[datetime]]:
    index: dict[str, list[datetime]] = {}
    root = repo / "docs/05_progresso/geral"
    enc = re.compile(r"Encerrada:\s*(\d{2})/(\d{2})/(\d{4})\s+(\d{2}):(\d{2})")
    for path in root.glob("SESSAO_*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        found = enc.search(text)
        stamp = None
        if found:
            day, month, year, hour, minute = found.groups()
            stamp = datetime(int(year), int(month), int(day), int(hour), int(minute))
        else:
            name = re.search(r"SESSAO_(\d{4})-(\d{2})-(\d{2})", path.name)
            if not name:
                continue
            year, month, day = name.groups()
            stamp = datetime(int(year), int(month), int(day), 18, 0)
        for code in _LEGACY_CODE_RE.findall(text):
            index.setdefault(code.upper(), []).append(stamp)
    return index


def _prev_same_day(times: list[datetime], moment: datetime) -> datetime | None:
    prev = None
    for item in times:
        if item >= moment:
            break
        if item.date() == moment.date():
            prev = item
    return prev


def _loose_dt(text: str) -> datetime | None:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2}))?", (text or "").strip())
    if not match:
        return None
    year, month, day, hour, minute = match.groups()
    return datetime(int(year), int(month), int(day), int(hour or 0), int(minute or 0))


def _codes_in(text: str) -> set[str]:
    found = {c.upper() for c in _F_CODE_RE.findall(text or "")}
    found.update(c.upper() for c in _LEGACY_CODE_RE.findall(text or ""))
    return found


def _pendency_index(repo: Path) -> dict[str, tuple[datetime, datetime]]:
    """Pendência [x] que cita um code: inserido → corrigido."""
    path = repo / "docs/05_progresso/pendencias/CHECKLIST_PENDENCIAS.md"
    if not path.is_file():
        return {}
    out: dict[str, tuple[datetime, datetime]] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("| PEND-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or "[x]" not in cells[1].lower():
            continue
        start = _loose_dt(cells[3])
        end = _loose_dt(cells[4])
        if not start or not end or end <= start:
            continue
        for code in _codes_in(cells[5]):
            out.setdefault(code, (start, end))
    return out


def _note_stamp(path: Path) -> datetime | None:
    name = path.name
    iso = re.search(r"(20\d{2})-(\d{2})-(\d{2})", name)
    if iso:
        year, month, day = (int(p) for p in iso.groups())
        return datetime(year, month, day, 9, 0)
    short = re.search(r"(?<!\d)(\d{2})-(\d{2})-(\d{2})(?!\d)", name)
    if short:
        day, month, year = (int(p) for p in short.groups())
        return datetime(2000 + year, month, day, 9, 0)
    return None


def _note_index(repo: Path) -> dict[str, tuple[datetime, datetime]]:
    """Nota em implementação ou operação que cita um code. Janela de 60 min."""
    out: dict[str, tuple[datetime, datetime]] = {}
    roots = [
        repo / "docs/03_implementacao",
        repo / "docs/04_operacao",
    ]
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            stamp = _note_stamp(path)
            if stamp is None:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            end = stamp + timedelta(minutes=_ESTIMATE_MINUTES)
            for code in _codes_in(text):
                out.setdefault(code, (stamp, end))
    return out


def _explicit_real(cand: dict) -> bool:
    if str(cand.get("temporal_source") or "") not in _EXPLICIT_SOURCES:
        return False
    return bool(_parse_dt(cand.get("real_start")) and _parse_dt(cand.get("real_end")))


def correlate_realized(cands: list[dict], repo_root: Path) -> int:
    """Datas reais das tarefas feitas: commit que fechou + sessão do dia.

    Várias tarefas no mesmo commit dividem o intervalo desde o commit anterior
    do dia (ou 60 min, se o commit abre o dia / o vão passa de 6 h).
    """
    if not (repo_root / ".git").exists():
        return 0
    legacy = _legacy_map(repo_root)
    windows = _plan_windows(repo_root)
    closed = _close_commits(repo_root)
    times = _commit_times(repo_root)
    sessions = _session_index(repo_root)
    pendencies = _pendency_index(repo_root)
    notes = _note_index(repo_root)

    groups: dict[str, list[dict]] = {}
    for cand in cands:
        status = str(cand.get("status_local") or cand.get("status") or "").lower()
        if status not in ("done", "archived"):
            continue
        if cand.get("level") not in ("S", "P"):
            continue
        if _explicit_real(cand):
            continue
        code = str(cand.get("code") or "").upper()
        old = legacy.get(code, "")
        src = ""
        for source in cand.get("sources") or []:
            if source.get("path"):
                src = str(source["path"])
                break
        hit = closed.get((src, old)) or closed.get((src, code))
        if not hit:
            continue
        sha, _when = hit
        cand["_close_sha"] = sha
        cand["_close_at"] = hit[1]
        cand["_legacy"] = old
        groups.setdefault(sha, []).append(cand)

    def sort_key(cand: dict) -> int:
        for source in cand.get("sources") or []:
            if source.get("line"):
                return int(source["line"])
        return 0

    later_by_sha: set[str] = set()
    by_day: dict = {}
    for sha, items in groups.items():
        by_day.setdefault(items[0]["_close_at"].date(), []).append(items[0]["_close_at"])
    for sha, items in groups.items():
        moment = items[0]["_close_at"]
        if any(other > moment for other in by_day.get(moment.date(), [])):
            later_by_sha.add(sha)

    changed = 0
    placed: set[str] = set()
    for sha, items in groups.items():
        moment = items[0]["_close_at"]
        end = moment
        if sha not in later_by_sha:
            mentioned = []
            for cand in items:
                old = cand.get("_legacy") or ""
                mentioned.extend(sessions.get(old, []))
                mentioned.extend(sessions.get(str(cand.get("code") or "").upper(), []))
            same_day = [s for s in mentioned if s.date() == moment.date() and s > moment]
            if same_day:
                latest = max(same_day)
                if latest - moment <= timedelta(hours=3):
                    end = latest
        prev = _prev_same_day(times, moment)
        if prev and timedelta(0) < moment - prev <= timedelta(hours=6):
            start = prev
        else:
            start = end - timedelta(minutes=_ESTIMATE_MINUTES)
        if start >= end:
            start = end - timedelta(minutes=_ESTIMATE_MINUTES)
        parents = {str(c.get("code") or "").upper() for c in items}
        tasks = [
            c for c in items
            if c.get("level") == "P" or str(c.get("parent_code") or "").upper() not in parents and not any(
                str(o.get("parent_code") or "").upper() == str(c.get("code") or "").upper() for o in items
            )
        ]
        if not tasks:
            tasks = items
        tasks.sort(key=sort_key)
        budget = end - start
        slice_td = budget / len(tasks)
        for index, cand in enumerate(tasks):
            real_start = start + slice_td * index
            real_end = start + slice_td * (index + 1)
            code = str(cand.get("code") or "").upper()
            table = windows.get(code)
            if table and table[0] <= real_end:
                plan_start, plan_end = table
                if plan_end < real_end:
                    plan_end = real_end
            else:
                plan_start, plan_end = real_start, real_end
            cand["plan_start"] = _fmt(plan_start)
            cand["plan_end"] = _fmt(plan_end)
            cand["real_start"] = _fmt(real_start)
            cand["real_end"] = _fmt(real_end)
            cand["temporal_source"] = "commit-session" if end != moment else "commit-chain"
            cand["planned_duration"] = int((plan_end - plan_start).total_seconds())
            cand["effective_duration"] = max(0, int((real_end - real_start).total_seconds()))
            placed.add(code)
            changed += 1

    for cand in cands:
        status = str(cand.get("status_local") or cand.get("status") or "").lower()
        if status not in ("done", "archived"):
            continue
        if cand.get("level") not in ("S", "P"):
            continue
        code = str(cand.get("code") or "").upper()
        if code in placed or _explicit_real(cand):
            if _explicit_real(cand):
                placed.add(code)
            continue
        old = str(cand.get("_legacy") or legacy.get(code, ""))
        hit = pendencies.get(old) or pendencies.get(code)
        source = "pendency"
        if not hit:
            hit = notes.get(old) or notes.get(code)
            source = "note"
        if not hit:
            continue
        real_start, real_end = hit
        table = windows.get(code)
        if table and table[0] <= real_end:
            plan_start, plan_end = table
            if plan_end < real_end:
                plan_end = real_end
        else:
            plan_start, plan_end = real_start, real_end
        cand["plan_start"] = _fmt(plan_start)
        cand["plan_end"] = _fmt(plan_end)
        cand["real_start"] = _fmt(real_start)
        cand["real_end"] = _fmt(real_end)
        cand["temporal_source"] = source
        cand["planned_duration"] = int((plan_end - plan_start).total_seconds())
        cand["effective_duration"] = max(0, int((real_end - real_start).total_seconds()))
        placed.add(code)
        changed += 1

    by_parent: dict[str, list[dict]] = {}
    for cand in cands:
        parent = str(cand.get("parent_code") or "").upper()
        if parent:
            by_parent.setdefault(parent, []).append(cand)
    for cand in cands:
        if cand.get("level") != "S":
            continue
        status = str(cand.get("status_local") or cand.get("status") or "").lower()
        if status not in ("done", "archived"):
            continue
        if _explicit_real(cand):
            continue
        kids = [
            k for k in by_parent.get(str(cand.get("code") or "").upper(), [])
            if str(k.get("code") or "").upper() in placed
        ]
        if not kids:
            continue
        plan_start = min(_parse_dt(k["plan_start"]) for k in kids)
        plan_end = max(_parse_dt(k["plan_end"]) for k in kids)
        real_start = min(_parse_dt(k["real_start"]) for k in kids)
        real_end = max(_parse_dt(k["real_end"]) for k in kids)
        cand["plan_start"] = _fmt(plan_start)
        cand["plan_end"] = _fmt(plan_end)
        cand["real_start"] = _fmt(real_start)
        cand["real_end"] = _fmt(real_end)
        cand["temporal_source"] = "children"
        cand["planned_duration"] = int((plan_end - plan_start).total_seconds())
        cand["effective_duration"] = int((real_end - real_start).total_seconds())
        placed.add(str(cand.get("code") or "").upper())
        changed += 1
    for cand in cands:
        cand.pop("_close_sha", None)
        cand.pop("_close_at", None)
        cand.pop("_legacy", None)
    return changed


def _durations(plan_start, plan_end, real_start, real_end, realized: bool) -> tuple[int, int]:
    """Segundos. Efetiva fica 0 enquanto não houver início e fim reais."""
    planned = EFFORT_SECONDS
    if plan_start and plan_end and plan_end > plan_start:
        planned = int((plan_end - plan_start).total_seconds())
    effective = 0
    if realized and real_start and real_end and real_end >= real_start:
        effective = max(0, int((real_end - real_start).total_seconds()))
    return planned, effective


def _fill_dates(cands: list[dict], repo_root: Path) -> None:
    correlate_realized(cands, repo_root)
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
        if (
            realized
            and status != "partial"
            and cand.get("temporal_source") not in (
                "commit-chain",
                "commit-session",
                "children",
                "checklist-tempo",
                "checklist-comment",
                "pendency",
                "note",
            )
            and (real_start is None or real_end is None)
        ):
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
        source = str(cand.get("temporal_source") or "")
        # Pack/commit já trouxe janela válida: não sobrescrever com slot estipulado.
        pack_kept = source in ("pack", "pack-lifecycle", "children", "commit-chain", "commit-session") and bool(
            plan_start and plan_end and plan_end > plan_start
        )
        if not realized and not pack_kept and (
            plan_start is None or plan_end is None or plan_end <= plan_start
        ):
            plan_start, plan_end = slots.take()
            cand["temporal_source"] = "stipulated"
            real_start = None
            real_end = None
        if not realized and pack_kept:
            # Planejado com evidência de pack: efetiva 0 até realizar.
            if status == "pending":
                real_start = None
                real_end = None
        if plan_start:
            cand["plan_start"] = _fmt(plan_start)
        if plan_end:
            cand["plan_end"] = _fmt(plan_end)
        if realized and real_start and real_end:
            cand["real_start"] = _fmt(real_start)
            cand["real_end"] = _fmt(real_end)
        elif not realized:
            cand["real_start"] = None
            cand["real_end"] = None
        planned, effective = _durations(plan_start, plan_end, real_start, real_end, realized and bool(real_end))
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
                cand["temporal_source"] = "children"
            else:
                cand["effective_duration"] = 0
                if cand.get("temporal_source") in (None, "", "stipulated"):
                    cand["temporal_source"] = "children"
            start = _parse_dt(cand["plan_start"])
            end = _parse_dt(cand["plan_end"])
            if start and end and end > start:
                cand["planned_duration"] = int((end - start).total_seconds())


def _rollup_status(cands: list[dict]) -> None:
    """Propaga status/percent/% GEP dos filhos para S e F."""
    by_parent: dict[str, list[dict]] = {}
    for cand in cands:
        parent = str(cand.get("parent_code") or "").upper()
        if parent:
            by_parent.setdefault(parent, []).append(cand)
    for level in ("S", "F"):
        for cand in cands:
            if cand.get("level") != level:
                continue
            kids = [
                k
                for k in by_parent.get(str(cand.get("code") or "").upper(), [])
                if k.get("level") in ("S", "P")
            ]
            if not kids:
                continue
            statuses = [str(k.get("status_local") or "pending").lower() for k in kids]
            if all(s in ("done", "archived") for s in statuses):
                cand["status_local"] = "done"
                cand["percent_done"] = 100
                cand["state"] = "gep7"
            elif all(s == "pending" for s in statuses):
                cand["status_local"] = "pending"
                cand["percent_done"] = 0
                cand["state"] = cand.get("state") or "gep1"
            else:
                pcts = [int(k.get("percent_done") or 0) for k in kids]
                avg = int(round(sum(pcts) / len(pcts))) if pcts else 50
                cand["status_local"] = "partial"
                cand["percent_done"] = avg
                cand["state"] = "gep3"


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
    _rollup_status(kept)
    # Segundo passe: S/F que saíram de pending herdam real_* dos filhos.
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
