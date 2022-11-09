#! /usr/bin/python3
# Encoding: UTF-8

from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from datetime import date

pat = Patient.construct()
nombre = HumanName.construct()

nombre.family = "de los Hoyos"
nombre.given = list()
nombre.given.append("Jaime")
nombre.given.append("Ignacio")

pat.id = "13549728-2"
pat.birthDate = date(year=1979, month=6, day=2)
pat.name = [nombre]
pat.gender="M"

print(pat.json())
