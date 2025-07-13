#!/usr/bin/env python3
"""
Investigar el problema con los porcentajes OVER/UNDER
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sports.mlb.database_mlb import MLBDatabase
import re

def investigar_over_under():
    """Investigar el problema con los porcentajes OVER/UNDER"""
    
    print("🔍 Investigando problema OVER/UNDER...")
    
    # Conectar a base de datos
    db = MLBDatabase()
    
    # Obtener datos de consensus totals
    consensus_response = db.supabase.table('mlb_consensus_totals').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-08-01').execute()
    consensus_data = consensus_response.data
    
    print(f"📊 Total registros: {len(consensus_data)}")
    
    # Analizar los primeros 10 registros
    print("\n🎯 Análisis de los primeros 10 registros:")
    
    conteo_over = 0
    conteo_under = 0
    
    for i, consensus in enumerate(consensus_data[:20]):
        print(f"\n{i+1}. {consensus.get('fecha_hora', '')} - {consensus.get('equipo_1', '')} vs {consensus.get('equipo_2', '')}")
        
        consensus_over = consensus.get('consensus_over', '')
        consensus_under = consensus.get('consensus_under', '')
        
        print(f"   Campo 'consensus_over': '{consensus_over}'")
        print(f"   Campo 'consensus_under': '{consensus_under}'")
        
        # Parsear porcentajes
        try:
            # Parsear consensus_over
            over_str = str(consensus_over)
            over_match = re.search(r'(\d+)\s*%', over_str)
            perc_over = float(over_match.group(1)) if over_match else 0
            
            # Parsear consensus_under
            under_str = str(consensus_under)
            under_match = re.search(r'(\d+)\s*%', under_str)
            perc_under = float(under_match.group(1)) if under_match else 0
            
            print(f"   Porcentaje OVER parseado: {perc_over}%")
            print(f"   Porcentaje UNDER parseado: {perc_under}%")
            
            # Verificar cuál es mayor
            if perc_over > perc_under:
                mejor_opcion = 'OVER'
                conteo_over += 1
            else:
                mejor_opcion = 'UNDER'
                conteo_under += 1
                
            print(f"   Mejor opción: {mejor_opcion}")
            
            # Verificar si el texto contiene "Over" o "Under"
            if 'Over' in str(consensus_over) or 'over' in str(consensus_over):
                print(f"   ✅ Campo 'consensus_over' contiene 'Over'")
            if 'Under' in str(consensus_over) or 'under' in str(consensus_over):
                print(f"   ⚠️  Campo 'consensus_over' contiene 'Under'")
                
            if 'Over' in str(consensus_under) or 'over' in str(consensus_under):
                print(f"   ⚠️  Campo 'consensus_under' contiene 'Over'")
            if 'Under' in str(consensus_under) or 'under' in str(consensus_under):
                print(f"   ✅ Campo 'consensus_under' contiene 'Under'")
                
        except Exception as e:
            print(f"   ❌ Error parseando: {str(e)}")
    
    print(f"\n📊 Resumen de los primeros 20 registros:")
    print(f"Mejor opción OVER: {conteo_over}")
    print(f"Mejor opción UNDER: {conteo_under}")
    
    if conteo_over > conteo_under * 3:
        print("⚠️  PROBLEMA DETECTADO: Demasiadas apuestas OVER")
        print("   Esto sugiere que los campos están mal parseados o hay un sesgo en los datos")
        
    # Verificar si los campos están invertidos
    print("\n🔄 Verificando si los campos están invertidos...")
    
    ejemplo = consensus_data[0]
    consensus_over = ejemplo.get('consensus_over', '')
    consensus_under = ejemplo.get('consensus_under', '')
    
    print(f"Ejemplo - consensus_over: '{consensus_over}'")
    print(f"Ejemplo - consensus_under: '{consensus_under}'")
    
    # Verificar contenido de los campos
    if 'Under' in str(consensus_over):
        print("⚠️  PROBLEMA: Campo 'consensus_over' contiene 'Under'")
        print("   Los campos están INVERTIDOS en la base de datos")
    elif 'Over' in str(consensus_over):
        print("✅ Campo 'consensus_over' contiene 'Over' (correcto)")
        
    if 'Over' in str(consensus_under):
        print("⚠️  PROBLEMA: Campo 'consensus_under' contiene 'Over'")
        print("   Los campos están INVERTIDOS en la base de datos")
    elif 'Under' in str(consensus_under):
        print("✅ Campo 'consensus_under' contiene 'Under' (correcto)")

if __name__ == '__main__':
    investigar_over_under()
