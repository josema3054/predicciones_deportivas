#!/usr/bin/env python3
"""
Clases base para la arquitectura modular de scraping deportivo
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Clase base para todos los scrapers deportivos"""
    
    def __init__(self, sport: str):
        self.sport = sport.lower()
        self.scraped_data: List[Dict[str, Any]] = []
        logger.info(f"Inicializando scraper para {sport.upper()}")
        
    @abstractmethod
    def scrape_consensus(self, fecha: str, tipo: str = "winners") -> List[Dict[str, Any]]:
        """Scraping de consensus (winners/losers o totals)"""
        pass
        
    @abstractmethod
    def scrape_results(self, fecha: str) -> List[Dict[str, Any]]:
        """Scraping de resultados reales"""
        pass
        
    @abstractmethod
    def validate_data(self, data: List[Dict[str, Any]]) -> bool:
        """Validación de datos scrapeados"""
        pass
        
    def save_to_csv(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """Guardar datos en CSV"""
        try:
            if data:
                df = pd.DataFrame(data)
                df.to_csv(filename, index=False)
                logger.info(f"✅ Datos guardados en {filename}")
                return True
            else:
                logger.warning(f"⚠️ No hay datos para guardar en {filename}")
                return False
        except Exception as e:
            logger.error(f"❌ Error al guardar CSV {filename}: {e}")
            return False

class BaseDatabase(ABC):
    """Clase base para gestión de base de datos"""
    
    def __init__(self, sport: str):
        self.sport = sport.lower()
        self.supabase = self._configure_supabase()
        logger.info(f"Inicializando database para {sport.upper()}")
        
    def _configure_supabase(self) -> Client:
        """Configurar conexión a Supabase"""
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("❌ Error: Las variables SUPABASE_URL y SUPABASE_ANON_KEY deben estar configuradas")
        
        client = create_client(url, key)
        logger.info("✅ Conexión a Supabase configurada")
        return client
    
    @abstractmethod
    def save_consensus(self, data: List[Dict[str, Any]], tipo: str = "winners") -> bool:
        """Guardar datos de consensus"""
        pass
        
    @abstractmethod
    def save_results(self, data: List[Dict[str, Any]]) -> bool:
        """Guardar resultados reales"""
        pass
        
    @abstractmethod
    def check_duplicates(self, data: Dict[str, Any], tabla: str) -> bool:
        """Verificar duplicados"""
        pass

class BaseTeams(ABC):
    """Clase base para gestión de equipos"""
    
    def __init__(self, sport: str):
        self.sport = sport.lower()
        
    @abstractmethod
    def get_team_name(self, sigla: str) -> str:
        """Obtener nombre completo del equipo desde sigla"""
        pass
        
    @abstractmethod
    def get_team_sigla(self, nombre_completo: str) -> str:
        """Obtener sigla del equipo desde nombre completo"""
        pass
        
    @abstractmethod
    def get_all_teams(self) -> Dict[str, str]:
        """Obtener diccionario completo de equipos"""
        pass
