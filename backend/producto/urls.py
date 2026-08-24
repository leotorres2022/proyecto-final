from django.urls import path, include
from rest_framework.routers import DefaultRouter    
from .views import ProductoViewSet, StockPorTalleView  ,ListaStockView
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)      

urlpatterns = [
   
path('tallestock/<int:producto_id>/<int:talle_id>/', StockPorTalleView.as_view(), name='stock-producto-talle'),
path( 'tallestock/',ListaStockView.as_view(), name='lista-stock'),
path('', include(router.urls)),  

]