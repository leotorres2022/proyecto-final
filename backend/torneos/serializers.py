from rest_framework import serializers
from .models import Division, Equipo, Partido
from rest_framework.permissions import IsAuthenticated
from .permisos import IsAdminUserOrGroup  

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
    def validate(self, data):
 
        equipo_local = data.get('equipo_local')
        equipo_visitante = data.get('equipo_visitante')

        if equipo_local and equipo_visitante and equipo_local == equipo_visitante:
            raise serializers.ValidationError({
                "equipo_visitante": "El equipo local y el equipo visitante no pueden ser el mismo."
            })

        #valido que los goles no sean negativos
        goles_local = data.get('goles_local', 0)
        goles_visitante = data.get('goles_visitante', 0)

        if goles_local < 0:
            raise serializers.ValidationError({
                "goles_local": "Los goles del equipo local no pueden ser negativos."
            })

        if goles_visitante < 0:
            raise serializers.ValidationError({
                "goles_visitante": "Los goles del equipo visitante no pueden ser negativos."
            })

        return data