# InfluencerConnect

Una plataforma para conectar empresas e influencers desarrollada con Django.

## Instalación

1. Clona este repositorio
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Realiza las migraciones: `python manage.py migrate`
6. Inicia el servidor: `python manage.py runserver`

## Estructura del proyecto

- `influencer_connect/` - Directorio principal del proyecto Django
  - `settings.py` - Configuración del proyecto
  - `urls.py` - Configuración de URLs
  - `wsgi.py` y `asgi.py` - Configuración para despliegue
- `templates/` - Plantillas HTML
  - `base.html` - Plantilla base con el diseño principal
  - `home.html` - Página de inicio
- `static/` - Archivos estáticos (CSS, JS, imágenes)
- `media/` - Archivos subidos por los usuarios
- `manage.py` - Script de gestión de Django

## Características

- Diseño moderno y responsive con Bootstrap 5
- Nombre "InfluencerConnect" destacado en la parte superior central
- Estructura básica lista para implementar funcionalidades

