---
id: GUI-011
tipo: guia
titulo: Dados, ER e dicionário
status: rascunho
versao: 0.1.0
data: 2026-11-09
autor: Ricardo
classificacao: publico
---

# G11 – Dados, ER e dicionário de dados

Aplica-se a qualquer projeto com banco de dados. O exemplo usa Prisma (ORM, Object-Relational Mapping), mas a estrutura vale para outros.

## 1. Estrutura em `09_dados_e_tabelas`

```text
09_dados_e_tabelas/
├── README.md
├── er/            diagramas por módulo (Mermaid)
├── dicionario/    um dic_<tabela>.md por tabela
├── enums/         catálogo de valores e significados
├── lgpd/          inventário de dados pessoais
└── linhagem/      origem e destino dos dados (integrações)
```

## 2. Fonte e geração

| Saída | Fonte | Ferramenta |
|---|---|---|
| ER por módulo | `schema.prisma` | `prisma-markdown` ou `prisma-erd-generator` |
| Dicionário base | `schema.prisma` | `prisma-markdown` |
| Documentação do banco real | PostgreSQL | `tbls` ou SchemaSpy |
| Descrições, domínios, LGPD | Curadoria humana | Comentários `///` e `dic_*.md` |

## 3. Comentários `///` no schema

```prisma
/// Atendimento. Entidade central do fluxo.
/// @sens: SAUDE
model Atendimento {
  /// Identificador único (UUID)
  id String @id @default(uuid())

  /// CPF do paciente
  /// @pii: true
  /// @base_legal: LGPD art. 11, II, f (tutela da saúde)
  cpfPaciente String? @map("cpf_paciente")
}
```

Onde:
- `///`: comentário que o Prisma entrega aos geradores.
- `@sens`: sensibilidade do modelo (`SAUDE`, `FINANCEIRO`, `NENHUMA`).
- `@pii`: indica dado pessoal (PII, Personally Identifiable Information).
- `@base_legal`: fundamento da LGPD para tratar o dado.

## 4. Regras do dicionário (ISO/IEC 11179)

1. Um documento `dic_` por tabela, com: finalidade, colunas, relacionamentos, índices e restrições, RN relacionadas.
2. Todo campo tem descrição, tipo, nulabilidade, padrão e se é dado pessoal.
3. Campos `String` que funcionam como enum listam os **valores permitidos**.
4. Campos JSON trazem um **exemplo** ou JSON Schema.
5. Relações sem `@relation` (chave solta) entram na seção de **dívida técnica**.
6. Dados pessoais repetidos em várias tabelas aparecem no inventário de G12.

## 5. Quando regenerar

| Evento | Ação |
|---|---|
| Mudança em `schema.prisma` ou nova migração | Regenerar ER e dicionário; revisar campos sem descrição |
| Novo enum ou valor | Atualizar `enums/` |
| Nova integração | Atualizar `linhagem/` |

## 6. Cobertura de documentação

$$
C_{doc} = \frac{N_{doc}}{N_{total}} \times 100
$$

Onde:
- $$C_{doc}$$ (Cobertura de Documentação): percentual de elementos do schema com descrição.
- $$N_{doc}$$ (Número de elementos documentados): modelos, campos e enums com comentário `///`.
- $$N_{total}$$ (Número total de elementos): todos os modelos, campos e enums.

Meta sugerida: $$C_{doc} \geq 95\%$$ ao final da F2.

## 7. Qualidade de dados (ISO/IEC 25012)

Para cada tabela crítica, avalie: exatidão, completude, consistência, atualidade e rastreabilidade. Registre no `dic_` quando houver risco conhecido.
