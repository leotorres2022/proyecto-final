# torneos/urls.py
from django.urls import path
from .views import (
    DivisionListCreateView, 
    DivisionRetrieveUpdateDestroyView, 
    TablaPosicionesView,
    PartidosPorDivisionListView
)

urlpatterns = [
    path('division/', DivisionListCreateView.as_view(), name='division-list'),
    path('division/<int:pk>/', DivisionRetrieveUpdateDestroyView.as_view(), name='division-detail'),
    path('division/<int:division_id>/tabla/', TablaPosicionesView.as_view(), name='tabla-posiciones'),
    path('division/<int:division_id>/partidos/', PartidosPorDivisionListView.as_view(), name='partidos-division'),
]
