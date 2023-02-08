import math

def reenviar_paq_perdidos(lista_paq_perdidos, lista_paq):
    #convertir a arreglo
    cadena = lista_paq_perdidos[0][0]
    arreglo = list(map(int, cadena.split("/")))
    port_client = lista_paq_perdidos[0][1]
    cliente = str(port_client)

    # return arreglo
    for i in arreglo:
        mensaje = lista_paq[i]

        # quitar el destinatario
        mensaje = mensaje[20:]
        paquete = cliente + mensaje

        # Enviar paquete
        client.sendto(paquete.encode(), (HOST,PORT))

# --------------------------------------------------------------------------- #

def solicitud_confirmacion(dest, remit):
    # -----Contenido----------------------------------------------
    # Destinatario: Todos
    # Remitente: HOST + PUERTO
    # Tipo de paquete: Control ("1")
    # Tipo de mensaje de control: Solicitud de confirmación ("1")
    # ------------------------------------------------------------
    solicitud = dest + remit + "1" + "1"

    # Se envía solicitud al servidor
    client.sendto(solicitud.encode(), (HOST,PORT))

    while(espera_conf == 1):
        pass # Se ejecutará mientras no se reciba confimacion.

    # Si llegaron todos los paquetes sigue con el siguiente.
    if modo_reenvio == 0:
        cont_paq = 0
        list_paq = [0,0,0,0,0,0,0,0,0,0]
        return

    # Si faltaron paquetes pidelos y vuelve a verificar
    else:
        while(modo_reenvio == 1):
            reenviar_paq_perdidos(lista_paq_perdidos, lista_paq)
            solicitud_confirmacion(dest, remit)

# --------------------------------------------------------------------------- #
#
# Recibe un paquete y lo empaqueta agregandole:
# Destinatario: TODOS
# Remitente: HOST + PUERTO
# Tipo de paquete: Mensaje ("0")
# Número del paquete. Ej: 1/10
# Fragmento del mensaje (980 caracteres)
#
# --------------------------------
def empaquetar(mensaje, port_client):
    long = len(mensaje)
    num_paq = math.ceil(long/980)

    inicio = 0
    cont_paq = 0
    list_paq = [0,0,0,0,0,0,0,0,0,0]

    # Destinatario por default: TODOS
    dest = "all                 " # 20 espacios

    # Remitente: HOST + PUERTO
    space = "               " # para rellenar al host y acompletar 15
    remit =  port_client[0] + space[(len(port_client[0])):] + port_client[1]

    # Empaquetado
    for cont_paq in range(0,num_paq):

        # Extensión del paquete
        fin = inicio + 980

        # Encabezado del paquete
        header = dest + remit + "0" + str(cont_paq) + "/9"

        # Paquete empaquetado
        paq = header + mensaje[inicio:fin]

        # Se modifica el inicio para el nuevo paquete
        inicio = fin
        
        # Enviar paquetes
        client.sendto(paq.encode(), (HOST,PORT))

        # Respaldar paquetes
        list_paq[i] = paq
        
        if cont_paq == 9:
            solicitud_confirmacion(dest, remit)
        
    #print(list_paq) # BORRAR
    
# ---------------------------------------------- #
# 
# ---------------------------------------------- #
def desempaquetar()
	global cola_de_clientes
    global messages
    global dict_messages
	while not messages.empty():
		# Tomar los mensajes de la cola y decodificarlos
		message, addr = messages.get()
		message = message.decode()
		# Tomar header, mensaje, numero de paquete (index)
		header = message[0:24]
		message = [24:]
		index = header[21]
		
		# Registrar al cliente si no está registrado
		ip_cliente = header[0:15]
		ip_cliente = ip_cliente.replace(" ","")
		puerto_cliente = header[15:20]
		puerto_cliente = puerto_cliente.replace(" ", "")
		cliente = (ip_cliente,puerto_cliente)
		if client not in cola_de_clientes:
			total = header[23]
			cola_de_clientes[client] = (total)
		if client not in dict_messages:
			dict_messages[client] = [0,0,0,0,0,0,0,0,0,0]

		# Guardar mensaje en lista del cliente en diccionario
		dict_messages[addr][index] =  message
        
# ---------------------------------------------- #
# ---------------------------------------------- #
def checa_si_llegaron_todos_paq():
	global todos_enviados
    global lista_todos_paquetes_env
    global dict_messages
	# Si el remitente ya mandó 10 paquetes, se checa que todos hayan llegado
	if todos_enviados:
		control = str(1)
		confirmacion = str(1)
		no_llegaron = str(3)

		for client in lista_todos_paquetes_env:
			total = cola_de_clientes[client]
			paquetes_recibidos = dict_messages[client][0:total+1]
			# No llegaron todos
			if 0 in paquetes_recibidos:
				# Ver que paquetes faltan y formar una cadena "x/y/z..." 
				# donde x,y,z... son paquetes faltantes
				indices = []
				for i, elem in enumerate(lista):
					if elem == 0:
						indices.append(i)
				cadena_paq_falt = ""
				for i in indices:
					cadena_paq_falt = cadena_paq_falt + str(i) + "/"
                
				# Formar mensaje de confirmación de envío no exitoso
				paquete = client[0].ljust(15) + client[1].ljust(5) + HOST.ljust(15) + PORT_CLIENT.ljust(5) + control + no_llegaron + paquetes_faltantes
                
				# Mandar mensaje al otro extremo para que active el modo envío
				client.sendto(paquete, (HOST, PORT_CLIENT))
            # Si llegaron todos
			else:
				# Formar mensaje completo y desplegarlo
				mensaje_completo = ''
				for item in paquetes_recibidos:
					mensaje_completo = mensaje_completo + item
				# TODO: Opcional, imprimir 50 caracteres por linea
				print("\t\t\t\t" + mensaje_completo)

				# Mandar confirmación de envío
				paquete = client[0].ljust(15) + client[1].ljust(5) + HOST.ljust(15) + PORT_CLIENT.ljust(5) + control + confirmacion

				if modo_reenvio == 1 and lista_todos_paquetes_env[0] == client:
					# Remover cliente de la cola (lista)
					lista_todos_paquetes_env.remove(client)

					# Si la lista está vacía cambio modo reenvio
					if len(lista_todos_paquetes_env) == 0:
						modo_reenvio == 0:



# MAIN (BORRAR)
port_client = [("192.168.0.1"),("85000")]; # BORRAR
empaquetar('hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola ', port_client)
