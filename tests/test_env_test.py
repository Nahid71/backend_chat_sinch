import os
import unittest
from dotenv import load_dotenv

load_dotenv() 

class TestAuthorizations(unittest.TestCase):
    
        
    def test_status_codes_200(self):
        print("Start pringing env varialbes")
        openai_key = os.getenv('OPENAI_KEY')
        print(os.getenv('OPENAI_KEY'))
        print(os.getenv('SECRET_KEY_FRONT'))
        print(os.getenv('ALGORITHM'))
        print(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
        self.assertEqual(openai_key, "demo_OPENAI_KEY")

    

        