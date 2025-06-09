#Algoritmo de busqueda y ordenamiento elaborado pata tp programación 1. Guirin - Iturralde.
import csv #Importa el módulo estándar csv que permite leer y escribir archivos en formato csv. 
import os # Se importa para verificar que los archivos .csv estén realmente en la carpeta.
import time # Importa el módulo time, que permite trabajar con el tiempo del sistema.

# Función para leer el archivo CSV
def cargar_datos(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"Error: El archivo {nombre_archivo} no existe.")
        return []
    with open(nombre_archivo, encoding="latin1") as f:
        lector = csv.DictReader(f, delimiter=';')
        datos = list(lector)
        for fila in datos:
            fila["Año"] = int(fila["Año"])
            fila["Lluvia (mm)"] = float(fila["Lluvia (mm)"].replace(",", "."))
        return datos

# Función para imprimir datos en formato legible
def imprimir_fila(fila):
    print(f"Año: {fila['Año']}, Localidad: {fila['Localidad']}, Lluvia (mm): {fila['Lluvia (mm)']:.2f}")

# Función para guardar resultados en CSV
def guardar_resultados(data, nombre_archivo):
    with open(nombre_archivo, "w", newline='', encoding="latin1") as f:
        campos = ["Año", "Localidad", "Lluvia (mm)"]
        escritor = csv.DictWriter(f, fieldnames=campos, delimiter=';')
        escritor.writeheader()
        for fila in data:
            escritor.writerow(fila)
    print(f"Resultados guardados en {nombre_archivo}.")

# Funciones de ordenamiento
def ordenar_por_lluvia(data):
    data = data.copy()
    for i in range(len(data)):
        max_idx = i
        for j in range(i+1, len(data)):
            if data[j]["Lluvia (mm)"] > data[max_idx]["Lluvia (mm)"]:
                max_idx = j
        data[i], data[max_idx] = data[max_idx], data[i]
    return data

def ordenar_por_año(data):
    data = data.copy()
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j]["Año"] > data[j+1]["Año"]:
                data[j], data[j+1] = data[j+1], data[j]
    return data

def ordenar_por_localidad(data):
    if len(data) <= 1:
        return data
    pivote = data[len(data)//2]["Localidad"]
    menores = [x for x in data if x["Localidad"] < pivote]
    iguales = [x for x in data if x["Localidad"] == pivote]
    mayores = [x for x in data if x["Localidad"] > pivote]
    return ordenar_por_localidad(menores) + iguales + ordenar_por_localidad(mayores)

# Funciones de búsquedas
def buscar_por_localidad(data, localidad):
    return [fila for fila in data if fila["Localidad"].lower() == localidad.lower()]

def buscar_por_año(data, año):
    return [fila for fila in data if fila["Año"] == año]

# Menú interactivo
def menu():
    print("\nSistema de Precipitaciones")
    print("1. Ordenar por lluvia (mm)")
    print("2. Ordenar por año")
    print("3. Ordenar por localidad")
    print("4. Buscar por localidad")
    print("5. Buscar por año")
    print("6. Cambiar archivo CSV")
    print("7. Salir")

#Programa principal
# Cargar dos archivos al inicio
print("Carga de datos:")
archivo1 = input("Ingrese el nombre del primer archivo CSV: ")
archivo2 = input("Ingrese el nombre del segundo archivo CSV: ")

datos1 = cargar_datos(archivo1)
datos2 = cargar_datos(archivo2)

datos_actuales = datos1 if datos1 else datos2

while True:
    print(f"\nActualmente trabajando con: {archivo1 if datos_actuales == datos1 else archivo2}")
    menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        inicio = time.time()
        ordenado = ordenar_por_lluvia(datos_actuales)
        fin = time.time()
        print(f"\nDatos ordenados por lluvia (mayor a menor) en {fin - inicio:.4f} segundos:")
        for fila in ordenado[:10]:
            imprimir_fila(fila)
        print("... Mostrando primeros 10 resultados.")

    elif opcion == "2":
        inicio = time.time()
        ordenado = ordenar_por_año(datos_actuales)
        fin = time.time()
        print(f"\nDatos ordenados por año en {fin - inicio:.4f} segundos:")
        for fila in ordenado[:10]:
            imprimir_fila(fila)

    elif opcion == "3":
        inicio = time.time()
        ordenado = ordenar_por_localidad(datos_actuales)
        fin = time.time()
        print(f"\nDatos ordenados por localidad en {fin - inicio:.4f} segundos:")
        for fila in ordenado[:10]:
            imprimir_fila(fila)

    elif opcion == "4":
        loc = input("Ingrese el nombre de la localidad: ")
        inicio = time.time()
        resultados = buscar_por_localidad(datos_actuales, loc)
        fin = time.time()
        print(f"\n{len(resultados)} resultados encontrados en {fin - inicio:.4f} segundos.")
        if resultados:
            for r in resultados[:10]:
                imprimir_fila(r)
            print("... Mostrando primeros 10 resultados.")
            if input("¿Desea guardar los resultados? (s/n): ").lower() == "s":
                guardar_resultados(resultados, "resultados_localidad.csv")
        else:
            print("No se encontraron registros para esa localidad.")

    elif opcion == "5":
        try:
            año = int(input("Ingrese el año: "))
            inicio = time.time()
            resultados = buscar_por_año(datos_actuales, año)
            fin = time.time()
            print(f"\n{len(resultados)} resultados encontrados en {fin - inicio:.4f} segundos.")
            if resultados:
                for r in resultados[:10]:
                    imprimir_fila(r)
                print("... Mostrando primeros 10 resultados.")
                if input("¿Desea guardar los resultados? (s/n): ").lower() == "s":
                    guardar_resultados(resultados, "resultados_año.csv")
            else:
                print("No hay datos para ese año.")
        except ValueError:
            print("Ingrese un año válido.")

    elif opcion == "6":
        print("1. Cambiar a primer archivo")
        print("2. Cambiar a segundo archivo")
        cambio = input("Seleccione una opción: ")
        if cambio == "1" and datos1:
            datos_actuales = datos1
        elif cambio == "2" and datos2:
            datos_actuales = datos2
        else:
            print("Archivo no disponible.")

    elif opcion == "7":
        print("¡Hasta luego!")
        break

    else:
        print("Opción inválida.")
