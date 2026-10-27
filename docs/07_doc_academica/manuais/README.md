# Manuais de usuário

Fonte única em Markdown. Saídas: HTML (leitura principal) e PDF A4/A5, geradas por
`scripts/build-manuais.sh`. Plano: `docs/05_progresso/planos_ativos/` (onda S5).

## Árvore (regenerada pelo build)

<!-- Exemplo de ARVORE:INICIO -->
docs/07_doc_academica/manuais/
├── README.md
├── ESTILO_MANUAIS.md
├── _modelo/
│   ├── manual.md
│   └── _fontes.md
├── _comum/
│   ├── cadastro-instalacao.md         v0.3.0
│   └── CHANGELOG.md
├── contato_de_seguranca/              (id: contato-de-confianca)
│   ├── guia_do_contato_de_confianca.md  v0.5.0-homologacao
│   ├── CHANGELOG.md
│   ├── _fontes.md
│   └── capturas/
├── titular-panico/                    (em elaboração)
├── titular-saude/                     (em elaboração)
├── cuidador/                          (em elaboração)
└── operador/                          (restrito: publico: false)
<!-- ARVORE:FIM -->

## Regras de versão

- Formato `MAIOR.MENOR.PATCH-estado`. MAIOR: o fluxo mudou. MENOR: seção ou passo novo. PATCH: correção
  de texto, link ou captura. Estado: `homologacao` ou `estavel`.
- Cada manual tem `CHANGELOG.md`. A primeira linha dele é igual a `versao_manual`.
- Mudança em `_comum/` sobe, no mínimo, o PATCH de todos os manuais que o incluem.
- Commit: `docs(manuais): <id> <versao> - <resumo> (S5.Pn)`. Tag na publicação: `manual-<id>-vX.Y.Z`.
- Operador: rodapé reduzido, sem caminho nem hash (documento restrito).
- Nenhuma publicação sem versão nova e entrada no CHANGELOG. `build-manuais.sh --check` falha se faltar.

## Fluxo de edição

Pedido (PO) → rascunho e versão proposta (Monica) → verificação no código e `_fontes.md` (Cursor) →
aprovação (PO) → gravação em commit pequeno (Cursor) → `--check` → publicação e tag (Cursor).
