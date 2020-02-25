"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""
import sys


def task_2_launcher():
    """ function to complete a task"""
    task_list = [b"class", b"function", b"method"]
    for text in task_list:
        print(f'байтовый формат написания слова {text} {list(text)} \n'
              f'тип содержимого относится к {type(text)} \n'
              f'длина которого состовляет {len(text)} символов \n'
              f'занимается {sys.getsizeof(text)} байт в памяти\n'
              f'\n')


task_2_launcher()
