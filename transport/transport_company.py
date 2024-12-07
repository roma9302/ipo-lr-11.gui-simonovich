from .client import Client
from .vehicle import *
from .function import *
import json

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_client(self, client):
        self.clients.append(client)


    def list_vehicles(self):
        try:
            with open("transport/database.json", 'r', encoding='utf-8') as file:
                vehicles_data = json.load(file)
                
            try:
                vehicles = vehicles_data["fields"]["vehicles"]
            except:
                print("Возникла ошибка при выводе т/с . Их нет")

            print("Доступные Транспортные средства:")
            for vehicle_data in vehicles:
                vehicle_id = vehicle_data['vehicle_id']
                vehicle_type = vehicle_data['type']
                capacity = vehicle_data['capacity']
                current_load = vehicle_data['current_load']
                is_refrigerated = vehicle_data.get('is_refrigerated') 
                max_altitude = vehicle_data.get('max_altitude')

                if vehicle_type == 'van':
                    print(f"""
                            Тип: {vehicle_type}
                            Айди: {vehicle_id}
                            Грузоподьемность: {capacity}
                            Текущая загруженность: {current_load}
                            Наличие холодильника: {is_refrigerated}
                            """)
                elif vehicle_type == 'airplane':
                    print(f"""
                            Тип: {vehicle_type}
                            Айди: {vehicle_id}
                            Грузоподьемность: {capacity}
                            Текущая загруженность: {current_load}
                            Максимальная высота подьема {max_altitude}
                            """)
        except:
            print("Ошибка при выводе транспорта. Проверьте его наличие")

    def optimize_cargo_distribution(self):
        optimize()


