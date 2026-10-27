# Hierarquia plano ↔ GLPI (C / R / F / S / P)

Canônico do toolkit. Substitui o modelo legado `S`/`M.*` descrito em
`HIERARQUIA_S_P_GLPI.md`.

## Cabeçalho (não é item da árvore)

| Nível | Onde | GLPI |
|-------|------|------|
| **C** | só no cabeçalho do plano / JSON | Ticket ITIL (`tickets_id`) |
| **R** | só no cabeçalho | Project raiz + `Itil_Project` |

## Árvore gravável

```text
Project (R)
├── [F] F1 … F5                 Project filho ou ProjectTask n1
│     ├── [S] F2.S1             ProjectTask (sessão / semana)
│     │     ├── [P] F2.S1.P1    ProjectTask (~2h; átomos no content)
│     │     └── [P] F2.S1.P2
│     └── [S] F2.S2
└── …
```

| Nível | Código | Observação |
|-------|--------|------------|
| F | `F1`…`F5` | Fases GEP fixas |
| S | `F#.S#` | Janela temporal (default: semana ISO) |
| P | `F#.S#.P#` | Pacote ~2h; detalhe dos átomos no `content` |
| Átomo | — | Só `content` + `atoms_detail` no JSON do pack |

## `--pack`

1. Infere fase GEP (path/módulo/commit) → `F#`.
2. Agrupa por semana → `F#.S#`.
3. Empacota até `--pack-target-min` → `F#.S#.P#`.
4. `crfsp.ensure_fsp` completa S faltantes, datas e durações.

Não gerar `M.BACKEND`, `M.DOCS.PKG3` nem `S0` como código de apply.

## Datas (obrigatório em F, S e P)

Ver skill `glpi-retro-scan` (seção Datas e durações) e `tools/glpi/lib/crfsp.py`.
`real_*` só com evidência (plano/`glpi:`/commit). Pending sem evidência →
`temporal_source=stipulated` (bloco 2 h) e `effective_duration=0`.
