"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но отерыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""
from chardet import detect


def task_6():
    """function to complete task"""
    task_list = ['сетевое программирование', 'сокет', 'декоратор']
    with open('task_6.txt', 'w') as f_obj:
        print(*task_list, file=f_obj, sep='\n')
        print(f_obj)
    with open('task_6.txt', 'rb') as f_obj:
        content_bytes = f_obj.read()
    detected = detect(content_bytes)
    encoding = detected['encoding']
    content_text = content_bytes.decode(encoding)
    with open('task_6.txt', 'w', encoding='utf-8') as f_obj:
        f_obj.write(content_text)
    with open('task_6.txt', encoding='utf-8') as f_obj:
        for line in f_obj:
            print(line)


task_6()
