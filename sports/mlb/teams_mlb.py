#!/usr/bin/env python3
"""
Diccionario de equipos MLB y funciones de conversión
Migrado desde equipos_data.py original
"""

from core.base import BaseTeams
from typing import Dict

# Diccionario de conversión de siglas a nombres completos
MLB_TEAMS = {
    # American League East
    'NYY': 'New York Yankees',
    'BOS': 'Boston Red Sox', 
    'TOR': 'Toronto Blue Jays',
    'TB': 'Tampa Bay Rays',
    'BAL': 'Baltimore Orioles',
    
    # American League Central  
    'CLE': 'Cleveland Guardians',
    'CHW': 'Chicago White Sox',
    'MIN': 'Minnesota Twins',
    'KC': 'Kansas City Royals',
    'DET': 'Detroit Tigers',
    
    # American League West
    'HOU': 'Houston Astros',
    'LAA': 'Los Angeles Angels',
    'SEA': 'Seattle Mariners',
    'TEX': 'Texas Rangers',
    'OAK': 'Oakland Athletics',
    'ATH': 'Oakland Athletics',  # Alias
    
    # National League East
    'ATL': 'Atlanta Braves',
    'NYM': 'New York Mets',
    'PHI': 'Philadelphia Phillies', 
    'WAS': 'Washington Nationals',
    'MIA': 'Miami Marlins',
    
    # National League Central
    'MIL': 'Milwaukee Brewers',
    'CHC': 'Chicago Cubs',
    'STL': 'St. Louis Cardinals',
    'CIN': 'Cincinnati Reds',
    'PIT': 'Pittsburgh Pirates',
    
    # National League West
    'LAD': 'Los Angeles Dodgers',
    'SD': 'San Diego Padres',
    'SF': 'San Francisco Giants',
    'COL': 'Colorado Rockies',
    'AZ': 'Arizona Diamondbacks'
}

class MLBTeams(BaseTeams):
    """Clase para gestión de equipos MLB"""
    
    def __init__(self):
        super().__init__("mlb")
    
    def get_team_name(self, sigla: str) -> str:
        """Obtener nombre completo del equipo desde sigla"""
        if not sigla:
            return sigla
        
        sigla_upper = sigla.upper().strip()
        return MLB_TEAMS.get(sigla_upper, sigla)
    
    def get_team_sigla(self, nombre_completo: str) -> str:
        """Obtener sigla del equipo desde nombre completo"""
        if not nombre_completo:
            return nombre_completo
        
        # Buscar por nombre completo
        for sigla, nombre in MLB_TEAMS.items():
            if nombre.lower() == nombre_completo.lower():
                return sigla
        
        return nombre_completo
    
    def get_all_teams(self) -> Dict[str, str]:
        """Obtener diccionario completo de equipos"""
        return MLB_TEAMS.copy()
    
    def is_valid_team(self, sigla: str) -> bool:
        """Verificar si una sigla corresponde a un equipo MLB válido"""
        if not sigla:
            return False
        
        return sigla.upper().strip() in MLB_TEAMS
    
    def get_team_abbreviation(self, nombre_equipo: str) -> str:
        """Obtener abreviación del equipo desde nombre (usado en scraping de resultados)"""
        if not nombre_equipo:
            return nombre_equipo
        
        nombre_lower = nombre_equipo.lower().strip()
        
        # Buscar por nombre completo
        for sigla, nombre in MLB_TEAMS.items():
            if nombre.lower() == nombre_lower:
                return sigla
        
        # Buscar por nombres parciales comunes
        nombre_mappings = {
            'yankees': 'NYY',
            'red sox': 'BOS',
            'blue jays': 'TOR',
            'rays': 'TB',
            'orioles': 'BAL',
            'guardians': 'CLE',
            'white sox': 'CHW',
            'twins': 'MIN',
            'royals': 'KC',
            'tigers': 'DET',
            'astros': 'HOU',
            'angels': 'LAA',
            'mariners': 'SEA',
            'rangers': 'TEX',
            'athletics': 'OAK',
            'braves': 'ATL',
            'mets': 'NYM',
            'phillies': 'PHI',
            'nationals': 'WAS',
            'marlins': 'MIA',
            'brewers': 'MIL',
            'cubs': 'CHC',
            'cardinals': 'STL',
            'reds': 'CIN',
            'pirates': 'PIT',
            'dodgers': 'LAD',
            'padres': 'SD',
            'giants': 'SF',
            'rockies': 'COL',
            'diamondbacks': 'AZ'
        }
        
        for nombre_parcial, sigla in nombre_mappings.items():
            if nombre_parcial in nombre_lower:
                return sigla
        
        return nombre_equipo

# Funciones auxiliares para mantener compatibilidad
def convert_team_name(sigla):
    """
    Convertir sigla de equipo a nombre completo
    
    Args:
        sigla (str): Sigla del equipo (ej: 'NYY')
        
    Returns:
        str: Nombre completo del equipo o None si no se encuentra
    """
    if not sigla:
        return None
        
    sigla_upper = sigla.upper().strip()
    return MLB_TEAMS.get(sigla_upper)

def get_team_sigla(team_name):
    """
    Obtener sigla desde nombre completo
    
    Args:
        team_name (str): Nombre completo del equipo
        
    Returns:
        str: Sigla del equipo o None si no se encuentra
    """
    if not team_name:
        return None
        
    # Buscar por nombre completo
    for sigla, nombre in MLB_TEAMS.items():
        if nombre.lower() == team_name.lower():
            return sigla
    
    return None

def is_valid_mlb_team(sigla):
    """
    Verificar si una sigla corresponde a un equipo MLB válido
    
    Args:
        sigla (str): Sigla a verificar
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    if not sigla:
        return False
        
    return sigla.upper().strip() in MLB_TEAMS

def get_all_teams():
    """
    Obtener lista de todos los equipos MLB
    
    Returns:
        dict: Diccionario completo de equipos
    """
    return MLB_TEAMS.copy()

def get_teams_by_division():
    """
    Obtener equipos organizados por división
    
    Returns:
        dict: Equipos agrupados por división
    """
    return {
        'AL_East': {
            'NYY': 'New York Yankees',
            'BOS': 'Boston Red Sox', 
            'TOR': 'Toronto Blue Jays',
            'TB': 'Tampa Bay Rays',
            'BAL': 'Baltimore Orioles'
        },
        'AL_Central': {
            'CLE': 'Cleveland Guardians',
            'CHW': 'Chicago White Sox',
            'MIN': 'Minnesota Twins',
            'KC': 'Kansas City Royals',
            'DET': 'Detroit Tigers'
        },
        'AL_West': {
            'HOU': 'Houston Astros',
            'LAA': 'Los Angeles Angels',
            'SEA': 'Seattle Mariners',
            'TEX': 'Texas Rangers',
            'OAK': 'Oakland Athletics'
        },
        'NL_East': {
            'ATL': 'Atlanta Braves',
            'NYM': 'New York Mets',
            'PHI': 'Philadelphia Phillies', 
            'WAS': 'Washington Nationals',
            'MIA': 'Miami Marlins'
        },
        'NL_Central': {
            'MIL': 'Milwaukee Brewers',
            'CHC': 'Chicago Cubs',
            'STL': 'St. Louis Cardinals',
            'CIN': 'Cincinnati Reds',
            'PIT': 'Pittsburgh Pirates'
        },
        'NL_West': {
            'LAD': 'Los Angeles Dodgers',
            'SD': 'San Diego Padres',
            'SF': 'San Francisco Giants',
            'COL': 'Colorado Rockies',
            'AZ': 'Arizona Diamondbacks'
        }
    }
