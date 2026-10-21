#!/usr/bin/env python3
"""Preenche janela e esforço de ProjectTask no GLPI.

Campos obrigatórios: plan_start_date, plan_end_date, planned_duration,
effective_duration. A data é a janela. A duração é o esforço, em segundos.

Ordem da evidência no realizado: real_start/real_end já gravados (plano ou
git). A duração efetiva é esse intervalo, em segundos, inclusive quando passa
de um dia. Se as duas datas reais são o mesmo instante, a efetiva fica 0.
Sem datas reais: esforço da janela planejada (pacote sem data = 2 h).
Planejado (percentual 0): duração efetiva 0.

Não sobrescreve data já gravada nem duração já > 0.
Dry-run por padrão. --apply grava no GLPI de produção (ou --env=homolog).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

LEAF_SECONDS = 2 * 3600
PHASE_EMPTY_SECONDS = 8 * 3600
PARTIAL_FLOOR = 30 * 60
EMPTY_DATES = {"", "null", "None", "0000-00-00 00:00:00", "0000-00-00"}


def blank_date(value) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text in EMPTY_DATES or text.startswith("0000-00-00")


def parse_dt(value) -> datetime | None:
    if blank_date(value):
        return None
    text = str(value).strip()[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def fmt_dt(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def as_int(value) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def build_patches(tasks: list[dict]) -> list[dict]:
    """Devolve um patch por tarefa que ainda tem lacuna temporal."""
    by_id = {int(t["id"]): t for t in tasks if t.get("id") is not None}
    children: dict[int, list[int]] = {}
    for task in by_id.values():
        parent = int(task.get("projecttasks_id") or 0)
        children.setdefault(parent, []).append(int(task["id"]))

    planned: dict[int, int] = {}
    effective: dict[int, int] = {}

    def walk(task_id: int) -> None:
        kids = [kid for kid in children.get(task_id, []) if kid in by_id]
        for kid in kids:
            walk(kid)
        task = by_id[task_id]
        percent = as_int(task.get("percent_done"))
        if kids:
            planned[task_id] = sum(planned[kid] for kid in kids)
            effective[task_id] = sum(effective[kid] for kid in kids)
            return
        is_leaf = int(task.get("projecttasks_id") or 0) in by_id
        effort = LEAF_SECONDS if is_leaf else PHASE_EMPTY_SECONDS
        planned[task_id] = effort
        real_start = parse_dt(task.get("real_start_date"))
        real_end = parse_dt(task.get("real_end_date"))
        plan_start = parse_dt(task.get("plan_start_date"))
        plan_end = parse_dt(task.get("plan_end_date"))
        span = 0
        if real_start and real_end and real_end >= real_start:
            span = int((real_end - real_start).total_seconds())
        if plan_start and plan_end and plan_end > plan_start:
            effort = int((plan_end - plan_start).total_seconds())
        if percent <= 0:
            effective[task_id] = 0
        elif span > 0 or (real_start and real_end):
            effective[task_id] = span
        elif percent >= 100:
            effective[task_id] = effort
        else:
            effective[task_id] = max(PARTIAL_FLOOR, int(effort * percent / 100))

    for task_id, task in by_id.items():
        if int(task.get("projecttasks_id") or 0) not in by_id:
            walk(task_id)

    patches: list[dict] = []
    for task_id, task in by_id.items():
        patch: dict = {}
        if as_int(task.get("planned_duration")) <= 0:
            patch["planned_duration"] = planned[task_id]
        if as_int(task.get("effective_duration")) <= 0:
            patch["effective_duration"] = effective[task_id]
        if blank_date(task.get("plan_start_date")):
            start = parse_dt(task.get("real_start_date")) or parse_dt(task.get("date_creation"))
            if start is None:
                start = datetime.now().replace(microsecond=0)
            patch["plan_start_date"] = fmt_dt(start)
            if blank_date(task.get("plan_end_date")):
                patch["plan_end_date"] = fmt_dt(start + timedelta(seconds=planned[task_id]))
        elif blank_date(task.get("plan_end_date")):
            start = parse_dt(task.get("plan_start_date"))
            if start is not None:
                patch["plan_end_date"] = fmt_dt(start + timedelta(seconds=planned[task_id]))
        if not patch:
            continue
        patches.append(
            {
                "id": task_id,
                "name": task.get("name") or "",
                "percent_done": as_int(task.get("percent_done")),
                "input": patch,
            }
        )
    return patches


def _request(api: str, headers: dict, method: str, path: str, payload: dict | None = None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(api + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Preenche datas e durações de ProjectTask")
    parser.add_argument("--project", type=int, required=True)
    parser.add_argument("--env", default="prod", choices=("prod", "homolog"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    lib = Path(__file__).resolve().parent
    sys.path.insert(0, str(lib))
    from env_context import apply_glpi_env
    from states_discover import init_session, kill_session

    info = apply_glpi_env(args.env)
    api = os.environ["GLPI_API_URL"].rstrip("/")
    app = os.environ.get("GLPI_APP_TOKEN")
    session = init_session(api, os.environ["GLPI_USER_TOKEN"], app)
    headers = {"Content-Type": "application/json", "Session-Token": session}
    if app:
        headers["App-Token"] = app
    print(f"env={info['env']} project={args.project} modo={'APPLY' if args.apply else 'DRY-RUN'}")
    try:
        code, body = _request(api, headers, "GET", f"/Project/{args.project}/ProjectTask?range=0-999")
        if code != 200:
            print(f"falha ao listar tarefas HTTP {code}: {body[:240]}")
            return 1
        tasks = json.loads(body)
        if not isinstance(tasks, list):
            print("resposta inesperada ao listar tarefas")
            return 1
        patches = build_patches(tasks)
        planned_h = sum(p["input"].get("planned_duration", 0) for p in patches) / 3600
        effective_h = sum(p["input"].get("effective_duration", 0) for p in patches) / 3600
        dates = sum(1 for p in patches if "plan_start_date" in p["input"])
        print(
            f"tarefas={len(tasks)} patches={len(patches)} "
            f"datas_novas={dates} esforco_planejado_h={planned_h:.1f} "
            f"esforco_efetivo_h={effective_h:.1f}"
        )
        for item in patches:
            fields = ",".join(sorted(item["input"]))
            print(f"  {item['id']} %{item['percent_done']} {fields} {(item['name'] or '')[:60]}")
        if not args.apply:
            print("dry-run. Reexecute com --apply para gravar.")
            return 0
        failed = 0
        for item in patches:
            code, body = _request(
                api,
                headers,
                "PUT",
                f"/ProjectTask/{item['id']}",
                {"input": item["input"]},
            )
            if code not in (200, 201):
                failed += 1
                print(f"ERRO {item['id']} HTTP {code}: {body[:180]}")
        print(f"gravados={len(patches) - failed} falhas={failed}")
        return 1 if failed else 0
    finally:
        kill_session(api, session, app)


if __name__ == "__main__":
    sys.exit(main())
