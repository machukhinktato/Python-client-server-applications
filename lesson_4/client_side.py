"""client server communication, client side code review"""
import sys
import json
import socket
import time
from shared.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from shared.utilities import get_message, send_message


def client_initializer():
    """
    Loading param of cmd and do init of socket
    with transfer by result
    """
    try:
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_addr = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Only a number between 1024 and 65535 can be specified as a port.')
        sys.exit(1)

    transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer.connect((server_addr, server_port))
    confirmation_for_server = launch_presence()
    send_message(transfer, confirmation_for_server)
    try:
        answer = server_response(get_message(transfer))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Failed to decode server message.')


def launch_presence(account_name='Anonymous'):
    """
    Function which generating presence of client
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def server_response(request):
    """
    Function to analyze server response
    """
    if RESPONSE in request:
        if request[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {request[ERROR]}'
    raise ValueError


if __name__ == '__main__':
    client_initializer()
