
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
from createModel import create_model, create_training_data

class TestCreateModel(unittest.TestCase):

    def _test_create_training_data(self):    

        is_created = create_training_data()
        self.assertTrue(is_created)

    def _test_create_model(self):
        is_created = create_model()
        self.assertTrue(is_created)
    
    def do_both_tests(self):
        self._test_create_training_data()
        self._test_create_model()
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()