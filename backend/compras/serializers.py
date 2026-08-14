
from rest_framework import serializers

from .models import Compra, DetalleCompra

from producto.models import Producto, TalleStock
from talles.models import Talle
from socios.models import Socio

from producto.serializers import ProductoSerializer
from socios.serializers import SocioSerializer


# ============================================================
# DETALLE DE COMPRA
# ============================================================

class DetalleCompraSerializer(serializers.ModelSerializer):

    # Mostrar producto cuando consultamos una compra
    producto = ProductoSerializer(
        read_only=True
    )

    # Recibir producto_id cuando creamos la compra
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='producto',
        write_only=True
    )

    # Mostrar talle cuando consultamos una compra
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


# ============================================================
# COMPRA
# ============================================================

class CompraSerializer(serializers.ModelSerializer):

    # Mostrar socio
    socio = SocioSerializer(
        read_only=True
    )

    # Recibir socio_id
    socio_id = serializers.PrimaryKeyRelatedField(
        queryset=Socio.objects.all(),
        source='socio',
        write_only=True,
        required=False
    )

    # Detalles de la compra
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

    # ========================================================
    # CREAR COMPRA
    # ========================================================

    def create(self, validated_data):

        print("========================================")
        print("🔥 CREATE COMPRA EJECUTADO")
        print("========================================")

        # Sacamos los detalles
        detalles_data = validated_data.pop('detalles')

        print("🔥 DETALLES RECIBIDOS:")
        print(detalles_data)

        # Acá guardamos los stocks que vamos a descontar
        stocks = []

        # ====================================================
        # 1. VALIDAR TODOS LOS DETALLES Y STOCK
        # ====================================================

        for detalle in detalles_data:

            producto = detalle['producto']
            talle = detalle['talle']
            cantidad = detalle['cantidad']

            print("----------------------------------------")
            print("➡️ Producto ID:", producto.id)
            print("➡️ Talle ID:", talle.id)
            print("➡️ Cantidad:", cantidad)

            # --------------------------------------------
            # Buscar stock por producto + talle
            # --------------------------------------------

            try:

                stock = TalleStock.objects.get(
                    producto_id=producto.id,
                    talle_id=talle.id
                )

            except TalleStock.DoesNotExist:

                print("❌ NO EXISTE TALLESTOCK")

                raise serializers.ValidationError({
                    'detalles': [
                        f"No existe stock para "
                        f"producto {producto.id} "
                        f"y talle {talle.id}."
                    ]
                })

            print("✅ TalleStock encontrado:", stock.id)
            print("📦 Stock antes:", stock.stock)

            # --------------------------------------------
            # Validar cantidad
            # --------------------------------------------

            if cantidad <= 0:

                raise serializers.ValidationError({
                    'detalles': [
                        f"La cantidad del producto "
                        f"{producto.id} debe ser mayor a 0."
                    ]
                })

            # --------------------------------------------
            # Validar stock disponible
            # --------------------------------------------

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

            # Guardamos el objeto stock y cantidad
            stocks.append(
                (stock, cantidad)
            )

        # ====================================================
        # 2. CREAR LA COMPRA
        # ====================================================

        compra = Compra.objects.create(
            **validated_data
        )

        print("✅ COMPRA CREADA")
        print("🧾 ID Compra:", compra.id)

        # ====================================================
        # 3. CREAR LOS DETALLES
        # ====================================================

        for detalle in detalles_data:

            print("📝 Creando detalle:")
            print(detalle)

            DetalleCompra.objects.create(
                compra=compra,
                **detalle
            )

        # ====================================================
        # 4. DESCONTAR STOCK
        # ====================================================

        for stock, cantidad in stocks:

            print("----------------------------------------")
            print("🔴 DESCONTANDO STOCK")
            print("Stock antes:", stock.stock)
            print("Cantidad vendida:", cantidad)

            stock.stock = stock.stock - cantidad

            stock.save()

            print("🟢 STOCK DESPUÉS:", stock.stock)

        print("========================================")
        print("✅ VENTA FINALIZADA")
        print("========================================")

        return compra

    # ========================================================
    # ACTUALIZAR COMPRA
    # ========================================================

    def update(self, instance, validated_data):

        instance.estado = validated_data.get(
            'estado',
            instance.estado
        )

        instance.save()

        return instance
