from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto                                    
from .serializers import ProductoSerializer
from .models import TalleStock
from .serializers import TalleStockSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny    

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()                             
    serializer_class = ProductoSerializer                         
    permission_classes = [IsAuthenticatedOrReadOnly]    

class StockPorTalleView(APIView):
    def get(self, request, producto_id, talle_id):
        try:
            talle_stock = TalleStock.objects.get(producto_id=producto_id, talle_id=talle_id)
            serializer = TalleStockSerializer(talle_stock)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TalleStock.DoesNotExist:
            return Response({"stock": 0}, status=status.HTTP_200_OK)