import requests
import json 

url = "http://localhost:5000"
data = "data.json"

allotments_ids = []
def get_allotments_ids():
    response = requests.get(url + "/allotment/get_allotments")
    allotments = response.json()["data"]
    for allotment in allotments:
        allotments_ids.append(allotment["id"])
    with open(data, "r") as f:
        test =json.load(f)
        print(test)
        #f.write(json.dumps(allotments_ids), )
    
    #for allotment in allotments:
    #    allotments_ids.append(allotment["id"])

def populate_allotments():
    allotments = [
        {
            "name": "Loteamento Nova Esperança",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 2",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 3",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 4",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 5",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 6",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 7",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {   
            "name": "Loteamento Nova Esperança 8",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 9",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        },
        {
            "name": "Loteamento Nova Esperança 10",
            "cep": "12345678",
            "address": "Rua Nova Esperança, 123",
            "img_url": "",
            "users_access": [100001,100006]
        }
    ]
    

    for allotment in allotments:
        response = requests.post(url + "/allotment/register", json=allotment)

def populate_allotment_access():
    pass

def populate_costumers():
    pass

get_allotments_ids()
#populate_allotments()