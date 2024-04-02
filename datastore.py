""" Module for db interconnection """
import os
from pydantic import BaseModel

class Secrets(BaseModel):
    """ 
    curhash: hash of input passphrase 
    enctext: encrypted text
    """
    curhash: str
    enctext: bytes

class Dataconnector():
    """ Manipulating data class """
    dbip: str = '127.0.0.1'
    dbport: str = ''
    dbname: str = 'irksecrets'
    dbpass: str

    def __init__(self) -> None:
        """ Init params """
        self.dbpass = os.environ.get('PSQLPASS')
