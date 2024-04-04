""" Final testing """
import unittest
import requests

class Interactiontest(unittest.TestCase):
    """ Testing user-side interaction """
    def test_creating_secretkey(self):
        """ Checking status code and secret key presense for good request """
        prm = {'bsi': 'Hello secrets', 'kp': 'somee'}
        url = 'http://127.0.0.1:8000/generate'
        resp = requests.post(url, json=prm, timeout=2)
        answer = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('secret_key' in answer.keys(), True)

    def test_bad_input(self):
        """ Test status code for error input """
        prm = {'bsi': 1, 'kp': 'somee'}
        prm1 = {'bsi': 'Hello secrets', 'kp': 1}
        prm2 = {'bsi': 'Hello secrets'}
        prm3 = {'kp': 'somee'}
        prm4 = {}
        url = 'http://127.0.0.1:8000/generate'
        for curprm in [prm, prm1, prm2, prm3, prm4]:
            resp = requests.post(url, json=curprm, timeout=2)
            self.assertNotEqual(resp.status_code, 200)

    def test_input_output(self):
        """ Final test equals sending and receiving data """
        prm = {'bsi': 'Hello secrets', 'kp': 'somee'}
        url = 'http://127.0.0.1:8000/generate'
        resp = requests.post(url, json=prm, timeout=2)
        answer = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('secret_key' in answer.keys(), True)
        secret_key = answer['secret_key']
        urlget = f'http://127.0.0.1:8000/secrets/{secret_key}'
        resp = requests.get(urlget, timeout=2)
        answer = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('bsi' in answer.keys(), True)
        self.assertEqual(prm['bsi'], answer['bsi'])
