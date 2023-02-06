import socket
import threading
import random
import sys

HOST = "localhost"
PORT = 9999

# Inicia socket del cliente (protocolo IP y socket UDP)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Coloca al cliente con la IP del local host y en un puerto aleatorio en el
# rango de 8000 a 9000
client.bind((HOST, random.randint(8000,9000)))
# Preguntar al usuario por su alias
alias = input("Ingresa tu alias: ")
print("\n\n-----------BIENVENIDO A LA SALA --------------")
client.sendto(f"SIGNUP_TAG: {alias}".encode(), (HOST,PORT))

# -----------------------------------------------------------
# Funcion del cliente para recibir mensajes 
# -----------------------------------------------------------
def receive():
	while True:
		try:
			# Recibir mensajes de longitud estandar (1024 bytes)
			# y decodificar
			message, addr = client.recvfrom(1024)
			message = message.decode()
			print("\t\t\t\t" + message)

		except():
			pass
# ---------------------------------------------------------------
# Funcion para mandar mensajes
# ---------------------------------------------------------------
def send_message():
	while True:
		message = input("")
		if message == "!q":
			exit()
		else:
			message = f"{alias}: {message}"
			client.sendto(message.encode(), (HOST, PORT))

# Declarar e inicializar los hilos de ejecución
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send_message)
t1.start()
t2.start()


