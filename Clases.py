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
        
        #Extrae metadatos y realiza el análisis de intensidad de la imagen.
        metadatos_extraidos = {}
       
        for nombre_columna, tag_id in self.TAGS_SOLICITADOS.items():
            # Generar la key del tag a partir del identificador (ej: 'PatientID')
            tag_keyword = pydicom.datadict.get_entry(*tag_id)[4]
            
            # Manejo casos donde el tag no esté presente (anonimizado) 
            valor = dataset.get(tag_keyword, None)
            
            # Formatear el valor si es un objeto DataElement complejo (como PatientName)
            if isinstance(valor, pydicom.valuerep.PersonName):
                valor = str(valor)
            
            metadatos_extraidos[nombre_columna] = valor


        # Cálculo de la intensidad promedio
        try:
           #llamamos al pixel array
            pixel_data = dataset.pixel_array
            
            # Cvalor de intensidad promedio de los píxeles 
            intensidad_promedio = np.mean(pixel_data)
        except AttributeError:
            # Manejo de error si el archivo no contiene datos de píxeles
            intensidad_promedio = "No-Imagen"
            print(f"  [Advertencia] Archivo sin 'pixel_array'. No se calculó la intensidad promedio.")

        #Añadimos este valor como una nueva columna [cite: 45]
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
