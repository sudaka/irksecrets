""" Module for db interconnection """
import os
from pydantic import BaseModel
import psycopg

class Secrets(BaseModel):
    """ 
    curhash: hash of input passphrase 
    enctext: encrypted text
    """
    curhash: str
    enctext: bytes

class Dataconnector():
    """ Manipulating data class """
    dbip: str
    dbport: str
    dbname: str
    dbuname: str
    dbpass: str

    def __init__(self, dbip: str = 'dbhost', dbport: str = '5432',
                 dbname: str = 'irksecrets', dbuname: str = 'irksecrets') -> None:
        """ Init params """
        self.dbip = dbip
        self.dbport = dbport
        self.dbname = dbname
        self.dbuname = dbuname
        self.dbpass = 'qaz123wsx' #os.environ.get('PSQLPASS')

    def exec(self, req: str, params: dict = {}):
        """ 
        Exec sql request 
        Input: req - SQL request, string
        Output: 
            resp - response, tuple or tuple of tuple
            error - True if there are errors
        """
        resp = tuple()
        error = False
        cstr = f'host={self.dbip} port={self.dbport} dbname={self.dbname}'
        cstr += f' user={self.dbuname} password={self.dbpass}'
        try:
            with psycopg.connect(cstr) as conn:
                with conn.cursor() as curr:
                    if params:
                        curr.execute(req, params=params)
                    else:
                        curr.execute(req)
                    if req.strip().lower().startswith('select'):
                        resp = curr.fetchone()
                    else:
                        conn.commit()
        except Exception as e:
            error = True
            #print(str(e))
        return resp, error
    
    def createsecrets(self, newline: Secrets) -> bool:
        """" Create new secret """
        req = """
        insert into secrets (chash, enctext)
        values (%(curhash)s, %(enctext)b);
        """
        params = newline.model_dump()
        _, err = self.exec(req, params=params)
        return err
    
    def deletesecret(self, chash: str) -> bool:
        """ Delete secret by hash """
        req = """
        delete from secrets where chash=%(curhash)s;
        """
        params = {'curhash': chash}
        _, err = self.exec(req, params=params)
        return err
    
    def findsecret(self, chash: str):
        """ Return secret by hash """
        req = """
        select enctext from secrets where chash=%(curhash)s;
        """
        params = {'curhash': chash}
        enctext, _ = self.exec(req, params=params)
        if enctext:
            return enctext[0]
        return b''
    
    def getsecret(self, chash: str):
        """ Return secret by hash and delete if exist """
        enc_b = self.findsecret(chash)
        if enc_b:
            err = self.deletesecret(chash)
            if not err:
                return enc_b
            return b''
        return b''
