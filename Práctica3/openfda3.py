import socket
import http.client

import json


PORT = 8117
IP = '192.168.0.13'
MAX_OPEN_REQUEST = 10


lista_m =[]
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")  # establecemos conexion con el servidor

conn.request("GET", "/drug/label.json?limit=10", None,headers)

r1 = conn.getresponse()
print(r1.status,r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
l_results = len(repos['results'])

for i in range(l_results):
    info_productos = repos['results'][i]

    if (info_productos['openfda']):
        print("El nombre del producto: ", info_productos['openfda']['generic_name'][0])
        lista_m.append(info_productos['openfda']['generic_name'][0])


def process_client(clientsocket):
    

    contenido="""<html>
      <body style='background-color: mediumaquamarine>
      <h1>Estos son tus 10 medicamentos:</h2>
      </body>
      </html>
    """
    for element in lista_m:
        contenido += element + "<br>"

    contenido += "</body></html>"

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()

# Creamos un socket para el servidor. Es por el que llegan las peticiones de los clientes.

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
# Asociar el socket a la direccion IP y puertos del servidor
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUEST)

    while True:

# Esperar a que lleguen conexiones del exterior. Cuando llega una conexion nueva, se obtiene un nuevo socket para
# comunicarnos con el cliente. Este sockets contiene la IP y Puerto del cliente
       print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
       (clientsocket, address) = serversocket.accept()
       # Procesamos la peticion del cliente, pasandole el socket como argumento
       process_client(clientsocket)


except socket.error:

#en caso de error conectandose al socket se lanzan los siguientes mensajes
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto y verifica la IP")











