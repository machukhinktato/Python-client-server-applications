"""
client server communication, server side code review
"""
import socket
import sys
import json
import argparse
import logging
import logs.config_log_server_side
from shared.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from shared.utilities import get_message, send_message
from shared.errors import UnreadableReceivedDataError
from shared.decorators import LogWriter


SERVER_SIDE_LOGGER = logging.getLogger('server_side_logger')


def server_launcher():
    """
    loading params of cmd, if they're not set,
    will defined by default, after that function detects
    addr which will be listen, prepares port and
    starts to receive a information
    """
    parser = argument_parser()
    namespace = parser.parse_args(sys.argv[1:])
    addr_data = namespace.a
    port_data = namespace.p
    if not 1023 < port_data < 65536:
        SERVER_SIDE_LOGGER.critical(
            f'port was defined incorrectly {port_data} '
            f'port address range available between 1024 and 65535'
        )
        sys.exit(1)
    SERVER_SIDE_LOGGER.info(
        f'server launched, port to connect: {port_data} '
        f'connection from address: {addr_data} '
        f'(If address not defined, connection will be available without it)'
    )

    transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer.bind((addr_data, port_data))
    transfer.listen(MAX_CONNECTIONS)

    while True:
        client_socket_box, client_addr = transfer.accept()
        SERVER_SIDE_LOGGER.info(f'connection with {client_addr} stabilized')
        try:
            message_receiver = get_message(client_socket_box)
            SERVER_SIDE_LOGGER.debug(f'message received: {message_receiver}')
            response = analyzer(message_receiver)
            SERVER_SIDE_LOGGER.info(f'response is ready to sent: {response}')
            send_message(client_socket_box, response)
            SERVER_SIDE_LOGGER.debug(f'connection with client {client_addr} will be closed')
            client_socket_box.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_SIDE_LOGGER.error(
                f'json file, received from {client_addr} '
                f'was unavailable to decode. Connection will be closed')
            client_socket_box.close()
        except UnreadableReceivedDataError:
            SERVER_SIDE_LOGGER.error(f'message format from {client_addr} is unreadable'
                                     f'the connection will be closed')


@LogWriter()
def analyzer(client_message):
    """
    A message handler from clients that accepts a dictionary -
    message from the client, checks the correctness, returns a
    response dictionary for a client
    """
    SERVER_SIDE_LOGGER.debug(f'analyze of client message {client_message}')
    if ACTION in client_message and client_message[ACTION] == PRESENCE \
            and TIME in client_message and USER in client_message \
            and client_message[USER][ACCOUNT_NAME] == 'Anonymous':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@LogWriter()
def argument_parser():
    """
    parsing arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


if __name__ == '__main__':
    server_launcher()
