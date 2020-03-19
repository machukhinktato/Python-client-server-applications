"""debugger launcher"""

import subprocess

PROCESS = []

while True:
    ACTION = input('please, choose the options: '
                   's - launch server, '
                   'x - close all windows, '
                   'q - quit program: ')
    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen(
            'python server_side.py',
            creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen(
            'python client_side.py -n 1',
            creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen(
            'python client_side.py -n 2',
            creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen(
            'python client_side.py -n 3',
            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            SACRIFICE = PROCESS.pop()
            SACRIFICE.kill()
