"""client server communication, client side code review"""
import sys
import json
import socket
import time
import argparse
import logging
import logs.config_log_client_side
from shared.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from shared.utilities import get_message, send_message
from shared.errors import RequestedFieldAbsentError
from shared.decorators import LogWriter


CLIENT_SIDE_LOGGER = logging.getLogger('client_side_logger')


def client_initializer():
    """
    Loading param of cmd and do init of socket
    with transfer by result
    """
    parser = argument_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port

    if not 1023 < server_port < 65536:
        CLIENT_SIDE_LOGGER.critical(
            f'attempt to launch client with wrong port: {server_port} '
            f'allowed ports between 1024 and 65535 numbers, process ends'
        )
        sys.exit(1)
    CLIENT_SIDE_LOGGER.info(
        f'client application was launched with parameters: '
        f'server address: {server_addr} '
        f'port: {server_port}'
    )
    try:
        transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transfer.connect((server_addr, server_port))
        confirm_presence_to_server = launch_presence()
        send_message(transfer, confirm_presence_to_server)
        answer = server_response(get_message(transfer))
        CLIENT_SIDE_LOGGER.info(f'received response from server {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_SIDE_LOGGER.error(
            f'failed to decode received Json string'
        )
    except RequestedFieldAbsentError as missing_error:
        CLIENT_SIDE_LOGGER.error(f'in server response has no requested field'
                                 f'{missing_error}{missing_field}')
    except ConnectionRefusedError:
        CLIENT_SIDE_LOGGER.critical(
            f'connection to server is unavailable {server_addr}:{server_port}, '
            f'request to connect was refused'
        )


@LogWriter()
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
    CLIENT_SIDE_LOGGER.debug(f'formed {PRESENCE} message from user {account_name}')
    return out


@LogWriter()
def server_response(request):
    """
    Function to analyze server response
    """
    CLIENT_SIDE_LOGGER.debug(f'analyzing server request: {request} ')
    if RESPONSE in request:
        if request[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {request[ERROR]}'
    raise RequestedFieldAbsentError(RESPONSE)


@LogWriter()
def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, nargs='?')
    return parser


if __name__ == '__main__':
    client_initializer()
