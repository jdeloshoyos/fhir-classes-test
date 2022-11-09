#! /usr/bin/python3
# Encoding: UTF-8

from fhir.resources.observation import Observation
from fhir.resources.reference import Reference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
import requests
from requests.auth import HTTPBasicAuth
from config import Configuracion as conf

# Referencia al paciente
paciente = Reference.construct()
paciente.type = "Patient"
paciente.reference = "/Patient/2655"

# Concepto codificable: peso
#codigo = CodeableConcept.construct()
#codigo.coding = list()
#cod = Coding.construct()
#cod.system = "http://loinc.org"
#cod.code = "29463-7"
#cod.display = "Peso"
#codigo.coding.append(cod)

# Concepto codificable: estatura
codigo = CodeableConcept.construct()
codigo.coding = list()
cod = Coding.construct()
cod.system = "http://loinc.org"
cod.code = "8302-2"
cod.display = "Estatura"
codigo.coding.append(cod)

# Cantidad / valor de la observación
cant = Quantity.construct()
cant.value = "193"
cant.unit = "cm"

# Construcción de la observación
obs = Observation.construct(status="final")
obs.subject = paciente
obs.code = codigo
obs.valueQuantity = cant

print(obs.json())

r = requests.post(f"{conf.url_base}/Observation",
    data=obs.json(),
    #json=obs.dict(),
    auth=HTTPBasicAuth(conf.usuario, conf.password),
    headers={"Content-Type": "application/fhir+json"})

print(f"STATUS: {r.status_code}")
print("RESPUESTA:")
print(r.text)
