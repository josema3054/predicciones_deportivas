#!/usr/bin/env python3
"""
Debug del simulador web - verificar datos y lógica
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sports.mlb.database_mlb import MLBDatabase
import re

def debug_simulador():
    """Debug del simulador web"""
    
    print("🔍 Debugging Simulador Web...")
    
    # Conectar a base de datos
    db = MLBDatabase()
    
    # Obtener datos de consensus totals
    consensus_response = db.supabase.table('mlb_consensus_totals').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-08-01').execute()
    consensus_data = consensus_response.data
    
    print(f"📊 Total registros consensus_totals: {len(consensus_data)}")
    
    # Verificar datos con resultados vinculados
    datos_con_resultados = [c for c in consensus_data if c.get('total_real') and c.get('resultado_total')]
    print(f"📈 Registros con resultados vinculados: {len(datos_con_resultados)}")
    
    if datos_con_resultados:
        print("\n🎯 Ejemplo de datos con resultados:")
        ejemplo = datos_con_resultados[0]
        print(f"Fecha: {ejemplo.get('fecha_hora', '')}")
        print(f"Equipos: {ejemplo.get('equipo_1', '')} vs {ejemplo.get('equipo_2', '')}")
        print(f"Consensus Over: {ejemplo.get('consensus_over', '')}")
        print(f"Consensus Under: {ejemplo.get('consensus_under', '')}")
        print(f"Línea Total: {ejemplo.get('linea_total', '')}")
        print(f"Total Real: {ejemplo.get('total_real', '')}")
        print(f"Resultado Total: {ejemplo.get('resultado_total', '')}")
    
    # Procesar apuestas con consensus_minimo = 60%
    consensus_minimo = 60
    cuota = 1.8
    
    apuestas_validas = []
    
    for consensus in datos_con_resultados:
        # Obtener consensus over/under
        consensus_over = consensus.get('consensus_over', 0)
        consensus_under = consensus.get('consensus_under', 0)
        
        # Procesar porcentajes - CORRECCIÓN: verificar contenido de los campos
        try:
            # Inicializar porcentajes
            perc_over = 0
            perc_under = 0
            
            # Parsear consensus_over
            over_str = str(consensus_over)
            over_match = re.search(r'(\d+)\s*%', over_str)
            if over_match:
                porcentaje = float(over_match.group(1))
                # Verificar si el texto contiene "Over" o "Under"
                if 'Over' in over_str:
                    perc_over = porcentaje
                elif 'Under' in over_str:
                    perc_under = porcentaje
            
            # Parsear consensus_under
            under_str = str(consensus_under)
            under_match = re.search(r'(\d+)\s*%', under_str)
            if under_match:
                porcentaje = float(under_match.group(1))
                # Verificar si el texto contiene "Over" o "Under"
                if 'Over' in under_str:
                    perc_over = porcentaje
                elif 'Under' in under_str:
                    perc_under = porcentaje
            
            # Verificar si cumple consenso mínimo
            mejor_opcion = None
            mejor_porcentaje = 0
            
            if perc_over >= consensus_minimo:
                mejor_opcion = 'over'
                mejor_porcentaje = perc_over
            elif perc_under >= consensus_minimo:
                mejor_opcion = 'under'
                mejor_porcentaje = perc_under
            
            if mejor_opcion:
                # Obtener resultado real
                resultado_total = consensus.get('resultado_total', '')
                
                # Determinar si la apuesta fue ganadora
                apuesta_ganadora = False
                if mejor_opcion == 'over' and resultado_total == 'OVER':
                    apuesta_ganadora = True
                elif mejor_opcion == 'under' and resultado_total == 'UNDER':
                    apuesta_ganadora = True
                
                apuestas_validas.append({
                    'fecha': consensus.get('fecha_hora', '').split(' ')[0],
                    'equipos': f"{consensus.get('equipo_1', '')} vs {consensus.get('equipo_2', '')}",
                    'tipo_apuesta': mejor_opcion,
                    'consensus_porcentaje': mejor_porcentaje,
                    'ganadora': apuesta_ganadora,
                    'resultado_real': resultado_total,
                    'linea_total': consensus.get('linea_total', 0),
                    'total_real': consensus.get('total_real', 0)
                })
                
        except Exception as e:
            print(f"Error procesando consensus: {str(e)}")
            continue
    
    print(f"\n🎰 Apuestas válidas encontradas: {len(apuestas_validas)}")
    
    if apuestas_validas:
        print("\n🎯 Primeras 5 apuestas válidas:")
        for i, apuesta in enumerate(apuestas_validas[:5]):
            print(f"{i+1}. {apuesta['fecha']} - {apuesta['equipos']}")
            print(f"   Apuesta: {apuesta['tipo_apuesta'].upper()} ({apuesta['consensus_porcentaje']}%)")
            print(f"   Resultado: {apuesta['resultado_real']} - {'✅ GANÓ' if apuesta['ganadora'] else '❌ PERDIÓ'}")
            print(f"   Línea: {apuesta['linea_total']}, Total Real: {apuesta['total_real']}")
        
        # Calcular estadísticas
        ganadas = sum(1 for a in apuestas_validas if a['ganadora'])
        perdidas = len(apuestas_validas) - ganadas
        porcentaje_acierto = (ganadas / len(apuestas_validas) * 100) if apuestas_validas else 0
        
        print(f"\n📊 Estadísticas:")
        print(f"Total apuestas: {len(apuestas_validas)}")
        print(f"Ganadas: {ganadas}")
        print(f"Perdidas: {perdidas}")
        print(f"Porcentaje acierto: {porcentaje_acierto:.1f}%")
        
        # Simular bankroll
        bankroll_inicial = 1000
        monto_apuesta = 20
        bankroll = bankroll_inicial
        
        for apuesta in apuestas_validas:
            bankroll -= monto_apuesta
            if apuesta['ganadora']:
                ganancia = monto_apuesta * cuota
                bankroll += ganancia
        
        beneficio_total = bankroll - bankroll_inicial
        porcentaje_cambio = (beneficio_total / bankroll_inicial * 100)
        
        print(f"\n💰 Simulación Bankroll:")
        print(f"Bankroll inicial: ${bankroll_inicial}")
        print(f"Bankroll final: ${bankroll:.2f}")
        print(f"Beneficio total: ${beneficio_total:.2f}")
        print(f"Porcentaje cambio: {porcentaje_cambio:.1f}%")
        
    else:
        print("❌ No se encontraron apuestas válidas")

if __name__ == '__main__':
    debug_simulador()
