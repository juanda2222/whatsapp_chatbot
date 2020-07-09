
import sys
import os
import base64
from pathlib import Path
import unittest


# generate the os independent path string
PROJECT_PATH = str(Path(__file__).parent.parent.parent)

# append the functions path to the search path
sys.path.append(PROJECT_PATH)
# import the functions to test
# form <folder>.<file> import <function
from on_message_received.main import on_message_received

class TestCloudFunction(unittest.TestCase):

    def test_post_return_stament(self):

        # encode the data the same way gcloud process it:
        test_request_method = "POST"
        print("Test request method: ", test_request_method)
        test_request_headers = {"content-type" : 'text/html; charset=utf-8'}
        print("Test request headers: ", test_request_headers)
        test_request_data = {'some_tag' : "this is the data"} 
        print("Test request data: ", test_request_data)

        # create dumb objects as arguments with properties
        test_request = type('obj', (object,), {
            "method" : test_request_method, 
            "headers": test_request_headers,
            "data": test_request_data,
            "get_json": lambda x: {"some_json_tag":"some_json_data"}
            })

        return_val = on_message_received(test_request)

        # test the return value to see if everything went ok
        self.assertEqual(True, True)

    # other tests:
    def test_other(self):
        pass

if __name__ == "__main__":
    unittest.main()