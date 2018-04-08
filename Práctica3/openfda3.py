import http.server
import socketserver
import http.client
import json

#puerto desde  donde se lanza el servidor

PORT = 8081


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





#clase derivada de BaseHttpRequestHandler
#Hereda todos los metodos de esta clase
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
#Get, este metodo se invoca automaticamente cada vez que
#hay una peticion Get por Http. El recurso solicitado se encunetra en self.path
     def do_GET(self):
         #La primera linea es la del status, indicamos que OK
         self.send_response(200)
         #En las siguientes lineas de la respuesta
         #colocamos las cabeceras necesarias para que
         #el cliente entienda el contenido que le enviamos(HTML)

         self.send_header('Content-type','text/html')
         self.end_headers()

         # Empezamos definiendo el contenido, porque necesitamos saber cuanto
         # ocupa para indicarlo en la cabecera
         # En este contenido pondremos el texto en HTML que queremos que se
         # visualice en el navegador cliente

         contenido="""<html>
      <body style='background-color: MEDIUMAQUAMARINE>
        <h1>Estos son tus 10 medicamentos:</h2>
      </body>
      </html>
    """



         for element in lista_m:

             contenido += element+ "<br>"

         contenido +="</body></html>"

         self.wfile.write(bytes(contenido ,"utf8"))
         return

 #El servidor comienza aqui
#Establecemos como mannejador nuestra propia clase
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("",PORT),Handler)
print("serving at port", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")







