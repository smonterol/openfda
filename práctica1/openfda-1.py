import json
import http.client

headers = {'User-Agent': 'http-client'}  #diccionario con clave-valor

conn = http.client.HTTPSConnection("api.fda.gov") #establecemos conexion con el servidor

# -- Enviar un mensaje de solicitud
conn.request("GET","/drug/label.json", None, headers)
# -- Leer el mensaje de respuesta recibido del servidor
r1 = conn.getresponse()
# -- Imprimir la linea de estado de la respuesta
print(r1.status, r1.reason)
# -- Leer el contenido de la respuesta y converirlo a una cadena
repos_raw = r1.read().decode("utf-8")

conn.close()


repos = json.loads(repos_raw)
info_productos=repos['results'][0]
#Obtenemos la id,el proposito y el nombre del fabricante

try:
    print("La id del producto es: ", info_productos['id'])
    print("El proposito del producto es: ",info_productos['purpose'][0])
    print("El nombre del fabricante es: ", info_productos['openfda']['manufacturer_name'][0])

except KeyError:
        print("No se encontraron resultados, por favor introduzca una clave válida")
        continue