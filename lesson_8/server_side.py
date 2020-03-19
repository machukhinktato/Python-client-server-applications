"""
client server communication, server side code review
"""
import socket
import sys
import json
import argparse
import logging
import select
import time
import logs.config_log_server_side
from shared.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, TIME, USER, \
    ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT
from shared.utilities import get_message, send_message
from shared.errors import UnreadableReceivedDataError
from shared.decorators import log

SERVER_SIDE_LOGGER = logging.getLogger('server_side_logger')


@log
def analyzer(client_message, message_list, client):
    """
    A message handler from clients that accepts a dictionary -
    message from the client, checks the correctness, returns a
    response dictionary for a client
    """
    SERVER_SIDE_LOGGER.debug(f'analyze of client message {client_message}')
    if ACTION in client_message and client_message[ACTION] == PRESENCE \
            and TIME in client_message and USER in client_message \
            and client_message[USER][ACCOUNT_NAME] == 'Anonymous':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in client_message and client_message[ACTION] == MESSAGE and \
            TIME in client_message and MESSAGE_TEXT in client_message:
        message_list.append((client_message[ACCOUNT_NAME], client_message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def argument_parser():
    """
    parsing arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    addr_to_listen = namespace.a
    port_to_listen = namespace.p

    if not 1023 < port_to_listen < 65536:
        SERVER_SIDE_LOGGER.critical(
            f'attempt to launch server with wrong port '
            f'{port_to_listen}, allowed ports from 1024 to 65535.'
        )
        sys.exit(1)

    return addr_to_listen, port_to_listen


def server_launcher():
    """
    loading params of cmd, if they're not set,
    will defined by default, after that function detects
    addr which will be listen, prepares port and
    starts to receive a information
    """
    addr_to_listen, port_to_listen = argument_parser()

    SERVER_SIDE_LOGGER.info(
        f'server launched, port to connect: {port_to_listen} '
        f'connection from address: {addr_to_listen} '
        f'(If address not defined, connection will be available without it)'
    )

    transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer.bind((addr_to_listen, port_to_listen))
    transfer.settimeout(0.5)
    clients_online = []
    messages_queue = []
    transfer.listen(MAX_CONNECTIONS)

    while True:
        try:
            client_socket_box, addr_to_listen = transfer.accept()
        except OSError:
            pass
        else:
            SERVER_SIDE_LOGGER.info(f'connection with PC {addr_to_listen} stabilized')
            clients_online.append(client_socket_box)

        data_list_for_receiving = []
        data_list_to_send = []
        data_list_of_err_occured = []

        try:
            if clients_online:
                data_list_for_receiving, data_list_to_send, data_list_of_err_occured = \
                    select.select(clients_online, clients_online, [], 0)
        except OSError:
            pass
        if data_list_for_receiving:
            for msg_by_client in data_list_for_receiving:
                try:
                    analyzer(get_message(msg_by_client),
                             messages_queue, msg_by_client)
                except:
                    SERVER_SIDE_LOGGER.info(f'client {msg_by_client.getpeername()} '
                                            f'disconnected from server')
                    clients_online.remove(msg_by_client)
        if messages_queue and data_list_to_send:
            message = {
                ACTION: MESSAGE,
                SENDER: messages_queue[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages_queue[0][1]
            }
            del messages_queue[0]
            for client_from_queue in data_list_to_send:
                try:
                    send_message(client_from_queue, message)
                except:
                    SERVER_SIDE_LOGGER.info(f' client {client_from_queue.getpeername()} '
                                            f'disconnected from server')
                    clients_online.remove(client_from_queue)


if __name__ == '__main__':
    server_launcher()
