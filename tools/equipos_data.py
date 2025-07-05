# 🏆 BASE DE DATOS DE EQUIPOS DEPORTIVOS
# Escalable para múltiples deportes

# 🏈 MLB - Major League Baseball
EQUIPOS_MLB = {
    # American League East
    'BAL': 'Baltimore Orioles',
    'BOS': 'Boston Red Sox',
    'NYY': 'New York Yankees',
    'TB': 'Tampa Bay Rays',
    'TOR': 'Toronto Blue Jays',
    
    # American League Central
    'CHW': 'Chicago White Sox',
    'CLE': 'Cleveland Guardians',
    'DET': 'Detroit Tigers',
    'KC': 'Kansas City Royals',
    'MIN': 'Minnesota Twins',
    
    # American League West
    'HOU': 'Houston Astros',
    'LAA': 'Los Angeles Angels',
    'ATH': 'Oakland Athletics',
    'SEA': 'Seattle Mariners',
    'TEX': 'Texas Rangers',
    
    # National League East
    'ATL': 'Atlanta Braves',
    'MIA': 'Miami Marlins',
    'NYM': 'New York Mets',
    'PHI': 'Philadelphia Phillies',
    'WAS': 'Washington Nationals',
    
    # National League Central
    'CHC': 'Chicago Cubs',
    'CIN': 'Cincinnati Reds',
    'MIL': 'Milwaukee Brewers',
    'PIT': 'Pittsburgh Pirates',
    'STL': 'St. Louis Cardinals',
    
    # National League West
    'AZ': 'Arizona Diamondbacks',
    'COL': 'Colorado Rockies',
    'LAD': 'Los Angeles Dodgers',
    'SD': 'San Diego Padres',
    'SF': 'San Francisco Giants'
}

# 🏀 NBA - National Basketball Association (para futuro)
EQUIPOS_NBA = {
    'LAL': 'Los Angeles Lakers',
    'GSW': 'Golden State Warriors',
    'BOS': 'Boston Celtics',
    # ... agregar más cuando sea necesario
}

# 🏈 NFL - National Football League (para futuro)
EQUIPOS_NFL = {
    'NE': 'New England Patriots',
    'KC': 'Kansas City Chiefs',
    'TB': 'Tampa Bay Buccaneers',
    # ... agregar más cuando sea necesario
}

# 🏆 DICCIONARIO PRINCIPAL
EQUIPOS_POR_DEPORTE = {
    'mlb': EQUIPOS_MLB,
    'nba': EQUIPOS_NBA,
    'nfl': EQUIPOS_NFL
}

def obtener_nombre_equipo(sigla, deporte='mlb'):
    """
    Convierte una sigla de equipo en el nombre completo.
    
    Args:
        sigla (str): Sigla del equipo (ej: 'SEA', 'LAD')
        deporte (str): Deporte ('mlb', 'nba', 'nfl')
    
    Returns:
        str: Nombre completo del equipo o la sigla original si no se encuentra
    
    Ejemplos:
        >>> obtener_nombre_equipo('SEA', 'mlb')
        'Seattle Mariners'
        >>> obtener_nombre_equipo('XYZ', 'mlb')
        'XYZ'  # Devuelve la sigla si no encuentra equivalencia
    """
    if deporte in EQUIPOS_POR_DEPORTE:
        return EQUIPOS_POR_DEPORTE[deporte].get(sigla, sigla)
    return sigla

def obtener_sigla_desde_nombre(nombre_completo, deporte='mlb'):
    """
    Convierte un nombre completo en la sigla (función inversa).
    
    Args:
        nombre_completo (str): Nombre completo del equipo
        deporte (str): Deporte ('mlb', 'nba', 'nfl')
    
    Returns:
        str: Sigla del equipo o el nombre original si no se encuentra
    """
    if deporte in EQUIPOS_POR_DEPORTE:
        equipos = EQUIPOS_POR_DEPORTE[deporte]
        for sigla, nombre in equipos.items():
            if nombre.lower() == nombre_completo.lower():
                return sigla
    return nombre_completo

def listar_equipos(deporte='mlb'):
    """
    Lista todos los equipos de un deporte.
    
    Args:
        deporte (str): Deporte ('mlb', 'nba', 'nfl')
    
    Returns:
        dict: Diccionario con todas las equivalencias del deporte
    """
    return EQUIPOS_POR_DEPORTE.get(deporte, {})

# 🧪 TESTS
if __name__ == "__main__":
    # Pruebas básicas
    print("🧪 Pruebas de la función:")
    print(f"SEA -> {obtener_nombre_equipo('SEA')}")
    print(f"LAD -> {obtener_nombre_equipo('LAD')}")
    print(f"XYZ -> {obtener_nombre_equipo('XYZ')}")  # No existe
    
    print(f"\n📊 Total equipos MLB: {len(EQUIPOS_MLB)}")
    print("✅ Archivo equipos_data.py creado exitosamente!")
