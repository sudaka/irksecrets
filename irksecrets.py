""" Main REST module """
from fastapi import FastAPI
from pydantic import BaseModel
from datastore import Dataconnector, Secrets
from crypto import Securedata

app = FastAPI()

class Inputdata(BaseModel):
    """
    bsi - string for encrypt, 
    kp - string for hashing
    """
    bsi: str
    kp: str

class Secretkey(BaseModel):
    """
    secret_key - string summ hash of kp and key for decode secret
    """
    secret_key: str

@app.post("/generate")
def generatesecret(bsi: str, kp: str):
    """ 
    Input: 
        bsi - string for encrypt, 
        kp - control phase
    Output: 
        secret_key - string join sha256 hash of kp and key for decode secret
    """
    newdata = Inputdata(bsi=bsi, kp=kp)
    out = Secretkey(secret_key='')
    if (isinstance(newdata.bsi, str) and isinstance(newdata.kp, str)):
        m = Securedata()
        key, curhash, enc_bytes, err = m.encrypt(newdata.bsi, newdata.kp)
        if err:
            return out
        d = Dataconnector()
        tst = Secrets(curhash=curhash, enctext=enc_bytes)
        err = d.createsecrets(tst)
        if err:
            return out
        str_key = key.decode('utf-8')
        secret_key = ''.join([curhash, str_key])
        out = Secretkey(secret_key=secret_key)
        return out
    return out
