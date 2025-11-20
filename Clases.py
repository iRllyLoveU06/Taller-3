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
        self.ruta_cargada = None

    def escanear_y_cargar_dicom(self, directorio_ruta: str, calcular_intensidad=True):

        #escanea un directorio, identifica y carga archivos DICOM.

        print(f"Buscando archivos DICOM en: {directorio_ruta}")
        self.ruta_cargada = directorio_ruta

        # Usa glob para encontrar todos los archivos, independientemente de la extensión
        archivos_posibles = glob.glob(os.path.join(directorio_ruta, '*'))
        
        archivos_validos = 0
        
        for archivo_ruta in archivos_posibles:
            try:
                dataset = pydicom.dcmread(archivo_ruta)
                self.procesar_archivo(dataset, calcular_intensidad)
                archivos_validos += 1

            except pydicom.errors.InvalidDicomError:
                print(f"[Omitido] '{os.path.basename(archivo_ruta)}' no es un DICOM.")

            except Exception as e:
                print(f"[Error] Problema con '{os.path.basename(archivo_ruta)}': {e}")

        # Estructurar los datos después de procesar todos los archivos
        self._estructurar_datos()
        return archivos_validos > 0
    

    def procesar_archivo(self, dataset: pydicom.Dataset, calcular_intensidad=True):
        
        #extracion y analisis de imagen
        metadatos = {}

        # Extracción de metadatos
        for nombre_columna, tag_tuple in self.TAGS_SOLICITADOS.items():

            elemento = dataset.get(tag_tuple, None)
            valor = None

            if elemento is not None:
                try:
                    valor = elemento.value
                except AttributeError:
                    valor = elemento

                if hasattr(valor, "original_string"):
                    valor = str(valor)

                if valor in ("", None):
                    valor = None

            metadatos[nombre_columna] = valor
            

        #Analisis imagen
        intensidad_promedio = None
        if calcular_intensidad:
            try:
                pixel_data = dataset.pixel_array
                metadatos["Intensidad_Promedio"] = float(np.mean(pixel_data))
            except:
                metadatos["Intensidad_Promedio"] = None
        else:
            metadatos["Intensidad_Promedio"] = None

        self.lista_metadatos.append(metadatos)

    def _estructurar_datos(self):
            #Convierte la lista de diccionarios en un DataFrame.
            if not self.lista_metadatos:
                self.dataframe_resultados = pd.DataFrame()
            else:
                self.dataframe_resultados = pd.DataFrame(self.lista_metadatos)

    def obtener_dataframe(self) -> pd.DataFrame:
       #devolver los datos
        return self.dataframe_resultados

    def guardar_dataframe_a_csv(self, nombre_archivo: str) -> bool:
        if self.dataframe_resultados.empty:
            return False
        
        try:
            self.dataframe_resultados.to_csv(nombre_archivo, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"[Error] No se pudo guardar {nombre_archivo}: {e}")
            return False