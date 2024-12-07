import random as r
import time
import json




# валидация(проверка имен/строк на корректность)
def validate_str(user_input):
    if user_input.isalpha(): #Проверка (состоит ли аргумент из букв. Если есть хоть 1 эленмент не удовлетворяющий условию -> return None)
        return user_input
    else:
        print(f"Ошибка: ввод '{user_input}'должен содержать только буквы.")
        return None



#Валидация(проверка на содержание одних лишь цифр)
def validate_number(user_input):
    try:
        float_value = float(user_input) #Если аргумент можно представить в виде float значения идем дальше.
        if float_value < 0:  #Если наше float значение меньше  0 -> return None .
            print(f"Ошибка: ввод '{user_input}' должен быть неотрицательным числом/нулевым ")
            return None   
        return float_value  # Нет -> return value
    except ValueError:
        print(f"Ошибка: ввод '{user_input}' должен содержать число")
        return None # Нет -> return None


#Генерация случайной строки (уникальный идентификатор  для клиента и т/с (строка, генерируется случайно при создание))
def generate():
    random_number = str(r.randint(1000, 99999999)) 

    repeat_client= open_clients_load()
    repeat_database = open_database_load()
    repeat_completed= open_completed_load()

    while random_number in repeat_client or random_number in repeat_database or random_number in repeat_completed:  #Продолжает генерировать новый айди пока он не станет уникальным 
        random_number = str(r.randint(1000, 99999999))
    return random_number


#Сортировка грузов клиентов (Внутрення функция для optimize)
def sort_cargo(clients):
    for i in range(len(clients)):
        for j in range(0, len(clients)-i-1):
            if clients[j][1] < clients[j + 1][1]: 
                clients[j], clients[j + 1] = clients[j + 1], clients[j]
    return clients


#функции чтения и записи json
def open_database_load():
    with open("transport/database.json", 'r', encoding='utf-8') as file:
        vehicles_data = json.load(file)
        return vehicles_data

def open_database_dump(vehicles_data):
    with open("transport/database.json", 'w', encoding='utf-8') as outfile:
        json.dump(vehicles_data, outfile, ensure_ascii=False, indent=4)

def open_clients_load():
    with open('transport/clients.json', 'r', encoding='utf-8') as file:
        clients_data = json.load(file)
        return clients_data

def open_clients_dump(clients_data):
    with open('transport/clients.json', 'w', encoding='utf-8') as output:
        json.dump(clients_data, output, ensure_ascii=False, indent=4)

def open_completed_load():
    with open('transport/completed_cargo.json', 'r', encoding='utf-8') as file:
        completed_cargo = json.load(file)    
        return completed_cargo

def open_completed_dump(completed_cargo):
    with open('transport/completed_cargo.json', 'w', encoding='utf-8') as output:
        json.dump(completed_cargo, output, ensure_ascii=False, indent=4)    



#Функция сбора клиентов для  дальнейших функций
def output_client():
    try:
        clients = open_clients_load()
            # Проверка clients и его наличия
        if 'clients' not in clients or not clients['clients']:
            return []  

        return clients['clients']  

    except:
        print("Возникла ошибка. Проверьте наличие клиентов ")

def del_client(client_id):
        clients_data = open_clients_load()
        clients = clients_data['clients']
        clients_data['clients'] = [client for client in clients if client['client']['client_id'] != str(client_id)]  #исключения не подходящих условию
        open_clients_dump(clients_data)


def del_vehicle(vehicle_id):
    vehicles_data = open_database_load()
    vehicles = vehicles_data['fields']['vehicles']
    vehicles_data['fields']['vehicles'] = [vehicle for vehicle in vehicles if vehicle['vehicle_id'] != str(vehicle_id)] #исключения не подходящих условию
    open_database_dump(vehicles_data)




#Функция добавления клиентов
def add_completed_client(client_data,vehicle):
    try:
        data = open_clients_load()
        if "clients" not in data:
            data = {"clients": []}  #Если файл пустой. Создание начальной структуры
                
#Если в файле неправильная структура . Создание начальной структуры
    except Exception:
        data = {"clients": []}     

#Создание структуры готового файла
    client_completed_cargo = {
        "client": client_data,
        "vehicle": vehicle
    }

    data["clients"].append(client_completed_cargo)
    open_completed_dump(data)



#Вывод загруженых клиентов из файла 
def output_completed_client():
    clients_completed = []  # Инициализация списка загруженных клиентов
    try:
        clients_completed = open_completed_load() # Загрузка данных
    
        # Проверка наличия clients 
        if 'clients' not in clients_completed or not clients_completed['clients']:
            return []  

        return clients_completed['clients']  
    except Exception as e:
        print(f"Возникла ошибка: {str(e)}")
        return []


