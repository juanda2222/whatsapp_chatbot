
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
from read_messages_function.main import read_messages_function

class TestWhatsappManager(unittest.TestCase):

    def test_return_stament(self):

        # encode the data the same way gcloud process it:
        data_bytes = "INPUT DATA".encode('utf-8')
        print("data bytes: ", data_bytes)
        data_bytes_64 = base64.b64encode(data_bytes)
        print("data bytes encoded with 64 bits: ", data_bytes_64)

        # create dumb objects as arguments with properties
        test_event = {'data' : data_bytes_64} 
        test_context = type('obj', (object,), {'event_id' : 123456, "timestamp":123345}) 
        return_val = read_messages_function(test_event, test_context)

        # test the return value to see if everything went ok
        self.assertEqual(return_val, True)

    # other tests:
    def test_other(self):
        pass

if __name__ == "__main__":
    unittest.main()