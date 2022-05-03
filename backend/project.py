#from dataclasses import dataclass
#from mimetypes import init
from lib.Mongo import Mongo
from lib.ENV import ENV
from FastSession.FastMongoSession import FastMongoSession

class Project:
    _mongo:Mongo  = None
    _session:FastMongoSession = None

    class SettingData:
        DBCONN:str
        DBNAME:str
        SESSIONTIME:int
        JWTKEY:str

        def __init__(self) -> None:
            self.DBCONN:str = ENV("DBCONN",str)
            self.DBNAME:str = ENV("DBNAME",str)
            self.SESSIONTIME:int = ENV("SESSIONTIME",int,False,500)
            self.JWTKEY:str = ENV("JWTKEY",str)


    settings:SettingData = None


    def __init__(self) -> None:
        self.settings = self.SettingData()
                
    
    def Mongo(self,reload:bool = False)->Mongo:
        if self._mongo is None or reload:
            self._mongo = Mongo(self.settings.DBCONN,self.settings.DBNAME)
        
        return self._mongo

    def Session(self,dbname:str = None):
        if self._session is None:
            coll = self.Mongo().db(dbname).get_collection("session")
            self._session =  FastMongoSession(  collection=coll,timeout=int(self.settings.SESSIONTIME) )
        
        return self._session
