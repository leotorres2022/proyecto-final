from django.db import models

# Create your models here.

class Socio(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre
