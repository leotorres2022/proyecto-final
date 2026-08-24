from django.shortcuts import render
from rest_framework import viewsets
from .models import Socio
from .serializers import SocioSerializer
from rest_framework.permissions import IsAuthenticated
from .permisos import IsAdminUserOrGroup

from .utils import enviar_notificacion_telegram #FUNCION DE TELEGRAM



class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrGroup]
    def perform_create(self, serializer):
      
        socio = serializer.save()
        print(f"[Socios] Socio creado: {socio.nombre}, telefono={socio.telefono}")
        print("[Socios] Llamando a enviar_notificacion_telegram...") #SI SE GUARDO CON EXITO MANDO LA FUNCION DE TELEGRAM
        try:
            enviar_notificacion_telegram(
                nombre_socio=socio.nombre,
                telefono_socio=socio.telefono
            )
            print("[Socios] enviar_notificacion_telegram finalizado")
        except Exception as e:
            print(f"[Socios] Error al enviar Telegram: {e}")



