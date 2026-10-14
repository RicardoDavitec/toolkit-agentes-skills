import argparse
import json
import os
from datetime import datetime
from pathlib import Path


ENV_SESSAO_HISTORICO_RELATIVO_REPO = "SESSAO_HISTORICO_RELATIVO_REPO"
ENV_SESSAO_FORMATO_NOME_ARQUIVO = "SESSAO_FORMATO_NOME_ARQUIVO"
ENV_SESSAO_TITULO_PADRAO = "SESSAO_TITULO_PADRAO"


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


def default_saida(repo_root: Path, config: dict) -> Path:
    sessao_cfg = config.get("sessao", {})
    pasta_rel = os.environ.get(ENV_SESSAO_HISTORICO_RELATIVO_REPO) or sessao_cfg.get(
        "historico_relativo_repo", "docs/06_progresso/historico"
    )
    formato = os.environ.get(ENV_SESSAO_FORMATO_NOME_ARQUIVO) or sessao_cfg.get(
        "formato_nome_arquivo", "sessao_{data}.md"
    )
    nome = formato.format(data=datetime.now().strftime("%Y-%m-%d"))
    return (repo_root / pasta_rel / nome).resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera bloco padrao de resumo de sessao")
    parser.add_argument("--repo", default=".", help="Caminho do repositorio")
    parser.add_argument("--saida", help="Arquivo markdown de destino (opcional)")
    parser.add_argument("--titulo", help="Titulo do bloco")
    parser.add_argument(
        "--config",
        default=".github/skills/config/endpoints_operacionais.json",
        help="Arquivo de configuracao de endpoints operacionais",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo))
    load_env_file(repo_root)
    config = load_config(repo_root, args.config)

    saida = Path(args.saida).resolve() if args.saida else default_saida(repo_root, config)
    titulo = (
        args.titulo
        or os.environ.get(ENV_SESSAO_TITULO_PADRAO)
        or config.get("sessao", {}).get("titulo_padrao", "Resumo da Sessao")
    )

    saida.parent.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bloco = f"""
## {titulo}

- Data/Hora: {ts}
- O que foi feito:
- Decisoes tomadas:
- Tentativas e erros:
- Correcao aplicada:
- Pendencias futuras:
- Riscos residuais:
""".strip() + "\n"

    if saida.exists():
        conteudo = saida.read_text(encoding="utf-8")
        saida.write_text(conteudo.rstrip() + "\n\n" + bloco, encoding="utf-8")
    else:
        saida.write_text("# Diario Tecnico\n\n" + bloco, encoding="utf-8")

    print(f"Resumo de sessao atualizado em: {saida}")


if __name__ == "__main__":
    main()
