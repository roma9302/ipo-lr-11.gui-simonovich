from .vehicle import *
import json

class Van(Vehicle):
    def __init__(self, is_refrigerated, capacity, current_load, clients_list):
        super().__init__(capacity, current_load, clients_list)
        self.is_refrigerated = True if is_refrigerated.lower() == "да" else False

        van_data = {
            "type": 'van',
            "vehicle_id": self.vehicle_id, 
            "capacity": self.capacity,
            "current_load": self.current_load,
            "is_refrigerated": self.is_refrigerated
        }

        try:
            with open("transport/database.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
                if "fields" not in data or "vehicles" not in data["fields"]:
                    data = {"company": "transport_company", "fields": {"vehicles": []}}
        except Exception:
            data = {"company": "transport_company", "fields": {"vehicles": []}}

        data["fields"]["vehicles"].append(van_data)

        with open('transport/database.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
