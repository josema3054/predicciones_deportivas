# 🏆 ESTRUCTURA DE TABLAS POR DEPORTES

## 📊 Nomenclatura de Tablas

### **MLB (Major League Baseball)**
```sql
mlb_consensus_winners    # Pronósticos Winner/Loser
mlb_consensus_totals     # Pronósticos Over/Under  
mlb_results              # Resultados reales
```

### **NBA (National Basketball Association)** - Futuro
```sql
nba_consensus_winners    # Pronósticos Winner/Loser
nba_consensus_totals     # Pronósticos Over/Under
nba_results              # Resultados reales
```

### **NFL (National Football League)** - Futuro
```sql
nfl_consensus_winners    # Pronósticos Winner/Loser  
nfl_consensus_totals     # Pronósticos Over/Under
nfl_results              # Resultados reales
```

### **NHL (National Hockey League)** - Futuro
```sql
nhl_consensus_winners    # Pronósticos Winner/Loser
nhl_consensus_totals     # Pronósticos Over/Under
nhl_results              # Resultados reales
```

## 🎯 Estructura de Datos

### **Consensus Winners** (Pronósticos Winner/Loser)
```sql
CREATE TABLE IF NOT EXISTS {deporte}_consensus_winners (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT '{DEPORTE}',
    equipo_1 VARCHAR(100) NOT NULL,
    equipo_2 VARCHAR(100) NOT NULL,
    equipo_1_sigla VARCHAR(10) NOT NULL,
    equipo_2_sigla VARCHAR(10) NOT NULL,
    fecha_hora VARCHAR(20),
    consensus_equipo_1 VARCHAR(10),
    consensus_equipo_2 VARCHAR(10),
    side_equipo_1 VARCHAR(20),
    side_equipo_2 VARCHAR(20),
    picks_equipo_1 VARCHAR(10),
    picks_equipo_2 VARCHAR(10),
    fecha_scraping VARCHAR(20) NOT NULL,
    
    -- Campos de resultados
    puntaje_equipo_1 INTEGER,
    puntaje_equipo_2 INTEGER,
    ganador_real VARCHAR(10),
    ganador_consensus VARCHAR(10),
    prediccion_correcta BOOLEAN,
    efectividad DECIMAL(5,2),
    estado_partido VARCHAR(20)
);
```

### **Consensus Totals** (Pronósticos Over/Under)
```sql
CREATE TABLE IF NOT EXISTS {deporte}_consensus_totals (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT '{DEPORTE}',
    equipo_1 VARCHAR(100) NOT NULL,
    equipo_2 VARCHAR(100) NOT NULL,
    equipo_1_sigla VARCHAR(10) NOT NULL,
    equipo_2_sigla VARCHAR(10) NOT NULL,
    fecha_hora VARCHAR(20),
    consensus_over VARCHAR(10),
    consensus_under VARCHAR(10),
    picks_over VARCHAR(10),
    picks_under VARCHAR(10),
    linea_total DECIMAL(4,1),
    fecha_scraping VARCHAR(20) NOT NULL,
    
    -- Campos de resultados
    puntaje_equipo_1 INTEGER,
    puntaje_equipo_2 INTEGER,
    total_real INTEGER,
    resultado_total VARCHAR(10), -- 'Over' o 'Under'
    prediccion_correcta BOOLEAN,
    efectividad DECIMAL(5,2)
);
```

### **Results** (Resultados Reales)
```sql
CREATE TABLE IF NOT EXISTS {deporte}_results (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT '{DEPORTE}',
    fecha VARCHAR(20) NOT NULL,
    equipo_local VARCHAR(100) NOT NULL,
    equipo_visitante VARCHAR(100) NOT NULL,
    equipo_local_sigla VARCHAR(10) NOT NULL,
    equipo_visitante_sigla VARCHAR(10) NOT NULL,
    score_local INTEGER NOT NULL,
    score_visitante INTEGER NOT NULL,
    ganador VARCHAR(100) NOT NULL,
    perdedor VARCHAR(100) NOT NULL,
    total_puntos INTEGER NOT NULL,
    fecha_scraping VARCHAR(20) NOT NULL
);
```

## 🚀 Ventajas de Esta Estructura

### **Separación por Deportes**
- Cada deporte tiene sus propias tablas
- Facilita análisis independiente
- Permite optimizaciones específicas

### **Escalabilidad**
- Fácil añadir nuevos deportes
- Estructura consistente
- Nomenclatura clara

### **Análisis**
- Comparación entre deportes
- Estadísticas independientes
- Queries optimizadas

### **Mantenimiento**
- Respaldos independientes
- Limpieza por deporte
- Monitoreo específico

## 📋 Checklist de Implementación

### MLB (Fase 2 - Actual)
- [ ] Crear tabla `mlb_consensus_winners`
- [ ] Crear tabla `mlb_consensus_totals`
- [ ] Crear tabla `mlb_results`
- [ ] Poblar con datos históricos
- [ ] Validar integridad de datos

### NBA (Fase 6 - Futuro)
- [ ] Implementar scraper NBA
- [ ] Crear tabla `nba_consensus_winners`
- [ ] Crear tabla `nba_consensus_totals`
- [ ] Crear tabla `nba_results`

### NFL (Fase 6 - Futuro)
- [ ] Implementar scraper NFL
- [ ] Crear tabla `nfl_consensus_winners`
- [ ] Crear tabla `nfl_consensus_totals`
- [ ] Crear tabla `nfl_results`

## 🎯 Ejemplo de Uso

```python
# Para MLB
mlb_db = MLBDatabase()
mlb_db.save_consensus(data, "winners")  # → mlb_consensus_winners
mlb_db.save_consensus(data, "totals")   # → mlb_consensus_totals
mlb_db.save_results(data)               # → mlb_results

# Para NBA (futuro)
nba_db = NBADatabase()
nba_db.save_consensus(data, "winners")  # → nba_consensus_winners
nba_db.save_consensus(data, "totals")   # → nba_consensus_totals
nba_db.save_results(data)               # → nba_results
```

---

**¡Estructura limpia, escalable y lista para múltiples deportes!** 🏆
