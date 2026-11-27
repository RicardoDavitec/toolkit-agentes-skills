---
id: GUI-017
tipo: guia
titulo: Política de publicação do repositório público
codigo: F1.S2.P2
status: rascunho
versao: 0.1.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Política de publicação do repositório público

O repositório público recebe o padrão genérico, os scripts, as skills, os agentes e a documentação de uso. O que segue não entra neste repositório.

## Nunca publicar
- Nome de produto interno.
- Número de chamado real.
- Plano interno, decisão interna, histórico real ou lista de pendência interna.
- Planilha, CSV ou outro arquivo com dado de produto ou de pessoa.
- Dado pessoal ou identificação de cliente.
- Credencial, token, `.env`, `instance.yaml` ou `service_account.json`.

Antes de cada commit, o diff em stage é conferido contra esta lista.
