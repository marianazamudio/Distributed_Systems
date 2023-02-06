import socket
import threading
import queue

# Aqui se almacenarán los mensajes de la cola
messages = queue.Queue()
# Esta lista almacena a los clientes
clients = []

# Crear socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# El servidor se aloja en la computadora host y utiliza el puerto 9999
server.bind(("localhost",9999))

# --------------------------------------------------------------------------
# Funcion para recibir los mensajes
# --------------------------------------------------------------------------
def receive():
	while True:
		try:
			# Recibir mensajes y añadirlos a la cola
			message, addr = server.recvfrom(1024)
			messages.put((message, addr))

		except:
			# Si hay un error al recibir el mensaje, se ignora
			pass

# --------------------------------------------------------------------------
# Funcion para mandar mensajes
# --------------------------------------------------------------------------
def broadcast():
	while True:
		# Cuando la cola tiene mensajes se hace lo siguiente:
		while not messages.empty():
			# Tomar los mensajes y decodificarlos
			message, addr = messages.get()
			print(message.decode())
			# Si el cliente no está registrado, se registra en la lista de clientes
			# del servidor
			if addr not in clients:
				clients.append(addr)

			# Para no reenviar el mensaje del cliente a el mismo
			# se inicializa al remitente y se omite el envío para éste.
			sender = addr

			# Mandar el mensaje
			for client in clients:
				try:
					# Omitir envío al sender
					if client == sender:
						continue  
					# Si el mensaje empieza con "SIGNUP_TAG" el usuario está especificando su alias
					if message.decode().startswith("SIGNUP_TAG:"):
						alias = message.decode()[message.decode().index(":")+1:]
						# Indicar que un nuevo cliente se unió al chat
						server.sendto(f"---{alias} joined!---".encode(), client)
					# De otro modo se envía en mesaje a todos los clientes
					else:
						server.sendto(message,client)
				# Si ocurre un error al enviar el mensaje, se elimina al cliente de la lista
				except:
					clients.remove(client)

# Declarar e inicializar los hilos para enviar y recibir mensajes
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()






