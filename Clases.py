import os
import glob
import pydicom
import pandas as pd
import numpy as np
from typing import List, Dict, Any

class ProcesadorDICOM:
    #Clase para automatizar la lectura, extracción y análisis de metadatos de archivos DICOM utilizando pydicom, pandas y numpy.
    
    # nombres de los tags investigaos
    TAGS_SOLICITADOS = {
        "Identificador_Paciente": ('0010', '0020'), # PatientID
        "Nombre_Paciente": ('0010', '0010'),        # PatientName
        "Identificador_Estudio": ('0020', '000D'),   # StudyInstanceUID
        "Descripcion_Estudio": ('0008', '1030'),    # StudyDescription
        "Fecha_Estudio": ('0008', '0020'),          # StudyDate
        "Modalidad_Imagen": ('0008', '0060'),       # Modality
        "Numero_Filas": ('0028', '0010'),           # Rows
        "Numero_Columnas": ('0028', '0011')         # Columns
    }

    def __init__(self):
        """Inicializa la lista para almacenar los metadatos."""
        self.lista_metadatos: List[Dict[str, Any]] = []
        self.dataframe_resultados: pd.DataFrame = pd.DataFrame()

    def escanear_y_cargar_dicom(self, directorio_ruta: str):
        #escanea un directorio, identifica y carga archivos DICOM.
        print(f"Buscando archivos DICOM en: {directorio_ruta}")
        # Usa glob para encontrar todos los archivos, independientemente de la extensión
        archivos_posibles = glob.glob(os.path.join(directorio_ruta, '*'))
        
        for archivo_ruta in archivos_posibles:
            try:
                # Leemos a ver si es un dicom, si no, se lanza exepción
                dataset = pydicom.dcmread(archivo_ruta)
                self.procesar_archivo(dataset)
            except pydicom.errors.InvalidDicomError:
                print(f"  [Error] Se omitió '{os.path.basename(archivo_ruta)}': No es un archivo DICOM válido.")
            except Exception as e:
                print(f"  [Error] Ocurrió un error inesperado al procesar '{os.path.basename(archivo_ruta)}': {e}")
                
        # Estructurar los datos después de procesar todos los archivos
        self._estructurar_datos()

    def procesar_archivo(self, dataset: pydicom.Dataset):
        #metadatos y cositas
        metadatos_extraidos = {}

        #Extracción de metadatos
        for nombre_columna, tag_keyword in self.TAGS_SOLICITADOS.items():

            valor = dataset.get(tag_keyword, None)
            
            if isinstance(valor, pydicom.valuerep.PersonName):
                valor = str(valor)
            elif valor is not None and isinstance(valor, pydicom.uid.UID):
                 valor = str(valor)
            
            metadatos_extraidos[nombre_columna] = valor

        # 4.4 Análisis de imagen
        intensidad_promedio = None
        try:
            pixel_data = dataset.pixel_array
            intensidad_promedio = np.mean(pixel_data)
        except AttributeError:
            intensidad_promedio = "N/A" 
        except Exception:
            intensidad_promedio = "Error" 

        metadatos_extraidos["Intensidad_Promedio"] = intensidad_promedio
        
        self.lista_metadatos.append(metadatos_extraidos)

    def _estructurar_datos(self):
       
        #Estructura los metadatos extraídos en un Dataframe de Pandas.
       
        if self.lista_metadatos:
            self.dataframe_resultados = pd.DataFrame(self.lista_metadatos)
            # Asegurar el orden de las columnas solicitadas
            columnas_ordenadas = list(self.TAGS_SOLICITADOS.keys()) + ["Intensidad_Promedio"]
            self.dataframe_resultados = self.dataframe_resultados[columnas_ordenadas]
            print("\n Datos estructurados exitosamente en un Dataframe de Pandas. :D ")
        else:
            print("\n No se encontraron metadatos para estructurar. :< ")

    def obtener_dataframe(self) -> pd.DataFrame:
       #mandar el pandas creao
        return self.dataframe_resultados

    def guardar_dataframe_a_csv(self, nombre_archivo: str) -> bool:
        #mejor exportar un archivo csv
        if self.dataframe_resultados.empty:
            return False
        
        try:
            # Exporta el Dataframe a un archivo CSV. index=False evita guardar los índices de Pandas.
            self.dataframe_resultados.to_csv(nombre_archivo, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"  [Error de Guardado] No se pudo guardar el archivo {nombre_archivo}: {e}")
            return False