from .vehicle import *
import json

class Airplane(Vehicle):
    def __init__(self, max_altitude, capacity, current_load, clients_list):
        super().__init__(capacity, current_load, clients_list)
        self.max_altitude = validate_number(max_altitude)

        airplane_data = {
            "type": 'airplane',
            "vehicle_id": self.vehicle_id, 
            "capacity": self.capacity,
            "current_load": self.current_load,
            "max_altitude": self.max_altitude
        }

        try:
            with open("transport/database.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
                if "fields" not in data or "vehicles" not in data["fields"]:
                    data = {"company": "transport_company", "fields": {"vehicles": []}}
        except Exception:
            data = {"company": "transport_company", "fields": {"vehicles": []}}

        data["fields"]["vehicles"].append(airplane_data)

        with open('transport/database.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

