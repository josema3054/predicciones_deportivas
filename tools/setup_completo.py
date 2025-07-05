#!/usr/bin/env python3
"""
Script unificado para gestionar la configuración y verificación del sistema de predicciones deportivas
Uso: python setup_completo.py [comando]

Comandos disponibles:
- verificar_entorno: Verificar variables de entorno
- verificar_supabase: Verificar estado de tablas en Supabase
- configurar_demo: Crear archivo .env de ejemplo
- test_conexion: Probar conexión a Supabase
- todo: Ejecutar todos los pasos de verificación
"""

import sys
import os
from datetime import datetime

# Intentar cargar variables desde archivo .env si existe
try:
    from dotenv import load_dotenv
    if os.path.exists('.env'):
        load_dotenv()
        print("📄 Archivo .env cargado")
except ImportError:
    pass

def verificar_variables_entorno():
    """Verificar si las variables de entorno están configuradas"""
    print("\n🔍 VERIFICACIÓN DE VARIABLES DE ENTORNO")
    print("-" * 50)
    
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_ANON_KEY')
    
    print(f"SUPABASE_URL: {'✅ Configurada' if url else '❌ No encontrada'}")
    print(f"SUPABASE_ANON_KEY: {'✅ Configurada' if key else '❌ No encontrada'}")
    
    return bool(url and key)

def configurar_supabase():
    """Configurar cliente de Supabase"""
    try:
        from supabase import create_client, Client
        
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_ANON_KEY')
        
        if not url or not key:
            return None
            
        return create_client(url, key)
    except ImportError:
        print("❌ Error: Módulo supabase no encontrado. Ejecuta: pip install supabase")
        return None

def verificar_columnas_tabla(supabase, tabla_nombre):
    """Verificar las columnas de una tabla específica"""
    print(f"\n📊 Verificando estructura de la tabla '{tabla_nombre}':")
    print("-" * 50)
    
    try:
        # Intentar obtener una fila de muestra para ver la estructura
        response = supabase.table(tabla_nombre).select("*").limit(1).execute()
        
        if response.data:
            columnas = list(response.data[0].keys())
            print(f"✅ Tabla '{tabla_nombre}' encontrada con {len(columnas)} columnas")
            
            # Columnas de resultados esperadas
            columnas_resultados_esperadas = {
                'mlb_consensus': ['puntaje_equipo_1', 'puntaje_equipo_2', 'ganador_real', 'efectividad'],
                'consensus_totals': ['puntaje_equipo_1', 'puntaje_equipo_2', 'total_real', 'resultado_real', 'efectividad']
            }
            
            esperadas = columnas_resultados_esperadas.get(tabla_nombre, [])
            encontradas = [col for col in esperadas if col in columnas]
            faltantes = [col for col in esperadas if col not in columnas]
            
            print(f"   Columnas de resultados encontradas: {len(encontradas)}/{len(esperadas)}")
            
            if encontradas:
                for col in encontradas:
                    print(f"   ✅ {col}")
            
            if faltantes:
                print(f"   ❌ Columnas faltantes:")
                for col in faltantes:
                    print(f"      - {col}")
                return False
            
            return True
            
        else:
            print(f"⚠️ Tabla '{tabla_nombre}' está vacía")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar tabla '{tabla_nombre}': {e}")
        return False

def verificar_supabase():
    """Verificar estado completo de Supabase"""
    print("\n🔗 VERIFICACIÓN DE SUPABASE")
    print("-" * 50)
    
    if not verificar_variables_entorno():
        print("\n❌ Variables de entorno no configuradas")
        print("Ejecuta: python setup_completo.py configurar_demo")
        return False
    
    supabase = configurar_supabase()
    if not supabase:
        return False
    
    print("✅ Conexión a Supabase establecida")
    
    # Verificar ambas tablas
    mlb_ok = verificar_columnas_tabla(supabase, 'mlb_consensus')
    totals_ok = verificar_columnas_tabla(supabase, 'consensus_totals')
    
    # Resumen
    print(f"\n📋 RESUMEN:")
    print(f"mlb_consensus: {'✅ Completa' if mlb_ok else '❌ Requiere columnas'}")
    print(f"consensus_totals: {'✅ Completa' if totals_ok else '❌ Requiere columnas'}")
    
    if not mlb_ok or not totals_ok:
        print(f"\n⚠️ ACCIÓN REQUERIDA:")
        print(f"   1. Ve a Supabase Dashboard > SQL Editor")
        print(f"   2. Ejecuta los comandos en sql_setup_columnas.sql")
        print(f"   3. Vuelve a ejecutar: python setup_completo.py verificar_supabase")
    
    return mlb_ok and totals_ok

def configurar_demo():
    """Crear archivo .env de ejemplo"""
    print("\n📄 CREANDO ARCHIVO .env DE EJEMPLO")
    print("-" * 50)
    
    contenido_env = """# Configuración de Supabase
# Copia este archivo como .env y completa con tus credenciales

SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_clave_anonima_aqui

# Instrucciones:
# 1. Ve a tu dashboard de Supabase
# 2. Proyecto > Settings > API
# 3. Copia la URL y la anon/public key
# 4. Pégalas arriba reemplazando los valores de ejemplo
"""
    
    with open('.env.ejemplo', 'w', encoding='utf-8') as f:
        f.write(contenido_env)
    
    print("✅ Archivo .env.ejemplo creado")
    print("\n📌 Pasos siguientes:")
    print("   1. Renombra .env.ejemplo a .env")
    print("   2. Edita .env con tus credenciales de Supabase")
    print("   3. Ejecuta: python setup_completo.py verificar_supabase")

def test_conexion():
    """Probar conexión básica a Supabase"""
    print("\n🔌 PRUEBA DE CONEXIÓN")
    print("-" * 50)
    
    supabase = configurar_supabase()
    if not supabase:
        print("❌ No se pudo configurar Supabase")
        return False
    
    try:
        # Intentar una consulta simple
        response = supabase.table('mlb_consensus').select("count").limit(1).execute()
        print("✅ Conexión exitosa a Supabase")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def ejecutar_todo():
    """Ejecutar todas las verificaciones"""
    print("🚀 VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    pasos = [
        ("Verificar variables de entorno", verificar_variables_entorno),
        ("Probar conexión a Supabase", test_conexion),
        ("Verificar estructura de Supabase", verificar_supabase)
    ]
    
    resultados = []
    
    for nombre, funcion in pasos:
        print(f"\n📋 {nombre}...")
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    todos_ok = True
    for nombre, resultado in resultados:
        estado = "✅" if resultado else "❌"
        print(f"{estado} {nombre}")
        if not resultado:
            todos_ok = False
    
    if todos_ok:
        print(f"\n🎉 ¡SISTEMA LISTO!")
        print(f"✅ Todas las verificaciones pasaron")
        print(f"\n📌 Próximos pasos:")
        print(f"   python comandos.py scrape_consensus  # Scraping de consensus")
        print(f"   python comandos.py scrape_resultados # Scraping de resultados")
        print(f"   python comandos.py diagnostico       # Diagnóstico completo")
    else:
        print(f"\n⚠️ CONFIGURACIÓN PENDIENTE")
        print(f"❌ Algunos pasos requieren atención")
        print(f"\n📌 Sigue las instrucciones mostradas arriba")

def mostrar_ayuda():
    """Mostrar ayuda de comandos"""
    print("""
🔧 CONFIGURACIÓN DEL SISTEMA DE PREDICCIONES DEPORTIVAS
========================================================

Comandos disponibles:

  verificar_entorno    - Verificar variables de entorno de Supabase
  verificar_supabase   - Verificar estructura de tablas en Supabase  
  configurar_demo      - Crear archivo .env de ejemplo
  test_conexion        - Probar conexión básica a Supabase
  todo                 - Ejecutar todas las verificaciones
  help                 - Mostrar esta ayuda

Uso:
  python setup_completo.py [comando]

Ejemplos:
  python setup_completo.py todo
  python setup_completo.py verificar_supabase
  python setup_completo.py configurar_demo

Para más información consulta README.md o GUIA_WINDOWS.md
""")

def main():
    comandos = {
        'verificar_entorno': verificar_variables_entorno,
        'verificar_supabase': verificar_supabase,
        'configurar_demo': configurar_demo,
        'test_conexion': test_conexion,
        'todo': ejecutar_todo,
        'help': mostrar_ayuda
    }
    
    if len(sys.argv) < 2:
        print("❌ Comando requerido")
        mostrar_ayuda()
        return
    
    comando = sys.argv[1].lower()
    
    if comando in comandos:
        comandos[comando]()
    else:
        print(f"❌ Comando desconocido: {comando}")
        mostrar_ayuda()

if __name__ == "__main__":
    main()
