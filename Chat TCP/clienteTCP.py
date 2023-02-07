#Programa para los clientes
import threading
import socket
# definir un alias
alias = input('Elige un alias >>> ')
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
                # recibir cualquier mensaje del servidor
                print(message)
        except:
            # indicar si hay un error
            print('Error!')
            # cerrar la conexion
            client.close()
            break

# funcion para mandar mensajes de otros clientes a traves del servidor
def client_send():
    while True:
        # el mensaje empieza con tu alias seguido del mensaje que quieres mandar
        message = f'{alias}: {input("")}'
        # mandar el mensaje
        client.send(message.encode('utf-8'))

# crear un hilo para client_receive
receive_thread = threading.Thread(target=client_receive)
# iniciar el hilo
receive_thread.start()
# crear un hilo para client_send
send_thread = threading.Thread(target=client_send)
# inicial el hilo
send_thread.start()
