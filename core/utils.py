#!/usr/bin/env python3
"""
Utilidades compartidas para el sistema de predicciones deportivas
"""

import re
from datetime import datetime, timedelta

def parse_date_from_text(date_text, reference_date=None):
    """
    Parsear fecha desde texto de la web
    Ejemplo: 'Sun. Jun 29\n1:35 pm ET' -> '2025-06-29'
    """
    if not date_text or date_text.strip() == '':
        if reference_date:
            return reference_date
        return datetime.now().strftime("%Y-%m-%d")
    
    # Diccionario de meses
    months = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    
    # Buscar patrón: Day Month DD
    pattern = r'(\w{3})\.\s+(\w{3})\s+(\d{1,2})'
    match = re.search(pattern, date_text)
    
    if match:
        month_name = match.group(2)
        day = match.group(3).zfill(2)
        
        if month_name in months:
            month = months[month_name]
            
            # Determinar año (asumir año actual si no se especifica)
            current_year = datetime.now().year
            return f"{current_year}-{month}-{day}"
    
    # Si no puede parsear, usar fecha de referencia
    if reference_date:
        return reference_date
    
    return datetime.now().strftime("%Y-%m-%d")

def parse_consensus_percentages(consensus_text):
    """
    Parsear porcentajes de consensus
    Ejemplo: '17%\n83%' -> ('17%', '83%')
    """
    if not consensus_text:
        return None, None
    
    # Buscar porcentajes
    percentages = re.findall(r'(\d+%)', consensus_text)
    
    if len(percentages) >= 2:
        return percentages[0], percentages[1]
    
    return None, None

def parse_picks_count(picks_text):
    """
    Parsear conteo de picks
    Ejemplo: '5\n25' -> (5, 25)
    """
    if not picks_text:
        return None, None
    
    # Buscar números
    numbers = re.findall(r'(\d+)', picks_text)
    
    if len(numbers) >= 2:
        try:
            return int(numbers[0]), int(numbers[1])
        except ValueError:
            return None, None
    
    return None, None

def clean_team_name(team_name):
    """Limpiar nombre de equipo"""
    if not team_name:
        return None
    
    # Remover espacios extra y caracteres especiales
    cleaned = re.sub(r'\s+', ' ', team_name.strip())
    return cleaned

def format_date_for_url(date_str):
    """
    Formatear fecha para URLs
    Entrada: '2025-06-29' -> Salida: '2025-06-29'
    """
    try:
        # Validar formato de fecha
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        # Si no es válida, usar fecha actual
        return datetime.now().strftime("%Y-%m-%d")

def is_current_season(sport, date_str):
    """
    Verificar si una fecha está en la temporada actual del deporte
    """
    from core.base import get_sport_config
    
    config = get_sport_config(sport)
    if not config:
        return True  # Asumir que sí si no hay configuración
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        month = date_obj.month
        
        return month in config.get('season_months', [1,2,3,4,5,6,7,8,9,10,11,12])
    except ValueError:
        return True

def log_scraping_result(sport, operation, date_str, count, success=True):
    """
    Log estandarizado para resultados de scraping
    """
    status = "✅" if success else "❌"
    print(f"{status} {sport.upper()} {operation}: {count} registros para {date_str}")
