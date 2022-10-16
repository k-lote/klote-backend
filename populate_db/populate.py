import requests
import random

url = "http://localhost:5000"

allotments_ids = []
user_ids = []
customer_ids = []
lots = []

def get_allotments_ids():
    response = requests.get(url + "/allotment/get_allotments")
    allotments = response.json()["data"]
    for allotment in allotments:
        allotments_ids.append(allotment["id"])

def get_user_ids():
    response = requests.get(url + "/user/get_users")
    users = response.json()["data"]
    for user in users:
        user_ids.append(user["user_id"])
    

def get_customer_ids():
    response = requests.get(url + "/customer/get_customers")
    customers = response.json()["data"]
    for customer in customers:
        customer_ids.append(customer["id"])

def get_lots():
    response = requests.get(url + "/lot/get_lots")
    lots_query = response.json()["data"]
    for lot in lots_query:
        lots.append([lot['allotment_id'], lot['number']])

def populate_allotments(qtd=1):
    get_user_ids()
    allotments_names = ["Nova Esperança", "Villa Lobos", "Jardim Girassol",
                        "Jardim das Flores", "Jardim das Margaridas", "Jardim das Rosas"]
    for i in range(qtd):
        allotment = {
            "name": "Loteamento " + allotments_names[random.randint(0, len(allotments_names) - 1)] + " " + str(random.randint(0, 10)),
            "cep": random.randint(54000000, 54999999),
            "address": "Rua " + str(random.randint(0, 100)) + ", " + str(random.randint(0, 1000)),
            "img_url": "",
            "users_access": random.sample(user_ids, 3)
        }

        requests.post(url + "/allotment/register", json=allotment)


def populate_lot(qtd=1):
    get_allotments_ids()
    for i in range(qtd):
        lot = {
            "allotment_id": random.choice(allotments_ids),
            "block": random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]),
            "value": random.randint(100000, 1000000)
        }

        requests.post(url + "/lot/register", json=lot)
    

def populate_costumers(qtd=1):
    get_user_ids()
    for i in range(qtd):
        customer = {
            "name": "Cliente " + str(random.randint(0, 100)),
            "phone1": random.randint(10000000000, 99999999999),
            "email": "cliente" + str(random.randint(0, 100)) + "@gmail.com",
            "address": "Rua " + str(random.randint(0, 100)) + ", " + str(random.randint(0, 1000)),
            "admin_id": random.choice(user_ids)
        }
        if random.randint(0, 1) == 0:
            customer["cpf"] = random.randint(10000000000, 99999999999)
        else:
            customer["cnpj"] = random.randint(10000000000000, 99999999999999)
            customer["company_name"] = "Empresa " + str(random.randint(1, 100))

        print(customer)

        requests.post(url + "/customer/register", json=customer)

def populate_purcharse(qtd):
    get_lots()
    get_customer_ids()
    for i in range(qtd):
        lot = random.choice(lots)
        purchase = {
            "customer_id": random.choice(customer_ids),
            "allotment_id": lot[0],
            "lot_number": lot[1]
        }

        requests.post(url + "/customer/purchase/register", json=purchase)
        
def populate_installments(qtd):
    get_lots()
    get_customer_ids()
    for i in range(qtd):
        lot = random.choice(lots)
        value = random.randint(1000, 10000)
        installment_qtd = random.randint(1, 20)
        
        installment = {
            "value": value,
            "date": "2021-01-01",
            "allottment_id": lot[0],
            "number": lot[1],
            "installment_qtd": installment_qtd,
        }

        requests.post(url + "/finances/installment/register", json=installment)

if __name__ == "__main__":
    menu = """
    1 - Popular loteamentos
    2 - Popular lotes
    3 - Popular clientes
    4 - Popular compras
    5 - Popular parcelas

    0 - Sair

    Opção: 
    """
    print(menu)
    option = int(input("Digite a opção desejada: "))
    if option == 1:
        qtd = int(input("Digite a quantidade de loteamentos: "))
        populate_allotments(qtd)
    elif option == 2:
        qtd = int(input("Digite a quantidade de lotes: "))
        populate_lot(qtd)
    elif option == 3:
        qtd = int(input("Digite a quantidade de clientes: "))
        populate_costumers(qtd)
    elif option == 4:
        qtd = int(input("Digite a quantidade de compras: "))
        populate_purcharse(qtd)
    elif option == 5:
        qtd = int(input("Digite a quantidade de parcelas: "))
        populate_installments(qtd)
    elif option == 0:
        exit()
    else:
        print("Opção inválida!")
