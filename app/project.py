import uvicorn
from fastapi import FastAPI
from lib.FastLib import FastLib
from fastapi.staticfiles import StaticFiles
from FastSession.FastMongoSession import FastMongoSession
from lib.Mongo import Mongo
from dotenv import load_dotenv
from pathlib import Path
import os

class Project:
    data: Mongo = None
    session: FastMongoSession = None
    lib: FastLib = None
    port: int
    _app: FastAPI = None

    settings:dict = {
        "JWTKEY":None,
        "DBCONN":None,
        "DBNAME":None,
        "PORT":None,
        "SESSIONTIME":None
    }

    def __init__(self,envfile = ".env") -> None:
        self._loadEnv(envfile=envfile)
        self.data = Mongo(self.settings["DBCONN"],self.settings["DBNAME"])
        self.lib = FastLib(self.settings["JWTKEY"])
        self.session = FastMongoSession( self.data.colletion("session"),timeout=int(self.settings["SESSIONTIME"]) )
        self.port = int( self.settings["PORT"] )
        
    
    def getApp(self)->FastAPI:
        if ( self._app is None ):
            self._app = FastAPI()
            self._app.mount("/static", StaticFiles(directory="static"), name="static")
            self._app.mount("/jsdist", StaticFiles(directory="jsdist"), name="jsdist")

        return self._app

    def _loadEnv(self, envfile:str):
        dotenv_path = Path(envfile)
        load_dotenv(dotenv_path=dotenv_path)

        for k in self.settings.keys():
            v = os.getenv(k)
            if v is None:
                raise Exception('ENV '+k+" dose not exist")
            else:
                self.settings[k] = v
    
    def run(self):
        if self._app is not None:
            uvicorn.run(self._app, host="0.0.0.0", port=self.port)
        else:
            raise 'Server has been not started!'
