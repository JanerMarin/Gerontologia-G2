"""
Script para validar y corregir pacientes con nombres duplicados
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from myapp.models import Identificacion
from collections import defaultdict

print("=" * 80)
print("VALIDACIÓN DE PACIENTES - VERIFICACIÓN DE NOMBRES DUPLICADOS")
print("=" * 80)

# Obtener todos los pacientes
pacientes = Identificacion.objects.all().order_by('id')

print(f"\n📊 Total de pacientes: {pacientes.count()}")
print("\n" + "=" * 80)
print("LISTADO COMPLETO DE PACIENTES")
print("=" * 80)

# Diccionario para detectar duplicados
nombres_completos = defaultdict(list)

for paciente in pacientes:
    nombre_completo = f"{paciente.primer_nombre} {paciente.segundo_nombre} {paciente.primer_apellido} {paciente.segundo_apellido}".strip()
    print(f"\nID: {paciente.id}")
    print(f"   Nombre: {nombre_completo}")
    print(f"   Documento: {paciente.tipo_documento} {paciente.numero_documento_paciente}")
    print(f"   Edad: {paciente.edad} años")
    print(f"   Ciudad: {paciente.ciudad_residencia}")
    
    # Guardar para detectar duplicados
    nombres_completos[nombre_completo].append(paciente)

# Detectar duplicados
print("\n" + "=" * 80)
print("ANÁLISIS DE NOMBRES DUPLICADOS")
print("=" * 80)

duplicados_encontrados = False
for nombre, lista_pacientes in nombres_completos.items():
    if len(lista_pacientes) > 1:
        duplicados_encontrados = True
        print(f"\n⚠️  DUPLICADO ENCONTRADO: {nombre}")
        print(f"   Cantidad de pacientes con este nombre: {len(lista_pacientes)}")
        for p in lista_pacientes:
            print(f"   - ID: {p.id}, Documento: {p.numero_documento_paciente}")

if not duplicados_encontrados:
    print("\n✅ No se encontraron nombres duplicados.")
else:
    print("\n" + "=" * 80)
    print("CORRECCIÓN DE DUPLICADOS")
    print("=" * 80)
    
    # Proponer correcciones automáticas
    contador = 1
    for nombre, lista_pacientes in nombres_completos.items():
        if len(lista_pacientes) > 1:
            print(f"\n🔧 Corrigiendo: {nombre}")
            for idx, paciente in enumerate(lista_pacientes):
                if idx > 0:  # Dejar el primero sin cambios
                    nuevo_nombre = f"{paciente.primer_nombre}"
                    nuevo_segundo_nombre = f"Variante{idx}"
                    
                    print(f"   - ID {paciente.id}: Cambiando segundo nombre a '{nuevo_segundo_nombre}'")
                    
                    paciente.segundo_nombre = nuevo_segundo_nombre
                    paciente.save()
                    
                    print(f"     ✓ Actualizado: {paciente.primer_nombre} {paciente.segundo_nombre} {paciente.primer_apellido}")

    print("\n✅ Corrección completada.")
    
    # Verificar nuevamente
    print("\n" + "=" * 80)
    print("VERIFICACIÓN POSTERIOR A LA CORRECCIÓN")
    print("=" * 80)
    
    pacientes_actualizados = Identificacion.objects.all().order_by('id')
    nombres_verificacion = defaultdict(list)
    
    for paciente in pacientes_actualizados:
        nombre_completo = f"{paciente.primer_nombre} {paciente.segundo_nombre} {paciente.primer_apellido} {paciente.segundo_apellido}".strip()
        nombres_verificacion[nombre_completo].append(paciente)
    
    duplicados_restantes = sum(1 for lista in nombres_verificacion.values() if len(lista) > 1)
    
    if duplicados_restantes == 0:
        print("\n✅ Todos los nombres duplicados han sido corregidos exitosamente.")
    else:
        print(f"\n⚠️  Aún quedan {duplicados_restantes} nombres duplicados.")

print("\n" + "=" * 80)
print("LISTADO FINAL DE PACIENTES")
print("=" * 80)

pacientes_final = Identificacion.objects.all().order_by('id')
for paciente in pacientes_final:
    nombre_completo = f"{paciente.primer_nombre} {paciente.segundo_nombre} {paciente.primer_apellido} {paciente.segundo_apellido}".strip()
    print(f"ID {paciente.id:2d}: {nombre_completo:40s} - Doc: {paciente.numero_documento_paciente}")

print("\n" + "=" * 80)
