# Scripts de manutenção por código

Python 3, só biblioteca padrão. Funcionam em Linux e em Windows.

O registro é um JSON do projeto, fora do template. Caminho sugerido: `.glpi/manutencao/registro-codigos.json`. A escala e o histórico do produto ficam na mesma pasta. `bootstrap-into.sh` e `upgrade-into.sh` não sobrescrevem `.glpi/manutencao/`. No Windows, `upgrade-into.sh` roda no Git Bash ou no WSL.

```json
{
  "itens": [
    {
      "codigo": "ppain1",
      "caminho": "painel.html",
      "descricao": "Painel inicial",
      "aposentado": false
    }
  ]
}
```

`codigo` segue `^[pqjmec][a-z]{2,4}[0-9]{1,2}$`. `caminho` é relativo à raiz do projeto e precisa existir, salvo quando `aposentado` é `true`. Código repetido, inclusive aposentado, é recusado.

## Comandos

```bash
python3 scripts/manutencao/varrer_codigos.py .
python3 scripts/manutencao/validar_registro.py registro-codigos.json --raiz .
python3 scripts/manutencao/gerar_tabela.py registro-codigos.json --saida tabela-mapeamento.md
scripts/manutencao/manutencao.sh varrer .
python3 -m unittest discover -s scripts/manutencao/testes -v
```

No Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/manutencao/manutencao.ps1 varrer .
```

`-ExecutionPolicy Bypass` vale só para esse processo, quando a política local recusa o arquivo. O script procura `python3` e, se faltar, `python`. Sem os dois, a mensagem é: `Python 3 nao encontrado. Instale Python 3 e tente de novo.`

`varrer_codigos.py` lista `data-maint-id` em arquivos de texto. Não entra em `.git` nem segue link.

## Migração de legado

O template não tem telas. O migrador não inventa código nem lê planilha.

A entrada é um JSON na mesma forma do registro, ou a pasta do projeto se os elementos já tiverem `data-maint-id`. A saída mescla em `.glpi/manutencao/registro-codigos.json`.

- Código que já está no destino permanece, com o caminho que já tinha.
- Código novo entra só se o formato for válido e o caminho existir, salvo aposentado.
- Sem `--apply`, o comando só mostra o que mudaria.
- Escala (`.glpi/manutencao/escala.json`) e histórico (`.glpi/manutencao/historico/`) não são gravados por este comando.

```bash
python3 scripts/manutencao/migrar_legado.py --origem mapa.json --destino .glpi/manutencao/registro-codigos.json --raiz .
python3 scripts/manutencao/migrar_legado.py --origem mapa.json --destino .glpi/manutencao/registro-codigos.json --raiz . --apply
```

`varrer_codigos.py` termina com código 2 se a pasta não existe. `validar_registro.py` termina com código 1 quando há erro e escreve a mensagem na saída de erro. `gerar_tabela.py` só confere se o JSON está bem formado; a checagem de código, duplicidade e caminho fica com `validar_registro.py`, que deve passar antes de publicar a tabela.
