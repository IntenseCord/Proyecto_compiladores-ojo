# Script para ejecutar programas MiniLang fácilmente
# Uso: .\run_example.ps1 [archivo.minilang]
# Ejemplo: .\run_example.ps1 tests\tu_programa.minilang

param(
    [string]$SourceFile = "tests\tu_programa.minilang"
)

# Obtener el directorio del script (donde está el proyecto)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Cambiar al directorio del proyecto
Push-Location $ProjectRoot

try {
    Write-Host "Compilando y ejecutando: $SourceFile" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    # Ejecutar el compilador con la VM
    python -m minilang_compiler.compiler $SourceFile --run
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host "✓ Ejecución completada exitosamente" -ForegroundColor Green
    } else {
        Write-Host "`n========================================" -ForegroundColor Red
        Write-Host "✗ Error durante la ejecución (código: $LASTEXITCODE)" -ForegroundColor Red
    }
} finally {
    # Volver al directorio original
    Pop-Location
}
