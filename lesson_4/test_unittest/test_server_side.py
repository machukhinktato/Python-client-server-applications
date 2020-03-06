"""Server unittest"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from shared.variables import RESPONSE, ERROR, USER,\
    ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server_side import analyzer


class TestServer(unittest.TestCase):
    """provides unittest checking for server"""
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def test_action_absence(self):
        """Error if there is no cation"""
        self.assertEqual(analyzer(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Anonymous'}}),
            self.err_dict)

    def test_wrong_action(self):
        """Error if action wasn't defined"""
        self.assertEqual(analyzer(
            {ACTION: 'Wrong', TIME: '1.1', USER: {
                ACCOUNT_NAME: 'Anonymous'}}), self.err_dict)

    def test_time_not_defined(self):
        """Error if request has no stamp of time"""
        self.assertEqual(analyzer(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Anonymous'}}),
            self.err_dict)

    def test_user_not_defined(self):
        """Error - user wasn't set"""
        self.assertEqual(analyzer(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_incorrect_user(self):
        """Error - not Anonymous"""
        self.assertEqual(analyzer(
            {ACTION: PRESENCE, TIME: 1.1, USER:
                {ACCOUNT_NAME: 'Anonymous1'}}), self.err_dict)

    def test_correct_request(self):
        """Correct request"""
        self.assertEqual(analyzer(
            {ACTION: PRESENCE, TIME: 1.1, USER:
                {ACCOUNT_NAME: 'Anonymous'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
