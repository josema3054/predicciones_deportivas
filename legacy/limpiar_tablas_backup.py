#!/usr/bin/env python3
"""
Script para vaciar/limpiar todas las tablas de consensus en Supabase
ADVERTENCIA: Este script eliminará TODOS los datos de las tablas
"""

import os
from dotenv import load_dotenv

load_dotenv()

def vaciar_tablas_consensus():
    """Vaciar completamente las tablas de consensus"""
    print("🗑️ LIMPIEZA COMPLETA DE TABLAS DE CONSENSUS")
    print("=" * 60)
    print("⚠️ ADVERTENCIA: Este script eliminará TODOS los datos de las siguientes tablas:")
    print("   • mlb_consensus")
    print("   • consensus_totals")
    print("   • mlb_resultados (si existe)")
    print()
    
    # Pedir confirmación
    confirmacion = input("¿Estás seguro de que quieres continuar? (escribe 'SI' para confirmar): ")
    
    if confirmacion.upper() != 'SI':
        print("❌ Operación cancelada por el usuario")
        return
    
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("❌ No hay configuración de Supabase")
            return
            
        supabase = create_client(url, key)
        
        tablas_a_limpiar = [
            'mlb_consensus',
            'consensus_totals',
            'mlb_resultados'
        ]
        
        print(f"\n🧹 INICIANDO LIMPIEZA...")
        
        for tabla in tablas_a_limpiar:
            try:
                print(f"\n📊 Limpiando tabla '{tabla}'...")
                
                # Primero verificar si la tabla existe y tiene datos
                response = supabase.table(tabla).select("id").limit(1).execute()
                
                if response.data:
                    # Contar registros actuales
                    count_response = supabase.table(tabla).select("id").execute()
                    total_registros = len(count_response.data) if count_response.data else 0
                    
                    print(f"   📈 Registros encontrados: {total_registros}")
                    
                    if total_registros > 0:
                        # Eliminar todos los registros
                        # Nota: Supabase requiere una condición, así que usamos una condición que siempre sea verdadera
                        delete_response = supabase.table(tabla).delete().neq('id', 0).execute()
                        
                        print(f"   ✅ Tabla '{tabla}' limpiada exitosamente")
                    else:
                        print(f"   ℹ️ Tabla '{tabla}' ya estaba vacía")
                else:
                    print(f"   ℹ️ Tabla '{tabla}' no existe o ya está vacía")
                    
            except Exception as e:
                print(f"   ⚠️ Error limpiando tabla '{tabla}': {e}")
        
        print(f"\n🎉 LIMPIEZA COMPLETADA")
        print("=" * 60)
        print("✅ Las tablas han sido vaciadas exitosamente")
        print("✅ Ahora puedes probar el scraping día a día desde cero")
        
        # Verificación final
        print(f"\n🔍 VERIFICACIÓN FINAL:")
        for tabla in tablas_a_limpiar:
            try:
                response = supabase.table(tabla).select("id").execute()
                registros_restantes = len(response.data) if response.data else 0
                status = "✅ VACÍA" if registros_restantes == 0 else f"⚠️ {registros_restantes} registros"
                print(f"   {tabla}: {status}")
            except:
                print(f"   {tabla}: ℹ️ No accesible")
                
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

def vaciar_solo_fecha(fecha):
    """Vaciar datos de una fecha específica"""
    print(f"🗑️ LIMPIEZA DE DATOS PARA LA FECHA: {fecha}")
    print("=" * 60)
    
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        supabase = create_client(url, key)
        
        tablas = ['mlb_consensus', 'consensus_totals']
        
        for tabla in tablas:
            try:
                # Contar registros de la fecha
                count_response = supabase.table(tabla).select("id").eq('fecha_scraping', fecha).execute()
                total_registros = len(count_response.data) if count_response.data else 0
                
                print(f"📊 Tabla '{tabla}': {total_registros} registros para {fecha}")
                
                if total_registros > 0:
                    # Eliminar registros de la fecha específica
                    delete_response = supabase.table(tabla).delete().eq('fecha_scraping', fecha).execute()
                    print(f"   ✅ Eliminados {total_registros} registros de '{tabla}'")
                else:
                    print(f"   ℹ️ No hay registros para {fecha} en '{tabla}'")
                    
            except Exception as e:
                print(f"   ❌ Error con tabla '{tabla}': {e}")
                
        print(f"\n✅ Limpieza completada para la fecha {fecha}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def menu_limpieza():
    """Menú principal para seleccionar tipo de limpieza"""
    print("🧹 HERRAMIENTA DE LIMPIEZA DE TABLAS")
    print("=" * 60)
    print("Selecciona una opción:")
    print("1. Vaciar TODAS las tablas completamente")
    print("2. Vaciar datos de una fecha específica")
    print("3. Cancelar")
    print()
    
    opcion = input("Ingresa tu opción (1-3): ")
    
    if opcion == "1":
        vaciar_tablas_consensus()
    elif opcion == "2":
        fecha = input("Ingresa la fecha a limpiar (YYYY-MM-DD): ")
        if fecha:
            vaciar_solo_fecha(fecha)
        else:
            print("❌ Fecha no válida")
    elif opcion == "3":
        print("❌ Operación cancelada")
    else:
        print("❌ Opción no válida")

def main():
    menu_limpieza()

if __name__ == "__main__":
    main()

def limpiar_tablas_supabase(tabla_nombre=None):
    """
    Función para limpiar tablas desde la interfaz web
    Args:
        tabla_nombre: Nombre de la tabla a limpiar ('consensus', 'consensus_totals' o None para ambas)
    Returns:
        int: Número de registros eliminados
    """
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise Exception("No hay configuración de Supabase")
            
        supabase = create_client(url, key)
        
        # Mapear nombres de tabla
        if tabla_nombre == "consensus":
            tabla_real = "mlb_consensus"
        elif tabla_nombre == "consensus_totals":
            tabla_real = "consensus_totals"
        elif tabla_nombre == "ambas":
            # Limpiar ambas tablas
            count1 = limpiar_tablas_supabase("consensus")
            count2 = limpiar_tablas_supabase("consensus_totals")
            return count1 + count2
        else:
            tabla_real = tabla_nombre
        
        # Contar registros antes de eliminar
        response = supabase.table(tabla_real).select("id").execute()
        registros_antes = len(response.data) if response.data else 0
        
        if registros_antes == 0:
            return 0
        
        # Eliminar todos los registros
        # Usar delete con un filtro que siempre sea true (como id >= 0)
        delete_response = supabase.table(tabla_real).delete().neq('id', -999999).execute()
        
        # Verificar registros después
        response_after = supabase.table(tabla_real).select("id").execute()
        registros_despues = len(response_after.data) if response_after.data else 0
        
        return registros_antes - registros_despues
        
    except Exception as e:
        raise Exception(f"Error al limpiar tabla {tabla_nombre}: {e}")
