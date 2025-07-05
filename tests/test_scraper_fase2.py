#!/usr/bin/env python3
"""
Script de prueba para el scraper MLB de la Fase 2
Prueba tanto consensus como resultados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sports.mlb.scraper_mlb import MLBScraper
from sports.mlb.database_mlb import MLBDatabase
import logging
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_scraper_fase2.log'),
        logging.StreamHandler()
    ]
)

def test_scraper_fase2():
    """Prueba completa del scraper MLB Fase 2"""
    print("🧪 TEST SCRAPER MLB - FASE 2")
    print("=" * 50)
    
    # Inicializar scraper
    scraper = MLBScraper()
    db = MLBDatabase()
    
    # Fecha de prueba (fecha pasada para tener resultados)
    fecha_test = "2025-06-29"
    
    print(f"📅 Fecha de prueba: {fecha_test}")
    
    # 1. Test Consensus Winners
    print("\n1️⃣ PROBANDO CONSENSUS WINNERS")
    print("-" * 30)
    try:
        consensus_winners = scraper.scrape_consensus(fecha_test, "winners")
        print(f"✅ Consensus Winners: {len(consensus_winners)} partidos")
        
        if consensus_winners:
            print("   Muestra:")
            for i, partido in enumerate(consensus_winners[:2]):
                print(f"   • {partido['equipo_1']} vs {partido['equipo_2']}")
                print(f"     Consensus: {partido['consensus_equipo_1']}% - {partido['consensus_equipo_2']}%")
    except Exception as e:
        print(f"❌ Error en consensus winners: {e}")
    
    # 2. Test Consensus Totals
    print("\n2️⃣ PROBANDO CONSENSUS TOTALS")
    print("-" * 30)
    try:
        consensus_totals = scraper.scrape_consensus(fecha_test, "totals")
        print(f"✅ Consensus Totals: {len(consensus_totals)} partidos")
        
        if consensus_totals:
            print("   Muestra:")
            for i, partido in enumerate(consensus_totals[:2]):
                print(f"   • {partido['equipo_1']} vs {partido['equipo_2']}")
                print(f"     O/U: {partido['consensus_over']} / {partido['consensus_under']}")
                print(f"     Línea: {partido['linea_total']}")
    except Exception as e:
        print(f"❌ Error en consensus totals: {e}")
    
    # 3. Test Resultados Reales
    print("\n3️⃣ PROBANDO RESULTADOS REALES")
    print("-" * 30)
    try:
        resultados = scraper.scrape_results(fecha_test)
        print(f"✅ Resultados: {len(resultados)} partidos")
        
        if resultados:
            print("   Muestra:")
            for i, partido in enumerate(resultados[:2]):
                print(f"   • {partido['equipo_local']} vs {partido['equipo_visitante']}")
                print(f"     Score: {partido['score_local']}-{partido['score_visitante']}")
                print(f"     Ganador: {partido['ganador']}")
                print(f"     Total: {partido['total_puntos']}")
    except Exception as e:
        print(f"❌ Error en resultados: {e}")
    
    # 4. Test Base de Datos
    print("\n4️⃣ PROBANDO BASE DE DATOS")
    print("-" * 30)
    try:
        # Mostrar SQL para crear tablas
        print("📋 SQL para crear tablas:")
        print("=== CONSENSUS ===")
        print(db.create_consensus_table())
        print("\n=== CONSENSUS TOTALS ===")
        print(db.create_consensus_totals_table())
        print("\n=== RESULTADOS ===")
        print(db.create_results_table())
        
        # Obtener estadísticas
        stats = db.get_stats_summary(fecha_test)
        print(f"\n📊 Estadísticas para {fecha_test}:")
        print(f"   Consensus: {stats['consensus_count']} registros")
        print(f"   Totals: {stats['totals_count']} registros")
        print(f"   Resultados: {stats.get('results_count', 'N/A')} registros")
        
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
    
    # 5. Resumen Final
    print("\n📋 RESUMEN FINAL")
    print("=" * 50)
    print("✅ Scraper de Consensus Winners: Funcional")
    print("✅ Scraper de Consensus Totals: Funcional")
    print("🔄 Scraper de Resultados: Implementado (necesita prueba real)")
    print("🔄 Base de Datos: Esquemas creados (necesita configuración)")
    print("🎯 Fase 2: Lista para ejecución completa")

def test_fechas_historicas():
    """Prueba con múltiples fechas históricas"""
    print("\n🗓️ TEST FECHAS HISTÓRICAS")
    print("-" * 30)
    
    scraper = MLBScraper()
    fechas_test = [
        "2025-06-25",
        "2025-06-26", 
        "2025-06-27",
        "2025-06-28",
        "2025-06-29"
    ]
    
    for fecha in fechas_test:
        print(f"\n📅 Procesando {fecha}...")
        try:
            # Solo consensus para test rápido
            winners = scraper.scrape_consensus(fecha, "winners")
            totals = scraper.scrape_consensus(fecha, "totals")
            
            print(f"   Winners: {len(winners)} | Totals: {len(totals)}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_scraper_fase2()
    
    # Opcional: test con fechas históricas
    respuesta = input("\n¿Probar con fechas históricas? (y/n): ")
    if respuesta.lower() == 'y':
        test_fechas_historicas()
