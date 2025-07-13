#!/usr/bin/env python3
"""
Simulador de Apuestas Deportivas Web
Interfaz web independiente para simular estrategias de apuestas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import plotly.utils
import json
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('simulador.html')

@app.route('/simular', methods=['POST'])
def simular():
    try:
        # Obtener parámetros del formulario
        bankroll_inicial = float(request.form.get('bankroll', 1000))
        monto_apuesta = float(request.form.get('monto_apuesta', 20))
        consensus_minimo = float(request.form.get('consensus_minimo', 60))
        max_apuestas = int(request.form.get('max_apuestas', 100))
        tipo_apuesta = request.form.get('tipo_apuesta', 'totals')
        cuota = float(request.form.get('cuota', 1.8))
        
        # Ejecutar simulación
        resultado = ejecutar_simulacion(
            bankroll_inicial, 
            monto_apuesta, 
            consensus_minimo, 
            max_apuestas, 
            tipo_apuesta,
            cuota
        )
        
        return render_template('resultados.html', **resultado)
        
    except Exception as e:
        return f"Error en simulación: {str(e)}", 500

def ejecutar_simulacion(bankroll_inicial, monto_apuesta, consensus_minimo, max_apuestas, tipo_apuesta, cuota):
    """Ejecutar simulación de apuestas con los parámetros dados"""
    
    try:
        print(f"Iniciando simulación con: bankroll={bankroll_inicial}, consensus_minimo={consensus_minimo}, tipo={tipo_apuesta}")
        
        # Conectar a la base de datos
        from sports.mlb.database_mlb import MLBDatabase
        db = MLBDatabase()
        
        # Obtener datos según tipo de apuesta
        if tipo_apuesta == 'totals':
            # Obtener consensus totals con resultados ya vinculados
            consensus_response = db.supabase.table('mlb_consensus_totals').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-08-01').execute()
            consensus_data = consensus_response.data
            
            # Procesar apuestas de totals - usar datos ya vinculados
            apuestas_validas = procesar_apuestas_totals_vinculados(consensus_data, consensus_minimo, cuota)
            
        else:  # winners
            # Obtener consensus winners
            consensus_response = db.supabase.table('mlb_consensus_winners').select('*').gte('fecha_hora', '2025-06-01').lt('fecha_hora', '2025-07-01').execute()
            consensus_data = consensus_response.data
            
            # Obtener resultados
            results_response = db.supabase.table('mlb_results').select('*').gte('fecha', '2025-06-01').lt('fecha', '2025-07-01').execute()
            results_data = results_response.data
            
            # Procesar apuestas de winners
            apuestas_validas = procesar_apuestas_winners(consensus_data, results_data, consensus_minimo, cuota)
        
        print(f"Apuestas válidas encontradas: {len(apuestas_validas) if apuestas_validas else 0}")
        
        # Simular bankroll
        if not apuestas_validas:
            # Si no hay apuestas válidas, retornar resultado con valores por defecto
            return {
                'bankroll_inicial': bankroll_inicial,
                'bankroll_final': bankroll_inicial,
                'beneficio_total': 0,
                'porcentaje_cambio': 0,
                'total_apuestas': 0,
                'apuestas_ganadas': 0,
                'apuestas_perdidas': 0,
                'porcentaje_acierto': 0,
                'apuestas_disponibles': 0,
                'apuestas_realizadas': [],
                'historial_bankroll': [bankroll_inicial],
                'grafico_json': json.dumps(go.Figure().add_trace(go.Scatter(x=[0], y=[bankroll_inicial])), cls=plotly.utils.PlotlyJSONEncoder),
                'parametros': {
                    'monto_apuesta': monto_apuesta,
                    'consensus_minimo': consensus_minimo,
                    'max_apuestas': max_apuestas,
                    'cuota': cuota
                },
                'mensaje': f'No se encontraron apuestas que cumplan con el criterio de consensus mínimo de {consensus_minimo}%'
            }
        
        resultado_simulacion = simular_bankroll(apuestas_validas, bankroll_inicial, monto_apuesta, max_apuestas, consensus_minimo, cuota)
        
        return resultado_simulacion
        
    except Exception as e:
        print(f"Error en ejecutar_simulacion: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'error': str(e),
            'bankroll_inicial': bankroll_inicial,
            'bankroll_final': bankroll_inicial,  # Agregar bankroll_final por defecto
            'beneficio_total': 0,
            'porcentaje_cambio': 0,
            'total_apuestas': 0,
            'apuestas_ganadas': 0,
            'apuestas_perdidas': 0,
            'porcentaje_acierto': 0,
            'apuestas_disponibles': 0,
            'apuestas_realizadas': [],
            'historial_bankroll': [bankroll_inicial],
            'grafico_json': None,
            'parametros': {
                'monto_apuesta': monto_apuesta,
                'consensus_minimo': consensus_minimo,  # Esta variable está disponible porque es un parámetro
                'max_apuestas': max_apuestas,
                'cuota': cuota
            }
        }

def procesar_apuestas_totals_vinculados(consensus_data, consensus_minimo, cuota):
    """Procesar apuestas de totals usando datos ya vinculados"""
    
    apuestas_validas = []
    
    for consensus in consensus_data:
        # Verificar que tenga resultados vinculados
        if not consensus.get('total_real') or not consensus.get('resultado_total'):
            continue
        
        # Obtener información del partido
        fecha_hora = consensus.get('fecha_hora', '')
        fecha = fecha_hora.split(' ')[0] if fecha_hora else ''
        
        equipo_1 = consensus.get('equipo_1', '')
        equipo_2 = consensus.get('equipo_2', '')
        sigla_1 = consensus.get('equipo_1_sigla', '')
        sigla_2 = consensus.get('equipo_2_sigla', '')
        
        # Obtener consensus over/under
        consensus_over = consensus.get('consensus_over', 0)
        consensus_under = consensus.get('consensus_under', 0)
        linea_total = consensus.get('linea_total', 0)
        
        # Obtener resultados reales
        total_real = consensus.get('total_real', 0)
        resultado_total = consensus.get('resultado_total', '')
        
        if not equipo_1 or not equipo_2:
            continue
        
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
                # Determinar si la apuesta fue ganadora
                apuesta_ganadora = False
                if mejor_opcion == 'over' and resultado_total == 'OVER':
                    apuesta_ganadora = True
                elif mejor_opcion == 'under' and resultado_total == 'UNDER':
                    apuesta_ganadora = True
                
                # Crear apuesta válida
                apuesta = {
                    'fecha': fecha,
                    'equipos': f"{equipo_1} vs {equipo_2}",
                    'equipo_1': equipo_1,
                    'equipo_2': equipo_2,
                    'sigla_1': sigla_1,
                    'sigla_2': sigla_2,
                    'linea_total': linea_total,
                    'total_real': total_real,
                    'prediccion': mejor_opcion,
                    'tipo_apuesta': mejor_opcion,
                    'porcentaje': mejor_porcentaje,
                    'consensus_porcentaje': mejor_porcentaje,
                    'cuota': cuota,
                    'ganadora': apuesta_ganadora,
                    'gano': apuesta_ganadora,
                    'resultado_real': resultado_total
                }
                
                apuestas_validas.append(apuesta)
                
        except Exception as e:
            print(f"Error procesando consensus {equipo_1} vs {equipo_2}: {str(e)}")
            continue
    
    return apuestas_validas

def procesar_apuestas_totals(consensus_data, results_data, consensus_minimo, cuota):
    """Procesar apuestas de totals con consenso mínimo"""
    
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
    
    apuestas_validas = []
    
    for consensus in consensus_data:
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
            
            print(f"DEBUG: {sigla_1} vs {sigla_2} - OVER: {perc_over}%, UNDER: {perc_under}%")
            
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
                    # Buscar resultado
                    key = f"{fecha}_{sigla_1}_{sigla_2}"
                    key_inv = f"{fecha}_{sigla_2}_{sigla_1}"
                    
                    result = results_dict.get(key) or results_dict.get(key_inv)
                    
                    if result:
                        total_real = result.get('total_puntos', 0)
                        linea = float(linea_total) if linea_total else 0
                        
                        if total_real and linea:
                            total_real = float(total_real)
                            resultado_real = 'over' if total_real > linea else 'under'
                            
                            # Determinar si ganó
                            gano = (mejor_opcion == resultado_real)
                            
                            apuestas_validas.append({
                                'fecha': fecha,
                                'equipos': f"{sigla_1} vs {sigla_2}",
                                'prediccion': mejor_opcion,
                                'porcentaje': mejor_porcentaje,
                                'linea': linea,
                                'total_real': total_real,
                                'resultado': resultado_real,
                                'gano': gano,
                                'cuota': cuota
                            })
                            
        except (ValueError, TypeError):
            continue
    
    return apuestas_validas

def procesar_apuestas_winners(consensus_data, results_data, consensus_minimo, cuota):
    """Procesar apuestas de winners con consenso mínimo"""
    
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
    
    apuestas_validas = []
    
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
        
        # Procesar porcentajes
        try:
            perc_1 = float(str(consensus_1).replace('%', ''))
            perc_2 = float(str(consensus_2).replace('%', ''))
            
            # Verificar si cumple consenso mínimo
            mejor_equipo = None
            mejor_porcentaje = 0
            
            if perc_1 >= consensus_minimo:
                mejor_equipo = sigla_1
                mejor_porcentaje = perc_1
            elif perc_2 >= consensus_minimo:
                mejor_equipo = sigla_2
                mejor_porcentaje = perc_2
            
            if mejor_equipo:
                # Buscar resultado
                key = f"{fecha}_{sigla_1}_{sigla_2}"
                key_inv = f"{fecha}_{sigla_2}_{sigla_1}"
                
                result = results_dict.get(key) or results_dict.get(key_inv)
                
                if result:
                    ganador_real = result.get('ganador', '').upper()
                    
                    # Determinar si ganó
                    gano = (mejor_equipo == ganador_real)
                    
                    apuestas_validas.append({
                        'fecha': fecha,
                        'equipos': f"{sigla_1} vs {sigla_2}",
                        'prediccion': mejor_equipo,
                        'porcentaje': mejor_porcentaje,
                        'ganador_real': ganador_real,
                        'gano': gano,
                        'cuota': cuota
                    })
                    
        except (ValueError, TypeError):
            continue
    
    return apuestas_validas

def simular_bankroll(apuestas_validas, bankroll_inicial, monto_apuesta, max_apuestas, consensus_minimo, cuota):
    """Simular evolución del bankroll"""
    
    bankroll = bankroll_inicial
    historial_bankroll = [bankroll]
    apuestas_realizadas = []
    
    # Ordenar apuestas por fecha
    apuestas_validas.sort(key=lambda x: x['fecha'])
    
    # Tomar solo las primeras max_apuestas
    apuestas_a_realizar = apuestas_validas[:max_apuestas]
    
    for i, apuesta in enumerate(apuestas_a_realizar):
        # Verificar si tenemos suficiente bankroll
        if bankroll < monto_apuesta:
            break
        
        # Realizar apuesta
        bankroll -= monto_apuesta
        
        if apuesta['ganadora']:
            # Cuota europea: si apuestas $100 con cuota 1.8, recibes $180
            ganancia = monto_apuesta * apuesta['cuota']
            bankroll += ganancia
            beneficio = ganancia - monto_apuesta
        else:
            beneficio = -monto_apuesta
        
        # Registrar resultado
        apuestas_realizadas.append({
            'numero': i + 1,
            'fecha': apuesta['fecha'],
            'equipos': apuesta['equipos'],
            'prediccion': apuesta['prediccion'],
            'porcentaje': apuesta['porcentaje'],
            'gano': apuesta['ganadora'],
            'beneficio': beneficio,
            'bankroll': bankroll,
            'cuota': apuesta['cuota']
        })
        
        historial_bankroll.append(bankroll)
    
    # Calcular estadísticas
    total_apuestas = len(apuestas_realizadas)
    apuestas_ganadas = sum(1 for a in apuestas_realizadas if a['gano'])
    apuestas_perdidas = total_apuestas - apuestas_ganadas
    
    beneficio_total = bankroll - bankroll_inicial
    porcentaje_acierto = (apuestas_ganadas / total_apuestas * 100) if total_apuestas > 0 else 0
    
    # Crear gráfico más pequeño
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(historial_bankroll))),
        y=historial_bankroll,
        mode='lines+markers',
        name='Bankroll',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title='Evolución del Bankroll',
        xaxis_title='Número de Apuestas',
        yaxis_title='Bankroll ($)',
        height=280,  # Más pequeño
        width=500,   # Más pequeño
        showlegend=False,
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50)  # Márgenes más pequeños
    )
    
    # Agregar línea de referencia
    fig.add_hline(y=bankroll_inicial, line_dash="dash", line_color="red", 
                  annotation_text="Bankroll Inicial")
    
    grafico_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return {
        'bankroll_inicial': bankroll_inicial,
        'bankroll_final': bankroll,
        'beneficio_total': beneficio_total,
        'porcentaje_cambio': ((bankroll - bankroll_inicial) / bankroll_inicial * 100),
        'total_apuestas': total_apuestas,
        'apuestas_ganadas': apuestas_ganadas,
        'apuestas_perdidas': apuestas_perdidas,
        'porcentaje_acierto': porcentaje_acierto,
        'apuestas_disponibles': len(apuestas_validas),
        'apuestas_realizadas': apuestas_realizadas,
        'historial_bankroll': historial_bankroll,
        'grafico_json': grafico_json,
        'parametros': {
            'monto_apuesta': monto_apuesta,
            'consensus_minimo': consensus_minimo,
            'max_apuestas': max_apuestas,
            'cuota': cuota
        }
    }

if __name__ == '__main__':
    print("🎰 Iniciando Simulador de Apuestas...")
    print("📊 Accede a: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
