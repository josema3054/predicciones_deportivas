# 📋 INSTRUCCIONES PARA GIT

## 🚀 Inicialización del Repositorio

### 1. Inicializar Git
```bash
cd "c:\Users\JVILLA\Desktop\predicciones_deportivas"
git init
```

### 2. Configurar Git (si es primera vez)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"
```

### 3. Crear .gitignore
```bash
# Crear archivo .gitignore con contenido básico
echo "# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/*.log

# Temporary files
*.tmp
*.temp
data/temp/*.html

# Data backups
backups/
*.bak

# Database
*.db
*.sqlite
*.sqlite3

# Jupyter Notebook
.ipynb_checkpoints

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json" > .gitignore
```

### 4. Agregar archivos al staging
```bash
git add .
```

### 5. Primer commit
```bash
git commit -m "🎉 Proyecto reorganizado - Fase 1 completada

- Estructura modular implementada
- Archivos organizados por función  
- Scripts, tests, tools y docs separados
- CSV históricos en data/csv/
- Proyecto listo para Fase 2"
```

## 🌿 Estrategia de Ramas

### Crear rama de desarrollo
```bash
git branch develop
git checkout develop
```

### Crear rama para Fase 2
```bash
git checkout -b fase-2-scraping-resultados
```

### Estructura de ramas recomendada
```
main/master     # Código estable y releases
├── develop     # Rama de desarrollo principal
│   ├── fase-2-scraping-resultados
│   ├── feature/nba-scraping
│   ├── feature/nfl-scraping
│   └── hotfix/critical-fixes
```

## 📝 Convenciones de Commits

### Formato recomendado:
```
tipo(scope): descripción

[cuerpo opcional]

[footer opcional]
```

### Tipos de commits:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato, sintaxis
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Tareas de mantenimiento

### Ejemplos:
```bash
git commit -m "feat(mlb): implementar scraping de resultados reales"
git commit -m "fix(consensus): corregir parsing de odds"
git commit -m "docs: actualizar README con nueva estructura"
git commit -m "test: agregar tests para scraper MLB"
git commit -m "refactor(core): reorganizar utilidades base"
```

## 🔄 Flujo de Trabajo

### Desarrollo diario:
```bash
# 1. Asegurar estar en la rama correcta
git checkout develop

# 2. Actualizar código
git pull origin develop

# 3. Crear rama feature
git checkout -b feature/nueva-funcionalidad

# 4. Hacer cambios y commits
git add .
git commit -m "feat: implementar nueva funcionalidad"

# 5. Subir rama
git push origin feature/nueva-funcionalidad

# 6. Crear Pull Request (si usas GitHub/GitLab)
```

### Merge a develop:
```bash
# 1. Volver a develop
git checkout develop

# 2. Merge de la feature
git merge feature/nueva-funcionalidad

# 3. Eliminar rama feature
git branch -d feature/nueva-funcionalidad

# 4. Subir develop
git push origin develop
```

## 📤 Repositorio Remoto (Opcional)

### GitHub/GitLab:
```bash
# Agregar remote
git remote add origin https://github.com/tu-usuario/predicciones-deportivas.git

# Subir por primera vez
git push -u origin main

# Subir develop
git push -u origin develop
```

### Verificar remotes:
```bash
git remote -v
```

## 🛠️ Comandos Útiles

### Estado del repositorio:
```bash
git status
git log --oneline
git branch -a
```

### Deshacer cambios:
```bash
# Deshacer cambios en archivo
git checkout -- archivo.py

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer último commit (perder cambios)
git reset --hard HEAD~1
```

### Stash (guardar cambios temporalmente):
```bash
git stash
git stash pop
git stash list
```

## 🎯 Checklist de Inicialización

- [ ] `git init` ejecutado
- [ ] `.gitignore` creado
- [ ] Configuración de usuario establecida
- [ ] Primer commit realizado
- [ ] Ramas `develop` y `fase-2` creadas
- [ ] Repositorio remoto configurado (opcional)
- [ ] Documentación de Git completada

## 📚 Recursos Adicionales

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Conventional Commits](https://www.conventionalcommits.org/)

**¡Repositorio listo para el desarrollo colaborativo! 🚀**
