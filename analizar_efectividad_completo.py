#!/usr/bin/env python3
"""
Script para analizar efectividad de predicciones vinculadas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sports.mlb.database_mlb import MLBDatabase
import re

def extraer_porcentaje_from_field(field_value):
    """Extraer porcentaje de un campo de consensus"""
    if not field_value:
        return 0
    
    # Buscar patron "X % Over" o "X % Under" 
    match = re.search(r'(\d+)\s*%', str(field_value))
    if match:
        return int(match.group(1))
    return 0

def analizar_efectividad_predicciones():
    """Analizar efectividad de predicciones vinculadas"""
    print("📊 ANÁLISIS DE EFECTIVIDAD DE PREDICCIONES")
    print("="*70)
    
    # Conectar a la base de datos
    db = MLBDatabase()
    
    # Obtener datos de consensus totals con resultados vinculados
    print("📈 Obteniendo datos de consensus totals con resultados...")
    # Obtener todos los datos y filtrar localmente
    response = db.supabase.table('mlb_consensus_totals').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-08-01').execute()
    all_data = response.data
    
    # Filtrar los que tienen resultados reales
    consensus_data = [record for record in all_data if record['total_real'] is not None]
    
    print(f"✅ Registros con resultados vinculados: {len(consensus_data)}")
    
    if not consensus_data:
        print("❌ No hay datos con resultados vinculados")
        return
    
    # Análisis de efectividad por rango de consensus
    print("\n" + "="*70)
    print("📊 ANÁLISIS DE EFECTIVIDAD POR RANGO DE CONSENSUS")
    print("="*70)
    
    # Rangos de analysis
    rangos = {
        '50-59%': (50, 59),
        '60-69%': (60, 69),
        '70-79%': (70, 79),
        '80-89%': (80, 89),
        '90-100%': (90, 100)
    }
    
    for rango_nombre, (min_pct, max_pct) in rangos.items():
        print(f"\n🎯 RANGO {rango_nombre}:")
        print("-" * 40)
        
        # Filtrar datos por rango
        predicciones_rango = []
        
        for record in consensus_data:
            # CORRECCIÓN: Los campos están invertidos en la base de datos
            # consensus_over contiene "X % Under" 
            # consensus_under contiene "X % Over"
            
            porcentaje_under = extraer_porcentaje_from_field(record['consensus_over'])  # Invertido
            porcentaje_over = extraer_porcentaje_from_field(record['consensus_under'])   # Invertido
            
            # Determinar porcentaje dominante
            if porcentaje_over > porcentaje_under:
                prediccion = 'OVER'
                porcentaje_dominante = porcentaje_over
            else:
                prediccion = 'UNDER'
                porcentaje_dominante = porcentaje_under
            
            # Filtrar por rango
            if min_pct <= porcentaje_dominante <= max_pct:
                predicciones_rango.append({
                    'prediccion': prediccion,
                    'porcentaje': porcentaje_dominante,
                    'resultado_real': record['resultado_total'],
                    'prediccion_correcta': record['prediccion_correcta'],
                    'total_real': record['total_real'],
                    'linea_total': record['linea_total'],
                    'equipo_1': record['equipo_1'],
                    'equipo_2': record['equipo_2'],
                    'fecha': record['fecha_hora']
                })
        
        if predicciones_rango:
            total_predicciones = len(predicciones_rango)
            correctas = sum(1 for p in predicciones_rango if p['prediccion_correcta'])
            efectividad = (correctas / total_predicciones) * 100
            
            # Contar OVER vs UNDER
            over_count = sum(1 for p in predicciones_rango if p['prediccion'] == 'OVER')
            under_count = sum(1 for p in predicciones_rango if p['prediccion'] == 'UNDER')
            
            print(f"📊 Total predicciones: {total_predicciones}")
            print(f"🔺 Predicciones OVER: {over_count}")
            print(f"🔻 Predicciones UNDER: {under_count}")
            print(f"✅ Predicciones correctas: {correctas}")
            print(f"📈 Efectividad: {efectividad:.1f}%")
            
            # Mostrar algunos ejemplos
            print(f"\n📋 Ejemplos (máximo 3):")
            for i, p in enumerate(predicciones_rango[:3]):
                status = "✅" if p['prediccion_correcta'] else "❌"
                print(f"   {i+1}. {status} {p['prediccion']} {p['porcentaje']}% - {p['equipo_1']} vs {p['equipo_2']}")
                print(f"      Línea: {p['linea_total']} | Real: {p['total_real']} | Resultado: {p['resultado_real']}")
        else:
            print("🚫 No hay predicciones en este rango")
    
    # Análisis general
    print("\n" + "="*70)
    print("📊 ANÁLISIS GENERAL")
    print("="*70)
    
    total_predicciones = len(consensus_data)
    correctas_total = sum(1 for p in consensus_data if p['prediccion_correcta'])
    efectividad_total = (correctas_total / total_predicciones) * 100
    
    # Contar OVER vs UNDER en el total
    over_total = 0
    under_total = 0
    
    for record in consensus_data:
        porcentaje_under = extraer_porcentaje_from_field(record['consensus_over'])  # Invertido
        porcentaje_over = extraer_porcentaje_from_field(record['consensus_under'])   # Invertido
        
        if porcentaje_over > porcentaje_under:
            over_total += 1
        else:
            under_total += 1
    
    print(f"📊 Total predicciones analizadas: {total_predicciones}")
    print(f"🔺 Predicciones OVER: {over_total}")
    print(f"🔻 Predicciones UNDER: {under_total}")
    print(f"✅ Predicciones correctas: {correctas_total}")
    print(f"📈 Efectividad general: {efectividad_total:.1f}%")
    
    # Analizar si hay mejores odds para OVER o UNDER
    print("\n🎯 ANÁLISIS DE SESGO EN RESULTADOS:")
    print("-" * 40)
    
    over_reales = sum(1 for p in consensus_data if p['resultado_total'] == 'OVER')
    under_reales = sum(1 for p in consensus_data if p['resultado_total'] == 'UNDER')
    
    print(f"🔺 Resultados reales OVER: {over_reales} ({over_reales/total_predicciones*100:.1f}%)")
    print(f"🔻 Resultados reales UNDER: {under_reales} ({under_reales/total_predicciones*100:.1f}%)")
    
    return efectividad_total

def main():
    """Función principal"""
    print("🎯 ANALIZADOR DE EFECTIVIDAD")
    print("="*70)
    
    try:
        efectividad = analizar_efectividad_predicciones()
        
        print("\n✅ Análisis completado!")
        print(f"🎰 Efectividad general: {efectividad:.1f}%")
        
        if efectividad > 52.38:  # Umbral para superar las casas de apuestas
            print("🎉 ¡Las predicciones superan el umbral de rentabilidad!")
        else:
            print("⚠️ Las predicciones no superan el umbral de rentabilidad")
            
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")

if __name__ == "__main__":
    main()
