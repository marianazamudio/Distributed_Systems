# -*- coding: utf-8 -*-
"""
Program that creates a simple "Hello world" using sockets
This script is for the client
"""

import socket
HOST = "192.168.1.73"  # IP del servidor
PORT = 65123        # Puerto de envio (puerto del servidor)

# Crear socket de cliente
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.sendall(b"Hola mundo")
    
    data = s.recv(1024)
    
print("Recibido", repr(data))
    