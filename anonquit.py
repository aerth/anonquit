#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################
# Anonquit es un cliente de gnusocial sencillo para la línea #
# de comandos. fanta - <http://elbinario.net>                #
##############################################################

import sys
import sqlite3
import subprocess
import os
import getpass

# Comprobaciones varias
if sys.version_info<(3,1,4):
	sys.stderr.write("Necesita python 3.1.4 o posterior\n")
	exit(1)
if sys.platform != "linux":
	print ("Necesita GNU/Linux para ejecutar anonquit correctamente")
	exit(1)
if subprocess.getoutput("whoami") == "root":
	print ("No esta permitido utilizar el usuario root para ejecutar anonquit")
	exit(1)

# Directorio de Anonquit
nombre = "AnonQuit"
version = "0.1"
apipath = "/api/statuses/update.xml"
tor_host = "localhost"
tor_port = "9050"
usuario = subprocess.getoutput("whoami") 
config_dir= "/home/" + usuario + "/.config"
db_dir = config_dir + "/anonquit"
db_name = "anonquit.db"

if os.path.exists(config_dir): 

	if os.path.exists(db_dir):
		if os.path.exists(db_dir + "/" + db_name):
			if len(sys.argv) == 1:
				print(nombre, version + "\n-h --help\tMuestra la ayuda\n-v --version\tMuestra la versión\n-u --user\tPara utilizar una cuenta de usuario\n-a --adduser\tAñadir una cuenta de usuario\n-d --deluser\tEliminar una cuenta de usuario")
			elif len(sys.argv) == 2:
				if sys.argv[1] == "-v" or sys.argv[1] == "--version":
					print(nombre, version)
				elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
					print(nombre, version + "\n-h --help\tMuestra la ayuda\n-v --version\tMuestra la versión\n-u --user\tPara utilizar una cuenta de usuario\n-a --adduser\tAñadir una cuenta de usuario\n-d --deluser\tEliminar una cuenta de usuario")
				elif sys.argv[1] == "-u" or sys.argv[1] == "--user":
					print ("Error: Falta el nombre del usuario.\nEjemplo: anonquit -u fanta@gnusocial.net")
				elif sys.argv[1] == "-a" or sys.argv[1] == "--adduser":
					nombre_usuario = input("Nombre de usuario (ejemplo fanta): ")
					nodo_usuario = input("Nodo (ejemplo gnusocial.net): ")
					passwd_usuario = getpass.getpass('Password: ')
					db = sqlite3.connect(db_dir +'/' + db_name)
					resultado = db.execute("SELECT user,node FROM accounts WHERE user = ? AND node = ?;", (nombre_usuario,nodo_usuario))
					row = []
					for row in resultado:
						nombre_usuario_db = row[0]
						nodo_usuario_db = row[1]
					db.commit()
					if len(row) == 2:
						print ("Esa cuenta de usuario ya esta configurada. NO se ha añadido de nuevo.")
					else:
						cursor = db.cursor()
						cursor.execute("INSERT INTO accounts(user,node,password) VALUES (?,?,?);", (nombre_usuario,nodo_usuario,passwd_usuario))
						db.commit()
						db.close()
						print ("cuenta de usuario " + nombre_usuario + " creada\nPara mandar un mensaje use: anonquit -u " + nombre_usuario + "@" + nodo_usuario + " 'El mensaje que quiera mandar'")
				elif sys.argv[1] == "-d" or sys.argv[1] == "--deluser":
					nombre_usuario = input("Nombre de usuario para borrar (ejemplo fanta): ")
					nodo_usuario = input("Nodo (ejemplo gnusocial.net): ")
					db = sqlite3.connect(db_dir +'/' + db_name)
					cursor = db.cursor()
					cursor.execute("DELETE FROM accounts WHERE user = ? AND node = ?;", (nombre_usuario,nodo_usuario))
					db.commit()
					db.close()
					print ("cuenta de usuario " + nombre_usuario + " borrada")

			elif len(sys.argv) == 3:
				if sys.argv[1] == "-u" or sys.argv[1] == "--user":
					nombre_usuario = sys.argv[2].split("@")[0]
					nodo_usuario = sys.argv[2].split("@")[1]
					db = sqlite3.connect(db_dir +'/' + db_name)
					resultado = db.execute("SELECT user,node FROM accounts WHERE user = ? AND node = ?;", (nombre_usuario,nodo_usuario))
					row = []
					for row in resultado:
						nombre_usuario_db = row[0]
						nodo_usuario_db = row[1]
					db.commit()
					db.close()
					if len(row) == 2:
						print ("La cuenta del usuario " + nombre_usuario + " en el nodo " + nodo_usuario + " esta configurada\nIndique el mensaje que quiere enviar ya que le falta el parametro del mensaje\nEjemplo: anonquit -u " + nombre_usuario_db + "@" + nodo_usuario_db + " 'Hola mundo'")
					else:
						print ("La cuenta del usuario " + nombre_usuario + " en el nodo " + nodo_usuario + " no esta añadida.\nPruebe a añadirla con la opción -a o --adduser")

			elif len(sys.argv) == 4 or len(sys.argv) == 5:
				if sys.argv[1] == "-u" or sys.argv[1] == "--user":
					nombre_usuario = sys.argv[2].split("@")[0]
					nodo_usuario = sys.argv[2].split("@")[1]
					db = sqlite3.connect(db_dir +'/' + db_name)
					resultado = db.execute("SELECT user,node,password FROM accounts WHERE user = ? AND node = ?;", (nombre_usuario,nodo_usuario))
					row = []
					for row in resultado:
						nombre_usuario_db = row[0]
						nodo_usuario_db = row[1]
						password_usuario_db = row[2]
					db.commit()
					db.close()
					if len(row) == 3:
						mensaje_usuario = sys.argv[3]
						url_status = "http://" + nodo_usuario + apipath
						if len(sys.argv) == 5:
							if sys.argv[4] == "-t" or sys.argv[4] == "--tor":
								subprocess.getoutput("curl --socks5 " + tor_host  + ":" + tor_port + " -u " + nombre_usuario + ":" + password_usuario_db + " " + url_status  + " -d status=\'" + mensaje_usuario  + "\'")
								print ("La publicación ha sido mandada por la red tor")
							else:
								print ("El cuarto argumento no es correcto. Pruebe -t o --tor para enviar por la red tor.")
						else:
							subprocess.getoutput("curl -u " + nombre_usuario + ":" + password_usuario_db + " " + url_status  + " -d status=\'" + mensaje_usuario  + "\'")
					else:
						print ("Revise el nombre de la cuenta y el nodo. Es posible que no este añadida o que este mal escrito.")

		else:
			db = sqlite3.connect(db_dir +'/' + db_name)
			cursor = db.cursor()
			cursor.execute('''CREATE TABLE IF NOT EXISTS accounts(user TEXT, node TEXT, password TEXT)''')
			db.commit()
			db.close()
	else:
		os.mkdir(db_dir)
else:
	os.mkdir(config_dir)
