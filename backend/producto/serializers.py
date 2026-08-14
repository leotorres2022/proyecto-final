from rest_framework import serializers
from .models import Producto, TalleStock    

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class TalleStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalleStock
        fields = ['id', 'producto', 'talle', 'stock']