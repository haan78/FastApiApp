from dataclasses import dataclass
from lib.Mongo import Mongo
from FastSession.FastMongoSession import FastMongoSession
import os

class Project:
    _mongo:Mongo  = None
    _session:FastMongoSession = None
    
    settings_:dict = {
        "DBCONN":None,
        "DBNAME":None,
        "SESSIONTIME":None,
        "JWTKEY":None
    }

    @dataclass
    class SettingData:
        DBCONN:str = None
        DBNAME:str = None
        SESSIONTIME:int = 600
        JWTKEY:str = None

    settings:SettingData = None


    def __init__(self) -> None:
        self.settings = self.SettingData()
        for k in self.settings.__annotations__:
            
            v = os.getenv(k)
            t = self.settings.__annotations__[k]
            ##print(k,v,t)
            if v is None:
                raise Exception('ENV '+k+" dose not exist")
            elif t is int:
                self.settings.__setattr__(k,int(v))
            elif t is bool:
                self.settings.__setattr__(k,bool(v))
            else:
                self.settings.__setattr__(k,str(v)) 
                
    
    def Mongo(self,reload:bool = False)->Mongo:
        if self._mongo is None or reload:
            self._mongo = Mongo(self.settings.DBCONN,self.settings.DBNAME)
        
        return self._mongo

    def Session(self,dbname:str = None):
        if self._session is None:
            coll = self.Mongo().db(dbname).get_collection("session")
            self._session =  FastMongoSession(  collection=coll,timeout=int(self.settings.SESSIONTIME) )
        
        return self._session
