import requests
import json
import time
import math
from requests.structures import CaseInsensitiveDict

base = "http://127.0.0.1:5000/"
n=1.0

def update_data(d):
    #response = requests.post(base + "Data/Update", json={"datenpunkt": d})
    headers = {"Content-Type": "application/json"}
    data = {"datenpunkt":d}
    response = requests.post(base + "Data/Update", json=data, headers=headers)
    return response.json()

def get_data():
    response = requests.get(base + "Data")
    return response.json()

while 1:
    value = (math.sin(n)+1)*5000
    
    time.sleep(1)
    print("Gesendet:\n" + json.dumps(update_data(value)) + "\n")
    print("Abgefragt:\n" + json.dumps(get_data(), indent = 4))
    n += 0.1