from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Division, Equipo, Partido
from .serializers import DivisionSerializer, PartidoSerializer # Asegurate de tener estos serializers
from rest_framework.decorators import api_view


class PartidosPorDivisionListView(generics.ListAPIView):
    serializer_class = PartidoSerializer

    def get_queryset(self):
        division_id = self.kwargs['division_id']
        # Obtenemos la fecha desde la URL (ej: ?fecha=2)
        fecha = self.request.query_params.get('fecha')
        
        queryset = Partido.objects.filter(division_id=division_id)
        
        if fecha:
            queryset = queryset.filter(fecha=fecha)
            
        return queryset.order_by('-fecha', 'id')
# 1. VISTA PARA LISTAR Y CREAR DIVISIONES
# Esta es la que alimentará tu DivisionList.vue
class DivisionListCreateView(generics.ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

# 2. VISTA PARA VER, EDITAR O ELIMINAR UNA DIVISIÓN ESPECÍFICA
class DivisionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

# 3. TU VISTA DE TABLA DE POSICIONES (Optimizada)
class TablaPosicionesView(APIView):
    def get(self, request, division_id):
        equipos = Equipo.objects.filter(division_id=division_id)
        # Traemos los partidos una sola vez para no saturar la base de datos
        partidos = Partido.objects.filter(division_id=division_id, jugado=True)
        tabla = []

        for equipo in equipos:
            stats = {
                'equipo': equipo.nombre,
                'pj': 0, 'pg': 0, 'pe': 0, 'pp': 0,
                'gf': 0, 'gc': 0, 'dg': 0, 'pts': 0
            }

            for p in partidos:
                if p.equipo_local_id == equipo.id or p.equipo_visitante_id == equipo.id:
                    stats['pj'] += 1
                    es_local = (p.equipo_local_id == equipo.id)
                    goles_favor = p.goles_local if es_local else p.goles_visitante
                    goles_contra = p.goles_visitante if es_local else p.goles_local
                    
                    stats['gf'] += goles_favor
                    stats['gc'] += goles_contra
                    
                    if goles_favor > goles_contra:
                        stats['pg'] += 1
                        stats['pts'] += 3
                    elif goles_favor == goles_contra:
                        stats['pe'] += 1
                        stats['pts'] += 1
                    else:
                        stats['pp'] += 1
            
            stats['dg'] = stats['gf'] - stats['gc']
            tabla.append(stats)

        # Ordenar por puntos, luego diferencia de gol, luego goles a favor
        tabla_ordenada = sorted(
            tabla, 
            key=lambda x: (x['pts'], x['dg'], x['gf']), 
            reverse=True
        )
        return Response(tabla_ordenada)
    
    # views.py
@api_view(['POST'])
def crear_partido(request):
    serializer = PartidoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)