from rest_framework import serializers
from .models import Talle

class TalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talle
        fields = '__all__'