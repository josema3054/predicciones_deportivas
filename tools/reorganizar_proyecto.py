#!/usr/bin/env python3
"""
Script para reorganizar automáticamente el proyecto
"""

import os
import shutil
from pathlib import Path

def reorganizar():
    print("🚀 REORGANIZANDO PROYECTO...")
    
    # 1. Crear carpetas
    carpetas = ['tests', 'scripts', 'docs', 'tools', 'data/csv', 'data/temp']
    for carpeta in carpetas:
        Path(carpeta).mkdir(parents=True, exist_ok=True)
        print(f"📁 {carpeta}")
    
    # 2. Mover CSVs
    csvs = ['mlb_consensus_2025-06-25.csv', 'mlb_consensus_2025-06-26.csv', 
            'mlb_consensus_2025-06-27.csv', 'mlb_consensus_2025-06-28.csv',
            'mlb_consensus_2025-06-29.csv', 'mlb_consensus_2025-06-30.csv',
            'mlb_consensus_totals_2025-06-25.csv', 'mlb_consensus_totals_2025-06-26.csv',
            'mlb_consensus_totals_2025-06-27.csv', 'mlb_consensus_totals_2025-06-28.csv',
            'mlb_consensus_totals_2025-06-29.csv', 'mlb_resultados_2025-06-29.csv']
    
    for archivo in csvs:
        if os.path.exists(archivo):
            shutil.move(archivo, f'data/csv/{archivo}')
            print(f"✅ {archivo} → data/csv/")
    
    # 3. Mover tests
    tests = ['test_mlb_architecture.py', 'test_scraping_quick.py', 'test_puntajes_final.py',
             'debug_selenium_resultados.py', 'debug_estructura_resultados.py', 'debug_scraper.py',
             'analizar_duplicados.py', 'analizar_estructura_consensus.py',
             'diagnostico_diferencias.py', 'diagnostico_equipos_contenedores.py',
             'diagnostico_puntajes_final.py', 'diagnostico_resultados.py']
    
    for archivo in tests:
        if os.path.exists(archivo):
            shutil.move(archivo, f'tests/{archivo}')
            print(f"✅ {archivo} → tests/")
    
    # 4. Mover scripts
    scripts = ['mlb_main.py', 'ejecutar_scraping_completo.py',
               'actualizar_consensus_temp.py', 'actualizar_consensus_winners.py',
               'actualizar_resultados_supabase.py', 'limpiar_csv.py',
               'limpiar_simple.py', 'limpiar_tablas.py', 'comandos.py']
    
    for archivo in scripts:
        if os.path.exists(archivo):
            shutil.move(archivo, f'scripts/{archivo}')
            print(f"✅ {archivo} → scripts/")
    
    # 5. Mover docs
    docs = ['README_MODULAR.md', 'FASE_1_COMPLETADA.md', 'PROYECTO_LIMPIO.md',
            'GUIA_WINDOWS.md', 'sql_setup_columnas.sql']
    
    for archivo in docs:
        if os.path.exists(archivo):
            shutil.move(archivo, f'docs/{archivo}')
            print(f"✅ {archivo} → docs/")
    
    # 6. Mover tools
    tools_list = ['config.py', 'setup_completo.py', 'ver_estructura.py',
                  'verificar_columnas_consensus_totals.py', 'verificar_partidos_completo.py',
                  'equipos_data.py']
    
    for archivo in tools_list:
        if os.path.exists(archivo):
            shutil.move(archivo, f'tools/{archivo}')
            print(f"✅ {archivo} → tools/")
    
    # 7. Mover temp
    if os.path.exists('consensus_page_source.html'):
        shutil.move('consensus_page_source.html', 'data/temp/')
        print("✅ consensus_page_source.html → data/temp/")
    
    # 8. Limpiar
    if os.path.exists('scraper_historico.py'):
        os.remove('scraper_historico.py')
        print("🗑️ scraper_historico.py eliminado")
    
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')
        print("🗑️ __pycache__ eliminado")
    
    print("\n✅ REORGANIZACIÓN COMPLETADA")

if __name__ == "__main__":
    reorganizar()
