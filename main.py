from transport.client import Client
from transport.van import Van 
from transport.airplane import Airplane
from transport.transport_company import TransportCompany
from transport.vehicle import *
import json


company = TransportCompany("Транспортная компания")



def hangar():
    hangar_close = True
    while hangar_close:
        with open("transport/database.json", 'r', encoding='utf-8') as file:
            hangar_count = json.load(file)
        counter =0
        print(f"""
            Количество Ангаров {hangar_count['fields']['hangars']}
            1) Добавить 1 ангар 
            2) Удалить 1 ангар
            3) Удалить т/с 
            4) Выйти в меню""")
        num = int(input("Введите число для взаимодействия "))
        if num == 1:
            with open("transport/database.json", 'r', encoding='utf-8') as file:
                vehicles_data = json.load(file)
                vehicles_data['fields']['hangars'] += 1  
                print("Ангар добавлен.")
                with open("transport/database.json", 'w', encoding='utf-8') as outfile:
                    json.dump(vehicles_data, outfile, ensure_ascii=False, indent=4)
        elif num == 2:
            with open("transport/database.json", 'r', encoding='utf-8') as file:
                vehicles_data = json.load(file)
                for a in vehicles_data['fields']['vehicles'] :
                    counter +=1 
                if vehicles_data['fields']['hangars'] - 1 >= counter:
                    vehicles_data['fields']['hangars'] -= 1 
                    print("Ангар удален.")
                    with open("transport/database.json", 'w', encoding='utf-8') as outfile:
                        json.dump(vehicles_data, outfile, ensure_ascii=False, indent=4)
                else:
                    print("Невозможно удалить ангар ")
        elif num == 3:
            company.list_vehicles()
            id_del = str(input("Введите айди т/с "))
            with open("transport/database.json", 'r', encoding='utf-8') as file:
                vehicles_data = json.load(file)
                vehicles = vehicles_data['fields']['vehicles']
                for vehicle in vehicles:
                    if vehicle['vehicle_id'] == id_del:
                        vehicles.remove(vehicle)  
                        with open("transport/database.json", 'w', encoding='utf-8') as outfile:
                            json.dump(vehicles_data, outfile, ensure_ascii=False, indent=4)
                        print(f"Т/с с айди {id_del} удалено.")
                        break
                else:
                    print(f"Т/с с айди {id_del} не найдено.")

        elif num == 4:
            hangar_close = False
        else:
            print("От 1 до 4")



def add_client():
    name = input("Введите имя клиента: ")
    cargo_weight = input("Введите вес груза: ")
    is_vip = input("VIP клиент (да/нет): ").lower() == "да"
    if validate_str(name) != None and validate_number(cargo_weight) != None:
        client = Client(name, cargo_weight, is_vip)
        company.add_client(client)




def add_vehicle():
    counter = 0
    try:
        with open("transport/database.json", 'r', encoding='utf-8') as file:
            vehicles_data = json.load(file)
            for a in vehicles_data['fields']['vehicles']:
                counter += 1 
            if vehicles_data['fields'].get('hangars', 0) - 1 >= counter:
                vehicle_type = input("Введите тип (van/airplane): ")
                capacity = input("Введите грузоподъемность: ")
                if validate_number(capacity) is not None:
                    if vehicle_type.lower() == "van":
                        is_refrigerated =  input("Холодильник (да/нет): ")
                        van = Van(is_refrigerated, capacity, 0, [])
                        company.add_vehicle(van)
                    elif vehicle_type.lower() == "airplane":
                        max_altitude = input("Введите максимальную высоту: ")
                        if validate_number(max_altitude) is not None:
                            airplane = Airplane(max_altitude, capacity, 0, [])
                            company.add_vehicle(airplane)
                        else:
                            print("Некорректное значение для максимальной высоты.")
                else:
                    print("Некорректное значение для грузоподъемности.")
            else:
                print("Доступных мест в ангаре нет.")
    except:
        print(f"Ошибка при создании т/с")


def leave():
    global close
    print("Программа завершена. Можно в любой момент вернуться к текущей базе клиентов/транспорта")
    close = False 





def console_programm():
    while close:
        try:
            menu()
            num = int(input("Выберите вариант взаимодействия "))
            if num == 1:
                hangar()
            elif num == 2:
                add_client()
            elif num == 3:
                add_vehicle()
            elif num == 4:
                output_client()
            elif num == 5:
                output_completed_client()
            elif num == 6:
                company.list_vehicles()
            elif num == 7:
                company.optimize_cargo_distribution()
            elif num == 8:
                Vehicle.load_cargo(0)
            elif num == 9:
                unloading_caro() 
            elif num == 10:
                example()
            elif num == 11:
                leave()
            else:
                print("Ошибка. Выберите От 1 до 11 ")
        except:
            print("Непредвиденная ошибка. Попробуйте еще раз ")

        
console_programm()

