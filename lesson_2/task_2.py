"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "printer",
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""
import json


def write_orders_to_json(item, quantity, price, buyer, date):
    """ function to write orders in json file"""
    with open('orders.json', 'r', encoding='utf-8') as forming:
        data = json.load(forming)

    with open('orders.json', 'w', encoding='utf-8') as filling:
        orders_list = data['orders']
        order_info = {
            "item": item,
            "quantity": quantity,
            "price": price,
            "buyer": buyer,
            "date": date
        }
        orders_list.append(order_info)
        json.dump(data, filling, indent=4, ensure_ascii=False)

    with open('orders.json', 'r', encoding='utf-8') as record_output:
        print(record_output.read())


write_orders_to_json('macbook', '1', '1000$', 'Tarabrin', '23.10.2020')
write_orders_to_json('макбук', '2', '2000$', 'Тарабрин', '23.10.2020')
write_orders_to_json('самый крутой и большой комп', '1', '1000$', 'Котова', '23.10.2020')
