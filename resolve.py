#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autor: Juan Luis Font
# Email: juanlufont@gmail.com
# Licencia: GPLv3

"""
El script toma como entrada un archivo CSV con una columna "lugar", obtiene las
coordenadas geográficas asociadas y genera un CSV incluyendo las columnas
"latitud" y "longitud". El código también normaliza el campo "tiempo" y lo
almacena en "tiempo_norm".
"""

from geopy.geocoders import Nominatim
import pandas as pd

# objeto geolocalizador
geo = Nominatim(user_agent="gephi")

# carga datos desde CSV
df = pd.read_csv("./gephi-raw.csv")

# obtener lista de coordenadas asociadas a lugares
# lista de tuplas (latitud, longitud)
coordinates = df.apply(
    lambda x: geo.geocode(",".join([x["lugar"], x["país"]]))[-1], axis=1
)

# crear columnas para latitud y longitud
df["latitud"] = coordinates.apply(lambda x: x[0])
df["longitud"] = coordinates.apply(lambda x: x[1])

# calcula sumatorio de tiempo de usuario
df_years = df[["nombre", "tiempo"]].groupby(["nombre"]).sum()
# conveniente diccionario con los sumatorios de cada participante
years = df_years.to_dict()["tiempo"]
# normaliza periodos de tiempo
df["tiempo_norm"] = df.apply(lambda x: x["tiempo"] / years[x["nombre"]], axis=1)

# guarda resultados en nuevo archivo CSV
df.to_csv("gephi-final.csv", index=False)
