import http.client

import json

headers = {'User-Agent': 'http-client'}

n = 0

while True:
    conn = http.client.HTTPSConnection("api.fda.gov")  #establecemos conexion con el servidor

    conn.request("GET","/drug/label.json?limit=100&skip="+str(n)+"&search=substance_name:%22ASPIRIN%22", None, headers)