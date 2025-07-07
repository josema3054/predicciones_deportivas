#!/usr/bin/env python3
"""
Análisis de efectividad corregido - usando porcentajes de consensus
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎯 ANÁLISIS DE EFECTIVIDAD CORREGIDO")
    print("="*50)
    
    try:
        from sports.mlb.database_mlb import MLBDatabase
        
        db = MLBDatabase()
        
        # Obtener datos de junio 2025
        print("📊 Obteniendo datos de junio 2025...")
        
        # Filtrar consensus de junio 2025
        consensus_response = db.supabase.table('mlb_consensus_winners').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-07-01').execute()
        consensus_data = consensus_response.data
        
        # Filtrar totals de junio 2025
        totals_response = db.supabase.table('mlb_consensus_totals').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-07-01').execute()
        totals_data = totals_response.data
        
        # Filtrar resultados de junio 2025
        results_response = db.supabase.table('mlb_results').select('*').gte('fecha', '2025-06-01').lt('fecha', '2025-07-01').execute()
        results_data = results_response.data
        
        print(f"✅ Datos de junio 2025:")
        print(f"   🏆 Consensus Winners: {len(consensus_data)} registros")
        print(f"   🎯 Consensus Totals: {len(totals_data)} registros")
        print(f"   📊 Resultados: {len(results_data)} registros")
        
        if not consensus_data or not results_data:
            print("❌ No hay datos suficientes para el análisis")
            return
        
        # Análisis de efectividad para Winners
        print("\n🏆 ANÁLISIS CONSENSUS WINNERS")
        print("="*40)
        
        winners_stats = analyze_winners_with_percentages(consensus_data, results_data)
        
        # Análisis de efectividad para Totals
        print("\n🎯 ANÁLISIS CONSENSUS TOTALS")
        print("="*40)
        
        totals_stats = analyze_totals_with_consensus(totals_data, results_data)
        
        # Resumen final
        print("\n📈 RESUMEN FINAL")
        print("="*50)
        print(f"🏆 Winners - Efectividad: {winners_stats['efectividad']:.1f}% ({winners_stats['aciertos']}/{winners_stats['encontradas']})")
        print(f"🎯 Totals - Efectividad: {totals_stats['efectividad']:.1f}% ({totals_stats['aciertos']}/{totals_stats['encontradas']})")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def analyze_winners_with_percentages(consensus_data, results_data):
    """Analizar winners usando porcentajes de consensus"""
    
    def clean_team_name(team_name: str) -> str:
        if not team_name:
            return ""
        return team_name.lower().strip().replace(".", "").replace("-", " ").replace("_", " ")
    
    # Crear diccionario de resultados
    results_dict = {}
    for result in results_data:
        fecha = result.get('fecha', '')
        
        # Usar siglas directamente
        local_sigla = result.get('equipo_local_sigla', '').upper()
        visitante_sigla = result.get('equipo_visitante_sigla', '').upper()
        
        if local_sigla and visitante_sigla:
            key = f"{fecha}_{local_sigla}_{visitante_sigla}"
            results_dict[key] = result
            
            key_inv = f"{fecha}_{visitante_sigla}_{local_sigla}"
            results_dict[key_inv] = result
    
    encontradas = 0
    aciertos = 0
    
    print("🔍 Analizando predicciones basadas en porcentajes...")
    
    for consensus in consensus_data:
        # Extraer fecha
        fecha_hora = consensus.get('fecha_hora', '')
        fecha = fecha_hora.split(' ')[0] if fecha_hora else ''
        
        # Obtener siglas
        sigla_1 = consensus.get('equipo_1_sigla', '').upper()
        sigla_2 = consensus.get('equipo_2_sigla', '').upper()
        
        # Obtener porcentajes
        consensus_1 = consensus.get('consensus_equipo_1', 0)
        consensus_2 = consensus.get('consensus_equipo_2', 0)
        
        if not sigla_1 or not sigla_2:
            continue
        
        # Buscar resultado
        key = f"{fecha}_{sigla_1}_{sigla_2}"
        key_inv = f"{fecha}_{sigla_2}_{sigla_1}"
        
        result = results_dict.get(key) or results_dict.get(key_inv)
        
        if result:
            encontradas += 1
            
            # Determinar predicción basada en porcentajes
            if consensus_1 and consensus_2:
                try:
                    perc_1 = float(str(consensus_1).replace('%', ''))
                    perc_2 = float(str(consensus_2).replace('%', ''))
                    
                    # El equipo con mayor porcentaje es la predicción
                    if perc_1 > perc_2:
                        prediccion = sigla_1
                    else:
                        prediccion = sigla_2
                    
                    # Comparar con resultado real
                    ganador_real = result.get('ganador', '').upper()
                    
                    if prediccion == ganador_real:
                        aciertos += 1
                        print(f"   ✅ {fecha}: {prediccion} vs {ganador_real} - ACIERTO")
                    else:
                        print(f"   ❌ {fecha}: {prediccion} vs {ganador_real} - FALLO")
                        
                except (ValueError, TypeError):
                    print(f"   ⚠️  Error en porcentajes: {consensus_1}, {consensus_2}")
    
    efectividad = (aciertos / encontradas * 100) if encontradas > 0 else 0
    
    print(f"📊 Resultados Winners:")
    print(f"   Predicciones encontradas: {encontradas}")
    print(f"   Aciertos: {aciertos}")
    print(f"   Efectividad: {efectividad:.1f}%")
    
    return {
        'encontradas': encontradas,
        'aciertos': aciertos,
        'efectividad': efectividad
    }

def analyze_totals_with_consensus(totals_data, results_data):
    """Analizar totals usando consensus over/under"""
    
    # Crear diccionario de resultados
    results_dict = {}
    for result in results_data:
        fecha = result.get('fecha', '')
        
        local_sigla = result.get('equipo_local_sigla', '').upper()
        visitante_sigla = result.get('equipo_visitante_sigla', '').upper()
        
        if local_sigla and visitante_sigla:
            key = f"{fecha}_{local_sigla}_{visitante_sigla}"
            results_dict[key] = result
            
            key_inv = f"{fecha}_{visitante_sigla}_{local_sigla}"
            results_dict[key_inv] = result
    
    encontradas = 0
    aciertos = 0
    
    print("🔍 Analizando predicciones de totals...")
    
    for consensus in totals_data:
        # Extraer fecha
        fecha_hora = consensus.get('fecha_hora', '')
        fecha = fecha_hora.split(' ')[0] if fecha_hora else ''
        
        # Obtener siglas
        sigla_1 = consensus.get('equipo_1_sigla', '').upper()
        sigla_2 = consensus.get('equipo_2_sigla', '').upper()
        
        # Obtener consensus over/under
        consensus_over = consensus.get('consensus_over', 0)
        consensus_under = consensus.get('consensus_under', 0)
        linea_total = consensus.get('linea_total', 0)
        
        if not sigla_1 or not sigla_2:
            continue
        
        # Buscar resultado
        key = f"{fecha}_{sigla_1}_{sigla_2}"
        key_inv = f"{fecha}_{sigla_2}_{sigla_1}"
        
        result = results_dict.get(key) or results_dict.get(key_inv)
        
        if result:
            encontradas += 1
            
            # Determinar predicción basada en consensus
            if consensus_over and consensus_under:
                try:
                    # Limpiar el formato de porcentajes
                    over_str = str(consensus_over).replace('%', '').strip()
                    under_str = str(consensus_under).replace('%', '').strip()
                    
                    # Extraer solo números
                    import re
                    over_match = re.search(r'(\d+)', over_str)
                    under_match = re.search(r'(\d+)', under_str)
                    
                    if over_match and under_match:
                        perc_over = float(over_match.group(1))
                        perc_under = float(under_match.group(1))
                        
                        # El side con mayor porcentaje es la predicción
                        if perc_over > perc_under:
                            prediccion = 'over'
                        else:
                            prediccion = 'under'
                        
                        # Comparar con resultado real
                        total_real = result.get('total_puntos', 0)
                        linea = float(linea_total) if linea_total else 0
                        
                        if total_real and linea:
                            total_real = float(total_real)
                            
                            resultado_real = 'over' if total_real > linea else 'under'
                            
                            if prediccion == resultado_real:
                                aciertos += 1
                                print(f"   ✅ {fecha}: {prediccion} vs {resultado_real} ({total_real} vs {linea}) - ACIERTO")
                            else:
                                print(f"   ❌ {fecha}: {prediccion} vs {resultado_real} ({total_real} vs {linea}) - FALLO")
                        else:
                            print(f"   ⚠️  Sin datos de totals: total={total_real}, linea={linea}")
                            
                except (ValueError, TypeError) as e:
                    print(f"   ⚠️  Error en datos: over={consensus_over}, under={consensus_under}, error={e}")
    
    efectividad = (aciertos / encontradas * 100) if encontradas > 0 else 0
    
    print(f"📊 Resultados Totals:")
    print(f"   Predicciones encontradas: {encontradas}")
    print(f"   Aciertos: {aciertos}")
    print(f"   Efectividad: {efectividad:.1f}%")
    
    return {
        'encontradas': encontradas,
        'aciertos': aciertos,
        'efectividad': efectividad
    }

if __name__ == "__main__":
    main()
