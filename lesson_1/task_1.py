"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить
в строковом формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление
в набор кодовых точек Unicode и также проверить тип и содержимое переменных.

Подсказки:
--- 'разработка' - строковый формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции
"""

TASK_WORDS_LIST = ['разработка', 'сокет', 'декоратор']
UNICODE_LIST = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                '\u0441\u043e\u043a\u0435\u0442',
                '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']


def task(word_list):
    """function to complete a task"""
    for word in word_list:
        if isinstance(word, str):
            encode_list = word.encode('utf-8')
            if word == UNICODE_LIST[0]:
                set_of_code_dots = r'\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
                print(f'{word} - строка, буквенный формат\n'
                      f'байтовый набор = {encode_list} \n'
                      f'{set_of_code_dots} набор кодовых точек \n'
                      f'тип которых = {type(UNICODE_LIST[0])}')
            if word == UNICODE_LIST[1]:
                set_of_code_dots = r'\u0441\u043e\u043a\u0435\u0442'
                print(f'{word} - строка, буквенный формат\n'
                      f'байтовый набор = {encode_list} \n'
                      f'{set_of_code_dots} набор кодовых точек \n'
                      f'тип которых = {type(UNICODE_LIST[1])}')

            if word == UNICODE_LIST[2]:
                set_of_code_dots = r'\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
                print(f'{word} - строка, буквенный формат\n'
                      f'байтовый набор = {encode_list} \n'
                      f'{set_of_code_dots} набор кодовых точек \n'
                      f'тип которых = {type(UNICODE_LIST[2])}')
        else:
            pass  # Задача не требует альтернативных ветвей


task(TASK_WORDS_LIST)
