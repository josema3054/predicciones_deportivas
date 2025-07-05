# 🏆 Sistema de Análisis de Consensus Deportivo

Sistema completo para scraping, análisis y visualización de datos de consensus de apuestas deportivas desde Covers.com.

## 🚀 Características

- **Scraping automatizado** de consensus Winners/Losers y Over/Under Totals
- **Extracción de resultados reales** de partidos finalizados
- **Análisis cruzado** de efectividad del consensus vs resultados
- **Interfaz web** con Streamlit para gestión completa
- **Almacenamiento** en Supabase + backup CSV automático
- **Prevención de duplicados** inteligente

## 📦 Instalación

> **🖥️ Usuarios de Windows**: Para instrucciones detalladas paso a paso, consultar [GUIA_WINDOWS.md](GUIA_WINDOWS.md)

### 1. Dependencias
```bash
pip install requests beautifulsoup4 selenium pandas supabase python-dotenv streamlit
```

### 2. ChromeDriver (para consensus)
- Descargar desde: https://chromedriver.chromium.org/
- Agregar al PATH del sistema

### 3. Variables de entorno
Crear archivo `.env` con:
```
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_key_de_supabase
```

## 🔧 Uso desde Consola

> **💡 Para usuarios de Windows**: Ver [GUIA_WINDOWS.md](GUIA_WINDOWS.md) para instrucciones paso a paso específicas de Windows.

### Pruebas básicas
```bash
# Verificar instalación y dependencias
python test_simple.py

# Pruebas completas del sistema
python test_resultados.py

# Pruebas rápidas
python comandos.py test
```

### Scraping de resultados
```bash
# Resultados del día anterior (por defecto)
python comandos.py resultados

# Resultados de fecha específica
python comandos.py resultados mlb 2025-06-29

# Otros deportes
python comandos.py resultados cfl 2025-06-29
python comandos.py resultados wnba 2025-06-29
```

### Scraping de consensus
```bash
# Consensus del día anterior
python comandos.py consensus

# Consensus de fecha específica
python comandos.py consensus mlb 2025-06-29
```

### Pipeline completo
```bash
# Ejecuta todo: consensus + resultados + análisis
python comandos.py pipeline mlb 2025-06-29
```

### Análisis de efectividad
```bash
# Solo análisis (requiere datos previos)
python comandos.py analisis mlb 2025-06-29
```

### Interfaz web
```bash
# Lanzar Streamlit
python comandos.py streamlit
# O directamente:
streamlit run app_streamlit.py
```

## 🗄️ Estructura de Datos

### Arquitectura Unificada
El sistema utiliza una arquitectura unificada donde **cada fila contiene tanto el consensus/pronóstico como el resultado real y su efectividad**. No hay tablas separadas para resultados.

### Tablas en Supabase

#### `mlb_consensus` - Winners/Losers
```sql
CREATE TABLE mlb_consensus (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    equipo_local VARCHAR,
    equipo_visitante VARCHAR,
    consensus_local INTEGER,
    consensus_visitante INTEGER,
    favorito VARCHAR,
    underdog VARCHAR,
    spread_favorito DECIMAL,
    
    -- Columnas de resultados reales (agregadas automáticamente)
    resultado_ganador VARCHAR,           -- Equipo que ganó el partido
    favorito_gano BOOLEAN,              -- Si el favorito ganó
    consensus_correcto BOOLEAN,         -- Si el consensus fue correcto
    diferencia_puntos INTEGER,          -- Diferencia real de puntos
    spread_cubierto BOOLEAN,           -- Si el spread se cubrió
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### `consensus_totals` - Over/Under
```sql
CREATE TABLE consensus_totals (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    equipo_local VARCHAR,
    equipo_visitante VARCHAR,
    total_line DECIMAL,
    consensus_over INTEGER,
    consensus_under INTEGER,
    
    -- Columnas de resultados reales (agregadas automáticamente)
    puntos_totales INTEGER,            -- Puntos totales del partido
    resultado_total VARCHAR,           -- 'Over' o 'Under'
    consensus_total_correcto BOOLEAN,  -- Si el consensus de totales fue correcto
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Flujo de Datos

1. **Scraping de Consensus**: Se extraen los datos de consensus y se guardan en las tablas correspondientes
2. **Scraping de Resultados**: Los resultados reales se actualizan directamente en las mismas filas de consensus
3. **Análisis Automático**: Se calcula la efectividad del consensus vs resultados en tiempo real

### Ventajas de esta Estructura

- ✅ **Datos completos en una sola consulta**: No necesitas JOIN entre tablas
- ✅ **Análisis directo**: Cada fila tiene consensus + resultado + efectividad
- ✅ **Prevención de duplicados**: Una fila por partido por tipo de apuesta
- ✅ **Flexibilidad**: Fácil agregar nuevas métricas de análisis

## 📊 Ejemplos de Análisis

### Consultas SQL Útiles

```sql
-- Efectividad general del consensus Winners/Losers
SELECT 
    fecha,
    COUNT(*) as total_partidos,
    SUM(CASE WHEN consensus_correcto THEN 1 ELSE 0 END) as aciertos,
    ROUND(AVG(CASE WHEN consensus_correcto THEN 1.0 ELSE 0.0 END) * 100, 2) as porcentaje_efectividad
FROM mlb_consensus 
WHERE consensus_correcto IS NOT NULL
GROUP BY fecha
ORDER BY fecha DESC;

-- Efectividad del consensus Over/Under
SELECT 
    fecha,
    COUNT(*) as total_partidos,
    SUM(CASE WHEN consensus_total_correcto THEN 1 ELSE 0 END) as aciertos,
    ROUND(AVG(CASE WHEN consensus_total_correcto THEN 1.0 ELSE 0.0 END) * 100, 2) as porcentaje_efectividad
FROM consensus_totals 
WHERE consensus_total_correcto IS NOT NULL
GROUP BY fecha
ORDER BY fecha DESC;

-- Análisis por equipo (como favorito)
SELECT 
    favorito,
    COUNT(*) as veces_favorito,
    SUM(CASE WHEN favorito_gano THEN 1 ELSE 0 END) as ganadas_como_favorito,
    ROUND(AVG(CASE WHEN favorito_gano THEN 1.0 ELSE 0.0 END) * 100, 2) as porcentaje_ganadas
FROM mlb_consensus 
WHERE favorito_gano IS NOT NULL
GROUP BY favorito
ORDER BY veces_favorito DESC;
```

### Análisis con Python

```python
import pandas as pd
from supabase import create_client

# Cargar datos de consensus con resultados
df_consensus = supabase.table('mlb_consensus').select('*').eq('fecha', '2025-06-29').execute()
df_totals = supabase.table('consensus_totals').select('*').eq('fecha', '2025-06-29').execute()

# Efectividad del día
consensus_efectividad = df_consensus.data['consensus_correcto'].mean() * 100
totals_efectividad = df_totals.data['consensus_total_correcto'].mean() * 100

print(f"Efectividad Winners/Losers: {consensus_efectividad:.1f}%")
print(f"Efectividad Over/Under: {totals_efectividad:.1f}%")
```

## 📁 Archivos del Proyecto

### Scripts Principales
- **`scraper_historico.py`**: Motor principal del sistema con todas las funciones de scraping, análisis y manejo de datos
- **`app_streamlit.py`**: Interfaz web completa para gestión del sistema
- **`equipos_data.py`**: Diccionario de equivalencias de nombres/siglas de equipos
- **`comandos.py`**: CLI para ejecutar todas las funciones desde línea de comandos

### Scripts de Prueba
- **`test_simple.py`**: Verificación básica de dependencias y conexiones
- **`test_resultados.py`**: Pruebas completas del sistema de scraping
- **`test_db.py`**: Pruebas específicas de base de datos
- **`test_insert.py`**: Pruebas de inserción de datos

### Archivos de Configuración
- **`requirements.txt`**: Dependencias de Python
- **`.env`**: Variables de entorno (crear manualmente)
- **`README.md`**: Esta documentación

### Datos
- **`mlb_consensus_*.csv`**: Backups automáticos de consensus por fecha
- **`mlb_consensus_totals_*.csv`**: Backups automáticos de totales por fecha

## 🔧 Migración de Datos (Solo si es necesario)

Si tienes tablas existentes sin las columnas de resultados, el sistema las agregará automáticamente. También puedes hacerlo manualmente:

```sql
-- Agregar columnas de resultados a mlb_consensus existente
ALTER TABLE mlb_consensus 
ADD COLUMN IF NOT EXISTS resultado_ganador VARCHAR,
ADD COLUMN IF NOT EXISTS favorito_gano BOOLEAN,
ADD COLUMN IF NOT EXISTS consensus_correcto BOOLEAN,
ADD COLUMN IF NOT EXISTS diferencia_puntos INTEGER,
ADD COLUMN IF NOT EXISTS spread_cubierto BOOLEAN;

-- Agregar columnas de resultados a consensus_totals existente
ALTER TABLE consensus_totals 
ADD COLUMN IF NOT EXISTS puntos_totales INTEGER,
ADD COLUMN IF NOT EXISTS resultado_total VARCHAR,
ADD COLUMN IF NOT EXISTS consensus_total_correcto BOOLEAN;
```

## 🐛 Troubleshooting

### Errores Comunes

#### Windows: Comandos no reconocidos
```bash
# Asegúrate de estar en el directorio correcto
cd C:\Users\JVILLA\Desktop\predicciones_deportivas

# Luego ejecuta el comando
python comandos.py test
```

#### ChromeDriver no encontrado
```bash
# Descargar ChromeDriver y agregar al PATH
# O instalar via chocolatey (Windows):
choco install chromedriver
```

#### Error de conexión a Supabase
```bash
# Verificar variables de entorno
python -c "import os; print(os.getenv('SUPABASE_URL')); print(os.getenv('SUPABASE_KEY'))"

# Probar conexión
python test_simple.py
```

#### Datos duplicados
```bash
# El sistema previene duplicados automáticamente
# Para forzar actualización:
python comandos.py resultados mlb 2025-06-29 --force
```

#### Partidos no encontrados
```bash
# Verificar formato de fecha (YYYY-MM-DD)
# Verificar que haya partidos en esa fecha
# Probar con scraping de consensus primero
```

### Logs y Debug

El sistema incluye logging detallado. Para ver más información:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Próximos Pasos

### Mejoras Planificadas
- [ ] Soporte para más deportes (NFL, NBA, etc.)
- [ ] Análisis avanzados de tendencias y patrones
- [ ] Alertas automáticas por email/Slack
- [ ] API REST para integración externa
- [ ] Dashboard avanzado con métricas en tiempo real

### Extensiones Posibles
- [ ] Machine Learning para predicciones mejoradas
- [ ] Integración con APIs de casas de apuestas
- [ ] Análisis de sharp money vs public money
- [ ] Tracking de line movements
- [ ] Análisis de weather conditions

## 📞 Soporte

### Reportar Issues
- Usar `test_simple.py` para diagnóstico básico
- Incluir logs completos al reportar problemas
- Verificar dependencias y variables de entorno

### Contribuciones
- Fork del proyecto
- Crear feature branch
- Submit pull request con descripción detallada

---

**Desarrollado con ❤️ para análisis deportivo automatizado**

