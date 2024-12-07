from .vehicle import *
import json

class Airplane(Vehicle):
    def __init__(self, max_altitude, capacity, current_load, clients_list):
        super().__init__(capacity, current_load, clients_list)
        self.max_altitude = validate_number(max_altitude)

        #Словарь для записи в файл обьеккта класса
        airplane_data = {
            "type": 'airplane',
            "vehicle_id": self.vehicle_id, 
            "capacity": self.capacity,
            "current_load": self.current_load,
            "max_altitude": self.max_altitude
        }

        try:
            data = open_database_load()
                
                #Если в файле нет нужной структуры , создаем ее
            if "fields" not in data or "vehicles" not in data["fields"]:
                data = {"company": "transport_company", "fields": {"vehicles": []}}
                    
        #Если в файле ошибочная структура , обновляем ее           
        except Exception:
            data = {"company": "transport_company", "fields": {"vehicles": []}}

        data["fields"]["vehicles"].append(airplane_data)

        open_database_dump(data)

