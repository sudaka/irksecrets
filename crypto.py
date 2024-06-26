""" Decrypt/encrypt module """
from hashlib import sha256
import random
from cryptography.fernet import Fernet

class Securedata():
    """ Decrypt / encrypt class """
    def encrypt(self, bsi: str, kp: str):
        """ 
        Input: 
            bsi - string for encrypt, 
            kp - string for hashing
        Output: 
            key - decode/encode key, bytes
            curhash - SHA256 hash of kp and random, string
            enctext - encripted bsi, bytes
            error - decode error, bool
        """
        error = False
        try:
            rndstr = str(random.random())
            fullstr = ''.join([kp, rndstr])
            curhash = sha256(fullstr.encode('utf-8')).hexdigest()
            key = Fernet.generate_key()
            f = Fernet(key)
            enctext = f.encrypt(bsi.encode('utf-8'))
        except Exception:
            key = b''
            curhash = ''
            enctext = b''
            error = True
        return key, curhash, enctext, error

    def decrypt(self, key: bytes, enctext: bytes):
        """
        Input:
            key: decode/encode key, bytes
            enctext - encripted bsi, bytes
        Output:
            decoded info, string
            error, False if ok, False if not boolean 
        """
        error = False
        f = Fernet(key)
        try:
            dectext = f.decrypt(enctext)
        except Exception:
            error = True
            dectext = b''
        return dectext.decode('utf-8'), error
