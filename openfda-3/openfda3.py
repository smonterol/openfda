import socketserver
import http.client
import json
import http.server


PORT = 8123
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


    # HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
        # GET
        def do_GET(self):
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()


            contenido="""<html>
            <body style='background-color: mediumaquamarine>
            <h1>Estos son tus 10 medicamentos:</h2>
            </body>
            </html>
            """
            for element in lista_m:
                contenido += element + "<br>"

            contenido += "</body></html>"
            self.wfile.write(bytes(contenido, "utf8"))
            return
#El servidor comienza aqui
#objeto de nuestra clase definida anteriormente
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
















