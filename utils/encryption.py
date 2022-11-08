import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from cryptography.fernet import Fernet

from utils.globals import PICKLE_ENC

class Encryption:
    def __init__(self, key):
        self.key = self.get_key(key.encode())
    
    @staticmethod
    def encrypted_key() -> str:
        encryptor = Fernet(PICKLE_ENC.encode())
        # Create key
        key = Fernet.generate_key()

        return encryptor.encrypt(key).decode()
            
    def get_key(self, key):
        decryptor = Fernet(PICKLE_ENC.encode())
        return decryptor.decrypt(key)
    
    def encrypt(self, string: str or int):
        encryptor = Fernet(self.key)
        encrypted_string = encryptor.encrypt(str(string).encode())

        return encrypted_string.decode()
        
    
    def decrypt(self, string: str):
        if string == None: return string
        decryptor = Fernet(self.key)
        decrypted_string = decryptor.decrypt(string.encode()).decode()
        return decrypted_string
    
    @staticmethod
    def key_encryptor():
        return Fernet(PICKLE_ENC.encode())