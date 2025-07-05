#!/usr/bin/env python3
"""
Script de prueba simple para validar las funciones implementadas
Ejecutar desde consola: python test_simple.py
"""

from datetime import datetime, timedelta

def test_funciones_auxiliares():
    """Prueba las funciones auxiliares sin importar el scraper completo"""
    print("🧪 === PRUEBA DE FUNCIONES AUXILIARES ===")
    
    # Simulamos las funciones auxiliares aquí para probar independientemente
    import re
    
    def _extraer_sigla_equipo(equipo_text):
        equipo_clean = equipo_text.strip().upper()
        
        siglas_especiales = {
            "CHI. WHITE SOX": "CHW",
            "CHI. CUBS": "CHC", 
            "LA DODGERS": "LAD",
            "LA ANGELS": "LAA",
            "NY YANKEES": "NYY",
            "NY METS": "NYM",
            "ST. LOUIS": "STL",
            "SAN FRANCISCO": "SF",
            "SAN DIEGO": "SD",
            "TAMPA BAY": "TB",
            "KANSAS CITY": "KC",
            "LOS ANGELES": "LAD"
        }
        
        if equipo_clean in siglas_especiales:
            return siglas_especiales[equipo_clean]
        
        if len(equipo_clean) <= 4 and equipo_clean.isalpha():
            return equipo_clean
        
        words = equipo_clean.split()
        if len(words) >= 2:
            sigla_candidate = ''.join(word[0] for word in words if word)
            if len(sigla_candidate) <= 4:
                return sigla_candidate
        
        return None
    
    def _extraer_puntajes_final(line, sigla_1, sigla_2):
        try:
            pattern = rf'{sigla_1}\s+(\d+)\s+FINAL\s+{sigla_2}\s+(\d+)'
            match = re.search(pattern, line, re.IGNORECASE)
            
            if match:
                return {
                    "puntaje_1": int(match.group(1)),
                    "puntaje_2": int(match.group(2))
                }
        except (ValueError, AttributeError):
            pass
        return None
    
    # Probar extracción de siglas
    print("\n🔤 Prueba de extracción de siglas:")
    casos_siglas = [
        "PHILADELPHIA",
        "CHI. WHITE SOX", 
        "ST. LOUIS",
        "NY YANKEES",
        "PHI",
        "ATL"
    ]
    
    for caso in casos_siglas:
        sigla = _extraer_sigla_equipo(caso)
        print(f"   '{caso}' -> '{sigla}'")
    
    # Probar extracción de puntajes
    print("\n🎯 Prueba de extracción de puntajes:")
    casos_puntajes = [
        ("PHI 2 FINAL ATL 1", "PHI", "ATL"),
        ("TB 1 FINAL BAL 5", "TB", "BAL"),
        ("LAD 8 FINAL SD 3", "LAD", "SD")
    ]
    
    for linea, sigla1, sigla2 in casos_puntajes:
        puntajes = _extraer_puntajes_final(linea, sigla1, sigla2)
        print(f"   '{linea}' -> {puntajes}")

def test_importaciones():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n📦 === VERIFICACIÓN DE DEPENDENCIAS ===")
    
    dependencias = [
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("selenium", "selenium"),
        ("pandas", "pandas"),
        ("supabase", "supabase"),
        ("python-dotenv", "dotenv")
    ]
    
    for paquete, modulo in dependencias:
        try:
            __import__(modulo)
            print(f"   ✅ {paquete}: OK")
        except ImportError:
            print(f"   ❌ {paquete}: FALTA - instalar con: pip install {paquete}")

def test_archivos_locales():
    """Verifica que los archivos del proyecto estén presentes"""
    print("\n📁 === VERIFICACIÓN DE ARCHIVOS ===")
    
    import os
    
    archivos_requeridos = [
        "scraper_historico.py",
        "equipos_data.py",
        "app_streamlit.py",
        ".env"  # Opcional pero recomendado
    ]
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}: Encontrado")
        else:
            print(f"   ❌ {archivo}: NO encontrado")

def test_conexion_web():
    """Prueba conexión a Covers.com (sin scraping real)"""
    print("\n🌐 === PRUEBA DE CONEXIÓN WEB ===")
    
    try:
        import requests
        
        # Headers básicos
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # URL de prueba
        url = "https://www.covers.com/sports/mlb"
        
        print(f"   Probando conexión a: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Conexión exitosa - Status: {response.status_code}")
            print(f"   📄 Tamaño respuesta: {len(response.content)} bytes")
        else:
            print(f"   ⚠️ Respuesta inusual - Status: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"   ❌ Error de conexión: {e}")
    except ImportError:
        print("   ❌ requests no está instalado")

def test_variables_entorno():
    """Verifica las variables de entorno de Supabase"""
    print("\n🔐 === VERIFICACIÓN VARIABLES DE ENTORNO ===")
    
    try:
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if supabase_url:
            print(f"   ✅ SUPABASE_URL: Configurada ({supabase_url[:20]}...)")
        else:
            print("   ❌ SUPABASE_URL: NO configurada")
        
        if supabase_key:
            print(f"   ✅ SUPABASE_KEY: Configurada ({supabase_key[:20]}...)")
        else:
            print("   ❌ SUPABASE_KEY: NO configurada")
            
    except ImportError:
        print("   ❌ python-dotenv no está instalado")

if __name__ == "__main__":
    print("🚀 === INICIANDO PRUEBAS DEL SISTEMA ===")
    print(f"📅 Fecha actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar todas las pruebas
    test_importaciones()
    test_archivos_locales()
    test_variables_entorno()
    test_conexion_web()
    test_funciones_auxiliares()
    
    print("\n✅ === PRUEBAS COMPLETADAS ===")
    print("\n📋 SIGUIENTES PASOS:")
    print("   1. Si hay dependencias faltantes, instalarlas con pip")
    print("   2. Si falta .env, crear con SUPABASE_URL y SUPABASE_KEY")
    print("   3. Para prueba completa, ejecutar: python test_resultados.py")
    print("   4. Para interfaz web, ejecutar: streamlit run app_streamlit.py")
