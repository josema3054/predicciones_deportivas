-- =====================================
-- COMANDOS SQL PARA SUPABASE
-- =====================================
-- Ejecutar estos comandos en el SQL Editor de Supabase

-- Para la tabla mlb_consensus (Winners/Losers)
ALTER TABLE mlb_consensus ADD COLUMN IF NOT EXISTS puntaje_equipo_1 INTEGER;
ALTER TABLE mlb_consensus ADD COLUMN IF NOT EXISTS puntaje_equipo_2 INTEGER;
ALTER TABLE mlb_consensus ADD COLUMN IF NOT EXISTS ganador_real INTEGER;
ALTER TABLE mlb_consensus ADD COLUMN IF NOT EXISTS efectividad INTEGER;

-- Para la tabla consensus_totals (Over/Under)  
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS puntaje_equipo_1 INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS puntaje_equipo_2 INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS total_real INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS resultado_real INTEGER;
ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS efectividad INTEGER;

-- Verificar que las columnas se agregaron correctamente
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'mlb_consensus' 
ORDER BY ordinal_position;

SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'consensus_totals' 
ORDER BY ordinal_position;
