"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from socios.views import SocioViewSet
from talles.views import TalleViewSet
from categorias.views import CategoriaViewSet
from compras.views import CompraViewSet 

# 1. Configuración de Routers (Solo para ViewSets de Socios, Talles, etc.)
router = routers.DefaultRouter()
router.register(r'socios', SocioViewSet)
router.register(r'talles', TalleViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'compras', CompraViewSet)

# 2. Configuración de URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas automáticas del router (socios, talles, etc.)
    path('api/', include(router.urls)),
    
    # Rutas manuales de TORNEOS (Donde están divisiones, tabla y partidos)
    # IMPORTANTE: Esto hará que las rutas empiecen con 'api/torneos/'
    path('api/torneos/', include('torneos.urls')),
]
