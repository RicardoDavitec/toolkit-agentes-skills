# Guia de Uso de Agentes e Skills (PT-BR)

Este guia descreve como usar os agentes e skills criados para um fluxo de desenvolvimento hexagonal com foco em seguranca operacional e rastreabilidade.

## Endpoints operacionais (configuracao central)

- Arquivo: `.github/skills/config/endpoints_operacionais.json`
- Objetivo: definir destinos padrao e politicas operacionais consumidas por skills e agentes.
- Blocos principais:
	- `backup`: destino por SO, fallback por SO e formato de nome de arquivo.
	- `sessao`: pasta de historico, formato de nome e titulo padrao.
	- `seguranca`: roots permitidos para escrita.

Padrao atual de backup:
- Windows: `E:/VSCode-bkp`
- Linux/WSL: `/mnt/e/VSCode-bkp`
- Darwin: `/Volumes/VSCode-bkp`
- Fallback nesta maquina quando externo ausente: `D:/VSCode-bkp`
- Estrutura: `<destino>/<nome-do-projeto>/<commit>_<DD-MM-YY_hh-mm>.tar.gz`
- Integridade: `<arquivo>.tar.gz.SHA256`

## Estrutura criada

### Agentes
- .github/agents/orquestrador-hexagonal.agent.md
- .github/agents/revisor-arquitetura-hexagonal.agent.md
- .github/agents/analista-incidentes-integracao.agent.md
- .github/agents/operador-entrega-controlada.agent.md

### Skills
- .github/skills/fluxo-orquestrado-hexagonal/SKILL.md
- .github/skills/guardrails-hexagonal/SKILL.md
- .github/skills/checar-contratos-portas/SKILL.md
- .github/skills/revisar-casos-de-uso/SKILL.md
- .github/skills/operacao-planilha-segura/SKILL.md
- .github/skills/gate-release-hexagonal/SKILL.md
- .github/skills/documentar-sessao/SKILL.md
- .github/skills/backup-projeto/SKILL.md
- .github/skills/encerrar-sessao/SKILL.md

## Como pensar o fluxo

1. O agente principal orquestra.
2. Skills definem procedimentos reutilizaveis.
3. Subagentes executam partes especializadas quando necessario.

## Fluxos recomendados

### Fluxo 0: Orquestracao completa
1. Invoque Orquestrador Hexagonal.
2. Aplique fluxo-orquestrado-hexagonal para quebrar etapas.
3. Delegue para subagentes por tipo de etapa.
4. Feche com documentar-sessao e encerrar-sessao.

### Fluxo 1: Implementacao segura
1. Invoque Orquestrador Hexagonal com objetivo claro.
2. Aplique revisar-casos-de-uso.
3. Se houver risco de arquitetura, aplique guardrails-hexagonal.
4. Implemente com Operador Entrega Controlada.
5. Finalize com documentar-sessao.

### Fluxo 2: Incidente de integracao
1. Invoque Analista Incidentes Integracao.
2. Aplique checar-contratos-portas.
3. Se envolver planilha, aplique operacao-planilha-segura.
4. Gere recomendacao de mitigacao e correcao definitiva.
5. Finalize com documentar-sessao.

### Fluxo 3: Pre-release
1. Invoque Orquestrador Hexagonal.
2. Aplique gate-release-hexagonal.
3. Resolva pendencias apontadas.
4. Encerrar com encerrar-sessao.
5. Opcional: backup-projeto.

## Padrao de prompts

Use prompts com 4 blocos:
1. Objetivo
2. Escopo
3. Restricoes
4. Criterio de pronto

Exemplo:

"Objetivo: ajustar fluxo de envio em lote.
Escopo: somente camada application e adapter twilio.
Restricoes: sem alterar dominio e sem mexer em deploy.
Criterio de pronto: testes passando e documentacao de decisao atualizada."

## Convencoes de nomeacao (PT-BR sem acento)

- Agentes: substantivo + contexto, exemplo: operador-entrega-controlada.
- Skills: verbo no infinitivo + objeto, exemplo: checar-contratos-portas.
- Evite acentos e espacos para manter compatibilidade de tooling.

## Boas praticas

1. Mantenha skills focadas e curtas.
2. Evite skill monolitica com muitos objetivos.
3. Prefira subagente para analise especializada.
4. Use documentar-sessao em marcos de trabalho.
5. Use encerrar-sessao no fechamento do dia.

## Proximas evolucoes sugeridas

1. Adicionar templates em .github/skills/<skill>/assets para padronizar saida.
2. Integrar backup-projeto com validacao de destino externo e retencao.
3. Criar script de gate-release com verificacoes automatizadas.

## Execucao rapida de scripts de apoio

1. Checklist de fluxo:
python .github/skills/fluxo-orquestrado-hexagonal/scripts/gerar_checklist_fluxo.py

2. Resumo de sessao:
python .github/skills/documentar-sessao/scripts/gerar_resumo_sessao.py
python .github/skills/documentar-sessao/scripts/gerar_resumo_sessao.py --saida docs/06_progresso/historico/sessao_2026-04-03.md

3. Checklist de encerramento:
python .github/skills/encerrar-sessao/scripts/checklist_encerramento.py --repo .

4. Backup por ambiente:
python .github/skills/backup-projeto/scripts/backup_projeto.py
python .github/skills/backup-projeto/scripts/backup_projeto.py --destino E:\\VSCode-bkp

## Variaveis de ambiente para endpoints de backup

- Destino principal por SO:
	- `BACKUP_DESTINO_WINDOWS`
	- `BACKUP_DESTINO_LINUX`
	- `BACKUP_DESTINO_DARWIN`
- Fallback por SO:
	- `BACKUP_DESTINO_FALLBACK_WINDOWS`
	- `BACKUP_DESTINO_FALLBACK_LINUX`
	- `BACKUP_DESTINO_FALLBACK_DARWIN`

Arquivo exemplo por maquina:
- `.env.endpoints.backup.example`

Fluxo recomendado:
1. Copiar as chaves necessarias do arquivo exemplo para o `.env` local.
2. Ajustar caminhos conforme a maquina atual.
3. Rodar `checklist_encerramento.py` para confirmar endpoint resolvido.

Observacao:
- Os scripts de backup, encerramento e documentacao carregam automaticamente variaveis do `.env` da raiz do repositorio (quando `python-dotenv` estiver disponivel).

## Variaveis de ambiente para endpoints de sessao

- `SESSAO_HISTORICO_RELATIVO_REPO`
- `SESSAO_FORMATO_NOME_ARQUIVO`
- `SESSAO_TITULO_PADRAO`
