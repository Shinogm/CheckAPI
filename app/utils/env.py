from dotenv import load_dotenv
import os
load_dotenv()

class Env():
    @staticmethod
    def get(key):
        return os.environ.get(key)
    
    @staticmethod
    def get_secure(key):
        value = Env.get(key)

        if value is None:
            raise Exception(f'Environment variable {key} is not set')
        
        return value