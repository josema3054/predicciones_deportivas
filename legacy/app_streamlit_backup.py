import streamlit as st
from datetime import date, timedelta
import pandas as pd
import os

# Configurar la página
st.set_page_config(page_title="Sistema de Análisis de Consensus Deportivo", layout="wide")

try:
    st.title("🏆 Sistema de Análisis de Consensus Deportivo")
    st.markdown("**Automatización completa:** Consensus + Resultados + Análisis de Efectividad")

    # Pestañas principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Scraping Consensus", "🏆 Scraping Resultados", "📈 Pipeline Completo", "📋 Análisis Histórico", "🔧 Herramientas Dev"])

    # === TAB 1: SCRAPING CONSENSUS ===
    with tab1:
        st.header("📊 Scraping de Consensus")
        
        # Selección de fechas
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Fecha inicio", value=date.today() - timedelta(days=2), key="consensus_inicio")
        with col2:
            fecha_fin = st.date_input("Fecha fin", value=date.today(), key="consensus_fin")

        # Selección de deportes
        opciones_deportes = ["mlb", "cfl", "wnba"]  # Puedes agregar más deportes
        seleccionados = st.multiselect("Deportes a scrapear", opciones_deportes, default=["mlb"], key="consensus_deportes")

        # Selección de tipo de consensus
        st.subheader("Tipo de Consensus")
        col3, col4 = st.columns(2)
        with col3:
            consensus_winners = st.checkbox("Winners/Losers Consensus", value=True)
        with col4:
            consensus_totals = st.checkbox("Over/Under Totals Consensus", value=False)

        # Botón para lanzar scraping de consensus
        if st.button("🚀 Iniciar Scraping Consensus", key="btn_consensus"):
            try:
                from scraper_historico import scrapear_consensus_por_fecha, scrapear_consensus_totals_por_fecha
                
                if not consensus_winners and not consensus_totals:
                    st.error("Selecciona al menos un tipo de consensus para scrapear.")
                else:
                    st.write(f"Scraping desde {fecha_inicio} hasta {fecha_fin} para: {', '.join(seleccionados)}")
                    total = 0
                    
                    for deporte in seleccionados:
                        st.info(f"Scrapeando {deporte.upper()}...")
                        fecha_actual = fecha_inicio
                        
                        while fecha_actual <= fecha_fin:
                            fecha_str = fecha_actual.strftime("%Y-%m-%d")
                            
                            # Scrapear Winners/Losers si está seleccionado
                            if consensus_winners:
                                with st.spinner(f"Scrapeando {deporte.upper()} WINNERS para {fecha_str}..."):
                                    try:
                                        scrapear_consensus_por_fecha(fecha_str, deporte=deporte)
                                        st.success(f"✅ {deporte.upper()} WINNERS {fecha_str}")
                                    except Exception as e:
                                        st.error(f"❌ Error en {deporte.upper()} WINNERS {fecha_str}: {e}")
                            
                            # Scrapear Over/Under si está seleccionado
                            if consensus_totals:
                                with st.spinner(f"Scrapeando {deporte.upper()} TOTALS para {fecha_str}..."):
                                    try:
                                        scrapear_consensus_totals_por_fecha(fecha_str, deporte=deporte)
                                        st.success(f"✅ {deporte.upper()} TOTALS {fecha_str}")
                                    except Exception as e:
                                        st.error(f"❌ Error en {deporte.upper()} TOTALS {fecha_str}: {e}")
                            
                            fecha_actual += timedelta(days=1)
                            total += 1
                    
                    st.success(f"🎉 Scraping de consensus finalizado para {total} días/deporte(s)")
            except Exception as e:
                st.error(f"Error al iniciar el scraping: {e}")

    # === TAB 2: SCRAPING RESULTADOS ===
    with tab2:
        st.header("🏆 Scraping de Resultados Reales")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_resultados = st.date_input("Fecha de los partidos", value=date.today() - timedelta(days=1), key="resultados_fecha")
        with col2:
            deporte_resultados = st.selectbox("Deporte", opciones_deportes, key="resultados_deporte")
        
        if st.button("🎯 Scrapear Resultados", key="btn_resultados"):
            try:
                from scraper_historico import scrape_resultados_deportivos, guardar_resultados_en_supabase
                
                fecha_str = fecha_resultados.strftime("%Y-%m-%d")
                
                with st.spinner(f"Scrapeando resultados de {deporte_resultados.upper()} para {fecha_str}..."):
                    resultados = scrape_resultados_deportivos(deporte_resultados, fecha_str)
                    
                    if resultados:
                        guardar_resultados_en_supabase(resultados, deporte_resultados)
                        
                        st.success(f"✅ {len(resultados)} resultados procesados para {deporte_resultados.upper()} - {fecha_str}")
                        
                        # Mostrar preview de resultados
                        df_resultados = pd.DataFrame(resultados)
                        st.subheader("📋 Preview de Resultados")
                        st.dataframe(df_resultados[['nombre_equipo_1', 'nombre_equipo_2', 'puntaje_equipo_1', 'puntaje_equipo_2', 'resultado_nombre', 'total_puntos', 'over_under']])
                    else:
                        st.warning("⚠️ No se encontraron resultados para esta fecha")
                        
            except Exception as e:
                st.error(f"❌ Error al scrapear resultados: {e}")

    # === TAB 3: PIPELINE COMPLETO ===
    with tab3:
        st.header("🚀 Pipeline Completo: Consensus + Resultados + Análisis")
        st.markdown("**Ejecuta todo el proceso automáticamente:** consensus, resultados y análisis de efectividad")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_pipeline = st.date_input("Fecha a procesar", value=date.today() - timedelta(days=1), key="pipeline_fecha")
        with col2:
            deporte_pipeline = st.selectbox("Deporte", opciones_deportes, key="pipeline_deporte")
        
        if st.button("🔥 Ejecutar Pipeline Completo", key="btn_pipeline"):
            try:
                from scraper_historico import scrape_y_analizar_fecha_completa
                
                fecha_str = fecha_pipeline.strftime("%Y-%m-%d")
                
                with st.spinner(f"Ejecutando pipeline completo para {deporte_pipeline.upper()} - {fecha_str}..."):
                    # Capturar output en contenedor expandible
                    with st.expander("📋 Log del Pipeline", expanded=True):
                        scrape_y_analizar_fecha_completa(deporte_pipeline, fecha_str)
                    
                    st.success(f"✅ Pipeline completo finalizado para {deporte_pipeline.upper()} - {fecha_str}")
                    st.info("📊 Revisa el log para ver estadísticas detalladas y archivos CSV generados")
                    
            except Exception as e:
                st.error(f"❌ Error en pipeline completo: {e}")

    # === TAB 4: ANÁLISIS HISTÓRICO ===
    with tab4:
        st.header("📈 Análisis de Efectividad Histórico")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_analisis = st.date_input("Fecha a analizar", value=date.today() - timedelta(days=1), key="analisis_fecha")
        with col2:
            deporte_analisis = st.selectbox("Deporte", opciones_deportes, key="analisis_deporte")
        
        if st.button("📊 Analizar Efectividad", key="btn_analisis"):
            try:
                from scraper_historico import analizar_efectividad_consensus
                
                fecha_str = fecha_analisis.strftime("%Y-%m-%d")
                
                with st.spinner(f"Analizando efectividad para {deporte_analisis.upper()} - {fecha_str}..."):
                    analisis = analizar_efectividad_consensus(deporte_analisis, fecha_str)
                    
                    if "error" not in analisis:
                        # Mostrar métricas principales
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Partidos", analisis['total_partidos'])
                        with col2:
                            st.metric("Con Consensus", analisis['partidos_con_consensus'])
                        with col3:
                            st.metric("Efectividad Winners", f"{analisis['efectividad_winners']}%")
                        with col4:
                            st.metric("Efectividad Totals", f"{analisis['efectividad_totals']}%")
                        
                        # Mostrar detalles
                        if analisis['detalles']:
                            st.subheader("📋 Detalles por Partido")
                            df_detalles = pd.DataFrame(analisis['detalles'])
                            st.dataframe(df_detalles)
                            
                            # Gráfico de efectividad
                            winners_pct = analisis['efectividad_winners']
                            totals_pct = analisis['efectividad_totals']
                            
                            chart_data = pd.DataFrame({
                                'Tipo': ['Winners/Losers', 'Over/Under'],
                                'Efectividad %': [winners_pct, totals_pct]
                            })
                            
                            st.subheader("📊 Efectividad del Consensus")
                            st.bar_chart(chart_data.set_index('Tipo'))
                    else:
                        st.error(f"❌ {analisis['error']}")
                        
            except Exception as e:
                st.error(f"❌ Error en análisis: {e}")
        
        # Información adicional
        st.markdown("---")
        st.markdown("### 📚 Información del Sistema")
        st.markdown("""
        **Funcionalidades disponibles:**
        - 📊 **Consensus Scraping**: Winners/Losers y Over/Under desde Covers.com
        - 🏆 **Resultados Reales**: Puntajes y estadísticas finales de partidos
        - 📈 **Análisis Cruzado**: Efectividad del consensus vs resultados reales
        - 💾 **Almacenamiento**: Supabase + backup CSV automático
        - 🔍 **Prevención Duplicados**: Sistema inteligente de verificación
        
        **Deportes soportados:** MLB, CFL, WNBA (expandible)
        """)

    # === TAB 5: HERRAMIENTAS DE DESARROLLO ===
    with tab5:
        st.header("🔧 Herramientas de Desarrollo")
        st.markdown("**Herramientas para testing y mantenimiento del sistema**")
        
        # Sección de limpieza de base de datos
        st.subheader("🗑️ Limpieza de Base de Datos")
        st.warning("⚠️ **ATENCIÓN**: Estas operaciones eliminarán datos permanentemente.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Limpiar tablas específicas:**")
            tabla_limpiar = st.selectbox(
                "Selecciona tabla a limpiar:",
                ["consensus", "consensus_totals", "ambas"],
                key="tabla_limpiar"
            )
            
            if st.button("🗑️ Limpiar Tabla Seleccionada", key="btn_limpiar_tabla"):
                if st.session_state.get('confirmar_limpieza', False):
                    try:
                        from limpiar_tablas import limpiar_tablas_supabase
                        
                        with st.spinner("Limpiando tabla(s)..."):
                            if tabla_limpiar == "ambas":
                                result1 = limpiar_tablas_supabase("consensus")
                                result2 = limpiar_tablas_supabase("consensus_totals")
                                st.success(f"✅ Tablas limpiadas: consensus ({result1} registros), consensus_totals ({result2} registros)")
                            else:
                                result = limpiar_tablas_supabase(tabla_limpiar)
                                st.success(f"✅ Tabla {tabla_limpiar} limpiada: {result} registros eliminados")
                                
                        st.session_state['confirmar_limpieza'] = False
                        
                    except Exception as e:
                        st.error(f"❌ Error al limpiar tabla: {e}")
                else:
                    st.session_state['confirmar_limpieza'] = True
                    st.warning("⚠️ Haz clic de nuevo para confirmar la eliminación")
        
        with col2:
            st.markdown("**Limpiar archivos CSV:**")
            if st.button("🗑️ Limpiar Archivos CSV", key="btn_limpiar_csv"):
                try:
                    import glob
                    import os
                    
                    csv_files = glob.glob("mlb_*.csv")
                    deleted_count = 0
                    
                    with st.spinner("Eliminando archivos CSV..."):
                        for file in csv_files:
                            try:
                                os.remove(file)
                                deleted_count += 1
                            except Exception as e:
                                st.warning(f"No se pudo eliminar {file}: {e}")
                    
                    st.success(f"✅ Eliminados {deleted_count} archivos CSV")
                    
                except Exception as e:
                    st.error(f"❌ Error al limpiar CSV: {e}")
        
        # Sección de verificación del sistema
        st.subheader("🔍 Verificación del Sistema")
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("📊 Verificar Estado Base de Datos", key="btn_verificar_bd"):
                try:
                    from supabase import create_client
                    
                    url = os.getenv("SUPABASE_URL")
                    key = os.getenv("SUPABASE_ANON_KEY")
                    supabase = create_client(url, key)
                    
                    with st.spinner("Verificando base de datos..."):
                        # Verificar consensus
                        response_consensus = supabase.table('consensus').select("*", count="exact").execute()
                        count_consensus = response_consensus.count
                        
                        # Verificar consensus_totals
                        response_totals = supabase.table('consensus_totals').select("*", count="exact").execute()
                        count_totals = response_totals.count
                        
                        st.success("✅ Conexión a Supabase exitosa")
                        st.info(f"📊 **Registros en base de datos:**\n- Consensus: {count_consensus}\n- Consensus Totals: {count_totals}")
                        
                except Exception as e:
                    st.error(f"❌ Error al verificar base de datos: {e}")
        
        with col4:
            if st.button("📁 Verificar Archivos CSV", key="btn_verificar_csv"):
                try:
                    import glob
                    
                    csv_files = glob.glob("mlb_*.csv")
                    
                    if csv_files:
                        st.success(f"✅ Encontrados {len(csv_files)} archivos CSV:")
                        for file in csv_files:
                            size = os.path.getsize(file) / 1024  # Size in KB
                            st.text(f"• {file} ({size:.1f} KB)")
                    else:
                        st.info("📁 No se encontraron archivos CSV")
                        
                except Exception as e:
                    st.error(f"❌ Error al verificar CSV: {e}")
        
        # Sección de pruebas rápidas
        st.subheader("🧪 Pruebas Rápidas")
        
        fecha_prueba = st.date_input("Fecha para pruebas", value=date.today() - timedelta(days=1), key="fecha_prueba")
        
        col5, col6 = st.columns(2)
        
        with col5:
            if st.button("🧪 Test Scraping Resultados", key="btn_test_resultados"):
                try:
                    from scraper_historico import scrape_resultados_deportivos
                    
                    fecha_str = fecha_prueba.strftime("%Y-%m-%d")
                    
                    with st.spinner(f"Probando scraping de resultados para {fecha_str}..."):
                        resultados = scrape_resultados_deportivos("mlb", fecha_str)
                        
                        if resultados:
                            st.success(f"✅ Test exitoso: {len(resultados)} partidos encontrados")
                            st.json(resultados[:3])  # Mostrar primeros 3 resultados
                        else:
                            st.warning("⚠️ No se encontraron resultados para esa fecha")
                            
                except Exception as e:
                    st.error(f"❌ Error en test de resultados: {e}")
        
        with col6:
            if st.button("🧪 Test Scraping Consensus", key="btn_test_consensus"):
                try:
                    from scraper_historico import scrapear_consensus_por_fecha
                    
                    fecha_str = fecha_prueba.strftime("%Y-%m-%d")
                    
                    with st.spinner(f"Probando scraping de consensus para {fecha_str}..."):
                        consensus = scrapear_consensus_por_fecha("mlb", fecha_str)
                        
                        if consensus:
                            st.success(f"✅ Test exitoso: {len(consensus)} partidos encontrados")
                            st.json(consensus[:3])  # Mostrar primeros 3 resultados
                        else:
                            st.warning("⚠️ No se encontraron consensus para esa fecha")
                            
                except Exception as e:
                    st.error(f"❌ Error en test de consensus: {e}")
        
        # Información de estado
        st.markdown("---")
        st.markdown("### ℹ️ Información de Desarrollo")
        st.markdown("""
        **Variables de entorno requeridas:**
        - `SUPABASE_URL`: ✅ Configurada
        - `SUPABASE_ANON_KEY`: ✅ Configurada
        
        **Scripts disponibles:**
        - `scraper_historico.py`: Script principal de scraping
        - `limpiar_tablas.py`: Limpieza de base de datos
        - `equipos_data.py`: Diccionario de equipos y conversiones
        """)

except Exception as e:
    st.error(f"❌ Error al iniciar la aplicación: {e}")
    st.markdown("**Solución sugerida:** Verifica que el archivo `scraper_historico.py` esté presente y las dependencias instaladas.")
