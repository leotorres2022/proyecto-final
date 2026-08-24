from rest_framework import serializers
from .models import Producto, TalleStock    

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre no puede estar vacío."
            )
        return value

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor a 0."
            )
        return value

    def validate_categoria(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debe seleccionar una categoría."
            )
        return value        

class TalleStockSerializer(serializers.ModelSerializer):

    producto_nombre = serializers.CharField(
        source='producto.nombre',
        read_only=True
    )

    categoria_nombre = serializers.CharField(
        source='producto.categoria.nombre',
        read_only=True
    )

    talle_nombre = serializers.CharField(
        source='talle.nombre',
        read_only=True
    )

    class Meta:
        model = TalleStock
        fields = [
            'id',
            'producto',
            'producto_nombre',
            'categoria_nombre',
            'talle',
            'talle_nombre',
            'stock'
        ]        