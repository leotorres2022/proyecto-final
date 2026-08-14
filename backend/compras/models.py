from django.db import models
from django.core.validators import MinValueValidator

class Compra(models.Model):
    ESTADO_COMPRAS = [
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_COMPRAS, default='pendiente')


    def __str__(self):
        return f"Compra #{self.id} - {self.estado}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        'producto.Producto',
        on_delete=models.CASCADE
    )

    talle = models.ForeignKey(
    'talles.Talle',
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
