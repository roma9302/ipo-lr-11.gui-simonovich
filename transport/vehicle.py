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

        client_id = str(input("Введите айди клиента "))

        clients = open_clients_load
            
        #Перебор клиента для получения клиентского груза
        for client in clients['clients']:
            if client_id == client['client']['client_id']:
                client_cargo = client['client']['cargo_weight']

                #Вывод списка т/с из класса
                company.list_vehicles()
                id_vehicle = str(input("Введите идентификационный номер т/с: "))

                #Получение т/с по отдельности из файла
                vehicles_data = open_database_load()
                vehicles = vehicles_data["fields"]["vehicles"]

                for vehicle_data in vehicles:
                    if id_vehicle == vehicle_data['vehicle_id']:  
                        if float(client_cargo) <= float(vehicle_data['capacity']): #Если груз не превышет грузоподьемность
                            if float(vehicle_data['capacity']) >= float(vehicle_data['current_load']) + float(client_cargo): #Если груз+текущая загруженность т/с не превышает грузоподьемность
                                vehicle_data['current_load'] += float(client_cargo)
                                #Добавляем клиента в лист загруженных клиентов(функция в function.py) принимет словарь клиент и айди т/с в который был загружен груз
                                add_completed_client(client['client'], vehicle_data['vehicle_id'])
                                #Удаление клиента из списка доступных
                                clients['clients'].remove(client) 

                                open_clients_dump(clients)
                        
                        open_database_load(vehicles_data)






    def __str__(self):
        return f"ID ТС: {self.vehicle_id}, Грузоподъемность: {self.capacity} т, Текущая загрузка: {self.current_load} т"


