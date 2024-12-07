import json
from .function import *

class Client: 
    def __init__(self, name, cargo_weight, is_vip):
        self.name = validate_str(name)  
        self.cargo_weight = validate_number(cargo_weight)
        self.is_vip = is_vip
        self.client_id = generate()


        #словарь для записи в файл обьекта класса
        client_data = {
            "client": {  
                "name": self.name,
                "cargo_weight": self.cargo_weight,
                "is_vip": self.is_vip,
                "client_id" : self.client_id
            }
        }

        try:
            data = open_clients_load()
                
                #Если структуры нет в файле , создаем ее
            if "clients" not in data:
                data = {"clients": []}
                    
        #Если в файле неправильная структура, обновляем ее           
        except Exception:
            data = {"clients": []}

        data["clients"].append(client_data)
        open_clients_dump(data)

