"""
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
    print("2- Analizar clústers de landing points en la red de cables")
    print("3- Buscar puntos de interconexión en la red")
    print("4- Buscar la ruta minima para enviar informacion entre dos paises")
    print("5- Identificar red de expansión mínima en la red")
    print("6- Analizar el impacto del fallo de un landing point en otros países")

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
        catalogoo = initcatalog()
        catalogo = catalogoo[0]
        print("Tiempo [ms]: ", f"{catalogoo[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{catalogoo[1]:.3f}")

    elif int(inputs[0]) == 2:
        lp1=input("Escriba el nombre del primer landing point: ")
        lp2=input("Escriba el nombre del segundo landing point: ")
        resultado = clusters(catalogo, lp1, lp2)
        print("El número de clusters es " + str(resultado[0][0]) + ".")
        if resultado[0][1]==True:
            print("Los landing points " + str(lp1) + " y " + str(lp2) + " pertenecen al mismo cluster.")
        else:
            print("Los landing points " + str(lp1) + " y " + str(lp2) + " no pertenecen al mismo cluster.")
        print("Tiempo [ms]: ", f"{resultado[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{resultado[1]:.3f}")

    elif int(inputs[0]) == 3:
        resultado=totalarcos(catalogo)
        print("Lista de resultados: ")
        print(resultado[0][0]["elements"])
        print("Número de cables conectados a los landing points de la lista: " + str(resultado[0][1]))
        print("Tiempo [ms]: ", f"{resultado[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{resultado[1]:.3f}")

    elif int(inputs[0]) == 4:
        paisa=input("Ingrese el país desde el que quiere buscar: ")
        paisb=input("Ingrese el país al que quiere llegar: ")
        resultado=rutaminima(catalogo, paisa, paisb)
        if not resultado[0] == "No hay data para uno(s) de los paises dados":
            print("La ruta minima entre "+paisa+" y "+paisb+" es: "+str(round(float(resultado[0]),1)) + " km.")
        else:
            print(resultado[0])
        print("Tiempo [ms]: ", f"{resultado[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{resultado[1]:.3f}")

    elif int(inputs[0]) == 5:
        resultado=redminima(catalogo)
        print("El numero total de vertices del MST es: " + str(resultado[0][0]))
        print("El peso total del MST es: " + str(round(float(resultado[0][1]),1)))
        print("Tiempo [ms]: ", f"{resultado[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{resultado[1]:.3f}")

    elif int(inputs[0]) == 6:
        vertice = input("Diga el nombre del vertice deseado: ")
        result = adjacentes(catalogo,vertice)
        if result[0]["size"] == 0:
            print("No se ha afectado ningún pais/El vertice dado es invalido")
        else:
            print("La cantidad de paises afectados es: " + str(result[0]["size"]))
            print("Los paises afectados son: " + str(result[0]["elements"]))
        print("Tiempo [ms]: ", f"{result[2]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{result[1]:.3f}")

    else:
        sys.exit(0)
sys.exit(0)
