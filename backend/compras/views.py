from django.shortcuts import render
from rest_framework import viewsets 
from .models import Compra
from .serializers import CompraSerializer
from rest_framework.permissions import IsAuthenticated
from .permisos import IsAdminUserOrGroup, IsAdminOrCreateAuthenticated   



class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer 
    # Permite a cualquier usuario autenticado crear (POST). Otras acciones requieren admin.
    permission_classes = [IsAuthenticated, IsAdminOrCreateAuthenticated]
    
