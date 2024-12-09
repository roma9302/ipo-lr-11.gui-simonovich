from .function import  *

# класс ангар
class Hangar:
    #метод для добавление к ангарам +1
    def hangar_add():
        vehicles_data = open_database_load()
        vehicles_data['fields']['hangars'] += 1  #Добавление к ангарам 1
        open_database_dump(vehicles_data)

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
                open_database_dump(vehicles_data) # обновление файла json
                return 2
            else:
                return 3

                    


    # счетчик количства ангаров
    def hangar_count():
        hangar_count = open_database_load()
        return hangar_count['fields']['hangars']
      
