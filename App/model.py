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
                    "paisesn't": None
                    }

    catalogo["vertices"] = m.newMap(numelements=14000,
                                     maptype='PROBING')

    catalogo['conexiones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000, comparefunction=None)

    catalogo["paises"] = m.newMap(numelements=14000,
                                     maptype='PROBING')

    catalogo["paisesn't"] =  m.newMap(numelements=14000, maptype='PROBING')
    print( catalogo["paisesn't"])
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
    if not gr.containsVertex(catalogo['conexiones'], vertice["landing_point_id"]):
        gr.insertVertex(catalogo['conexiones'], vertice["landing_point_id"])
   


def addConexion(catalogo,origen,destino,distancia):
    edge = gr.getEdge(catalogo['conexiones'], origen, destino)
    if edge is None:
        gr.addEdge(catalogo['conexiones'], origen, destino, distancia)

def addPaisesnt(catalogo, id):
     m.put(catalogo["paisesn't"],id["name"],id["landing_point_id"])