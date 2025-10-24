from flask import Flask, request, Response, send_file
from lxml import etree

app = Flask(__name__)

# "Banco" de usuários
users = {1: "Alice", 2: "Bob"}

SOAP_ENVELOPE = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:urn="urn:userservice">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getUserResponse>
         <urn:name>{name}</urn:name>
      </urn:getUserResponse>
   </soapenv:Body>
</soapenv:Envelope>"""

@app.route("/soap", methods=["POST"])
def soap():
    xml = etree.fromstring(request.data)

    # Define o namespace
    ns = {"urn": "urn:userservice"}

    # Busca o userId
    user_id_node = xml.xpath("//urn:userId", namespaces=ns)
    if not user_id_node:
        name = "Missing userId"
    else:
        user_id = int(user_id_node[0].text)
        name = users.get(user_id, "User not found")

    response_xml = SOAP_ENVELOPE.format(name=name)
    return Response(response_xml, mimetype="text/xml")

# Endpoint para servir o WSDL
@app.route("/wsdl", methods=["GET"])
def wsdl():
    return send_file("users.wsdl", mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
