import argparse
import hashlib
import json
import os
import platform
import tarfile
from datetime import datetime
from pathlib import Path


ENV_BACKUP_DESTINO_WINDOWS = "BACKUP_DESTINO_WINDOWS"
ENV_BACKUP_DESTINO_LINUX = "BACKUP_DESTINO_LINUX"
ENV_BACKUP_DESTINO_DARWIN = "BACKUP_DESTINO_DARWIN"
ENV_BACKUP_DESTINO_FALLBACK_WINDOWS = "BACKUP_DESTINO_FALLBACK_WINDOWS"
ENV_BACKUP_DESTINO_FALLBACK_LINUX = "BACKUP_DESTINO_FALLBACK_LINUX"
ENV_BACKUP_DESTINO_FALLBACK_DARWIN = "BACKUP_DESTINO_FALLBACK_DARWIN"


def current_commit(repo: Path) -> str:
    import subprocess

    proc = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return "sem-commit"
    return proc.stdout.strip() or "sem-commit"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


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
        # Silencioso: o script continua com variaveis do ambiente atual.
        return


def resolve_destino(repo_root: Path, config: dict, destino_arg: str | None) -> tuple[Path, str]:
    if destino_arg:
        return Path(destino_arg).resolve(), "argumento --destino"

    system = platform.system().lower()
    backup_cfg = config.get("backup", {})
    destino_cfg = backup_cfg.get("destino_padrao", {})
    fallback_cfg = backup_cfg.get("fallback_por_so", {})

    if "windows" in system:
        destino_env = os.environ.get(ENV_BACKUP_DESTINO_WINDOWS)
        fallback_env = os.environ.get(ENV_BACKUP_DESTINO_FALLBACK_WINDOWS)
        destino_sugerido = destino_env or destino_cfg.get("windows")
        fallback_sugerido = fallback_env or fallback_cfg.get("windows")
        origem_primaria = f"env {ENV_BACKUP_DESTINO_WINDOWS}" if destino_env else "config destino_padrao.windows"
        origem_fallback = (
            f"env {ENV_BACKUP_DESTINO_FALLBACK_WINDOWS}"
            if fallback_env
            else "config fallback_por_so.windows"
        )
    elif "linux" in system:
        destino_env = os.environ.get(ENV_BACKUP_DESTINO_LINUX)
        fallback_env = os.environ.get(ENV_BACKUP_DESTINO_FALLBACK_LINUX)
        destino_sugerido = destino_env or destino_cfg.get("linux")
        fallback_sugerido = fallback_env or fallback_cfg.get("linux")
        origem_primaria = f"env {ENV_BACKUP_DESTINO_LINUX}" if destino_env else "config destino_padrao.linux"
        origem_fallback = (
            f"env {ENV_BACKUP_DESTINO_FALLBACK_LINUX}"
            if fallback_env
            else "config fallback_por_so.linux"
        )
    elif "darwin" in system:
        destino_env = os.environ.get(ENV_BACKUP_DESTINO_DARWIN)
        fallback_env = os.environ.get(ENV_BACKUP_DESTINO_FALLBACK_DARWIN)
        destino_sugerido = destino_env or destino_cfg.get("darwin")
        fallback_sugerido = fallback_env or fallback_cfg.get("darwin")
        origem_primaria = f"env {ENV_BACKUP_DESTINO_DARWIN}" if destino_env else "config destino_padrao.darwin"
        origem_fallback = (
            f"env {ENV_BACKUP_DESTINO_FALLBACK_DARWIN}"
            if fallback_env
            else "config fallback_por_so.darwin"
        )
    else:
        destino_sugerido = None
        fallback_sugerido = None
        origem_primaria = "indefinido"
        origem_fallback = "indefinido"

    if destino_sugerido:
        destino = Path(destino_sugerido)
        if destino.exists():
            return destino.resolve(), origem_primaria

    if fallback_sugerido:
        fallback = Path(fallback_sugerido)
        ensure_dir(fallback)
        return fallback.resolve(), origem_fallback

    fallback_rel = backup_cfg.get("fallback_relativo_repo", "_backups_local")
    return (repo_root / fallback_rel).resolve(), "fallback local"


def formato_nome_backup(config: dict, projeto: str, commit: str, stamp: str, extensao: str) -> str:
    template = config.get("backup", {}).get(
        "formato_nome_arquivo", "{projeto}_{commit}_{timestamp}{extensao}"
    )
    return template.format(
        projeto=projeto,
        commit=commit,
        timestamp=stamp,
        extensao=extensao,
    )


def criar_tar_gz(repo: Path, archive: Path, projeto: str) -> None:
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(repo, arcname=projeto)


def gerar_sha256(arquivo: Path) -> str:
    h = hashlib.sha256()
    with arquivo.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def escrever_sha256_sidecar(archive: Path, digest: str) -> Path:
    sidecar = Path(str(archive) + ".SHA256")
    sidecar.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return sidecar


def main() -> None:
    parser = argparse.ArgumentParser(description="Backup do projeto com tar.gz e SHA256")
    parser.add_argument("--repo", default=".", help="Caminho do repositorio")
    parser.add_argument("--destino", help="Diretorio base de backup (opcional)")
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

    destino_base, origem_destino = resolve_destino(repo_root, config, args.destino)
    projeto = repo.name
    commit = current_commit(repo)
    stamp = datetime.now().strftime("%d-%m-%y_%H-%M")

    out_dir = destino_base / projeto
    ensure_dir(out_dir)

    nome = formato_nome_backup(config, projeto, commit, stamp, ".tar.gz")
    archive = out_dir / nome
    criar_tar_gz(repo, archive, projeto)
    digest = gerar_sha256(archive)
    sidecar = escrever_sha256_sidecar(archive, digest)

    print(f"Destino de backup ({origem_destino}): {destino_base}")
    print(f"Backup gerado: {archive}")
    print(f"SHA256 gerado: {sidecar}")


if __name__ == "__main__":
    main()
