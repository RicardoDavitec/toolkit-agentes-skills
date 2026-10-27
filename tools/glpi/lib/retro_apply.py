#!/usr/bin/env python3
"""glpi-retro-apply — aplica candidatos do retro-scan em ordem pai(S) → filho(P).

Dry-run por padrão. Com --apply chama `glpi task upsert` de verdade.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Alinhado ao teto do retro_scan (GLPI_RETRO_CONTENT_MAX)
CONTENT_MAX = int(os.environ.get("GLPI_RETRO_CONTENT_MAX", "4000"))
EFFORT_SECONDS = 2 * 3600
DAY_BUCKET = 8 * 3600


def _parse_ts(value) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def temporal_duration_args(c: dict) -> list[str]:
    """Duração planejada e efetiva, em segundos.

    A planejada é o intervalo entre as datas planejadas. Sem essas datas, fica 2 h.
    A efetiva do realizado é o intervalo real (0 se o commit for um instante).
    A efetiva do planejado é 0.
    """
    g = c.get("suggested_glpi") or {}

    def pick(key: str):
        return g.get(key) or c.get(key)

    plan_start = _parse_ts(pick("plan_start"))
    plan_end = _parse_ts(pick("plan_end"))
    real_start = _parse_ts(pick("real_start"))
    real_end = _parse_ts(pick("real_end"))
    status = str(c.get("status") or "").lower()
    try:
        percent = int(c.get("percent_done") if c.get("percent_done") is not None else g.get("percent_done") or 0)
    except (TypeError, ValueError):
        percent = 0
    realized = status in ("done", "archived", "partial") or percent > 0
    planned = EFFORT_SECONDS
    if plan_start and plan_end and plan_end > plan_start:
        planned = int((plan_end - plan_start).total_seconds())
    if not realized:
        effective = 0
    elif real_start and real_end and real_end >= real_start:
        effective = int((real_end - real_start).total_seconds())
    else:
        effective = 0
    return [f"--planned-duration={planned}", f"--effective-duration={effective}"]


def parse_phase_projects(raw: str) -> dict[str, str]:
    """F1:91,F2:92 — sessão e tarefa nascem no subprojeto da fase."""
    out: dict[str, str] = {}
    for part in (raw or "").split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise SystemExit(f"phase-projects invalido: {part} (use F1:91)")
        key, value = part.split(":", 1)
        key, value = key.strip().upper(), value.strip()
        if not key or not value.isdigit():
            raise SystemExit(f"phase-projects invalido: {part}")
        out[key] = value
    return out


def phase_key(c: dict) -> str:
    code = str(c.get("code") or "").upper()
    return code.split(".", 1)[0]


def sort_for_apply(cands: list[dict]) -> list[dict]:
    def key(c: dict):
        kind_order = 0 if c.get("kind") == "phase" else 1
        return (
            kind_order,
            c.get("parent_code") or "",
            c.get("code") or "",
            c.get("title") or "",
        )

    return sorted(cands, key=key)


def build_upsert_args(c: dict, apply: bool) -> list[str] | None:
    g = c.get("suggested_glpi") or {}
    name = (g.get("name") or c.get("title") or "").strip()
    code = (g.get("code") or c.get("code") or "").strip()
    if not name:
        return None
    # códigos instáveis (S4.P?) — upsert só por name
    unstable = (not code) or code.endswith(".P?") or code == "?"
    args = ["task", "upsert", f"--name={name}"]
    if not unstable:
        args.append(f"--code={code}")
    parent = g.get("parent_code") or c.get("parent_code")
    if parent and (c.get("kind") == "item" or (code and ".P" in code.upper())):
        args.append(f"--parent-code={parent}")
    kind = g.get("kind") or c.get("kind")
    if kind:
        args.append(f"--kind={kind}")
    pct = g.get("percent_done", c.get("percent_done"))
    if pct is not None:
        args.append(f"--percent={pct}")
    state = g.get("state") or c.get("state")
    if state:
        args.append(f"--state={state}")
    content = g.get("content")
    if content:
        args.append(f"--content={content[:CONTENT_MAX]}")
    for flag, key in (
        ("--plan-start", "plan_start"),
        ("--plan-end", "plan_end"),
        ("--real-start", "real_start"),
        ("--real-end", "real_end"),
    ):
        val = g.get(key) or c.get(key)
        if val:
            # CLI aceita YYYY-MM-DD
            args.append(f"{flag}={str(val)[:19]}")
    args.extend(temporal_duration_args(c))
    if apply:
        args.append("--apply")
    return args


def glpi_prefix_args() -> list[str]:
    """Prefixo global --env= para o CLI bash (homolog/prod)."""
    env = (os.environ.get("GLPI_ENV") or "prod").strip().lower()
    if env in ("hml", "homo", "homologacao", "homologação"):
        env = "homolog"
    if env == "homolog":
        return ["--env=homolog"]
    return ["--env=prod"]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Aplica JSON do retro-scan (pais S antes dos filhos P). Dry-run padrao."
    )
    ap.add_argument("--from", dest="from_path", required=True, help="JSON gerado pelo retro-scan")
    ap.add_argument("--glpi-bin", default="", help="Caminho do CLI glpi (default: tools/glpi/glpi)")
    ap.add_argument("--apply", action="store_true", help="Grava no GLPI (sem isso = dry-run)")
    ap.add_argument(
        "--env",
        default=os.environ.get("GLPI_ENV", "prod"),
        help="prod|homolog (default: GLPI_ENV ou prod)",
    )
    ap.add_argument(
        "--include-skip",
        action="store_true",
        help="Inclui action=SKIP (re-upsert). Padrao: so NEW",
    )
    ap.add_argument("--kinds", default="phase,item", help="phase,item ou so phase")
    ap.add_argument("--limit", type=int, default=0, help="Max candidatos (0=todos)")
    ap.add_argument("--codes", default="", help="Filtro CSV de codes (ex: S4,S4.P1)")
    ap.add_argument("--continue-on-error", action="store_true")
    ap.add_argument(
        "--phase-projects",
        default="",
        help="Mapa fase=subprojeto, ex. F1:91,F2:92. A fase não vira ProjectTask.",
    )
    args = ap.parse_args()
    phase_projects = parse_phase_projects(args.phase_projects)

    src = Path(args.from_path)
    if not src.is_file():
        print(f"erro: arquivo nao encontrado: {src}", file=sys.stderr)
        return 1

    report = json.loads(src.read_text(encoding="utf-8"))
    cands = list(report.get("candidates") or [])

    kinds = {k.strip() for k in args.kinds.split(",") if k.strip()}
    code_filter = {c.strip().upper() for c in args.codes.split(",") if c.strip()}

    selected: list[dict] = []
    for c in cands:
        if c.get("kind") not in kinds:
            continue
        action = c.get("action", "NEW")
        if not args.include_skip and action != "NEW":
            continue
        code = (c.get("code") or "").upper()
        if code_filter and code not in code_filter:
            continue
        selected.append(c)

    selected = sort_for_apply(selected)
    if args.limit and args.limit > 0:
        selected = selected[: args.limit]

    glpi = args.glpi_bin
    if not glpi:
        # tools/glpi/lib/retro_apply.py → tools/glpi/glpi
        glpi = str(Path(__file__).resolve().parent.parent / "glpi")

    os.environ["GLPI_ENV"] = args.env
    prefix = glpi_prefix_args()

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(
        json.dumps(
            {
                "ok": True,
                "mode": mode,
                "env": os.environ.get("GLPI_ENV", "prod"),
                "from": str(src),
                "selected": len(selected),
                "phases": sum(1 for c in selected if c.get("kind") == "phase"),
                "items": sum(1 for c in selected if c.get("kind") != "phase"),
            },
            ensure_ascii=False,
        )
    )

    ok = 0
    fail = 0
    for i, c in enumerate(selected, 1):
        phase_id = phase_projects.get(phase_key(c), "")
        if phase_id and c.get("kind") == "phase":
            print(
                f"[{i}/{len(selected)}] SKIP fase {c.get('code')} já é o subprojeto {phase_id}",
                file=sys.stderr,
            )
            continue
        upsert_args = build_upsert_args(c, args.apply)
        if not upsert_args:
            print(f"[{i}/{len(selected)}] SKIP sem nome: {c.get('code')}", file=sys.stderr)
            continue
        if phase_id:
            kept = []
            for arg in upsert_args:
                if arg.startswith("--parent-code="):
                    parent = arg.split("=", 1)[1].upper()
                    if parent in phase_projects:
                        continue
                kept.append(arg)
            upsert_args = kept
            upsert_args.append(f"--project={phase_id}")
            code = str(c.get("code") or "").upper()
            if ".P" not in code:
                upsert_args.append("--parent-task=0")
        label = f"{c.get('kind')}:{c.get('code') or '-'} ← {c.get('parent_code') or '-'}"
        print(f"\n=== [{i}/{len(selected)}] {label} | {c.get('title', '')[:60]} ===", file=sys.stderr)
        cmd = [glpi, *prefix, *upsert_args]
        print("+ " + " ".join(cmd), file=sys.stderr)
        try:
            proc = subprocess.run(cmd, check=False)
            if proc.returncode == 0:
                ok += 1
            else:
                fail += 1
                print(f"falha exit={proc.returncode}", file=sys.stderr)
                if not args.continue_on_error:
                    break
        except OSError as e:
            fail += 1
            print(f"erro ao executar glpi: {e}", file=sys.stderr)
            if not args.continue_on_error:
                return 1

    summary = {"ok_count": ok, "fail_count": fail, "mode": mode}
    print(json.dumps(summary, ensure_ascii=False))
    if fail:
        return 1
    if not args.apply:
        print(
            "Dry-run concluido. Revise e reexecute com --apply para gravar.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
