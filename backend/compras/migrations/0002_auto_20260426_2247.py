from django.db import migrations

def cargar_compras_iniciales(apps, schema_editor):
    Compra = apps.get_model('compras', 'Compra')
    Socio = apps.get_model('socios', 'Socio')
    Talle = apps.get_model('talles', 'Talle')
    Categoria = apps.get_model('categorias', 'Categoria')
    
    # (descripcion, precio, cantidad, talle_id, categoria_id, socio_id)
    datos_compras = [
        ("Camiseta titular 2024", 15000.0, 20, 1, 1, 12),
        ("Short oficial", 9000.0, 15, 2, 2, 13),
        ("Medias deportivas", 4000.0, 30, 3, 3, 14),
        ("Camiseta suplente 2024", 15500.0, 10, 1, 1, 15),
        ("Buzo entrenamiento", 18000.0, 8, 4, 4, 16)
    ]
    
    for desc, precio, cant, t_id, c_id, s_id in datos_compras:
        try:
            # Buscamos todos los objetos relacionados
            socio_obj = Socio.objects.get(id=s_id)
            talle_obj = Talle.objects.get(id=t_id)
            cat_obj = Categoria.objects.get(id=c_id)
            
            Compra.objects.create(
                descripcion=desc,
                precio=precio,
                cantidad=cant,
                socio=socio_obj,      # Agregamos el socio
                talle=talle_obj,
                categoria=cat_obj
            )
        except (Socio.DoesNotExist, Talle.DoesNotExist, Categoria.DoesNotExist):
            print(f"Error: No se encontró relación para {desc}")

class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
        ('socios', '0001_initial'),     # Importante: depende de que existan los socios
        ('talles', '0002_auto_20260426_2243'),       # Pon el nombre real de tu migración de talles
        ('categorias', '0002_auto_20260426_2245'),   # Pon el nombre real de tu migración de categorías
    ]

    operations = [
        migrations.RunPython(cargar_compras_iniciales),
    ]
