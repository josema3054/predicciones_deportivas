#!/usr/bin/env python3
"""
Scripts de comandos para ejecutar funciones específicas desde consola
Ejecutar: python comandos.py [funcion] [parametros]

Ejemplos:
  python comandos.py test
  python comandos.py resultados mlb 2025-06-29
  python comandos.py consensus mlb 2025-06-29
  python comandos.py pipeline mlb 2025-06-29
  python comandos.py analisis mlb 2025-06-29
"""

import sys
import os
from datetime import datetime, timedelta

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    if os.path.exists('.env'):
        load_dotenv()
        print("📄 Variables de entorno cargadas desde .env")
except ImportError:
    pass  # dotenv no está instalado, continuar con variables del sistema

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def cmd_test():
    """Ejecuta pruebas básicas del sistema"""
    print("🧪 Ejecutando pruebas básicas...")
    
    try:
        # Verificar importaciones
        import requests
        import pandas as pd
        print("✅ Dependencias básicas OK")
        
        # Verificar archivos
        archivos = ["scraper_historico.py", "equipos_data.py", "app_streamlit.py"]
        for archivo in archivos:
            if os.path.exists(archivo):
                print(f"✅ {archivo} encontrado")
            else:
                print(f"❌ {archivo} NO encontrado")
        
        # Prueba de conexión
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get("https://www.covers.com", headers=headers, timeout=10)
        print(f"✅ Conexión web OK - Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def cmd_resultados(deporte="mlb", fecha=None):
    """Ejecuta scraping de resultados"""
    if not fecha:
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"🏆 Scrapeando resultados de {deporte.upper()} para {fecha}...")
    
    try:
        from scraper_historico import scrape_resultados_deportivos
        
        resultados = scrape_resultados_deportivos(deporte, fecha)
        
        if resultados:
            print(f"✅ {len(resultados)} resultados encontrados:")
            for i, r in enumerate(resultados[:5], 1):  # Mostrar primeros 5
                print(f"  {i}. {r['nombre_equipo_1']} vs {r['nombre_equipo_2']}: {r['puntaje_equipo_1']}-{r['puntaje_equipo_2']}")
            
            # Guardar en CSV local
            import pandas as pd
            df = pd.DataFrame(resultados)
            filename = f"{deporte}_resultados_{fecha}.csv"
            df.to_csv(filename, index=False)
            print(f"📄 Guardado en: {filename}")
        else:
            print("⚠️ No se encontraron resultados")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def cmd_consensus(deporte="mlb", fecha=None):
    """Ejecuta scraping de consensus"""
    if not fecha:
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"📊 Scrapeando consensus de {deporte.upper()} para {fecha}...")
    print("⚠️ NOTA: Requiere Chrome instalado")
    
    try:
        from scraper_historico import scrapear_consensus_por_fecha
        
        scrapear_consensus_por_fecha(fecha, deporte=deporte)
        print(f"✅ Consensus scraping completado")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica que Chrome y ChromeDriver estén instalados")

def cmd_pipeline(deporte="mlb", fecha=None):
    """Ejecuta pipeline completo"""
    if not fecha:
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"🚀 Ejecutando pipeline completo para {deporte.upper()} - {fecha}...")
    
    try:
        from scraper_historico import scrape_y_analizar_fecha_completa
        
        scrape_y_analizar_fecha_completa(deporte, fecha)
        print(f"✅ Pipeline completado")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def cmd_analisis(deporte="mlb", fecha=None):
    """Ejecuta solo análisis de efectividad"""
    if not fecha:
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"📈 Analizando efectividad para {deporte.upper()} - {fecha}...")
    
    try:
        from scraper_historico import analizar_efectividad_consensus
        
        analisis = analizar_efectividad_consensus(deporte, fecha)
        
        if "error" not in analisis:
            print(f"📊 RESULTADOS DEL ANÁLISIS:")
            print(f"   Total partidos: {analisis['total_partidos']}")
            print(f"   Con consensus: {analisis['partidos_con_consensus']}")
            print(f"   Efectividad Winners: {analisis['efectividad_winners']}%")
            print(f"   Efectividad Totals: {analisis['efectividad_totals']}%")
        else:
            print(f"❌ {analisis['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def cmd_streamlit():
    """Lanza la interfaz web"""
    print("🌐 Iniciando interfaz web Streamlit...")
    
    try:
        import subprocess
        subprocess.run(["streamlit", "run", "app_streamlit.py"])
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Instalar con: pip install streamlit")

def mostrar_ayuda():
    """Muestra ayuda de comandos"""
    print("📋 === COMANDOS DISPONIBLES ===")
    print("")
    print("🧪 PRUEBAS:")
    print("   python comandos.py test")
    print("")
    print("🏆 RESULTADOS:")
    print("   python comandos.py resultados [deporte] [fecha]")
    print("   Ejemplo: python comandos.py resultados mlb 2025-06-29")
    print("")
    print("📊 CONSENSUS:")
    print("   python comandos.py consensus [deporte] [fecha]")
    print("   Ejemplo: python comandos.py consensus mlb 2025-06-29")
    print("")
    print("🚀 PIPELINE COMPLETO:")
    print("   python comandos.py pipeline [deporte] [fecha]")
    print("   Ejemplo: python comandos.py pipeline mlb 2025-06-29")
    print("")
    print("📈 ANÁLISIS:")
    print("   python comandos.py analisis [deporte] [fecha]")
    print("   Ejemplo: python comandos.py analisis mlb 2025-06-29")
    print("")
    print("🌐 INTERFAZ WEB:")
    print("   python comandos.py streamlit")
    print("")
    print("💡 NOTAS:")
    print("   - Si no especificas fecha, usa el día anterior")
    print("   - Deportes disponibles: mlb, cfl, wnba")
    print("   - Consensus requiere Chrome instalado")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        mostrar_ayuda()
        sys.exit(1)
    
    comando = sys.argv[1].lower()
    
    if comando == "test":
        cmd_test()
    
    elif comando == "resultados":
        deporte = sys.argv[2] if len(sys.argv) > 2 else "mlb"
        fecha = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_resultados(deporte, fecha)
    
    elif comando == "consensus":
        deporte = sys.argv[2] if len(sys.argv) > 2 else "mlb"
        fecha = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_consensus(deporte, fecha)
    
    elif comando == "pipeline":
        deporte = sys.argv[2] if len(sys.argv) > 2 else "mlb"
        fecha = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_pipeline(deporte, fecha)
    
    elif comando == "analisis":
        deporte = sys.argv[2] if len(sys.argv) > 2 else "mlb"
        fecha = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_analisis(deporte, fecha)
    
    elif comando == "streamlit":
        cmd_streamlit()
    
    elif comando in ["help", "ayuda", "-h", "--help"]:
        mostrar_ayuda()
    
    else:
        print(f"❌ Comando desconocido: {comando}")
        mostrar_ayuda()
