
import sys
import os
import base64
from pathlib import Path
import unittest


# generate the os independent path string
FUNCTION_PATH = str(Path(__file__).parent.parent)

# append the functions path to the search path
sys.path.append(FUNCTION_PATH)
# import the functions to test
# form <folder>.<file> import <function
from whatsManager import read_messages, send_message, secrets_json

class TestWhatsappManager(unittest.TestCase):

    def test_send_whatsapp(self):

        # encode the data the same way gcloud process it:
        is_done = send_message("Test message", secrets_json["test_number"], show_details = True)

        # test the return value to see if everything went ok
        self.assertEqual(is_done, True)

    # other tests:
    def test_read_whatsapps(self):

        # encode the data the same way gcloud process it:
        message_list = read_messages(show_details = True)

        # test the return value to see if everything went ok
        self.assertEqual(type(message_list[0]), str)

if __name__ == "__main__":
    unittest.main()