# coding=utf-8
import os
import sqlite3

###SQLITE
def connection_sqlite3():
	conexion=sqlite3.connect("/opt/database.bd")
	return conexion

def create_table_bloqueos():
	conexion=connection_sqlite3()
	try:
		conexion.execute("""CREATE TABLE IPS_SEARCH (codigo integer primary key autoincrement, IP text, estado text)""")
		print("se creo la tabla ips")
	except sqlite3.OperationalError as e:
		print("La tabla IPS_SEARCH ya existe",e)

	try:
		conexion.execute("""CREATE TABLE DNSBL_IPS  (codigo integer primary key autoincrement, IP text, DNSBL_IPS text, estado text)""")
		print("se creo la tabla dnsbl_ips")
	
	except sqlite3.OperationalError as e:
		print("La tabla DNSBL_IPS ya existe",e)

	conexion.close()
	return 1

def insert(insert_text,list_values=()):#update
	conexion=connection_sqlite3()
	try:
		conexion.execute(insert_text, list_values )
		conexion.commit()
	except sqlite3.OperationalError as e:
		print("",e)

	conexion.close()

def select(select_text):
	conexion=connection_sqlite3()
	cursor=conexion.execute(select_text)
	list_select=[]
	filas=cursor.fetchall()
	if len(filas)>0:
		for fila in filas:
			list_select.append(fila)
	else:
		print("fallo select")
	conexion.close()
	return list_select
