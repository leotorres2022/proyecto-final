from django.contrib import admin
from .models import Producto, TalleStock

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria', 'imagen')
    search_fields = ('nombre',)
  
@admin.register(TalleStock)
class TalleStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'talle', 'stock')
    search_fields = ('producto__nombre', 'talle__nombre')