# 🖥️ Guía Completa para Windows - Predicciones Deportivas

Esta guía te ayudará a configurar y usar el proyecto de predicciones deportivas en Windows con PowerShell.

## 🚀 Configuración Automática (Recomendado)

### Opción 1: Script de Configuración Automática
```powershell
# Navegar al directorio del proyecto
cd "C:\Users\JVILLA\Desktop\predicciones_deportivas"

# Ejecutar configuración automática
.\setup_powershell.ps1
```

### Opción 2: Comandos Integrados
```powershell
# Ver todos los comandos disponibles
.\comandos_powershell.ps1 -Comando ayuda

# Verificar estado del proyecto
.\comandos_powershell.ps1 -Comando estado

# Ejecutar pruebas básicas
.\comandos_powershell.ps1 -Comando test
```

## 📋 Configuración Manual

Si prefieres configurar manualmente o si los scripts automáticos no funcionan:

### 1. Preparación del Entorno
```powershell
cd "C:\Users\JVILLA\Desktop\predicciones_deportivas"
```

Verificar que tienes Python:
```powershell
python --version
```

Instalar dependencias:
```powershell
pip install -r requirements.txt
```

### 2. Configuración Automática
Usar el script de configuración completa:
```powershell
python setup_completo.py todo
```

Este comando ejecutará todas las verificaciones y te guiará paso a paso.

### 3. Configuración Manual de Supabase (si es necesario)

**Opción A - Variables de Entorno (PowerShell):**
```powershell
$env:SUPABASE_URL="https://tu-proyecto.supabase.co"
$env:SUPABASE_ANON_KEY="tu_clave_anonima"
```

**Opción B - Archivo .env:**
```powershell
python setup_completo.py configurar_demo
# Luego edita .env con tus credenciales
```

## 📋 Comandos de Verificación (Windows)

### Verificaciones del Sistema

**1. Verificación completa automática:**
```powershell
python setup_completo.py todo
```

**2. Verificar solo variables de entorno:**
```powershell
python setup_completo.py verificar_entorno
```

**3. Verificar solo estructura de Supabase:**
```powershell
python setup_completo.py verificar_supabase
```

**4. Probar conexión a Supabase:**
```powershell
python setup_completo.py test_conexion
```

### Scraping y Análisis

**3. Prueba rápida:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python test_quick.py
```

### Scraping de Resultados

**1. Resultados del día anterior (automático):**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py resultados
```

**2. Resultados de fecha específica:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py resultados mlb 2025-06-29
```

**3. Otros deportes:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py resultados cfl 2025-06-29
```

```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py resultados wnba 2025-06-29
```

### Scraping de Consensus

**IMPORTANTE:** Requiere Chrome instalado en el sistema.

**1. Consensus del día anterior:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py consensus
```

**2. Consensus de fecha específica:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py consensus mlb 2025-06-29
```

### Pipeline Completo

**1. Pipeline automático (día anterior):**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py pipeline
```

**2. Pipeline para fecha específica:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py pipeline mlb 2025-06-29
```

### Análisis de Efectividad

**1. Análisis del día anterior:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py analisis
```

**2. Análisis de fecha específica:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py analisis mlb 2025-06-29
```

### Interfaz Web

**1. Lanzar Streamlit:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py streamlit
```

**2. O directamente:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
streamlit run app_streamlit.py
```

## 🔧 Instalación de ChromeDriver (Windows)

### Opción 1: Descarga Manual
1. Ir a: https://chromedriver.chromium.org/
2. Descargar la versión compatible con tu Chrome
3. Extraer `chromedriver.exe` a `C:\Windows\System32\` o agregar al PATH

### Opción 2: Chocolatey (Recomendado)
```cmd
choco install chromedriver
```

### Verificar instalación:
```cmd
chromedriver --version
```

## 🐛 Solución de Problemas Windows

### Error: "python no se reconoce"
```cmd
# Verificar instalación de Python
where python
```

Si no está instalado, descargar desde: https://python.org

### Error: ChromeDriver no encontrado
```cmd
# Verificar PATH
echo %PATH%
```

Asegúrate de que la carpeta de ChromeDriver esté en el PATH.

### Error: Módulo no encontrado
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
pip install -r requirements.txt
```

### Error: Variables de entorno
```cmd
# Verificar archivo .env
type .env
```

### Error: Permisos de PowerShell
Si usas PowerShell y tienes errores de ejecución:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Estructura de Archivos Windows

```
C:\Users\JVILLA\Desktop\predicciones_deportivas\
├── .env                          # Variables de entorno
├── comandos.py                   # CLI principal
├── scraper_historico.py          # Motor del sistema
├── app_streamlit.py              # Interfaz web
├── equipos_data.py               # Datos de equipos
├── test_simple.py                # Pruebas básicas
├── test_resultados.py            # Pruebas completas
├── requirements.txt              # Dependencias
├── README.md                     # Documentación principal
├── GUIA_WINDOWS.md               # Esta guía
└── datos\                        # Archivos CSV generados
    ├── mlb_consensus_*.csv
    └── mlb_resultados_*.csv
```

## 🚀 Flujo de Trabajo Recomendado (Windows)

### Para uso diario:

**1. Abrir terminal (cmd o PowerShell):**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
```

**2. Ejecutar prueba rápida:**
```cmd
python test_quick.py
```

**3. Obtener resultados del día anterior:**
```cmd
python comandos.py resultados
```

**4. Obtener consensus del día anterior:**
```cmd
python comandos.py consensus
```

**5. Ejecutar análisis:**
```cmd
python comandos.py analisis
```

### Para análisis específico:

**1. Cambiar al directorio:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
```

**2. Pipeline completo para fecha específica:**
```cmd
python comandos.py pipeline mlb 2025-06-29
```

## 📊 Verificación de Resultados

Después de ejecutar cualquier comando, verifica los archivos generados:

```cmd
dir *.csv
```

Los archivos CSV se guardan automáticamente con nombres como:
- `mlb_consensus_2025-06-29.csv`
- `mlb_consensus_totals_2025-06-29.csv`
- `mlb_resultados_2025-06-29.csv`

## 💡 Consejos para Windows

1. **Usa cmd.exe o PowerShell**: Evita Git Bash para estos comandos
2. **Rutas absolutas**: Siempre usa `cd` para ir al directorio del proyecto primero
3. **Un comando a la vez**: No uses `&&` o `;` para encadenar comandos
4. **Variables de entorno**: Asegúrate de que el archivo `.env` existe y tiene las credenciales correctas
5. **Permisos**: Ejecuta como administrador si tienes problemas de permisos

---

**✅ Con esta guía deberías poder ejecutar todos los comandos sin problemas en Windows**

## 📊 Estado Actual del Proyecto (30 Junio 2025)

### ✅ Funcionalidades Operativas
- **✅ Scraping de consensus Winners/Losers**: Funcionando perfectamente
  - Captura equipos, porcentajes, picks correctamente
  - Guarda en Supabase y CSV
  - Conversión de fechas operativa
  
- **✅ Scraping de consensus Over/Under Totals**: Funcionando perfectamente
  - Captura líneas totales, porcentajes over/under
  - Guarda en Supabase y CSV
  
- **✅ Scraping de resultados reales**: Funcionando perfectamente
  - Detecta partidos finalizados correctamente
  - Extrae puntajes finales
  - Guarda en formato CSV

- **✅ Sistema de comandos**: Totalmente funcional
  - CLI completa disponible (`comandos.py`)
  - Scripts de diagnóstico operativos
  - Interfaz Streamlit disponible

### 🔧 Estado del Matching y Actualización
- **✅ Lógica de matching implementada**: Busca por siglas, nombres y fechas flexibles
- **✅ Columnas mlb_consensus agregadas**: Listas para actualización
- **⚠️ Columnas consensus_totals**: **NECESITAN AGREGARSE MANUALMENTE**

### 🎯 Pendiente Inmediato

**PASO CRÍTICO: Agregar columnas a consensus_totals**

Ejecutar en Supabase SQL Editor:
```sql
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS puntaje_equipo_1 INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS puntaje_equipo_2 INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS total_real INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS resultado_real INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS efectividad INTEGER;
```

### 🎯 Pruebas Recomendadas

**1. Diagnóstico completo del sistema:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python diagnostico_windows.py
```

**2. Verificar sistema básico:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python test_simple.py
```

**3. Probar scraping de resultados (funciona):**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py resultados mlb 2025-06-29
```

**4. Verificar datos en Supabase:**
```cmd
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python test_matching_29.py
```

### 🚀 Próximos Pasos Sugeridos
1. **Corregir scraping de consensus** - El parsing de equipos necesita revisión
2. **Probar con fechas más recientes** - Usar datos de diciembre 2024 o enero 2025
3. **Validar pipeline completo** - Una vez corregido el consensus

---

## 🔧 Scripts de PowerShell (Nuevos)

### Configuración Automática
```powershell
# Configurar todo el proyecto automáticamente
.\setup_powershell.ps1
```

### Comandos Integrados
```powershell
# Ver todos los comandos disponibles
.\comandos_powershell.ps1 -Comando ayuda

# Verificar estado del proyecto
.\comandos_powershell.ps1 -Comando estado

# Ejecutar pruebas
.\comandos_powershell.ps1 -Comando test

# Verificar tablas de Supabase
.\comandos_powershell.ps1 -Comando tablas

# Ejecutar scraping completo
.\comandos_powershell.ps1 -Comando scraping

# Recopilar datos históricos
.\comandos_powershell.ps1 -Comando historicos

# Analizar efectividad
.\comandos_powershell.ps1 -Comando efectividad

# Abrir dashboard
.\comandos_powershell.ps1 -Comando dashboard
```

## 📋 Resumen de Comandos Principales (Windows)

### Diagnóstico y Verificación
```cmd
# Diagnóstico completo del sistema
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python diagnostico_windows.py

# Prueba básica
cd C:\Users\JVILLA\Desktop\predicciones_deportivas  
python test_simple.py

# Ver ayuda completa
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py help
```

### Comandos Operativos (Listos para usar)
```cmd
# Obtener resultados de una fecha específica
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py resultados mlb 2025-06-29

# Obtener resultados del día anterior (automático)
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py resultados

# Interfaz web
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py streamlit
```

### Análisis de Datos
```cmd
# Verificar matching y datos
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python test_matching_29.py

# Pipeline completo (cuando consensus esté corregido)
cd C:\Users\JVILLA\Desktop\predicciones_deportivas
python comandos.py pipeline mlb 2025-06-29
```

---
