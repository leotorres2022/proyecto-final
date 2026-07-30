from django.db import models

# Create your models here.
class Compra(models.Model):
    ESTADO_COMPRAS = [
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    descripcion = models.CharField(max_length=255)
    precio = models.FloatField()
    cantidad = models.IntegerField()
    talle = models.ForeignKey('talles.Talle', on_delete=models.CASCADE)
    categoria = models.ForeignKey('categorias.Categoria', on_delete=models.CASCADE)
    socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_COMPRAS, default='pendiente')

    def __str__(self):
        return f"Compra #{self.id} - {self.estado}"
        return f"{self.descripcion} - Socio: {self.socio}"
