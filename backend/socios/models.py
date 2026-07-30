from django.db import models

class Socio(models.Model):
    # Opciones con palabras completas
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Moroso', 'Moroso'),
        ('Pendiente', 'Pendiente'),
    ]

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    dni = models.CharField(max_length=20, blank=True, default='')
    division = models.CharField(max_length=50, blank=True, default='')
    direccion = models.TextField()
    email = models.EmailField(unique=True)
    
    # Ajustamos max_length para que quepa la palabra más larga ("Pendiente")
    estado = models.CharField(
        max_length=15, 
        choices=ESTADO_CHOICES,
        default='Pendiente',
    )

    def __str__(self):
        return f"{self.nombre} - {self.estado}"
