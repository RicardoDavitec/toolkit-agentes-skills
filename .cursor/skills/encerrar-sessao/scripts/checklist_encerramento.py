import argparse
import json
import os
import platform
import subprocess
from pathlib import Path


ENV_BACKUP_DESTINO_WINDOWS = "BACKUP_DESTINO_WINDOWS"
ENV_BACKUP_DESTINO_LINUX = "BACKUP_DESTINO_LINUX"
ENV_BACKUP_DESTINO_DARWIN = "BACKUP_DESTINO_DARWIN"
ENV_BACKUP_DESTINO_FALLBACK_WINDOWS = "BACKUP_DESTINO_FALLBACK_WINDOWS"
ENV_BACKUP_DESTINO_FALLBACK_LINUX = "BACKUP_DESTINO_FALLBACK_LINUX"
ENV_BACKUP_DESTINO_FALLBACK_DARWIN = "BACKUP_DESTINO_FALLBACK_DARWIN"


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    while True:
        if (cur / ".git").exists():
            return cur
        if cur.parent == cur:
            return start.resolve()
        cur = cur.parent


def load_config(repo_root: Path, config_path: str) -> dict:
    path = Path(config_path)
    if not path.is_absolute():
        path = repo_root / path
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_env_file(repo_root: Path) -> None:
    env_path = repo_root / ".env"
    if not env_path.exists():
        return
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv(env_path, override=False)
    except Exception:
        return


def resolve_backup_destino(repo_root: Path, config: dict) -> Path:
    backup_cfg = config.get("backup", {})
    destinos = backup_cfg.get("destino_padrao", {})
    fallbacks = backup_cfg.get("fallback_por_so", {})
    system = platform.system().lower()
    if "windows" in system:
        destino = os.environ.get(ENV_BACKUP_DESTINO_WINDOWS) or destinos.get("windows")
        fallback = os.environ.get(ENV_BACKUP_DESTINO_FALLBACK_WINDOWS) or fallbacks.get("windows")
    elif "linux" in system:
        destino = os.environ.get(ENV_BACKUP_DESTINO_LINUX) or destinos.get("linux")
        fallback = os.environ.get(ENV_BACKUP_DESTINO_FALLBACK_LINUX) or fallbacks.get("linux")
    elif "darwin" in system:
        destino = os.environ.get(ENV_BACKUP_DESTINO_DARWIN) or destinos.get("darwin")
        fallback = os.environ.get(ENV_BACKUP_DESTINO_FALLBACK_DARWIN) or fallbacks.get("darwin")
    else:
        destino = None
        fallback = None

    if destino and Path(destino).exists():
        return Path(destino).resolve()

    if fallback:
        path_fallback = Path(fallback)
        path_fallback.mkdir(parents=True, exist_ok=True)
        return path_fallback.resolve()

    fallback_rel = backup_cfg.get("fallback_relativo_repo", "_backups_local")
    return (repo_root / fallback_rel).resolve()


def resolve_sessao_historico(repo_root: Path, config: dict) -> Path:
    sessao_cfg = config.get("sessao", {})
    pasta_rel = sessao_cfg.get("historico_relativo_repo", "docs/06_progresso/historico")
    return (repo_root / pasta_rel).resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Checklist de encerramento de sessao")
    parser.add_argument("--repo", default=".", help="Caminho do repositorio")
    parser.add_argument(
        "--config",
        default=".github/skills/config/endpoints_operacionais.json",
        help="Arquivo de configuracao de endpoints operacionais",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    repo_root = find_repo_root(repo)
    load_env_file(repo_root)
    config = load_config(repo_root, args.config)
    destino_backup = resolve_backup_destino(repo_root, config)
    historico_sessao = resolve_sessao_historico(repo_root, config)

    rc_status, out_status, _ = run(["git", "status", "--short"], repo)
    rc_branch, out_branch, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)

    print("Checklist de encerramento")
    print("- Branch:", out_branch if rc_branch == 0 else "nao identificado")
    if rc_status == 0 and out_status:
        print("- Alteracoes pendentes: sim")
        print(out_status)
    elif rc_status == 0:
        print("- Alteracoes pendentes: nao")
    else:
        print("- Nao foi possivel verificar status do git")

    print(f"- Endpoint historico de sessao: {historico_sessao}")
    print(f"- Endpoint destino de backup: {destino_backup}")
    print("- Proximo passo sugerido: rodar documentar-sessao e decidir commit/push")


if __name__ == "__main__":
    main()
