from django.shortcuts import render
from rest_framework import viewsets
from .models import Socio
from .serializers import SocioSerializer
# Importamos la función de Telegram para enviar mensajes al crear un socio
from .utils import enviar_notificacion_telegram

# Create your views here.

class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer

    def perform_create(self, serializer):
        # 1. Primero guardamos el socio en la base de datos y lo guardamos en una variable
        socio = serializer.save()
        print(f"[Socios] Socio creado: {socio.nombre}, telefono={socio.telefono}")
        
        # 2. Una vez guardado con éxito, disparamos la función de Telegram
        print("[Socios] Llamando a enviar_notificacion_telegram...")
        try:
            enviar_notificacion_telegram(
                nombre_socio=socio.nombre,
                telefono_socio=socio.telefono
            )
            print("[Socios] enviar_notificacion_telegram finalizado")
        except Exception as e:
            print(f"[Socios] Error al enviar Telegram: {e}")



