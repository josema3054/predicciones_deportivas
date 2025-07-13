#!/usr/bin/env python3
"""
Recopilador SOLO para TOTALS + RESULTADOS
Versión simplificada que solo captura lo que necesitas para el simulador
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta

def main():
    print("=== RECOPILACION SOLO TOTALS + RESULTADOS ===")
    print("Versión optimizada para simulador de apuestas")
    print("="*50)
    
    # Generar todas las fechas de junio 2025
    fechas_junio = []
    fecha_inicio = datetime(2025, 6, 1)
    fecha_fin = datetime(2025, 6, 30)
    
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        fechas_junio.append(fecha_actual.strftime("%Y-%m-%d"))
        fecha_actual += timedelta(days=1)
    
    print(f"📅 Procesando {len(fechas_junio)} fechas de junio 2025")
    print(f"🎯 Solo recopilando: CONSENSUS TOTALS + RESULTADOS")
    print(f"📊 Desde {fechas_junio[0]} hasta {fechas_junio[-1]}")
    
    # Contadores para estadísticas
    total_consensus_totals = 0
    total_resultados = 0
    fechas_procesadas = 0
    fechas_con_datos = 0
    errores = 0
    
    for fecha in fechas_junio:
        print(f"\n📅 Procesando: {fecha} ({fechas_procesadas + 1}/{len(fechas_junio)})")
        
        try:
            # Importar después de agregar el path
            from sports.mlb.scraper_mlb import MLBScraper
            from sports.mlb.database_mlb import MLBDatabase
            
            scraper = MLBScraper()
            db = MLBDatabase()
            
            fecha_tiene_datos = False
            
            # 1. SOLO Obtener Consensus Totals  
            print(f"  🎯 Obteniendo consensus totals...")
            consensus_totals = scraper.scrape_consensus(fecha, "totals")
            
            # 2. SOLO Obtener Resultados
            print(f"  📊 Obteniendo resultados...")
            resultados_data = scraper.scrape_results(fecha)
            
            # Procesar datos obtenidos
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
                print(f"  ⚪ Sin datos para {fecha}")
                
        except Exception as e:
            print(f"  ❌ Error procesando {fecha}: {str(e)}")
            errores += 1
            
        fechas_procesadas += 1
        
        # Mostrar progreso cada 5 fechas
        if fechas_procesadas % 5 == 0:
            print(f"\n📈 PROGRESO: {fechas_procesadas}/{len(fechas_junio)} fechas")
            print(f"   🎯 Totals: {total_consensus_totals}") 
            print(f"   📊 Resultados: {total_resultados}")
            print(f"   ❌ Errores: {errores}")
    
    # Resumen final
    print("\n" + "="*50)
    print("🎉 RECOPILACIÓN TOTALS + RESULTADOS COMPLETADA")
    print("="*50)
    print(f"📅 Fechas procesadas: {fechas_procesadas}/{len(fechas_junio)}")
    print(f"📈 Fechas con datos: {fechas_con_datos}")
    print(f"🎯 Total consensus totals: {total_consensus_totals}")
    print(f"📊 Total resultados: {total_resultados}")
    print(f"❌ Errores encontrados: {errores}")
    print(f"🎯 Total registros recopilados: {total_consensus_totals + total_resultados}")
    
    if total_consensus_totals > 0 and total_resultados > 0:
        print("\n✅ Datos listos para simulador de apuestas")
        print("🔄 Para calcular efectividad:")
        print("   .\\comandos_simple.ps1 -Comando efectividad")
        print("🎰 Para usar simulador:")
        print("   .\\comandos_simple.ps1 -Comando simulador")
    else:
        print("\n⚠️  Datos insuficientes para simulador")
        print("   Verificar conexión a internet y reintentar")

if __name__ == "__main__":
    main()
