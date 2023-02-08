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

# Contador confirmaciones
cont_conf = 0

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
	global PORT_CLIENT
	while True:
		message = input("")
		message = f"{alias}: {message}"
		
		if len(message) < 980:
			message = f"{alias}: {message}"
			client.sendto(message.encode(), (HOST, PORT))
		# TODO: poner el empaquetar
		else: 
			empaquetar(message, PORT_CLIENT)
			
			

# ---------------------------------------------
# TODO: Desempaquetar
#-----------------------------------------------

#-----------------------------
# hilo para ver si llego todo
#-----------------------------

# --------------------
# hilo de banderas
# ---------------------
def cola_control():
	while not control.empty()
		# Tomar los mensajes de la cola y decodificarlos
		message, addr = control.get()

		# Tomar header, mensaje, numero de paquete
		remitente = message[0:20]
		host_rem = remitente[0:15]
		host_rem = host_rem.replace(" ", "")
		port_rem = remitente[15:]
		port_rem = port_rem.replace(" ", "")
		tipo_control = message[21] # 1: ya me enviaron todo, 2: llegó todo bien, 3: no llegó bien

		if tipo_control == "1":
			todos_enviados = 1
			
		elif tipo_control == "2":
			numero_clientes = int(message[22:])
			cont_conf += 1
			
			if cont_conf == numero_clientes:
				
			
			
			# Al final pasa esto
			modo_reenvío = 0
			

		elif tipo_control == "3":
			cadenas_faltantes = message[22:]
			# Guardar datos de a quien no le llegó bien en un diccionario
			lista_paq_perdidos.append((cadenas_faltantes,client))
			modo_reenvío = 1

	
	
# Declarar e inicializar los hilos de ejecución
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send_message)
t3 = threading.Tread(target=desempaquetar)
t4 = threading.Thread(target=checa_si_llegaron_todos_paq)
t5 = threading.Thread(target=cola_control)
t1.start()
t2.start()

#hola mariana
