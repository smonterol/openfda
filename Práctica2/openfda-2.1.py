import http.client

import json

headers = {'User-Agent': 'http-client'}

n = 0

while True:
    conn = http.client.HTTPSConnection("api.fda.gov")  #establecemos conexion con el servidor

    conn.request("GET","/drug/label.json?limit=100&skip="+str(n)+"&search=substance_name:%22ASPIRIN%22", None, headers)

    r1 = conn.getresponse() #respuesta
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")

    conn.close()

    repos = json.loads(repos_raw)
    l_results= len(repos['results'])

    for i in range(l_results):
        print("La id del producto es: ", repos['results'][i]['id'])
        print("El nombre del fabricante es: ", repos['results']['openfda']['manufacturer_name'])

    if l_results <100:
        break


