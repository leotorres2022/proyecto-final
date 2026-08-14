from django.db import models


# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey('categorias.Categoria', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='tienda/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class TalleStock(models.Model):
    producto = models.ForeignKey('producto.Producto', on_delete=models.CASCADE, related_name='talles_disponibles')
    talle = models.ForeignKey('talles.Talle', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'talle')
        verbose_name = 'Talle Stock'
        verbose_name_plural = 'Talles Stock'

    def __str__(self):
        return f'{self.producto.nombre} - {self.talle.nombre}: {self.stock}'

    