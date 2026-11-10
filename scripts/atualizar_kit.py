#!/usr/bin/env python3
"""atualizar_kit.py — verifica updates no toolkit-agentes-skills e sincroniza no produto.

Uso tipico (a partir do kit ou via wrapper do produto):
  python3 scripts/atualizar_kit.py --target=/path/produto --check-only
  python3 scripts/atualizar_kit.py --target=/path/produto --profile=full-skeleton --yes
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = False,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=check,
        text=True,
        capture_output=capture,
    )


def git_ok(repo: Path) -> bool:
    return (repo / ".git").exists() or run(["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"]).returncode == 0


def git_out(repo: Path, *args: str) -> str:
    p = run(["git", "-C", str(repo), *args])
    if p.returncode != 0:
        return ""
    return (p.stdout or "").strip()


def resolve_target(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    env = os.environ.get("ATUALIZAR_KIT_TARGET")
    if env:
        return Path(env).expanduser().resolve()
    # cwd se for git repo
    cwd = Path.cwd().resolve()
    if git_ok(cwd):
        top = git_out(cwd, "rev-parse", "--show-toplevel")
        return Path(top).resolve() if top else cwd
    return cwd


def read_kit_path_from_yaml(target: Path) -> Path | None:
    cfg = target / ".glpi" / "kit.yaml"
    if not cfg.is_file():
        return None
    for line in cfg.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("path:"):
            val = s.split(":", 1)[1].strip().strip("\"'")
            if val:
                return Path(val).expanduser().resolve()
    return None


def resolve_kit(explicit: str | None, target: Path, script_file: Path) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())
    for key in ("TOOLKIT_KIT", "TOOLKIT_ROOT", "PMF_DEV_KIT", "PMF_KIT_ROOT"):
        if os.environ.get(key):
            candidates.append(Path(os.environ[key]).expanduser().resolve())
    yaml_path = read_kit_path_from_yaml(target)
    if yaml_path:
        candidates.append(yaml_path)
    # script vive em <kit>/scripts/atualizar_kit.py
    kit_from_script = script_file.resolve().parent.parent
    if (kit_from_script / "scripts" / "upgrade-into.sh").is_file():
        candidates.append(kit_from_script)
    candidates.append((target / ".." / "toolkit-agentes-skills").resolve())
    candidates.append((Path.home() / "projetos" / "toolkit-agentes-skills").resolve())
    # fallback legado: instalacoes antigas do pmf-dev-kit
    candidates.append((target / ".." / "pmf-dev-kit").resolve())
    candidates.append((Path.home() / "projetos" / "pmf-dev-kit").resolve())

    seen: set[Path] = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if (c / "scripts" / "upgrade-into.sh").is_file() and (c / "tools" / "glpi").is_dir():
            return c
    return None


def infer_profile(target: Path, override: str | None) -> str:
    if override:
        return override
    if (target / "docs" / "00_visao_geral").is_dir():
        return "full-skeleton"
    if (target / "docs" / "05_progresso").is_dir() or (target / ".github" / "skills" / "atualizar").is_dir():
        return "pmf-core"
    return "pmf-core"


def ensure_product_wrapper(kit: Path, target: Path) -> Path:
    """Instala wrapper fino no produto apontando para o kit."""
    scripts = target / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    wrapper = scripts / "atualizar-kit"
    body = f"""#!/usr/bin/env bash
# Wrapper local — delega ao toolkit-agentes-skills (nao editar logica aqui).
set -euo pipefail
KIT="{kit}"
TARGET="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"
exec python3 "$KIT/scripts/atualizar_kit.py" --kit="$KIT" --target="$TARGET" "$@"
"""
    old = wrapper.read_text(encoding="utf-8") if wrapper.is_file() else ""
    if old != body:
        wrapper.write_text(body, encoding="utf-8")
        wrapper.chmod(wrapper.stat().st_mode | 0o111)
    # registrar path do kit
    glpi = target / ".glpi"
    glpi.mkdir(parents=True, exist_ok=True)
    kit_yaml = glpi / "kit.yaml"
    desired = f"# Caminho do repositorio fonte toolkit-agentes-skills (sync via scripts/atualizar-kit)\npath: {kit}\n"
    if not kit_yaml.is_file() or "path:" not in kit_yaml.read_text(encoding="utf-8", errors="replace"):
        kit_yaml.write_text(desired, encoding="utf-8")
    return wrapper


def _fetch_remotes(repo: Path, remotes: list[str]) -> tuple[bool, list[str]]:
    """Fetch listed remotes. Returns (all_ok, messages)."""
    msgs: list[str] = []
    all_ok = True
    for remote in remotes:
        if not git_out(repo, "remote", "get-url", remote):
            continue
        fp = run(["git", "-C", str(repo), "fetch", "--quiet", remote])
        if fp.returncode != 0:
            all_ok = False
            err = (fp.stderr or fp.stdout or "").strip()[:200]
            msgs.append(f"fetch {remote} falhou: {err}")
        else:
            msgs.append(f"fetch {remote} ok")
    return all_ok, msgs


def _branch_vs_ref(repo: Path, ref: str) -> tuple[int, int, list[str]]:
    """Return (behind, ahead, remote_commit_lines) for HEAD vs ref."""
    if not git_out(repo, "rev-parse", "--verify", ref):
        return 0, 0, []
    behind = int(git_out(repo, "rev-list", "--count", f"HEAD..{ref}") or "0")
    ahead = int(git_out(repo, "rev-list", "--count", f"{ref}..HEAD") or "0")
    commits: list[str] = []
    if behind > 0:
        log = git_out(repo, "log", "--oneline", f"HEAD..{ref}")
        commits = [ln for ln in log.splitlines() if ln][:15]
    return behind, ahead, commits


def check_repo_branch(repo: Path, label: str, do_fetch: bool) -> dict:
    """Diagnostico de branch do kit ou do produto destino.

    Antes de transferir o template, o destino NAO pode estar atras do remoto
    de tracking (e, se existir, de github/gitness). Kit atras de origin tambem
    bloqueia apply (atualize o kit primeiro ou use --pull-kit).
    """
    info: dict = {
        "repo": str(repo),
        "label": label,
        "branch": git_out(repo, "branch", "--show-current") or "?",
        "head": git_out(repo, "rev-parse", "--short", "HEAD") or "?",
        "dirty": bool(git_out(repo, "status", "--porcelain")),
        "fetched": False,
        "behind": 0,
        "ahead": 0,
        "behind_extra": {},  # remote/branch -> behind count
        "remote_commits": [],
        "has_updates": False,
        "block_reason": "",
        "messages": [],
    }
    if not git_ok(repo):
        info["messages"].append(f"{label}: nao e repositorio git; sync local mesmo assim e possivel")
        return info

    remotes = ["origin"]
    for extra in ("github", "gitness"):
        if git_out(repo, "remote", "get-url", extra):
            remotes.append(extra)

    if do_fetch:
        ok, fmsgs = _fetch_remotes(repo, remotes)
        info["fetched"] = ok
        info["messages"].extend(fmsgs)

    upstream = git_out(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    branch = info["branch"]

    # Tracking principal (@{u} ou origin/<branch>)
    primary_ref = upstream or (f"origin/{branch}" if branch and branch != "?" else "")
    if primary_ref:
        behind, ahead, commits = _branch_vs_ref(repo, primary_ref)
        info["behind"] = behind
        info["ahead"] = ahead
        info["remote_commits"] = commits
        if behind > 0:
            info["has_updates"] = True
            info["block_reason"] = (
                f"{label} branch '{branch}' esta {behind} commit(s) atras de {primary_ref}. "
                f"Atualize antes do upgrade: git pull --ff-only (ou skill sincronize)."
            )
            info["messages"].append(info["block_reason"])
        elif ahead > 0:
            info["messages"].append(
                f"{label} esta {ahead} commit(s) a frente de {primary_ref} (local)"
            )
        else:
            info["messages"].append(f"{label} em sync com {primary_ref}")
    else:
        info["messages"].append(f"{label} sem upstream; usando working tree local")

    # Espelhos adicionais (github / gitness) — so reportam; bloqueiam se atrasados
    for remote in remotes:
        if remote == "origin" and primary_ref.startswith("origin/"):
            continue
        ref = f"{remote}/{branch}" if branch and branch != "?" else ""
        if not ref or ref == primary_ref:
            continue
        if not git_out(repo, "rev-parse", "--verify", ref):
            info["messages"].append(f"{label}: ref {ref} ausente apos fetch (ok se remoto novo)")
            continue
        b, a, _ = _branch_vs_ref(repo, ref)
        info["behind_extra"][ref] = b
        if b > 0:
            msg = (
                f"{label} branch '{branch}' esta {b} commit(s) atras de {ref}. "
                f"Equalize com skill sincronize antes do upgrade."
            )
            info["messages"].append(msg)
            if not info["block_reason"]:
                info["block_reason"] = msg
                info["has_updates"] = True
                info["behind"] = max(info["behind"], b)
        elif a > 0:
            info["messages"].append(f"{label} esta {a} commit(s) a frente de {ref}")

    if info["dirty"]:
        info["messages"].append(
            f"{label}: working tree suja — upgrade segue, mas revise git status depois"
        )

    return info


def check_kit_updates(kit: Path, do_fetch: bool) -> dict:
    return check_repo_branch(kit, "kit", do_fetch)


def check_target_updates(target: Path, do_fetch: bool) -> dict:
    return check_repo_branch(target, "destino", do_fetch)


def pull_kit(kit: Path) -> tuple[bool, str]:
    if git_out(kit, "status", "--porcelain"):
        return False, "working tree do kit suja; faca commit/stash antes do pull"
    p = run(["git", "-C", str(kit), "pull", "--ff-only"])
    if p.returncode != 0:
        err = (p.stderr or p.stdout or "pull falhou").strip()
        return False, err[:400]
    return True, (p.stdout or "ok").strip()


def run_upgrade(kit: Path, target: Path, profile: str) -> int:
    """Aplica upgrade-into.sh e, no perfil full-skeleton, garante instalar_docs.

    upgrade-into.sh nao aceita --profile (isso e do bootstrap). Usa --target/--apply/--yes.
    O perfil so influencia se rodamos instalar_docs de novo apos o upgrade
    (full-skeleton / pmf-core: sim; glpi-only: nao — o proprio upgrade ja chama
    instalar_docs no fim quando --apply).
    """
    script = kit / "scripts" / "upgrade-into.sh"
    if not script.is_file():
        print(f"erro: nao encontrado {script}", file=sys.stderr)
        return 1
    cmd = [str(script), f"--target={target}", "--apply", "--yes"]
    print(f"→ {' '.join(cmd)}  (perfil inferido/flag: {profile})", file=sys.stderr)
    p = run(cmd, capture=False)
    return p.returncode


def target_status(target: Path) -> dict:
    return {
        "target": str(target),
        "branch": git_out(target, "branch", "--show-current") if git_ok(target) else None,
        "porcelain_count": len(git_out(target, "status", "--porcelain").splitlines())
        if git_ok(target)
        else 0,
        "status_sb": git_out(target, "status", "-sb") if git_ok(target) else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Verifica updates no toolkit-agentes-skills e sincroniza no repositorio produto."
    )
    ap.add_argument("--target", default="", help="Raiz do produto (default: git toplevel / cwd)")
    ap.add_argument("--kit", default="", help="Raiz do toolkit-agentes-skills")
    ap.add_argument(
        "--profile",
        default="",
        help="glpi-only|pmf-core|full-skeleton (default: inferido)",
    )
    ap.add_argument("--check-only", action="store_true", help="So verifica; nao sincroniza")
    ap.add_argument("--pull-kit", action="store_true", help="git pull --ff-only no kit antes do sync")
    ap.add_argument("--no-fetch", action="store_true", help="Nao executa git fetch no kit/destino")
    ap.add_argument(
        "--allow-behind",
        action="store_true",
        help="Permite apply mesmo com kit ou destino atras do remoto (perigoso)",
    )
    ap.add_argument("--yes", "-y", action="store_true", help="Aplica sync sem perguntar")
    ap.add_argument("--json", action="store_true", help="Saida JSON")
    args = ap.parse_args()

    script_file = Path(__file__).resolve()
    target = resolve_target(args.target or None)
    kit = resolve_kit(args.kit or None, target, script_file)
    if kit is None:
        print(
            "erro: toolkit-agentes-skills nao encontrado. Use --kit=PATH ou export TOOLKIT_KIT=...",
            file=sys.stderr,
        )
        return 1

    if target.resolve() == kit.resolve():
        msg = {
            "ok": False,
            "error": "TARGET e o proprio kit; nada a sincronizar para si mesmo",
            "kit": str(kit),
            "target": str(target),
        }
        print(json.dumps(msg, ensure_ascii=False) if args.json else msg["error"], file=sys.stderr)
        return 2

    profile = infer_profile(target, args.profile or None)
    do_fetch = not args.no_fetch
    check = check_kit_updates(kit, do_fetch=do_fetch)
    target_check = check_target_updates(target, do_fetch=do_fetch)

    report = {
        "ok": True,
        "mode": "check-only" if args.check_only else "sync",
        "profile": profile,
        "kit": check,
        "target_branch": target_check,
        "target": target_status(target),
        "actions": [],
    }

    def _print_branch_report() -> None:
        print(f"Kit:     {kit}")
        print(f"Target:  {target}")
        print(f"Perfil:  {profile} (inferido/flag)")
        print(f"Kit branch:     {check['branch']} @ {check['head']}  behind={check['behind']} ahead={check['ahead']} dirty={check['dirty']}")
        print(
            f"Destino branch: {target_check['branch']} @ {target_check['head']}  "
            f"behind={target_check['behind']} ahead={target_check['ahead']} dirty={target_check['dirty']}"
        )
        for m in check["messages"] + target_check["messages"]:
            print(f"- {m}")
        if check["remote_commits"]:
            print("Commits remotos pendentes no kit:")
            for c in check["remote_commits"]:
                print(f"  {c}")
        if target_check["remote_commits"]:
            print("Commits remotos pendentes no destino:")
            for c in target_check["remote_commits"]:
                print(f"  {c}")

    if args.check_only:
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            _print_branch_report()
            print("\nCheck-only: nenhuma escrita no produto.")
            print(f"Para sincronizar: {script_file} --target={target} --profile={profile} --yes")
        return 0

    # Gate: kit e destino precisam estar atualizados vs remotos antes da transferencia
    blockers: list[str] = []
    if check.get("block_reason"):
        blockers.append(str(check["block_reason"]))
    if target_check.get("block_reason"):
        blockers.append(str(target_check["block_reason"]))

    if blockers and not args.allow_behind:
        # --pull-kit pode resolver so o kit
        if args.pull_kit and check.get("block_reason") and not target_check.get("block_reason"):
            ok, msg = pull_kit(kit)
            report["actions"].append({"pull_kit": ok, "detail": msg})
            if not ok:
                print(f"erro pull kit: {msg}", file=sys.stderr)
                return 1
            check = check_kit_updates(kit, do_fetch=False)
            report["kit"] = check
            blockers = ([str(check["block_reason"])] if check.get("block_reason") else []) + (
                [str(target_check["block_reason"])] if target_check.get("block_reason") else []
            )
        if blockers:
            print("erro: branch desatualizada — recusando transferencia do template.", file=sys.stderr)
            for b in blockers:
                print(f"  - {b}", file=sys.stderr)
            print(
                "Atualize kit e destino (git pull --ff-only / skill sincronize) "
                "ou use --allow-behind (nao recomendado).",
                file=sys.stderr,
            )
            report["ok"] = False
            report["blockers"] = blockers
            if args.json:
                print(json.dumps(report, ensure_ascii=False, indent=2))
            return 3

    if not args.yes and sys.stdin.isatty():
        print(f"Kit={kit} → Target={target} perfil={profile}", file=sys.stderr)
        for m in check["messages"] + target_check["messages"]:
            print(f"  {m}", file=sys.stderr)
        ans = input("Aplicar upgrade-into no produto? [y/N] ").strip().lower()
        if ans not in ("y", "yes", "s", "sim"):
            print("Cancelado.", file=sys.stderr)
            return 0
    elif not args.yes:
        print("erro: use --yes em modo nao interativo", file=sys.stderr)
        return 1

    if args.pull_kit and not any(a.get("pull_kit") for a in report["actions"] if isinstance(a, dict)):
        ok, msg = pull_kit(kit)
        report["actions"].append({"pull_kit": ok, "detail": msg})
        if not ok:
            print(f"erro pull kit: {msg}", file=sys.stderr)
            return 1
        check = check_kit_updates(kit, do_fetch=False)
        report["kit"] = check

    ensure_product_wrapper(kit, target)
    report["actions"].append({"wrapper": str(target / "scripts" / "atualizar-kit")})

    rc = run_upgrade(kit, target, profile)
    report["upgrade_exit"] = rc
    report["target"] = target_status(target)
    report["target_branch"] = check_target_updates(target, do_fetch=False)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"ok": rc == 0, "profile": profile, "upgrade_exit": rc}, ensure_ascii=False))
        st = report["target"].get("status_sb") or ""
        if st:
            print(st, file=sys.stderr)
        print(
            "Sync concluido. Revise git status no produto; commit sob demanda (skill exporte/commit).",
            file=sys.stderr,
        )
    return 0 if rc == 0 else rc


if __name__ == "__main__":
    raise SystemExit(main())
