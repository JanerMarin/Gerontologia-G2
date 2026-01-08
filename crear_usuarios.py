import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Crear o obtener el grupo Enfermeria
enfermeria_group, created = Group.objects.get_or_create(name='Enfermeria')
print(f'Grupo Enfermeria: {"creado" if created else "ya existe"}')

# Crear usuario administrador
try:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@gerontologia.com',
        password='Admin123',
        first_name='Administrador',
        last_name='Sistema'
    )
    print('✓ Usuario ADMIN creado exitosamente')
except Exception as e:
    print(f'Usuario admin ya existe o error: {e}')

# Crear usuario enfermero
try:
    enfermero_user = User.objects.create_user(
        username='enfermero1',
        email='enfermero1@gerontologia.com',
        password='Enfermero123',
        first_name='Juan',
        last_name='Pérez'
    )
    enfermero_user.groups.add(enfermeria_group)
    enfermero_user.is_active = True
    enfermero_user.save()
    print('✓ Usuario ENFERMERO creado exitosamente')
except Exception as e:
    print(f'Usuario enfermero1 ya existe o error: {e}')

print('\n' + '='*50)
print('USUARIOS CREADOS:')
print('='*50)
print('\n1. ADMINISTRADOR:')
print('   Usuario: admin')
print('   Contraseña: Admin123')
print('   Rol: Superusuario (Acceso completo)')
print('\n2. ENFERMERO:')
print('   Usuario: enfermero1')
print('   Contraseña: Enfermero123')
print('   Rol: Enfermería')
print('='*50)
