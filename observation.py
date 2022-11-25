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


# Función de construcción de concepto codificable
def concepto_codif(codigo:str, glosa:str, sistema:str="http://loinc.org") -> CodeableConcept:
    """
    Construye un concepto codificable. Sistema por defecto es LOINC
    """

    concepto = CodeableConcept.construct()
    concepto.coding = list()
    cod = Coding.construct()
    cod.system = sistema
    cod.code = codigo
    cod.display = glosa
    concepto.coding.append(cod)

    return concepto


# Función de inserción de observación
def inserta_observacion(paciente:Reference, codigo:CodeableConcept, cantidad:Quantity, tiempo:datetime=datetime.now()):
    """
    Inserta una nueva observación
    """

    # Construcción de la observación
    obs = Observation.construct(status="final")
    obs.subject = paciente
    obs.code = codigo
    obs.valueQuantity = cantidad
    obs.effectiveDateTime = tiempo

    print(obs.json())

    r = requests.post(f"{conf.url_base}/Observation",
        data=obs.json(),
        auth=HTTPBasicAuth(conf.usuario, conf.password),
        headers={"Content-Type": "application/fhir+json"})

    print(f"STATUS: {r.status_code}")
    print("RESPUESTA:")
    print(r.text)


# Referencia al paciente
paciente = Reference.construct()
paciente.type = "Patient"
paciente.reference = "/Patient/2655"

# Cantidad / valor de la observación
cant = Quantity.construct()
cant.value = "88.5"
cant.unit = "kg"

inserta_observacion(paciente, concepto_codif("29463-7", "Peso"), cant)

# Cantidad / valor de la observación
cant = Quantity.construct()
cant.value = "195"
cant.unit = "cm"

inserta_observacion(paciente, concepto_codif("8302-2", "Talla"), cant)
