#!/usr/bin/env python3
"""
Gestión de base de datos específica para MLB
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base import BaseDatabase
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class MLBDatabase(BaseDatabase):
    """Gestor de base de datos específico para MLB"""
    
    def __init__(self):
        super().__init__("mlb")
        self.tables = {
            'consensus': 'mlb_consensus_winners',
            'consensus_totals': 'mlb_consensus_totals', 
            'results': 'mlb_results'
        }
    
    def save_consensus(self, data: List[Dict[str, Any]], tipo: str = "winners") -> bool:
        """Guardar datos de consensus en la base de datos"""
        if not data:
            logger.warning("No hay datos de consensus para guardar")
            return False
        
        tabla = self.tables['consensus'] if tipo == "winners" else self.tables['consensus_totals']
        saved_count = 0
        
        try:
            for partido in data:
                # Verificar duplicados
                if not self.check_duplicates(partido, tabla):
                    # Normalizar deporte a mayúsculas
                    partido_normalized = partido.copy()
                    partido_normalized['deporte'] = partido_normalized.get('deporte', 'MLB').upper()
                    
                    self.supabase.table(tabla).insert(partido_normalized).execute()
                    saved_count += 1
                    logger.info(f"✅ Guardado: {partido.get('equipo_1')} vs {partido.get('equipo_2')}")
                else:
                    logger.info(f"🔄 Duplicado omitido: {partido.get('equipo_1')} vs {partido.get('equipo_2')}")
            
            logger.info(f"💾 {saved_count} registros guardados en {tabla}")
            return saved_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error al guardar consensus: {e}")
            return False
    
    def save_results(self, data: List[Dict[str, Any]]) -> bool:
        """Guardar resultados reales"""
        if not data:
            logger.warning("No hay datos de resultados para guardar")
            return False
        
        # Agregar tabla de resultados
        if 'results' not in self.tables:
            self.tables['results'] = 'mlb_results'
        
        saved_count = 0
        
        try:
            for resultado in data:
                # Verificar duplicados
                if not self.check_result_duplicates(resultado):
                    # Normalizar deporte a mayúsculas
                    resultado_normalized = resultado.copy()
                    resultado_normalized['deporte'] = resultado_normalized.get('deporte', 'MLB').upper()
                    
                    self.supabase.table(self.tables['results']).insert(resultado_normalized).execute()
                    saved_count += 1
                    logger.info(f"✅ Resultado guardado: {resultado.get('equipo_local')} vs {resultado.get('equipo_visitante')}")
                else:
                    logger.info(f"🔄 Resultado duplicado omitido: {resultado.get('equipo_local')} vs {resultado.get('equipo_visitante')}")
            
            logger.info(f"💾 {saved_count} resultados guardados en {self.tables['results']}")
            return saved_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error al guardar resultados: {e}")
            return False
    
    def check_result_duplicates(self, data: Dict[str, Any]) -> bool:
        """Verificar si ya existe un resultado con los mismos datos"""
        try:
            deporte_upper = data.get('deporte', 'MLB').upper()
            equipo_local_sigla = data.get('equipo_local_sigla')
            equipo_visitante_sigla = data.get('equipo_visitante_sigla')
            fecha = data.get('fecha')
            
            if not all([equipo_local_sigla, equipo_visitante_sigla, fecha]):
                return False
            
            existing = self.supabase.table(self.tables['results']).select("id").eq("deporte", deporte_upper).eq("equipo_local_sigla", equipo_local_sigla).eq("equipo_visitante_sigla", equipo_visitante_sigla).eq("fecha", fecha).execute()
            
            return len(existing.data) > 0
        except Exception as e:
            logger.error(f"❌ Error al verificar duplicados de resultados: {e}")
            return False
    
    def check_duplicates(self, data: Dict[str, Any], tabla: str) -> bool:
        """Verificar si ya existe un registro con los mismos datos"""
        try:
            deporte_upper = data.get('deporte', 'MLB').upper()
            equipo_1_sigla = data.get('equipo_1_sigla')
            equipo_2_sigla = data.get('equipo_2_sigla')
            fecha_scraping = data.get('fecha_scraping')
            
            if not all([equipo_1_sigla, equipo_2_sigla, fecha_scraping]):
                return False
            
            existing = self.supabase.table(tabla).select("id").eq("deporte", deporte_upper).eq("equipo_1_sigla", equipo_1_sigla).eq("equipo_2_sigla", equipo_2_sigla).eq("fecha_scraping", fecha_scraping).execute()
            
            return len(existing.data) > 0
        except Exception as e:
            logger.error(f"❌ Error al verificar duplicados: {e}")
            return False
    
    def create_consensus_table(self):
        """
        SQL para crear tabla de consensus Winners/Losers - MLB
        NOTA: Ejecutar manualmente en Supabase si no existe
        """
        sql = """
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
        """
        return sql
    
    def create_consensus_totals_table(self):
        """
        SQL para crear tabla de consensus Over/Under - MLB
        NOTA: Ejecutar manualmente en Supabase si no existe
        """
        sql = """
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
        """
        return sql
    
    def create_results_table(self):
        """
        SQL para crear tabla de resultados reales - MLB
        NOTA: Ejecutar manualmente en Supabase si no existe
        """
        sql = """
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
        """
        return sql
    
    def get_results_by_date(self, date_str):
        """Obtener resultados reales por fecha"""
        try:
            response = self.supabase.table(self.tables['results']).select("*").eq('fecha', date_str).execute()
            return response.data
        except Exception as e:
            logger.error(f"❌ Error obteniendo resultados por fecha: {e}")
            return []
    
    def get_consensus_by_date(self, date_str):
        """Obtener consensus Winners/Losers por fecha"""
        try:
            response = self.supabase.table(self.tables['consensus']).select("*").eq('fecha_scraping', date_str).execute()
            return response.data
        except Exception as e:
            logger.error(f"❌ Error obteniendo consensus por fecha: {e}")
            return []
    
    def get_consensus_totals_by_date(self, date_str):
        """Obtener consensus Totals por fecha"""
        try:
            response = self.supabase.table(self.tables['consensus_totals']).select("*").eq('fecha_scraping', date_str).execute()
            return response.data
        except Exception as e:
            logger.error(f"❌ Error obteniendo consensus totals por fecha: {e}")
            return []
    
    def update_consensus_with_results(self, consensus_id, puntaje_1, puntaje_2, ganador_real):
        """Actualizar registro de consensus con resultados"""
        client = self.db_manager.get_client()
        
        update_data = {
            'puntaje_equipo_1': puntaje_1,
            'puntaje_equipo_2': puntaje_2,
            'ganador_real': ganador_real,
            'estado_partido': 'FINAL'
        }
        
        response = client.table(self.tables['consensus']).update(update_data).eq('id', consensus_id).execute()
        return response.data
    
    def update_totals_with_results(self, totals_id, puntaje_1, puntaje_2, total_real):
        """Actualizar registro de totals con resultados"""
        client = self.db_manager.get_client()
        
        update_data = {
            'puntaje_equipo_1': puntaje_1,
            'puntaje_equipo_2': puntaje_2,
            'total_real': total_real
        }
        
        response = client.table(self.tables['consensus_totals']).update(update_data).eq('id', totals_id).execute()
        return response.data
    
    def clear_table(self, table_type):
        """Limpiar tabla específica"""
        client = self.db_manager.get_client()
        
        table_name = self.tables.get(table_type)
        if not table_name:
            raise ValueError(f"Tipo de tabla desconocido: {table_type}")
        
        # Obtener count antes de eliminar
        count_response = client.table(table_name).select("id").execute()
        initial_count = len(count_response.data)
        
        if initial_count == 0:
            return 0
        
        # Eliminar todos los registros
        delete_response = client.table(table_name).delete().neq('id', -999999).execute()
        
        return initial_count
    
    def verify_table_exists(self, table_name: str) -> bool:
        """Verificar si una tabla existe"""
        try:
            # Intentar hacer una consulta simple
            response = self.supabase.table(table_name).select("id").limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"❌ Tabla {table_name} no existe: {e}")
            return False
    
    def get_table_structure(self, table_name: str) -> List[str]:
        """Obtener estructura de una tabla"""
        try:
            # Obtener un registro para ver la estructura
            response = self.supabase.table(table_name).select("*").limit(1).execute()
            if response.data:
                return list(response.data[0].keys())
            return []
        except Exception as e:
            logger.error(f"❌ Error obteniendo estructura de {table_name}: {e}")
            return []
    
    def get_stats_summary(self, fecha: str) -> Dict[str, Any]:
        """Obtener resumen de estadísticas para una fecha"""
        try:
            # Obtener datos de consensus
            consensus_response = self.supabase.table(self.tables['consensus']).select("*").eq('fecha_scraping', fecha).execute()
            consensus_data = consensus_response.data
            
            # Obtener datos de totals
            totals_response = self.supabase.table(self.tables['consensus_totals']).select("*").eq('fecha_scraping', fecha).execute()
            totals_data = totals_response.data
            
            return {
                'fecha': fecha,
                'consensus_count': len(consensus_data),
                'totals_count': len(totals_data),
                'consensus_with_results': len([c for c in consensus_data if c.get('puntaje_equipo_1') is not None]),
                'totals_with_results': len([t for t in totals_data if t.get('total_real') is not None])
            }
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas: {e}")
            return {
                'fecha': fecha,
                'consensus_count': 0,
                'totals_count': 0,
                'consensus_with_results': 0,
                'totals_with_results': 0
            }

def main():
    """Función principal para testing"""
    db = MLBDatabase()
    
    print("📊 SQL para crear tablas:")
    print("=== CONSENSUS ===")
    print(db.create_consensus_table())
    print("\n=== CONSENSUS TOTALS ===")
    print(db.create_consensus_totals_table())
    print("\n=== RESULTADOS ===")
    print(db.create_results_table())
    
    # Test de conexión
    try:
        stats = db.get_stats_summary('2025-06-29')
        print(f"\n🧪 Test de conexión exitoso:")
        print(f"Stats para 2025-06-29: {stats}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    main()
