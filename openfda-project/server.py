import socketserver
import http.server
import http.client
import json  # para trabajar con los ficheros recibidps de openfda

PORT = 8000  # siempre usamos el puerto 8000


# Utilizamos la misma clase que en la práctica anterior, una clase derivada de BaseHTTPRequestHandler

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # Parametros de configuración

    SERVER_NAME = "api.fda.gov"
    RESOURCE_NAME = "/drug/label.json"
    DRUG_openfda = '&search=active_ingredient:'
    COMPANY_openfda = '&search=openfda.manufacturer_name:'

    def pagina_inicio(self):  # funcion para controlar el hmtl de nuestra pagina de inicio(principal)
        # este html contiene la estructurade nuestra pagina principal
        html = """   
            <html>
                <head>
                    <title> OpenFDA</title>
                </head>
                <body align=center>

                    <h1>Drug product labelling OpenFDA </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>

                    <br>
                    <br>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <br>
                    <br>

                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    <br>
                    <br>

                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <br>
                    <br>

                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html

    def pagina_2(self, lista):  # esta funcion trabajará con los elementos introducidos en los inputs anteriores
        datos_html = """
                                <html>
                                    <head>
                                        <title>Sara´s App</title>   
                                    </head>
                                    <body style='background-color: lightblue'>
                                        <ul>
                            """
        for i in lista:  # utilizamos un bucle for para iterar sobre los datos obtenidos anterirormente y los almacenamos
            datos_html += "<li>" + i + "</li>"

        datos_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return datos_html

    def resultados(self, limit=10):  # estableecemos el limite en 10
        conn = http.client.HTTPSConnection(self.SERVER_NAME)  # establecemos conexion
        conn.request("GET", self.RESOURCE_NAME + "?limit=" + str(limit))  # enviamos mensaje de solicitud
        print(self.RESOURCE_NAME + "?limit=" + str(limit))
        r1 = conn.getresponse()  # obtenemos la respuesta de servidor
        data_raw = r1.read().decode("utf8")  # Leer el contenido en json, y transformarlo en una cadena
        data = json.loads(data_raw)  # procesamos el contenido json
        resultados = data['results']
        return resultados

    def do_GET(self):
        lista_recursos = self.path.split("?")
        if len(lista_recursos) > 1:
            parametros = lista_recursos[1]
        else:
            parametros = ""

        limit = 1

        # obtenemos las partes de nuestro recurso
        if parametros:
            partes = parametros.split("=")
            if partes[0] == "limit":
                limit = int(partes[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")

        # Aquí trabajamos con los datos introducidos en los inputs
        if self.path == '/':

            self.send_response(200)  # envia respuesta con el estado

            self.send_header('Content-type', 'text/html')  # envia los headers
            self.end_headers()
            html = self.pagina_inicio()
            self.wfile.write(bytes(html, "utf8"))

        elif 'listDrugs' in self.path:  # entramos aqui si elegimos la opción 'listDrugs'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            drugs = []
            resultados = self.resultados(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    drugs.append(resultado['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')
            resultado_html = self.pagina_2(drugs)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listCompanies' in self.path:  # entramos aqui si elegimos la opcion 'listCompanies'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []
            resultados = self.resultados(limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies.append(resultado['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocido')
            resultado_html = self.pagina_2(companies)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listWarnings' in self.path:  # entramos aqui si elegimos la opcion 'listWarnings'

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []
            resultados = self.resultados(limit)
            for resultado in resultados:  # introducimos nuestros resultados en una lista
                if ('warnings' in resultado):
                    warnings.append(resultado['warnings'][0])
                else:
                    warnings.append('Desconocido')
            resultado_html = self.pagina_2(warnings)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'searchDrug' in self.path:  # Esta opción es algo más compleja porque buscamos un medicamento especifico dentro del buscador

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Por defecto 10 en este caso, no 1
            limit = 10
            drug = self.path.split('=')[1]

            medicamentos = []
            conn = http.client.HTTPSConnection(self.SERVER_NAME)  # establecemos conexion con el servidor
            conn.request("GET", self.RESOURCE_NAME + "?limit=" + str(limit) + self.DRUG_openfda + drug)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            events_search_drug = biblioteca_data['results']
            for resultado in events_search_drug:
                if ('generic_name' in resultado['openfda']):
                    medicamentos.append(resultado['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Desconocido')

            resultado_html = self.pagina_2(medicamentos)
            self.wfile.write(bytes(resultado_html, "utf8"))


        elif 'searchCompany' in self.path:  # Esta opción tambien es algo mas compleja, trabaja como la anterior pero con las compañias

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            company = self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection(self.SERVER_NAME)
            conn.request("GET", self.RESOURCE_NAME + "?limit=" + str(limit) + self.COMPANY_openfda + company)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_company = json.loads(data)
            search_company = biblioteca_company['results']

            for search in search_company:
                companies.append(search['openfda']['manufacturer_name'][0])
            resultado_html = self.pagina_2(companies)
            self.wfile.write(bytes(resultado_html, "utf8"))

        # Aquí comenzamos algunas extensiones

        elif 'redirect' in self.path:
            print('Redirección  a  página principal')
            self.send_response(301)
            self.send_header('Location', 'http://localhost:' + str(PORT))
            self.end_headers()

        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        else:  # Si el recurso solicitado no se encuentra en el servidor.
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("ERROR 404, NOT FOUND '{}'.".format(self.path).encode())
        return


socketserver.TCPServer.allow_reuse_address = True  # reutilizamos el puerto sin necesidad de cambiarlo
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

httpd.serve_forever()