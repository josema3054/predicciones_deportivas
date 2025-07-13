# 📋 GUÍA PASO A PASO - CREAR TABLAS EN SUPABASE

## 🎯 **LO QUE VAMOS A HACER:**
Crear 3 tablas nuevas para la Fase 2:
- `mlb_consensus_winners` (pronósticos ganadores)
- `mlb_consensus_totals` (pronósticos over/under)
- `mlb_results` (resultados reales)

## 🚀 **PASOS A SEGUIR:**

### **1. Ir a Supabase Dashboard**
- Abrir navegador en: https://supabase.com/dashboard
- Iniciar sesión en tu cuenta
- Seleccionar tu proyecto

### **2. Abrir SQL Editor**
- En el menú lateral izquierdo, buscar **"SQL Editor"**
- Hacer clic en **"SQL Editor"**
- Hacer clic en **"New Query"** (botón verde)

### **3. Ejecutar el SQL**
- Abrir el archivo: `sql_fase2_simplificado.sql`
- **Copiar TODO el contenido** del archivo
- **Pegar** en el editor SQL de Supabase
- Hacer clic en **"RUN"** (botón verde)

### **4. Verificar Resultado**
Deberías ver algo como:
```
✅ CREATE TABLE mlb_consensus_winners
✅ CREATE INDEX idx_mlb_consensus_winners_fecha
✅ CREATE TABLE mlb_consensus_totals
✅ CREATE INDEX idx_mlb_consensus_totals_fecha  
✅ CREATE TABLE mlb_results
✅ CREATE INDEX idx_mlb_results_fecha
```

### **5. Verificar en Table Editor**
- Ir a **"Table Editor"** en el menú lateral
- Deberías ver las 3 tablas nuevas:
  - ✅ mlb_consensus_winners
  - ✅ mlb_consensus_totals
  - ✅ mlb_results

## 🧪 **VERIFICAR QUE FUNCIONÓ:**
Después de crear las tablas, ejecuta en tu computadora:
```bash
python tools/verificar_tablas_supabase.py
```

Deberías ver:
```
✅ mlb_consensus_winners: 0 registros
✅ mlb_consensus_totals: 0 registros  
✅ mlb_results: 0 registros
```

## 🚨 **SI HAY ERRORES:**

### **Error: "relation already exists"**
- **Solución**: Está bien, significa que ya existe
- **Continuar** con el siguiente comando

### **Error: "permission denied"**
- **Verificar**: Que estés en el proyecto correcto
- **Verificar**: Que tengas permisos de administrador

### **Error: "syntax error"**
- **Verificar**: Que copiaste TODO el SQL completo
- **Intentar**: Ejecutar una tabla a la vez

## 🎉 **CUANDO TERMINE:**
¡Perfecto! Las tablas están creadas. 

**Próximo paso:**
```bash
python tests/test_scraper_fase2.py
```

---

**📁 Archivos importantes:**
- `sql_fase2_simplificado.sql` - SQL a ejecutar
- `tools/verificar_tablas_supabase.py` - Verificar creación
- `tests/test_scraper_fase2.py` - Probar scraping
