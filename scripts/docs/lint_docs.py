#!/usr/bin/env python3
"""lint_docs.py - valida os documentos de apoio em docs/ (padrao 12_padrao_documentacao).

Uso:
    python3 scripts/docs/lint_docs.py            # erros bloqueiam (exit 1)
    python3 scripts/docs/lint_docs.py --estrito  # documento sem front matter vira erro

Nao valida planos, anexos, SESSAO_*, pendencias, legados nem docs/06_glpi
(formatos proprios, cobertos pelas skills do kit).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs"

IGNORAR = (
    "12_padrao_documentacao/02_modelos",
    "06_glpi/",
    "05_progresso/planos_ativos",
    "05_progresso/legados",
    "05_progresso/pendencias",
    "05_progresso/historico",
    "07_doc_academica",
    "08_imagens",
    "node_modules",
)
SEM_REGISTRO_DE_ID = "12_padrao_documentacao/03_exemplos"

OBRIGATORIOS = ["id", "tipo", "titulo", "status", "versao", "data", "autor"]
STATUS = {"rascunho", "em_revisao", "aprovado", "obsoleto"}
CLASSIFICACOES = {"publico", "interno", "restrito", "pessoal"}

PREFIXOS = {
    "visao": "VIS", "requisito": "REQ", "regra_negocio": "RN", "glossario": "GLO",
    "arquitetura": "ARQ", "adr": "ADR", "teste": "TST", "homologacao": "HML",
    "operacao": "OPS", "dicionario_dados": "DIC", "inventario_lgpd": "LGP",
    "relatorio": "REL", "guia": "GUI",
}
TIPOS = set(PREFIXOS)

SECOES = {
    "visao": ["## Objetivo", "## Escopo", "## Partes interessadas"],
    "requisito": ["## Descrição", "## Critérios de aceite", "## Rastreabilidade"],
    "regra_negocio": ["## Enunciado", "## Fonte", "## Exceções"],
    "glossario": ["## Termos"],
    "arquitetura": ["## 5. Visão de blocos", "## 7. Visão de implantação",
                    "## 11. Riscos e dívida técnica"],
    "adr": ["## Contexto", "## Decisão", "## Alternativas consideradas", "## Consequências"],
    "teste": ["## Escopo", "## Estratégia", "## Casos de teste", "## Critérios de saída"],
    "homologacao": ["## Participantes", "## Cenários", "## Achados", "## Decisão"],
    "operacao": ["## Quando usar", "## Pré-requisitos", "## Passos", "## Verificação",
                 "## Reversão"],
    "dicionario_dados": ["## Finalidade", "## Colunas", "## Relacionamentos"],
    "inventario_lgpd": ["## Inventário", "## Pendências de decisão"],
    "relatorio": ["## Resumo", "## Resultado", "## Riscos residuais"],
}

RE_PASTA_RAIZ = re.compile(r"^\d{2}_[a-z0-9_]+$")
RE_PASTA = re.compile(r"^[a-z0-9_]+$")
RE_ARQUIVO = re.compile(r"^[a-z0-9_]+\.md$")
RE_ARQUIVO_GUIA = re.compile(r"^G\d{2}_[a-z0-9_]+\.md$")
RE_ID = re.compile(r"^[A-Z]{2,5}-[A-Za-z0-9._-]+$")
RE_CHAVE = re.compile(r"^([a-z_]+):\s*(.*)$")
RE_CODIGO = re.compile(r"^F[1-5](\.S\d+(\.P\d+)?)?$")
RE_PREFIXO_CR = re.compile(r"\bC\d+\.R\d+\b")


def ignorado(rel: str) -> bool:
    return any(i in rel for i in IGNORAR)


def ler_front_matter(texto: str) -> dict[str, str] | None:
    if not texto.startswith("---\n"):
        return None
    fim = texto.find("\n---", 4)
    if fim == -1:
        return None
    dados: dict[str, str] = {}
    for linha in texto[4:fim].splitlines():
        m = RE_CHAVE.match(linha)
        if m:
            valor = re.split(r"\s#", m.group(2))[0].strip().strip('"').strip("'")
            dados[m.group(1)] = valor
    return dados


def main() -> int:
    estrito = "--estrito" in sys.argv
    erros: list[str] = []
    avisos: list[str] = []
    ids: dict[str, str] = {}

    for pasta in sorted(p for p in DOCS.rglob("*") if p.is_dir()):
        rel = pasta.relative_to(DOCS).as_posix()
        if ignorado(rel + "/") or ignorado(rel):
            continue
        if "/" not in rel and not RE_PASTA_RAIZ.match(pasta.name):
            erros.append(f"{rel}: pasta de nivel 1 deve seguir NN_nome_snake_case")
        elif "/" in rel and not RE_PASTA.match(pasta.name):
            avisos.append(f"{rel}: use snake_case sem acento")

    for arq in sorted(DOCS.rglob("*.md")):
        rel = arq.relative_to(DOCS).as_posix()
        if ignorado(rel) or arq.name.lower() == "readme.md" or arq.name.startswith("SESSAO_"):
            continue

        texto = arq.read_text(encoding="utf-8")
        fm = ler_front_matter(texto)
        if fm is None:
            (erros if estrito else avisos).append(f"{rel}: sem front matter")
            continue

        nome_ok = RE_ARQUIVO.match(arq.name) or (
            fm.get("tipo") == "guia" and RE_ARQUIVO_GUIA.match(arq.name)
        )
        if not nome_ok:
            avisos.append(f"{rel}: nome de arquivo deve ser snake_case minusculo sem acento")

        for chave in OBRIGATORIOS:
            if not fm.get(chave):
                erros.append(f"{rel}: campo obrigatorio ausente '{chave}'")

        tipo = fm.get("tipo", "")
        doc_id = fm.get("id", "")
        if doc_id:
            if not RE_ID.match(doc_id):
                erros.append(f"{rel}: id invalido '{doc_id}'")
            elif SEM_REGISTRO_DE_ID not in rel:
                if doc_id in ids:
                    erros.append(f"{rel}: id duplicado (ja usado em {ids[doc_id]})")
                ids[doc_id] = rel
        if tipo and tipo not in TIPOS:
            erros.append(f"{rel}: tipo desconhecido '{tipo}'")
        elif tipo and doc_id and not doc_id.startswith(PREFIXOS[tipo] + "-"):
            erros.append(f"{rel}: id deve comecar com '{PREFIXOS[tipo]}-' para o tipo '{tipo}'")

        if fm.get("status") and fm["status"] not in STATUS:
            erros.append(f"{rel}: status invalido '{fm['status']}'")
        if fm.get("classificacao") and fm["classificacao"] not in CLASSIFICACOES:
            erros.append(f"{rel}: classificacao invalida '{fm['classificacao']}'")
        if not fm.get("classificacao"):
            avisos.append(f"{rel}: sem 'classificacao'")
        if fm.get("chamado") and not fm["chamado"].isdigit():
            erros.append(f"{rel}: 'chamado' deve ser so o numero")
        if fm.get("requisicao") and not fm["requisicao"].isdigit():
            erros.append(f"{rel}: 'requisicao' deve ser so o numero")
        if fm.get("codigo") and not RE_CODIGO.match(fm["codigo"]):
            erros.append(f"{rel}: 'codigo' fora do formato F#[.S#[.P#]]")

        for secao in SECOES.get(tipo, []):
            if secao not in texto:
                erros.append(f"{rel}: secao obrigatoria ausente '{secao}'")

        corpo = texto.split("\n---", 1)[-1]
        for n, linha in enumerate(corpo.splitlines(), 1):
            if not linha.lstrip().startswith(">") and RE_PREFIXO_CR.search(linha):
                avisos.append(f"{rel}: prefixo C#.R# fora do cabecalho (linha ~{n})")
                break

    for a in avisos:
        print(f"AVISO: {a}")
    for e in erros:
        print(f"ERRO : {e}")
    print(f"\nResumo: {len(erros)} erro(s), {len(avisos)} aviso(s).")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
