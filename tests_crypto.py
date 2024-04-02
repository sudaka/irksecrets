""" Test cases for crypto module """
import unittest
from crypto import SecureData

class Cryptotests(unittest.TestCase):
    """ Test class """
    def test_simple_encrypt_decrypt(self):
        """ Encrypt, decrypt and check result """
        secret_list = [
            'first',
            'second на русском',
            '!@#$%^&*()'
        ]
        cur_secret_ph = 'asdf'
        for cursec in secret_list:
            m = SecureData()
            key, _, enc_bytes, _ = m.encrypt(cursec, cur_secret_ph)
            dec_cursec = m.decrypt(key, enc_bytes)
            self.assertEqual(cursec, dec_cursec)

    def test_hash_check(self):
        """ Check hash length """
        m = SecureData()
        hashlist = [
            'one',
            'g'*5000,
        ]
        for curh in hashlist:
            _, curhash, _, _ = m.encrypt('one', curh)
            self.assertEqual(len(curhash), 64)

    def test_check_error(self):
        """ Check is error returned when bad data entered """
        