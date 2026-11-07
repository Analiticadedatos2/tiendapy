# Proyecto Final: tiendapy
# Archivo: ventas.py
# Lógica registro ventas, carrito y descuentos


import validaciones

def registrar_venta(inventario):
    """Procesa una venta completa (M2)."""
    print("\n--- NUEVA VENTA ---")
    
    # Si el inventario está vacío, no se puede vender
    if len(inventario) == 0:
        print("El inventario está vacío. Registre productos primero.")
        return inventario

    carrito = [] # aqui se guarda diccionario para producto y la cantidad
    subtotal = 0.0
    
    while True:
        codigo = validaciones.pedir_texto("Ingrese el código del producto (o 'FIN' para terminar): ").upper()
        
        if codigo == "FIN":
            break
            
        if codigo not in inventario:
            print(f"El producto con código {codigo} no existe.")
            continue # Vuelve a pedir el código
            
        producto = inventario[codigo]
        print(f"Producto: {producto['nombre']} | Precio: ${producto['precio']} | Stock disponible: {producto['stock']}")
        
        # Validamos que haya stock
        if producto['stock'] <= 0:
            print("Error: Este producto está agotado.")
            continue
            
        cantidad = validaciones.pedir_entero("Ingrese la cantidad a llevar: ")
        
        # Regla de negocio: No vender más de lo que hay en stock
        if cantidad > producto['stock']:
            print(f"Error: Solo hay {producto['stock']} unidades disponibles.")
            continue
            
        # verificamos si el producto ya esta en el carrito para sumar la cantidad
        ya_en_carrito = False
        for item in carrito:
            if item['codigo'] == codigo:
                # Validamos que la suma total no supere el stock
                if item['cantidad'] + cantidad > producto['stock']:
                    print(f"Error: Si suma esta cantidad, supera el stock ({producto['stock']}).")
                    ya_en_carrito = True # Para que no lo agregue de nuevo
                    break
                item['cantidad'] += cantidad
                item['subtotal_item'] = item['cantidad'] * producto['precio']
                ya_en_carrito = True
                print("Cantidad actualizada en el carrito.")
                break
                
        if not ya_en_carrito:
            # lo agregamos al carrito por primera vez
            subtotal_item = cantidad * producto['precio']
            carrito.append({
                'codigo': codigo,
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'cantidad': cantidad,
                'subtotal_item': subtotal_item
            })
            print(f"Agregado: {cantidad} x {producto['nombre']}")
            
    # si el carrito quedo vacio (el usuario puso FIN de una vez)
    if len(carrito) == 0:
        print("No se agregaron productos. Venta cancelada.")
        return inventario

    #CÁLCULO DE TOTALES
    subtotal = 0.0
    for item in carrito:
        subtotal += item['subtotal_item']
        
    # Aplicar descuentos 
    descuento = 0.0
    porcentaje = 0
    if subtotal >= 100000:
        porcentaje = 10
        descuento = subtotal * 0.10
    elif subtotal >= 50000:
        porcentaje = 5
        descuento = subtotal * 0.05
        
    total_a_pagar = subtotal - descuento
    
    # el TICKET 
    print("\n=================================")
    print("         RESUMEN DE VENTA        ")
    print("=================================")
    for item in carrito:
        print(f"{item['cantidad']}x {item['nombre']:<15} ${item['subtotal_item']:.2f}")
    print("---------------------------------")
    print(f"Subtotal:       ${subtotal:.2f}")
    if porcentaje > 0:
        print(f"Descuento ({porcentaje}%): -${descuento:.2f}")
    print(f"TOTAL A PAGAR:  ${total_a_pagar:.2f}")
    print("=================================")

    #PAGO 
    while True:
        pago = validaciones.pedir_decimal("Ingrese el monto con el que paga el cliente: $")
        
        if pago < total_a_pagar:
            print(f"Error: El pago es insuficiente. Faltan ${total_a_pagar - pago:.2f}")
            print("Intente de nuevo.")
        else:
            cambio = pago - total_a_pagar
            print(f"\nPago recibido: ${pago:.2f}")
            print(f"CAMBIO:        ${cambio:.2f}")
            print("¡Venta exitosa!")
            break

    return inventario, carrito, total_a_pagar