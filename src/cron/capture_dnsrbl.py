#!/usr/local/bin/python
import sys
sys.path.append('/opt/back_dnsrbl/')
import config 
import datetime
from database import insert,select

print(config.BLACKLIST_DNSBL )

def print_log(func):
	def wrapper(*args,**kwargs):
		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":",end=" ")
		return func(*args,**kwargs)
	return wrapper

@print_log
def print_info(data):
	print(data)

# database connection 
def get_iptable():
	query = """ SELECT * FROM IPS_SEARCH WHERE estado = 'Prepared' """
	print(query)
	output = select(query)
	return output

def get_blacklist_ip():
	query =  """SELECT * FROM DNSBL_IPS"""
	print(query)
	output = select(query)
	return output

def search_blacklist_ip(ip):
	print("asip",ip[1])
	query =  """SELECT * FROM DNSBL_IPS WHERE IP= '%s'""" %(ip[1])
	print(query)
	output = select(query)
	return output

def create_blacklist_intable(ip,typee):
	output="salida"
	if typee == "full":
		for black in config.BLACKLIST_DNSBL:
			query = """ INSERT INTO DNSBL_IPS(IP, DNSBL_IPS, estado) VALUES ('%s','%s','Prepared') """ % (ip[1],black)
			print(query)
			output = insert(query,())
	elif typee == "miss":
		for black in config.BLACKLIST_DNSBL:
			query = """ SELECT * FROM IPS_SEARCH WHERE IP= '%s' and DNSBL_IPS='%s' """ % (ip[1],black)
			print(query)
			output = select(query)
			if(len(output) == 0):
				query = """ INSERT INTO DNSBL_IPS(IP, DNSBL_IPS, estado) VALUES ('%s','%s','Prepared') """ % (ip[1],black)
				print(query)
				output = insert(query,())
	
	query = """ UPDATE IPS_SEARCH SET estado='Staging' WHERE IP ='%s' """ % (ip[1])
	output = insert(query,())
	print_info("termino la busqueda de las blacklist faltantes de "+ip[1])

def select_DNSBL_IPS_prepared():
	query = """ SELECT * FROM DNSBL_IPS WHERE estado = 'Prepared' """
	print(query)
	return select(query)

# controller
def review_list(data,index):
	output=[]
	if(len(data) == 0):
		print_info("no hay ips para crear o reportar informacion")
		output=[]
	else:
		for i in data:
			if( 'Prepared' in i[index]):
				output.append(i)
	return output
	

def review_report(ips_selected):
	output=[]
	ip = []
	ip = review_list(ips_selected,2)
	if(len(ip) == 0 ):
		print_info("no hay ips por tanto no hay nada que revisar y reportar")
		return 1
	else:
		for i in ip:
			search_table_ip = search_blacklist_ip(i)
			if(len(search_table_ip) == 0 ):
				create_blacklist_intable(i,"full")
			else:
				if(len(search_table_ip) != len(config.BLACKLIST_DNSBL)):
					create_blacklist_intable(i,"miss")
		print_info("se termino revision de ips en tablas")
	
def stop_demon():
	import os
	try:
		os.popen("""ps aux | grep create_demon | grep -v 'grep' | awk '{print $2}' | xargs -I {} kill -9 {}""")
		print_info("stop demon")
	except:
		print_info("stop failed")

def start_demon():
	import os
	try:
		os.popen("""/usr/local/bin/python /opt/back_dnsrbl/demon/create_demon.py""")
		print_info("start demon")
	except:
		print_info("start failed")

def report_demon(get_list_planned):
	#(codigo integer primary key autoincrement, IP text, DNSBL_IPS text, estado text)
	import os
	lines=[]
	
	file_path = '/opt/back_dnsrbl/demon/process.py'
	try:
		os.remove(file_path)
		print(f"File '{file_path}' has been successfully removed.")
	except OSError as e:
		print(f"Error: {e.strerror}")
	
	if (len(get_list_planned) > 0):
		lines.append("""from funciones import funcion1,funcion_search_blacklist""")
		lines.append("""funciones=[ {"name":"funcion_1","function":funcion1,"hungry":0,"id_blacklist":"1","ip":"185.64.112.10","blacklist":"ucprotect.tumami.org"},""")
		for l in get_list_planned:
			dict_a=""" {"name":"funcion_%s","function":funcion_search_blacklist,"hungry":0,"id_blacklist":"%s","ip":"%s","blacklist":"%s"}, """ % (l[0],l[0],l[2],l[1])
			lines.append(dict_a)
		lines.append("]")
		with open(file_path, "w") as file:
			for line in lines:
				file.write(str(line) + "\n")
		
	return 1

#planificaciones

if __name__ == "__main__":
	print_info("-------INICIO PLANIFICACION-------")
	
	ips_selected= get_iptable()
	print(ips_selected)
	review_oldest=	review_report(ips_selected)
	stop_demon()
	get_list_planned = select_DNSBL_IPS_prepared()
	print(get_list_planned)
	create_file_function = report_demon(get_list_planned)
	start_demon()
	print_info("-------FIN PLANIFICACION-------")
