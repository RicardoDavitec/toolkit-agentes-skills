---
id: GUI-007
tipo: guia
titulo: Fase F4 – Homologação
status: rascunho
versao: 0.1.0
data: 2026-11-09
autor: Ricardo
classificacao: publico
---
# G07 – Fase F4: Homologação

**Objetivo:** validar o sistema com o usuário final, em ambiente de homologação.

## 1. Preparação

| Item | Detalhe |
|---|---|
| Ambiente | Cópia fiel da produção, com dados fictícios ou anonimizados |
| Configuração GLPI | O kit traz `project.homolog.yaml.example` em `.glpi/` |
| Participantes | Usuários-chave, solicitante do chamado, equipe técnica |
| Roteiro | Cenários em linguagem do negócio, ligados aos REQ |

## 2. Fluxo

```mermaid
flowchart TD
  A["Preparar ambiente e roteiro"] --> B["Executar com o usuário"]
  B --> C["Registrar achados"]
  C --> D{"Resultado"}
  D -- aprovado --> E["Ata assinada"]
  D -- ressalvas --> F["Ajustes: F2 e F3"]
  D -- reprovado --> F
  F --> B
  E --> G["Marcar [A] com accept_ref"]
```

## 3. Ata de homologação (`hml_`)

Seções: participantes e data, escopo, cenários executados e resultado, achados (com gravidade), decisão (aprovado, aprovado com ressalvas, reprovado), prazos dos ajustes, assinaturas ou referência de aceite.

## 4. Regras

- Dado pessoal real não vai para homologação sem base legal e autorização (G12).
- Mudança pedida no teste é ajuste de escopo: nova P no plano e rastro no GLPI.
- O marcador `[A]` (closed) exige `accept_ref`, a referência do aceite (ata, e-mail ou parecer).
- Anexe evidências ao GLPI com a skill `glpi-document-attach`.

## 5. Checklist de saída (DoD da F4)

- [ ] Roteiro executado com o usuário
- [ ] Ata registrada e aceita
- [ ] Ajustes tratados ou formalizados como pendência
- [ ] Documentação de usuário e runbooks revisados com o que a homologação revelou
