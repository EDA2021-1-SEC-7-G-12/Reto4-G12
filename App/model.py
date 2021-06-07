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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import math
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def initcatalogo():
    catalogo  = {
                    'vertices': None,
                    'conexiones': None,
                    "paises": None,
                    "paisesn't": None,
                    "mapaises": None
                    }

    catalogo["vertices"] = m.newMap(numelements=14000,
                                     maptype='PROBING')

    catalogo['conexiones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000, comparefunction=None)

    catalogo["paises"] = m.newMap(numelements=14000,
                                     maptype='PROBING')

    catalogo["invertices"] =  m.newMap(numelements=14000, maptype='PROBING')

    catalogo["mapaises"] =  m.newMap(numelements=600, maptype='PROBING')

    return catalogo


def addInfo(catalogo,ruta):
    addConexion(catalogo,ruta["origin"],ruta["destination"],haversine(catalogo,ruta))


def haversine(catalogo,ruta):
    origen = ruta["origin"]
    destination = ruta["destination"]
    inforigen = m.get(catalogo["vertices"],origen)["value"]
    infodest = m.get(catalogo["vertices"],destination)["value"]
    c = math.pi/180 
    dist = abs(2*6371000*math.asin(math.sqrt(math.sin(c*(float(infodest["latitude"])-float(inforigen["latitude"]))/2)**2 + math.cos(c*float(inforigen["latitude"]))*math.cos(c*float(infodest["latitude"]))*math.sin(c*(float(infodest["longitude"])-float(inforigen["longitude"]))/2)**2)))
    return dist


def addVer(catalogo,vertice):
    m.put(catalogo["vertices"],vertice["landing_point_id"],vertice)
    m.put(catalogo["invertices"],vertice["name"].split(",")[0],vertice["landing_point_id"])
    if not gr.containsVertex(catalogo['conexiones'], vertice["landing_point_id"]):
        gr.insertVertex(catalogo['conexiones'], vertice["landing_point_id"])
    pais = vertice["name"].split(",") 
    if len(pais)>1:
        if len(pais[1]) > 3:
            if not m.contains(catalogo["mapaises"],pais[1].strip(" ")):
                m.put(catalogo["mapaises"],pais[1].strip(" "),lt.newList("ARRAY_LIST"))
            lt.addLast(m.get(catalogo["mapaises"],pais[1].strip(" "))["value"],vertice["landing_point_id"])
        else:
            if not m.contains(catalogo["mapaises"],pais[2].strip(" ")):
                m.put(catalogo["mapaises"],pais[2].strip(" "),lt.newList("ARRAY_LIST"))
            lt.addLast(m.get(catalogo["mapaises"],pais[2].strip(" "))["value"],vertice["landing_point_id"])


def addConexion(catalogo,origen,destino,distancia):
    edge = gr.getEdge(catalogo['conexiones'], origen, destino)
    if edge is None:
        gr.addEdge(catalogo['conexiones'], origen, destino, distancia)


def addcountry(catalogo,pais):
    if not pais == None: 
        m.put(catalogo["paises"],pais["CountryName"],pais)
        gr.insertVertex(catalogo['conexiones'], pais["CapitalName"])
        if not m.get(catalogo["mapaises"],pais["CountryName"]) == None:
            listapoints = m.get(catalogo["mapaises"],pais["CountryName"])["value"]
            for x in range(int(listapoints["size"])):
                vertice = lt.getElement(listapoints,x)
                edge = gr.getEdge(catalogo['conexiones'], pais["CapitalName"], vertice)
                infodestino = m.get(catalogo["vertices"],vertice)["value"]
                c = math.pi/180 
                dist = abs(2*6371000*math.asin(math.sqrt(math.sin(c*(float(infodestino["latitude"])-float(pais["CapitalLatitude"]))/2)**2 + math.cos(c*float(pais["CapitalLatitude"]))*math.cos(c*float(infodestino["latitude"]))*math.sin(c*(float(infodestino["longitude"])-float(pais["CapitalLongitude"]))/2)**2)))
                if edge is None:
                    gr.addEdge(catalogo['conexiones'], pais["CapitalName"], vertice, dist)


def clusters(catalogo, lp1, lp2):
    componentes=scc.KosarajuSCC(catalogo["conexiones"])
    conexionlp=scc.stronglyConnected(componentes, m.get(catalogo["invertices"],lp1)["value"], m.get(catalogo["invertices"],lp2)["value"])
    return componentes["components"], conexionlp


def totalarcos(catalogo):
    lista=lt.newList("ARRAY_LIST")
    for x in catalogo["vertices"]:
        grado=gr.degree(catalogo, x)
        if grado>1:
            lt.addLast(lista, x)

    return lt.size(lista)