"""
3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b''.

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- Попробуйте усложнить задачу, "отлавливая" и обрабатывая исключение
"""


def task_3_launcher():
    """function to compelte task"""
    task_list = ["attribute", "класс", "функция", "type"]
    for word in task_list:
        try:
            print(f'слово записано в байтовом типе:', eval(f'b"{word}"'))
        except SyntaxError:
            print(f'слово {word} не возможно записать в байтовом варианте')


task_3_launcher()

# task_3.py:16:80: W0123: Use of eval (eval-used) не знаю как пофиксить
