from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from categorias.models import Categoria
from producto.models import Producto, TalleStock
from talles.models import Talle


class SeedProductosTests(TestCase):
    def test_seed_productos_creates_default_products(self):
        out = StringIO()
        call_command('seed_productos', stdout=out)

        self.assertEqual(Producto.objects.count(), 5)
        self.assertIn('Camiseta titular', [p.nombre for p in Producto.objects.all()])


class StockPorTalleTests(TestCase):
    def test_get_stock_by_producto_and_talle(self):
        categoria = Categoria.objects.create(nombre='Deportiva')
        producto = Producto.objects.create(nombre='Camiseta', precio=100, categoria=categoria)
        talle, _ = Talle.objects.get_or_create(nombre='M')
        TalleStock.objects.create(producto=producto, talle=talle, stock=7)

        url = reverse('talle_stock', kwargs={'producto_id': producto.id, 'talle_id': talle.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['stock'], 7)
