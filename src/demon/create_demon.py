#!/usr/local/bin/python
import daemon
import threading
import time
import sys
from process import funciones
from funciones import show_process
# Crear una lista de funciones
#funciones = [
#    {"name":"funcion_1","function":funcion1,"hungry":0,"id_blacklist":"1","ip":"185.64.112.10","blacklist":"ucprotect.tumami.org"},
#    {"name":"funcion_2","function":funcion2,"hungry":0,"id_blacklist":"1","ip":"185.64.112.10","blacklist":"ucprotect.tumami.org"},
#]
funciones_activas=[]
funciones_activas=[]

# Controlar la cantidad máxima de procesos activos
max_procesos_activos = 2
procesos_activos = 0
lock = threading.Lock()

def ejecutar_funcion(funcion,name,id_blacklist,ip,blacklist):
    global procesos_activos
    global funciones_activas
    global funciones
    with lock:
        funciones_activas.append(name)
        procesos_activos += 1
        
    
    funcion(id_blacklist,ip,blacklist)
    
    with lock:
        funciones_activas.remove(name)
        procesos_activos -= 1

def search_hungry(lista):
    menor= lista[0]["hungry"]
    posicion=0
    for i in range(0,len(lista)):
        if(lista[posicion]["hungry"] < lista[i]["hungry"]):
            posicion=i
    return posicion


def demonio():
    while True:
        # Realiza aquí las tareas que deseas que el demonio ejecute en segundo plano
        #print("Ejecutando tarea del demonio...")        
        show_process(funciones_activas)
        #print(funciones_activas)
        sys.stdout.flush()  # Asegura que la salida se escriba inmediatamente en el archivo
        if procesos_activos < max_procesos_activos:
            index=search_hungry(funciones)
            funcion= funciones[index]
            if not (funcion["name"] in funciones_activas) and  procesos_activos < max_procesos_activos:
                funciones[index]["hungry"]=0#print(funcion["name"])
                threading.Thread(target=ejecutar_funcion, args=(funcion["function"],funcion["name"],funcion["id_blacklist"],funcion["ip"],funcion["blacklist"])).start()
            for i in range (0,len(funciones)):
                funciones[i]["hungry"]+=1
            #for i in range (0,len(funciones)):
            #    print(funciones[i]["name"],funciones[i]["hungry"])

        time.sleep(1)  # Espera 5 segundos antes de realizar la siguiente iteración

ruta_log = '/opt/back_dnsrbl/demon/demon.log'  

# Crea el contexto del demonio y redirige la salida al archivo
with daemon.DaemonContext(stdout=open(ruta_log, 'a+')):
    demonio()
