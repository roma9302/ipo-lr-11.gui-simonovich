import json
from .function import *

class Client: 
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = validate_str(name)  
        self.cargo_weight = validate_number(cargo_weight)
        self.is_vip = is_vip
        self.client_id = generate()



        client_data = {
            "client": {  
                "name": self.name,
                "cargo_weight": self.cargo_weight,
                "is_vip": self.is_vip,
                "client_id" : self.client_id
            }
        }

        try:
            with open("transport/clients.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
                if "clients" not in data:
                    data = {"clients": []}
                    
        except Exception:
            data = {"clients": []}


        data["clients"].append(client_data)
        

        with open('transport/clients.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


