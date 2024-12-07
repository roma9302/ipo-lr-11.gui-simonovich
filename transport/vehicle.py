from .function import *
from .transport_company import TransportCompany
from .client import Client
from .function import *
import json


company = TransportCompany("Транспортная компания")

class Vehicle:
    def __init__(self, capacity, current_load=0, clients_list=[]):
        self.vehicle_id = generate() 
        self.capacity = validate_number(capacity)  
        self.current_load = validate_number(current_load) 
        self.clients_list = clients_list 


        
    def load_cargo(self):
        try:
            output_client()
            client_id = str(input("Введите айди клиента "))

            with open("transport/clients.json", 'r', encoding='utf-8') as file:
                clients = json.load(file)
                for client in clients['clients']:
                    if client_id == client['client']['client_id']:
                        client_cargo = client['client']['cargo_weight']

                        company.list_vehicles()
                        id_vehicle = str(input("Введите идентификационный номер т/с: "))
                        with open("transport/database.json", 'r', encoding='utf-8') as file:
                            vehicles_data = json.load(file)
                            vehicles = vehicles_data["fields"]["vehicles"]

                            for vehicle_data in vehicles:
                                if id_vehicle == vehicle_data['vehicle_id']:
                                    if float(client_cargo) <= float(vehicle_data['capacity']):
                                        if float(vehicle_data['capacity']) >= float(vehicle_data['current_load']) + float(client_cargo):
                                            vehicle_data['current_load'] += float(client_cargo)
                                            add_completed_client(client['client'], vehicle_data['vehicle_id'])
                                            clients['clients'].remove(client) 

                                            with open("transport/clients.json", 'w', encoding='utf-8') as outfile:
                                                json.dump(clients, outfile, ensure_ascii=False, indent=4)
                                            print("Клиент успешно загружен ")
                                        else:
                                            print(f"Груз {client_cargo} превышает грузоподъемность т/с {vehicle_data['capacity']}.")
                                    else:
                                        print(f"Груз {client_cargo} превышает грузоподъемность т/с {vehicle_data['capacity']}.")
                                    
                                    with open("transport/database.json", 'w', encoding='utf-8') as outfile:
                                        json.dump(vehicles_data, outfile, ensure_ascii=False, indent=4)

        except :
            print(f"Ошибка при ручной загрузке: Проверьте наличие т/с и клиента.")




    def __str__(self):
        return f"ID ТС: {self.vehicle_id}, Грузоподъемность: {self.capacity} т, Текущая загрузка: {self.current_load} т"


