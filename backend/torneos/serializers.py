from rest_framework import serializers
from .models import Division, Equipo, Partido

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'nombre']

class PartidoSerializer(serializers.ModelSerializer):
    nombre_local = serializers.ReadOnlyField(source='equipo_local.nombre')
    nombre_visitante = serializers.ReadOnlyField(source='equipo_visitante.nombre')

    class Meta:
        model = Partido
        fields = [
            'id', 'division', 'equipo_local', 'nombre_local', 
            'equipo_visitante', 'nombre_visitante', 
            'goles_local', 'goles_visitante', 'fecha', 'jugado'
        ]