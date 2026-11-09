---
id: GUI-003
tipo: guia
titulo: Nomenclatura e front matter
status: rascunho
versao: 0.1.0
data: 2026-11-09
autor: Ricardo
classificacao: publico
---

# G03 – Nomenclatura e front matter

## 1. Regras de nome

| Item | Regra | Exemplo |
|---|---|---|
| Pasta de nível 1 | `NN_nome` em snake_case, sem acento | `09_dados_e_tabelas` |
| Subpasta | snake_case, sem acento | `planos_ativos` |
| Documento novo | `<prefixo>_<NNN>_<slug>.md`, minúsculo | `adr_001_banco_relacional.md` |
| Plano | `<nome>-DD_MM_AA-hh_mm.md` | `offline_sync-24_07_26-09_40.md` |
| Anexo de plano | `F<n>_S<n>_<slug>-DD_MM_AA.md` | `F2_S1_contrato_fila-24_07_26.md` |

Planos e anexos seguem a regra da skill `documente-o-plano`, não a tabela acima.

## 1-B. Nomes que já existem no kit (não renomear)

| Documento | Nome | Criado por |
|---|---|---|
| Registro diário de sessão | `SESSAO_AAAA-MM-DD_<DESCRICAO>.md` em `05_progresso/geral/` | skill `encerrar-sessao` |
| Plano | `<nome>-DD_MM_AA-hh_mm.md` em `planos_ativos/` | skill `documente-o-plano` |
| Anexo | `F<n>_S<n>_<slug>-DD_MM_AA.md` em `planos_ativos/anexos/` | skill `documente-o-plano` |
| Pendência | pasta `05_progresso/pendencias/` | skill `inserir-pendencia` |

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
| `teste` | `tst` | `03_implementacao/testes` | *(proposta)* |
| `homologacao` | `hml` | `03_implementacao/homologacao` | *(proposta)* |
| `operacao` | `ops` | `04_operacao` | Runbooks |
| `pendencia` | `pen` | `05_progresso/pendencias` | Criada pela skill `inserir-pendencia` |
| `relatorio` | `rel` | `05_progresso/geral` | |
| `dicionario_dados` | `dic` | `09_dados_e_tabelas/dicionario` | |
| `guia` | `gui` | conforme o assunto | |

Crie a subpasta se ela ainda não existir.

## 3. Front matter

````yaml
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
requisitos: [REQ-003, RN-001]
classificacao: interno
---
````
## 5. O que o lint cobra

| Alvo | Resultado |
|---|---|
| Planos, anexos, `SESSAO_*`, pendências, `legados/` | Ignorados (têm formato próprio) |
| `README.md` | Ignorado |
| `02_modelos` | Ignorado |
| Documento com front matter | Erro se faltar campo obrigatório, id duplicado ou valor inválido |
| Documento sem front matter | Aviso (erro só no modo estrito, a partir da F2) |