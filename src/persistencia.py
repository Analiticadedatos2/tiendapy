
# Proyecto Final: TiendaPy
# Manejo de archivos plano para guardar y cargr datos

def cargar_inventario():
    """Carga los productos desde data/inventario.txt a un diccionario."""
    inventario = {}
    try:
        # Usamos 'with' para garantizar que el archivo se cierre (CR-05)
        with open("data/inventario.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea != "":
                    partes = linea.split("|")
                    # Validamos que la línea tenga los 7 campos (CR-04)
                    if len(partes) == 7:
                        codigo = partes[0]
                        try:
                            inventario[codigo] = {
                                "nombre": partes[1],
                                "categoria": partes[2],
                                "precio": float(partes[3]),
                                "stock": int(partes[4]),
                                "stock_minimo": int(partes[5]),
                                "proveedor": partes[6]
                            }
                        except ValueError:
                            print(f"Advertencia: Datos numéricos corruptos en la línea: {linea}")
                    else:
                        print(f"Advertencia: Línea incompleta omitida: {linea}")
    except FileNotFoundError:
        #si el archivo no existe, inicia con inventario vacio
        print("Aviso: No se encontró data/inventario.txt. Se creará uno nuevo al guardar.")
    return inventario

def guardar_inventario(inventario):
    """Guarda el diccionario del inventario en data/inventario.txt."""
    try:
        with open("data/inventario.txt", "w", encoding="utf-8") as archivo:
            for codigo, datos in inventario.items():
                # Formato: codigo|nombre|categoria|precio|stock|stock_minimo|proveedor
                linea = f"{codigo}|{datos['nombre']}|{datos['categoria']}|{datos['precio']}|{datos['stock']}|{datos['stock_minimo']}|{datos['proveedor']}\n"
                archivo.write(linea)
    except Exception as e:
        print(f"Error crítico al guardar el inventario: {e}")

def registrar_venta_en_archivo(fecha, total, carrito):
    """Agrega una venta al final de data/ventas.txt."""
    try:
        #usamos modo 'a' (append) para agregar al final sin borrar lo anterior
        with open("data/ventas.txt", "a", encoding="utf-8") as archivo:
            # Construimos el string del carrito: codigo:cantidad;codigo:cantidad
            texto_carrito = ""
            for item in carrito:
                texto_carrito += f"{item['codigo']}:{item['cantidad']};"
            
            #fecha|total|codigo:cantidad;codigo:cantidad;
            linea = f"{fecha}|{total}|{texto_carrito}\n"
            archivo.write(linea)
    except Exception as e:
        print(f"Error al registrar la venta: {e}")