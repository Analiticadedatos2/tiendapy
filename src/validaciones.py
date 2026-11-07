
# Proyecto Final: TiendaPy
# para validar entradas del usuario y evitar fallos

def pedir_texto(mensaje):
    """Pide un texto por consola y asegura que no esté vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor != "":
            return valor
        else:
            print("Error: El campo no puede estar vacío. Intente de nuevo.")

def pedir_entero(mensaje):
    """Pide un número entero por consola y asegura que sea mayor a cero."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            else:
                print("Error: El valor debe ser mayor a cero (no se permiten negativos o cero).")
        except ValueError:
            # se captura el error si el usuario escribe letras en vez de números (CR-01)
            print("Error: Debe ingresar un número entero válido.")

def pedir_decimal(mensaje):
    """Pide un número decimal (float) por consola y asegura que sea mayor a cero."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor > 0:
                return valor
            else:
                print("Error: El valor debe ser mayor a cero.")
        except ValueError:
            print("Error: Debe ingresar un número válido (puede usar punto decimal).")