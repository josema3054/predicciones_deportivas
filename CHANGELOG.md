# 🎰 Simulador de Apuestas Deportivas MLB

## 📋 Información de la Versión

**Versión:** v1.0  
**Fecha:** 13 de julio de 2025  
**Estado:** Funcional y probado  

## 🎯 Características Principales

- ✅ **Simulador Web Completamente Funcional**
- ✅ **Parsing Correcto de Porcentajes OVER/UNDER**
- ✅ **Análisis de Efectividad con Datos Reales**
- ✅ **Distribución Balanceada de Apuestas**
- ✅ **Gráficos Interactivos con Plotly**
- ✅ **Base de Datos con 264 Registros Validados**

## 🚀 Inicio Rápido

### 1. Clona el Repositorio
```bash
git clone https://github.com/tu-usuario/predicciones-deportivas.git
cd predicciones-deportivas
```

### 2. Instala las Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configura la Base de Datos
```bash
# Configura tus credenciales de Supabase
# Crea las tablas usando: sql_crear_tablas_supabase.sql
```

### 4. Ejecuta el Simulador
```bash
python simulador_apuestas.py
```

### 5. Abre tu Navegador
```
http://localhost:5001
```

## 📊 Resultados de Prueba

### Estadísticas Verificadas
- **Total de Registros**: 284 consensus totals
- **Registros con Resultados**: 264 (93% de cobertura)
- **Apuestas Válidas**: 226 (consensus ≥ 60%)
- **Distribución**: Balanceada OVER/UNDER
- **Porcentaje de Acierto**: 50-60% (realista)

### Pruebas Realizadas
- ✅ Parsing de porcentajes corregido
- ✅ Simulación con diferentes parámetros
- ✅ Verificación de distribución balanceada
- ✅ Validación de resultados reales
- ✅ Interfaz web operativa

## 🔧 Estructura del Proyecto

```
predicciones_deportivas/
├── simulador_apuestas.py          # 🎯 Aplicación principal
├── templates/                     # 🎨 Plantillas HTML
│   ├── simulador.html            # Interfaz principal
│   └── resultados.html           # Página de resultados
├── sports/mlb/                   # 📊 Módulos MLB
│   ├── database_mlb.py          # Conexión base de datos
│   ├── scraper_mlb.py           # Scraping de datos
│   └── teams_mlb.py             # Equipos MLB
├── core/                         # 🏗️ Módulos base
├── docs/                         # 📚 Documentación
├── analizar_efectividad_completo.py  # 📈 Análisis completo
├── obtener_resultados_espn.py    # 🏈 Scraper ESPN
├── recopilador_totals_only.py    # 📥 Recopilador totals
├── verificacion_final.py         # ✅ Verificación sistema
└── requirements.txt              # 📦 Dependencias
```

## 🔍 Scripts de Verificación

### Verificar Funcionamiento
```bash
python verificacion_final.py
```

### Debug del Simulador
```bash
python debug_simulador_web.py
```

### Investigar Datos
```bash
python investigar_over_under.py
```

## 🎲 Parámetros de Simulación

### Configuración Recomendada
- **Bankroll Inicial**: $1,000
- **Monto por Apuesta**: $20
- **Consensus Mínimo**: 60-70%
- **Máximo Apuestas**: 100
- **Cuota Europea**: 1.8
- **Tipo**: Totals (Over/Under)

### Resultados Esperados
- **Porcentaje de Acierto**: 50-60%
- **ROI**: Variable según estrategia
- **Distribución**: Balanceada OVER/UNDER

## 🛠️ Mantenimiento

### Actualizar Datos
```bash
python recopilador_totals_only.py
python obtener_resultados_espn.py
```

### Limpiar Base de Datos
```bash
python limpiar_bd.py
```

### Análisis de Efectividad
```bash
python analizar_efectividad_completo.py
```

## 🚨 Problemas Conocidos Resueltos

### ✅ Parsing de Porcentajes
- **Problema**: Campos OVER/UNDER parcialmente invertidos
- **Solución**: Parsing inteligente según contenido del texto

### ✅ Distribución Sesgada
- **Problema**: Todas las apuestas eran OVER
- **Solución**: Verificación de contenido en lugar de nombre de campo

### ✅ Porcentajes Irreales
- **Problema**: 100% de acierto
- **Solución**: Corrección del parsing → 50-60% realista

## 📈 Próximas Mejoras

- [ ] Soporte para más deportes
- [ ] Análisis de tendencias temporales
- [ ] Estrategias de apuestas avanzadas
- [ ] API REST para integración
- [ ] Dashboard analítico mejorado

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añade mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún problema:
1. Revisa la documentación
2. Ejecuta `python verificacion_final.py`
3. Crea un issue en GitHub

---

⚠️ **Advertencia**: Este software es para propósitos educativos. Las apuestas deportivas involucran riesgo financiero. Apuesta responsablemente.
