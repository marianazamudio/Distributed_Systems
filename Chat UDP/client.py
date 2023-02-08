import socket
import threading
import queue
import random
import sys
import Funciones_cliente

# TODO: metodo para vacíar o introducir elementos
# Inicializar lista de tuplas (cadena_paq_per, destinatario)
lista_paq_perdidos = []

# Inicializar lista de clientes con cola  (HOST,PORT):(total de paq)
cola_de_clientes = {}

# Crear diccionario con clientes
dict_messages = {}

# Crear lista con clientes que ya enviaron todo #TODO: controlar esta cosa
lista_todos_paquetes_env = []

# ---- INICIALIZAR BANDERAS ------ #
# Cuando está en 1, indica que el otro cliente ya mandó 10 paquetes
# por lo tanto, se checa que los 10 paquetes hayan llegado a este cliente
todos_enviados = 0
# Cuando está en 1, indica que se deben reenvíar algunos paquetes que no 
# llegaron al otro extremo
modo_reenvio = 0
# Cuando está en 1, indica que se debe esperar a que el cliente dé
# su confirmación de que todos los paquetes llegaron correctamente
# antes de seguir enviando mensajes
espera_conf = 1

# Hacer colas  mensajes y mensajes de control
messages = queue.Queue()
control = queue.Queue()

# Define la dirección y puerto del servidor
HOST = "localhost"
PORT = 9999

# Inicia socket del cliente (protocolo IP y socket UDP)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Coloca al cliente con la IP del local host y en un puerto aleatorio en el
# rango de 8000 a 9000
PORT_CLIENT = random.randint(8000,9000)
client.bind((HOST, PORT_CLIENT))

# Preguntar al usuario por su alias e imprime mensaje de bienvenida
alias = input("Ingresa tu alias: ")
print("\n\n-----------BIENVENIDO A LA SALA --------------")

# Mandar registro de usuario al servidor 
# TODO: agregar header
client.sendto(f"SIGNUP_TAG: {alias}".encode(), (HOST,PORT))

# -----------------------------------------------------------
# Funcion del cliente para recibir mensajes
# TODO: Clasifica todo lo que llega en control o mensaje y
# lo almacena en la cola 
# -----------------------------------------------------------
def receive():
	while True:
		try:
			# Recibir mensaje
			message, addr = client.recvfrom(1024)
			message = message.decode()
			# Si el mensaje es menor a 980 bytes se despliega
			if len(message) < 980:
				print("\t\t\t\t" + message)
			else:
				# Ver si es mensaje o mensaje de control
				if message[20] == "1"
					# Añadir mensaje a cola de control
					control.put((message,addr))
				else:
					# Añadir mensaje a cola de mensajes
					messages.put((message, addr))

		except():
			pass
# ---------------------------------------------------------------
# Funcion del cliente para mandar mensajes
# TODO: Aqui estara empaquetar
# ---------------------------------------------------------------
def send_message():
	while True:
		message = input("")
		message = f"{alias}: {message}"
		
		if len(message) < 980:
			message = f"{alias}: {message}"
			client.sendto(message.encode(), (HOST, PORT))
		# TODO: poner el empaquetar
		else: 
			

# ---------------------------------------------
# TODO: Desempaquetar
#-----------------------------------------------

#-----------------------------
# hilo para ver si llego todo
#-----------------------------

# --------------------
# hilo de banderas
# ---------------------


# Declarar e inicializar los hilos de ejecución
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send_message)
t1.start()
t2.start()

#hola mariana
