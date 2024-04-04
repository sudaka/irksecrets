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

class Secretphase(BaseModel):
    """
    bsi - secret string
    """
    bsi: str

@app.post("/generate", response_model=Secretkey)
#def generatesecret(bsi: str, kp: str):
def generatesecret(curd: Inputdata):
    """ 
    Input: 
        bsi - string for encrypt, 
        kp - control phase
    Output: 
        secret_key - string join sha256 hash of kp+random and key for decode secret
    """
    newdata = Inputdata(bsi=curd.bsi, kp=curd.kp)
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

@app.get('/secrets/{secret_key}', response_model=Secretphase)
def getsecret(secret_key: str):
    """
    Input: 
        secret_key - string join sha256 hash of kp and key for decode secret
    Output: 
        bsi - string for encrypt
    """
    out = Secretphase(bsi='')
    if isinstance(secret_key, str) and len(secret_key) > 64:
        curhash = secret_key[:64]
        keystr = secret_key[64:]
        print(curhash)
        print(keystr)
        key = keystr.encode('utf-8')
        d = Dataconnector()
        m = Securedata()
        enc_b = d.getsecret(curhash)       
        dec_cursec, err = m.decrypt(key, enc_b)
        if err:
            return out
        return Secretphase(bsi=dec_cursec)
    else:
        return out
