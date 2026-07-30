from django.contrib import admin
from .models import Division, Equipo, Partido

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'division', 'escudo')
    search_fields = ('nombre',)

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'division', 'equipo_local', 'equipo_visitante', 'fecha', 'jugado')
