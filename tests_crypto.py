""" Test cases for crypto module """
import unittest
from crypto import Securedata

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
            m = Securedata()
            key, _, enc_bytes, _ = m.encrypt(cursec, cur_secret_ph)
            dec_cursec, _ = m.decrypt(key, enc_bytes)
            self.assertEqual(cursec, dec_cursec)

    def test_hash_check(self):
        """ Check hash length """
        m = Securedata()
        hashlist = [
            'one',
            'g'*5000,
        ]
        for curh in hashlist:
            _, curhash, _, _ = m.encrypt('one', curh)
            self.assertEqual(len(curhash), 64)

    def test_check_encrypt_error(self):
        """ Check is error returned when bad data in encrypt entered """
        m = Securedata()
        key, curhash, enc, err = m.encrypt(1, 1)
        self.assertEqual(key, b'')
        self.assertEqual(curhash, '')
        self.assertEqual(enc, b'')
        self.assertEqual(err, True)

    def test_check_decrypt_error(self):
        """ Check is error returned when bad data in decrypt entered """
        m = Securedata()
        _, _, enc, _ = m.encrypt('1', '1')
        key = b'Izy02bdCKPYA-uoUKeDs54UjZw41GmF3RmXoVCk65L4='
        dec_cursec, err = m.decrypt(key, enc)
        self.assertEqual(dec_cursec, '')
        self.assertEqual(err, True)

    def test_check_string_transform(self):
        """ Check correct transform bytes to str """
        m = Securedata()
        key, _, enc, _ = m.encrypt('asdf', 'jk;l')
        newstr = enc.decode('utf-8')
        newbytes = newstr.encode('utf-8')
        dec_cursec, _ = m.decrypt(key, newbytes)
        self.assertEqual('asdf', dec_cursec)
