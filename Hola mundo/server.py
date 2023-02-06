# -*- coding: utf-8 -*-
"""
Programa que hace un "Hola Mundo" por medio de sockets
está es la versión del servidor
"""
import socket 
HOST = "localhost"   # Direccion de loopback (Este programa se comunica con el propio equipo)
PORT = 65123         # Puerto de escucha (Puertos > 1023 están liberados)

# Bloque with para abrir socket
                   # IPv4          # TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(socket.gethostbyname(socket.gethostname()))
    # Asociar host y puerto a un socket
    s.bind((HOST, PORT))
    # Poner socket en modo escucha
    s.listen()
    # Se queda esperando, y devuleve el socket del cliente
    # conn --> socket del cliente, addr --> direccion del cliente
    conn, addr = s.accept()
    
    # Lo que llegue al servidor, se lo devuelvo al cliente
    with conn:
        print(f"Conectado a {addr}:")
        # While recibe los datos
        while True:
            data = conn.recv(1024)  # Valor estándar
            if not data:
                break
            # Envio de vuelta todo lo que me llega del cliete
            conn.sendall(data)
                        
        
