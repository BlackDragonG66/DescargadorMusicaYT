# Guía para Crear Releases en GitHub

## Opción 1: Build Local (Windows)

1. Abre una terminal en la carpeta del proyecto
2. Ejecuta:
   ```bash
   build.bat
   ```
3. Espera a que termine (tomará unos 5-10 minutos)
4. El .exe estará en: `dist/DescargadorMusicaYT.exe`

## Opción 2: Crear Release en GitHub

### Paso 1: Verificar cambios
```bash
git status
```

### Paso 2: Hacer commit final (si hay cambios)
```bash
git add .
git commit -m "Versión X.X.X"
git push origin main
```

### Paso 3: Crear tag (etiqueta)
```bash
git tag -a v1.0.0 -m "Release v1.0.0 - Primera versión estable"
git push origin v1.0.0
```

### Paso 4: GitHub creará automáticamente
- ✓ Una Release página en GitHub
- ✓ Descargará el código fuente (ZIP)
- ✓ Compilará el .exe automáticamente (GitHub Actions)

## Ejemplo de Versiones

```
v0.1.0 - Primera versión beta
v1.0.0 - Primera versión estable
v1.1.0 - Nueva característica
v1.0.1 - Fix de bugs
```

## En GitHub verás:

```
Your project
├── Releases
│   ├── v1.0.0
│   │   ├── DescargadorMusicaYT.exe
│   │   ├── Source code (zip)
│   │   ├── Source code (tar.gz)
│   │   └── Notas del release
│   └── ...
└── Code
```

## Pasos Actuales Realizados

1. ✓ Creado `build.spec` para PyInstaller
2. ✓ Creado `build.bat` para compilación local
3. ✓ Configurado GitHub Actions en `.github/workflows/build.yml`
4. ✓ README.md actualizado con instrucciones completas
5. ✓ .gitignore mejorado

## Próximos Pasos

1. Ejecuta `build.bat` para crear el .exe local
2. Prueba el .exe
3. Crea un tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. Push: `git push origin v1.0.0`
5. GitHub Actions compilará automáticamente
6. Verás el release en https://github.com/BlackDragonG66/DescargadorMusicaYT/releases

## Solución de Problemas

### El .exe es muy grande
- Es normal (incluye Python + librerías)
- Tamaño típico: 200-300MB

### GitHub Actions falla
- Revisa la sección "Actions" en GitHub
- Verifica que el token tenga permisos

### .exe no funciona
- Asegúrate de tener FFmpeg instalado
- Intenta ejecutar desde cmd para ver errores
