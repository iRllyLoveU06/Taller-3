import os
import sys
from Clases import ProcesadorDICOM

def mostrar_menu(): #menú
    print("\n" + "="*50)
    print("      Sistema de Procesamiento DICOM")
    print("="*50)
    print("1. Cargar y Analizar Carpeta DICOM")
    print("2. Mostrar Metadatos Procesados (Dataframe)")
    print("3. Salir")
    print("-" * 50)

def main():
    procesador = ProcesadorDICOM()
    opcion = None

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == '1':
            # 1. Cargar carpeta con archivos DICOM
            ruta_carpeta = input("Ingrese la RUTA de la carpeta con archivos DICOM: ")
            
            if not os.path.isdir(ruta_carpeta):
                print(f"\n[Error] La ruta '{ruta_carpeta}' no es un directorio válido o no existe.")
                continue

            print("\n--- Iniciando Carga y Análisis ---")
            
            # Se llama al método que ejecuta la carga, extracción y estructuración
            carga_exitosa = procesador.escanear_y_cargar_dicom(ruta_carpeta)

            if carga_exitosa:
                num_registros = len(procesador.lista_metadatos)
                print(f"✅ Proceso completado. Se procesaron {num_registros} archivos DICOM.")
                print(f"   Metadatos disponibles para la ruta: {procesador.ruta_cargada}")
            else:
                 print("❌ Proceso de carga finalizado. No se pudieron extraer metadatos.")

        elif opcion == '2':
            # 2. Devolver y mostrar Dataframe con los datos
            df_final = procesador.obtener_dataframe()
            
            if df_final.empty:
                print("\n[Advertencia] No hay datos cargados. Por favor, use la opción 1 primero.")
            else:
                print("\n" + "="*70)
                print("           Dataframe de Metadatos DICOM (Primeras 5 Filas)")
                print("="*70)
                print(df_final.head().to_string())
                print(f"\nTotal de archivos procesados: {df_final.shape[0]}")
                print(f"Columnas: {list(df_final.columns)}")

        elif opcion == '3':
            # 3. Salir
            print("\nSaliendo del sistema. chau")
            sys.exit(0)

        else:
            print("\n[Error] Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()