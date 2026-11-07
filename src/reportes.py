
# Proyecto Final: tiendapy
#modulo de alertas y cierre de caja diario


def mostrar_alertas(inventario):
    """Muestra productos con stock bajo o agotado agrupados por proveedor (CF-11)."""
    print("\n--- ALERTAS DE REABASTECIMIENTO ---")
    
    #diccionario para proveedor: { "Proveedor": ["Producto1", "Producto2"] }
    alertas_por_proveedor = {}
    
    for codigo, producto in inventario.items():
        if producto['stock'] <= producto['stock_minimo']:
            proveedor = producto['proveedor']
            
            # Si el proveedor no está en el diccionario, lo creamos con una lista vacía
            if proveedor not in alertas_por_proveedor:
                alertas_por_proveedor[proveedor] = []
                
            #texto de la alerta
            estado = "AGOTADO" if producto['stock'] == 0 else f"Bajo stock ({producto['stock']})"
            texto = f"[{codigo}] {producto['nombre']} - {estado} (Mínimo: {producto['stock_minimo']})"
            
            alertas_por_proveedor[proveedor].append(texto)
            
    # si no hubo alertas
    if len(alertas_por_proveedor) == 0:
        print("Todo en orden. No hay productos con bajo stock.")
        return

    # Imprimimos las alertas 
    for proveedor, lista_alertas in alertas_por_proveedor.items():
        print(f"\nProveedor: {proveedor}")
        for alerta in lista_alertas:
            print(f"  - {alerta}")

def cierre_de_caja(inventario):
    """Calcula las estadísticas del día leyendo el archivo de ventas (CF-12)."""
    print("\n--- CIERRE DE CAJA DEL DÍA ---")
    
    total_vendido = 0.0
    num_ventas = 0
    conteo_productos = {} # { "LAC001": 10, "BEB003": 5 }
    
    try:
        with open("data/ventas.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea != "":
                    partes = linea.split("|")
                    # Formato: fecha|total|carrito_string
                    if len(partes) >= 3:
                        # Sumar total y contar ventas
                        total_vendido += float(partes[1])
                        num_ventas += 1
                        
                        # procesar el carrito para ver los más vendidos
                        string_carrito = partes[2]
                        items = string_carrito.split(";")
                        
                        for item in items:
                            if item != "":
                                datos_item = item.split(":")
                                codigo = datos_item[0]
                                cantidad = int(datos_item[1])
                                
                                if codigo in conteo_productos:
                                    conteo_productos[codigo] += cantidad
                                else:
                                    conteo_productos[codigo] = cantidad
                                    
    except FileNotFoundError:
        print("No hay registro de ventas hoy (data/ventas.txt no existe).")
        return
        
    if num_ventas == 0:
        print("No se registraron ventas el día de hoy.")
        return

    #calcular ticket promedio
    ticket_promedio = total_vendido / num_ventas
    
    #encontrar el producto más vendido
    producto_mas_vendido = "Ninguno"
    max_cantidad = 0
    for codigo, cantidad in conteo_productos.items():
        if cantidad > max_cantidad:
            max_cantidad = cantidad
            # Buscamos el nombre en el inventario para que se vea bonito
            nombre = inventario.get(codigo, {}).get('nombre', codigo)
            producto_mas_vendido = f"{nombre} ({cantidad} unidades)"
            
    #productos sin ventas
    productos_sin_ventas = []
    for codigo, datos in inventario.items():
        if codigo not in conteo_productos:
            productos_sin_ventas.append(datos['nombre'])

    #IMPRIMIR EL REPORTE
    print(f"Total vendido:      ${total_vendido:.2f}")
    print(f"Número de ventas:   {num_ventas}")
    print(f"Ticket promedio:    ${ticket_promedio:.2f}")
    print(f"Producto más vendido: {producto_mas_vendido}")
    print("Productos sin ventas hoy:")
    if len(productos_sin_ventas) == 0:
        print("  (Todos los productos tuvieron al menos una venta)")
    else:
        for nombre in productos_sin_ventas:
            print(f"  - {nombre}")
    print("--------")