﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- ")

def initcatalog():
    return controller.initcatalog()

def clusters(catalogo, lp1, lp2):
    return controller.clusters(catalogo, lp1, lp2)

def totalarcos(catalogo):
    return controller.totalarcos(catalogo)

def rutaminima(catalogo, paisa, paisb):
    return controller.rutaminima(catalogo, paisa, paisb)

def redminima(catalogo):
    return controller.redminima(catalogo)

def adjacentes(catalogo,vertice):
    return controller.adjacentes(catalogo,vertice)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalogo = initcatalog()
    elif int(inputs[0]) == 2:
        lp1=input("Escriba el nombre del primer landing point: ")
        lp2=input("Escriba el nombre del segundo landing point: ")
        resultado = clusters(catalogo, lp1, lp2)
        print("El número de clusters es " + str(resultado[0]) + ".")
        if resultado[1]==True:
            print("Los landing points " + str(lp1) + " y " + str(lp2) + " pertenecen al mismo cluster.")
        elif resultado[1]==False:
            print("Los landing points " + str(lp1) + " y " + str(lp2) + " no pertenecen al mismo cluster.")
    elif int(inputs[0]) == 3:
        resultado=totalarcos(catalogo)
        print(resultado)
    
    elif int(inputs[0]) == 4:
        paisa=input("Ingrese el país desde el que quiere buscar: ")
        paisb=input("Ingrese el país al que quiere llegar: ")
        resultado=rutaminima(catalogo, paisa, paisb)
        if not resultado == "No hay data para uno(s) de los paises dados":
            print("La ruta minima entre "+paisa+" y "+paisb+" es: "+str(round(float(resultado),1)) + "km")
        else:
            print(resultado)

    elif int(inputs[0]) == 5:
        resultado=redminima(catalogo)
        print(resultado[0])
        print(resultado[1])
    elif int(inputs[0]) == 6:
        vertice = input("Diga el nombre del vertice deseado: ")
        result = adjacentes(catalogo,vertice)
        if result["size"] == 0:
            print("No se ha afectado ningún pais/El vertice dado es invalido")
        else:
            print("La cantidad de paises afectados es: " + str(result["size"]))
            print("Los paises afectados son: " + str(result["elements"]))
    else:
        sys.exit(0)
sys.exit(0)
