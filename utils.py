import json

def load_data_offers():
    with open('data/Offers.json',"r", encoding="utf-8") as f:
        offers = json.load(f)
        return offers

def load_data_orders():
    with open('data/Orders.json',"r", encoding="utf-8") as f:
        offers = json.load(f)
        return offers

def load_data_users():
    with open('data/Users.json',"r", encoding="utf-8") as f:
        offers = json.load(f)
        return offers

