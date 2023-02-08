#Programa para los clientes
import threading
import socket
# definir un alias
alias = input('Ingresa tu alias: ')
# crear el objeto cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conectar el cliente a la direccion local y a un puerto disponible
client.connect(('127.0.0.1', 65123))

# funcion para recibir mensajes de otros clientes a traves del servidor
def client_receive():
	while True:
		try:
			# encode para mandar, decode para recibir
			message = client.recv(1024).decode('utf-8')
			if message == "alias?":
				# mandar el alias
				client.send(alias.encode('utf-8'))
			else:
				# This is a message from another client
				if(("Ahora ya estas conectado!" in message) or ("se ha conectado al chat" in message)):
					print(message)
					
				else:
					print("\t\t\t\t" + message)
		except:
			# indicar si hay un error
			print('Error!')
			# indicar si hay un error
			client.close()
			break

# funcion para mandar mensajes de otros clientes a traves del servidor
def client_send():
    while True:
        # funcion para mandar mensajes de otros clientes a traves del servidor
        message = f'{input("")}'
        # mandar el mensaje
        client.send(message.encode('utf-8'))
        
# mandar el mensaje
receive_thread = threading.Thread(target=client_receive)
# mandar el mensaje
receive_thread.start()
# mandar el mensaje
send_thread = threading.Thread(target=client_send)

send_thread.start()
