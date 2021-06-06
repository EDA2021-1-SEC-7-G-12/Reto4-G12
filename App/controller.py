"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def initcatalog():
    catalogo = model.initcatalogo()
    loadCatalogo(catalogo)
    return catalogo

def loadCatalogo(catalogo):

    """
    Carga los datos de los archivos CSV en el modelo.
    """
    verfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(verfile, encoding="utf-8"),
                                delimiter=",")
    for vertice in input_file:
        model.addVer(catalogo,vertice)

    confile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(confile, encoding="utf-8"),
                                delimiter=",")
    
    for ruta in input_file:
        ruta["origin"] = ruta["\ufefforigin"]
        model.addInfo(catalogo,ruta)
    paisfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(paisfile, encoding="utf-8"),
                                delimiter=",")
    for pais in input_file:
        model.addcountry(catalogo,pais)

    return catalogo

def clusters(catalogo, lp1, lp2):
    return model.clusters(catalogo, lp1, lp2)