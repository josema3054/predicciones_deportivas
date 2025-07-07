# 🚀 Inicio Rápido - PowerShell

## Configuración Inicial (Una sola vez)

```powershell
# 1. Navegar al directorio del proyecto
cd "C:\Users\JVILLA\Desktop\predicciones_deportivas"

# 2. Ejecutar configuración automática
.\setup_powershell.ps1

# 3. Editar archivo .env con tus credenciales de Supabase
notepad .env
```

## Comandos Más Utilizados

```powershell
# Ver todos los comandos disponibles
.\comandos_powershell.ps1 -Comando ayuda

# Verificar que todo funciona
.\comandos_powershell.ps1 -Comando test

# Ejecutar scraping completo
.\comandos_powershell.ps1 -Comando scraping

# Recopilar datos históricos
.\comandos_powershell.ps1 -Comando historicos

# Analizar efectividad
.\comandos_powershell.ps1 -Comando efectividad

# Abrir dashboard web
.\comandos_powershell.ps1 -Comando dashboard
```

## Flujo de Trabajo Típico

### 1. Primera vez (Configuración)
```powershell
.\setup_powershell.ps1
# Editar .env con credenciales
.\comandos_powershell.ps1 -Comando tablas
.\comandos_powershell.ps1 -Comando test
```

### 2. Uso diario (Scraping)
```powershell
.\comandos_powershell.ps1 -Comando scraping
```

### 3. Análisis (Fase 3)
```powershell
.\comandos_powershell.ps1 -Comando historicos
.\comandos_powershell.ps1 -Comando efectividad
.\comandos_powershell.ps1 -Comando dashboard
```

## Solución de Problemas

### Error: "No se puede ejecutar scripts"
```powershell
# Ejecutar una sola vez como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Python no encontrado"
- Instalar Python desde https://python.org
- Asegurarse de marcar "Add Python to PATH"

### Error: "Archivo .env no encontrado"
```powershell
# El script setup_powershell.ps1 lo crea automáticamente
# Solo necesitas editarlo con tus credenciales
```

## Archivos Importantes

- `setup_powershell.ps1` - Configuración automática
- `comandos_powershell.ps1` - Comandos integrados
- `.env` - Credenciales de Supabase
- `docs/GUIA_WINDOWS.md` - Guía completa
