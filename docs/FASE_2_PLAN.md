# 🚀 FASE 2 - SCRAPING DE DATOS COMPLETOS

## 🎯 Objetivo Principal
Obtener y guardar todos los datos históricos necesarios para el análisis posterior (Fase 3).

## 📋 Tareas Específicas

### 1. **Scraping de Consensus** ✅ (Ya funcional)
- Winner/Loser predictions
- Totals (Over/Under) predictions
- Datos de líderes/expertos
- Fechas y equipos

### 2. **Scraping de Resultados Reales** 🔴 (Por arreglar)
- **Winner/Loser reales**: Qué equipo ganó
- **Totales reales**: Puntaje final total
- **Scores individuales**: Puntaje por equipo
- **Fechas exactas**: Sincronización con consensus

### 3. **Estructura de Base de Datos**
```
databases/
├── mlb/
│   ├── consensus_mlb.db
│   │   ├── winners_consensus     # Predicciones Winner/Loser
│   │   └── totals_consensus      # Predicciones Over/Under
│   ├── results_mlb.db
│   │   ├── winners_results       # Resultados Winner/Loser
│   │   ├── totals_results        # Resultados Over/Under
│   │   └── scores_results        # Puntajes individuales
│   └── teams_mlb.db
│       └── teams_info            # Información de equipos
```

### 4. **Validación de Datos**
- Verificar coincidencia de fechas
- Validar nombres de equipos
- Confirmar integridad de datos
- Exportar CSVs para revisión

### 5. **Interfaz de Control**
- Ejecutar scraping manual
- Monitorear estado de datos
- Validar información capturada
- Exportar para análisis

## 🔧 Archivos a Trabajar

### Scrapers
- `sports/mlb/scraper_mlb.py` - Arreglar scraping de resultados
- `scripts/mlb_main.py` - Coordinar scraping completo

### Base de Datos
- `sports/mlb/database_mlb.py` - Actualizar esquemas
- `scripts/actualizar_resultados_supabase.py` - Revisar y corregir

### Tests y Validación
- `tests/debug_selenium_resultados.py` - Debugging
- `tests/diagnostico_resultados.py` - Validación

### Interfaz
- `scripts/app_streamlit.py` - Controles para scraping

## 📊 Datos a Capturar

### Consensus Data
```python
{
    "fecha": "2025-07-05",
    "equipo_local": "Yankees",
    "equipo_visitante": "Red Sox",
    "winner_consensus": "Yankees",
    "winner_confidence": 65,
    "total_consensus": "Over",
    "total_line": 8.5,
    "total_confidence": 72
}
```

### Results Data
```python
{
    "fecha": "2025-07-05",
    "equipo_local": "Yankees",
    "equipo_visitante": "Red Sox",
    "score_local": 7,
    "score_visitante": 4,
    "winner_real": "Yankees",
    "total_real": 11,
    "over_under_result": "Over"
}
```

## 🎯 Criterios de Éxito

### Datos Completos
- [ ] Consensus histórico de Winner/Loser
- [ ] Consensus histórico de Totales
- [ ] Resultados reales de Winner/Loser
- [ ] Resultados reales de Totales
- [ ] Puntajes individuales

### Calidad de Datos
- [ ] Fechas sincronizadas
- [ ] Nombres de equipos consistentes
- [ ] Sin datos faltantes
- [ ] Exportación CSV exitosa

### Funcionalidad
- [ ] Scraper de consensus funcional
- [ ] Scraper de resultados funcional
- [ ] Base de datos poblada
- [ ] Interfaz de control operativa

## 🚀 Plan de Ejecución

### Paso 1: Revisar Scraper Actual
- Analizar `sports/mlb/scraper_mlb.py`
- Identificar problemas en scraping de resultados
- Actualizar selectores CSS/XPath si es necesario

### Paso 2: Arreglar Scraping de Resultados
- Implementar captura de Winner/Loser reales
- Implementar captura de Totales reales
- Manejar errores robustamente

### Paso 3: Actualizar Base de Datos
- Crear/actualizar esquemas de tablas
- Implementar inserción de datos
- Validar integridad referencial

### Paso 4: Ejecutar Scraping Histórico
- Ejecutar 1-2 veces para obtener datos históricos
- Validar calidad de datos
- Exportar para revisión

### Paso 5: Preparar para Fase 3
- Documentar estructura de datos
- Crear scripts de validación
- Preparar datos para análisis

## 🎉 Resultado Final

Al completar la Fase 2 tendremos:
- **Base de datos histórica completa** con consensus y resultados
- **Datos validados y limpios** listos para análisis
- **Sistema de scraping robusto** para Winner/Loser y Totales
- **Fundación sólida** para la Fase 3 (Análisis de Patrones)

---

**¡Vamos a construir la base de datos más completa para análisis deportivo!** 🏆
