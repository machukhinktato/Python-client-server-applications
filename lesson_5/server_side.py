"""
client server communication, server side code review
"""
import socket
import sys
import json
from shared.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from shared.utilities import get_message, send_message


def server_launcher():
    """
    loading params of cmd, if they're not set,
    will defined by default, after that function detects
    addr which will be listen, prepares port and
    starts to receive a information
    """
    try:
        if '-p' in sys.argv:
            port_data = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port_data = DEFAULT_PORT
        if port_data < 1024 or port_data > 65535:
            raise ValueError
    except IndexError:
        print('After the parameter -\'p\' must be specified the port'
              ' number.')
        sys.exit(1)
    except ValueError:
        print('Only a number between 1024 and 65535 can be specified'
              ' as a port.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            addr_data = sys.argv[sys.argv.index('-a') + 1]
        else:
            addr_data = ''

    except IndexError:
        print('After the parameter \'a\'- must be specified the address'
              ' that the server will listen to.')
        sys.exit(1)

    transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer.bind((addr_data, port_data))
    transfer.listen(MAX_CONNECTIONS)

    while True:
        client_socket_box, client_addr = transfer.accept()
        try:
            message_receiver = get_message(client_socket_box)
            print(message_receiver)
            response = analyzer(message_receiver)
            send_message(client_socket_box, response)
            client_socket_box.close()
        except (ValueError, json.JSONDecodeError):
            print('Incorrect message was received from client side')
            client_socket_box.close()


def analyzer(client_message):
    """
    A message handler from clients that accepts a dictionary -
    message from the client, checks the correctness, returns a
    response dictionary for a client
    """
    if ACTION in client_message and client_message[ACTION] == PRESENCE \
            and TIME in client_message and USER in client_message \
            and client_message[USER][ACCOUNT_NAME] == 'Anonymous':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


if __name__ == '__main__':
    server_launcher()
