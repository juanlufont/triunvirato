#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autor: Juan Luis Font
# Email: juanlufont@gmail.com
# Licencia: GPLv3

"""
El script toma como entrada un archivo CSV y genera los archivos de nodos y
aristas compatibles con las especificaciones del sofware Gephi,
https://gephi.org/
"""

import unidecode
import pandas as pd


def flatstring(name):
    """
    La función toma una cadena de texto y realiza las siguientes
    transformaciones: elimina espacios en blanco, convierte la cadena a
    minúsculas y reemplaza vocales acentuadas (á, é, ..) por vocales sin
    acentuar.
    """
    idaux = name.replace(" ", "").lower()
    return unidecode.unidecode(idaux)


# cargar datos desde CSV
df = pd.read_csv("./gephi-final.csv")

# renombrar campos por otros más "friendly" con Gephi
names = {
    "nombre": "name",
    "lugar": "label",
    "latitud": "lat",
    "longitud": "long",
    "tiempo_norm": "time",
}
df = df.rename(columns=names)

# generar identificadores para nodos y personas
# los identificadores necesitan estar libres de caracteres "problemáticos"
# como espacios en blanco
df["id"] = df.apply(lambda x: flatstring(x["label"]), axis=1)
df["person"] = df.apply(lambda x: flatstring(x["name"]), axis=1)

# calcular sumatorio de todos los valores de tiempo asociados a cada usuario
df_nodes = (
    df[["id", "label", "lat", "long", "time"]]
    .groupby(["id", "label", "lat", "long"])
    .sum()
).reset_index()

# guardar resultado en archivo de nodos Gephi
df_nodes.to_csv("gephi-nodes.csv", index=False)

# data frame con información de aristas Gephi
df["source"] = df.apply(lambda x: flatstring(x["label"]), axis=1)
df["name_s"] = df["name"].shift(-1)
df["target"] = df["source"].shift(-1)

df_edges = df[["source", "target", "name", "name_s", "person"]]
df_edges = df_edges[df_edges["name_s"] == df_edges["name"]]
df_edges = df_edges.drop(["name", "name_s"], axis=1)

# guardar resultado en CSV
df_edges.to_csv("gephi-edges.csv", index=False)
