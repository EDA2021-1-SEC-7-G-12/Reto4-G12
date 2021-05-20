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
    catalogo = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

    catalogo['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

    catalogo['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
    return catalogo

def addStopConnection(catalogo, lastservice, service):
    origin = formatVertex(lastservice)
    destination = formatVertex(service)
    cleanServiceDistance(lastservice, service)
    distance = float(service['Distance']) - float(lastservice['Distance'])
    distance = abs(distance)
    addStop(catalogo, origin)
    addStop(catalogo, destination)
    addConnection(catalogo, origin, destination, distance)
    addRouteStop(catalogo, service)
    addRouteStop(catalogo, lastservice)
    return catalogo

def compareStopIds(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def addStop(catalogo, stopid):
    if not gr.containsVertex(catalogo['connections'], stopid):
            gr.insertVertex(catalogo['connections'], stopid)
    return catalogo


def addRouteStop(catalogo, service):
    entry = m.get(catalogo['stops'], service['BusStopCode'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, service['ServiceNo'])
        m.put(catalogo['stops'], service['BusStopCode'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['ServiceNo']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return catalogo

def cleanServiceDistance(lastservice, service):
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name

def addConnection(catalogo, origin, destination, distance):
    edge = gr.getEdge(catalogo['connections'], origin, destination)
    if edge is None:
        gr.addEdge(catalogo['connections'], origin, destination, distance)
    return catalogo

def addRouteConnections(catalogo):

    lststops = m.keySet(catalogo['stops'])
    for key in lt.iterator(lststops):
        lstroutes = m.get(catalogo['stops'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(catalogo, prevrout, route, 0)
                addConnection(catalogo, route, prevrout, 0)
            prevrout = route