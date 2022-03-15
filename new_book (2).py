from pprint import pprint
import csv
import re
import pandas as pd


def for_fio(item):
    str_fio = ' '.join(item)  # склеиваем строку указанным разделителем
    s = re.sub("\s+", " ", str_fio)  # заменяем пробелы на 1 пробел
    a = s.strip()  # метод убирает пробелы вначале и конце строки
    fio_list = a.split(' ')  # преобразуем в список строк по указанному разделителю - пробелу
    while len(fio_list) < 3:  # до тех пор, пока не наберем 3 элемента добавляем пустые строки
        fio_list.append('')
    return fio_list


def for_phone(item):
    pattern = r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*'
    new_phone = r'+7(\2)-\3-\4-\5 \6\7'
    return re.sub(pattern, new_phone, item)


def duplicates(items):  # ищем дубликаты все (имя+фамилия)
    duplicate = []  # будем складывать в список дубликаты (индексы их)
    # pprint(len(items))   # пересчитаем наши словари
    for i in range(len(items)):  # получаем индексы наших словарей
        for j in range(i, len(items)):  # индексы от i до последнего словаря, чтобы не сравнивать одно и тоже
            # добираемся до значений и сравниваем, сравниваютя (0 индекс i начала со всеми j, затем 1i со всеми j)
            if (items[i]['lastname'], items[i]['firstname']) == (
                    items[j]['lastname'], items[j]['firstname']) and i != j:
                duplicate.append((i, j))  # добавляем в наш список индексы дубликатов
    # print(duplicate)
    for pair in duplicate:  # пошли по парам индексов дубликатов
        # pprint(pair)
        for key in items[0]:  # идем по списку заголовков
            # pprint(key)
            # pprint(items[pair[0]][key])   # это значение pair[0]-ого человека в key столбце
            if not items[pair[0]][key]:  # если по какому-либо из заголовков значение отсутствует
                items[pair[0]][key] = items[pair[1]][key]  # то мы это значение берем из дубликата
            elif not items[pair[1]][key]:  # второй дубликат тоже заполняем значениями из превого
                items[pair[1]][key] = items[pair[0]][key]
    deleted = 0  # счетчик
    for pair in duplicate:
        # pprint(pair)
        # pprint(items[pair[0]])
        del items[pair[0] - deleted]
        deleted += 1
    return items  # возвращает список наших словарей без дублей


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)[1:]  # убрали 0 список с заголовками, чтобы работать с нужным материалом

list_of_dicts = []  # список словарей для склеивания дубликатов
for person in contacts_list:  # цикл по нашему листу, перебираем списки по каждому человеку
    fio = for_fio(person[:3])  # применяем функцию по преобразованию фио
    # pprint(fio)   # исправленные списки фио
    # pprint(person)   # исходные полные списки
    curr_dict = {'lastname': fio[0],
                 'firstname': fio[1],
                 'surname': fio[2],
                 'organization': person[3],
                 'position': person[4],
                 'phone': for_phone(person[5]),  # применяем функцию по преобразованию номеров телефонов
                 'email': person[6]}  # создали словарь по каждому человеку
    # pprint(curr_dict)
    list_of_dicts.append(curr_dict)  # добавляем в список все наши словари
    # pprint(list_of_dicts)   # список словарей по каждому человеку, ключ-описание, значение-данные.
    # pprint(duplicates(list_of_dicts)) # функция возвращает список наших словарей без дублей

columns = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
with open("phonebook.csv", "w") as f:  # write
    datawriter = csv.writer(f, delimiter=',')  # CSV - comma separated values
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(columns)
    huge_list = []  # list(list())
    for curr_dictionary in duplicates(list_of_dicts):
        new_list = [i for i in curr_dictionary.values()]  # ['Наркаев', 'Вячеслав', 'Рифхатович', 'ФНС', '', '+7(495)-913-01-68 ', '']
        huge_list.append(new_list)
    datawriter.writerows(huge_list)
