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


# MAIN (BORRAR)
port_client = [("192.168.0.1"),("85000")]; # BORRAR
empaquetar('hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola hola ', port_client)
