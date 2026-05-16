from django.db import models

# Create your models here.

class Talle(models.Model):
    nombre = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre
