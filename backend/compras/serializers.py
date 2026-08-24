
from rest_framework import serializers

from .models import Compra, DetalleCompra

from producto.models import Producto, TalleStock
from talles.models import Talle
from socios.models import Socio

from producto.serializers import ProductoSerializer
from socios.serializers import SocioSerializer


class DetalleCompraSerializer(serializers.ModelSerializer):

    producto = ProductoSerializer(
        read_only=True
    )

    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='producto',
        write_only=True
    )

    talle = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    # Recibir talle_id cuando creamos la compra
    talle_id = serializers.PrimaryKeyRelatedField( 
        queryset=Talle.objects.all(),
        source='talle',
        write_only=True
    )

    class Meta:
        model = DetalleCompra

        fields = [
            'id',
            'producto',
            'producto_id',
            'talle',
            'talle_id',
            'cantidad',
            'precio_unitario'
        ]


class CompraSerializer(serializers.ModelSerializer):

    socio = SocioSerializer(
        read_only=True
    )

    socio_id = serializers.PrimaryKeyRelatedField(
        queryset=Socio.objects.all(),
        source='socio',
        write_only=True,
        required=False
    )
    detalles = DetalleCompraSerializer(
        many=True
    )

    class Meta:
        model = Compra

        fields = [
            'id',
            'socio',
            'socio_id',
            'total',
            'fecha',
            'estado',
            'detalles'
        ]
    def create(self, validated_data):

        print("========================================")
        print(" CREATE COMPRA RECIBIDA")
        detalles_data = validated_data.pop('detalles')
        print(" DETALLES RECIBIDOS:")
        print(detalles_data)
        stocks = []
        for detalle in detalles_data:

            producto = detalle['producto']
            talle = detalle['talle']
            cantidad = detalle['cantidad']

            print("----------------------------------------")
            print("Producto ID:", producto.id)
            print("Talle ID:", talle.id)
            print("Cantidad:", cantidad)

            try:

                stock = TalleStock.objects.get(
                    producto_id=producto.id,
                    talle_id=talle.id
                )

            except TalleStock.DoesNotExist:

                print(" NO EXISTE TALLESTOCK")

                raise serializers.ValidationError({
                    'detalles': [
                        f"No existe stock para "
                        f"producto {producto.id} "
                        f"y talle {talle.id}."
                    ]
                })

            if cantidad <= 0:

                raise serializers.ValidationError({
                    'detalles': [
                        f"La cantidad del producto "
                        f"{producto.id} debe ser mayor a 0."
                    ]
                })

            if cantidad > stock.stock:

                raise serializers.ValidationError({
                    'detalles': [
                        f"Stock insuficiente para "
                        f"producto {producto.id}, "
                        f"talle {talle.id}. "
                        f"Disponible: {stock.stock}. "
                        f"Solicitado: {cantidad}."
                    ]
                })

            stocks.append(
                (stock, cantidad)
            )

      
        compra = Compra.objects.create(
            **validated_data
        )

        print(" COMPRA CREADA")
        print(" ID Compra:", compra.id)

        for detalle in detalles_data:

            print(" Creando detalle:")
            print(detalle)

            DetalleCompra.objects.create(
                compra=compra,
                **detalle
            )


        for stock, cantidad in stocks:

            print("----------------------------------------")
            print(" DESCONTANDO STOCK")
            print("Stock antes:", stock.stock)
            print("Cantidad vendida:", cantidad)
            stock.stock = stock.stock - cantidad
            stock.save()
            print("STOCK DESPUÉS:", stock.stock)

        print("✅ VENTA FINALIZADA")
    

        return compra

    def update(self, instance, validated_data):

        instance.estado = validated_data.get(
            'estado',
            instance.estado
        )

        instance.save()

        return instance
