# Definir funciones adicionales
import datetime
import time
#database
import sys
sys.path.append('/opt/back_dnsrbl/')
from database import insert

def printer_log(func):
	def wrapper(*args,**kwargs):
		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":",end=" ")
		return func(*args,**kwargs)
	return wrapper

@printer_log
def show_process(procesos_act):
	print("procesos:",procesos_act) 

@printer_log
def funcion1(id_blacklist,ip,blacklist):
	print("Ejecutando función 1...",id_blacklist,ip,blacklist)
	time.sleep(5)

@printer_log
def funcion_search_blacklist(id_blacklist,ip,blacklist):
	import os
	import subprocess
	value_update="Prepared"
	try:
		ip_reverse = ".".join(ip.split(".")[::-1])
		command="""host -W 2 -t a %s.%s""" % (ip_reverse,blacklist)
		result = subprocess.run(command, shell=True, capture_output=True, text=True)
		output = result.stdout.split("\n")
		if "not found" in output:
			value_update="Done"
		elif( "address" in output):
			value_update="Exist"
	except:
		output = "Error"
	
	query = """ UPDATE IPS_SEARCH SET estado='%s' WHERE codigo ='%s' """ % (value_update,id_blacklist)
	output = insert(query,())

	print("Execute funcion_search_blacklist(params):",id_blacklist,ip,blacklist)
	time.sleep(1)
	

@printer_log
def example_function(id_blacklist,ip,blacklist):
	print("Ejecutando función 2...",id_blacklist,ip,blacklist)
	time.sleep(10)