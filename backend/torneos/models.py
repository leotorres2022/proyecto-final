from django.db import models

class Division(models.Model):
    nombre = models.CharField(max_length=50) # Ej: "7ma División"
    
    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Partido(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    equipo_local = models.ForeignKey(Equipo, related_name='locales', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='visitantes', on_delete=models.CASCADE)
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    fecha = models.PositiveIntegerField(default=1)
    jugado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"
# Create your models here.
