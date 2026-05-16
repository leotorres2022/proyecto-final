from django.db import migrations

def cargar_socios(apps, schema_editor):
    Socio = apps.get_model('socios', 'Socio')
    lista_socios = [
        ('Juan Pérez', '1144556677', 'Av. Córdoba 1234, CABA', 'juan.perez@gmail.com'),
        ('María González', '1167891234', 'Calle Falsa 456, Rosario', 'maria.gonzalez@hotmail.com'),
        ('Carlos López', '1133445566', 'Av. San Martín 789, Mendoza', 'carlos.lopez@yahoo.com'),
        ('Ana Torres', '1122334455', 'Mitre 321, La Plata', 'ana.torres@gmail.com'),
        ('Lucía Fernández', '1198765432', 'Belgrano 987, Córdoba', 'lucia.fernandez@gmail.com'),
        ('Martín Ramírez', '1177889900', 'Av. Rivadavia 4321, CABA', 'martin.ramirez@gmail.com'),
        ('Sofía Castro', '1100112233', 'Urquiza 1111, Mar del Plata', 'sofia.castro@gmail.com'),
        ('Diego Sosa', '1188997766', 'Alsina 654, Bahía Blanca', 'diego.sosa@gmail.com'),
        ('Valentina Díaz', '1155667788', 'Av. Colon 2020, Salta', 'valentina.diaz@gmail.com'),
        ('Federico Ruiz', '1133221100', 'San Juan 3030, Tucumán', 'federico.ruiz@gmail.com')
    ]
    
    for nombre, telefono, direccion, email in lista_socios:
        Socio.objects.create(
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            email=email,
            estado=True  # Asumiendo que el campo se llama 'estado'
        )

class Migration(migrations.Migration):
    dependencies = [
        ('socios', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(cargar_socios),
    ]