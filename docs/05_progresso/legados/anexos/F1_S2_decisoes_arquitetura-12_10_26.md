# F1.S2 — Decisoes de arquitetura do template (opcoes em aberto)

> Plano: [`unificacao_template_kit_glpi-12_10_26-10_40.md`](../unificacao_template_kit_glpi-12_10_26-10_40.md)
> Nenhuma decisao abaixo esta tomada; cada uma fecha um P do F1.S2.

## F1.S2.P1 — Fonte unica e espelho Cursor/Copilot

Diretriz ja definida pelo responsavel (12/10/2026): **fonte unica** de skills e
agentes; acabar com copias divergentes.

| Opcao | Como | Pro | Contra |
|-------|------|-----|--------|
| A (preferida) | Canonico em `.github/skills`; `.cursor/skills` e link simbolico | Zero copia; Copilot e Cursor leem o mesmo | Windows sem WSL exige `core.symlinks=true` e modo desenvolvedor |
| B | Canonico em `.github/skills`; script copia para `.cursor/skills` | Funciona em qualquer SO | Copia pode desatualizar; exige validador no CI |
| C | Canonico em `.cursor/skills` | Nativo do Cursor | Exige reescrever scripts do kit que escrevem em `.github` |

Agentes: os formatos sao diferentes (Copilot `.agent.md` com `tools`/`agents`;
Cursor `.cursor/agents/*.md`). Link simbolico nao basta — decidir entre gerador
a partir de um arquivo unico ou wrapper fino no Cursor apontando para o agente
canonico.

## F1.S2.P2 — Arvore de documentacao

| Template hoje | Kit GLPI hoje |
|---------------|---------------|
| `05_progresso` (status macro) | `05_progresso/planos_ativos`, `geral`, `legados`, `pendencias` |
| `06_progresso/historico` (sessoes) | `05_progresso/geral` (sessoes `SESSAO_*`) |
| — | `06_glpi` (manuais e hierarquia) |

Proposta a validar: adotar a arvore do kit GLPI (`06` = GLPI) e mover o
historico de sessoes para `05_progresso/geral`, ajustando
`endpoints_operacionais.json` e a skill `documentar-sessao`.

## F1.S2.P3 — Importacao com historico

| Metodo | Observacao |
|--------|------------|
| `git subtree add --prefix=...` | Historico preservado em subpasta; depois mover arquivos |
| `git merge --allow-unrelated-histories` em branch | Historico na raiz; conflitos em `README.md`, `.gitignore`, `encerrar-sessao` |

Regras obrigatorias, qualquer que seja o metodo:

- Resolver conflito **arquivo a arquivo**; proibido `-X union` ou aceitar
  "ambos" sem edicao (causa raiz dos defeitos do Bot_Pan).
- Antes do commit de merge: `rg -n '^(<<<<<<<|=======|>>>>>>>)'` sem resultado
  e lint de cabecalho das skills sem erro.

## F1.S2.P4 — Glossario PT-BR

Itens a traduzir e padronizar (identificadores sem acento):

- nomes de skills e agentes (ex.: `glpi-orchestrator` → `glpi-orquestrador`);
- `description` e palavras-chave de acionamento das skills;
- titulos, categorias e tags dos chamados GLPI;
- rotulos dos estados (`todo`, `doing`, `testing`, `done`, `closed`) e das
  fases F1..F5 nos templates `.glpi/`.

Renomear skill quebra comandos ja usados nos projetos: manter alias depreciado
(padrao ja usado em `glpi-followup` → `acompanhar-chamado`).
