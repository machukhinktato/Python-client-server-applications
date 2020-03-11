"""Errors"""


# IncorrectDataReceivedError
class UnreadableReceivedDataError(Exception):
    """
    Incorrect data were received from socket
    """
    def __str__(self):
        return 'Invalid message received from a remote computer.'


# ReqFieldMissingError
class RequestedFieldAbsentError(Exception):
    """
    Requested field is absent
    """
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'In accepted dictionary a required field ' \
               f'{self.missing_field} was missed.'
