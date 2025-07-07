# Recopilador completo para TODO junio 2025
# Incluye consensus y resultados para análisis

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta

def main():
    print("=== RECOPILACION COMPLETA JUNIO 2025 ===")
    print("Obteniendo consensus y resultados para análisis de efectividad")
    
    # Generar todas las fechas de junio 2025
    fechas_junio = []
    fecha_inicio = datetime(2025, 6, 1)
    fecha_fin = datetime(2025, 6, 30)
    
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        fechas_junio.append(fecha_actual.strftime("%Y-%m-%d"))
        fecha_actual += timedelta(days=1)
    
    print(f"Procesando {len(fechas_junio)} fechas de junio 2025...")
    print(f"Desde {fechas_junio[0]} hasta {fechas_junio[-1]}")
    
    # Contadores para estadísticas
    total_consensus_winners = 0
    total_consensus_totals = 0
    total_resultados = 0
    fechas_procesadas = 0
    fechas_con_datos = 0
    
    for fecha in fechas_junio:
        print(f"\n📅 Procesando fecha: {fecha} ({fechas_procesadas + 1}/{len(fechas_junio)})")
        
        try:
            # Importar después de agregar el path
            from sports.mlb.scraper_mlb import MLBScraper
            from sports.mlb.database_mlb import MLBDatabase
            
            scraper = MLBScraper()
            db = MLBDatabase()
            
            fecha_tiene_datos = False
            
            # 1. Obtener Consensus Winners
            print(f"  🏆 Obteniendo consensus winners...")
            consensus_winners = scraper.scrape_consensus(fecha, "winners")
            
            # 2. Obtener Consensus Totals  
            print(f"  🎯 Obteniendo consensus totals...")
            consensus_totals = scraper.scrape_consensus(fecha, "totals")
            
            # 3. Obtener Resultados
            print(f"  📊 Obteniendo resultados...")
            resultados_data = scraper.scrape_results(fecha)
            
            # Procesar datos obtenidos
            if consensus_winners:
                winners_count = len(consensus_winners)
                total_consensus_winners += winners_count
                print(f"    ✅ {winners_count} consensus winners obtenidos")
                fecha_tiene_datos = True
                
            if consensus_totals:
                totals_count = len(consensus_totals)
                total_consensus_totals += totals_count
                print(f"    ✅ {totals_count} consensus totals obtenidos")
                fecha_tiene_datos = True
                
            if resultados_data:
                resultados_count = len(resultados_data)
                total_resultados += resultados_count
                print(f"    ✅ {resultados_count} resultados obtenidos")
                fecha_tiene_datos = True
            
            if fecha_tiene_datos:
                fechas_con_datos += 1
                print(f"  🎉 Fecha {fecha} procesada exitosamente")
            else:
                print(f"  ⚪ Sin datos para {fecha} (normal para días sin partidos)")
                
        except Exception as e:
            print(f"  ❌ Error procesando {fecha}: {str(e)}")
            
        fechas_procesadas += 1
        
        # Mostrar progreso cada 5 fechas
        if fechas_procesadas % 5 == 0:
            print(f"\n📈 PROGRESO: {fechas_procesadas}/{len(fechas_junio)} fechas procesadas")
            print(f"   🏆 Winners: {total_consensus_winners}")
            print(f"   🎯 Totals: {total_consensus_totals}") 
            print(f"   📊 Resultados: {total_resultados}")
    
    # Resumen final
    print("\n" + "="*50)
    print("🎉 RECOPILACIÓN DE JUNIO 2025 COMPLETADA")
    print("="*50)
    print(f"📅 Fechas procesadas: {fechas_procesadas}/{len(fechas_junio)}")
    print(f"📈 Fechas con datos: {fechas_con_datos}")
    print(f"🏆 Total consensus winners: {total_consensus_winners}")
    print(f"🎯 Total consensus totals: {total_consensus_totals}")
    print(f"📊 Total resultados: {total_resultados}")
    print(f"🎯 Total registros recopilados: {total_consensus_winners + total_consensus_totals + total_resultados}")
    print("\n✅ Datos listos para análisis de efectividad")
    print("🔄 Ejecutar: .\\comandos_simple.ps1 -Comando efectividad")

if __name__ == "__main__":
    main()
