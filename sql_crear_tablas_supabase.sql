🗄️ SQL PARA CREAR TABLAS EN SUPABASE
============================================================

-- ================================
-- TABLAS PARA MLB (FASE 2)
-- ================================

-- 1. Tabla: mlb_consensus_winners
-- Pronósticos Winner/Loser

        CREATE TABLE IF NOT EXISTS mlb_consensus_winners (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            deporte VARCHAR(10) NOT NULL DEFAULT 'MLB',
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
            
            -- Campos de resultados (se llenan después)
            puntaje_equipo_1 INTEGER,
            puntaje_equipo_2 INTEGER,
            ganador_real VARCHAR(10),
            ganador_consensus VARCHAR(10),
            prediccion_correcta BOOLEAN,
            efectividad DECIMAL(5,2),
            estado_partido VARCHAR(20),
            resultado_sigla VARCHAR(10),
            resultado_nombre VARCHAR(100)
        );
        
        -- Índices para optimización
        CREATE INDEX IF NOT EXISTS idx_mlb_consensus_winners_fecha ON mlb_consensus_winners(fecha_scraping);
        CREATE INDEX IF NOT EXISTS idx_mlb_consensus_winners_equipos ON mlb_consensus_winners(equipo_1_sigla, equipo_2_sigla);
        

-- 2. Tabla: mlb_consensus_totals
-- Pronósticos Over/Under

        CREATE TABLE IF NOT EXISTS mlb_consensus_totals (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            deporte VARCHAR(10) NOT NULL DEFAULT 'MLB',
            equipo_1 VARCHAR(100) NOT NULL,
            equipo_2 VARCHAR(100) NOT NULL,
            equipo_1_sigla VARCHAR(10) NOT NULL,
            equipo_2_sigla VARCHAR(10) NOT NULL,
            fecha_hora VARCHAR(20),
            consensus_over VARCHAR(10),
            consensus_under VARCHAR(10),
            side_over VARCHAR(10),
            side_under VARCHAR(10),
            picks_over VARCHAR(10),
            picks_under VARCHAR(10),
            linea_total DECIMAL(4,1),
            fecha_scraping VARCHAR(20) NOT NULL,
            
            -- Campos de resultados (se llenan después)
            puntaje_equipo_1 INTEGER,
            puntaje_equipo_2 INTEGER,
            total_real INTEGER,
            resultado_total VARCHAR(10), -- 'Over' o 'Under'
            prediccion_correcta BOOLEAN,
            efectividad DECIMAL(5,2)
        );
        
        -- Índices para optimización
        CREATE INDEX IF NOT EXISTS idx_mlb_consensus_totals_fecha ON mlb_consensus_totals(fecha_scraping);
        CREATE INDEX IF NOT EXISTS idx_mlb_consensus_totals_equipos ON mlb_consensus_totals(equipo_1_sigla, equipo_2_sigla);
        

-- 3. Tabla: mlb_results
-- Resultados reales

        CREATE TABLE IF NOT EXISTS mlb_results (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            deporte VARCHAR(10) NOT NULL DEFAULT 'MLB',
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
        
        -- Índices para optimización
        CREATE INDEX IF NOT EXISTS idx_mlb_results_fecha ON mlb_results(fecha);
        CREATE INDEX IF NOT EXISTS idx_mlb_results_equipos ON mlb_results(equipo_local_sigla, equipo_visitante_sigla);
        

-- ================================
-- TABLAS PARA NBA (FUTURO)
-- ================================

-- 4. Tabla: nba_consensus_winners
CREATE TABLE IF NOT EXISTS nba_consensus_winners (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT 'NBA',
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

CREATE INDEX IF NOT EXISTS idx_nba_consensus_winners_fecha ON nba_consensus_winners(fecha_scraping);
CREATE INDEX IF NOT EXISTS idx_nba_consensus_winners_equipos ON nba_consensus_winners(equipo_1_sigla, equipo_2_sigla);


-- 5. Tabla: nba_consensus_totals
CREATE TABLE IF NOT EXISTS nba_consensus_totals (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT 'NBA',
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
    resultado_total VARCHAR(10),
    prediccion_correcta BOOLEAN,
    efectividad DECIMAL(5,2)
);

CREATE INDEX IF NOT EXISTS idx_nba_consensus_totals_fecha ON nba_consensus_totals(fecha_scraping);
CREATE INDEX IF NOT EXISTS idx_nba_consensus_totals_equipos ON nba_consensus_totals(equipo_1_sigla, equipo_2_sigla);


-- 6. Tabla: nba_results
CREATE TABLE IF NOT EXISTS nba_results (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT 'NBA',
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

CREATE INDEX IF NOT EXISTS idx_nba_results_fecha ON nba_results(fecha);
CREATE INDEX IF NOT EXISTS idx_nba_results_equipos ON nba_results(equipo_local_sigla, equipo_visitante_sigla);


-- ================================
-- TABLAS PARA NFL (FUTURO)
-- ================================

-- 7. Tabla: nfl_consensus_winners
CREATE TABLE IF NOT EXISTS nfl_consensus_winners (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT 'NFL',
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

CREATE INDEX IF NOT EXISTS idx_nfl_consensus_winners_fecha ON nfl_consensus_winners(fecha_scraping);
CREATE INDEX IF NOT EXISTS idx_nfl_consensus_winners_equipos ON nfl_consensus_winners(equipo_1_sigla, equipo_2_sigla);


-- 8. Tabla: nfl_consensus_totals
CREATE TABLE IF NOT EXISTS nfl_consensus_totals (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT 'NFL',
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
    resultado_total VARCHAR(10),
    prediccion_correcta BOOLEAN,
    efectividad DECIMAL(5,2)
);

CREATE INDEX IF NOT EXISTS idx_nfl_consensus_totals_fecha ON nfl_consensus_totals(fecha_scraping);
CREATE INDEX IF NOT EXISTS idx_nfl_consensus_totals_equipos ON nfl_consensus_totals(equipo_1_sigla, equipo_2_sigla);


-- 9. Tabla: nfl_results
CREATE TABLE IF NOT EXISTS nfl_results (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deporte VARCHAR(10) NOT NULL DEFAULT 'NFL',
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

CREATE INDEX IF NOT EXISTS idx_nfl_results_fecha ON nfl_results(fecha);
CREATE INDEX IF NOT EXISTS idx_nfl_results_equipos ON nfl_results(equipo_local_sigla, equipo_visitante_sigla);


-- ================================
-- INSTRUCCIONES
-- ================================

-- PASOS PARA IMPLEMENTAR:
-- 1. Copiar todo el SQL de arriba
-- 2. Ir a Supabase Dashboard
-- 3. Ir a SQL Editor
-- 4. Pegar el SQL y ejecutar
-- 5. Verificar que las tablas se crearon correctamente
-- 6. Ejecutar script de prueba para poblar datos

-- PARA FASE 2 (AHORA):
-- Solo ejecutar las tablas MLB (1, 2, 3)

-- PARA FASES FUTURAS:
-- Ejecutar tablas NBA/NFL cuando se implementen

