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
def broadcast(message, client):
    for c in clients:
        if c != client:
            c.send(message) 

# Funcion para manejar las conexiones de cada cliente
def handle_client(client):
    # Get the index of the client in the client list
    index = clients.index(client)
    # Get the alias of the client
    alias = aliases[index].decode('utf-8')

    while True:
        try:
            # Receive message from client
            message = client.recv(1024).decode('utf-8')
            
            # Send message to all clients except the sender
            for i, c in enumerate(clients):
                if i != index:
                    c.send(f'{alias}: {message}'.encode('utf-8'))

        except:
            # Remove client and its alias from lists
            clients.remove(client)
            client.close()
            aliases.remove(alias)
            
            # Notify other clients that this client has left the chat
            broadcast(f'{alias} has left the chat!'.encode('utf-8'),client)
            break

# Main function to receive the clients connection
def receive():
    while True:
        print('\nEl servidor esta funcionando y escuchando...')
        client, address = server.accept()
        print(f'Conexion establecida con {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)        
        print(f'El alias de este cliente es "{alias.decode("utf-8")}"')

        #broadcast(f'{alias.decode("utf-8")} se ha conectado al chat'.encode('utf-8'), client)
        message = f"{alias.decode('utf-8')} se ha conectado al chat"
        center_message = message.center(80).encode('utf-8')
        broadcast(center_message, client)

        
        #client.send('Ahora ya estas conectado!'.encode('utf-8'))
        message = "Ahora ya estas conectado!"
        center_message = message.center(80).encode('utf-8')
        client.send(center_message)
        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
