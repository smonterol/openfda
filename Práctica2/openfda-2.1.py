import http.client

import json

headers = {'User-Agent': 'http-client'}



while True:
    conn = http.client.HTTPSConnection("api.fda.gov")  #establecemos conexion con el servidor

    conn.request("GET","/drug/label.json?limit=100&skip="+'&search=active_ingredient:"acetylsalicylic"', None, headers)

    r1 = conn.getresponse() #respuesta
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")

    conn.close()

    repos = json.loads(repos_raw)
    l_results= len(repos['results'])

    try:

       for i in range(l_results):

           info_productos = repos['results'][i]
           print("La id del producto es: ", info_productos['id'])
           print("El nombre del fabricante es: ", info_productos['openfda']['manufacturer_name'][0])
           if l_results < 100:
               break
    except KeyError:
        print("Por favor introduzca una clave válida")
        continue




