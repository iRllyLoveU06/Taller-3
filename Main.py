import os
import sys
from Clases import ProcesadorDICOM


carpetas_cargadas = {}  # {nombre_carpeta: ruta_real}


def mostrar_menu():
    print("\n" + "=" * 55)
    print("      Sistema de Procesamiento DICOM")
    print("=" * 55)
    print("1. Registrar carpeta con archivos DICOM")
    print("2. Extraer metadatos de carpeta registrada")
    print("3. Mostrar DataFrame actual")
    print("4. Guardar DataFrame a CSV")
    print("5. Salir")
    print("-" * 55)


def seleccionar_carpeta():
    """Permite escoger una carpeta previamente registrada."""
    if not carpetas_cargadas:
        print("\n[Advertencia] No hay carpetas cargadas aún.")
        return None

    print("\nCarpetas disponibles:")
    for i, nombre in enumerate(carpetas_cargadas.keys(), start=1):
        print(f"{i}. {nombre}")

    try:
        opcion = int(input("\nSeleccione el número de la carpeta: "))
        nombres = list(carpetas_cargadas.keys())
        return nombres[opcion - 1]
    except:
        print("[Error] Selección inválida.")
        return None


# -------------------------------------------
def main():
    procesador = ProcesadorDICOM()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ")

        # 1. Registrar carpeta
        if opcion == "1":
            ruta = input("\nIngrese la ruta de la carpeta DICOM: ").strip()

            if not os.path.isdir(ruta):
                print("[Error] La ruta no es válida.")
                continue

            nombre_mostrado = os.path.basename(ruta.rstrip("/\\"))
            if nombre_mostrado == "":
                nombre_mostrado = ruta  # carpeta raíz

            carpetas_cargadas[nombre_mostrado] = ruta
            print(f"✔ Carpeta '{nombre_mostrado}' registrada correctamente.")

        # 2. Extraer metadatos de carpeta seleccionada
        elif opcion == "2":
            carpeta_seleccionada = seleccionar_carpeta()

            if carpeta_seleccionada is None:
                continue

            ruta_real = carpetas_cargadas[carpeta_seleccionada]

            resp = input("¿Calcular intensidad promedio de la imagen? (s/n): ").lower()
            calcular_intensidad = True if resp == "s" else False

            print("\n--- Iniciando extracción de metadatos ---")
            exito = procesador.escanear_y_cargar_dicom(
                ruta_real, calcular_intensidad=calcular_intensidad
            )

            if exito:
                print(f"✔ Metadatos extraídos de la carpeta '{carpeta_seleccionada}'.")
                print(f"  Total de archivos procesados: {len(procesador.lista_metadatos)}")
            else:
                print("❌ No se encontraron archivos DICOM válidos.")

        
        # 3. Mostrar DataFrame
        elif opcion == "3":
            df = procesador.obtener_dataframe()

            if df.empty:
                print("\n[Advertencia] No hay datos procesados aún.")
            else:
                print("\n=== Vista previa del DataFrame ===")
                print(df.head())
                print(f"\nTotal de filas: {df.shape[0]}")


        # 4. Guardar CSV
        elif opcion == "4":
            df = procesador.obtener_dataframe()
            if df.empty:
                print("\n[Advertencia] No hay datos para guardar.")
                continue

            nombre_archivo = input("Nombre del archivo CSV (ejemplo: salida.csv): ").strip()

            if not nombre_archivo.lower().endswith(".csv"):
                nombre_archivo += ".csv"

            if procesador.guardar_dataframe_a_csv(nombre_archivo):
                print(f"✔ Archivo '{nombre_archivo}' guardado exitosamente.")
            else:
                print("❌ Error al guardar el archivo.")

        # 5. Salir
        elif opcion == "5":
            print("\nSaliendo del sistema. ¡Chao!")
            sys.exit(0)

        else:
            print("\n[Error] Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
