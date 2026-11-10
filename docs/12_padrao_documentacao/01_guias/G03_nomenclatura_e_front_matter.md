---
id: GUI-003
tipo: guia
titulo: Nomenclatura e front matter
status: rascunho
versao: 0.2.0
data: 2026-11-09
autor: Ricardo
classificacao: publico
---
# G03 – Nomenclatura e front matter

## 1. Regras de nome

### 1.1 Documentos de apoio

| Item | Regra | Exemplo |
|---|---|---|
| Pasta de nível 1 | `NN_nome` em snake_case, sem acento | `09_dados_e_tabelas` |
| Subpasta | snake_case, sem acento | `planos_ativos` |
| Documento numerado | `<prefixo>_<NNN>_<slug>.md`, minúsculo | `adr_001_banco_relacional.md` |
| Dicionário de dados | `dic_<tabela>.md` | `dic_atendimentos.md` |
| Guia do padrão | `G<NN>_<slug>.md` | `G04_fase_f1_planejamento.md` |

### 1.2 Nomes que já existem no kit (não renomear)

| Documento | Nome | Criado por |
|---|---|---|
| Plano | `<nome>-DD_MM_AA-hh_mm.md` em `planos_ativos/` | skill `documente-o-plano` |
| Anexo de plano | `F<n>_S<n>_<slug>-DD_MM_AA.md` em `planos_ativos/anexos/` | skill `documente-o-plano` |
| Registro diário | `SESSAO_AAAA-MM-DD_<DESCRICAO>.md` em `05_progresso/geral/` | skill `encerrar-sessao` |
| Pendência | arquivos em `05_progresso/pendencias/` | skill `inserir-pendencia` |

Atenção ao vocabulário: o **S** da hierarquia (sessão, semana ou sprint) é uma janela de tempo no plano. O **SESSAO_*** é o registro do dia, e um S pode ter vários desses registros.

## 2. Tipos de documento

| Tipo | Prefixo | Pasta destino | Observação |
|---|---|---|---|
| `visao` | `vis` | `00_visao_geral` | |
| `requisito` | `req` | `01_requisitos` | |
| `regra_negocio` | `rn` | `01_requisitos` | Nunca inventar |
| `glossario` | `glo` | `01_requisitos` | |
| `arquitetura` | `arq` | `02_arquitetura` | Estrutura arc42 |
| `adr` | `adr` | `02_arquitetura/adr` | |
| `teste` | `tst` | `03_implementacao/testes` | |
| `homologacao` | `hml` | `03_implementacao/homologacao` | |
| `operacao` | `ops` | `04_operacao` | Runbooks |
| `relatorio` | `rel` | `05_progresso/geral` | |
| `dicionario_dados` | `dic` | `09_dados_e_tabelas/dicionario` | Um por tabela |
| `inventario_lgpd` | `lgp` | `09_dados_e_tabelas/lgpd` | Classificação `pessoal` |
| `guia` | `gui` | conforme o assunto | |

Planos, anexos, `SESSAO_*` e pendências **não** têm tipo aqui: seguem as skills próprias. Crie a subpasta se ela ainda não existir. O script `scripts/docs/novo_doc.py` cria os documentos acima a partir dos modelos de `02_modelos`.

## 3. Front matter

```yaml
---
id: ADR-001
tipo: adr
titulo: Banco relacional como base principal
chamado: "00000"
requisicao: "00"
codigo: F1.S1.P2
status: aprovado
versao: 1.0.0
data: 2026-11-09
autor: Nome
classificacao: interno
---
```
