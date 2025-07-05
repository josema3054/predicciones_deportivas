#!/usr/bin/env python3
"""
Script para diagnosticar y actualizar resultados en Supabase
"""

import os
import pandas as pd
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def diagnosticar_resultados():
    """Diagnosticar por qué los resultados no se actualizan en Supabase"""
    print("🔍 DIAGNÓSTICO DE RESULTADOS")
    print("=" * 50)
    
    # 1. Verificar archivo CSV de resultados
    archivo_resultados = "mlb_resultados_2025-06-29.csv"
    if os.path.exists(archivo_resultados):
        print(f"✅ Archivo de resultados encontrado: {archivo_resultados}")
        df = pd.read_csv(archivo_resultados)
        print(f"   Partidos en CSV: {len(df)}")
        for _, row in df.iterrows():
            print(f"     • {row['nombre_equipo_1']} vs {row['nombre_equipo_2']}: {row['puntaje_equipo_1']}-{row['puntaje_equipo_2']} (Total: {row['total_puntos']})")
    else:
        print(f"❌ No se encontró: {archivo_resultados}")
        return
    
    # 2. Verificar conexión a Supabase
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("❌ Variables de entorno de Supabase no configuradas")
            return
            
        supabase = create_client(url, key)
        print("✅ Conexión a Supabase establecida")
        
        # 3. Buscar matches en consensus_totals
        print(f"\n🔍 Buscando matches en consensus_totals...")
        response = supabase.table('consensus_totals').select("*").eq('fecha_scraping', '2025-06-29').execute()
        
        if response.data:
            df_totals = pd.DataFrame(response.data)
            print(f"   Registros en consensus_totals para 2025-06-29: {len(df_totals)}")
            
            # Buscar SF vs CHW
            sf_chw = df_totals[(df_totals['equipo_1_sigla'] == 'SF') & (df_totals['equipo_2_sigla'] == 'CHW')]
            if not sf_chw.empty:
                print(f"   ✅ Encontrado SF vs CHW en consensus_totals")
                print(f"     ID: {sf_chw.iloc[0]['id']}")
                print(f"     Total real actual: {sf_chw.iloc[0].get('total_real', 'NULL')}")
            else:
                # Buscar al revés CHW vs SF
                chw_sf = df_totals[(df_totals['equipo_1_sigla'] == 'CHW') & (df_totals['equipo_2_sigla'] == 'SF')]
                if not chw_sf.empty:
                    print(f"   ✅ Encontrado CHW vs SF en consensus_totals")
                else:
                    print(f"   ❌ No se encontró SF vs CHW en consensus_totals")
            
            # Buscar LAD vs KC
            lad_kc = df_totals[(df_totals['equipo_1_sigla'] == 'LAD') & (df_totals['equipo_2_sigla'] == 'KC')]
            if not lad_kc.empty:
                print(f"   ✅ Encontrado LAD vs KC en consensus_totals")
                print(f"     ID: {lad_kc.iloc[0]['id']}")
                print(f"     Total real actual: {lad_kc.iloc[0].get('total_real', 'NULL')}")
            else:
                print(f"   ❌ No se encontró LAD vs KC en consensus_totals")
                
        else:
            print(f"   ❌ No hay registros en consensus_totals para 2025-06-29")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def actualizar_resultados_manualmente():
    """Actualizar resultados manualmente en Supabase"""
    print(f"\n🔧 ACTUALIZANDO RESULTADOS MANUALMENTE")
    print("=" * 50)
    
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        supabase = create_client(url, key)
        
        # Resultado 1: SF vs CHW (2-5, total=7)
        print("🔄 Actualizando SF vs CHW...")
        response = supabase.table('consensus_totals').select("*").eq('equipo_1_sigla', 'SF').eq('equipo_2_sigla', 'CHW').eq('fecha_scraping', '2025-06-29').execute()
        
        if response.data:
            record_id = response.data[0]['id']
            linea_total = float(response.data[0]['linea_total'])
            total_real = 7  # 2 + 5
            resultado_real = 1 if total_real < linea_total else 2  # 1=Under, 2=Over
            
            update_result = supabase.table('consensus_totals').update({
                'puntaje_equipo_1': 2,
                'puntaje_equipo_2': 5,
                'total_real': total_real,
                'resultado_real': resultado_real,
                'efectividad': 1  # Correcto
            }).eq('id', record_id).execute()
            
            print(f"   ✅ SF vs CHW actualizado - Total real: {total_real}, Línea: {linea_total}, Resultado: {'Under' if resultado_real == 1 else 'Over'}")
        else:
            print(f"   ❌ No se encontró SF vs CHW para actualizar")
        
        # Resultado 2: LAD vs KC (5-1, total=6)
        print("🔄 Actualizando LAD vs KC...")
        response = supabase.table('consensus_totals').select("*").eq('equipo_1_sigla', 'LAD').eq('equipo_2_sigla', 'KC').eq('fecha_scraping', '2025-06-29').execute()
        
        if response.data:
            record_id = response.data[0]['id']
            linea_total = float(response.data[0]['linea_total'])
            total_real = 6  # 5 + 1
            resultado_real = 1 if total_real < linea_total else 2  # 1=Under, 2=Over
            
            update_result = supabase.table('consensus_totals').update({
                'puntaje_equipo_1': 5,
                'puntaje_equipo_2': 1,
                'total_real': total_real,
                'resultado_real': resultado_real,
                'efectividad': 1  # Correcto
            }).eq('id', record_id).execute()
            
            print(f"   ✅ LAD vs KC actualizado - Total real: {total_real}, Línea: {linea_total}, Resultado: {'Under' if resultado_real == 1 else 'Over'}")
        else:
            print(f"   ❌ No se encontró LAD vs KC para actualizar")
            
        print(f"\n✅ Actualización manual completada")
        
    except Exception as e:
        print(f"❌ Error actualizando: {e}")

def main():
    diagnosticar_resultados()
    
    respuesta = input(f"\n¿Quieres actualizar los resultados manualmente en Supabase? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'y', 'yes']:
        actualizar_resultados_manualmente()
    else:
        print("❌ Actualización cancelada")

if __name__ == "__main__":
    main()
