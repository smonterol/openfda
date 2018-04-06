import http.client

import json

headers = {'User-Agent': 'http-client'}  #diccionario con clave-valor

conn = http.client.HTTPSConnection("api.fda.gov") #establecemos conexion con el servidor

conn.request("GET","/drug/label.json?search=active_ingredient:acetylsalicylic&limit=4", None, headers)

r1 = conn.getresponse()

print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")

conn.close()


repos = json.loads(repos_raw)

#Obtenemos la id,el proposito y el nombre del fabricante

print("La id del producto es: ", repos['results'][0]['id'])
print("El proposito del producto es: ",repos['results'][0]['purpose'])
print("El nombre del fabricante es: ", repos['results'][0]['openfda']['manufacturer_name'])
