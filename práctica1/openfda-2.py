import http.client

import json

headers = {'User-Agent': 'http-client'}  #diccionario con clave-valor

conn = http.client.HTTPSConnection("api.fda.gov") #establecemos conexion con el servidor

conn.request("GET","/drug/label.json?limit=10", None, headers)

r1 = conn.getresponse()

print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")

conn.close()

repos=json.loads(repos_raw)

for i in repos['results']:
    print('La id del producto es : ', i['id'])