# Breve análisis de la movilidad

Este repositorio contiene el código fuente y datos usados en la realización del trabajo *"Breve análisis de la movilidad de los estudiantes del Máster de Historia y Humanidades Digitales de la UPO (2020-2021) mediante un grafo georreferenciado realizado en Gephi"*, realizado en el contexto de la asignatura *"Metodología para la investigación en Historia y Humanidades Digitales I"*, curso académico 2020-2021.

El código y datos permiten generar un grafo georreferenciado usando el software [Gephi](https://gephi.org/).

## Anonimización de datos

Los datos han sido anonimizados:

- no incluyen nombres reales, únicamente aliases elegidos por los propios encuestados.
- los valores del campo `tiempo` han sido previamente normalizados, mostrando solo valores entre 0 y 1, calculados en función del tiempo total declarado por el encuestado.

## Archivos de datos

### Datos originales gephi-raw.csv

El archivo `gephi-raw.csv` contiene los datos recopilados por la encuesta creada en Google Forms, con algunas modificaciones de formato como son la división de la lista de lugares de residencia en varias filas independientes.

Los campos del archivo `gephi-raw.csv` son:

- `nombre`: nombre / alias del participante
- `lugar`: nombre de la localidad donde el participante ha residido
- `país`: país en el que se encuentra el lugar de residencia
- `tiempo`: cantidad de tiempo, en años, en la que el participante ha residido la localidad

Los valores del campo `tiempo` en la versión del archivo disponible en el repositorio han sido reemplazados por valores normalizados, para aumentar el grado de anonimato de los datos. Este cambio no tiene ningún impacto en el posterior procesado de los datos.

### Datos con información geográfica, gephi-total.csv

El archivo `gephi-total.csv` es el resultado de procesar los datos del archivo `gephi-raw.csv` con el script `resolve.py`.

Los campos del archivo `gephi-final.csv` son:

- `nombre`: nombre / alias del participante
- `lugar`: nombre de la localidad donde el participante ha residido
- `país`: país en el que se encuentra el lugar de residencia
- `tiempo`: cantidad de tiempo, en años, en la que el participante ha residido la localidad
- `latitud`: latitud asociada al lugar de residencia
- `longitud`: longitud asociada al lugar de residencia
- `tiempo_norm`: normalización del campo `tiempo`, resultado de dividir este campo por la suma de todos los periodos de tiempo reportados por el participante

### Archivo con nodos Gephi, gephi-nodes.csv

El archivo `gephi-nodes.csv` define los nodos del grafo georreferenciado en formato _Gephi_. Cada nodo representa una ciudad, incluyendo sus coordenadas geográficas, y el sumatorio del tiempo reportado por todos los encuestados para dicha ciudad. Este archivo es el resultado de aplicar el scrip `refactor.py` al archivo `gephi-total.csv`.

Los campos del archivo `gephi-nodes.csv` son:

- `id`: identificador de nodo Gephi, generado a partir del nombre de la ciudad, eliminando espacios y caracteres no ASCII
- `label`: nombre de la ciudad
- `lat`: latitud
- `long`: longitud
- `time`: sumatorio de tiempos (normalizados) declarados para el nodo

### Archivo con aristas Gephi, gephi-edges.csv

El archivo `gephi-edges.csv` define las aristas del grafo georreferenciado en formato _Gephi_. Cada nodo une una ciudad con la siguiente en el que el encuestado a residido. Este archivo es el resultado de aplicar el scrip `refactor.py` al archivo `gephi-total.csv`.

Los campos del archivo `gephi-edges.csv` son:

- `source`: ciudad de origen
- `target`: ciudad de destino
- `person`: etiqueta generada a partir del nombre / alias del encuestado

## Procesado de datos

Los scripts `resolve.py` y `refactor.py` realizan el procesado y transformaciones necesarias para pasar de los datos originales obtenidos por Google Forms a los archivos CSV usados por Gephi para generar el grafo georreferenciado.

### Requisitos software

El código fuente para procesado de datos está escrito en Python 3. Las librerías necesarias para ejecutar los scripts están listadas en el archivo `requisitos.txt`.

Para generar un _virtual environment_ para la ejecución de los scripts en un entorno con Python 3 y paquete `venv` preinstalados, ejecutar:

```
python3 -m vnev venv
source ./venv/bin/active
pip3 install -r requirements.txt
```

### Script resolve.py

El script `resolve.py` procesa el archivo `gephi-raw.csv` y genera `gephi-final.csv`.

El script `resolve.py` hace uso de la librería `geopy` para obtener la latitud y longitud de los lugares de residencia reportados por los participantes de la encuesta.

La normalización de los periodos de tiempo está basada en la librería para análisis datos `pandas`.

### Script refactor.py

El script `refactor.py` procesa el archivo `gephi-total.csv` y genera los archivos `gephi-nodes` y `gephi-edges.csv`, los cuales definen un grafo georreferenciado que puede ser representado usando Gephi.
