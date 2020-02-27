"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import re
# import chardet

HEADER = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
FILES = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def task_1():
    """function creating dict for write and get data"""
    os_prod_list = list()
    os_name_list = list()
    os_code_list = list()
    os_type_list = list()
    main_data = [HEADER]
    looking_for = [r'Изготовитель системы:\s', r'Название ОС:\s',
                   r'Код продукта:\s', r'Тип системы:\s']
    for file in FILES:
        with open(file, 'rb') as tmp_f:
            for line in tmp_f.readlines():
                # с поиском кодировки не заполняется файл
                # encoding = chardet.detect(line)
                # print(encoding)
                # line = bytes.decode(line, encoding=encoding['encoding']).\
                #     encode('utf-8').decode('utf-8')
                # при тестировании не забыть импортировать chardet
                line = bytes.decode(line, encoding='cp1251'). \
                    encode('utf-8').decode('utf-8')
                for counter, reg_ex in enumerate(looking_for):
                    found_string = re.search(reg_ex, line)
                    if found_string is not None and counter == 0:
                        found_string = re.split(r'\W{2,}', line)
                        os_prod_list.append(found_string[1])
                    if found_string is not None and counter == 1:
                        found_string = re.split(r'\W{2,}', line)
                        os_name_list.append(found_string[1])
                    if found_string is not None and counter == 2:
                        found_string = re.split(r'\W{2,}', line)
                        os_code_list.append(found_string[1])
                    if found_string is not None and counter == 3:
                        found_string = re.split(r'\W{2,}', line)
                        os_type_list.append(found_string[1])
    for counter in range(len(os_prod_list)):
        tmp_list = [os_prod_list[counter], os_name_list[counter],
                    os_code_list[counter], os_type_list[counter]]
        main_data.append(tmp_list)
    return main_data


def task_1_launcher(file_obj):
    """Function to save dict in file csv format"""
    with open(file_obj, 'w', encoding='utf-8') as f_writer:
        f_writer = csv.writer(f_writer, quoting=csv.QUOTE_ALL)
        for row in task_1():
            f_writer.writerow(row)


task_1_launcher('main_data.csv')
print('Программа выполнена')
