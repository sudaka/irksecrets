""" Decrypt/encrypt module """
from hashlib import sha256
from cryptography.fernet import Fernet

class SecureData():
    """ Decrypt / encrypt class """
    def encrypt(self, bsi: str, kp: str):
        """ 
        Input: 
            bsi - string for encrypt, 
            kp - string for hashing
        Output: 
            key - decode/encode key, bytes
            curhash - SHA256 hash of kp, string
            enctext - encripted bsi, bytes
        """
        error = False
        try:
            curhash = sha256(kp.encode('utf-8'), usedforsecurity=False).hexdigest()
            key = Fernet.generate_key()
            f = Fernet(key)
            enctext = f.encrypt(bsi.encode('utf-8'))
        except Exception as e:
            key = b''
            curhash = b''
            enctext = b''
            error = e
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
        except Exception as e:
            error = e
            dectext = b''
        return dectext.decode('utf-8'), error

if __name__ == '__main__':
    m = SecureData()
    '''
    k, c, e = m.encrypt('dsdкецу', 'aasdfasdfasdf')
    print(type(c))
    print(e)
    k = b'lXlAUao_diba6Ifyj5hDr7ntuaUtzhXLCDcVQ6IL8b0='
    e = b'gAAAAABmC7WFfDE6qSbq1T1uOruloctUY-K-k6DdFT4cE_KCI_4KZ40NAHPXeFdHaW5x6fKLHsQ3aBsWZF6TQV4G8PvY2ofYDw=='
    out = m.decrypt(k, e)
    print(type(out), out)
    '''
