#! /usr/bin/python3
# Encoding: UTF-8

import requests
from requests.auth import HTTPBasicAuth
from config import Configuracion as conf

r = requests.get(f"{conf.url_base}/Observation",
    params={
        "subject": "Patient/2655"
    },
    auth=HTTPBasicAuth(conf.usuario, conf.password)
    )

print(f"STATUS: {r.status_code}")
print(r.text)
