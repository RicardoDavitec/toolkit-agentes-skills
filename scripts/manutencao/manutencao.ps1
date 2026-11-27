param(
    [Parameter(Position = 0)]
    [string]$Comando,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Resto
)

$ErrorActionPreference = "Stop"
$Dir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($null -eq $Resto) { $Resto = @() }

switch ($Comando) {
    "varrer" { & python3 (Join-Path $Dir "varrer_codigos.py") @Resto; exit $LASTEXITCODE }
    "validar" { & python3 (Join-Path $Dir "validar_registro.py") @Resto; exit $LASTEXITCODE }
    "tabela" { & python3 (Join-Path $Dir "gerar_tabela.py") @Resto; exit $LASTEXITCODE }
    default {
        Write-Error "Uso: manutencao.ps1 varrer|validar|tabela [argumentos]"
        exit 2
    }
}
