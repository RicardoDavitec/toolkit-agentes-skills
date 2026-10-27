#!/usr/bin/env python3
"""Espelha pacotes em andamento e futuros como TicketTask do chamado pai.

Entram tarefas F#.S#.P# e sessoes F#.S# que nao tem tarefa filha.
Dry-run por padrão. Produção só grava com --confirm-prod.
Não apaga tarefa. Se o código já está no texto, não grava de novo.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crfsp import EFFORT_SECONDS, DAY_SECONDS, load_glpi_ids  # noqa: E402

CHECKBOX_RE = re.compile(
    r"^\s*[-*]\s*\[([ xX~tT])\]\s+\*\*(F\d+\.S\d+\.P\d+)\*\*\s+(.+)$"
)
MARK = {" ": "pending", "x": "done", "X": "done", "~": "partial", "t": "partial", "T": "partial"}


def _parse(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("T", " ")[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _fmt(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def select_open(items: list[dict], now: datetime) -> list[dict]:
    """[~]/[t] entram. [ ] entra se o início planejado é agora ou depois, ou se não há data."""
    chosen = []
    for item in items:
        status = str(item.get("status") or "").lower()
        if status in ("done", "archived"):
            continue
        if status == "pending":
            start = _parse(item.get("plan_start"))
            if start is not None and start < now:
                continue
        elif status not in ("partial", "pending"):
            continue
        chosen.append(item)
    return chosen


def from_markdown(plans: Path) -> list[dict]:
    items: list[dict] = []
    if not plans.is_dir():
        return items
    for path in sorted(plans.glob("*.md")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for idx, line in enumerate(lines):
            match = CHECKBOX_RE.match(line)
            if not match:
                continue
            mark, code, title = match.groups()
            blob = line
            if idx + 1 < len(lines):
                blob += "\n" + lines[idx + 1]
            plan_start = plan_end = None
            for found in re.finditer(
                r"(plan_start|plan_end)\s*=\s*[\"']([^\"']+)[\"']", blob
            ):
                if found.group(1) == "plan_start":
                    plan_start = found.group(2)
                else:
                    plan_end = found.group(2)
            items.append(
                {
                    "code": code.upper(),
                    "title": title.strip(),
                    "status": MARK.get(mark, "pending"),
                    "plan_start": plan_start,
                    "plan_end": plan_end,
                    "source": str(path),
                }
            )
    return items


def from_report(path: Path) -> list[dict]:
    report = json.loads(path.read_text(encoding="utf-8"))
    cands = list(report.get("candidates") or [])
    parents_with_p = {
        str(c.get("parent_code") or "").upper()
        for c in cands
        if re.fullmatch(r"F\d+\.S\d+\.P\d+", str(c.get("code") or ""), re.I)
    }
    items = []
    for cand in cands:
        code = str(cand.get("code") or "")
        is_task = re.fullmatch(r"F\d+\.S\d+\.P\d+", code, re.I)
        is_session = re.fullmatch(r"F\d+\.S\d+", code, re.I)
        if not is_task and not (is_session and code.upper() not in parents_with_p):
            continue
        status = cand.get("status") or cand.get("status_local")
        if is_session and not status:
            continue
        items.append(
            {
                "code": code.upper(),
                "title": cand.get("title") or code,
                "status": status or "pending",
                "plan_start": cand.get("plan_start"),
                "plan_end": cand.get("plan_end"),
                "source": str(path),
            }
        )
    return items


def _actiontime(start: datetime | None, end: datetime | None) -> int:
    if start and end and end > start:
        delta = int((end - start).total_seconds())
        if 0 < delta <= DAY_SECONDS:
            return delta
    return EFFORT_SECONDS


def _request(api: str, headers: dict, method: str, path: str, payload: dict | None = None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(api + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")[:400]


def main() -> int:
    parser = argparse.ArgumentParser(description="Espelha P em andamento e futuros no chamado pai")
    parser.add_argument("--env", default=os.environ.get("GLPI_ENV", "homolog"), choices=("prod", "homolog"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-prod", action="store_true")
    parser.add_argument("--from", dest="from_path", default="", help="JSON do retro-scan")
    parser.add_argument("--plans", default="docs/05_progresso/planos_ativos")
    parser.add_argument("--ticket", default="")
    parser.add_argument("--only", default="")
    parser.add_argument("--user-id", type=int, default=821)
    parser.add_argument("--group-id", type=int, default=3)
    args = parser.parse_args()

    if args.apply and args.env == "prod" and not args.confirm_prod:
        print("producao exige --confirm-prod. Homologacao e o caminho padrao.")
        return 2

    repo = Path.cwd()
    os.environ["GLPI_ENV"] = args.env
    ids = load_glpi_ids(repo)
    ticket = args.ticket or ids.get("ticket_id") or ""
    if not ticket:
        print("sem ticket_id. Informe --ticket ou preencha .glpi/project.yaml")
        return 2

    if args.from_path:
        items = from_report(Path(args.from_path))
    else:
        items = from_markdown(repo / args.plans)
    only = {c.strip().upper() for c in args.only.split(",") if c.strip()}
    if only:
        items = [i for i in items if i["code"] in only]
    chosen = select_open(items, datetime.now())
    print(f"env={args.env} chamado={ticket} candidatos={len(items)} espelho={len(chosen)} modo={'APPLY' if args.apply else 'DRY-RUN'}")
    for item in chosen:
        print(f"  {item['code']} {item['status']} {item.get('plan_start') or 'sem-data'} {item['title'][:60]}")
    if not args.apply:
        print("dry-run. Reexecute com --apply para gravar TicketTask.")
        return 0

    from env_context import apply_glpi_env
    from states_discover import init_session, kill_session

    info = apply_glpi_env(args.env)
    api = info["api_url"].rstrip("/")
    if args.env == "homolog" and "suporte-homolog" not in api:
        print(f"recusa: URL nao e homolog ({api})")
        return 2
    app = os.environ.get("GLPI_APP_TOKEN")
    session = init_session(api, os.environ["GLPI_USER_TOKEN"], app)
    headers = {"Content-Type": "application/json", "Session-Token": session}
    if app:
        headers["App-Token"] = app
    failed = 0
    created = 0
    skipped = 0
    try:
        code, body = _request(api, headers, "GET", f"/Ticket/{ticket}/TicketTask?range=0-999")
        existing = json.loads(body) if code == 200 and body.strip().startswith("[") else []
        have = "\n".join((row.get("content") or "") for row in existing)

        def already(code: str) -> bool:
            return re.search(rf"(?<![\w.]){re.escape(code)}(?![\w.])", have) is not None
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in chosen:
            if already(item["code"]):
                skipped += 1
                continue
            start = _parse(item.get("plan_start"))
            end = _parse(item.get("plan_end"))
            if start is None or end is None or end <= start:
                start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
                end = start.replace(hour=11)
            payload = {
                "input": {
                    "tickets_id": int(ticket),
                    "content": f"<p>{item['code']} {item['title']}</p>",
                    "begin": _fmt(start),
                    "end": _fmt(end),
                    "actiontime": _actiontime(start, end),
                    "state": 1,
                    "is_private": 0,
                    "users_id_tech": args.user_id,
                    "groups_id_tech": args.group_id,
                    "date": now,
                }
            }
            status, resp = _request(api, headers, "POST", "/TicketTask", payload)
            if status not in (200, 201):
                failed += 1
                print(f"ERRO {item['code']} HTTP {status}: {resp[:160]}")
                continue
            created += 1
        print(f"gravadas={created} ja_existiam={skipped} falhas={failed}")
    finally:
        kill_session(api, session, app)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
