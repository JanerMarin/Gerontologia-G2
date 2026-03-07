# Generated migration for Medico group creation

from django.db import migrations
from django.contrib.auth.models import Group


def crear_grupo_medico(apps, schema_editor):
    """Crear el grupo Medico si no existe"""
    Group.objects.get_or_create(name='Medico')


def eliminar_grupo_medico(apps, schema_editor):
    """Eliminar el grupo Medico"""
    try:
        grupo = Group.objects.get(name='Medico')
        grupo.delete()
    except Group.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_consultamedica_enunciadomedico'),
    ]

    operations = [
        migrations.RunPython(crear_grupo_medico, eliminar_grupo_medico),
    ]
