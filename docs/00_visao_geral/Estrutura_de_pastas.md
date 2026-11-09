docs/
├── 12_padrao_documentacao/
│   ├── README.md
│   ├── 01_guias/
│   │   ├── G01_visao_geral_do_padrao.md
│   │   ├── G02_identificacao_c_r_f_s_p.md
│   │   ├── G03_front_matter_e_nomenclatura.md
│   │   ├── G04_fase_f1_planejamento.md
│   │   ├── G05_fase_f2_implementacao.md
│   │   ├── G06_fase_f3_testes_internos.md
│   │   ├── G07_fase_f4_homologacao.md
│   │   ├── G08_fase_f5_producao.md
│   │   ├── G09_commits_prs_e_rastreabilidade.md
│   │   ├── G10_sincronizacao_glpi.md
│   │   ├── G11_dados_prisma_e_dicionario.md
│   │   ├── G12_lgpd_e_classificacao.md
│   │   ├── G13_diagramas_como_codigo.md
│   │   └── G14_cursor_extensoes_agentes_skills.md
│   ├── 02_modelos/
│   │   ├── MOD_requisito.md
│   │   ├── MOD_regra_negocio.md
│   │   ├── MOD_adr.md
│   │   ├── MOD_arquitetura_arc42.md
│   │   ├── MOD_plano_implementacao.md
│   │   ├── MOD_sessao.md
│   │   ├── MOD_pendencia.md
│   │   ├── MOD_plano_testes.md
│   │   ├── MOD_ata_homologacao.md
│   │   ├── MOD_runbook.md
│   │   ├── MOD_dicionario_dados.md
│   │   ├── MOD_glossario.md
│   │   └── MOD_relatorio_fase.md
│   └── 03_exemplos/
│       └── projeto_exemplo/          (projeto fictício "PRJ-EXEMPLO")
│           ├── ADR_C0001.R1.F1_banco_relacional.md
│           ├── SES_C0001.R1.F2.S1.md
│           └── DIC_C0001.R1_attendances.md
├── 00_visao_geral/ ... 11_ia/        (existentes, sem renomear)

.cursor/
├── rules/documentacao.mdc
├── agents/
│   ├── doc-orquestrador.md
│   ├── doc-arquiteto.md
│   ├── doc-escriba.md
│   ├── doc-revisor.md
│   ├── doc-dados-lgpd.md
│   └── doc-glpi-sync.md
└── skills/
    ├── doc-novo/SKILL.md
    ├── doc-lint/SKILL.md
    ├── doc-sessao-de-commits/SKILL.md
    ├── doc-adr/SKILL.md
    ├── doc-dicionario-prisma/SKILL.md
    ├── doc-rastreabilidade/SKILL.md
    ├── doc-gate-fase/SKILL.md
    ├── doc-glpi-sync/SKILL.md
    └── doc-publicar-portal/SKILL.md

scripts/docs/
├── novo_doc.py
├── lint_docs.py
├── gerar_rastreabilidade.py
├── sessao_de_commits.py
├── gerar_dados_prisma.sh
└── instalar_docs.sh

tools/docs/
├── mkdocs.yml
├── tbls.yml
└── README.md

.vscode/
├── extensions.json
└── settings.json

.github/
├── pull_request_template.md
└── workflows/docs.yml
