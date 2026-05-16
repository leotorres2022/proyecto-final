from rest_framework import serializers
from .models import Compra

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

    def to_representation(self, instance):
        # Tomamos la representación original (que tiene los IDs)
        ret = super().to_representation(instance)
        
        # Reemplazamos los IDs por el nombre real en la respuesta
        # Asegúrate de que los modelos Talle, Categoria y Socio tengan el campo 'nombre'
        ret['talle'] = instance.talle.nombre if instance.talle else "Sin talle"
        ret['categoria'] = instance.categoria.nombre if instance.categoria else "Sin categoria"
        ret['socio'] = instance.socio.nombre if instance.socio else "Sin nombre"
        
        return ret