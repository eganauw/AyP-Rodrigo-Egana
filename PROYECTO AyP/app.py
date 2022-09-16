
import requests
import random
from Cliente import Cliente
from ComidaRest import ComidaRest
from BebidaRest import BebidaRest
from Equipo import Equipo
from Partido import Partido
from Jugador import Jugador
from Estadio import Estadio
from ResultadoPartido import ResultadoPartido
import pickle
class App:
    def __init__(self):
        self.teams = ''
        self.equipos = []
        self.arbitros = []
        self.partidos_finalizados = []
        self.partidos_activos = []
        self.resultados = []
        self.clientes = []
        self.productos_rest = []
        self.comidas =[]
        self.bebidas = []
        self.goleadores = []
        self.goleados = []
        self.productos_comprados = []
    

    def start(self):  #Esta función da la bienvenida al programa y muestra el menú inicial.
        print("""
        --- ¡Bienvenido a Saman FIFA! ---
        """)
        while True:
            opcion1 = (input("""
                    ¿Qué desea hacer?
                    Introduzca el número de su elección:

                        1. Precargar datos
                        2. Buscar equipos
                        3. Gestionar partidos
                        4. Comprar entradas
                        5. Buscar en el restaurante
                        6. Comprar en el restaurante
                        7. Ver estadísticas
                        8. Salir 
                        """))
            if opcion1 != "1" and opcion1 != "2" and opcion1 != "3" and opcion1 != "4" and opcion1 != "5" and opcion1 != "6" and opcion1 != "7" and opcion1 != "8":
                print("Error, intente de nuevo: ")
            elif opcion1 == "1":
                self.precargar_datos()
            elif opcion1 == "2":
                self.buscar_equipos()
            elif opcion1 == "3":
                self.gestionar_partidos()
            elif opcion1 == "4":
                self.comprar_entrada()
            elif opcion1 == "5":
                self.buscar_productos()
            elif opcion1 == "6":
                self.comprar_productos()
            elif opcion1 == "7":
                self.estadisticas() 
            else:
                break   

    def precargar_datos(self): #Esta función elimina los datos guardados en archivos txt y importa los datos desde la API
        endpoint = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2122-3/saman_fifa_api/main/api.json"
        res = requests.request("GET",endpoint).json()
        self.teams = res["teams"]
        self.arbitros = res["referees"]
        for equipo in self.teams:
            name = equipo["name"]
            stadiumname = equipo["stadium"]["name"]
            generalmap = equipo["stadium"]["map"]["general"]
            vipmap = equipo["stadium"]["map"]["vip"]
            stadium = Estadio(stadiumname,generalmap,vipmap)
            stats = {"Goles recibidos": 0, "Goles anotados": 0, "Partidos jugados":0, "Puntos": 0}
            lineup = []
            for jugador in equipo["lineup"]:
                playername = jugador["name"]
                number = jugador["number"]
                position = jugador["position"]
                jugador = Jugador(playername,number,position)
                lineup.append(jugador)
            equipo = Equipo(name,stadium,lineup,stats)
            self.equipos.append(equipo)
        
        for i in res["restaurant"]:
            if i["type"] == "c": #Esto para poder distinguir las bebidas de las comidas, ya que una comida no tiene el atributo "alcoholic", ni una bebida tiene el atributo "packing".
                name = i["name"]   
                price = i["price"] 
                quantity = i["quantity"]
                type = i["type"]
                packing = i["packing"]
                comida = ComidaRest(name,price,quantity,type,packing)
                self.productos_rest.append(comida)
                self.comidas.append(comida)
            else:
                name = i["name"]
                price = i["price"] 
                quantity = i["quantity"]
                type = i["type"]
                alcoholic = i["alcoholic"]
                bebida = BebidaRest(name,price,quantity,type,alcoholic)
                self.productos_rest.append(bebida)
                self.bebidas.append(bebida)
        print("¡Los datos se han registrado correctamente desde la API!")

    def buscar_equipos(self): #Esta función enseña las distintas opciones para buscar equipos
        while True:
            opcion = input("""
            1. Buscar por nombre
            2. Buscar por estadio
            3. Buscar por jugador
            4. Ver todos los equipos
            5. <-- Atrás
            """)
            if opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5":
                print("Error, intente de nuevo")
            elif opcion == "1":
                self.equipos_by_name()
            elif opcion == "2":
                self.equipos_by_stadium()
            elif opcion == "3":
                self.equipos_by_player()
            elif opcion == "4":
                for i in self.equipos:
                    print(i.show_attr())
            else:
                break

    def equipos_by_name(self): #Esta función muestra el equipo (y sus atributos) que el usuario ingrese.
        status = 0
        nombre = input("Ingrese el nombre del equipo: ")
        nombre = nombre.title()
        for i in self.equipos:
            if nombre == i.name: #Aqui compara el nombre ingresado con los nombres de los equipos en la lista "self.equipos".
                status = 1
                team = i
        if status == 1:
            print(team.show_attr())
        else:
            print(f"No se encontró ningún equipo llamado '{nombre}'")
                
    def equipos_by_stadium(self): #Esta función permite que el usuario introduzca el nombre de el estadio y retorna el equipo perteneciente a ese estadio
        status = 0
        stadium = input("Introduzca el nombre del estadio: ")
        stadium = stadium.title()
        for i in self.equipos:
            if stadium == i.stadium.stadiumname: #Compara el nombre ingresado con los nombres de los estadios de los equipos.
                status = 1
                team = i
        if status == 1:
            print(team.show_attr())
        else:
            print(f"No existe ningún estadio llamado '{stadium}'")
            
    def equipos_by_player(self): #Esta función muestra el equipo al que el jugador ingresado pertenece.
        status = 0
        player = input("Introduzca el nombre del jugador: ")
        player = player.title()
        for i in self.equipos:
            for x in i.lineup:
                if player == x.playername: #Compara el nombre ingresado con los nombres de cada lista de jugadores de cada equipo.
                    status = 1
                    team = i
        if status == 1:
            print(team.show_attr())
        else:
            print(f"No se encontró ningún jugador llamado '{player}'")

    def gestionar_partidos(self): #Muestra el menú con las opciones de crear y finalizar partidos.
        while True:
            opcion = input("""
            ¿Qué desea hacer?
            1. Crear un partido
            2. Finalizar partidos en curso (ver resultados)
            3. <-- Atrás
            """)
            if opcion != "1" and opcion != "2" and opcion != "3":
                print("Ingrese una opción válida")
            elif opcion == "1":
                self.crear_partido()
            elif opcion == "2":
                self.finalizar_partidos()
            else:
                break

    def crear_partido(self): # Esta función permite crear y registrar un partido
        while True:    
            status1 = 0
            status2 = 0
            equipo1 = input("Ingrese el nombre del primer equipo: ")
            equipo1 = equipo1.title()
            for i in self.equipos:
                if equipo1 == i.name: #Verifica que el nombre ingresado sea un nombre de un equipo, de lo contrario mostrará un error y continúa el loop.
                    status1 = 1
                    team = i
                    break
            if status1 == 1:
                equipo1 = team
                break
            else:
                print(f"No se encontró ningún equipo llamado '{equipo1}'")
        while True: 
            equipo2 = input("Ingrese el nombre del segundo equipo: ")
            equipo2 = equipo2.title()
            if equipo2 != equipo1.name: #Verifica que no se haya seleccionado el mismo equipo 2 veces.
                for i in self.equipos:
                    if equipo2 == i.name:
                        status2 = 1
                        team = i
                        break 
                if status2 == 1:
                    equipo2 = team
                    break
                else:
                    print(f"No se encontró ningún equipo llamado '{equipo2}'")
            else:
                print("Error, ya has seleccionado a ese equipo")
        while True:
            status = 0
            stadium = input("Introduzca el nombre del estadio: ")
            stadium = stadium.title()
            for i in self.equipos:
                if stadium == i.stadium.stadiumname: #Verifica que el nombre del estadio ingresado exista en la lista de equipos.
                    status = 1
                    estadio = i.stadium
            if status == 1:
                stadium = estadio.stadiumname
                break
            else:
                print(f"No existe ningún estadio llamado '{stadium}'")
        arbitro = self.arbitros[random.randint(0,2)] #Escoge un índice al azar de la lista de árbitros.
        asientos_ocupados = {"General":[],"Vip":[]} #Esto servirá mas adelante para validar la selección de asientos en la compra de entradas.
        partido = Partido(equipo1,equipo2,estadio,arbitro,asientos_ocupados)
        self.partidos_activos.append(partido) 
        goleslocal= random.randint(0,8) #Los resultados se generan inmediatamente despues de crear un partido, sin embargo no se muestran hasta que se finalice el partido.
        golesvisitante = random.randint(0,8) #Escoge una cantidad de goles al azar del 0 al 8.
        goleadoreslocal = []
        goleadoresvisitante = []
        count1 = goleslocal
        count2 = golesvisitante
        while count1 != 0: #Escoge jugadores al azar dependiendo de la cantidad de goles anotados
            goleador = equipo1.lineup[random.randint(0,10)].playername
            goleadoreslocal.append(goleador)
            self.goleadores.append(goleador)
            goalkeeper = equipo1.getGoalkeeper()
            self.goleados.append(goalkeeper)
            count1 -= 1
        while count2 != 0:
            goleador = equipo2.lineup[random.randint(0,10)].playername
            goleadoresvisitante.append(goleador)
            self.goleadores.append(goleador)
            goalkeeper = equipo2.getGoalkeeper()
            self.goleados.append(goalkeeper)
            count2 -= 1
        resultado = {"Equipo local": equipo1.name,"Goles equipo1" : goleslocal,"Equipo visitante": equipo2.name,"Goles equipo2" : golesvisitante,"formatg1": (f"Goleadores del {equipo1.name}"),"goleadoreslocal": goleadoreslocal, "formatg2":(f"Goleadores del {equipo2.name}"),"goleadoresvisitante":goleadoresvisitante} #El resultado esta expresado de esta forma para facilitar el dislay de los resultados.
        #Para las estadísticas:
        equipo1.stats["Goles anotados"] += goleslocal 
        equipo1.stats["Goles recibidos"] += golesvisitante
        equipo1.stats["Partidos jugados"] += 1
        equipo1.stats["Puntos"] += goleslocal - golesvisitante
        equipo2.stats["Goles anotados"] += golesvisitante
        equipo2.stats["Goles recibidos"] += goleslocal
        equipo2.stats["Partidos jugados"] += 1
        equipo2.stats["Puntos"] += golesvisitante - goleslocal

        resultadopartido = ResultadoPartido(equipo1,equipo2,estadio,arbitro,asientos_ocupados,resultado)
        self.resultados.append(resultadopartido)
        print(partido.show_attr())
        print("¡Ha comenzado la venta de entradas para este partido!")
    
    def finalizar_partidos(self): #Función que finaliza un partido activo y muestra el resultado final del mismo.
        if len(self.partidos_activos) >0:   
            i = 1
            cant_pa = len(self.partidos_activos)
            while cant_pa > 0: #Muestra los partidos activos con un entero "i" al lado para que el cliente pueda seleccionar el que desee.
                print(f"""
                {i}: {self.partidos_activos[i-1].show_attr()}
                """)
                i+=1
                cant_pa-=1
            while True: 
                while True:
                    try:
                        opcion = int(input("Ingrese el número del partido que desea finalizar: "))
                        break
                    except ValueError:
                        print("Error")
                if opcion not in range(1,len(self.partidos_activos)+1) : #Verifica que el número ingresado coincida con algún partido activo.
                    print("Error, introduzca una opción válida")
                else:
                    print(self.resultados[opcion-1].show_attr())
                    self.partidos_activos.remove(self.partidos_activos[opcion-1]) #Elimina el partido de la lista de partidos activos.
                    self.partidos_finalizados.append(self.resultados[opcion-1])
                    self.resultados.remove(self.resultados[opcion-1])
                    break
        else:
            print("No hay partidos activos por el momento...")
    
    def comprar_entrada(self): #Esta función permite comprar una entrada y registra al cliente con sus datos.
        if len(self.partidos_activos) != 0:
            name = input("Introduzca su nombre: ")
            name = name.title()
            while True:
                while True:  
                    try:
                        cedula = int(input("Introduzca su cédula: "))
                        break
                    except ValueError:
                        print("Ingrese un numero de cédula válido")
                if cedula < 1:
                    print("Ingrese un número de cédula válido")
                else:
                    status = 0
                    for i in self.clientes:
                        if cedula == i.cedula and name != i.name: #Un cliente podra comprar cuantas entradas quiera siempre y cuando se registre con el mismo nombre.
                            status = 1
                    if status == 1:
                        print("Error, ya hay un cliente registrado con ese número de cédula")
                    else:
                        break
            while True: 
                while True:  
                    try:
                        edad = int(input("Introduzca su edad: "))
                        break
                    except ValueError:
                        print("Ingrese una edad válida")
                if edad < 0:
                    print("Ingrese una edad válida")
                else:
                    break
            i = 1
            cant_pa = len(self.partidos_activos)
            while cant_pa > 0:
                print(f"""
                {i}: {self.partidos_activos[i-1].show_attr()}
                """)
                i+=1
                cant_pa-=1
            while True:
                while True:
                    try:
                        opcion = int(input("Ingrese el número del partido que desea ver: "))
                        break
                    except ValueError:
                        print("Error")
                if opcion not in range(1,len(self.partidos_activos)+1) :
                        print("Error, introduzca una opción válida")
                else:
                    partido = self.partidos_activos[opcion-1]
                    break
            while True:   
                entrada_type = input("""¿Qué tipo de entrada desea comprar?
                1. General ($10)
                2. Vip ($20)
                """)
                if entrada_type != "1" and entrada_type != "2":
                    print("Error, ingrese una opción válida")
                else:
                    break
            if entrada_type == "1": #Define el ancho y el largo del mapa según el tipo de entrada para la impresión del mapa de los asientos.
                entrada_type = "General"
                largomapa = self.partidos_activos[opcion-1].estadio.generalmap[0]
                anchomapa = self.partidos_activos[opcion-1].estadio.generalmap[1]
            else:
                entrada_type = "VIP"
                largomapa = self.partidos_activos[opcion-1].estadio.vipmap[0]
                anchomapa = self.partidos_activos[opcion-1].estadio.vipmap[1]
            
            mapa = []
            fila = 0
            asientos = []
            for i in range(largomapa):#El loop se repetirá de manera que tendrá una cantidad de filas y columnas de acuerdo a las dimensiones del mapa.
                puesto = 0
                fila += 1
                row = []
                for i in range(anchomapa):
                    puesto+=1
                    silla = (fila*10+puesto) #Esto hace que los números de los asientos sean concorde a la fila y la columna.
                    asientos.append(silla) #Esta lista tendrá todos los asientos existentes para validar la elección.
                    row.append(silla) #Agrega el asiento a la fila
                mapa.append(row) #Agrega la fila al mapa
            for i in mapa:
                print(i) #Imprime el mapa por filas.
            while True:
                while True:
                    try:
                        asiento = int(input(("Introduzca el asiento que desea: ")))
                        break
                    except ValueError:
                        print("Error, introduzca un asiento válido")
                if asiento not in asientos: #Valida que el asiento existe en la lista de asientos.
                    print("Error, introduzca un asiento válido")
                else:
                    if entrada_type == "General":
                        if asiento in self.partidos_activos[opcion-1].asientos_ocupados["General"]: #Verifica si el asiento ya ha sido escogido por un cliente.
                            print("Ese asiento ya ha sido ocupado :(")
                        else:
                            print(f"Has seleccionado el asiento general {asiento}")
                            break
                    else: 
                        if asiento in self.partidos_activos[opcion-1].asientos_ocupados["Vip"]:
                            print("Ese asiento ya ha sido ocupado :(")
                        else:
                            print(f"Has seleccionado el asiento VIP {asiento}")
                            break
                
            if entrada_type == "General":
                precio_entrada = 10 
            else:
                precio_entrada = 20 

            total = precio_entrada + (precio_entrada*0.16)
            
            print(f"""
                -------------------
                Asiento: {asiento}
                Precio: ${precio_entrada}
                IVA: 16% 
                Descuento: 0%
                Total a pagar: ${total}
                -------------------
                """)
            while True:       
                decision = input("""
                ¿Desea confirmar su compra?
                1. Sí
                2. No
                """)
                if decision != "1" and decision != "2":
                    print("Ingrese una opción válida")
                else:
                    break
            if decision == "1": #Una vez confirmada la compra, agrega el asiento a la lista de asientos ocupados.
                if entrada_type == "General":
                    self.partidos_activos[opcion-1].asientos_ocupados["General"].append(asiento)
                else:
                    self.partidos_activos[opcion-1].asientos_ocupados["Vip"].append(asiento)
                gastos = total
                cliente = Cliente(name,cedula,edad,partido,asiento,entrada_type,gastos) #Registra al cliente.
                self.clientes.append(cliente)
                print("¡Gracias por su compra!")
            else:
                pass
        else:
            print("Por los momentos no hay partidos activos...")
        
    def buscar_productos(self): #Muestra las distintas opciones para buscar productos
        while True:
            opcion = input("""
            ¿Qué desea hacer?
            1. Buscar productos por nombre
            2. Buscar productos por tipo
            3. Buscar productos por rango de precio
            4. Ver todos los productos
            5. <-- Atrás
            """)  
            if opcion != "1" and opcion != "2" and opcion != "3"and opcion != "4" and opcion != "5":
                print("Error, ingrese una opción válida")
            elif opcion == "1":
                self.products_byname()
            elif opcion == "2":
                self.products_bytype()
            elif opcion == "3":
                self.products_byprice()
            elif opcion == "4":
                for i in self.productos_rest:
                    print(i.show_attr())
            else:
                break

    def products_byname(self): #Devuelve el producto con sus datos que tenga el mismo nombre que el ususario ingrese
        status = 0
        nombre = input("Introduzca el nombre del producto: ")
        nombre = nombre.title()
        for i in self.productos_rest:
            if nombre == i.name: #Verifica si el nombre del producto ingresado es un producto existente.
                producto = i
                status = 1
        if status == 1:
            print(producto.show_attr())
        else:
            print(f"No se encontró ningún producto llamado {nombre}")

    def products_bytype(self): #Muestra los productos segun la categoría que el cliente escoja
        while True:
            opcion1 = input("""
            Elija el tipo de productos que desea ver:
            1. Comidas
            2. Bebidas
            3. <-- Atrás
            """)
            if opcion1 != "1" and opcion1 != "2" and opcion1 != "3":
                print("Ingrese una opción válida")
            elif opcion1 == "1":
                while True:
                    opcion2 = input("""
                    Elija una opción:
                    1. Comidas de empaque
                    2. Comidas de preparación
                    3. Ver todas las comidas
                    4. <-- Atrás
                    """)
                    if opcion2 != "1" and opcion2 != "2" and opcion2 != "3" and opcion2 != "4":
                        print("Error, ingrese una opción válida")
                    elif opcion2 == "1":
                        for i in self.comidas:
                            if i.packing == True:
                                print(i.show_attr())
                    elif opcion2 == "2":
                        for i in self.comidas:
                            if i.packing == False:
                                print(i.show_attr())
                    elif opcion2 == "3":
                        for i in self.comidas:
                            print(i.show_attr())
                    else:
                        break
            elif opcion1 == "2":
                while True:
                    opcion3 = input("""
                    Elija una opción:
                    1. Bebidas no alcohólicas
                    2. Bebidas alcohólicas
                    3. Ver todas las bebidas
                    4. <-- Atrás
                    """)
                    if opcion3 != "1" and opcion3 != "2" and opcion3 != "3" and opcion3 != "4":
                        print("Error, ingrese una opción válida")
                    elif opcion3 == "1":
                        for i in self.bebidas:
                            if i.alcoholic == False:
                                print(i.show_attr())
                    elif opcion3 == "2":
                        for i in self.bebidas:
                            if i.alcoholic == True:
                                print(i.show_attr())
                    elif opcion3 == "3":
                        for i in self.bebidas:
                            print(i.show_attr())
                    else:
                        break
            else:
                break

    def products_byprice(self): #Con esta función el cliente puede ingresar un precio mínimo y uno máximo y retorna todos los productos cuyos precios estén en ese rango
        status = 0
        while True:
            try:
                min = int(input("Ingrese el precio mínimo: "))
                break
            except ValueError:
                print("Ingrese un monto válido")   
        while True:
            try:
                max = int(input("Ingrese el precio máximo: "))  
                break
            except ValueError:
                print("Error, ingrese un monto válido")
        for i in self.productos_rest:
            if int(i.price)in range(min,max):
                print(i.show_attr())
                status = 1
        if status == 0:
            print("No se encontró ningún producto en ese rango de precios :(")
    
    def comprar_productos(self): #Permite al cliente comprar productos
        while True:
            try:
                cedula = int(input("Ingrese su número de cédula: "))
                break
            except ValueError:
                print("Error, ingrese un número de cédula válido")
        cedulastatus = 0
        for cliente in self.clientes:
            if cedula == cliente.cedula and cliente.entrada_type == "VIP": #Verifica que la cedula este vinculada a un cliente VIP.
                cedulastatus = 1
                client = cliente
        if cedulastatus == 1:
            i = 1
            cant_products = len(self.productos_rest)
            while cant_products > 0:
                print(f"{i}: {self.productos_rest[i-1].show_attr()}") #Imprime los productos con un indice 'i' al lado para su selección.
                i+=1
                cant_products-=1
            while True:
                while True:
                    try:
                        prod = int(input("Ingrese el número del producto que desea : "))
                        break
                    except ValueError:
                        print("Error")
                if prod not in range(1,len(self.productos_rest)+1) :
                    print("Error, introduzca una opción válida")
                else:
                    prod = self.productos_rest[prod-1]
                    if prod.quantity == 0: #Verifica que esté en stock.
                        print("Lo sentimos, ese producto está agotado :(")
                    else:
                        #NUMERO PERFECTO: un número que la suma de sus divisores es el mismo número.
                        descuento = 0
                        divisores = []
                        msg = ''
                        for i in range(1,cedula):
                            if cedula%i == 0:
                                divisores.append(i) #Busca los divisores
                        if sum(divisores)==cedula: #Verifica si la suma de los divisores es igual a la cedula ingresada.
                            descuento = 15
                            msg = f"¡Tu cédula es un número perfecto, has recibido 15% de descuento!"
                        total = ((prod.price+prod.price*0.16))-((prod.price+prod.price*0.16)*(descuento/100))
                        factura = (f"""
                        Subtotal: ${prod.price}
                        IVA: 16%
                        Descuento: {descuento}%
                        Total a pagar: ${total}
                        {msg}
                        """)
                        print(factura)
                        while True:
                            decision = input("""
                            ¿Desea confirmar su compra?
                            1. Sí
                            2. No
                            """)
                            if decision != "1" and decision != "2":
                                print("Ingrese una opción válida")
                            elif decision == "1":
                                prod.quantity -= 1 #Al confirmar la compra se resta el producto comprado del inventario
                                self.productos_comprados.append(prod)
                                client.gastos += total #Le suma el costo del producto a los gastos totales del cliente.
                                print("¡Gracias por su compra!")
                                break
                            elif decision == "2":
                                break
                            break
                        break
        else:
            print("Para comprar en el restaurante debes comprar una entrada VIP")
            
    def estadisticas(self): #Muestra el menú de opciones para ver las diferentes estadísticas
        while True:
            opcion = input("""
            ¿Qué desea ver?
            1. Promedio de gastos de los clientes VIP
            2. Estadísticas de los equipos
            3. Jugador con mas goles anotados
            4. Arquero con mas goles recibidos
            5. Top 3 productos del restaurante
            6. <-- Atrás
            """)
            if opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5" and opcion != "6":
                print("Error, ingrese una opción válida")
            elif opcion == "1":
                self.promedio_vip()
            elif opcion == "2":
                self.team_stats()
            elif opcion == "3":
                self.best_player()
            elif opcion == "4":
                self.worst_goalie()
            elif opcion == "5":
                self.top3()
            else:
                break
    
    def promedio_vip(self): #Calcula el promedio de todos los atributos "gastos" de los clientes VIP
        if len(self.clientes) != 0:
            gastoslist = []
            for i in self.clientes:
                if i.entrada_type == "VIP":
                    gastoslist.append(i.gastos)
            promedio = sum(gastoslist)/len(gastoslist)
            print(f"El promedio de gasto de los clientes VIP es de {promedio}$")
        else:
            print("Aún no se ha registrado ningún cliente...")

    def team_stats(self): #Retorna una tabla con cada equipo y sus respectivos goles anotados, recibidos, partidos jugados y puntos(los puntos serán los goles anotados menos los goles recibidos)
        print("""___________________________________________________________________________________________
|_____Nombre_____|___Goles recibidos___|__Goles anotados__|__Partidos jugados__|__Puntos__|""")
        for i in self.equipos:
            print(f"""|_{i.name}__|_______{i.stats["Goles recibidos"]}________|________{i.stats["Goles anotados"]}________|________{i.stats["Partidos jugados"]}________|_______{i.stats["Puntos"]}_______|""")

    def best_player(self): #Retorna el jugador con más goles anotados que se encuentran en la lista "self.goleadores".
        if len(self.goleadores) != 0:
            while True:
                opcion = input("""Esto finalizará todos los partidos en curso, ¿Desea continuar?
                        1. Si
                        2. No
                        """)
                if opcion != "1" and opcion != "2":
                    print("Error, ingrese una opción válida")
                elif opcion == "1":
                    self.partidos_activos.clear()
                    best_player = max(self.goleadores,key = self.goleadores.count)
                    print(f"El jugador con mas goles hasta el momento es {best_player}")
                    break
                else:
                    break
        else:
            print("Hasta el momento no se han registrado goles...")

    def worst_goalie(self): #Retorna el arquero con mas goles recibidos de la lista "self.goleados"
        if len(self.goleados) != 0:   
            while True:
                opcion = input("""Esto finalizará todos los partidos en curso, ¿Desea continuar?
                        1. Si
                        2. No 
                        """)
                if opcion != "1" and opcion != "2":
                    print("Error, ingrese una opción válida")
                elif opcion == "1":
                    self.partidos_activos.clear()
                    worst_goalie = max(self.goleados,key=self.goleados.count)
                    print(f"El arquero con más goles recibidos hasta el momento es {worst_goalie.playername}")
                    break
                else:
                    break
        else:
            print("Hasta el momento no se han registrado goles...")

    def top3(self): #Muestra los 3 productos mas vendidos del restaurante
        productos_comprados = []
        for i in self.productos_comprados:
            productos_comprados.append(i)
        if len(self.productos_comprados) != 0:
            no1 = max(productos_comprados,key=productos_comprados.count)
            for i in self.productos_comprados:
                if i == no1:
                    productos_comprados.remove(i)
            print(f"1: {no1.name}")
            if len(productos_comprados)!= 0:
                no2 = max(productos_comprados,key=productos_comprados.count)
                for i in self.productos_comprados:
                    if i == no2:
                        productos_comprados.remove(i)
                print(f"2: {no2.name}")
                if len(productos_comprados) != 0:
                    no3 = max(productos_comprados,key=productos_comprados.count)
                    print(f"3: {no3.name}")
                else:
                    print("Solo se han vendido 2 productos")
            else:
                print("Solo se ha vendido un producto")
                pass
        else:
            print("Aún no se ha registrado ninguna compra...")

     


        
          
        
        


