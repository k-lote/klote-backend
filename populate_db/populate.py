import requests
import json 
import random

url = "http://localhost:5000"

allotments_ids = [100010, 100011, 100012, 100013, 100014, 100015, 100016, 100017, 100018, 100019, 100020, 100021, 100022, 100023, 100024, 100025, 100026]
user_ids = [3, 100001, 100002, 100003, 100006, 100007, 100008, 100009, 100010, 100011, 100012, 100013, 100014]
def get_allotments_ids():
    response = requests.get(url + "/allotment/get_allotments")
    allotments = response.json()["data"]
    allotments_ids = []
    for allotment in allotments:
        allotments_ids.append(allotment["id"])
    
    print(allotments_ids)

def get_user_ids():
    response = requests.get(url + "/user/get_users")
    users = response.json()["data"]
    for user in users:
        user_ids.append(user["user_id"])
    
    print(user_ids)

def populate_allotments():
    allotments_names = ["Nova Esperança", "Villa Lobos", "Jardim Girassol",
                        "Jardim das Flores", "Jardim das Margaridas", "Jardim das Rosas"]
    for i in range(3):
        allotment = {
            "name": "Loteamento " + allotments_names[random.randint(0, len(allotments_names) - 1)] + " " + str(random.randint(0, 10)),
            "cep": random.randint(54000000, 54999999),
            "address": "Rua " + str(random.randint(0, 100)) + ", " + str(random.randint(0, 1000)),
            "img_url": "",
            "users_access": random.sample(user_ids, 3)
        }

        requests.post(url + "/allotment/register", json=allotment)


def populate_lot():
    for i in range(1):
        lot = {
            "allotment_id": random.choice(allotments_ids),
            "block": random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]),
            "value": random.randint(100000, 1000000),
        }

        requests.post(url + "/lot/register", json=lot)
    

def populate_costumers():
    pass

#get_allotments_ids()
#get_user_ids()
#populate_allotments()
populate_lot()