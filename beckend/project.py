from dotenv import load_dotenv
from pathlib import Path
from lib.Mongo import Mongo
from FastSession.FastMongoSession import FastMongoSession
import os

class Project:
    _mongo:Mongo  = None
    _session:FastMongoSession = None
    
    settings:dict = {
        "DBCONN":None,
        "DBNAME":None,
        "SESSIONTIME":None
    }

    def __init__(self,envfile = ".env") -> None:
        dotenv_path = Path(envfile)
        load_dotenv(dotenv_path=dotenv_path)

        for k in self.settings.keys():
            v = os.getenv(k)
            if v is None:
                raise Exception('ENV '+k+" dose not exist")
            else:
                self.settings[k] = v
    
    def Mongo(self,reload:bool = False)->Mongo:
        if self._mongo is None or reload:
            self._mongo = Mongo(self.settings["DBCONN"],self.settings["DBNAME"])
        
        return self._mongo

    def Session(self,dbname:str = None):
        if self._session is None:
            coll = self.Mongo().db(dbname).get_collection("session")
            self._session =  FastMongoSession(  collection=coll,timeout=int(self.settings["SESSIONTIME"]) )
        
        return self._session
