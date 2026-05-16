from django.db import migrations

def cargar_categorias_iniciales(apps, schema_editor):
  
    Categoria = apps.get_model('categorias', 'Categoria')
   
    lista_nombres = [
        'Short de Futbol',
        'Medias Largas',
        'Camisetas',
        'Gorra',
        'Pantalon Largo',
        'Buso',
        'Bandera'
    ]
    
    for nombre_cat in lista_nombres:
        # get_or_create evita duplicados si se corre de nuevo
        Categoria.objects.get_or_create(nombre=nombre_cat)

class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(cargar_categorias_iniciales),
    ]