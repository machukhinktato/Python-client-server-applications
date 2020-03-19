"""client server communication, client side code review"""
import sys
import json
import socket
import time
import argparse
import logging
import logs.config_log_client_side
from shared.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, TIME, USER, ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, \
    ERROR, MESSAGE, MESSAGE_TEXT
from shared.utilities import get_message, send_message
from shared.errors import RequestedFieldAbsentError, ExceptionServerError
from shared.decorators import log

CLIENT_SIDE_LOGGER = logging.getLogger('client_side_logger')


@log
def server_msg_handler(message):
    """
    function - handler of messages from other users, sent from server
    """
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'received message by user '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_SIDE_LOGGER.info(
            f'received message by user '
            f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_SIDE_LOGGER.error(
            f'received incorrect message from server: {message}'
        )


@log
def message_writer(own_socket, account_name='Anonymous'):
    """
    function requests message text and returns him,
    also it may leave program, by necessity
    :param own_socket:
    :param account_name:
    :return formed_dict_to_send:
    """
    message = input('Please, enter message to send'
                    '(to stop process write - exit): ')
    if message == 'exit':
        own_socket.close()
        CLIENT_SIDE_LOGGER.info('program is closed by user request')
        print('Thank you for cooperation with us, see you later!')
        sys.exit(0)
    formed_dict_to_send = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_SIDE_LOGGER.debug(
        f'dictionary was formed {formed_dict_to_send}')
    return formed_dict_to_send


@log
def launch_presence(account_name='Anonymous'):
    """
    Function which generating presence of client
    """
    note_to_server = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_SIDE_LOGGER.debug(
        f'formed {PRESENCE} message from user {account_name}')
    return note_to_server


@log
def server_response(message):
    """
    Function to detect user presence which returns OK or Error
    """
    CLIENT_SIDE_LOGGER.debug(f'analyzing server request: {message} ')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ExceptionServerError(f'400 : {message[ERROR]}')
    raise RequestedFieldAbsentError(RESPONSE)


@log
def argument_parser():
    """
    function to create parser of cmd, reads parameters and return
    three of them
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_SIDE_LOGGER.critical(
            f'attempt to launch client with wrong port number: {server_port}. '
            f'ports allowed from 1024 to 65535, process will be closed'
        )
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_SIDE_LOGGER.critical(
            f'worng work mode defined {client_mode},'
            f'allowed modes: listen, send '
        )
        sys.exit(1)

    return server_addr, server_port, client_mode


def client_initializer():
    """
    Loading param of cmd and do init of socket
    with transfer by result
    """
    server_addr, server_port, client_mode = argument_parser()

    CLIENT_SIDE_LOGGER.info(
        f'client application was launched with parameters: '
        f'server address: {server_addr} '
        f'port: {server_port}, mode: {client_mode}'
    )
    try:
        transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transfer.connect((server_addr, server_port))
        send_message(transfer, launch_presence())
        answer = server_response(get_message(transfer))
        CLIENT_SIDE_LOGGER.info(f'received response from server {answer}')
        print('Сonnection to the server has been established')
    except json.JSONDecodeError:
        CLIENT_SIDE_LOGGER.error(
            f'failed to decode received Json string'
        )
        sys.exit(1)
    except ExceptionServerError as error:
        CLIENT_SIDE_LOGGER.error(
            f'during attempt to connect, server return error: {error.text}'
        )
        sys.exit(1)
    except RequestedFieldAbsentError as missing_error:
        CLIENT_SIDE_LOGGER.error(f'in server response has no requested field'
                                 f'{missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_SIDE_LOGGER.critical(
            f'connection to server is unavailable {server_addr}:{server_port}, '
            f'request to connect was refused'
        )
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Status - preparing to send messages')
        else:
            print('Status - receiving messages')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transfer, message_writer(transfer))
                except (ConnectionResetError, ConnectionError,
                        ConnectionAbortedError):
                    CLIENT_SIDE_LOGGER.error(
                        f'connection with server {server_addr} was lost'
                    )
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    server_msg_handler(get_message(transfer))
                except (ConnectionResetError, ConnectionError,
                        ConnectionAbortedError):
                    CLIENT_SIDE_LOGGER.error(
                        f'connection with server {server_addr} was lost'
                    )
                    sys.exit(1)


if __name__ == '__main__':
    client_initializer()
