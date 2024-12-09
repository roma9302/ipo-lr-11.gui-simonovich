import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip
from tkinter import messagebox
from tkinter import simpledialog
from transport.client import Client
from transport.van import Van 
from transport.airplane import Airplane
from transport.transport_company import TransportCompany
from transport.vehicle import *
from transport.hangar import Hangar
import json


company = TransportCompany("Транспортная компания")


# функция обновление статус бара
def status_label_update(message):
    status_var.set(message)



# функция очистки каждой таблицы
def clearning_tree():
    for item in transport_tree.get_children():
        transport_tree.delete(item)
    for item in load_tree.get_children():
        load_tree.delete(item)
    for item in client_tree.get_children():
        client_tree.delete(item)



# обновление лейбла для ангара
def update_label_hangar():
    label_transport.config(text=f"Количество ангаров {Hangar.hangar_count()}")


# класс ангар
class Hangar:
    #метод для добавление к ангарам +1
    def hangar_add():
        vehicles_data = open_database_load()
        vehicles_data['fields']['hangars'] += 1  #Добавление к ангарам 1
        open_database_dump(vehicles_data)
        update_label_hangar()  # обновление лейбла
        status_label_update("ангар добавлен")  # вывод в статус бар

    # Метод для удаление ангаров -1
    def hangar_del():
            vehicles_data = open_database_load() # чтение данных json
            counter = 0 # счетчик кол-ва т/с
            
            #Нахождение количества т/с в файле
            for a in vehicles_data['fields']['vehicles'] :
                counter +=1 
                
            #Проверка если удалить ангар будет ли хватать места на все машины
            if vehicles_data['fields']['hangars'] - 1 >= counter:
                vehicles_data['fields']['hangars'] -= 1 
                status_label_update("ангар удален.")
                
                open_database_dump(vehicles_data) # обновление файла json
                update_label_hangar() # обнвление лейбла
                    
            else:
                messagebox.showerror("Ошибка", "транспорта слишком много . Удалите сперва т/с") # уведомление об ошибке
                status_label_update("транспорта слишком много . Удалите сперва т/с") # обновление статус бара

    # счетчик количства ангаров
    def hangar_count():
        hangar_count = open_database_load()
        return hangar_count['fields']['hangars']
            

# обновление таблицы 
def update_tables(company):
    for tree in [transport_tree, load_tree, client_tree]:
        for row in tree.get_children():
            tree.delete(row)


    table(company)

#функция для сортировка по столбццам таблицы
def sort(col, reverse, tree):
    # Получаем все значения столбцов в виде списка кортежей 
    l = [(tree.set(k, col), k) for k in tree.get_children("")]
    
    # Проверка на наличие данных
    if not l:
        messagebox.showinfo("Информация", "Нет данных для сортировки.")
        return

    # Сортируем список по значению, учитывая флаг reverse
    l.sort(reverse=reverse, key=lambda x: (x[0] == '', x[0]))

    for index, (_, k) in enumerate(l):
        tree.move(k, "", index)

    #  сортировка для следующего нажатия заголовка
    tree.heading(col, command=lambda: sort(col, not reverse, tree))
    status_label_update("сортировка прошла успешно.")


#функция  оптимизированной загрузки в т/с
def optimize():
        clients_data = open_clients_load()  # чтение файла
        vehicles_data = open_database_load() # чтение файла
 
        # создание пустой структуры если файл  пуст 
        try:
            completed_cargo  = open_completed_load()
        except Exception:
            completed_cargo = {"clients": []}

        vehicles = vehicles_data['fields']['vehicles']

        vip_clients = [] #лист для вип клиентов 
        clients_non_vip = [] #Лист для обычных клиентов

 #Перебор клиентов всех групп и добавление по флагу вип в листы 
        for client in clients_data['clients']: 
            cargo_weight = int(client['client']['cargo_weight'])
            if client['client']['is_vip']:
                vip_clients.append((client, cargo_weight))
            else:
                clients_non_vip.append((client, cargo_weight))

#Сортировка значений по порядку возврастания
        sort_cargo(vip_clients)
        sort_cargo(clients_non_vip)

        sorted_clients = vip_clients + clients_non_vip  #Создание общего списка(vip - first; min - first)

#Обновление загруженности т/с , удаление клиента из списка доступных , добавление клиента в файл загруженных пользователей 
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

        #запись в файлы
        open_clients_dump(clients_data)  
        open_database_dump(vehicles_data)
        open_completed_dump(completed_cargo)

        #обновление статус бара и таблиц
        update_tables(company)
        status_label_update("Оптимизиция прошла успешно") 

#выгрузка данных из таблиц. Освобождние т/с
def uploading_cargo():
    try:
            
        time.sleep(5)   # 5 секунд задержки программы

        status_label_update("выгрузка прошла успешно") # обновление статус бара

        vehicles_data = open_database_load() # чтение данных json
        vehicles = vehicles_data["fields"]["vehicles"]
        

        #логика проверки на наличие в машине грузов
        for vehicle_data in vehicles:
            if vehicle_data['current_load'] > 0:  #Если загруженность машины больше 0, ей присваивается 0
                vehicle_data['current_load'] = 0
                open_database_dump(vehicles_data)

        # открытие клиентского файла для его последующей очистки
        clients_completed = open_completed_load()
        clients_completed['clients'] = [] #Создает пустую структуру []

        #Обновление клиентского списка 
        open_completed_dump(clients_completed)
        update_tables(company)

    # при ошибке вывод уведомления 
    except:
        messagebox.showerror("Ошибка", "возникла ошибка при выгрузке т/с")


#Добавление нового т/с
def add_new_vehicle():
    def new_vehicle():
        # Получаем значения из полей ввода
        capacity = capacity_entry.get()
        vehicle_type = vehicle_type_var.get()

        # Валидация введенных данных
        if validate_number(capacity) is not None and vehicle_type:
            try:
                    vehicles_data = open_database_load() # чтение данных
                    counter = len(vehicles_data['fields'].get('vehicles', []))  # колво т/с
                    
                    #Логика проверки на не превышение количества ангаров 1 ангар = 1 т/с
                    if vehicles_data['fields'].get('hangars', 0) - 1 >= counter:
                        #Далее логика выбора т/с и их индивидуальных и общих атрибутов
                        if vehicle_type == "van":
                            is_refrigerated = simpledialog.askstring("Холодильник", " есть холодильник? (да/нет)")
                            van = Van(is_refrigerated, capacity, 0, [])
                            company.add_vehicle(van)
                            clearning_tree()
                            table(company) 

                        elif vehicle_type == "airplane":
                            max_altitude = tk.simpledialog.askfloat("Максимальная высота", "Введите максимальную высоту:")
                            if max_altitude is not None:
                                airplane = Airplane(max_altitude, capacity, 0, [])
                                company.add_vehicle(airplane)
                                clearning_tree()
                                table(company) 
                            else:
                                messagebox.showerror("Ошибка", "Максимальная высота должна быть указана.")
                                return

                        messagebox.showinfo("Успешно", "Транспортное средство успешно добавлено!")
                        vehicle_topic.destroy() # воход из окна 
                        status_label_update("Данные транспортного средства добавлены.")
                    else:
                        messagebox.showerror("Ошибка", "Мест в ангаре нет.")
            except Exception :
                messagebox.showerror("Ошибка", f"Ошибка при добавлении транспортного средства: ")
        else:
            messagebox.showerror("Ошибка", "Некорректные данные. Транспортное средство не добавлено.")
            status_label_update("Ошибка. Транспортное средство не добавлено.")
    def enter(event):  #Обработка события  клавиши enter 
        new_vehicle()
    def escape(event): #Обработка события  клавиши esc
        vehicle_topic.destroy()

    # Создание окна для ввода данных о транспортном средстве
    vehicle_topic = tk.Toplevel(root)
    vehicle_topic.title("Добавить транспортное средство")

    #поле для выбора типа т/с
    ttk.Label(vehicle_topic, text="Тип транспорта:").grid(row=0, column=0)
    vehicle_type_var = tk.StringVar()
    vehicle_type_combobox = ttk.Combobox(vehicle_topic, textvariable=vehicle_type_var) # привязка переменной вводимой информации
    vehicle_type_combobox['values'] = ("van", "airplane")
    vehicle_type_combobox.grid(row=0, column=1)

    # поле для выбора грузоподьемности
    ttk.Label(vehicle_topic, text="Грузоподъемность:").grid(row=1, column=0)
    capacity_entry = ttk.Entry(vehicle_topic)
    capacity_entry.grid(row=1, column=1)

    submit_button_add = ttk.Button(vehicle_topic, text="Добавить", command=new_vehicle)
    submit_button_add.grid(row=3, column=0)  

    submit_button_cancel = ttk.Button(vehicle_topic, text="Отмена", command=vehicle_topic.destroy)
    submit_button_cancel.grid(row=3, column=1)
    vehicle_topic.bind('<Return>', enter) 
    vehicle_topic.bind('<Escape>', escape)
    #Всплывающая подсказка
    ToolTip(capacity_entry, msg="Обязательное, числовое / дробное значение положительного значения ")



def delete_vehicle():
    selected_item = transport_tree.selection()  # Получаем выбранный элемент
    if selected_item:  
        vehicle_id = transport_tree.item(selected_item)['values'][5]  # получение айди из таблицы
        del_vehicle(vehicle_id)  # Удаляем клиента по айди
        transport_tree.delete(selected_item)  # Удаляем элемент из таблицы
        status_label_update("транспорт удален.")  # обновление статус бара
    else:
        messagebox.showwarning("Ошибка", "Выберите т/с для удаления.") # ошибка при сбое
        status_label_update("транспорт не удален.")  # обновление статус бара


# добавление нового клиента
def add_new_client():
    def new_client():
        # получение данных после ввода их в поля
        name = name_entry.get() 
        cargo_weight = cargo_weight_entry.get()
        is_vip =  vip_var.get() 

        # Валидация
        if validate_str(name) is not None and validate_number(cargo_weight) is not None and len(name) >= 2 and int(cargo_weight) < 10000:
            clearning_tree() # очистка всекх таблиц
            client = Client(name, cargo_weight, is_vip ) # создание обьекта класса
            company.add_client(client)
            messagebox.showinfo("Успешно", "Клиент успешно добавлен!") # обновление статус бара
            client_topic.destroy() # закрытие окна 
            table(company)  # Обновляем таблицу
            status_label_update("Данные клиента добавлены .") # обновление статус бара

        else:
            status_label_update("Ошибка. Клиент не добавлен.") # обновление статус бара
            messagebox.showerror("Ошибка", "Клиент не добавлен") # уведомление об ощшибке

    # Обработка кликов enter и esc
    def enter(event):
        new_client()
    def escape(event):
        client_topic.destroy()


    client_topic = tk.Toplevel(root)
    client_topic.title("Добавить клиента")

    ttk.Label(client_topic, text="Имя клиента:").grid(row=0, column=0)
    name_entry = ttk.Entry(client_topic)
    name_entry.grid(row=0, column=1)

    ttk.Label(client_topic, text="Вес груза:").grid(row=1, column=0)
    cargo_weight_entry = ttk.Entry(client_topic)
    cargo_weight_entry.grid(row=1, column=1)

    vip_var = tk.BooleanVar()
    ttk.Checkbutton(client_topic, text="VIP клиент", variable=vip_var).grid(row=2, columnspan=2)

    submit_button_add = ttk.Button(client_topic, text="Добавить", command=new_client)
    submit_button_add.grid(row=3, column=0)  

    submit_button_cancel = ttk.Button(client_topic, text="Отмена", command=client_topic.destroy)
    submit_button_cancel.grid(row=3, column=1)  
    client_topic.bind('<Return>', enter) 
    client_topic.bind('<Escape>', escape)
    #Всплывающие подсказки
    ToolTip(name_entry, msg="Обязательное, текстовое (валидация: только буквы, минимум 2 символа).")
    ToolTip(cargo_weight_entry, msg="Обязательное, числовое (валидация: положительное число, не более 10000 кг).")


# функция удаление клиента
def delete_client():
    selected_item = client_tree.selection()  # Получаем выбранный элемент
    if selected_item:  
        client_id = client_tree.item(selected_item)['values'][3]  # извлечение из таблицы client_id
        del_client(client_id)  # Удаляем клиента по client_id
        client_tree.delete(selected_item)  # Удаляем элемент из таблицы
        status_label_update("Клиент удален.")  # обновление статус бара
    else:
        messagebox.showwarning("Ошибка", "Выберите клиента для удаления.")
        status_label_update("Клиент не удален.")  # обновление статус бара




# Изменение клиента
def edit_client(event):
    selected_item = client_tree.selection()  # Получаем выбранный элемент
    if selected_item:  
        client_id = client_tree.item(selected_item)['values'][3]  # извлечение client_id

        # сбор данных клиента из файла
        current_client_data = None
        clients_data = open_clients_load()
        for client in clients_data['clients']:
            if client['client']['client_id'] == str(client_id):
                current_client_data = client['client']
                break
        
        if current_client_data is None:
            messagebox.showerror("Ошибка", "Клиент не найден.") # уведовление об ошибке если клиента нет
            return

        #  диалоговые окна для редактирования данных
        new_name = simpledialog.askstring("Редактировать имя", "Имя клиента:", initialvalue=current_client_data['name'])
        if validate_str(new_name) is None or new_name == "":
            messagebox.showwarning("Ошибка", "Неправильные данные.Только буквы, минимум 2 символа")
            return  

        new_cargo_weight = simpledialog.askfloat("Редактировать вес груза", "Вес груза (в кг):", initialvalue=current_client_data['cargo_weight'])
        if validate_number(new_cargo_weight) is None  or validate_number(new_cargo_weight) >= 10000 :  
            messagebox.showwarning("Ошибка", "Положительное число, не более 10000 кг")
            return

        is_vip = simpledialog.askstring("Редактировать статус вип", "вип (да/нет):", initialvalue='да' if current_client_data['is_vip'] else 'нет')
        if is_vip is None: return  

        is_vip = True if is_vip.lower() == 'да' else False

        # обновление таблицы
        current_client_data['name'] = new_name
        current_client_data['cargo_weight'] = new_cargo_weight
        current_client_data['is_vip'] = is_vip

        # запись в файл
        open_clients_dump(clients_data)
        # Также обновляем интерфейс: заменяем старые данные новыми
        clearning_tree() #очистка таблиц
        table(company)  # заполнение таблиц из файла

        status_label_update("Данные клиента обновлены успешно.")  # обновление статус бара
    else:
        messagebox.showwarning("Ошибка", "Выберите клиента для редактирования.") # уведомление об ошибке
        status_label_update("Клиент не обновлен") # обновление статус бара


#функция измекнения т/с
def edit_vehicle(event):
    selected_item = transport_tree.selection()  # Получаем выбранный элемент
    if selected_item:  
        vehicle_id = transport_tree.item(selected_item)['values'][5]  # извлечение vehicle_id

        # сбор данных из файла
        current_vehicle_data = None
        transport_data = open_database_load()
        for vehicle in transport_data['fields']['vehicles']:
            if vehicle['vehicle_id'] == str(vehicle_id):
                current_vehicle_data = vehicle
                break
        
        if current_vehicle_data is None:
            messagebox.showerror("Ошибка", "Транспортное средство не найдено.") # уведомление об ошибке
            return

        # диалоговые окна для редактирования данных
        new_type = simpledialog.askstring("Редактировать тип", "Тип транспортного средства (airplane/van):", initialvalue=current_vehicle_data['type'])
        if new_type is None or new_type == "":
            messagebox.showwarning("Ошибка", "Тип не может быть пустым.")
            return  
        if new_type not in ["airplane", "van"]:
            messagebox.showwarning("Ошибка", "Тип должен быть airplane или van.")
            return

        new_capacity = simpledialog.askfloat("Редактировать вместимость", "Вместимость (в тоннах):", initialvalue=current_vehicle_data['capacity'])
        if validate_number(new_capacity) is None or new_capacity <= 0:  
            messagebox.showwarning("Ошибка", "Вместимость должна быть положительным числом.")
            return

        # Обновление т/с
        current_vehicle_data['type'] = new_type
        current_vehicle_data['capacity'] = new_capacity
        current_vehicle_data['current_load'] = 0  #сброс текущей загрузки авто

        # логика добавления уникальных атрибутов
        if new_type == "airplane":
            new_max_altitude = simpledialog.askfloat("Редактировать максимальную высоту", "Максимальная высота (в метрах):", initialvalue=current_vehicle_data.get('max_altitude', 0))
            if validate_number(new_max_altitude) is None or new_max_altitude <= 0:  
                messagebox.showwarning("Ошибка", "Максимальная высота должна быть положительным числом.")
                return
            current_vehicle_data['max_altitude'] = new_max_altitude
            # удаление не соответствующего атрибута
            if 'is_refrigerated' in current_vehicle_data:
                del current_vehicle_data['is_refrigerated']
        else:  
            is_refrigerated = simpledialog.askstring("Редактировать холодильник", "Есть ли холодильник? (да/нет):", initialvalue=current_vehicle_data.get('is_refrigerated', 'нет'))
            if is_refrigerated not in ["да", "нет"]:
                messagebox.showwarning("Ошибка", "Ответ должен быть да или нет.")
                return
            current_vehicle_data['is_refrigerated'] = is_refrigerated
            # удаление не соответствующиего атрибутта
            if 'max_altitude' in current_vehicle_data:
                del current_vehicle_data['max_altitude']

        # запись данных в файл
        open_database_dump(transport_data)

       
        clearning_tree() #очистка таблиц
        table(company)  # заполнение таблиц новыми данными

        status_label_update("Данные транспортного средства обновлены успешно.")  # Обновляем статус
    else:
        messagebox.showwarning("Ошибка", "Выберите транспортное средство для редактирования.")
        status_label_update("Транспортное средство не обновлено.")  # Обновляем статус


# функция заполнения таблиц
def table(company):
    vehicles = company.list_vehicles()
    for vehicle in vehicles:
            transport_tree.insert('', 'end', values=(
                vehicle["type"],
                vehicle["capacity"],
                vehicle["current_load"],
                'Да' if vehicle["is_refrigerated"]  == True or  vehicle["is_refrigerated"]  == 'да' else 'Нет',
                vehicle['max_altitude'] if vehicle['max_altitude'] != None else "Не относится к данному транспорту",
                vehicle["vehicle_id"]
            ))

    client_completed = output_completed_client()
    for completed in client_completed:
        load_tree.insert('', 'end', values=(
            completed['client']['name'],
            completed['client']['cargo_weight'],
            'да' if completed['client']['is_vip'] == True else 'нет',
            completed['client']['client_id'],
            completed['vehicle']
        ))
    clients = output_client()
    for client in clients:
        client_tree.insert('', 'end', values =(
            client['client']['name'],
            client['client']['cargo_weight'],
            'да' if client['client']['is_vip'] == True else 'нет',
            client['client']['client_id'],
        ))
        status_label_update("Данные загружены успешно.")
   

# окна в меню
def export_results():
    messagebox.showinfo('Выполнено', "Данные о клиентах/транспорте/выполненных заказах автоматически сохраняются в json файлы.")

# обо мне
def show_about():
    messagebox.showinfo("О программе", "Номер л/р: 12 \n Вариант: 4 \n ФИО разработчика: Симонович Роман Дмитриевич")

# главное окно
root = tk.Tk()
root.title("Транспортная компания")
root.geometry("1000x600")

# страницы для разных таблиц
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# вкладка меню
menu = tk.Menu(root)
root.config(menu=menu)

# Подменю  файл
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Экспорт результата", command=export_results)
file_menu.add_command(label="Выход", command=root.quit)
menu.add_cascade(label="Файл", menu=file_menu)

# Подменю справка
help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(label="О программе", command=show_about)
menu.add_cascade(label="Справка", menu=help_menu)

#Создание статус бара
status_var = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor='w')
status_label.pack(side=tk.BOTTOM, fill=tk.X)


# Создание 3 страниц
load_frame = ttk.Frame(notebook) 
vehicle_frame = ttk.Frame(notebook)  
client_frame = ttk.Frame(notebook) 

# добавление страниц в блокнот
notebook.add(load_frame, text='Загруженные грузы')
notebook.add(vehicle_frame, text='Ангар')
notebook.add(client_frame, text='Клиентская база')



# лист для загруженных клиентов
label_load = ttk.Label(load_frame, text="Список загруженных клиентов")
label_load.pack(pady=10)

# кнопки работы с грузом
cargo_opimization_button = ttk.Button(load_frame, text="Распределить грузы ", command=optimize)
cargo_opimization_button.pack(pady=10)
cargo_uploading_button = ttk.Button(load_frame, text="Выгрузить грузы ", command= uploading_cargo)
cargo_uploading_button.pack(pady=10)

load_tree = ttk.Treeview(load_frame, columns=('Имя', 'Груз', 'Вип?' ,'Айди клиента' ,'т/с куда загружен груз'), show='headings')
load_tree.heading('Имя', text='Имя')
load_tree.heading('Груз', text='Груз(кг)' , command=lambda: sort("Груз", False ,load_tree ))
load_tree.heading('Вип?', text='Вип?')
load_tree.heading('Айди клиента', text='Айди Клиента' ,command=lambda: sort("Айди клиента", False ,load_tree ) )
load_tree.heading('т/с куда загружен груз', text='т/с куда загружен груз' , command=lambda: sort("т/с куда загружен груз", False ,load_tree ))
load_tree.pack(fill=tk.BOTH, expand=True)


# Таблица для транспорта (фургоны и самолеты)
label_transport = ttk.Label(vehicle_frame, text=f"Количество ангаров {Hangar.hangar_count()} ")
label_transport.pack(pady=10)

#кнопки работы с т/с и ангаром
delete_vehicle_button = ttk.Button(vehicle_frame, text="Удалить т/с", command=delete_vehicle)
delete_vehicle_button.pack(pady=10)
add_vehicle_button = ttk.Button(vehicle_frame, text="Добавить т/с", command=add_new_vehicle)
add_vehicle_button.pack(pady=10 )
add_hangar_button = ttk.Button(vehicle_frame, text="Добавить ангар", command=Hangar.hangar_add)
add_hangar_button.pack(pady=10 )
del_hangar_button = ttk.Button(vehicle_frame, text="Удлалить ангар", command=Hangar.hangar_del)
del_hangar_button.pack(pady=10 )


transport_tree = ttk.Treeview(vehicle_frame, columns=('Тип', 'Грузоподъемность', 'Текущая загруженность', 'Есть ли холодильник', 'Максимальная высота полета' , "айди"), show='headings')
transport_tree.heading('Тип', text='Тип транспорта')
transport_tree.heading('Грузоподъемность', text='Грузоподъемность (кг)', command=lambda: sort("Грузоподъемность", False ,transport_tree ))
transport_tree.heading('Текущая загруженность', text='Текущая загруженность' , command=lambda: sort("Текущая загруженность", False ,transport_tree ))
transport_tree.heading('Есть ли холодильник', text='Есть ли холодильник' )
transport_tree.heading('Максимальная высота полета', text='Максимальная высота полета'   )
transport_tree.heading('айди', text='Айди' , command=lambda: sort("айди", False ,transport_tree ))
transport_tree.pack(fill=tk.BOTH, expand=True)
transport_tree.bind("<Double-1>", edit_vehicle)


# Таблица для клиентов
label_client = ttk.Label(client_frame, text="Таблица для клиентов")
label_client.pack(pady=10)

#кнопки работы с клиентами
add_client_button = ttk.Button(client_frame, text="Добавить клиента", command=add_new_client)
add_client_button.pack(pady=10)
delete_client_button = ttk.Button(client_frame, text="Удалить клиента", command=delete_client)
delete_client_button.pack(pady=10)

client_tree = ttk.Treeview(client_frame, columns=('Имя', 'Груз' , 'Вип?' , 'Айди клиента'), show='headings')
client_tree.heading('Имя', text='Имя')
client_tree.heading('Груз', text='Груз (кг)' , command=lambda: sort("Груз", False ,client_tree ) )
client_tree.heading('Вип?', text='Вип?')
client_tree.heading('Айди клиента', text='Айди клиента'  , command=lambda: sort("Айди клиента", False ,client_tree ))
client_tree.pack(fill=tk.BOTH, expand=True)
client_tree.bind("<Double-1>", edit_client)


# Заполнение таблиц данными из словаря
table(company)


#открытие окна программы
root.mainloop()

