#! /usr/bin/python3
# Encoding: UTF-8

from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from datetime import date
import requests
from requests.auth import HTTPBasicAuth
from config import Configuracion as conf
from typing import List

def construye_paciente(nombres:List, apellidos:str, rut_param:str, ppn_param:str, estado_civil_param:str, fecha_nacimiento:date, sexo:str) -> Patient:
    """
    Construye y devuelve un recurso paciente, a partir de los parámetros pasados
    """

    pat = Patient.construct()
    nombre = HumanName.construct()

    nombre.family = apellidos
    nombre.given = list()
    nombre.given = nombres
    nombre.text = f"{' '.join(nombre.given)} {nombre.family}"

    # RUT codificado
    concepto = CodeableConcept.construct()
    concepto.coding = list()
    cod = Coding.construct()
    cod.system = "https://registrocivil.gob.cl"
    cod.code = "RUN"
    cod.display = "Rol Único Nacional"
    concepto.coding.append(cod)

    rut = Identifier.construct()
    rut.use = "official"
    rut.type = concepto
    rut.type.text = "RUN"
    rut.system = "https://registrocivil.gob.cl"
    rut.value = rut_param

    # PPN codificado
    concepto = CodeableConcept.construct()
    concepto.coding = list()
    cod = Coding.construct()
    cod.system = "https://clinicaalemana.cl"
    cod.code = "PPN"
    cod.display = "PPN (Identificador Clientes CAS)"
    concepto.coding.append(cod)

    ppn = Identifier.construct()
    ppn.use = "official"
    ppn.type = concepto
    ppn.type.text = "PPN"
    ppn.system = "https://clinicaalemana.cl"
    ppn.value = ppn_param

    # Estado civil. La letra de código es lo que usa internamente Clientes
    estados = {
        "T": {
            "code": "20295000",
            "display": "Divorced (finding)",
            "text": "Divorciado(a)"
        },
        "C": {
            "code": "87915002",
            "display": "Married (finding)",
            "text": "Casado(a)"
        },
        "S": {
            "code": "55876004",
            "display": "Bachelor (finding)",
            "text": "Soltero(a)"
        },
        "V": {
            "code": "33553000",
            "display": "Widowed (finding)",
            "text": "Viudo(a)"
        },
        "J": {
            "code": "276125006",
            "display": "Separated from cohabitee (finding)",
            "text": "Separado(a)"
        },
        "U": {
            "code": "14012001",
            "display": "Common law partnership (finding)",
            "text": "Conviviente Civil"
        },
        "X": {
            "code": "160504008",
            "display": "Marital state unknown (finding)",
            "text": "Sin información"
        }
    }

    estado_civil = CodeableConcept.construct()
    estado_civil.coding = list()
    cod = Coding.construct()
    cod.system = "http://snomed.info/sct"
    cod.code = estados[estado_civil_param]["code"]
    cod.display = estados[estado_civil_param]["display"]
    estado_civil.coding.append(cod)
    estado_civil.text = estados[estado_civil_param]["text"]

    # Construcción del paciente
    pat.identifier = [rut, ppn]
    pat.birthDate = fecha_nacimiento    #date(year=2011, month=11, day=27)
    pat.name = [nombre]
    pat.gender=sexo
    pat.maritalStatus = estado_civil

    return pat


# PUNTO DE ENTRADA

pat = construye_paciente(["Jaime", "Ignacio"], "de los Hoyos Moreno", "13549728-2", "7204913", "C", date(year=1979, month=6, day=2), "male")
print(pat.json())
print("----------------------")

pat = construye_paciente(["Antonia", "Emilia"], "de los Hoyos Leal", "23272864-7", "6304355", "S", date(year=2010, month=3, day=16), "female")
print(pat.json())
print("----------------------")

pat = construye_paciente(["Catalina", "Montserrat"], "de los Hoyos Leal", "23808281-1", "6304356", "S", date(year=2012, month=11, day=27), "female")
print(pat.json())
print("----------------------")

#r = requests.post(f"{conf.url_base}/Patient",
#    data=pat.json(),
#    #json=obs.dict(),
#    auth=HTTPBasicAuth(conf.usuario, conf.password),
#    headers={"Content-Type": "application/fhir+json"})
#
#print(f"STATUS: {r.status_code}")
#print("RESPUESTA:")
#print(r.text)
