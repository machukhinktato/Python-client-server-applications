"""decorators"""

import sys
import logging
import inspect
import logs.config_log_client_side
import logs.config_log_server_side


class LogWriter:
    """decorator with logger which detecting on which side he is
    (server|client) and writes programs logs"""
    def __call__(self, function_to_care):
        def writer_hands(*args, **kwargs):
            if sys.argv[0].find('client_side_logger') == -1:
                logger_note = logging.getLogger('server_side_logger')
            else:
                logger_note = logging.getLogger('client_side_logger')
            note = function_to_care(*args, **kwargs)
            logger_note.debug(f'function {function_to_care.__name__} '
                              f'with parameters: {args} and {kwargs}, '
                              f'from module {function_to_care.__module__}, '
                              f'and function {inspect.stack()[1][3]}')
            return note

        return writer_hands
