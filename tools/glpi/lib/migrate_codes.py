#!/usr/bin/env python3
"""Migracao de codes v1 (S/P, PF/CO/SL/RF) para v2 (F/S/P).

Dry-run gera mapa revisavel. --apply reescreve markdown (nunca apaga).
Migracao reversa (F -> legado) e recusada. Scope padrao: docs.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple

REPO = Path(__file__).resolve().parents[3]
PLANOS = REPO / "docs" / "05_progresso" / "planos_ativos"
RETRO = REPO / "docs" / "06_glpi" / "retro-scans"
BACKUP_ROOT = REPO / ".glpi" / ".backups"

# Codes v1: S0, S0.P1, PF7.P2, CO3, SL4.P1, RF1.P3
V1_RE = re.compile(
    r"(?<![A-Z0-9.])((?:PF|CO|SL|RF)\d+(?:\.P\d+)?|S\d+(?:\.P\d+)?)(?![A-Z0-9.])"
)
# Ja migrado / v2
V2_RE = re.compile(r"^F\d+(?:\.S\d+(?:\.P\d+)?)?$")


@dataclass
class PlanRule:
    """Regra por arquivo de plano (match no stem)."""

    match: str
    # (kind, n) -> (phase, session)  kind in S|PF|CO|SL|RF
    mapper: Callable[[str, int], Tuple[str, int]]
    rationale: str
    confidence: float = 0.9


def _map_shift(phase: str, base: int) -> Callable[[str, int], Tuple[str, int]]:
    def _m(_kind: str, n: int) -> Tuple[str, int]:
        return phase, base + n

    return _m


def _auditoria(kind: str, n: int) -> Tuple[str, int]:
    # S5 manuais/docs -> F1; restante implementacao F2. S0->S1 (shift+1)
    if kind == "S" and n == 5:
        return "F1", 1
    return "F2", n + 1


def _pwa(kind: str, n: int) -> Tuple[str, int]:
    # S0 contrato -> F1.S2; S1-S4 impl -> F2.S101..; S5 homolog -> F4.S1
    if kind != "S":
        return "F2", 100 + n
    if n == 0:
        return "F1", 2
    if n == 5:
        return "F4", 1
    return "F2", 100 + n


def _oem(kind: str, n: int) -> Tuple[str, int]:
    return "F2", 120 + n


def _demo_essencial(kind: str, n: int) -> Tuple[str, int]:
    return "F4", 10 + n


def _demo_estendida(kind: str, n: int) -> Tuple[str, int]:
    return "F4", 20 + n


def _rf(kind: str, n: int) -> Tuple[str, int]:
    return "F2", 30 + n


def _co(kind: str, n: int) -> Tuple[str, int]:
    return "F2", 40 + n


def _sl(kind: str, n: int) -> Tuple[str, int]:
    return "F2", 50 + n


def _pf(kind: str, n: int) -> Tuple[str, int]:
    return "F2", 60 + n


RULES: List[PlanRule] = [
    PlanRule("auditoria_corretiva", _auditoria, "Linha 1 Auditoria: S5->F1; demais F2 shift+1", 0.95),
    PlanRule("pwa_paliativo", _pwa, "Linha 9 PWA: S0=F1.S2; S1-4=F2.S101+; S5=F4.S1", 0.95),
    PlanRule("protecao_oem", _oem, "Linha 6 OEM -> F2.S120+", 0.9),
    PlanRule("demonstracao_panico_essencial", _demo_essencial, "Linha 7 demo essencial -> F4.S10+", 0.9),
    PlanRule("demonstracao_panico_basico_estendida", _demo_estendida, "Linha 8 demo estendida -> F4.S20+", 0.9),
    PlanRule("refinamento_cadastro", _rf, "Linha 2 RF -> F2.S30+", 0.95),
    PlanRule("contingencia_operadores", _co, "Linha 3 CO -> F2.S40+", 0.95),
    PlanRule("sala_mensagens", _sl, "Linha 4 SL -> F2.S50+", 0.95),
    PlanRule("correcao_perfis", _pf, "Linha 5 PF -> F2.S60+", 0.95),
]


@dataclass
class Occurrence:
    file: str
    line: int
    snippet: str


@dataclass
class Entry:
    from_code: str
    to: str
    confidence: float
    source: str
    rationale: str
    file_scope: str
    occurrences: List[Occurrence] = field(default_factory=list)
    action_required: Optional[str] = None

    def as_dict(self) -> dict:
        d = {
            "from": self.from_code,
            "to": self.to,
            "confidence": self.confidence,
            "source": self.source,
            "rationale": self.rationale,
            "file_scope": self.file_scope,
            "occurrences": [
                {"file": o.file, "line": o.line, "snippet": o.snippet[:120]}
                for o in self.occurrences
            ],
        }
        if self.action_required:
            d["action_required"] = self.action_required
        return d


def parse_v1(code: str) -> Optional[Tuple[str, int, Optional[int]]]:
    m = re.fullmatch(r"(PF|CO|SL|RF|S)(\d+)(?:\.P(\d+))?", code)
    if not m:
        return None
    kind, n, p = m.group(1), int(m.group(2)), m.group(3)
    return kind, n, int(p) if p is not None else None


def to_v2(phase: str, session: int, p: Optional[int]) -> str:
    if p is None:
        return f"{phase}.S{session}"
    return f"{phase}.S{session}.P{p}"


def rule_for(path: Path) -> Optional[PlanRule]:
    stem = path.stem
    name = path.name
    for rule in RULES:
        if rule.match in stem or rule.match in name:
            return rule
    # anexos: CO1_*, PF0_*, S2_*, PWA_*, OEM_*, DP_*, RF3_*, SL1_*
    m = re.match(r"^(PF|CO|SL|RF|S|PWA|GAP_PWA|OEM|DP)\d*_", name)
    if m:
        pref = m.group(1)
        prefix_map = {
            "PWA": "pwa_paliativo",
            "GAP_PWA": "pwa_paliativo",
            "OEM": "protecao_oem",
            "DP": (
                "demonstracao_panico_basico_estendida"
                if "estendida" in name
                else "demonstracao_panico_essencial"
            ),
            "PF": "correcao_perfis",
            "CO": "contingencia_operadores",
            "SL": "sala_mensagens",
            "RF": "refinamento_cadastro",
            "S": "auditoria_corretiva",
        }
        match = prefix_map.get(pref)
        if match:
            for rule in RULES:
                if rule.match == match:
                    return rule
    return None


def collect_files(scope_docs: bool) -> List[Path]:
    files: List[Path] = []
    if scope_docs:
        if PLANOS.exists():
            for p in sorted(PLANOS.rglob("*.md")):
                if p.name == "README.md":
                    continue  # indice multi-linha: migrar depois / manual
                files.append(p)
    return files


def mapper_for_kind(kind: str) -> Callable[[str, int], Tuple[str, int]]:
    """Mapper canonico por familia de code (referencias cruzadas entre planos)."""
    return {
        "S": _auditoria,  # S solto fora de plano S-específico: fallback Auditoria
        "RF": _rf,
        "CO": _co,
        "SL": _sl,
        "PF": _pf,
    }.get(kind, _auditoria)


def propose_to(code: str, rule: PlanRule) -> Tuple[str, float, str]:
    parsed = parse_v1(code)
    if not parsed:
        return "?", 0.0, "code nao parseavel"
    kind, n, p = parsed
    # Prefixo do proprio plano (S em PWA/OEM/demo) usa a regra do arquivo;
    # PF/CO/SL/RF sempre pelo mapper da familia (evita colisao PF1/CO1 no mesmo arquivo).
    if kind in ("PF", "CO", "SL", "RF"):
        phase, session = mapper_for_kind(kind)(kind, n)
        rat = f"familia {kind} -> {phase}.S{session}"
        return to_v2(phase, session, p), 0.95, rat
    phase, session = rule.mapper(kind, n)
    return to_v2(phase, session, p), rule.confidence, rule.rationale


def scan(files: Iterable[Path], min_confidence: float) -> Tuple[List[Entry], int]:
    # key = (file_scope, from_code)
    bucket: Dict[Tuple[str, str], Entry] = {}
    unresolved = 0
    for path in files:
        rel = str(path.relative_to(REPO))
        rule = rule_for(path)
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            for m in V1_RE.finditer(line):
                code = m.group(1)
                if V2_RE.match(code):
                    continue
                if rule is None:
                    to, conf, rat = "?", 0.0, f"sem regra para {path.name}"
                    source = "unknown"
                else:
                    to, conf, rat = propose_to(code, rule)
                    source = "plan_rule"
                if conf < min_confidence:
                    to = "?"
                key = (rel, code)
                if key not in bucket:
                    entry = Entry(
                        from_code=code,
                        to=to,
                        confidence=conf if to != "?" else 0.0,
                        source=source,
                        rationale=rat,
                        file_scope=rel,
                    )
                    if to == "?":
                        entry.action_required = "definir a fase manualmente antes de --apply"
                        unresolved += 1
                    bucket[key] = entry
                else:
                    # atualiza to se ainda ?
                    pass
                bucket[key].occurrences.append(
                    Occurrence(file=rel, line=i, snippet=line.strip())
                )
    return list(bucket.values()), unresolved


def write_map(entries: List[Entry], unresolved: int, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "schema_from": 1,
        "schema_to": 2,
        "reverse_policy": "forbid",
        "entries": [e.as_dict() for e in sorted(entries, key=lambda e: (e.file_scope, e.from_code))],
        "unresolved": unresolved,
        "blocking": unresolved > 0,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def load_map(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("reverse_policy") != "forbid":
        print("ERRO: reverse_policy invalida", file=sys.stderr)
        sys.exit(13)
    # recusa se algum 'to' for v1 e 'from' for v2
    for e in data.get("entries", []):
        if V2_RE.match(e.get("from", "")) and not V2_RE.match(e.get("to", "?")):
            print("ERRO: tentativa de migracao reversa", file=sys.stderr)
            sys.exit(13)
        if e.get("to") == "?":
            print(f"ERRO: entrada pendente {e.get('from')} em {e.get('file_scope')}", file=sys.stderr)
            sys.exit(10)
    return data


def replace_in_text(text: str, mapping: Dict[str, str], keep_alias: bool) -> Tuple[str, int]:
    """Substitui codes v1 por v2 (maior comprimento primeiro)."""
    if not mapping:
        return text, 0
    # ordenar por len desc
    items = sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True)
    count = 0

    def sub_code(m: re.Match) -> str:
        nonlocal count
        code = m.group(1)
        if code in mapping:
            count += 1
            return mapping[code]
        return code

    # **CODE** e code="CODE" e prosa com word boundary
    pattern = re.compile(
        r"(?<![A-Z0-9.])(" + "|".join(re.escape(k) for k, _ in items) + r")(?![A-Z0-9.])"
    )
    new_text = pattern.sub(sub_code, text)

    if keep_alias and count:
        # inserir alias uma vez por code migrado, apos primeiro comentario glpi: code=
        for old, new in items:
            marker = f'<!-- glpi-legacy: was="{old}" -->'
            if marker in new_text:
                continue
            needle = f'<!-- glpi: code="{new}"'
            if needle in new_text:
                new_text = new_text.replace(
                    needle, f"{marker}\n    {needle}", 1
                )
    return new_text, count


def product_keys() -> List[str]:
    """Aliases aceitos em --confirm (project.yaml key + nome da pasta do repo)."""
    keys = {REPO.name, "Bot_Pan"}
    py = REPO / ".glpi" / "project.yaml"
    if py.exists():
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(py.read_text(encoding="utf-8")) or {}
            if data.get("key"):
                keys.add(str(data["key"]))
            if data.get("product"):
                keys.add(str(data["product"]))
        except Exception:
            for line in py.read_text(encoding="utf-8").splitlines():
                if line.startswith("key:"):
                    keys.add(line.split(":", 1)[1].strip().strip("\"'"))
    return sorted(keys)


def apply_docs(data: dict, keep_alias: bool, product_confirm: str) -> int:
    expected = product_keys()
    if product_confirm not in expected:
        print(
            f"ABORT: confirmacao deve ser um de {expected!r} (recebido {product_confirm!r})",
            file=sys.stderr,
        )
        sys.exit(6)

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / f"migrate-{ts}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # agrupar por file_scope
    by_file: Dict[str, Dict[str, str]] = {}
    for e in data["entries"]:
        by_file.setdefault(e["file_scope"], {})[e["from"]] = e["to"]

    total = 0
    for rel, mapping in sorted(by_file.items()):
        path = REPO / rel
        if not path.exists():
            print(f"skip missing {rel}")
            continue
        # backup
        dest = backup_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        text = path.read_text(encoding="utf-8")
        new_text, n = replace_in_text(text, mapping, keep_alias=keep_alias)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"ok {rel}: {n} substituicoes")
            total += n
        else:
            print(f"skip {rel}: 0")

    # renomear anexos S*_ / prefixos legados quando o nome comeca com code v1
    anexos = PLANOS / "anexos"
    if anexos.exists():
        for path in sorted(anexos.iterdir()):
            if not path.is_file():
                continue
            # tentar mapear pelo conteudo do arquivo no mapa; senao pelo rule no nome
            rule = rule_for(path)
            m = re.match(r"^(S\d+|PF\d+|CO\d+|SL\d+|RF\d+)_(.+)$", path.name)
            if not m or rule is None:
                continue
            old_code = m.group(1)
            rest = m.group(2)
            to, conf, _ = propose_to(old_code, rule)
            if conf < 0.8 or to == "?":
                continue
            new_name = f"{to.replace('.', '_')}_{rest}"
            new_path = path.with_name(new_name)
            if new_path.exists():
                continue
            bdest = backup_dir / str(path.relative_to(REPO))
            bdest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, bdest)
            path.rename(new_path)
            print(f"rename {path.name} -> {new_name}")

    meta = backup_dir / "migrate-meta.json"
    meta.write_text(
        json.dumps({"ts": ts, "total": total, "map_entries": len(data["entries"])}, indent=2),
        encoding="utf-8",
    )
    print(f"backup: {backup_dir}")
    print(f"total substituicoes: {total}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Migrar codes GLPI v1 -> v2")
    ap.add_argument("--dry-run", action="store_true", help="Gera mapa; nao escreve docs")
    ap.add_argument("--apply", action="store_true", help="Aplica mapa")
    ap.add_argument("--from", dest="from_map", help="Mapa JSON revisado")
    ap.add_argument("--scope", choices=["docs", "glpi", "all"], default="docs")
    ap.add_argument("--min-confidence", type=float, default=0.8)
    ap.add_argument("--keep-alias", action="store_true", default=True)
    ap.add_argument("--no-keep-alias", action="store_false", dest="keep_alias")
    ap.add_argument("--confirm", default="", help="Confirmacao dupla (key do projeto / nome do repo)")
    ap.add_argument("--out", default="", help="Caminho do mapa dry-run")
    args = ap.parse_args(argv)

    if args.scope in ("glpi", "all") and args.apply:
        print("AVISO: --scope=glpi ainda nao implementado neste binario; use docs.", file=sys.stderr)
        if args.scope == "glpi":
            return 5

    if args.apply:
        if not args.from_map:
            print("ERRO: --apply exige --from=mapa.json", file=sys.stderr)
            return 2
        data = load_map(Path(args.from_map))
        if not args.confirm:
            print(f"ERRO: --apply exige --confirm=... (aceitos: {product_keys()})", file=sys.stderr)
            return 6
        return apply_docs(data, keep_alias=args.keep_alias, product_confirm=args.confirm)

    # dry-run (default)
    files = collect_files(scope_docs=True)
    entries, unresolved = scan(files, min_confidence=args.min_confidence)
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    out = Path(args.out) if args.out else RETRO / f"migrate-codes-{ts}.json"
    write_map(entries, unresolved, out)
    print(f"mapa: {out}")
    print(f"entries: {len(entries)} | unresolved: {unresolved} | blocking: {unresolved > 0}")
    # resumo por arquivo
    by = {}
    for e in entries:
        by.setdefault(e.file_scope, []).append(e)
    for f, es in sorted(by.items()):
        ok = sum(1 for e in es if e.to != "?")
        print(f"  {f}: {ok}/{len(es)} ok")
        for e in sorted(es, key=lambda x: x.from_code)[:8]:
            print(f"    {e.from_code} -> {e.to} ({e.confidence})")
        if len(es) > 8:
            print(f"    ... +{len(es)-8}")
    return 0 if unresolved == 0 else 10


if __name__ == "__main__":
    sys.exit(main())
