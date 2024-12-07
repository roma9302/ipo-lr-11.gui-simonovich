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

#метод для чтения обьектов из файла json
    def list_vehicles(self):
        vehicles_list =[]
        try:
            vehicles_data = open_database_load() #чтение данных из файла
            try:
                vehicles = vehicles_data["fields"]["vehicles"]
            except:
                print("Возникла ошибка при выводе т/с . Их нет")

            #Перебор всех атрибутов обьектов в файле (get дабы избежать ошибок если значения не будет. Т.е для разделения на подклассы)
            for vehicle_data in vehicles:
                vehicle_id = vehicle_data['vehicle_id']
                vehicle_type = vehicle_data['type']
                capacity = vehicle_data['capacity']
                current_load = vehicle_data['current_load']
                is_refrigerated = vehicle_data.get('is_refrigerated')
                max_altitude = vehicle_data.get('max_altitude')

                vehicles_list.append({
                    "type": vehicle_type,
                    "capacity": capacity,
                    "current_load": current_load,
                    "is_refrigerated": is_refrigerated,
                    "vehicle_id": vehicle_id,
                    "max_altitude": max_altitude
                })

            return vehicles_list  #возвращает список т/с
        except:
            print("Ошибка при выводе транспорта. Проверьте его наличие")


