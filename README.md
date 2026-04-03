# toolkit-agentes-skills

Kit reutilizavel de agentes e skills para VS Code + Copilot Chat, com foco em operacao segura, documentacao de sessao e backup portavel por maquina.

## Conteudo

- `.github/agents/`: agentes especializados (orquestrador, revisor, operador, analista).
- `.github/skills/`: skills operacionais e de fluxo.
- `.github/skills/config/endpoints_operacionais.json`: endpoints padrao de backup/sessao.
- `.env.endpoints.example`: exemplo de variaveis de ambiente por maquina.
- `docs/guia_agentes_skills_ptbr.md`: guia de uso em Portugues-BR.
- `docs/00_visao_geral` ate `docs/06_progresso/historico`: esqueleto padrao de documentacao.

## Skills principais

- `backup-projeto`
- `documentar-sessao`
- `encerrar-sessao`
- `fluxo-orquestrado-hexagonal`
- `guardrails-hexagonal`
- `checar-contratos-portas`
- `revisar-casos-de-uso`
- `operacao-planilha-segura`
- `gate-release-hexagonal`

## Setup rapido

1. Copie os arquivos deste repositiorio para o projeto alvo.
2. Copie as variaveis necessarias de `.env.endpoints.example` para o `.env` local do projeto alvo.
3. Ajuste caminhos por maquina (Windows/Linux/Darwin).
4. Use os scripts das skills para validar operacao.

## Arvore padrao de docs

- `docs/00_visao_geral`
- `docs/01_requisitos`
- `docs/02_arquitetura`
- `docs/03_implementacao`
- `docs/04_operacao`
- `docs/05_progresso`
- `docs/06_progresso/historico`

## Precedencia de configuracao (backup/sessao)

1. Argumentos de linha de comando (`--destino`, `--saida`, `--titulo`)
2. Variaveis de ambiente no shell ou no `.env`
3. `.github/skills/config/endpoints_operacionais.json`
4. Fallback local no repositorio

## Publicar no GitHub

```powershell
git init
git add .
git commit -m "chore: estrutura inicial toolkit-agentes-skills"
git branch -M main
git remote add origin <URL_DO_REPO_NO_GITHUB>
git push -u origin main
```

## Observacoes

- Este kit funciona tambem em projetos nao-hexagonais. Basta manter as skills operacionais e adaptar os agentes/skills de arquitetura para o dominio do projeto.
- Nomes de arquivos e identificadores estao sem acentos para manter compatibilidade ampla com tooling.
