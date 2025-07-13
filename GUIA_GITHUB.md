# 🐙 Guía para Subir a GitHub

## 📋 Pasos para Crear el Repositorio en GitHub

### 1. Crear Repositorio en GitHub.com

1. Ve a [GitHub.com](https://github.com) e inicia sesión
2. Haz clic en el botón **"New"** o **"+"** → **"New repository"**
3. Configura el repositorio:
   - **Repository name**: `predicciones-deportivas-mlb`
   - **Description**: `🎰 Simulador web de apuestas deportivas MLB con análisis de consensus y datos reales`
   - **Visibility**: `Public` (o `Private` si prefieres)
   - **⚠️ NO marques**: "Initialize with README" (ya tenemos uno)
   - **⚠️ NO marques**: "Add .gitignore" (ya tenemos uno)
   - **⚠️ NO marques**: "Add a license" (ya tenemos uno)
4. Haz clic en **"Create repository"**

### 2. Conectar Repositorio Local con GitHub

Ejecuta estos comandos en PowerShell:

```powershell
# Cambiar al directorio del proyecto
cd c:\Users\JVILLA\Desktop\predicciones_deportivas

# Agregar el repositorio remoto (reemplaza 'tu-usuario' con tu usuario de GitHub)
git remote add origin https://github.com/tu-usuario/predicciones-deportivas-mlb.git

# Verificar que el remote se agregó correctamente
git remote -v

# Subir la rama principal
git push -u origin simulador-web-v1
```

### 3. Configurar Rama Principal (Opcional)

Si quieres que `simulador-web-v1` sea tu rama principal:

```powershell
# Cambiar a la rama principal en GitHub
# Esto se hace desde la interfaz web de GitHub:
# Settings → Branches → Default branch → Change to simulador-web-v1
```

### 4. Agregar Descripciones y Tags

```powershell
# Crear un tag para la versión
git tag -a v1.0 -m "Simulador Web MLB v1.0 - Versión funcional"

# Subir el tag
git push origin v1.0
```

## 🔧 Comandos Útiles

### Ver Estado del Repositorio
```powershell
git status
git log --oneline -10
```

### Agregar Archivos Adicionales
```powershell
git add nombre_archivo.py
git commit -m "Descripción del cambio"
git push
```

### Crear Nueva Rama
```powershell
git checkout -b nueva-caracteristica
# ... hacer cambios ...
git add .
git commit -m "Mensaje"
git push -u origin nueva-caracteristica
```

## 📊 Información del Proyecto para GitHub

### Datos del Repositorio
- **Nombre**: predicciones-deportivas-mlb
- **Descripción**: 🎰 Simulador web de apuestas deportivas MLB con análisis de consensus y datos reales
- **Temas/Tags**: `sports-betting`, `mlb`, `flask`, `data-analysis`, `web-scraping`, `plotly`, `supabase`

### README.md Automático
El README.md existente ya contiene:
- ✅ Descripción del proyecto
- ✅ Instrucciones de instalación
- ✅ Guía de uso
- ✅ Estructura del proyecto
- ✅ Características principales

### Archivos Importantes Incluidos
- ✅ `LICENSE` - Licencia MIT
- ✅ `CHANGELOG.md` - Historial de cambios
- ✅ `requirements.txt` - Dependencias
- ✅ `.gitignore` - Archivos ignorados
- ✅ Documentación completa

## 🚀 Después de Subir a GitHub

### 1. Configurar GitHub Pages (Opcional)
Para documentación:
- Settings → Pages → Source: Deploy from a branch
- Branch: simulador-web-v1
- Folder: / (root)

### 2. Configurar Issues y Projects
- Enable Issues para reportes de bugs
- Crear Project para roadmap
- Agregar templates para issues

### 3. Configurar Releases
- Crear release v1.0 desde el tag
- Agregar descripción detallada
- Incluir archivos binarios si es necesario

### 4. Configurar Protección de Ramas
- Settings → Branches → Add rule
- Branch name pattern: `main` o `simulador-web-v1`
- Require pull request reviews

## 📱 Compartir el Proyecto

### URL del Repositorio
```
https://github.com/tu-usuario/predicciones-deportivas-mlb
```

### Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/predicciones-deportivas-mlb.git
```

### Instalar y Ejecutar
```bash
cd predicciones-deportivas-mlb
pip install -r requirements.txt
python simulador_apuestas.py
```

---

🎉 **¡Listo!** Tu proyecto estará disponible en GitHub para que otros lo vean, usen y contribuyan.
