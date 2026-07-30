from django.test import TestCase
from rest_framework.test import APIClient
from .models import Division, Equipo, Partido


class TorneosApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.division = Division.objects.create(nombre='Primera División')
        self.equipo_local = Equipo.objects.create(nombre='Local FC', division=self.division)
        self.equipo_visitante = Equipo.objects.create(nombre='Visitante FC', division=self.division)

    def test_division_and_equipos_endpoints_return_data(self):
        response_divisiones = self.client.get('/api/torneos/division/')
        self.assertEqual(response_divisiones.status_code, 200)
        self.assertGreaterEqual(len(response_divisiones.json()), 1)

        response_equipos = self.client.get('/api/torneos/equipos/')
        self.assertEqual(response_equipos.status_code, 200)
        self.assertGreaterEqual(len(response_equipos.json()), 1)

    def test_partidos_endpoint_creates_match(self):
        payload = {
            'division': self.division.id,
            'equipo_local': self.equipo_local.id,
            'equipo_visitante': self.equipo_visitante.id,
            'goles_local': 1,
            'goles_visitante': 0,
            'fecha': 1,
            'jugado': True,
        }

        response = self.client.post('/api/torneos/partidos/', payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Partido.objects.filter(division=self.division).exists())
