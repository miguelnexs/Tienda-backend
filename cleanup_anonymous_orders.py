#!/usr/bin/env python
"""
Script para limpiar pedidos con cliente anónimo
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from pedidos.models import Pedido
from ventas.models import Cliente

def cleanup_anonymous_orders():
    """
    Elimina pedidos que tienen cliente anónimo o cliente None
    """
    print("🧹 Limpiando pedidos con cliente anónimo...")
    
    # Buscar pedidos sin cliente o con cliente anónimo
    pedidos_sin_cliente = Pedido.objects.filter(cliente__isnull=True)
    pedidos_anonimos = Pedido.objects.filter(cliente__nombre__icontains='anónimo')
    
    total_a_eliminar = pedidos_sin_cliente.count() + pedidos_anonimos.count()
    
    if total_a_eliminar == 0:
        print("✅ No hay pedidos con cliente anónimo para eliminar")
        return
    
    print(f"📊 Encontrados {total_a_eliminar} pedidos para eliminar:")
    print(f"   - Pedidos sin cliente: {pedidos_sin_cliente.count()}")
    print(f"   - Pedidos con cliente anónimo: {pedidos_anonimos.count()}")
    
    # Mostrar detalles de los pedidos a eliminar
    print("\n📋 Detalles de pedidos a eliminar:")
    
    for pedido in pedidos_sin_cliente:
        print(f"   - Pedido #{pedido.numero_pedido} (ID: {pedido.id}) - Sin cliente")
    
    for pedido in pedidos_anonimos:
        print(f"   - Pedido #{pedido.numero_pedido} (ID: {pedido.id}) - Cliente: {pedido.cliente.nombre}")
    
    # Confirmar eliminación
    confirmacion = input("\n¿Desea eliminar estos pedidos? (s/N): ").lower().strip()
    
    if confirmacion == 's':
        # Eliminar pedidos sin cliente
        pedidos_sin_cliente.delete()
        print(f"✅ Eliminados {pedidos_sin_cliente.count()} pedidos sin cliente")
        
        # Eliminar pedidos con cliente anónimo
        pedidos_anonimos.delete()
        print(f"✅ Eliminados {pedidos_anonimos.count()} pedidos con cliente anónimo")
        
        print("🎉 Limpieza completada exitosamente")
    else:
        print("❌ Operación cancelada")

def list_anonymous_orders():
    """
    Lista pedidos con cliente anónimo sin eliminarlos
    """
    print("📋 Listando pedidos con cliente anónimo...")
    
    pedidos_sin_cliente = Pedido.objects.filter(cliente__isnull=True)
    pedidos_anonimos = Pedido.objects.filter(cliente__nombre__icontains='anónimo')
    
    total = pedidos_sin_cliente.count() + pedidos_anonimos.count()
    
    if total == 0:
        print("✅ No hay pedidos con cliente anónimo")
        return
    
    print(f"📊 Encontrados {total} pedidos con cliente anónimo:")
    
    for pedido in pedidos_sin_cliente:
        print(f"   - Pedido #{pedido.numero_pedido} (ID: {pedido.id}) - Sin cliente")
    
    for pedido in pedidos_anonimos:
        print(f"   - Pedido #{pedido.numero_pedido} (ID: {pedido.id}) - Cliente: {pedido.cliente.nombre}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        list_anonymous_orders()
    else:
        cleanup_anonymous_orders() 