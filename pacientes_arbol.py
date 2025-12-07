import os


# =============================================================================
# EXAMEN FINAL - Gestión de pacientes con ABB
# =============================================================================

class NodoPaciente:
    def __init__(self, dni, nombre, prioridad):
        self.dni = dni  # int
        self.nombre = nombre  # str
        self.prioridad = prioridad  # int (1 = baja, 2 = media, 3 = alta)
        self.izq = None
        self.der = None


def insertar_paciente(raiz, paciente):
    """Inserta un paciente en el ABB ordenado por dni."""
    if raiz is None:
        return paciente

    if paciente.dni < raiz.dni:
        raiz.izq = insertar_paciente(raiz.izq, paciente)
    elif paciente.dni > raiz.dni:
        raiz.der = insertar_paciente(raiz.der, paciente)
    # Si el dni es igual, no insertamos duplicado.
    return raiz


def cargar_pacientes_desde_archivo(ruta_archivo):
    """Lee el archivo pacientes.txt y construye el ABB de pacientes."""
    raiz = None
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea: continue

                partes = linea.split(";")
                if len(partes) != 3: continue

                dni_str, nombre, prioridad_str = partes
                try:
                    dni = int(dni_str)
                    prioridad = int(prioridad_str)
                except ValueError:
                    continue

                nuevo = NodoPaciente(dni, nombre, prioridad)
                raiz = insertar_paciente(raiz, nuevo)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_archivo}")
    return raiz


# =======================
# FUNCIONES DE LÓGICA
# =======================

def buscar_paciente(raiz, dni_busqueda):
    """Busca un paciente por DNI de forma recursiva."""
    if raiz is None or raiz.dni == dni_busqueda:
        return raiz
    if dni_busqueda < raiz.dni:
        return buscar_paciente(raiz.izq, dni_busqueda)
    return buscar_paciente(raiz.der, dni_busqueda)


def mostrar_pacientes_inorden(raiz):
    """Recorrido In-Orden para mostrar datos ordenados."""
    if raiz is not None:
        mostrar_pacientes_inorden(raiz.izq)
        print(f"DNI: {raiz.dni:<10} | Nombre: {raiz.nombre:<20} | Prioridad: {raiz.prioridad}")
        mostrar_pacientes_inorden(raiz.der)


def generar_reporte_prioridad_alta(raiz, ruta_salida, prioridad_minima):
    """Genera archivo con pacientes de alta prioridad."""

    def _escribir_recursivo(nodo, archivo, contador_ref):
        if nodo is not None:
            _escribir_recursivo(nodo.izq, archivo, contador_ref)
            if nodo.prioridad >= prioridad_minima:
                linea = f"{nodo.dni};{nodo.nombre};{nodo.prioridad}\n"
                archivo.write(linea)
                contador_ref[0] += 1
            _escribir_recursivo(nodo.der, archivo, contador_ref)

    try:
        contador = [0]
        with open(ruta_salida, "w", encoding="utf-8") as f:
            _escribir_recursivo(raiz, f, contador)

        with open(ruta_salida, "a", encoding="utf-8") as f:
            f.write(f"TOTAL_PACIENTES_REPORTE:{contador[0]}\n")
        print(f" Reporte generado en '{ruta_salida}'. Pacientes exportados: {contador[0]}")
    except Exception as e:
        print(f" Error al generar reporte: {e}")


def contar_pacientes_hoja(raiz):
    """Cuenta nodos hoja."""
    if raiz is None: return 0
    if raiz.izq is None and raiz.der is None: return 1
    return contar_pacientes_hoja(raiz.izq) + contar_pacientes_hoja(raiz.der)


# --- NUEVA FUNCIÓN AGREGADA ---
def registrar_nuevo_paciente(raiz, ruta_archivo):
    """
    Pide datos al usuario, actualiza el árbol Y escribe en el archivo txt.
    """
    print("\n--- Registrar Nuevo Paciente ---")
    try:
        dni = int(input("Ingrese DNI: "))

        # 1. Validar que no exista ya en el árbol
        if buscar_paciente(raiz, dni) is not None:
            print(f" Error: El paciente con DNI {dni} ya existe.")
            return raiz

        nombre = input("Ingrese Nombre: ").strip()
        prioridad = int(input("Ingrese Prioridad (1-3): "))

        # 2. Guardar en el archivo FÍSICO (Append)
        # Usamos 'a' para agregar al final sin borrar lo anterior
        with open(ruta_archivo, "a", encoding="utf-8") as f:
            # Aseguramos formato correcto: dni;nombre;prioridad
            # Si el archivo no termina en nueva linea, poner \n al inicio es buena practica,
            # pero asumiremos formato limpio.
            f.write(f"\n{dni};{nombre};{prioridad}")

            # 3. Actualizar el ÁRBOL (Memoria)
        nuevo_nodo = NodoPaciente(dni, nombre, prioridad)
        raiz = insertar_paciente(raiz, nuevo_nodo)

        print(" Paciente registrado y guardado en archivo exitosamente.")

    except ValueError:
        print(" Error: DNI y Prioridad deben ser números enteros.")
    except Exception as e:
        print(f" Error escribiendo en archivo: {e}")

    return raiz


# =======================
# MENÚ Y PROGRAMA PRINCIPAL
# =======================

def mostrar_menu():
    print("\n=== Menú - Gestión de pacientes ===")
    print("1. Buscar paciente por DNI")
    print("2. Listar pacientes ordenados por DNI (inorden)")
    print("3. Generar reporte de prioridad alta en archivo")
    print("4. Mostrar cantidad de pacientes hoja en el árbol")
    print("5. Agregar nuevo paciente (Guardar en TXT)")  # <--- NUEVA OPCIÓN
    print("0. Salir")


def main():
    # --- CREACIÓN AUTOMÁTICA DE DATOS DE PRUEBA ---
    ruta_pacientes = "pacientes.txt"
    if not os.path.exists(ruta_pacientes):
        with open(ruta_pacientes, "w", encoding="utf-8") as f:
            f.write("400;Carlos Ruiz;2\n")
            f.write("100;Ana Lopez;3\n")
            f.write("600;Juan Perez;1\n")
            f.write("200;Maria Garcia;3\n")
            f.write("50;Luis Gomez;1\n")
            f.write("500;Elena Diaz;2")  # Sin salto de linea al final para probar append
        print(" Archivo 'pacientes.txt' creado automáticamente para pruebas.")
    # -----------------------------------------------

    raiz = cargar_pacientes_desde_archivo(ruta_pacientes)

    if raiz is None:
        print("El árbol está vacío o no se pudo cargar.")
    else:
        print(f" Árbol de pacientes cargado desde '{ruta_pacientes}'")

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            try:
                dni_input = int(input("Ingrese el DNI a buscar: "))
                nodo = buscar_paciente(raiz, dni_input)
                if nodo:
                    print(f"\n PACIENTE ENCONTRADO:")
                    print(f"   - DNI: {nodo.dni}")
                    print(f"   - Nombre: {nodo.nombre}")
                    print(f"   - Prioridad: {nodo.prioridad}")
                else:
                    print(f"\n No se encontró ningún paciente con DNI {dni_input}.")
            except ValueError:
                print(" Error: El DNI debe ser un número entero.")

        elif opcion == "2":
            print("\n--- Listado de Pacientes (Ordenados por DNI) ---")
            mostrar_pacientes_inorden(raiz)

        elif opcion == "3":
            try:
                p_min = int(input("Ingrese la prioridad mínima (1, 2 o 3): "))
                nombre_rep = "reporte_prioridad.txt"
                generar_reporte_prioridad_alta(raiz, nombre_rep, p_min)
            except ValueError:
                print(" Error: La prioridad debe ser un número.")

        elif opcion == "4":
            cantidad = contar_pacientes_hoja(raiz)
            print(f"\n Cantidad de pacientes hoja (sin hijos) en el árbol: {cantidad}")

        # --- NUEVA LÓGICA ---
        elif opcion == "5":
            # Llamamos a la nueva función y actualizamos la raiz
            raiz = registrar_nuevo_paciente(raiz, ruta_pacientes)

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()