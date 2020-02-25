"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet
"""
import subprocess
import chardet


def task_5_launcher():
    """function to complete task"""
    ping_data = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]
    for ping_request in ping_data:
        request_made = subprocess.Popen(ping_request, stdout=subprocess.PIPE)
        for call in request_made.stdout:
            encode_var = chardet.detect(call)
            call = bytes.decode(call, encoding=encode_var['encoding']).encode('CP1251')
            call = call.decode('CP1251')
            print(call)


task_5_launcher()
