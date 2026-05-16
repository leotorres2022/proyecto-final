from django.db import migrations

def cargar_talles_iniciales(apps, schema_editor):
    # Obtenemos el modelo Talle del historial de la app
    Talle = apps.get_model('talles', 'Talle')
    
    # Tu lista de talles
    lista_nombres = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
    
    for nombre_talle in lista_nombres:
        # get_or_create evita que se dupliquen si corres la migración dos veces
        Talle.objects.get_or_create(nombre=nombre_talle)

class Migration(migrations.Migration):

    dependencies = [
        ('talles', '0001_initial'), # Esto apunta a la creación de la tabla
    ]

    operations = [
        migrations.RunPython(cargar_talles_iniciales),
    ]