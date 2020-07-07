
import sys
import os
import base64
from pathlib import Path
import unittest
import json

import requests





class TestIntegrationMessageReceived(unittest.TestCase):

    # other tests:
    def test_public_call__on_message_received(self):

        # test the converters one at the time
        url = 'https://www.w3schools.com/python/demopage.php'
        myobj = {'somekey': 'somevalue'}

        x = requests.post(url, data = myobj)

        print(x.text)
    
if __name__ == "__main__":
    unittest.main()