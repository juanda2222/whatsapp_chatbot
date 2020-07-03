
import sys
import os
import base64
from pathlib import Path
import unittest
import json


# generate the os independent path string
FUNCTION_PATH = str(Path(__file__).parent.parent)

# append the functions path to the search path
sys.path.append(FUNCTION_PATH)
# import the functions to test
# form <folder>.<file> import <function
from read_messages_function.chatbotManager import TextProcessor, input_convert_text2binary, output_convert_binary2text

class TestChatbot(unittest.TestCase):

    # other tests:
    def test_ai_io_formatting(self):

        # test the converters one at the time
        print("Testing input formatting...")
        DICTIONARY_LENGTH = 200 # this should be imported from the ai module
        binnary_input = input_convert_text2binary("Are you open?", show_details=True)
        self.assertTrue( len(binnary_input[0]) == DICTIONARY_LENGTH ) # pass if true
        
        print("Testing output formatting...")
        # import our chat-bot intents file
        INTENTS_FILE_PATH = (Path(__file__).parent.parent / "read_messages_function/intents.json").absolute()
        with open(INTENTS_FILE_PATH) as json_data:
            intents = json.load(json_data)
        # compare the size with the output file
        tagged_output = output_convert_binary2text([0,0.9,0,0,0,1,0,0.3,0], show_details=True)
        self.assertTrue(len(tagged_output) == len(intents["intents"])) # pass if true
        self.assertTrue(len(tagged_output[0]) == 2) # check the items to be a tuple with size 2
        self.assertTrue(type(tagged_output[0][1]) == str) # check second in the tuple to be string

    def test_text_processor(self):

        print("Loading chatbot...")
        chatBot = TextProcessor()
        question = "hello! how r you?"
        response = chatBot.response(question)
        print("Question: ", question)
        print("Response", response)
        # test the return value to see if everything went ok
        self.assertEqual(type(response), str)


if __name__ == "__main__":
    unittest.main()