"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""


def task_4_launcher():
    """function to complete task"""
    task_list = ["разработка", "администрирование", "protocol", "standard"]
    for i in task_list:
        intermediary = i.encode('utf-8')
        print(f'слово {i}, \n'
              f'байтовое представление{intermediary}, \n'
              f'тип= {type(intermediary)}')
        task_list = bytes.decode(intermediary, 'utf-8')
        print(f'по результату декодирования, значение= {task_list}, \n'
              f'тип= {type(task_list)} \n'
              f'кодировка прошла успешно')
        print('\n')


task_4_launcher()
