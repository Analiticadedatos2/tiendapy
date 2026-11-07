
# Proyecto Final: TiendaPy
# Descripción: Lógica para gestonar el inventario (CRUD)

# Importamos nuestros propios archivos 
import validaciones

def registrar_producto(inventario):
    """Registra un producto nuevo validando que el código no exista (CF-03)."""
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    
    # pedimos el código
    codigo = validaciones.pedir_texto("Ingrese el código del producto (ej. LAC001): ").upper()
    
    # validamos que el codigo no se repita
    if codigo in inventario:
        print(f"Error: El producto con código {codigo} ya existe en el inventario.")
        return inventario
    
    nombre = validaciones.pedir_texto("Ingrese el nombre del producto: ")
    categoria = validaciones.pedir_texto("Ingrese la categoría (Lacteos, Bebidas, Aseo, Abarrotes, Snacks): ")
    precio = validaciones.pedir_decimal("Ingrese el precio unitario: $")
    stock = validaciones.pedir_entero("Ingrese la cantidad en stock: ")
    stock_minimo = validaciones.pedir_entero("Ingrese el stock mínimo para alertas: ")
    proveedor = validaciones.pedir_texto("Ingrese el nombre del proveedor: ")
    
    #guardamos en el diccionario 
    inventario[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "proveedor": proveedor
    }
    
    print(f"\n¡Éxito! El producto '{nombre}' ha sido registrado.")
    return inventario

def consultar_productos(inventario):
    """Permite buscar por código o por categoría (CF-04)."""
    print("\n--- CONSULTAR PRODUCTOS ---")
    print("1. Buscar por código")
    print("2. Buscar por categoría")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        codigo = input("Ingrese el código a buscar: ").upper()
        if codigo in inventario:
            p = inventario[codigo]
            print(f"\n[Código: {codigo}] {p['nombre']} - Categoría: {p['categoria']}")
            print(f"Precio: ${p['precio']} | Stock: {p['stock']} | Proveedor: {p['proveedor']}")
        else:
            print(f"El producto con código {codigo} no existe.")
            
    elif opcion == "2":
        categoria = input("Ingrese la categoría a buscar: ")
        encontrados = 0
        print(f"\nProductos en la categoría '{categoria}':")
        for codigo, p in inventario.items():
            if p['categoria'].lower() == categoria.lower():
                print(f"- [{codigo}] {p['nombre']} | Precio: ${p['precio']} | Stock: {p['stock']}")
                encontrados += 1
        
        if encontrados == 0:
            print("No se encontraron productos en esa categoría.")
    else:
        print("Opción no válida.")

def modificar_producto(inventario):
    """Permite modificar el precio y el stock de un producto existente (CF-05)."""
    print("\n--- MODIFICAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto a modificar: ").upper()
    
    if codigo in inventario:
        print(f"Producto actual: {inventario[codigo]['nombre']}")
        print("1. Modificar Precio")
        print("2. Modificar Stock")
        opcion = input("Seleccione qué desea modificar: ")
        
        if opcion == "1":
            nuevo_precio = validaciones.pedir_decimal("Ingrese el nuevo precio: $")
            inventario[codigo]['precio'] = nuevo_precio
            print("Precio actualizado correctamente.")
        elif opcion == "2":
            nuevo_stock = validaciones.pedir_entero("Ingrese el nuevo stock: ")
            inventario[codigo]['stock'] = nuevo_stock
            print("Stock actualizado correctamente.")
        else:
            print("Opción no válida.")
    else:
        print(f"El producto con código {codigo} no existe.")

def eliminar_producto(inventario):
    """Elimina un producto del inventario (CF-05)."""
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto a eliminar: ").upper()
    
    if codigo in inventario:
        nombre = inventario[codigo]['nombre']
        inventario.pop(codigo)
        print(f"El producto '{nombre}' ha sido eliminado del inventario.")
    else:
        print(f"El producto con código {codigo} no existe.")