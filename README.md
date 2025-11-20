Integrantes: Luis Ángel Caro Pérez

1. Breve descripción del proyecto
  Este trabajo tiene como objetivo el desarrollo de una aplicación desarrollada en Python, que pueda automatizar la lectura, la extracción y la organización de metadatos de archivos DICOM.
  Este sistema permite la identificación de archivos DICOM contenidos en un específico directorio, la extracción de información clínica relevante para cada archivo de imagen
  (como datos del paciente, del estudio y de la imagen), el cálculo de la intensidad media de la imagen si está disponible y en último lugar la estructuración de la información generada en un DataFrame,
  de manera que sea posible consultarla o exportarla.
  El objetivo es dar una imagen de parte del flujo funcional de un PACS y de qué forma esas imágenes médicas y sus metadatos pueden ser manipulados gracias a herramientas de software libre.


2. ¿Por qué DICOM y HL7 son cruciales para la interoperabilidad en salud y en qué se diferencian conceptualmente?
  Tanto DICOM como HL7 son estándares esenciales para garantizar la interoperabilidad entre sistemas en el ámbito de la salud, pero cada uno cumple funciones distintas.
  Por el lado de DICOM (Digital Imaging and Communications in Medicine) está diseñado específicamente para el manejo de imágenes médicas. 
  Establece cómo se deben almacenar, transmitir y describir las imágenes generadas por equipos como TAC, resonancia magnética, ultrasonido, medicina nuclear, entre otros. 
  También define una estructura estándar de metadatos que permite que sistemas PACS y modalidades distintas puedan comunicarse sin perder información.
  Por otro lado, HL7 (Health Level 7) está orientado a la comunicación de información clínica y administrativa. Es el estándar utilizado para transmitir admisiones, órdenes médicas, resultados de laboratorio,     
  datos demográficos, notas clínicas y otros elementos que describen la atención del paciente, pero no maneja imágenes.
  La diferencia conceptual principal es que DICOM opera sobre imágenes diagnósticas y sus metadatos, mientras que HL7 opera sobre información clínica textual y administrativa del paciente. Sin ambos, un sistema 
  hospitalario no podría integrar los datos clínicos con las imágenes de forma coherente.


3. Relevancia clínica o de preprocesamiento del análisis de intensidades en una imagen médica
   La distribución de intensidades en una imagen médica puede aportar información clave tanto para interpretación clínica como para etapas de preprocesamiento. Clínicamente, las intensidades reflejan propiedades
   físicas de los tejidos: zonas hipodensas o hiperdensas en tomografía, áreas hiperintensas o hipointensas en resonancia, y variaciones importantes en ultrasonido o medicina nuclear. Analizar estas intensidades
   puede ayudar a identificar patrones anormales como edema, hemorragia, necrosis, inflamación o lesiones.
   En términos de preprocesamiento, estudiar la distribución de intensidades permite realizar normalización, corrección de contraste, eliminación de ruido o ajustar rangos dinámicos antes de aplicar técnicas más
   complejas como segmentación, registro, análisis volumétrico o algoritmos de machine learning. Es un primer paso esencial para garantizar que las imágenes se encuentren en condiciones óptimas para su análisis
   posterior.


5. Dificultades encontradas y la importancia de las herramientas de Python para el análisis de datos médicos
  Durante el desarrollo surgieron varias dificultades comunes en el procesamiento de imágenes médicas, como la presencia de archivos DICOM incompletos, formatos comprimidos no soportados, estudios parcialmente
  anonimizados con metadatos faltantes, variaciones entre modalidades y archivos sin información de imagen (pixel_array). También fue necesario gestionar adecuadamente errores en la lectura y estandarizar los
  datos extraídos para garantizar su coherencia dentro del DataFrame.
  El uso de herramientas de Python como pydicom, numpy y pandas fue fundamental para superar estos desafíos. Pydicom facilitó la lectura y manipulación de metadatos DICOM de forma transparente, numpy permitió
  realizar cálculos numéricos eficientes sobre las matrices de imagen y pandas proporcionó una estructura poderosa para organizar, limpiar y exportar los datos obtenidos. Estas bibliotecas permiten crear flujos
  de trabajo robustos, reproducibles y escalables en el análisis de datos médicos, representando un apoyo clave tanto para aplicaciones educativas como para soluciones reales en informática médica.
