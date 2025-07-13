#!/usr/bin/env python3
"""
Script para obtener resultados de ESPN y vincularlos con predicciones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sports.mlb.database_mlb import MLBDatabase
import requests
import json
import re
from datetime import datetime, timedelta
import logging
from time import sleep

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('obtener_resultados_espn.log'),
        logging.StreamHandler()
    ]
)

def obtener_resultados_espn_por_fecha(fecha_str):
    """Obtener resultados de ESPN para una fecha específica"""
    try:
        # Convertir fecha a formato ESPN
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        fecha_espn = fecha_obj.strftime('%Y%m%d')
        
        # URL de ESPN para resultados
        url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={fecha_espn}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        resultados = []
        
        if 'events' in data:
            for event in data['events']:
                if event.get('status', {}).get('type', {}).get('completed', False):
                    # Partido terminado
                    competitions = event.get('competitions', [])
                    if competitions:
                        competition = competitions[0]
                        competitors = competition.get('competitors', [])
                        
                        if len(competitors) >= 2:
                            equipo_1 = competitors[0].get('team', {}).get('displayName', '')
                            equipo_2 = competitors[1].get('team', {}).get('displayName', '')
                            
                            score_1 = competitors[0].get('score', '0')
                            score_2 = competitors[1].get('score', '0')
                            
                            try:
                                puntaje_1 = int(score_1)
                                puntaje_2 = int(score_2)
                                
                                resultados.append({
                                    'fecha': fecha_str,
                                    'equipo_1': equipo_1,
                                    'equipo_2': equipo_2,
                                    'puntaje_1': puntaje_1,
                                    'puntaje_2': puntaje_2,
                                    'total': puntaje_1 + puntaje_2
                                })
                            except (ValueError, TypeError):
                                continue
        
        return resultados
        
    except Exception as e:
        logging.error(f"Error obteniendo resultados de ESPN para {fecha_str}: {e}")
        return []

def normalizar_nombre_equipo(nombre):
    """Normalizar nombres de equipos para comparación"""
    # Diccionario de equivalencias
    equivalencias = {
        'LA Angels': 'Los Angeles Angels',
        'LA Dodgers': 'Los Angeles Dodgers',
        'NY Yankees': 'New York Yankees',
        'NY Mets': 'New York Mets',
        'Chi Cubs': 'Chicago Cubs',
        'Chi White Sox': 'Chicago White Sox',
        'SD Padres': 'San Diego Padres',
        'SF Giants': 'San Francisco Giants',
        'TB Rays': 'Tampa Bay Rays',
        'KC Royals': 'Kansas City Royals',
        'StL Cardinals': 'St. Louis Cardinals',
        'Los Angeles Angels of Anaheim': 'Los Angeles Angels',
        'Chicago Cubs': 'Chicago Cubs',
        'Chicago White Sox': 'Chicago White Sox',
        'San Diego Padres': 'San Diego Padres',
        'San Francisco Giants': 'San Francisco Giants',
        'Tampa Bay Rays': 'Tampa Bay Rays',
        'Kansas City Royals': 'Kansas City Royals',
        'St. Louis Cardinals': 'St. Louis Cardinals'
    }
    
    nombre_limpio = nombre.strip()
    return equivalencias.get(nombre_limpio, nombre_limpio)

def buscar_partido_en_resultados(equipo_1, equipo_2, resultados):
    """Buscar un partido específico en los resultados"""
    equipo_1_norm = normalizar_nombre_equipo(equipo_1)
    equipo_2_norm = normalizar_nombre_equipo(equipo_2)
    
    for resultado in resultados:
        result_equipo_1 = normalizar_nombre_equipo(resultado['equipo_1'])
        result_equipo_2 = normalizar_nombre_equipo(resultado['equipo_2'])
        
        # Verificar ambas combinaciones de equipos
        if ((result_equipo_1 == equipo_1_norm and result_equipo_2 == equipo_2_norm) or
            (result_equipo_1 == equipo_2_norm and result_equipo_2 == equipo_1_norm)):
            return resultado
    
    return None

def extraer_porcentaje_from_field(field_value):
    """Extraer porcentaje de un campo de consensus"""
    if not field_value:
        return 0
    
    # Buscar patron "X % Over" o "X % Under" 
    match = re.search(r'(\d+)\s*%', str(field_value))
    if match:
        return int(match.group(1))
    return 0

def obtener_y_vincular_resultados():
    """Obtener resultados de ESPN y vincularlos con consensus"""
    print("🏀 OBTENIENDO RESULTADOS DE ESPN")
    print("="*60)
    
    # Conectar a la base de datos
    db = MLBDatabase()
    
    # Obtener datos de consensus totals sin resultados vinculados
    print("📊 Obteniendo datos de consensus totals...")
    response = db.supabase.table('mlb_consensus_totals').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-08-01').is_('total_real', 'null').execute()
    consensus_data = response.data
    
    print(f"✅ Registros de consensus sin resultados: {len(consensus_data)}")
    
    if not consensus_data:
        print("❌ No hay datos de consensus para vincular")
        return
    
    # Obtener fechas únicas para scraping
    fechas_unicas = set()
    for consensus in consensus_data:
        fechas_unicas.add(consensus['fecha_hora'])
    
    print(f"📅 Fechas únicas para scraping: {len(fechas_unicas)}")
    
    # Obtener resultados de ESPN para cada fecha
    todos_resultados = []
    
    for i, fecha in enumerate(sorted(fechas_unicas)):
        print(f"📈 Obteniendo resultados para {fecha} ({i+1}/{len(fechas_unicas)})")
        
        resultados_fecha = obtener_resultados_espn_por_fecha(fecha)
        todos_resultados.extend(resultados_fecha)
        
        print(f"   ✅ Encontrados {len(resultados_fecha)} partidos")
        
        # Pausa para evitar rate limiting
        sleep(1)
    
    print(f"\n📊 Total de resultados obtenidos: {len(todos_resultados)}")
    
    if not todos_resultados:
        print("❌ No se pudieron obtener resultados de ESPN")
        return
    
    # Procesar vinculación
    vinculados = 0
    no_encontrados = 0
    
    print("\n🔗 VINCULANDO RESULTADOS...")
    
    for consensus in consensus_data:
        equipo_1 = consensus['equipo_1']
        equipo_2 = consensus['equipo_2']
        fecha = consensus['fecha_hora']
        linea_total = consensus['linea_total']
        
        # Buscar resultado correspondiente
        resultados_fecha = [r for r in todos_resultados if r['fecha'] == fecha]
        resultado = buscar_partido_en_resultados(equipo_1, equipo_2, resultados_fecha)
        
        if resultado:
            # Calcular totales
            puntaje_1 = resultado['puntaje_1']
            puntaje_2 = resultado['puntaje_2']
            total_real = resultado['total']
            
            # Determinar resultado (OVER/UNDER)
            resultado_total = 'OVER' if total_real > linea_total else 'UNDER'
            
            # Extraer porcentajes de consensus (recordar que están invertidos)
            porcentaje_under = extraer_porcentaje_from_field(consensus['consensus_over'])  # Invertido
            porcentaje_over = extraer_porcentaje_from_field(consensus['consensus_under'])   # Invertido
            
            # Determinar predicción dominante
            prediccion_dominante = 'OVER' if porcentaje_over > porcentaje_under else 'UNDER'
            
            # Verificar si la predicción fue correcta
            prediccion_correcta = prediccion_dominante == resultado_total
            
            # Actualizar registro
            try:
                db.supabase.table('mlb_consensus_totals').update({
                    'puntaje_equipo_1': puntaje_1,
                    'puntaje_equipo_2': puntaje_2,
                    'total_real': total_real,
                    'resultado_total': resultado_total,
                    'prediccion_correcta': prediccion_correcta
                }).eq('id', consensus['id']).execute()
                
                vinculados += 1
                
                if vinculados % 10 == 0:
                    print(f"🔗 Vinculados: {vinculados}")
                    
            except Exception as e:
                logging.error(f"Error actualizando registro {consensus['id']}: {e}")
        else:
            no_encontrados += 1
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE VINCULACIÓN")
    print("="*60)
    print(f"✅ Registros vinculados exitosamente: {vinculados}")
    print(f"❌ Registros no encontrados: {no_encontrados}")
    print(f"📊 Total procesados: {len(consensus_data)}")
    
    if vinculados > 0:
        print(f"📈 Porcentaje de vinculación: {(vinculados/len(consensus_data)*100):.1f}%")
    
    return vinculados

def main():
    """Función principal"""
    print("🏀 OBTENEDOR DE RESULTADOS ESPN")
    print("="*60)
    
    try:
        vinculados = obtener_y_vincular_resultados()
        
        if vinculados > 0:
            print("\n✅ Vinculación completada exitosamente!")
            print("🎰 Ahora puedes usar el simulador con datos reales")
        else:
            print("\n⚠️ No se pudieron vincular resultados")
            print("Verifica la conexión a ESPN y los nombres de equipos")
            
    except Exception as e:
        logging.error(f"Error en obtención de resultados: {e}")
        print(f"❌ Error durante la obtención: {e}")

if __name__ == "__main__":
    main()
