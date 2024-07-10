#Bibliotecas
from utils.datetime import get_actual_date, add_days_actual_date
import json 
import ipaddress
from datetime import date
from database import insert,select

# database connection 
def review_ip(ip):
	query = """ SELECT * FROM IPS_SEARCH WHERE IP = '%s' """ % (ip)
	print(query)
	output = select(query)
	return ( len(output) == 0)

def get_iptable():
	query = """ SELECT * FROM IPS_SEARCH """
	print(query)
	output = select(query)
	return output

def get_ipselect(ips):
	query = """ SELECT * FROM IPS_SEARCH WHERE IP IN (%s) """ % (ips)
	print(query)
	output = select(query)
	return output

def add_ip(ip):
	if(review_ip(ip)):
		query = """ INSERT INTO IPS_SEARCH(IP,estado) VALUES ('%s','Prepared')  """ % (ip)
		print(query)
		salida = insert(query,())
		return salida
	else:
		print("existe en el table")
	return 1

def get_dnsbl_ip():
	query = """ SELECT * FROM DNSBL_IPS WHERE estado != 'Prepared' """
	print(query)
	output = select(query)
	return output

# functions de app

def ping():
	return {"status":"success","messages":"aqui estmoas de chile para el mundo"}

def set_group_ips(ips_group):
	salida = {"status":"error", "message":""}
	try:
		list_ips = ips_group.dict()
		if(len(list_ips["ips"]) > 1):
			for ips in list_ips["ips"].split(","):
				if len(ips) > 0:
					uotput= add_ip(ips)
					print(uotput)
	except:
		print("not range")
		salida["status"] = "error"
		salida["message"] = "error en guardar el rango nombre: list_ips"
	
	#esto es un rango
	try:
		if(len(list_ips["ranges"]) > 1):
			for ranges in list_ips["ranges"].split(","):
				if len(ranges) > 0:
					range_ip=list(ipaddress.ip_network(ranges).hosts())  
					for ipss in range_ip:
						#print(str(ipss))
						add_ip(str(ipss))
	except:
		print("not range")
		salida["status"] = "error"
		salida["message"] = "error en guardar el rango nombre: ips"
	salida["status"] = "success"
	salida["message"] = "se guardaron todos los rangos e ips"

	return salida


def get_blacklists():
	output = {"status":"error", "message":"No existen ips ingresadas"}
	IpsTables = get_iptable()
	if (len(IpsTables) > 0):
		output["data"]=IpsTables
		output["message"]="existen ips"
		output["status"]="success"
	else:
		output["message"]="no existen ips"
		output["status"]="error"
	return output

def get_ips(ip):
	output = {"status":"error", "message":"No existen ips ingresadas"}
	try:
		ip_identify = str(ip)
	except:
		output["message"]="el valor "+ip_identify+"no cumple con el formato"
		return output

	if(ip_identify.find("/") >= 0):#this is range
		range_ip=list(ipaddress.ip_network(ip_identify).hosts())
		string_ips="'"
		for ips in range_ip:
			string_ips+=ips+"',"
		string_ips= string_ips[:-1]
		output["status"]="success"
		output["data"] = get_ipselect(string_ips)
	else:#just ip
		string_ips="'"+ip_identify+"'"
		output["data"] = get_ipselect(string_ips)
	if(len(output["data"]) >= 0):
		output["messages"]="Existen ips ingresadas"
		output["status"]="success"
	return output

def forced_search_ip(ip):
	set_group_ips(ip)


def stop_demon():
	import os
	import subprocess
	salida = {"status":"error", "message":""}
	output=""
	#try:
	command="""/usr/bin/ps aux | /usr/bin/grep create_demon | /usr/bin/grep -v 'grep' | /usr/bin/awk '{print $2}' | /usr/bin/xargs -I {} /usr/bin/kill -9 {}"""
	print(command)
	result = subprocess.run(command, shell=True, capture_output=True, text=True)
	output = result.stdout
	salida["status"]="success"
	#except:
	#	output = "Error"
	salida["message"]=output
	return salida


def start_demon():
	import os
	import subprocess
	salida = {"status":"error", "message":""}
	output=""
	try:
		command="""/usr/local/bin/python /opt/back_dnsrbl/demon/create_demon.py"""
		result = subprocess.run(command, shell=True, capture_output=True, text=True)
		output = result.stdout
		salida["status"]="success"
	except:
		output = "Error"
	salida["message"]=output
	return salida

def restart_demon():
	import time
	stop_demon()
	time.sleep(3)
	start_demon()

def status_demon():
	import os
	import subprocess
	salida = {"status":"error", "message":""}
	output=""
	try:
		command="""/usr/bin/tail -n120 /opt/back_dnsrbl/demon/demon.log"""
		result = subprocess.run(command, shell=True, capture_output=True, text=True)
		output = result.stdout.split("\n")
		salida["status"]="success"
	except:
		output = "Error"
	salida["message"]=output
	return salida

def get_review_blacklists():
	output = {"status":"error", "message":"No existen ips ingresadas"}
	IpsTables = get_dnsbl_ip()
	if( len(IpsTables) > 0):
		output["data"]=IpsTables
		output["message"]="dnsblacklist reportadas ips hasta el momento"
		output["status"]="success"
	else:
		output["message"]="dnsblacklist sin reporte"
		output["status"]="error"
	return output
