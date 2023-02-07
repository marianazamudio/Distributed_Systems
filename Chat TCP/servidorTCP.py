# Programa para el servidor
'Chat Room Connection - Client-To-Client'
import threading
import socket

# Definir direccion IP y puerto
host = '127.0.0.1'
port = 65123

# crear un objeto servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
# activar el modo de escucha
server.listen()
# crear lista para los clientes
clients = []
# crear lista para los alias
aliases = []

# Funcion para mandar un mensaje del servidor a todos los clientes connectados
# esta funcion va a iterar entre la lista de clientes para mandar el mensaje
def broadcast(message):
    for client in clients:
        client.send(message)

# Funcion para manejar las conexiones de cada cliente
def handle_client(client):
    while True:
        try:
            # mensaje recibido del cliente
            # cantidad maxima de bytes que el servidor puede recibir del cliente = 1024
            message = client.recv(1024)
            # mandar el mensaje
            broadcast(message)
        except:
            # en caso de un error en la conexion
            # se identifica el cliente con el error para quitarlo de la lista de clientes
            # index busca en la tupla un valor especifico y devuelve la posicion donde se
            # se encontro, en este caso, donde se encontro el cliente
            index = clients.index(client)
            # elimimnar el cliente que devolvio index
            clients.remove(client)
            # cerrar la conexion con el cliente
            client.close()
            # se identifica el alias del cliente
            alias = aliases[index]
            # La función encode con el argumento 'utf-8' codifica un objeto de tipo string
            # en formato UTF-8. UTF-8 es una codificación de caracteres que permite
            # representar una amplia gama de caracteres internacionales
            # convierte los mensajes de tipo string en bytes
            # mandamos un mensaje para indicar quien dejo el chat
            broadcast(f'{alias} ha abandonado el chat!'.encode('utf-8'))
            # eliminar el alias de la lista aliases
            aliases.remove(alias)
            break

# Funcion para recibir la conexion de los clientes
def receive():
    while True:
        # se empieza indicando que el servidor ya esta corriendo
        print('El servidor esta funcionando y escuchando...')
        # hacer que el servidor acepte cualquier conexion entrante
        # se propociona el cliente y la direccion de la conexion
        # .accept se mantiene corriendo en la espera de una conexion nueva, y regresa un
        # socket que representa la conexion y la direccion del cliente
        client, address = server.accept()
        print(f'Conexion establecida con {str(address)}')
        # enviar un mensaje al cliente para preguntarle su alias
        client.send('alias?'.encode('utf-8'))
        # guardar la respuesta del cliente
        alias = client.recv(1024)
        # agregar el alias a la lista
        aliases.append(alias)
        # agregar el cliente a la lista
        clients.append(client)
        print(f'El alias de este cliente es {alias}'.encode('utf-8'))
        # indicar a los demas clientes de la nueva conexion
        broadcast(f'{alias} se ha conectado al chat'.encode('utf-8'))
        # informarle al cliente que ya esta conectado
        client.send('Ahora ya estas conectado!'.encode('utf-8'))
        # crear el hilo
        # llamar a la funcion handle_client se debe hacer a traves de un hilo
        # se debe tener un hilo por cada cliente conectado
        # crear un hilo en el módulo de threading, con la función "handle_client"
        # target y con el argumento "client"
        # este hilo se usa para ejecutar "handle_client" en paralelo con otras tareas
        thread = threading.Thread(target=handle_client, args=(client,))
        # iniciar el hilo
        thread.start()


if __name__ == "__main__":
    receive()
