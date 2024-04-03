""" Test cases for crypto module """
import unittest
from datastore import Dataconnector, Secrets
from crypto import Securedata

class Datastoretests(unittest.TestCase):
    """Main class"""
    def test_connection(self):
        """Test connection and table presense"""
        d = Dataconnector()
        req = """
        select tableowner from pg_catalog.pg_tables 
        where tablename='secrets';
        """
        dt, err = d.exec(req)
        self.assertGreater(len(dt), 0)
        self.assertEqual(err, False)

    def test_param_req(self):
        """Test param request"""
        req = """
        select tableowner from pg_catalog.pg_tables 
        where tablename=%(tablename)s;
        """
        d = Dataconnector()
        params = {'tablename': 'secrets'}
        dt, err = d.exec(req, params=params)
        self.assertGreater(len(dt), 0)
        self.assertEqual(err, False)

    def test_insert(self):
        """ Test insert & delete data """
        d = Dataconnector()
        tst = Secrets(curhash='fff', enctext=b'jkl')
        err = d.createsecrets(tst)
        self.assertEqual(err, False)
        if not err:
            err = d.deletesecret(tst.curhash)
            self.assertEqual(err, False)

    def test_ok_search_by_hash(self):
        """ Test elem existed """
        d = Dataconnector()
        tst = Secrets(curhash='fff', enctext=b'jkl')
        err = d.createsecrets(tst)
        if not err:
            enctext = d.findsecret(tst.curhash)
            self.assertEqual(enctext, tst.enctext)
            _ = d.deletesecret(tst.curhash)

    def test_empty_search_by_hash(self):
        """ Test elem not existed """
        d = Dataconnector()
        enc_bytes = d.findsecret('dfd')
        self.assertEqual(enc_bytes, b'')

    def test_input_str_key_storing_get(self):
        """ Test encoding, save, decoding """
        m = Securedata()
        cursec = 'first sec'
        cur_secret_ph = 'key phase'
        key, curhash, enc_bytes, err = m.encrypt(cursec, cur_secret_ph)
        self.assertEqual(err, False)
        d = Dataconnector()
        tst = Secrets(curhash=curhash, enctext=enc_bytes)
        err = d.createsecrets(tst)
        self.assertEqual(err, False)
        enc_b = d.getsecret(curhash)
        dec_cursec, _ = m.decrypt(key, enc_b)
        self.assertEqual(cursec, dec_cursec)
