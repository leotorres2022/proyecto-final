from django.urls import path, include
from rest_framework.routers import DefaultRouter    
from .views import ProductoViewSet, StockPorTalleView  
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)      

urlpatterns = [
   
path('tallestock/<int:producto_id>/<int:talle_id>/', StockPorTalleView.as_view(), name='stock-producto-talle'),
path('', include(router.urls)),      
]