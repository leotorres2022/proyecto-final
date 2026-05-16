from django.shortcuts import render
from rest_framework import viewsets
from .models import Talle
from .serializers import TalleSerializer

# Create your views here.

class TalleViewSet(viewsets.ModelViewSet):
    queryset = Talle.objects.all()
    serializer_class = TalleSerializer
