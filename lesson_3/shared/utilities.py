"""utilities"""

import json
from usable.variables import MAX_PACKAGE_LENGTH, ENCODING


def get_message(data):
    """Message receiving and decoding utility
    takes bytes, produces a dictionary,
    if accepted something else gives an error of value"""
    encoded_response = data.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_transporter = encoded_response.decode(ENCODING)
        decoded_response = json.loads(json_transporter)
        if isinstance(decoded_response, dict):
            return decoded_response
        raise ValueError
    raise ValueError


def send_message(socket, message):
    """Message encoding and send utility
    takes message, convert to json format
    and encodes to bytes"""
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    socket.send(encoded_message)
