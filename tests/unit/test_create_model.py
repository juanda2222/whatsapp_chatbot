
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
from create_model import create_model, create_training_data

class TestCreateModel(unittest.TestCase):

    def _test_create_training_data(self):    

        is_created = create_training_data()
        self.assertTrue(is_created)

    def _test_create_model(self):
        is_created = create_model()
        self.assertTrue(is_created)
    
    def tests_do_both(self):
        self._test_create_training_data()
        self._test_create_model()
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()