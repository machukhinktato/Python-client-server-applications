"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml

items_list = ['mouse',
              'keyboard',
              'monitor',
              'computer']
price_dict = {
    'mouse': '10€ - 500€',
    'keyboard': '50€ - 700€',
    'monitor': '150€ - 1000€',
    'computer': '300€ - 10000€'
    }
quantity_var = 5
data_to_yaml = {'items': items_list, 'items_price': price_dict, 'items_quantity': quantity_var}
with open('data_write.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(data_to_yaml, f_n, default_flow_style=False, allow_unicode=True)
with open('data_write.yaml', 'r', encoding='utf-8') as f_n:
    tmp = yaml.load(f_n, Loader=yaml.SafeLoader)
    print(tmp)
