# Script de comandos simples para PowerShell
# Predicciones Deportivas - Comandos basicos

param(
    [string]$Comando = "ayuda"
)

function Show-Help {
    Write-Host "=== COMANDOS DISPONIBLES ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "INFORMACION:" -ForegroundColor Blue
    Write-Host "  ayuda          - Mostrar esta ayuda" -ForegroundColor Cyan
    Write-Host "  estado         - Verificar estado del proyecto" -ForegroundColor Cyan
    Write-Host "  test           - Ejecutar pruebas basicas" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "SCRAPING:" -ForegroundColor Blue
    Write-Host "  consensus      - Obtener consensus de hoy" -ForegroundColor Cyan
    Write-Host "  resultados     - Obtener resultados recientes" -ForegroundColor Cyan
    Write-Host "  recopilar      - Recopilar SOLO totals + resultados (optimizado)" -ForegroundColor Cyan
    Write-Host "  limpiar        - Vaciar base de datos" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "ANALISIS:" -ForegroundColor Blue
    Write-Host "  historicos     - Recopilar datos historicos" -ForegroundColor Cyan
    Write-Host "  efectividad    - Analizar efectividad" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "SIMULADOR:" -ForegroundColor Blue
    Write-Host "  simulador      - Abrir simulador de apuestas web" -ForegroundColor Cyan
    Write-Host "  sim            - Abrir simulador de apuestas web" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\comandos_simple.ps1 -Comando <comando>" -ForegroundColor Yellow
}

function Check-Status {
    Write-Host "=== ESTADO DEL PROYECTO ===" -ForegroundColor Green
    python verificar_sistema.py
}

# Ejecutar comando
switch ($Comando.ToLower()) {
    "ayuda" { Show-Help }
    "help" { Show-Help }
    "estado" { Check-Status }
    "status" { Check-Status }
    "test" {
        Write-Host "🧪 Ejecutando pruebas básicas..." -ForegroundColor Blue
        python tests/test_simple.py
    }
    "consensus" {
        Write-Host "📊 Obteniendo consensus..." -ForegroundColor Blue
        python scripts/mlb_main.py
    }
    "resultados" {
        Write-Host "📈 Obteniendo resultados..." -ForegroundColor Blue
        python scripts/actualizar_resultados_supabase.py
    }
    "historicos" {
        Write-Host "📚 Recopilando datos históricos..." -ForegroundColor Blue
        python analytics/recopilar_datos_historicos.py
    }
    "efectividad" {
        Write-Host "📊 Analizando efectividad..." -ForegroundColor Blue
        python analytics/mlb/analizador_efectividad.py
    }
    "recopilar" {
        Write-Host "🎯 Recopilando SOLO totals + resultados..." -ForegroundColor Blue
        Write-Host "⚠️  Versión optimizada para simulador" -ForegroundColor Yellow
        python recopilador_totals_only.py
    }
    "limpiar" {
        Write-Host "🧹 Limpiando base de datos..." -ForegroundColor Blue
        Write-Host "⚠️  PRECAUCIÓN: Eliminará todos los datos" -ForegroundColor Red
        python limpiar_bd.py
    }
    "simulador" {
        Write-Host "🎰 Iniciando simulador de apuestas..." -ForegroundColor Blue
        Write-Host "📊 Accede a: http://localhost:5001" -ForegroundColor Green
        Start-Process "http://localhost:5001"
        python simulador_apuestas.py
    }
    "sim" {
        Write-Host "🎰 Iniciando simulador de apuestas..." -ForegroundColor Blue
        Write-Host "📊 Accede a: http://localhost:5001" -ForegroundColor Green
        Start-Process "http://localhost:5001"
        python simulador_apuestas.py
    }
    default {
        Write-Host "❌ Comando no reconocido: $Comando" -ForegroundColor Red
        Write-Host "Usa 'ayuda' para ver comandos disponibles" -ForegroundColor Yellow
    }
}
