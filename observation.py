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
from datetime import datetime


# Función de inserción de observación
def inserta_observacion(paciente:Reference, codigo:CodeableConcept, cantidad:Quantity, tiempo:datetime=None):
    """
    Inserta una nueva observación
    """

    # Fecha y hora de la observación
    tiempo_obs = datetime.now() if tiempo is None else tiempo

    # Construcción de la observación
    obs = Observation.construct(status="final")
    obs.subject = paciente
    obs.code = codigo
    obs.valueQuantity = cantidad
    obs.effectiveDateTime = tiempo_obs

    print(obs.json())

    r = requests.post(f"{conf.url_base}/Observation",
        data=obs.json(),
        #json=obs.dict(),
        auth=HTTPBasicAuth(conf.usuario, conf.password),
        headers={"Content-Type": "application/fhir+json"})

    print(f"STATUS: {r.status_code}")
    print("RESPUESTA:")
    print(r.text)


# Referencia al paciente
paciente = Reference.construct()
paciente.type = "Patient"
paciente.reference = "/Patient/2655"

# Concepto codificable: peso
codigo_peso = CodeableConcept.construct()
codigo_peso.coding = list()
cod = Coding.construct()
cod.system = "http://loinc.org"
cod.code = "29463-7"
cod.display = "Peso"
codigo_peso.coding.append(cod)

# Concepto codificable: talla
codigo_talla = CodeableConcept.construct()
codigo_talla.coding = list()
cod = Coding.construct()
cod.system = "http://loinc.org"
cod.code = "8302-2"
cod.display = "Talla"
codigo_talla.coding.append(cod)

# Cantidad / valor de la observación
cant = Quantity.construct()
cant.value = "87.2"
cant.unit = "kg"

inserta_observacion(paciente, codigo_peso, cant)

# Cantidad / valor de la observación
cant = Quantity.construct()
cant.value = "194"
cant.unit = "cm"

inserta_observacion(paciente, codigo_talla, cant)
