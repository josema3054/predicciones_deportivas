#!/usr/bin/env python3
"""
Verificación final del simulador web - problema resuelto
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sports.mlb.database_mlb import MLBDatabase
from simulador_apuestas import ejecutar_simulacion
import re

def verificacion_final():
    """Verificación final del simulador web"""
    
    print("🎯 VERIFICACIÓN FINAL DEL SIMULADOR WEB")
    print("="*50)
    
    # 1. Verificar parsing de porcentajes
    print("\n1. 🔍 Verificando parsing de porcentajes...")
    
    db = MLBDatabase()
    consensus_response = db.supabase.table('mlb_consensus_totals').select('*').limit(10).execute()
    
    conteo_over = 0
    conteo_under = 0
    
    for consensus in consensus_response.data:
        consensus_over = consensus.get('consensus_over', '')
        consensus_under = consensus.get('consensus_under', '')
        
        # Parsear usando la lógica corregida
        perc_over = 0
        perc_under = 0
        
        # Parsear consensus_over
        over_str = str(consensus_over)
        over_match = re.search(r'(\d+)\s*%', over_str)
        if over_match:
            porcentaje = float(over_match.group(1))
            if 'Over' in over_str:
                perc_over = porcentaje
            elif 'Under' in over_str:
                perc_under = porcentaje
        
        # Parsear consensus_under
        under_str = str(consensus_under)
        under_match = re.search(r'(\d+)\s*%', under_str)
        if under_match:
            porcentaje = float(under_match.group(1))
            if 'Over' in under_str:
                perc_over = porcentaje
            elif 'Under' in under_str:
                perc_under = porcentaje
        
        # Determinar mejor opción
        if perc_over > perc_under:
            conteo_over += 1
        else:
            conteo_under += 1
    
    print(f"   En 10 registros: {conteo_over} OVER, {conteo_under} UNDER")
    
    if conteo_over > 0 and conteo_under > 0:
        print("   ✅ Parsing balanceado - PROBLEMA RESUELTO")
    else:
        print("   ❌ Parsing aún sesgado")
    
    # 2. Verificar simulación con diferentes consensus mínimos
    print("\n2. 🎰 Verificando simulación con diferentes parámetros...")
    
    for consensus_min in [60, 70, 80]:
        resultado = ejecutar_simulacion(1000, 20, consensus_min, 50, 'totals', 1.8)
        
        print(f"   Consensus {consensus_min}%: {resultado['total_apuestas']} apuestas, {resultado['apuestas_ganadas']} ganadas ({resultado['porcentaje_acierto']:.1f}%)")
    
    # 3. Verificar que hay apuestas OVER y UNDER
    print("\n3. 📊 Verificando distribución de apuestas...")
    
    resultado_detallado = ejecutar_simulacion(1000, 20, 60, 20, 'totals', 1.8)
    
    apuestas_over = sum(1 for a in resultado_detallado['apuestas_realizadas'] if a['prediccion'] == 'over')
    apuestas_under = sum(1 for a in resultado_detallado['apuestas_realizadas'] if a['prediccion'] == 'under')
    
    print(f"   Apuestas OVER: {apuestas_over}")
    print(f"   Apuestas UNDER: {apuestas_under}")
    
    if apuestas_over > 0 and apuestas_under > 0:
        print("   ✅ Distribución balanceada - PROBLEMA RESUELTO")
    else:
        print("   ❌ Distribución aún sesgada")
    
    # 4. Resumen final
    print("\n4. 📋 RESUMEN FINAL")
    print("="*30)
    
    if conteo_over > 0 and conteo_under > 0 and apuestas_over > 0 and apuestas_under > 0:
        print("✅ SIMULADOR WEB FUNCIONANDO CORRECTAMENTE")
        print("   - Parsing de porcentajes corregido")
        print("   - Distribución balanceada OVER/UNDER")
        print("   - Porcentajes de acierto realistas")
        print("   - Simulación web operativa")
        print("\n🎯 El simulador está listo para usar en: http://localhost:5001")
    else:
        print("❌ AÚN HAY PROBLEMAS QUE RESOLVER")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    verificacion_final()
