#!/usr/bin/env python3
"""
Scraper especializado para MLB - Baseball
Basado en el scraper original que funciona
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base import BaseScraper
from core.utils import (
    parse_date_from_text, 
    parse_consensus_percentages, 
    parse_picks_count,
    format_date_for_url
)
from .teams_mlb import MLBTeams
from .database_mlb import MLBDatabase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MLBScraper(BaseScraper):
    """Scraper especializado para MLB"""
    
    def __init__(self):
        super().__init__('mlb')
        self.teams = MLBTeams()
        self.database = MLBDatabase()
        self.urls = {
            'consensus': 'https://contests.covers.com/consensus/topconsensus/mlb/expert/{date}',
            'totals': 'https://contests.covers.com/consensus/topoverunderconsensus/mlb/expert/{date}',
            'results': 'https://www.covers.com/sports/mlb/matchups/{date}'
        }
        
    def scrape_consensus(self, fecha: str, tipo: str = "winners") -> List[Dict[str, Any]]:
        """Scraping de consensus MLB"""
        if tipo == "winners":
            return self._scrape_consensus_winners(fecha)
        elif tipo == "totals":
            return self._scrape_consensus_totals(fecha)
        else:
            logger.error(f"Tipo de consensus no válido: {tipo}")
            return []
    
    def scrape_results(self, fecha: str) -> List[Dict[str, Any]]:
        """Scraping de resultados reales MLB"""
        logger.info(f"📊 Scrapeando resultados reales MLB para {fecha}")
        
        # URL de ESPN para resultados MLB
        url = f"https://www.espn.com/mlb/scoreboard/_/date/{fecha.replace('-', '')}"
        driver = self._setup_driver()
        resultados = []
        
        try:
            logger.info(f"📍 URL: {url}")
            driver.get(url)
            
            # Esperar a que carguen los partidos
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ScoreCell"))
            )
            
            # Buscar todos los partidos
            partidos = driver.find_elements(By.CSS_SELECTOR, ".Scoreboard")
            logger.info(f"📊 Partidos encontrados: {len(partidos)}")
            
            for partido in partidos:
                resultado = self._parse_resultado_partido(partido, fecha)
                if resultado:
                    resultados.append(resultado)
            
            # Guardar en base de datos
            if resultados:
                self.database.save_results(resultados)
                self.save_to_csv(resultados, f"mlb_resultados_{fecha}.csv")
            
            logger.info(f"✅ MLB resultados: {len(resultados)} registros para {fecha}")
            return resultados
            
        except Exception as e:
            logger.error(f"❌ Error en scraping resultados: {e}")
            return []
        finally:
            driver.quit()
    
    def validate_data(self, data: List[Dict[str, Any]]) -> bool:
        """Validación de datos MLB"""
        if not data:
            return False
        
        for item in data:
            # Verificar campos requeridos
            required_fields = ['equipo_1', 'equipo_2', 'equipo_1_sigla', 'equipo_2_sigla', 'fecha_scraping']
            if not all(field in item for field in required_fields):
                return False
            
            # Verificar que las siglas sean válidas
            if not self.teams.is_valid_team(item['equipo_1_sigla']) or not self.teams.is_valid_team(item['equipo_2_sigla']):
                return False
        
        return True
    
    def _setup_driver(self):
        """Configurar driver de Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        return webdriver.Chrome(options=chrome_options)
    
    def _scrape_consensus_winners(self, fecha: str) -> List[Dict[str, Any]]:
        """Scraping de consensus Winners/Losers"""
        logger.info(f"🏆 Scrapeando consensus Winners/Losers MLB para {fecha}")
        
        url = self.urls['consensus'].format(date=fecha)
        driver = self._setup_driver()
        partidos = []
        
        try:
            logger.info(f"📍 URL: {url}")
            driver.get(url)
            
            # Esperar carga
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
            )
            
            # Obtener filas
            filas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            logger.info(f"📊 Filas encontradas: {len(filas)}")
            
            for fila in filas:
                columnas = fila.find_elements(By.TAG_NAME, "td")
                if len(columnas) >= 5:
                    partido = self._parse_consensus_row(columnas, fecha)
                    if partido and self.validate_data([partido]):
                        partidos.append(partido)
            
            # Guardar en base de datos
            if partidos:
                self.database.save_consensus(partidos, "winners")
                self.save_to_csv(partidos, f"mlb_consensus_{fecha}.csv")
            
            logger.info(f"✅ MLB consensus Winners: {len(partidos)} registros para {fecha}")
            return partidos
            
        except Exception as e:
            logger.error(f"❌ Error en scraping consensus: {e}")
            return []
        finally:
            driver.quit()
    
    def _scrape_consensus_totals(self, fecha: str) -> List[Dict[str, Any]]:
        """Scraping de consensus Totals"""
        logger.info(f"🎯 Scrapeando consensus Totals MLB para {fecha}")
        
        url = self.urls['totals'].format(date=fecha)
        driver = self._setup_driver()
        partidos = []
        
        try:
            logger.info(f"📍 URL: {url}")
            driver.get(url)
            
            # Esperar carga
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
            )
            
            # Obtener filas
            filas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            logger.info(f"📊 Filas encontradas: {len(filas)}")
            
            for fila in filas:
                columnas = fila.find_elements(By.TAG_NAME, "td")
                if len(columnas) >= 5:
                    partido = self._parse_totals_row(columnas, fecha)
                    if partido and self.validate_data([partido]):
                        partidos.append(partido)
            
            # Guardar en base de datos
            if partidos:
                self.database.save_consensus(partidos, "totals")
                self.save_to_csv(partidos, f"mlb_consensus_totals_{fecha}.csv")
            
            logger.info(f"✅ MLB consensus Totals: {len(partidos)} registros para {fecha}")
            return partidos
            
        except Exception as e:
            logger.error(f"❌ Error en scraping totals: {e}")
            return []
        finally:
            driver.quit()
    
    def _parse_consensus_row(self, columnas, fecha: str) -> Dict[str, Any]:
        """Parsear fila de consensus Winners/Losers"""
        try:
            # Extraer datos de las columnas
            equipos_col = columnas[0].text.strip()
            fecha_col = columnas[1].text.strip()
            consensus_col = columnas[2].text.strip()
            odds_col = columnas[3].text.strip()
            picks_col = columnas[4].text.strip()
            
            # Parsear equipos
            equipos_lines = equipos_col.split('\n')
            if len(equipos_lines) < 3:
                return None
                
            equipo_1_sigla = equipos_lines[1].strip()
            equipo_2_sigla = equipos_lines[2].strip()
            
            # Convertir a nombres completos
            equipo_1 = self.teams.get_team_name(equipo_1_sigla)
            equipo_2 = self.teams.get_team_name(equipo_2_sigla)
            
            # Parsear consensus
            consensus_1, consensus_2 = parse_consensus_percentages(consensus_col)
            if not consensus_1 or not consensus_2:
                return None
            
            # Parsear picks
            picks_1, picks_2 = parse_picks_count(picks_col)
            if picks_1 is None or picks_2 is None:
                return None
            
            # Parsear odds
            odds_lines = odds_col.split('\n')
            side_1 = odds_lines[0].strip() if len(odds_lines) > 0 else ''
            side_2 = odds_lines[1].strip() if len(odds_lines) > 1 else ''
            
            # Parsear fecha
            fecha_hora = parse_date_from_text(fecha_col, fecha)
            
            return {
                'deporte': 'MLB',
                'equipo_1': equipo_1,
                'equipo_2': equipo_2,
                'equipo_1_sigla': equipo_1_sigla,
                'equipo_2_sigla': equipo_2_sigla,
                'fecha_hora': fecha_hora,
                'consensus_equipo_1': consensus_1,
                'consensus_equipo_2': consensus_2,
                'side_equipo_1': side_1,
                'side_equipo_2': side_2,
                'picks_equipo_1': str(picks_1),
                'picks_equipo_2': str(picks_2),
                'fecha_scraping': fecha
            }
            
        except Exception as e:
            logger.error(f"⚠️ Error parseando fila consensus: {e}")
            return None
    
    def _parse_totals_row(self, columnas, fecha: str) -> Dict[str, Any]:
        """Parsear fila de consensus Totals"""
        try:
            # Extraer datos de las columnas
            equipos_col = columnas[0].text.strip()
            fecha_col = columnas[1].text.strip()
            consensus_col = columnas[2].text.strip()
            linea_col = columnas[3].text.strip()
            picks_col = columnas[4].text.strip()
            
            # Parsear equipos
            equipos_lines = equipos_col.split('\n')
            if len(equipos_lines) < 3:
                return None
                
            equipo_1_sigla = equipos_lines[1].strip()
            equipo_2_sigla = equipos_lines[2].strip()
            
            # Convertir a nombres completos
            equipo_1 = self.teams.get_team_name(equipo_1_sigla)
            equipo_2 = self.teams.get_team_name(equipo_2_sigla)
            
            # Parsear consensus Over/Under
            consensus_lines = consensus_col.split('\n')
            consensus_over = consensus_lines[0].strip() if len(consensus_lines) > 0 else ''
            consensus_under = consensus_lines[1].strip() if len(consensus_lines) > 1 else ''
            
            # Parsear picks
            picks_1, picks_2 = parse_picks_count(picks_col)
            if picks_1 is None or picks_2 is None:
                return None
            
            # Parsear línea total
            linea_total = None
            try:
                linea_total = float(linea_col.replace('O', '').replace('U', '').strip())
            except (ValueError, AttributeError):
                pass
            
            # Parsear fecha
            fecha_hora = parse_date_from_text(fecha_col, fecha)
            
            return {
                'deporte': 'MLB',
                'equipo_1': equipo_1,
                'equipo_2': equipo_2,
                'equipo_1_sigla': equipo_1_sigla,
                'equipo_2_sigla': equipo_2_sigla,
                'fecha_hora': fecha_hora,
                'consensus_over': consensus_over,
                'consensus_under': consensus_under,
                'picks_over': str(picks_1),
                'picks_under': str(picks_2),
                'linea_total': linea_total,
                'fecha_scraping': fecha
            }
            
        except Exception as e:
            logger.error(f"⚠️ Error parseando fila totals: {e}")
            return None
            equipos_lines = equipos_col.split('\n')
            if len(equipos_lines) < 3:
                return None
                
            equipo_1_sigla = equipos_lines[1].strip()
            equipo_2_sigla = equipos_lines[2].strip()
            
            # Convertir a nombres completos
            equipo_1 = self.normalize_team_name(equipo_1_sigla)
            equipo_2 = self.normalize_team_name(equipo_2_sigla)
            
            if not equipo_1 or not equipo_2:
                return None
            
            # Parsear consensus
            consensus_1, consensus_2 = parse_consensus_percentages(consensus_col)
            if not consensus_1 or not consensus_2:
                return None
            
            # Parsear picks
            picks_1, picks_2 = parse_picks_count(picks_col)
            if picks_1 is None or picks_2 is None:
                return None
            
            # Parsear odds
            odds_lines = odds_col.split('\n')
            side_1 = odds_lines[0].strip() if len(odds_lines) > 0 else ''
            side_2 = odds_lines[1].strip() if len(odds_lines) > 1 else ''
            
            # Parsear fecha
            fecha_hora = parse_date_from_text(fecha_col, date_str)
            
            return {
                'deporte': 'MLB',
                'equipo_1': equipo_1,
                'equipo_2': equipo_2,
                'equipo_1_sigla': equipo_1_sigla,
                'equipo_2_sigla': equipo_2_sigla,
                'fecha_hora': fecha_hora,
                'consensus_equipo_1': consensus_1,
                'consensus_equipo_2': consensus_2,
                'side_equipo_1': side_1,
                'side_equipo_2': side_2,
                'picks_equipo_1': str(picks_1),
                'picks_equipo_2': str(picks_2),
                'fecha_scraping': date_str
            }
            
        except Exception as e:
            print(f"⚠️ Error parseando fila: {e}")
            return None
    
    def _is_duplicate_consensus(self, partido):
        """Verificar si el registro ya existe"""
        filters = {
            'deporte': partido['deporte'],
            'equipo_1_sigla': partido['equipo_1_sigla'],
            'equipo_2_sigla': partido['equipo_2_sigla'],
            'fecha_scraping': partido['fecha_scraping']
        }
        
        return self.check_duplicates(self.config['tables']['consensus'], filters)
    
    def _save_consensus_party(self, partido):
        """Guardar partido en base de datos"""
        try:
            client = self.db_manager.get_client()
            client.table(self.config['tables']['consensus']).insert(partido).execute()
            print(f"✅ Nuevo registro guardado: {partido['equipo_1']} vs {partido['equipo_2']}")
        except Exception as e:
            print(f"⚠️ Error guardando: {e}")

    def _parse_resultado_partido(self, elemento_partido, fecha: str) -> Dict[str, Any]:
        """Parsear resultado de un partido individual"""
        try:
            # Extraer nombres de equipos
            equipos = elemento_partido.find_elements(By.CSS_SELECTOR, ".ScoreCell__TeamName")
            if len(equipos) < 2:
                return None
                
            equipo_visitante = equipos[0].text.strip()
            equipo_local = equipos[1].text.strip()
            
            # Extraer puntajes
            puntajes = elemento_partido.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score")
            if len(puntajes) < 2:
                return None
                
            score_visitante = int(puntajes[0].text.strip())
            score_local = int(puntajes[1].text.strip())
            
            # Determinar ganador
            if score_local > score_visitante:
                ganador = equipo_local
                perdedor = equipo_visitante
            else:
                ganador = equipo_visitante
                perdedor = equipo_local
            
            # Calcular total
            total_puntos = score_local + score_visitante
            
            # Normalizar nombres de equipos a siglas
            equipo_local_sigla = self.teams.get_team_abbreviation(equipo_local)
            equipo_visitante_sigla = self.teams.get_team_abbreviation(equipo_visitante)
            
            # Obtener nombres completos
            equipo_local_nombre = self.teams.get_team_name(equipo_local_sigla)
            equipo_visitante_nombre = self.teams.get_team_name(equipo_visitante_sigla)
            
            return {
                'deporte': 'MLB',
                'fecha': fecha,
                'equipo_local': equipo_local_nombre,
                'equipo_visitante': equipo_visitante_nombre,
                'equipo_local_sigla': equipo_local_sigla,
                'equipo_visitante_sigla': equipo_visitante_sigla,
                'score_local': score_local,
                'score_visitante': score_visitante,
                'ganador': ganador,
                'perdedor': perdedor,
                'total_puntos': total_puntos,
                'fecha_scraping': fecha
            }
            
        except Exception as e:
            logger.error(f"⚠️ Error parseando partido: {e}")
            return None

def main():
    """Función principal para testing"""
    scraper = MLBScraper()
    
    # Test con fecha actual
    from datetime import datetime
    fecha_test = datetime.now().strftime("%Y-%m-%d")
    
    print(f"🧪 TEST MLB Scraper para {fecha_test}")
    resultados = scraper.scrape_consensus_winners(fecha_test)
    print(f"📊 Resultados: {len(resultados)} partidos")

if __name__ == "__main__":
    main()
