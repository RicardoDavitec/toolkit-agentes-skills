---
id: GUI-012
tipo: guia
titulo: LGPD e classificação de informação
status: rascunho
versao: 0.1.0
data: 2026-11-09
autor: Ricardo
classificacao: publico
---

# G12 – LGPD e classificação

> Este guia orienta a prática do projeto. Não substitui parecer jurídico nem a orientação do encarregado (DPO, Data Protection Officer) do órgão.

## 1. Níveis de classificação

| Nível | Quando usar | Exemplo |
|---|---|---|
| `publico` | Pode ir a repositório público | Este padrão |
| `interno` | Uso da equipe e do órgão | Arquitetura, ADRs |
| `restrito` | Exposição causa dano | Topologia de rede, configuração |
| `pessoal` | Contém ou descreve dado pessoal | Inventário LGPD, dicionário de dados de saúde |

## 2. Conceitos da LGPD (Lei nº 13.709/2018)

| Conceito | Resumo |
|---|---|
| Dado pessoal | Informação de pessoa natural identificada ou identificável |
| Dado pessoal sensível (art. 5º, II) | Saúde, origem racial, convicção religiosa, biometria e outros |
| Bases legais | Art. 7º (dados comuns) e art. 11 (sensíveis) |
| Poder público | Regras específicas nos arts. 23 a 30 |
| ANPD | Autoridade Nacional de Proteção de Dados |
| RIPD | Relatório de Impacto à Proteção de Dados Pessoais |

## 3. Inventário de dados pessoais (`09_dados_e_tabelas/lgpd`)

| Tabela | Campo | Dado | Sensível? | Finalidade | Base legal | Retenção | Acesso |
|---|---|---|---|---|---|---|---|
| `pacientes` | `cpf` | CPF | Não | Identificação | A definir | A definir | Papéis X, Y |

Regra: **cada ponto onde o dado aparece é uma exposição**. Se `cpf` está em cinco tabelas, são cinco linhas.

## 4. Regras para os documentos

1. Nunca inclua dado pessoal real em exemplos, prints, logs ou atas. Use dados fictícios.
2. Nunca inclua segredos. O `lint_template.py` bloqueia padrões que lembram chave ou token.
3. Em prints, oculte nomes, CPFs, telefones e endereços.
4. Marque a `classificacao` no front matter.
5. Documento `pessoal` não vai para repositório público.

## 5. Quando fazer o RIPD

Avalie a necessidade quando o sistema tratar dado sensível em escala, geolocalização, ou decisões automatizadas. A decisão fica registrada em ADR.

## 6. Por fase

| Fase | Ação |
|---|---|
| F1 | Classificar dados previstos e levantar bases legais |
| F2 | Manter o inventário a cada mudança de esquema |
| F3 | Testar controle de acesso e mascaramento |
| F4 | Usar dados fictícios ou anonimizados |
| F5 | Validar retenção, descarte e resposta a incidente |

## 7. Incidente de segurança

Se houver vazamento ou suspeita, abra incidente ITIL e acione o encarregado imediatamente. O registro não deve repetir o dado vazado.
