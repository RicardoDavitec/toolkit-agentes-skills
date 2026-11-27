param(
    [Parameter(Position = 0)]
    [string]$Comando,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Resto
)

$ErrorActionPreference = "Stop"
$Dir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($null -eq $Resto) { $Resto = @() }

$Python = $null
foreach ($nome in @("python3", "python")) {
    $achado = Get-Command $nome -ErrorAction SilentlyContinue
    if ($achado) { $Python = $achado.Source; break }
}
if (-not $Python) {
    Write-Error "Python 3 nao encontrado. Instale Python 3 e tente de novo."
    exit 127
}

switch ($Comando) {
    "varrer" { & $Python (Join-Path $Dir "varrer_codigos.py") @Resto; exit $LASTEXITCODE }
    "validar" { & $Python (Join-Path $Dir "validar_registro.py") @Resto; exit $LASTEXITCODE }
    "tabela" { & $Python (Join-Path $Dir "gerar_tabela.py") @Resto; exit $LASTEXITCODE }
    default {
        Write-Error "Uso: manutencao.ps1 varrer|validar|tabela [argumentos]"
        exit 2
    }
}
