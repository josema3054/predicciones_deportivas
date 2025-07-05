# Proyecto: Scraping histórico de pronósticos deportivos (Covers.com)
# Objetivo: Recolectar datos históricos de la sección "Consensus" de Covers para MLB (y otros deportes en el futuro),
#           recorriendo un rango de fechas y guardando los datos en Supabase y CSV.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime, timedelta, date
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import time
import requests
import re
from equipos_data import obtener_nombre_equipo
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

# === CONFIGURACIÓN DE SUPABASE ===
load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

def configurar_supabase():
    """
    Configurar la conexión a Supabase cargando las variables de entorno.
    Esta función permite que otros scripts importen y usen la configuración.
    
    Returns:
        Client: Cliente de Supabase configurado
    """
    global supabase, url, key
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise ValueError("❌ Error: Las variables SUPABASE_URL y SUPABASE_ANON_KEY deben estar configuradas en el archivo .env")
    
    supabase = create_client(url, key)
    print("✅ Conexión a Supabase configurada correctamente")
    return supabase

# === PARÁMETROS DE SCRAPING HISTÓRICO ===
# Prueba: solo los últimos 3 días
FECHA_FIN = date.today()
FECHA_INICIO = (FECHA_FIN - timedelta(days=2)).strftime("%Y-%m-%d")
FECHA_FIN = FECHA_FIN.strftime("%Y-%m-%d")
DEPORTES = ["mlb", "cfl", "wnba"]  # Puedes agregar más deportes aquí

# === FUNCIÓN DE SCRAPING POR FECHA ===
def scrapear_consensus_por_fecha(fecha_str, deporte="mlb"):
    print(f"\nScrapeando {deporte.upper()} para la fecha {fecha_str}...")
    options = Options()
    # options.add_argument("--headless")  # Descomenta para headless
    driver = webdriver.Chrome(options=options)
    url = f"https://contests.covers.com/consensus/topconsensus/{deporte}/expert/{fecha_str}"
    print(f"URL: {url}")  # Debug: verificar la URL
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
        )
        filas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        print("Filas encontradas:", len(filas))
        partidos = []
        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, "td")
            if len(columnas) < 6:
                continue
            try:
                # Debug: mostrar contenido de columnas
                print(f"\nDEBUG COLUMNAS WINNERS ({len(columnas)} columnas):")
                for i, col in enumerate(columnas):
                    print(f"  Columna {i}: '{col.text.strip()}'")
                
                matchup_raw = columnas[0].text.strip()
                matchup_lines = matchup_raw.split('\n')
                deporte_raw = matchup_lines[0] if len(matchup_lines) > 0 else None
                equipo_1_sigla = matchup_lines[1] if len(matchup_lines) > 1 else None
                equipo_2_sigla = matchup_lines[2] if len(matchup_lines) > 2 else None
                
                # 🏆 CONVERTIR SIGLAS A NOMBRES COMPLETOS
                equipo_1 = obtener_nombre_equipo(equipo_1_sigla, deporte.lower()) if equipo_1_sigla else None
                equipo_2 = obtener_nombre_equipo(equipo_2_sigla, deporte.lower()) if equipo_2_sigla else None
                
                print(f"🏆 CONVERSIÓN: {equipo_1_sigla} -> {equipo_1}")
                print(f"🏆 CONVERSIÓN: {equipo_2_sigla} -> {equipo_2}")
                
                # 🕐 CONVERTIR FECHA DE TEXTO A FORMATO ESTÁNDAR
                fecha_hora_raw = columnas[1].text.strip()
                fecha_hora = convertir_fecha_texto_a_estandar(fecha_hora_raw, fecha_str)
                print(f"🕐 FECHA CONVERSIÓN: '{fecha_hora_raw}' -> '{fecha_hora}'")
                
                consensus_str = columnas[2].text.strip()
                consensus_parts = consensus_str.replace('%', '').split('\n')
                
                # Para Top Consensus, los datos vienen como "74%" y "26%"
                consensus_1 = None
                consensus_2 = None
                if len(consensus_parts) > 0 and consensus_parts[0].strip() != '':
                    try:
                        consensus_1 = f"{int(consensus_parts[0].strip())}%"
                    except (ValueError, IndexError):
                        consensus_1 = None
                        
                if len(consensus_parts) > 1 and consensus_parts[1].strip() != '':
                    try:
                        consensus_2 = f"{int(consensus_parts[1].strip())}%"
                    except (ValueError, IndexError):
                        consensus_2 = None
                        
                sides_str = columnas[3].text.strip()
                sides_parts = sides_str.split('\n')
                side_1 = sides_parts[0] if len(sides_parts) > 0 else None
                side_2 = sides_parts[1] if len(sides_parts) > 1 else None
                picks_str = columnas[4].text.strip()
                print(f"DEBUG PICKS WINNERS: '{picks_str}'")  # Debug para ver qué contiene
                picks_parts = picks_str.split('\n')
                picks_1 = int(picks_parts[0]) if len(picks_parts) > 0 and picks_parts[0].strip() != '' else None
                picks_2 = int(picks_parts[1]) if len(picks_parts) > 1 and picks_parts[1].strip() != '' else None
                print(f"DEBUG: picks_1 = {picks_1}, picks_2 = {picks_2}")  # Debug
                partido = {
                    "deporte": deporte_raw,
                    "equipo_1": equipo_1,
                    "equipo_2": equipo_2,
                    "equipo_1_sigla": equipo_1_sigla,  # 🆕 SIGLA ORIGINAL
                    "equipo_2_sigla": equipo_2_sigla,  # 🆕 SIGLA ORIGINAL
                    "fecha_hora": fecha_hora,
                    "consensus_equipo_1": consensus_1,
                    "consensus_equipo_2": consensus_2,
                    "side_equipo_1": side_1,
                    "side_equipo_2": side_2,
                    "picks_equipo_1": picks_1,
                    "picks_equipo_2": picks_2,
                    "fecha_scraping": fecha_str
                }
                # Solo insertar si consensus_equipo_1 y consensus_equipo_2 no son None
                if consensus_1 is not None and consensus_2 is not None:
                    # Verificar si ya existe un registro con estos datos
                    try:
                        deporte_upper = deporte.upper()  # Normalizar a mayúscula
                        existing = supabase.table("mlb_consensus").select("id").eq("deporte", deporte_upper).eq("equipo_1_sigla", equipo_1_sigla).eq("equipo_2_sigla", equipo_2_sigla).eq("fecha_scraping", fecha_str).execute()
                        
                        if len(existing.data) == 0:
                            # No existe, insertar nuevo registro
                            supabase.table("mlb_consensus").insert(partido).execute()
                            partidos.append(partido)
                            print(f"✅ Nuevo registro guardado: {equipo_1} vs {equipo_2}")
                        else:
                            print(f"🔄 Registro ya existe: {equipo_1} vs {equipo_2} - Omitido")
                    except Exception as e:
                        print(f"⚠️ Error al verificar/insertar: {e}")
                else:
                    print(f"Fila ignorada por consensus_equipo_1 o consensus_equipo_2 nulo: {partido}")
            except Exception as e:
                print("⚠️ Error en fila:", e)
        # Guardar backup local
        if partidos:
            df = pd.DataFrame(partidos)
            df.to_csv(f"mlb_consensus_{fecha_str}.csv", index=False)
            print(f"Archivo guardado: mlb_consensus_{fecha_str}.csv")
        else:
            print("No se encontraron partidos para esta fecha.")
    except Exception as e:
        print(f"❌ Error al scrapear {fecha_str}: {e}")
    finally:
        driver.quit()

# === FUNCIÓN DE SCRAPING PARA TOTALS ===
def scrapear_consensus_totals_por_fecha(fecha_str, deporte="mlb"):
    print(f"\nScrapeando TOTALS {deporte.upper()} para la fecha {fecha_str}...")
    options = Options()
    # options.add_argument("--headless")  # Descomenta para headless
    driver = webdriver.Chrome(options=options)
    url = f"https://contests.covers.com/consensus/topoverunderconsensus/{deporte}/expert/{fecha_str}"
    print(f"URL TOTALS: {url}")  # Debug: verificar la URL
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
        )
        filas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        print("Filas encontradas:", len(filas))
        partidos = []
        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, "td")
            if len(columnas) < 6:
                continue
            try:
                # Debug: mostrar el contenido de todas las columnas
                print(f"\nDEBUG COLUMNAS ({len(columnas)} columnas):")
                for i, col in enumerate(columnas):
                    print(f"  Columna {i}: '{col.text.strip()}'")
                
                matchup_raw = columnas[0].text.strip()
                matchup_lines = matchup_raw.split('\n')
                deporte_data = matchup_lines[0] if len(matchup_lines) > 0 else None
                equipo_1_sigla = matchup_lines[1] if len(matchup_lines) > 1 else None
                equipo_2_sigla = matchup_lines[2] if len(matchup_lines) > 2 else None
                
                # 🏆 CONVERTIR SIGLAS A NOMBRES COMPLETOS
                equipo_1 = obtener_nombre_equipo(equipo_1_sigla, deporte.lower()) if equipo_1_sigla else None
                equipo_2 = obtener_nombre_equipo(equipo_2_sigla, deporte.lower()) if equipo_2_sigla else None
                
                print(f"🏆 TOTALS CONVERSIÓN: {equipo_1_sigla} -> {equipo_1}")
                print(f"🏆 TOTALS CONVERSIÓN: {equipo_2_sigla} -> {equipo_2}")
                
                # 🕐 CONVERTIR FECHA DE TEXTO A FORMATO ESTÁNDAR
                fecha_hora_raw = columnas[1].text.strip()
                fecha_hora = convertir_fecha_texto_a_estandar(fecha_hora_raw, fecha_str)
                print(f"🕐 TOTALS FECHA CONVERSIÓN: '{fecha_hora_raw}' -> '{fecha_hora}'")
                
                # Para totals, viene como "74 Under" y "26 Over"
                consensus_str = columnas[2].text.strip()
                consensus_parts = consensus_str.replace('%', '').split('\n')
                
                consensus_over = None
                consensus_under = None
                side_over = "Over"
                side_under = "Under"
                
                # Extraer porcentajes y determinar cuál es over/under
                for part in consensus_parts:
                    if part.strip():
                        try:
                            parts = part.strip().split()
                            porcentaje = int(parts[0])
                            tipo = parts[1] if len(parts) > 1 else ""
                            
                            if "Over" in tipo:
                                consensus_over = f"{porcentaje}%"
                            elif "Under" in tipo:
                                consensus_under = f"{porcentaje}%"
                        except (ValueError, IndexError):
                            continue
                
                # Extraer picks (vienen como números separados por línea)
                picks_str = columnas[4].text.strip()
                print(f"DEBUG PICKS: '{picks_str}'")  # Debug para ver qué contiene
                picks_parts = picks_str.split('\n')
                
                picks_over = None
                picks_under = None
                
                # Los picks vienen en el mismo orden que el consensus
                # Necesitamos determinar cuál es over y cuál es under basado en el consensus
                if len(picks_parts) >= 2:
                    try:
                        pick1 = int(picks_parts[0].strip())
                        pick2 = int(picks_parts[1].strip())
                        
                        # Determinar qué pick corresponde a over/under basado en el consensus
                        # Si consensus_over tiene mayor porcentaje, pick1 es over, pick2 es under
                        if consensus_over and consensus_under:
                            over_pct = int(consensus_over.replace('%', ''))
                            under_pct = int(consensus_under.replace('%', ''))
                            
                            if over_pct > under_pct:
                                picks_over = pick1
                                picks_under = pick2
                            else:
                                picks_over = pick2
                                picks_under = pick1
                                
                        print(f"DEBUG: picks_over = {picks_over}, picks_under = {picks_under}")
                    except (ValueError, IndexError) as e:
                        print(f"DEBUG: Error parsing picks: {e}")
                        picks_over = None
                        picks_under = None
                
                # Extraer línea total (puede estar en columna 3 o 5)
                linea_total = columnas[3].text.strip() if len(columnas) > 3 else None
                
                partido = {
                    "deporte": deporte,
                    "equipo_1": equipo_1,
                    "equipo_2": equipo_2,
                    "equipo_1_sigla": equipo_1_sigla,  # 🆕 SIGLA ORIGINAL
                    "equipo_2_sigla": equipo_2_sigla,  # 🆕 SIGLA ORIGINAL
                    "fecha_hora": fecha_hora,
                    "consensus_over": consensus_over,
                    "consensus_under": consensus_under,
                    "side_over": side_over,
                    "side_under": side_under,
                    "picks_over": picks_over,
                    "picks_under": picks_under,
                    "linea_total": linea_total,
                    "fecha_scraping": fecha_str
                }
                
                # Solo insertar si tenemos datos válidos
                if consensus_over is not None and consensus_under is not None:
                    # Verificar si ya existe
                    try:
                        deporte_upper = deporte.upper()  # Normalizar a mayúscula
                        existing = supabase.table("consensus_totals").select("id").eq("deporte", deporte_upper).eq("equipo_1", equipo_1).eq("equipo_2", equipo_2).eq("fecha_hora", fecha_hora).eq("fecha_scraping", fecha_str).execute()
                        
                        if len(existing.data) == 0:
                            supabase.table("consensus_totals").insert(partido).execute()
                            partidos.append(partido)
                            print(f"✅ Nuevo registro TOTALS guardado: {equipo_1} vs {equipo_2}")
                        else:
                            print(f"🔄 Registro TOTALS ya existe: {equipo_1} vs {equipo_2} - Omitido")
                    except Exception as e:
                        print(f"⚠️ Error al verificar/insertar TOTALS: {e}")
                else:
                    print(f"Fila TOTALS ignorada por consensus nulo: {partido}")
            except Exception as e:
                print("⚠️ Error en fila TOTALS:", e)
        
        # Guardar backup local
        if partidos:
            df = pd.DataFrame(partidos)
            df.to_csv(f"{deporte}_consensus_totals_{fecha_str}.csv", index=False)
            print(f"Archivo TOTALS guardado: {deporte}_consensus_totals_{fecha_str}.csv")
        else:
            print("No se encontraron partidos TOTALS para esta fecha.")
    except Exception as e:
        print(f"❌ Error al scrapear TOTALS {fecha_str}: {e}")
    finally:
        driver.quit()

# === FUNCIÓN DE SCRAPING DE RESULTADOS DEPORTIVOS ===
def scrape_resultados_deportivos(deporte: str, fecha: str) -> List[Dict]:
    """
    Extrae resultados reales de partidos deportivos desde Covers.com usando Selenium
    
    Esta función obtiene los resultados finales de partidos para análisis
    de efectividad del consensus de apuestas. Ahora usa Selenium para mayor
    robustez y consistencia con las otras fases del scraper.
    
    Args:
        deporte (str): Código del deporte ('mlb', 'cfl', 'wnba', etc.)
        fecha (str): Fecha en formato 'YYYY-MM-DD'
    
    Returns:
        List[Dict]: Lista de diccionarios con resultados de partidos
        
    Ejemplo de retorno:
        [
            {
                "deporte": "mlb",
                "fecha_partido": "2025-06-29",
                "sigla_equipo_1": "PHI",
                "sigla_equipo_2": "ATL", 
                "nombre_equipo_1": "Philadelphia Phillies",
                "nombre_equipo_2": "Atlanta Braves",
                "puntaje_equipo_1": 2,
                "puntaje_equipo_2": 1,
                "resultado_sigla": "PHI",
                "resultado_nombre": "Philadelphia Phillies",
                "total_puntos": 3,
                "linea_total": 8.0,
                "over_under": "under",
                "margen_ou": -5.0,
                "odds_ganador": "+140",
                "estado_partido": "final",
                "fecha_scraping": "2025-06-30"
            }
        ]
    """
    
    # Configurar Chrome options (modo headless para resultados)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Inicializar driver
    driver = webdriver.Chrome(options=chrome_options)
    resultados = []
    
    try:
        # Construir URL de la página de resultados
        url = f"https://www.covers.com/sports/{deporte}/matchups/{fecha}"
        print(f"🔍 Scrapeando resultados de {deporte.upper()} para {fecha}...")
        print(f"📍 URL: {url}")
        
        # Navegar a la página
        driver.get(url)
        time.sleep(3)  # Esperar a que cargue la página
        
        # Buscar partidos finalizados
        try:
            # Buscar elementos que contengan información de partidos
            game_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid*='matchup'], .CMsGameBox, .game-box, .matchup-card")
            
            if not game_elements:
                # Usar directamente la nueva función de búsqueda de puntajes
                resultados = _buscar_resultados_por_puntajes_final(driver, deporte, fecha)
            
            else:
                print(f"🎮 Encontrados {len(game_elements)} elementos de partidos")
                
                # Procesar cada elemento de partido
                for game_elem in game_elements:
                    try:
                        # Verificar si el partido está finalizado
                        game_html = game_elem.get_attribute('outerHTML')
                        if 'FINAL' in game_html.upper():
                            resultado = _procesar_elemento_partido_selenium(game_elem, deporte, fecha)
                            if resultado:
                                resultados.append(resultado)
                    except Exception as e:
                        print(f"⚠️ Error procesando elemento de partido: {e}")
                        continue
        
        except Exception as e:
            print(f"⚠️ Error buscando elementos de partidos: {e}")
            # Fallback final: usar parsing de texto completo
            resultados = _fallback_parsing_texto_completo(driver, deporte, fecha)
        
        print(f"📊 Total de resultados encontrados: {len(resultados)}")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Error al scrapear resultados para {deporte} {fecha}: {e}")
        return []
    finally:
        driver.quit()


def _extraer_contexto_partido_selenium(parent_element, deporte: str) -> Optional[Dict]:
    """
    Extrae información del partido desde el elemento padre que contiene "FINAL"
    """
    try:
        # Obtener todo el texto del contexto
        context_text = parent_element.get_text()
        
        # Buscar patrones de equipos y puntajes
        lines = [line.strip() for line in context_text.split('\n') if line.strip()]
        
        # Buscar línea con equipos (formato: EQUIPO @ EQUIPO o EQUIPO vs EQUIPO)
        matchup_line = None
        for line in lines:
            if '@' in line or ' vs ' in line:
                matchup_line = line
                break
        
        if not matchup_line:
            return None
        
        # Extraer equipos
        if '@' in matchup_line:
            equipo_1_raw, equipo_2_raw = matchup_line.split('@')
        else:
            equipo_1_raw, equipo_2_raw = matchup_line.split(' vs ')
        
        equipo_1_raw = equipo_1_raw.strip()
        equipo_2_raw = equipo_2_raw.strip()
        
        # Obtener siglas
        sigla_1 = _extraer_sigla_equipo(equipo_1_raw)
        sigla_2 = _extraer_sigla_equipo(equipo_2_raw)
        
        if not sigla_1 or not sigla_2:
            return None
        
        # Buscar puntajes
        puntajes = _buscar_puntajes_en_texto(context_text, sigla_1, sigla_2)
        
        if not puntajes:
            return None
        
        # Determinar ganador
        if puntajes['puntaje_1'] > puntajes['puntaje_2']:
            resultado_sigla = sigla_1
            resultado_nombre = obtener_nombre_equipo(sigla_1, deporte)
        elif puntajes['puntaje_2'] > puntajes['puntaje_1']:
            resultado_sigla = sigla_2
            resultado_nombre = obtener_nombre_equipo(sigla_2, deporte)
        else:
            resultado_sigla = "TIE"
            resultado_nombre = "Empate"
        
        # Construir resultado
        resultado = {
            "deporte": deporte,
            "fecha_partido": datetime.now().strftime("%Y-%m-%d"),  # Se actualizará con fecha real
            "sigla_equipo_1": sigla_1,
            "sigla_equipo_2": sigla_2,
            "nombre_equipo_1": obtener_nombre_equipo(sigla_1, deporte),
            "nombre_equipo_2": obtener_nombre_equipo(sigla_2, deporte),
            "puntaje_equipo_1": puntajes['puntaje_1'],
            "puntaje_equipo_2": puntajes['puntaje_2'],
            "resultado_sigla": resultado_sigla,
            "resultado_nombre": resultado_nombre,
            "total_puntos": puntajes['puntaje_1'] + puntajes['puntaje_2'],
            "linea_total": None,
            "over_under": None,
            "margen_ou": None,
            "odds_ganador": None,
            "estado_partido": "final",
            "fecha_scraping": datetime.now().strftime("%Y-%m-%d")
        }
        
        return resultado
        
    except Exception as e:
        print(f"⚠️ Error extrayendo contexto: {e}")
        return None


def _procesar_elemento_partido_selenium(game_elem, deporte: str, fecha: str) -> Optional[Dict]:
    """
    Procesa un elemento específico de partido usando Selenium
    """
    try:
        # Obtener texto del elemento
        game_text = game_elem.text
        
        # Buscar equipos y puntajes en el texto
        lines = [line.strip() for line in game_text.split('\n') if line.strip()]
        
        # Similar lógica que en la versión BeautifulSoup pero adaptada para Selenium
        current_matchup = None
        
        for i, line in enumerate(lines):
            if '@' in line and len(line.split('@')) == 2:
                matchup_parts = line.split('@')
                equipo_1_raw = matchup_parts[0].strip()
                equipo_2_raw = matchup_parts[1].strip()
                
                sigla_1 = _extraer_sigla_equipo(equipo_1_raw)
                sigla_2 = _extraer_sigla_equipo(equipo_2_raw)
                
                if sigla_1 and sigla_2:
                    current_matchup = {
                        'sigla_equipo_1': sigla_1,
                        'sigla_equipo_2': sigla_2,
                        'nombre_equipo_1': obtener_nombre_equipo(sigla_1, deporte),
                        'nombre_equipo_2': obtener_nombre_equipo(sigla_2, deporte)
                    }
            
            elif current_matchup and line.upper() == 'FINAL':
                # Buscar puntajes
                puntajes = _buscar_puntajes_cerca_de_final(lines, i, current_matchup)
                
                if puntajes:
                    # Determinar ganador
                    if puntajes['puntaje_1'] > puntajes['puntaje_2']:
                        resultado_sigla = current_matchup['sigla_equipo_1']
                        resultado_nombre = current_matchup['nombre_equipo_1']
                    else:
                        resultado_sigla = current_matchup['sigla_equipo_2']
                        resultado_nombre = current_matchup['nombre_equipo_2']
                    
                    resultado = {
                        "deporte": deporte,
                        "fecha_partido": fecha,
                        "sigla_equipo_1": current_matchup['sigla_equipo_1'],
                        "sigla_equipo_2": current_matchup['sigla_equipo_2'],
                        "nombre_equipo_1": current_matchup['nombre_equipo_1'],
                        "nombre_equipo_2": current_matchup['nombre_equipo_2'],
                        "puntaje_equipo_1": puntajes['puntaje_1'],
                        "puntaje_equipo_2": puntajes['puntaje_2'],
                        "resultado_sigla": resultado_sigla,
                        "resultado_nombre": resultado_nombre,
                        "total_puntos": puntajes['puntaje_1'] + puntajes['puntaje_2'],
                        "linea_total": None,
                        "over_under": None,
                        "margen_ou": None,
                        "odds_ganador": None,
                        "estado_partido": "final",
                        "fecha_scraping": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    return resultado
        
        return None
        
    except Exception as e:
        print(f"⚠️ Error procesando elemento: {e}")
        return None


def _buscar_resultados_por_puntajes_final(driver, deporte: str, fecha: str) -> List[Dict]:
    """
    Busca resultados usando la estructura específica donde los puntajes están en <strong>
    que contienen 'team-score' en sus clases, cerca de elementos que contienen "Final"
    """
    try:
        print("🔍 Buscando resultados con estructura específica de puntajes...")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        resultados = []
        
        # Buscar todos los elementos <strong> que contengan 'team-score' en sus clases
        all_score_elements = soup.find_all('strong', class_=lambda x: x and 'team-score' in x)
        print(f"📊 Encontrados {len(all_score_elements)} elementos team-score")
        
        # Agrupar puntajes por contenedor que tenga "Final"
        partidos_procesados = set()
        
        for score_elem in all_score_elements:
            try:
                # Verificar si este puntaje está cerca de un "Final"
                container = score_elem.parent
                found_final = False
                final_container = None
                
                # Buscar "Final" en contenedores padre (hasta nivel 3)
                for level in range(4):
                    if container:
                        container_text = container.get_text().upper()
                        if 'FINAL' in container_text and 'NBA FINALS' not in container_text:
                            found_final = True
                            final_container = container
                            break
                        container = container.parent
                    else:
                        break
                
                if found_final and final_container:
                    # Crear un identificador único para este contenedor basado en el texto
                    container_text = final_container.get_text().strip()
                    container_id = hash(container_text)
                    
                    if container_id not in partidos_procesados:
                        partidos_procesados.add(container_id)
                        
                        # Buscar todos los puntajes en este contenedor
                        score_elements_in_container = final_container.find_all('strong', class_=lambda x: x and 'team-score' in x)
                        
                        if len(score_elements_in_container) >= 2:
                            resultado = _extraer_partido_de_contenedor_mejorado(final_container, score_elements_in_container, deporte, fecha)
                            if resultado:
                                resultados.append(resultado)
                                print(f"✅ Partido encontrado: {resultado['sigla_equipo_1']} {resultado['puntaje_equipo_1']} - {resultado['puntaje_equipo_2']} {resultado['sigla_equipo_2']}")
                            
            except Exception as e:
                print(f"⚠️ Error procesando elemento score: {e}")
                continue
        
        print(f"📊 Total de partidos encontrados: {len(resultados)}")
        return resultados
        
    except Exception as e:
        print(f"⚠️ Error en búsqueda por puntajes FINAL: {e}")
        return []


def _extraer_partido_de_contenedor_mejorado(container, score_elements, deporte: str, fecha: str) -> Optional[Dict]:
    """
    Versión mejorada que extrae información del partido desde un contenedor con puntajes
    """
    try:
        # Extraer puntajes válidos (solo tomar los primeros 2 únicos)
        puntajes_unicos = []
        for score_elem in score_elements:
            score_text = score_elem.get_text().strip()
            try:
                puntaje = int(score_text)
                if puntaje not in puntajes_unicos:  # Evitar duplicados
                    puntajes_unicos.append(puntaje)
                if len(puntajes_unicos) >= 2:  # Solo necesitamos 2
                    break
            except ValueError:
                continue
        
        if len(puntajes_unicos) < 2:
            return None
        
        puntaje_1, puntaje_2 = puntajes_unicos[0], puntajes_unicos[1]
        
        # Buscar siglas de equipos en el contenedor y contenedores padre
        equipos_encontrados = []
        
        # Expandir búsqueda a contenedores hermanos y padre
        search_containers = [container]
        if container.parent:
            search_containers.append(container.parent)
            # También buscar en contenedores hermanos
            for sibling in container.parent.find_all():
                if sibling != container:
                    search_containers.append(sibling)
        
        from equipos_data import EQUIPOS_MLB
        
        for search_container in search_containers:
            container_text = search_container.get_text().upper()
            
            for sigla in EQUIPOS_MLB.keys():
                if sigla in container_text and sigla not in equipos_encontrados:
                    equipos_encontrados.append(sigla)
                    if len(equipos_encontrados) >= 2:
                        break
            
            if len(equipos_encontrados) >= 2:
                break
        
        if len(equipos_encontrados) >= 2:
            # Ordenar equipos y puntajes basándose en la posición en el texto
            container_text = container.get_text()
            equipo_positions = []
            
            for i, sigla in enumerate(equipos_encontrados[:2]):
                position = container_text.find(sigla)
                equipo_positions.append((position, sigla, puntajes_unicos[i]))
            
            # Ordenar por posición en el texto
            equipo_positions.sort(key=lambda x: x[0])
            
            # Extraer equipos y puntajes ordenados
            sigla_1 = equipo_positions[0][1]
            puntaje_1 = equipo_positions[0][2]
            sigla_2 = equipo_positions[1][1]
            puntaje_2 = equipo_positions[1][2]
            
            # Determinar ganador
            if puntaje_1 > puntaje_2:
                resultado_sigla = sigla_1
                resultado_nombre = obtener_nombre_equipo(sigla_1, deporte)
            elif puntaje_2 > puntaje_1:
                resultado_sigla = sigla_2
                resultado_nombre = obtener_nombre_equipo(sigla_2, deporte)
            else:
                resultado_sigla = "TIE"
                resultado_nombre = "Empate"
            
            resultado = {
                "deporte": deporte,
                "fecha_partido": fecha,
                "sigla_equipo_1": sigla_1,
                "sigla_equipo_2": sigla_2,
                "nombre_equipo_1": obtener_nombre_equipo(sigla_1, deporte),
                "nombre_equipo_2": obtener_nombre_equipo(sigla_2, deporte),
                "puntaje_equipo_1": puntaje_1,
                "puntaje_equipo_2": puntaje_2,
                "resultado_sigla": resultado_sigla,
                "resultado_nombre": resultado_nombre,
                "total_puntos": puntaje_1 + puntaje_2,
                "linea_total": None,
                "over_under": None,
                "margen_ou": None,
                "odds_ganador": None,
                "estado_partido": "final",
                "fecha_scraping": datetime.now().strftime("%Y-%m-%d")
            }
            
            return resultado
        
        return None
        
    except Exception as e:
        print(f"⚠️ Error extrayendo partido mejorado: {e}")
        return None


def _extraer_partido_de_contenedor(container, score_elements, deporte: str, fecha: str) -> Optional[Dict]:
    """
    Extrae información completa del partido desde un contenedor que tiene puntajes
    """
    try:
        # Extraer puntajes de los elementos <strong> que contienen class="team-score"
        puntajes = []
        for score_elem in score_elements:
            score_text = score_elem.get_text().strip()
            try:
                puntaje = int(score_text)
                puntajes.append(puntaje)
            except ValueError:
                continue
        
        if len(puntajes) < 2:
            return None
        
        # Tomar los primeros dos puntajes válidos
        puntaje_1, puntaje_2 = puntajes[0], puntajes[1]
        
        # Buscar información de equipos en el contenedor y contenedores padre
        equipos_encontrados = []
        
        # Buscar en varios niveles del DOM
        current_container = container
        for _ in range(5):  # Buscar hasta 5 niveles arriba
            if current_container:
                container_text = current_container.get_text().upper()
                
                # Buscar siglas conocidas en el texto
                from equipos_data import EQUIPOS_MLB
                for sigla in EQUIPOS_MLB.keys():
                    if sigla in container_text and sigla not in equipos_encontrados:
                        equipos_encontrados.append(sigla)
                        if len(equipos_encontrados) >= 2:
                            break
                
                if len(equipos_encontrados) >= 2:
                    break
                    
                current_container = current_container.parent
            else:
                break
        
        # Si encontramos exactamente 2 equipos, usarlos
        if len(equipos_encontrados) >= 2:
            sigla_1 = equipos_encontrados[0]
            sigla_2 = equipos_encontrados[1]
            
            # Determinar ganador
            if puntaje_1 > puntaje_2:
                resultado_sigla = sigla_1
                resultado_nombre = obtener_nombre_equipo(sigla_1, deporte)
            elif puntaje_2 > puntaje_1:
                resultado_sigla = sigla_2
                resultado_nombre = obtener_nombre_equipo(sigla_2, deporte)
            else:
                resultado_sigla = "TIE"
                resultado_nombre = "Empate"
            
            resultado = {
                "deporte": deporte,
                "fecha_partido": fecha,
                "sigla_equipo_1": sigla_1,
                "sigla_equipo_2": sigla_2,
                "nombre_equipo_1": obtener_nombre_equipo(sigla_1, deporte),
                "nombre_equipo_2": obtener_nombre_equipo(sigla_2, deporte),
                "puntaje_equipo_1": puntaje_1,
                "puntaje_equipo_2": puntaje_2,
                "resultado_sigla": resultado_sigla,
                "resultado_nombre": resultado_nombre,
                "total_puntos": puntaje_1 + puntaje_2,
                "linea_total": None,
                "over_under": None,
                "margen_ou": None,
                "odds_ganador": None,
                "estado_partido": "final",
                "fecha_scraping": datetime.now().strftime("%Y-%m-%d")
            }
            
            return resultado
        
        return None
        
    except Exception as e:
        print(f"⚠️ Error extrayendo partido de contenedor: {e}")
        return None


def _fallback_parsing_texto_completo(driver, deporte: str, fecha: str) -> List[Dict]:
    """
    Último recurso: parsing completo del texto de la página
    """
    try:
        # Obtener todo el texto de la página
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Usar la lógica de parsing existente
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        resultados = []
        current_matchup = None
        
        for i, line in enumerate(lines):
            if '@' in line and len(line.split('@')) == 2:
                matchup_parts = line.split('@')
                equipo_1_raw = matchup_parts[0].strip()
                equipo_2_raw = matchup_parts[1].strip()
                
                sigla_1 = _extraer_sigla_equipo(equipo_1_raw)
                sigla_2 = _extraer_sigla_equipo(equipo_2_raw)
                
                if sigla_1 and sigla_2:
                    current_matchup = {
                        'sigla_equipo_1': sigla_1,
                        'sigla_equipo_2': sigla_2,
                        'nombre_equipo_1': obtener_nombre_equipo(sigla_1, deporte),
                        'nombre_equipo_2': obtener_nombre_equipo(sigla_2, deporte)
                    }
            
            elif current_matchup and line.upper() == 'FINAL':
                puntajes = _buscar_puntajes_cerca_de_final(lines, i, current_matchup)
                
                if puntajes:
                    if puntajes['puntaje_1'] > puntajes['puntaje_2']:
                        resultado_sigla = current_matchup['sigla_equipo_1']
                        resultado_nombre = current_matchup['nombre_equipo_1']
                    else:
                        resultado_sigla = current_matchup['sigla_equipo_2']
                        resultado_nombre = current_matchup['nombre_equipo_2']
                    
                    resultado = {
                        "deporte": deporte,
                        "fecha_partido": fecha,
                        "sigla_equipo_1": current_matchup['sigla_equipo_1'],
                        "sigla_equipo_2": current_matchup['sigla_equipo_2'],
                        "nombre_equipo_1": current_matchup['nombre_equipo_1'],
                        "nombre_equipo_2": current_matchup['nombre_equipo_2'],
                        "puntaje_equipo_1": puntajes['puntaje_1'],
                        "puntaje_equipo_2": puntajes['puntaje_2'],
                        "resultado_sigla": resultado_sigla,
                        "resultado_nombre": resultado_nombre,
                        "total_puntos": puntajes['puntaje_1'] + puntajes['puntaje_2'],
                        "linea_total": None,
                        "over_under": None,
                        "margen_ou": None,
                        "odds_ganador": None,
                        "estado_partido": "final",
                        "fecha_scraping": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    resultados.append(resultado)
                    current_matchup = None
        
        return resultados
        
    except Exception as e:
        print(f"⚠️ Error en fallback parsing: {e}")
        return []


def _extraer_sigla_equipo(equipo_text: str) -> Optional[str]:
    """
    Extrae la sigla del equipo desde texto que puede contener ciudad y nombre.
    
    Ejemplos:
        "PHILADELPHIA" -> "PHI" (no implementado, devuelve texto)
        "CHI. WHITE SOX" -> "CHW" (busca en diccionario)
        "ST. LOUIS" -> "STL" (busca en diccionario)
    """
    # Limpiar texto
    equipo_clean = equipo_text.strip().upper()
    
    # Casos especiales comunes
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
        "LOS ANGELES": "LAD"  # Por defecto Dodgers, puede necesitar contexto
    }
    
    if equipo_clean in siglas_especiales:
        return siglas_especiales[equipo_clean]
    
    # Si es una sigla conocida de 2-4 caracteres, devolverla
    if len(equipo_clean) <= 4 and equipo_clean.isalpha():
        return equipo_clean
    
    # Intentar extraer sigla de múltiples palabras
    words = equipo_clean.split()
    if len(words) >= 2:
        # Intentar primera letra de cada palabra
        sigla_candidate = ''.join(word[0] for word in words if word)
        if len(sigla_candidate) <= 4:
            return sigla_candidate
    
    return None


def _extraer_puntajes_final(line: str, sigla_1: str, sigla_2: str) -> Optional[Dict]:
    """
    Extrae puntajes de una línea que contiene resultado final.
    
    Ejemplos:
        "PHI 2 FINAL ATL 1" -> {"puntaje_1": 2, "puntaje_2": 1}
        "TB 1 FINAL BAL 5" -> {"puntaje_1": 1, "puntaje_2": 5}
    """
    try:
        # Buscar patrón: SIGLA NUMERO FINAL SIGLA NUMERO
        pattern = rf'{sigla_1}\s+(\d+)\s+FINAL\s+{sigla_2}\s+(\d+)'
        match = re.search(pattern, line, re.IGNORECASE)
        
        if match:
            return {
                "puntaje_1": int(match.group(1)),
                "puntaje_2": int(match.group(2))
            }
        
        # Patrón alternativo con enlaces o texto adicional
        pattern2 = rf'(\d+)\s+FINAL\s+.*?(\d+)'
        matches = re.findall(pattern2, line)
        
        if matches and len(matches[0]) == 2:
            return {
                "puntaje_1": int(matches[0][0]),
                "puntaje_2": int(matches[0][1])
            }
            
    except (ValueError, AttributeError):
        pass
    
    return None


def _buscar_odds_y_totals(lines: List[str]) -> Dict:
    """
    Busca información de cuotas y líneas totales en líneas de texto.
    
    Busca patrones como:
        "+140", "-120", "o/u Margin u5", "total score of 3 was under 8"
    """
    info = {}
    
    for line in lines:
        line = line.strip()
        
        # Buscar cuotas (formato +XXX o -XXX)
        odds_match = re.search(r'([+-]\d+)', line)
        if odds_match and 'odds' not in info:
            info['odds'] = odds_match.group(1)
        
        # Buscar línea total en descripción
        total_match = re.search(r'total score of \d+ was (?:over|under) ([\d.]+)', line, re.IGNORECASE)
        if total_match:
            info['linea_total'] = total_match.group(1)
        
        # Buscar margen O/U
        margin_match = re.search(r'o/u\s+margin\s*([ou])?([\d.]+)', line, re.IGNORECASE)
        if margin_match and 'margen_ou' not in info:
            direction = margin_match.group(1)
            value = margin_match.group(2)
            info['margen_ou_raw'] = f"{direction}{value}" if direction else value
    
    return info


def _buscar_puntajes_cerca_de_final(lines: List[str], final_index: int, matchup: Dict) -> Optional[Dict]:
    """
    Busca puntajes en las líneas alrededor de donde aparece 'FINAL'.
    La estructura típica es:
    
    [puntaje1]
    Final
    [puntaje2]
    
    O variaciones como puntajes antes del final.
    """
    try:
        # Rango de búsqueda alrededor del índice donde aparece "Final"
        start_idx = max(0, final_index - 5)
        end_idx = min(len(lines), final_index + 5)
        
        search_lines = lines[start_idx:end_idx]
        puntajes_encontrados = []
        
        print(f"🔍 Buscando puntajes alrededor de FINAL (líneas {start_idx}-{end_idx}):")
        for i, line in enumerate(search_lines):
            print(f"   {start_idx + i}: '{line}'")
            
            # Buscar números que parezcan puntajes (solo dígitos, rango típico de baseball)
            if line.isdigit() and 0 <= int(line) <= 50:
                puntajes_encontrados.append({
                    'puntaje': int(line),
                    'posicion': start_idx + i,
                    'distancia_del_final': abs((start_idx + i) - final_index)
                })
        
        print(f"🎯 Puntajes candidatos encontrados: {puntajes_encontrados}")
        
        # Si encontramos exactamente 2 puntajes, usar esos
        if len(puntajes_encontrados) == 2:
            # Ordenar por posición para mantener el orden correcto
            puntajes_encontrados.sort(key=lambda x: x['posicion'])
            
            return {
                "puntaje_1": puntajes_encontrados[0]['puntaje'],
                "puntaje_2": puntajes_encontrados[1]['puntaje']
            }
        
        # Si hay más de 2 puntajes, tomar los 2 más cercanos al "Final"
        elif len(puntajes_encontrados) > 2:
            # Ordenar por distancia al "Final"
            puntajes_encontrados.sort(key=lambda x: x['distancia_del_final'])
            closest_two = puntajes_encontrados[:2]
            
            # Ordenar los dos más cercanos por posición
            closest_two.sort(key=lambda x: x['posicion'])
            
            return {
                "puntaje_1": closest_two[0]['puntaje'],
                "puntaje_2": closest_two[1]['puntaje']
            }
        
        # Si solo hay 1 puntaje, buscar patrones alternativos
        elif len(puntajes_encontrados) == 1:
            # Buscar líneas que contengan números separados por espacios, guiones, etc.
            for line in search_lines:
                # Patrón: "5-3", "5 - 3", "5 3"
                score_pattern = r'(\d+)\s*[-\s]\s*(\d+)'
                match = re.search(score_pattern, line)
                if match:
                    score1, score2 = int(match.group(1)), int(match.group(2))
                    if 0 <= score1 <= 50 and 0 <= score2 <= 50:
                        return {
                            "puntaje_1": score1,
                            "puntaje_2": score2
                        }
        
        print(f"❌ No se encontraron puntajes válidos para {matchup['sigla_equipo_1']} @ {matchup['sigla_equipo_2']}")
        return None
        
    except Exception as e:
        print(f"❌ Error buscando puntajes: {e}")
        return None


# === FUNCIÓN PARA ACTUALIZAR RESULTADOS EN CONSENSUS EXISTENTE ===
def actualizar_resultados_en_consensus(resultados: List[Dict], deporte: str, fecha: str) -> Dict:
    """
    Actualiza los registros existentes de consensus con los resultados reales.
    Utiliza matching flexible para encontrar correspondencias.
    
    Args:
        resultados: Lista de diccionarios con los resultados de los partidos
        deporte: El deporte (ej: 'mlb')
        fecha: Fecha en formato YYYY-MM-DD
    
    Returns:
        Diccionario con estadísticas de actualización
    """
    stats = {
        'consensus_actualizados': 0,
        'totals_actualizados': 0,
        'errores': []
    }
    
    try:
        print(f"\n📝 === ACTUALIZANDO RESULTADOS EN CONSENSUS ({deporte} - {fecha}) ===")
        
        # Definir rango de fechas flexible (±3 días)
        fecha_base = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_inicio = (fecha_base - timedelta(days=3)).strftime("%Y-%m-%d")
        fecha_fin = (fecha_base + timedelta(days=3)).strftime("%Y-%m-%d")
        
        for resultado in resultados:
            sigla1 = resultado['sigla_equipo_1'] 
            sigla2 = resultado['sigla_equipo_2']
            puntos1 = resultado['puntaje_equipo_1']
            puntos2 = resultado['puntaje_equipo_2']
            
            print(f"\n🔄 Procesando: {sigla1} vs {sigla2} ({puntos1}-{puntos2})")
            
            # === BUSCAR EN MLB_CONSENSUS (Winners/Losers) ===
            consensus_match = None
            
            # Estrategia 1: Match exacto por siglas y fecha
            consensus_exacto = supabase.table("mlb_consensus").select("*").eq(
                "deporte", deporte
            ).eq(
                "fecha_scraping", fecha
            ).or_(
                f"and(equipo_1_sigla.eq.{sigla1},equipo_2_sigla.eq.{sigla2}),"
                f"and(equipo_1_sigla.eq.{sigla2},equipo_2_sigla.eq.{sigla1})"
            ).execute()
            
            if consensus_exacto.data:
                consensus_match = consensus_exacto.data[0]
                print(f"   ✅ Match exacto encontrado por siglas y fecha")
            else:
                # Estrategia 2: Match por siglas en rango de fechas flexible
                consensus_flexible = supabase.table("mlb_consensus").select("*").eq(
                    "deporte", deporte
                ).gte(
                    "fecha_scraping", fecha_inicio
                ).lte(
                    "fecha_scraping", fecha_fin
                ).or_(
                    f"and(equipo_1_sigla.eq.{sigla1},equipo_2_sigla.eq.{sigla2}),"
                    f"and(equipo_1_sigla.eq.{sigla2},equipo_2_sigla.eq.{sigla1})"
                ).execute()
                
                if consensus_flexible.data:
                    # Tomar el más reciente
                    consensus_match = max(consensus_flexible.data, key=lambda x: x.get('created_at', ''))
                    print(f"   ✅ Match flexible encontrado (fecha: {consensus_match.get('fecha_scraping')})")
                else:
                    # Estrategia 3: Match por nombres si las siglas no funcionan
                    nombre1 = resultado['nombre_equipo_1']
                    nombre2 = resultado['nombre_equipo_2']
                    
                    # Buscar por nombres parciales
                    consensus_nombres = supabase.table("mlb_consensus").select("*").eq(
                        "deporte", deporte
                    ).gte(
                        "fecha_scraping", fecha_inicio
                    ).lte(
                        "fecha_scraping", fecha_fin
                    ).execute()
                    
                    # Buscar match manual por nombres
                    for c in consensus_nombres.data:
                        equipo1_db = c.get('equipo_1', '').lower()
                        equipo2_db = c.get('equipo_2', '').lower()
                        
                        if ((nombre1.lower() in equipo1_db or equipo1_db in nombre1.lower()) and 
                            (nombre2.lower() in equipo2_db or equipo2_db in nombre2.lower())) or \
                           ((nombre1.lower() in equipo2_db or equipo2_db in nombre1.lower()) and 
                            (nombre2.lower() in equipo1_db or equipo1_db in nombre2.lower())):
                            consensus_match = c
                            print(f"   ✅ Match por nombres: {equipo1_db} vs {equipo2_db}")
                            break
            
            if consensus_match:
                # Determinar orientación de equipos y calcular efectividad
                equipo_1_es_primero = (consensus_match['equipo_1_sigla'] == sigla1 or 
                                     consensus_match['equipo_1'].lower() in resultado['nombre_equipo_1'].lower())
                
                if equipo_1_es_primero:
                    ganador_real = 1 if puntos1 > puntos2 else 2
                    puntos_db_1, puntos_db_2 = puntos1, puntos2
                else:
                    ganador_real = 2 if puntos1 > puntos2 else 1
                    puntos_db_1, puntos_db_2 = puntos2, puntos1
                
                # Calcular predicción basándose en consensus
                consensus_1_pct = int(consensus_match.get('consensus_equipo_1', '0%').replace('%', ''))
                consensus_2_pct = int(consensus_match.get('consensus_equipo_2', '0%').replace('%', ''))
                prediccion = 1 if consensus_1_pct > consensus_2_pct else 2
                
                efectividad = 1 if prediccion == ganador_real else 0
                
                # Actualizar el registro
                actualizacion = {
                    'puntaje_equipo_1': puntos_db_1,
                    'puntaje_equipo_2': puntos_db_2,
                    'ganador_real': ganador_real,
                    'efectividad': efectividad
                }
                
                supabase.table("mlb_consensus").update(actualizacion).eq(
                    "id", consensus_match['id']
                ).execute()
                
                stats['consensus_actualizados'] += 1
                print(f"   ✅ Consensus actualizado - Pred: {prediccion}, Real: {ganador_real}, Efect: {efectividad}")
            else:
                print(f"   ❌ No se encontró consensus para {sigla1} vs {sigla2}")
            
            # === BUSCAR EN CONSENSUS_TOTALS (Over/Under) ===
            totals_match = None
            
            # Misma estrategia de matching para totals
            totals_exacto = supabase.table("consensus_totals").select("*").eq(
                "deporte", deporte
            ).eq(
                "fecha_scraping", fecha
            ).or_(
                f"and(equipo_1_sigla.eq.{sigla1},equipo_2_sigla.eq.{sigla2}),"
                f"and(equipo_1_sigla.eq.{sigla2},equipo_2_sigla.eq.{sigla1})"
            ).execute()
            
            if totals_exacto.data:
                totals_match = totals_exacto.data[0]
                print(f"   ✅ Totals match exacto encontrado")
            else:
                totals_flexible = supabase.table("consensus_totals").select("*").eq(
                    "deporte", deporte
                ).gte(
                    "fecha_scraping", fecha_inicio
                ).lte(
                    "fecha_scraping", fecha_fin
                ).or_(
                    f"and(equipo_1_sigla.eq.{sigla1},equipo_2_sigla.eq.{sigla2}),"
                    f"and(equipo_1_sigla.eq.{sigla2},equipo_2_sigla.eq.{sigla1})"
                ).execute()
                
                if totals_flexible.data:
                    totals_match = max(totals_flexible.data, key=lambda x: x.get('created_at', ''))
                    print(f"   ✅ Totals match flexible encontrado")
            
            if totals_match:
                # Calcular total real y efectividad
                total_real = puntos1 + puntos2
                linea_total = float(totals_match['linea_total']) if totals_match['linea_total'] else 0.0
                
                # Calcular predicción basándose en consensus over/under
                over_pct = int(totals_match.get('consensus_over', '0%').replace('%', ''))
                under_pct = int(totals_match.get('consensus_under', '0%').replace('%', ''))
                prediccion_total = 1 if over_pct > under_pct else 2  # 1 = Over, 2 = Under
                
                resultado_total = 1 if total_real > linea_total else 2  # 1 = Over, 2 = Under
                efectividad_total = 1 if prediccion_total == resultado_total else 0
                
                # Determinar orientación de equipos para totals
                equipo_1_es_primero_totals = (totals_match['equipo_1_sigla'] == sigla1)
                
                actualizacion_total = {
                    'puntaje_equipo_1': puntos1 if equipo_1_es_primero_totals else puntos2,
                    'puntaje_equipo_2': puntos2 if equipo_1_es_primero_totals else puntos1,
                    'total_real': total_real,
                    'resultado_real': resultado_total,
                    'efectividad': efectividad_total
                }
                
                supabase.table("consensus_totals").update(actualizacion_total).eq(
                    "id", totals_match['id']
                ).execute()
                
                stats['totals_actualizados'] += 1
                print(f"   ✅ Totals actualizado - Total: {total_real}/{linea_total}, Efect: {efectividad_total}")
            else:
                print(f"   ❌ No se encontró totals para {sigla1} vs {sigla2}")
    
    except Exception as e:
        error_msg = f"Error actualizando resultados: {e}"
        stats['errores'].append(error_msg)
        print(f"❌ {error_msg}")
    
    return stats


def agregar_columnas_resultados_si_no_existen():
    """
    Agrega las columnas de resultados a las tablas de consensus si no existen.
    Ejecuta ALTER TABLE para cada columna nueva necesaria.
    """
    try:
        print("🔧 Verificando y agregando columnas de resultados...")
        
        # Columnas para mlb_consensus (Winners/Losers)
        columnas_winners = [
            "puntaje_equipo_1 INTEGER",
            "puntaje_equipo_2 INTEGER", 
            "resultado_sigla VARCHAR(10)",
            "resultado_nombre VARCHAR(100)",
            "ganador_consensus VARCHAR(10)",
            "prediccion_correcta BOOLEAN",
            "estado_partido VARCHAR(20)"
        ]
        
        # Columnas para consensus_totals (Over/Under)
        columnas_totals = [
            "puntaje_equipo_1 INTEGER",
            "puntaje_equipo_2 INTEGER",
            "total_puntos INTEGER",
            "over_under_real VARCHAR(10)",
            "margen_ou DECIMAL(4,1)",
            "linea_total_real DECIMAL(4,1)",
            "consensus_favorito VARCHAR(10)",
            "prediccion_correcta BOOLEAN",
            "estado_partido VARCHAR(20)"
        ]
        
        print("ℹ️  NOTA: Las columnas se agregan automáticamente en el primer uso")
        print("   Si hay errores, ejecuta manualmente en Supabase SQL Editor:")
        print("\n   -- Para mlb_consensus:")
        for col in columnas_winners:
            print(f"   ALTER TABLE mlb_consensus ADD COLUMN IF NOT EXISTS {col};")
        
        print("\n   -- Para consensus_totals:")
        for col in columnas_totals:
            print(f"   ALTER TABLE consensus_totals ADD COLUMN IF NOT EXISTS {col};")
            
    except Exception as e:
        print(f"⚠️ Error verificando columnas: {e}")


def crear_tabla_resultados_si_no_existe():
    """
    FUNCIÓN OBSOLETA: Ya no se usa tabla separada de resultados.
    Los resultados se guardan directamente en las tablas de consensus.
    """
    print("ℹ️  Función obsoleta: Los resultados se guardan en las tablas de consensus existentes")
    pass


def analizar_efectividad_consensus(deporte: str, fecha: str) -> Dict:
    """
    Analiza la efectividad del consensus usando los datos ya unidos en las tablas.
    Ahora es más simple porque los resultados están en las mismas tablas.
    
    Args:
        deporte: Código del deporte (ej: 'mlb')
        fecha: Fecha en formato 'YYYY-MM-DD'
    
    Returns:
        Dict con estadísticas de efectividad del consensus
    """
    try:
        # Obtener datos de consensus Winners/Losers con resultados
        consensus_data = supabase.table("mlb_consensus").select("*").eq(
            "deporte", deporte
        ).eq(
            "fecha_scraping", fecha
        ).not_.is_("prediccion_correcta", "null").execute()
        
        # Obtener datos de consensus Over/Under con resultados
        totals_data = supabase.table("consensus_totals").select("*").eq(
            "deporte", deporte
        ).eq(
            "fecha_scraping", fecha
        ).not_.is_("prediccion_correcta", "null").execute()
        
        if not consensus_data.data and not totals_data.data:
            return {"error": "No hay datos con resultados para el análisis"}
        
        analisis = {
            "fecha": fecha,
            "deporte": deporte,
            "total_partidos_winners": len(consensus_data.data),
            "total_partidos_totals": len(totals_data.data),
            "winners_correctos": 0,
            "winners_total": len(consensus_data.data),
            "over_under_correctos": 0,
            "over_under_total": len(totals_data.data),
            "efectividad_winners": 0.0,
            "efectividad_totals": 0.0,
            "detalles_winners": [],
            "detalles_totals": []
        }
        
        # Analizar Winners/Losers
        for consensus in consensus_data.data:
            if consensus.get("prediccion_correcta"):
                analisis["winners_correctos"] += 1
            
            detalle = {
                "partido": f"{consensus.get('equipo_1')} vs {consensus.get('equipo_2')}",
                "resultado": f"{consensus.get('puntaje_equipo_1')}-{consensus.get('puntaje_equipo_2')}",
                "ganador_real": consensus.get("resultado_nombre"),
                "favorito_consensus": consensus.get("ganador_consensus"),
                "consensus_1": consensus.get("consensus_equipo_1"),
                "consensus_2": consensus.get("consensus_equipo_2"),
                "prediccion_correcta": consensus.get("prediccion_correcta")
            }
            analisis["detalles_winners"].append(detalle)
        
        # Analizar Over/Under
        for total in totals_data.data:
            if total.get("prediccion_correcta"):
                analisis["over_under_correctos"] += 1
            
            detalle = {
                "partido": f"{total.get('equipo_1')} vs {total.get('equipo_2')}",
                "total_puntos": total.get("total_puntos"),
                "linea_total": total.get("linea_total_real"),
                "over_under_real": total.get("over_under_real"),
                "consensus_favorito": total.get("consensus_favorito"),
                "consensus_over": total.get("consensus_over"),
                "consensus_under": total.get("consensus_under"),
                "margen": total.get("margen_ou"),
                "prediccion_correcta": total.get("prediccion_correcta")
            }
            analisis["detalles_totals"].append(detalle)
        
        # Calcular porcentajes de efectividad
        if analisis["winners_total"] > 0:
            analisis["efectividad_winners"] = round((analisis["winners_correctos"] / analisis["winners_total"]) * 100, 2)
        
        if analisis["over_under_total"] > 0:
            analisis["efectividad_totals"] = round((analisis["over_under_correctos"] / analisis["over_under_total"]) * 100, 2)
        
        return analisis
        
    except Exception as e:
        return {"error": f"Error en análisis: {str(e)}"}


def scrape_y_analizar_fecha_completa(deporte: str, fecha: str) -> None:
    """
    Función principal que ejecuta todo el pipeline:
    1. Scrapeando consensus de Winners/Losers
    2. Scrapeando consensus de Over/Under Totals  
    3. Scrapeando resultados reales y los une a las tablas de consensus
    4. Analiza efectividad del consensus
    
    Args:
        deporte: Código del deporte (ej: 'mlb')
        fecha: Fecha en formato 'YYYY-MM-DD'
    """
    print(f"\n🚀 === PIPELINE COMPLETO PARA {deporte.upper()} - {fecha} ===")
    
    # 1. Scrapear consensus Winners/Losers
    print("\n📊 1. Scrapeando consensus Winners/Losers...")
    try:
        scrapear_consensus_por_fecha(fecha, deporte=deporte)
    except Exception as e:
        print(f"❌ Error en consensus Winners/Losers: {e}")
    
    # 2. Scrapear consensus Over/Under Totals
    print("\n📊 2. Scrapeando consensus Over/Under Totals...")
    try:
        scrapear_consensus_totals_por_fecha(fecha, deporte=deporte)
    except Exception as e:
        print(f"❌ Error en consensus Totals: {e}")
    
    # 3. Scrapear resultados reales y actualizar consensus
    print("\n🏆 3. Scrapeando resultados reales y actualizando consensus...")
    try:
        resultados = scrape_resultados_deportivos(deporte, fecha)
        if resultados:
            # Usar nueva función de diagnóstico avanzado
            diagnosticar_problemas_matching(resultados, deporte, fecha)
            
            # Actualizar con la nueva función mejorada
            stats = actualizar_resultados_en_consensus(resultados, deporte, fecha)
            print(f"✅ Estadísticas de actualización:")
            print(f"   Consensus actualizados: {stats['consensus_actualizados']}")
            print(f"   Totals actualizados: {stats['totals_actualizados']}")
            print(f"   Errores: {len(stats['errores'])}")
        else:
            print("⚠️ No se encontraron resultados para esta fecha")
    except Exception as e:
        print(f"❌ Error en resultados reales: {e}")
    
    # 4. Analizar efectividad del consensus
    print("\n📈 4. Analizando efectividad del consensus...")
    try:
        analisis = analizar_efectividad_consensus(deporte, fecha)
        
        if "error" not in analisis:
            print(f"📊 RESUMEN DE EFECTIVIDAD - {fecha}")
            print(f"   Partidos Winners/Losers: {analisis['total_partidos_winners']}")
            print(f"   Partidos Over/Under: {analisis['total_partidos_totals']}")
            print(f"   Winners correctos: {analisis['winners_correctos']}/{analisis['winners_total']} ({analisis['efectividad_winners']}%)")
            print(f"   Over/Under correctos: {analisis['over_under_correctos']}/{analisis['over_under_total']} ({analisis['efectividad_totals']}%)")
            
            # Guardar análisis en CSV
            if analisis['detalles_winners']:
                df_winners = pd.DataFrame(analisis['detalles_winners'])
                csv_winners = f"{deporte}_analisis_winners_{fecha}.csv"
                df_winners.to_csv(csv_winners, index=False)
                print(f"📄 Análisis Winners guardado en: {csv_winners}")
            
            if analisis['detalles_totals']:
                df_totals = pd.DataFrame(analisis['detalles_totals'])
                csv_totals = f"{deporte}_analisis_totals_{fecha}.csv"
                df_totals.to_csv(csv_totals, index=False)
                print(f"📄 Análisis Totals guardado en: {csv_totals}")
        else:
            print(f"⚠️ {analisis['error']}")
            
    except Exception as e:
        print(f"❌ Error en análisis de efectividad: {e}")
    
    print(f"\n✅ === PIPELINE COMPLETADO PARA {deporte.upper()} - {fecha} ===")


# === FUNCIÓN DE COMPATIBILIDAD ===
def guardar_resultados_en_supabase(resultados: List[Dict], deporte: str) -> None:
    """
    Función de compatibilidad que redirige a la nueva función de actualización.
    """
    print("ℹ️  Redirigiendo a actualizar_resultados_en_consensus...")
    actualizar_resultados_en_consensus(resultados, deporte)


# === LOOP PRINCIPAL DE SCRAPING HISTÓRICO ===
def main():
    for deporte in DEPORTES:
        print(f"\n=== Scrapeando deporte: {deporte.upper()} ===")
        fecha_actual = datetime.strptime(FECHA_INICIO, "%Y-%m-%d")
        fecha_final = datetime.strptime(FECHA_FIN, "%Y-%m-%d")
        while fecha_actual <= fecha_final:
            fecha_str = fecha_actual.strftime("%Y-%m-%d")
            for intento in range(3):
                try:
                    scrapear_consensus_por_fecha(fecha_str, deporte=deporte)
                    break
                except Exception as e:
                    print(f"Reintentando {fecha_str} {deporte} (intento {intento+1}/3)...")
                    time.sleep(5)
            fecha_actual += timedelta(days=1)
    print("Scraping histórico finalizado.")

def mostrar_debug_consensus_vs_resultados(resultados: List[Dict], deporte: str, fecha: str) -> None:
    """
    Función de debug para mostrar qué consensus y resultados tenemos,
    y por qué no están haciendo match.
    """
    try:
        print(f"\n🔍 === DEBUG: CONSENSUS VS RESULTADOS ({deporte} - {fecha}) ===")
        
        # Obtener todos los consensus de la fecha
        consensus_data = supabase.table("mlb_consensus").select("*").eq(
            "deporte", deporte
        ).eq(
            "fecha_scraping", fecha
        ).execute()
        
        totals_data = supabase.table("consensus_totals").select("*").eq(
            "deporte", deporte
        ).eq(
            "fecha_scraping", fecha
        ).execute()
        
        print(f"📊 CONSENSUS DISPONIBLE:")
        print(f"   Winners/Losers: {len(consensus_data.data)} partidos")
        for i, consensus in enumerate(consensus_data.data):
            print(f"     {i+1}. {consensus.get('equipo_1_sigla')} vs {consensus.get('equipo_2_sigla')} ({consensus.get('equipo_1')} vs {consensus.get('equipo_2')})")
        
        print(f"   Over/Under: {len(totals_data.data)} partidos")
        for i, total in enumerate(totals_data.data):
            print(f"     {i+1}. {total.get('equipo_1_sigla')} vs {total.get('equipo_2_sigla')} ({total.get('equipo_1')} vs {total.get('equipo_2')})")
        
        print(f"\n📊 RESULTADOS ENCONTRADOS:")
        for i, resultado in enumerate(resultados):
            print(f"   {i+1}. {resultado['sigla_equipo_1']} vs {resultado['sigla_equipo_2']} ({resultado['nombre_equipo_1']} vs {resultado['nombre_equipo_2']}) - {resultado['puntaje_equipo_1']}-{resultado['puntaje_equipo_2']}")
        
        print(f"\n💡 SUGERENCIAS:")
        if not resultados:
            print("   • No se encontraron resultados para esta fecha")
            print("   • Verificar que los partidos hayan finalizado")
        elif len(consensus_data.data) == 0:
            print("   • No hay consensus para esta fecha")
            print("   • Ejecutar primero el scraping de consensus")
        else:
            print("   • Los equipos en resultados no coinciden con los del consensus")
            print("   • Puede ser que sean partidos de diferentes fechas")
            print("   • O que las siglas de equipos sean diferentes")
        
    except Exception as e:
        print(f"❌ Error en debug: {e}")

def diagnosticar_problemas_matching(resultados: List[Dict], deporte: str, fecha: str) -> None:
    """
    Función de diagnóstico avanzada para entender problemas de matching
    entre consensus y resultados.
    """
    try:
        print(f"\n🔬 === DIAGNÓSTICO AVANZADO ({deporte} - {fecha}) ===")
        
        # 1. Verificar qué se insertó realmente en Supabase
        print("\n1️⃣ VERIFICANDO INSERCIÓN RECIENTE EN SUPABASE:")
        
        # Buscar consensus insertados HOY (no por fecha_scraping)
        consensus_hoy = supabase.table("mlb_consensus").select("*").gte(
            "created_at", datetime.now().strftime("%Y-%m-%d")
        ).execute()
        
        totals_hoy = supabase.table("consensus_totals").select("*").gte(
            "created_at", datetime.now().strftime("%Y-%m-%d")
        ).execute()
        
        print(f"   Consensus insertados HOY: {len(consensus_hoy.data)}")
        for c in consensus_hoy.data:
            print(f"     • {c.get('equipo_1_sigla')} vs {c.get('equipo_2_sigla')} - Fecha hora: {c.get('fecha_hora')} - Fecha scraping: {c.get('fecha_scraping')}")
        
        print(f"   Totals insertados HOY: {len(totals_hoy.data)}")
        for t in totals_hoy.data:
            print(f"     • {t.get('equipo_1_sigla')} vs {t.get('equipo_2_sigla')} - Fecha hora: {t.get('fecha_hora')} - Fecha scraping: {t.get('fecha_scraping')}")
        
        # 2. Analizar fechas en consensus vs fecha solicitada
        print(f"\n2️⃣ ANÁLISIS DE FECHAS:")
        print(f"   Fecha solicitada: {fecha}")
        
        fechas_consensus = set()
        for c in consensus_hoy.data:
            fecha_hora = c.get('fecha_hora', '')
            # Extraer parte de fecha del campo fecha_hora
            if 'Jun' in fecha_hora:
                fechas_consensus.add(fecha_hora)
        
        fechas_totals = set()
        for t in totals_hoy.data:
            fecha_hora = t.get('fecha_hora', '')
            if 'Jun' in fecha_hora:
                fechas_totals.add(fecha_hora)
        
        print(f"   Fechas encontradas en consensus: {fechas_consensus}")
        print(f"   Fechas encontradas en totals: {fechas_totals}")
        
        # 3. Analizar equipos en resultados vs consensus
        print(f"\n3️⃣ ANÁLISIS DE EQUIPOS:")
        print(f"   Equipos en resultados:")
        for r in resultados:
            print(f"     • {r['sigla_equipo_1']} vs {r['sigla_equipo_2']} ({r['nombre_equipo_1']} vs {r['nombre_equipo_2']})")
        
        print(f"   Equipos en consensus de HOY:")
        equipos_consensus = set()
        for c in consensus_hoy.data:
            equipos_consensus.add(f"{c.get('equipo_1_sigla')} vs {c.get('equipo_2_sigla')}")
        
        for equipo in equipos_consensus:
            print(f"     • {equipo}")
        
        # 4. Buscar posibles matches con lógica flexible
        print(f"\n4️⃣ BÚSQUEDA DE MATCHES FLEXIBLES:")
        
        for resultado in resultados:
            sigla1, sigla2 = resultado['sigla_equipo_1'], resultado['sigla_equipo_2']
            
            # Buscar en consensus recientes (últimos 3 días)
            consensus_flexibles = supabase.table("mlb_consensus").select("*").eq(
                "deporte", deporte
            ).or_(
                f"and(equipo_1_sigla.eq.{sigla1},equipo_2_sigla.eq.{sigla2}),"
                f"and(equipo_1_sigla.eq.{sigla2},equipo_2_sigla.eq.{sigla1})"
            ).gte(
                "created_at", (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
            ).execute()
            
            print(f"   Resultado {sigla1} vs {sigla2}:")
            print(f"     Matches en consensus (últimos 3 días): {len(consensus_flexibles.data)}")
            
            for match in consensus_flexibles.data:
                print(f"       • {match.get('equipo_1_sigla')} vs {match.get('equipo_2_sigla')} - {match.get('fecha_hora')} - {match.get('created_at')}")
        
        # 5. Recomendaciones
        print(f"\n5️⃣ RECOMENDACIONES:")
        
        if not consensus_hoy.data:
            print("   ❌ No se insertaron consensus HOY")
            print("   ✅ Verificar que el scraping de consensus funcione correctamente")
        elif not resultados:
            print("   ❌ No se encontraron resultados")
            print("   ✅ Verificar que la fecha tenga partidos finalizados")
        elif len(set(fechas_consensus)) > 1:
            print("   ⚠️  Los consensus tienen fechas mixtas")
            print("   ✅ Revisar lógica de parsing de fechas en el scraper")
        else:
            print("   ⚠️  Equipos no coinciden entre consensus y resultados")
            print("   ✅ Posible problema: partidos de diferentes fechas reales")
            print("   ✅ Considerar buscar consensus por rango de fechas flexible")
        
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")

def convertir_fecha_texto_a_estandar(fecha_texto: str, fecha_referencia: str) -> str:
    """
    Convierte una fecha en formato texto (ej: "Mon. Jun 30") a formato estándar (YYYY-MM-DD).
    
    Args:
        fecha_texto: Fecha en formato "Day. Mon DD" (ej: "Mon. Jun 30")
        fecha_referencia: Fecha de referencia en formato "YYYY-MM-DD" para determinar el año
    
    Returns:
        Fecha en formato YYYY-MM-DD
    """
    try:
        # Limpiar el texto de fecha
        fecha_limpia = fecha_texto.strip()
        
        # Si ya está en formato YYYY-MM-DD, retornar tal como está
        if re.match(r'\d{4}-\d{2}-\d{2}', fecha_limpia):
            return fecha_limpia
        
        # Mapeo de meses abreviados a números
        meses = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        
        # Extraer año de la fecha de referencia
        año_ref = datetime.strptime(fecha_referencia, "%Y-%m-%d").year
        
        # Buscar patrón "Mon. DD" o "Month DD"
        patron = r'(\w{3})[.\s]+(\d{1,2})'
        match = re.search(patron, fecha_limpia)
        
        if match:
            mes_abrev = match.group(1)
            dia = match.group(2).zfill(2)  # Añadir cero inicial si es necesario
            
            # Convertir mes abreviado a número
            mes_num = meses.get(mes_abrev, '01')
            
            # Formar fecha en formato YYYY-MM-DD
            fecha_estandar = f"{año_ref}-{mes_num}-{dia}"
            
            # Validar que la fecha sea válida
            datetime.strptime(fecha_estandar, "%Y-%m-%d")
            
            return fecha_estandar
        
        # Si no puede parsear, usar la fecha de referencia
        print(f"⚠️ No se pudo parsear fecha '{fecha_texto}', usando fecha referencia: {fecha_referencia}")
        return fecha_referencia
        
    except Exception as e:
        print(f"❌ Error parseando fecha '{fecha_texto}': {e}")
        return fecha_referencia

def _buscar_puntajes_en_texto(texto: str) -> Dict[str, int]:
    """
    Buscar puntajes en un texto usando regex
    Formato esperado: algo como "SF 2 CHW 5" o "LAD 5 KC 1"
    """
    import re
    
    # Patrón para encontrar puntajes: [SIGLA] [NUMERO] [SIGLA] [NUMERO]
    patron = r'([A-Z]{2,4})\s+(\d+)\s+([A-Z]{2,4})\s+(\d+)'
    
    match = re.search(patron, texto)
    if match:
        sigla1, puntaje1, sigla2, puntaje2 = match.groups()
        return {
            'puntaje_1': int(puntaje1),
            'puntaje_2': int(puntaje2),
            'sigla_1': sigla1,
            'sigla_2': sigla2
        }
    
    # Patrón alternativo para formatos como "Final 2 5"
    patron_alt = r'Final\s+(\d+)\s+(\d+)'
    match_alt = re.search(patron_alt, texto)
    if match_alt:
        puntaje1, puntaje2 = match_alt.groups()
        return {
            'puntaje_1': int(puntaje1),
            'puntaje_2': int(puntaje2),
            'sigla_1': None,
            'sigla_2': None
        }
    
    return None
