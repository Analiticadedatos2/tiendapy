
# Proyecto final tiendapy
# Diego Fernando Batero
# CC.1033686550
# noviembre 2026

import time  
import persistencia
import inventario
import ventas
import reportes

def menu_inventario(mi_inventario):
    """Sub-menú para la Gestión de Inventario (M1)."""
    while True:
        print("\n--- GESTIÓN DE INVENTARIO ---")
        print("1. Registrar producto")
        print("2. Consultar producto")
        print("3. Modificar producto")
        print("4. Eliminar producto")
        print("5. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            mi_inventario = inventario.registrar_producto(mi_inventario)
            persistencia.guardar_inventario(mi_inventario)
        elif opcion == "2":
            inventario.consultar_productos(mi_inventario)
        elif opcion == "3":
            inventario.modificar_producto(mi_inventario)
            persistencia.guardar_inventario(mi_inventario)
        elif opcion == "4":
            inventario.eliminar_producto(mi_inventario)
            persistencia.guardar_inventario(mi_inventario)
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def menu_ventas(mi_inventario):
    """Sub-menú para registrar ventas y actualizar stock."""
    
    #fecha actual del sistema 
    tiempo = time.localtime()
    dia = str(tiempo.tm_mday).zfill(2)    # zfill(2) asegura que el día 5 sea "05"
    mes = str(tiempo.tm_mon).zfill(2)     # Asegura que el mes 3 sea "03"
    anio = str(tiempo.tm_year)
    fecha_venta = anio + "-" + mes + "-" + dia

    #llamamos a la función de ventas
    resultado = ventas.registrar_venta(mi_inventario)
    
    # Si la venta se cancelo la función devuelve solo el inventrio
    if len(resultado) == 1:
        print("Volviendo al menú principal...")
        return mi_inventario
        
    #si la venta fue exitosa devuelve el inventarion el carrito y el total
    mi_inventario_actualizado, carrito, total = resultado
    
    #descontar el stock de los productos vendidos
    for item in carrito:
        mi_inventario_actualizado[item['codigo']]['stock'] -= item['cantidad']
        
    #guardar cambios en el archivo de inventario
    persistencia.guardar_inventario(mi_inventario_actualizado)
    
    #registrar la venta 
    persistencia.registrar_venta_en_archivo(fecha_venta, total, carrito)
    
    return mi_inventario_actualizado

def menu_reportes(mi_inventario):
    """Sub-menú para los reportes (M3)."""
    print("\n--- MENÚ DE REPORTES ---")
    print("1. Alertas de reabastecimiento")
    print("2. Cierre de caja diario")
    sub_opcion = input("Seleccione un reporte: ")
    
    if sub_opcion == "1":
        reportes.mostrar_alertas(mi_inventario)
    elif sub_opcion == "2":
        reportes.cierre_de_caja(mi_inventario)
    else:
        print("Opción no válida.")

def menu_principal():
    """Menú principal del sistema (CF-02)."""
    #Cargamos el inventario al iniciar
    mi_inventario = persistencia.cargar_inventario()
    
    while True:
        print("\n=== TIENDAPY - MENÚ PRINCIPAL ===")
        print("1. Gestión de Inventario (M1)")
        print("2. Registrar Venta (M2)")
        print("3. Reportes y Alertas")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            menu_inventario(mi_inventario)
        elif opcion == "2":
            mi_inventario = menu_ventas(mi_inventario)
        elif opcion == "3":
            menu_reportes(mi_inventario)
        elif opcion == "4":
            print("Saliendo del sistema... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

#INICIO
if __name__ == "__main__":
    print("Iniciando TiendaPy...")
    menu_principal()