import random as r
import time
import json





# валидация(проверка имен/строк на корректность)
def validate_str(user_input):
    if user_input.isalpha():
        return user_input
    else:
        print(f"Ошибка: ввод '{user_input}'должен содержать только буквы.")
        return None

#Валидация(проверка на содержание одних лишь цифр)
def validate_number(user_input):
    try:
        float_value = float(user_input)
        if float_value < 0:
            print(f"Ошибка: ввод '{user_input}' должен быть неотрицательным числом/нулевым ")
            return None
        return float_value  
    except ValueError:
        print(f"Ошибка: ввод '{user_input}' должен содержать число")
        return None


#Генерация случайной строки (уникальный идентификатор (строка, генерируется случайно при создание))
def generate():
    random_number = str(r.randint(1000, 99999999)) 

    with open('transport/list_id.txt', 'r', encoding='utf-8') as file:
        repeat = file.read().splitlines()  

    while random_number in repeat:
        random_number = str(r.randint(1000, 99999999))

    with open('transport/list_id.txt', 'a', encoding='utf-8') as file:
        file.write(random_number + '\n')
    return random_number



def sort_cargo(clients):
    for i in range(len(clients)):
        for j in range(0, len(clients)-i-1):
            if clients[j][1] < clients[j + 1][1]: 
                clients[j], clients[j + 1] = clients[j + 1], clients[j]
    return clients





def output_client():
    with open("transport/clients.json", 'r', encoding='utf-8') as file:
        try:
            clients = json.load(file)
            for client in clients['clients']:
                print(f"""
                        Клиент {client['client']['name']}
                        Вес груза {client['client']['cargo_weight']}
                        Вип клиент {client['client']['is_vip']} 
                        Номер клиента в базе данных {client['client']['client_id']}
                        """)
        except:
            print("Возникла ошибка. Проверьте наличие транспорта ")
            

def add_completed_client(client_data,vehicle):
    try:
        with open("transport/completed_cargo.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "clients" not in data:
                data = {"clients": []}
                
    except Exception:
        data = {"clients": []}              
    client_completed_cargo = {
        "client": client_data,
        "vehicle": vehicle
    }


    data["clients"].append(client_completed_cargo)


    with open('transport/completed_cargo.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)



def output_completed_client():
    try:
        with open("transport/completed_cargo.json", 'r', encoding='utf-8') as file:
            clients_completed = json.load(file)
            for client in clients_completed['clients']:
                print(f"""
                        Клиент {client['client']['name']}
                        Вес груза {client['client']['cargo_weight']}
                        Вип клиент {client['client']['is_vip']} 
                        Номер клиента в базе данных {client['client']['client_id']}
                        Т/С в которую загружен груз клиента {client['vehicle']}
                        """)
    except:
        print("Загруженых клиентов нет")




def example():
    print("""
    Добавление нового т/с:
          1)тип (van/airplane)
          2)Грузоподьемность (200, 200.4) в тоннах
          3)Если тип van:
            Есть ли холодильник (да/нет)       
          Если airplane:
            Максимальная высота полета(200,200.3)
    Добавление Клиента:
          1) Имя Клиета (Рома)
          2)Вес груза (200,200.5)
          3) Vip клиент (да,нет) По умолчанию нет          
        """)
    

    
def menu():
    print("""
        1)Управление ангаром
        2)Добавить клиента
        3)Добавить Т/С 
        4)Вывести список  доступных клиентов 
        5)Список клиентов, чьи грузы загружены 
        6)Вывести список доступного транспорта
        7)Автоматическое распределение грузов
        8)Ручное управление грузами 
        9)Выгрузка грузов
        10)Пример заполнения форм
        11) Выход """)
    




def unloading_caro():
    try:
        print("Все грузы отправлены на разгрузку. Для выполнения следующего действия подождите 5 секунд ")
        seconds = 5
        while seconds > 0:
            if seconds == 5:
                print("5 секунд осталось")
            elif seconds == 4:
                print("4 секунды осталось")
            elif seconds == 3:
                print("3 секунды осталось")
            elif seconds == 2:
                print("2 секунды осталось")
            elif seconds == 1:
                print("1 секунда осталась")
            
            time.sleep(1) 
            seconds -= 1

        print("Все грузы были успешно отгружены!")

        with open("transport/database.json", 'r', encoding='utf-8') as file:
            vehicles_data = json.load(file)
            vehicles = vehicles_data["fields"]["vehicles"]
            
            for vehicle_data in vehicles:
                if vehicle_data['current_load'] > 0:
                    vehicle_data['current_load'] = 0

                    with open("transport/database.json", 'w', encoding='utf-8') as outfile:
                        json.dump(vehicles_data, outfile, ensure_ascii=False, indent=4)

        with open("transport/completed_cargo.json", 'r', encoding='utf-8') as file:
                clients_completed = json.load(file)
                clients_completed['clients'] = [] 

                with open("transport/completed_cargo.json", 'w', encoding='utf-8') as outfile:
                    json.dump(clients_completed, outfile, ensure_ascii=False, indent=4)
    except:
        print("Ошибка при разгрузке т/с. Проверьте их загруженность ")



def optimize():
    try:
        with open('transport/clients.json', 'r', encoding='utf-8') as file:
            clients_data = json.load(file)

        with open('transport/database.json', 'r', encoding='utf-8') as file:
            vehicles_data = json.load(file)

        try:
            with open('transport/completed_cargo.json', 'r', encoding='utf-8') as file:
                completed_cargo = json.load(file)
        except Exception:
            completed_cargo = {"clients": []}

        vehicles = vehicles_data['fields']['vehicles']

        vip_clients = []
        clients_non_vip = []

        for client in clients_data['clients']:
            cargo_weight = int(client['client']['cargo_weight'])
            if client['client']['is_vip']:
                vip_clients.append((client, cargo_weight))
            else:
                clients_non_vip.append((client, cargo_weight))


        sort_cargo(vip_clients)
        sort_cargo(clients_non_vip)

        sorted_clients = vip_clients + clients_non_vip

        for client, cargo_weight in sorted_clients:
            for vehicle in vehicles:
                if float(cargo_weight) <= float(vehicle['capacity']) - vehicle['current_load']:
                    vehicle['current_load'] += float(cargo_weight)
                    completed_cargo["clients"].append({
                        "client": client['client'],
                        "vehicle": vehicle['vehicle_id']
                    })
                    clients_data['clients'].remove(client)
                    break

        with open('transport/clients.json', 'w', encoding='utf-8') as output:
            json.dump(clients_data, output, ensure_ascii=False, indent=4)

        with open('transport/database.json', 'w', encoding='utf-8') as output:
            json.dump(vehicles_data, output, ensure_ascii=False, indent=4)

        # Сохраняем обновленные загруженные клиенты
        with open('transport/completed_cargo.json', 'w', encoding='utf-8') as output:
            json.dump(completed_cargo, output, ensure_ascii=False, indent=4)

        for item in completed_cargo["clients"]:
            print(f"Клиент: {item['client']['name']} загружен в транспортное средство ID: {item['vehicle']} с весом груза: {item['client']['cargo_weight']}")
    except:
        print("Ошибка при автоматическом распределениии . Проверьте наличие клиентов и свободных т/с")
